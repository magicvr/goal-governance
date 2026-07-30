#!/usr/bin/env python3
"""Run a host entrypoint probe and write replayable runtime evidence."""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ID = "https://github.com/magicvr/goal-governance/schema/runtime-evidence/v1"
FORMAT = "goal-governance.host-runtime-evidence"
CLAUDE_STREAM_MODE = "claude-stream-json-sanitized"
REQUEST_URL_REDACTED_MODE = "request-url-redacted"


class CaptureError(ValueError):
    """Raised when a requested probe cannot produce valid evidence."""


def _sha256_bytes(value: bytes) -> str:
    return sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _sha256_repo_text(path: Path) -> str:
    """Hash text the way git stores it under text eol=lf (.gitattributes)."""
    return _sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def _repo_file(root: Path, value: str, label: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise CaptureError(f"{label} must stay inside the repository: {value}")
    root = root.resolve()
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise CaptureError(f"{label} must stay inside the repository: {value}") from error
    if not resolved.is_file():
        raise CaptureError(f"{label} is missing: {value}")
    return resolved


def _normalize_command(command: list[str]) -> list[str]:
    if not command:
        raise CaptureError("probe command is empty")
    normalized = list(command)
    executable = Path(normalized[0]).name.lower()
    if executable in {"python.exe", "python3.exe"} or executable.startswith("python"):
        normalized[0] = "python"
    return normalized


def _timeout_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _safe_tool_metadata(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    allowed = {
        "countIsComplete",
        "durationMs",
        "filenames",
        "numFiles",
        "numLines",
        "startLine",
        "totalLines",
        "totalMatches",
        "truncated",
    }
    return {key: value[key] for key in sorted(allowed & set(value))}


def _sanitize_claude_stream(value: str) -> str:
    transcript: list[dict[str, Any]] = []
    for line_number, line in enumerate(value.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            transcript.append(
                {
                    "event": "unparseable-line",
                    "line": line_number,
                    "length": len(line),
                    "sha256": _sha256_bytes(line.encode("utf-8")),
                }
            )
            continue
        event_type = event.get("type")
        if event_type == "system" and event.get("subtype") == "init":
            transcript.append(
                {
                    "event": "session-init",
                    "sessionId": event.get("session_id"),
                    "cwd": event.get("cwd"),
                    "tools": event.get("tools", []),
                    "model": event.get("model"),
                    "permissionMode": event.get("permissionMode"),
                    "slashCommands": event.get("slash_commands", []),
                    "claudeCodeVersion": event.get("claude_code_version"),
                }
            )
            continue
        if event_type == "assistant":
            message = event.get("message")
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    transcript.append(
                        {
                            "event": "tool-call",
                            "toolUseId": block.get("id"),
                            "name": block.get("name"),
                            "input": block.get("input"),
                        }
                    )
                elif block.get("type") == "text":
                    transcript.append(
                        {
                            "event": "assistant-text",
                            "text": block.get("text", ""),
                        }
                    )
            continue
        if event_type == "user":
            message = event.get("message")
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                raw_content = block.get("content", "")
                raw_bytes = (
                    raw_content.encode("utf-8")
                    if isinstance(raw_content, str)
                    else _canonical_json(raw_content)
                )
                summary = {
                    "event": "tool-result",
                    "toolUseId": block.get("tool_use_id"),
                    "isError": bool(block.get("is_error", False)),
                    "contentLength": len(raw_bytes),
                    "contentSha256": _sha256_bytes(raw_bytes),
                }
                metadata = _safe_tool_metadata(event.get("tool_use_result"))
                if metadata:
                    summary["metadata"] = metadata
                transcript.append(summary)
            continue
        if event_type == "result":
            transcript.append(
                {
                    "event": "process-result",
                    "subtype": event.get("subtype"),
                    "isError": event.get("is_error"),
                    "durationMs": event.get("duration_ms"),
                    "numTurns": event.get("num_turns"),
                    "result": event.get("result"),
                    "stopReason": event.get("stop_reason"),
                    "terminalReason": event.get("terminal_reason"),
                    "permissionDenials": event.get("permission_denials", []),
                }
            )
    return "".join(
        json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
        for event in transcript
    )


def _redact_request_urls(value: str) -> str:
    return re.sub(
        r"(?m)^(Request URL:\s*)\S+\s*$",
        r"\1<redacted>",
        value,
    )


def _validate(payload: dict[str, Any], root: Path) -> None:
    schema_path = root / "docs/contracts/runtime-evidence.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        raise CaptureError(f"runtime evidence schema failed at {location}: {error.message}")


def capture(
    *,
    consumer: str,
    entrypoint: str,
    protocol_version: str,
    product: str,
    product_version: str,
    provider: str | None,
    model: str | None,
    prompt: str,
    marker: str,
    behavior_sources: list[str],
    command: list[str],
    output: Path,
    root: Path = REPO_ROOT,
    screenshots: list[str] | None = None,
    timeout_seconds: float = 120,
    stdout_mode: str = "raw",
    stderr_mode: str = "raw",
) -> dict[str, Any]:
    root = root.resolve()
    output = output.resolve()
    try:
        output.relative_to(root)
    except ValueError as error:
        raise CaptureError("runtime evidence output must stay inside the repository") from error
    raw_dir = output.parent / f"{output.stem}.d"
    raw_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = raw_dir / "stdout.txt"
    stderr_path = raw_dir / "stderr.txt"

    if timeout_seconds <= 0:
        raise CaptureError("probe timeout must be greater than zero")
    timed_out = False
    try:
        proc = subprocess.run(
            command,
            cwd=root,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout_seconds,
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        exit_code = proc.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout = _timeout_text(error.stdout)
        stderr = _timeout_text(error.stderr)
        exit_code = 124
    if stdout_mode == CLAUDE_STREAM_MODE:
        stdout = _sanitize_claude_stream(stdout)
    elif stdout_mode != "raw":
        raise CaptureError(f"unsupported stdout mode: {stdout_mode}")
    if stderr_mode == REQUEST_URL_REDACTED_MODE:
        stderr = _redact_request_urls(stderr)
    elif stderr_mode != "raw":
        raise CaptureError(f"unsupported stderr mode: {stderr_mode}")
    # Persist LF only so digests match git text=eol=lf and Linux CI checkout.
    stdout_path.write_bytes(stdout.replace("\r\n", "\n").encode("utf-8"))
    stderr_path.write_bytes(stderr.replace("\r\n", "\n").encode("utf-8"))
    marker_observed = marker in stdout
    warnings: list[str] = []
    if timed_out:
        warnings.append(f"Probe timed out after {timeout_seconds:g} seconds.")
    if "unknown provider for model grok-build" in stderr:
        warnings.append(
            "The optional Grok session-title request for model alias grok-build returned provider 502; the main probe result is evaluated separately."
        )
    if timed_out:
        verdict = "blocked"
        reason = "Probe exceeded its bounded runtime before a complete result was available."
    elif exit_code == 0 and marker_observed:
        verdict = "pass"
        reason = "Main process exited 0 and emitted the required marker after the host reported the loaded skill and repository-derived facts."
    else:
        verdict = "fail"
        reason = "Main process did not both exit 0 and emit the required dispatch marker."
    sources = [
        {
            "path": value.replace("\\", "/"),
            "sha256": _sha256_repo_text(_repo_file(root, value, "behavior source")),
        }
        for value in behavior_sources
    ]
    screenshot_values = [value.replace("\\", "/") for value in (screenshots or [])]
    for value in screenshot_values:
        _repo_file(root, value, "screenshot")
    payload = {
        "schemaId": SCHEMA_ID,
        "format": FORMAT,
        "formatVersion": "1.0.0",
        "capturedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "unit": {
            "consumer": consumer,
            "entrypoint": entrypoint,
            "protocolVersion": protocol_version,
        },
        "environment": {
            "product": product,
            "version": product_version,
            "platform": platform.platform(),
            "provider": provider,
            "model": model,
        },
        "behaviorSources": sources,
        "invocation": {
            "command": _normalize_command(command),
            "cwd": ".",
            "timeoutSeconds": timeout_seconds,
            "inputSha256": _sha256_bytes(prompt.encode("utf-8")),
            "inputSummary": f"Read-only /{entrypoint} dispatch probe requiring marker {marker} after repository-backed skill execution.",
        },
        "result": {
            "exitCode": exit_code,
            "verdict": verdict,
            "marker": marker,
            "markerObserved": marker_observed,
            "stdoutPath": str(stdout_path.relative_to(root)).replace("\\", "/"),
            "stdoutSha256": _sha256_file(stdout_path),
            "stdoutMode": stdout_mode,
            "stderrPath": str(stderr_path.relative_to(root)).replace("\\", "/"),
            "stderrSha256": _sha256_file(stderr_path),
            "stderrMode": stderr_mode,
            "warnings": warnings,
            "reason": reason,
        },
        "artifacts": {"screenshots": screenshot_values},
    }
    _validate(payload, root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer", required=True)
    parser.add_argument(
        "--entrypoint",
        choices=("govern", "audit", "vision", "vision-audit"),
        required=True,
    )
    parser.add_argument("--protocol-version", required=True)
    parser.add_argument("--product", required=True)
    parser.add_argument("--product-version", required=True)
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--marker", required=True)
    parser.add_argument("--behavior-source", action="append", default=[], required=True)
    parser.add_argument("--screenshot", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=120)
    parser.add_argument(
        "--stdout-mode",
        choices=("raw", CLAUDE_STREAM_MODE),
        default="raw",
    )
    parser.add_argument(
        "--stderr-mode",
        choices=("raw", REQUEST_URL_REDACTED_MODE),
        default="raw",
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command and args.command[0] == "--" else args.command
    try:
        prompt = args.prompt_file.read_text(encoding="utf-8")
        evidence = capture(
            consumer=args.consumer,
            entrypoint=args.entrypoint,
            protocol_version=args.protocol_version,
            product=args.product,
            product_version=args.product_version,
            provider=args.provider,
            model=args.model,
            prompt=prompt,
            marker=args.marker,
            behavior_sources=args.behavior_source,
            command=command,
            output=args.output,
            root=args.root,
            screenshots=args.screenshot,
            timeout_seconds=args.timeout_seconds,
            stdout_mode=args.stdout_mode,
            stderr_mode=args.stderr_mode,
        )
    except (OSError, json.JSONDecodeError, CaptureError) as error:
        print(f"runtime evidence capture failed: {error}", file=sys.stderr)
        return 1
    print(f"wrote runtime evidence: {args.output}")
    print(f"verdict: {evidence['result']['verdict']}")
    return 0 if evidence["result"]["verdict"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
