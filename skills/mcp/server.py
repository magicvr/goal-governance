#!/usr/bin/env python3
"""Minimal MCP stdio server for the four goal-governance entries (R1).

Speaks the MCP stdio transport: newline-delimited JSON-RPC 2.0 messages over
stdin/stdout (one JSON object per line; nothing else on stdout). No third-party
runtime required, so the channel works without Docker and without installing
the full File skills package (VP-004 R1: thin MCP channel).

Tools exposed (governance-mandatory set, VP-004 entry surface):
    vision / vision-audit / govern / audit
``commit`` is intentionally NOT exposed (convenience, orthogonal to governance).

Read-only dispatch contract: ``tools/call`` returns structured metadata
(entrypoint, layer, role boundary, readonly flag, prompt path, guidance) and
never mutates repository state for the four entries. Role boundaries are
enforced by the caller (host) reading the guidance; the server itself performs
no filesystem writes on any governance tool call.

Usage:  python skills/mcp/server.py [--repo-root PATH] [--version]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:  # package context (python -m / import)
    from . import __version__
    from .entries import LEDGER_TARGETS, entrypoint_specs, tool_definitions
except ImportError:  # plain script context (python skills/mcp/server.py)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from __init__ import __version__  # type: ignore[no-redef]
    from entries import (  # type: ignore[no-redef]
        LEDGER_TARGETS,
        entrypoint_specs,
        tool_definitions,
    )

PROTOCOL_VERSION = "2025-03-26"
SERVER_NAME = "goal-governance-mcp"


class MCPError(Exception):
    """JSON-RPC error carrying a protocol error code."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class MCPServer:
    """Newline-delimited JSON-RPC 2.0 server for the MCP stdio transport."""

    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = (repo_root or Path.cwd()).resolve()
        self.initialized = False

    # ------------------------------------------------------------------ I/O
    def _write(self, payload: dict[str, Any]) -> None:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        sys.stdout.flush()

    def _read_message(self) -> dict[str, Any] | None:
        line = sys.stdin.readline()
        if not line:
            return None
        line = line.strip()
        if not line:
            return self._read_message()
        try:
            message = json.loads(line)
        except json.JSONDecodeError as error:
            raise MCPError(-32700, f"Parse error: {error}") from error
        if not isinstance(message, dict):
            raise MCPError(-32600, "Invalid Request: message must be an object")
        return message

    # ------------------------------------------------------------- methods
    def handle_initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        self.initialized = True
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": __version__},
            "instructions": (
                "Goal-governance MCP channel. Tools: vision (decision layer), "
                "vision-audit (independent Vision Review, opinions only), "
                "govern (implementation orchestration), audit (goal cross-audit, "
                "opinions only). Instance truth stays in the repository "
                "governance tree; this server never becomes an authoritative "
                "state store."
            ),
        }

    def handle_tools_list(self) -> dict[str, Any]:
        return {"tools": tool_definitions()}

    def handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        name = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            raise MCPError(-32602, "Invalid params: arguments must be an object")
        specs = entrypoint_specs()
        if name not in specs:
            raise MCPError(-32602, f"Unknown tool: {name}")
        spec = specs[name]

        # Validate required parameters against the recorded boundary.
        missing = [
            key
            for key, (_, is_required, _) in spec.parameters.items()
            if is_required and (key not in arguments or arguments.get(key) in (None, ""))
        ]
        if missing:
            raise MCPError(
                -32602,
                f"Missing required parameter(s) for {name}: {', '.join(missing)}",
            )

        prompt_path = spec.prompt_path
        prompt_sha256: str | None = None
        candidate = self.repo_root / "skills" / prompt_path
        if candidate.is_file():
            prompt_sha256 = _sha256_hex(candidate.read_bytes())

        guidance = (
            f"{spec.role} 本入口由 {prompt_path} 承载方法论正文"
            + ("（仓内已存在，可核对 sha256）" if prompt_sha256 else "（仓内无 File 大包，用内置摘要）")
        )
        structured = {
            "entrypoint": spec.name,
            "layer": spec.layer,
            "role": spec.role,
            "readonly": spec.readonly_dispatch,
            "writesTo": _ledger_targets(spec.name),
            "promptPath": prompt_path,
            "promptSha256": prompt_sha256,
            "guidance": guidance,
            "status": "ok",
        }
        return {
            "content": [{"type": "text", "text": guidance}],
            "structuredContent": structured,
            "isError": False,
        }

    def handle_ping(self) -> dict[str, Any]:
        return {}

    # ------------------------------------------------------------- loop
    def serve(self) -> int:
        while True:
            try:
                message = self._read_message()
            except MCPError as error:
                self._write(
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": error.code, "message": error.message},
                    }
                )
                continue
            if message is None:
                return 0  # EOF on stdin: client closed the transport.

            request_id = message.get("id")
            method = message.get("method")
            params = message.get("params") or {}
            if not isinstance(params, dict):
                params = {}

            # Notifications carry no id; do not respond.
            if request_id is None:
                if method == "notifications/initialized":
                    self.initialized = True
                continue

            try:
                if method == "initialize":
                    result = self.handle_initialize(params)
                elif method == "tools/list":
                    result = self.handle_tools_list()
                elif method == "tools/call":
                    result = self.handle_tools_call(params)
                elif method == "ping":
                    result = self.handle_ping()
                elif method == "notifications/initialized":
                    result = {}
                else:
                    raise MCPError(-32601, f"Method not found: {method}")
            except MCPError as error:
                self._write(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": error.code, "message": error.message},
                    }
                )
                continue

            self._write({"jsonrpc": "2.0", "id": request_id, "result": result})


def _sha256_hex(value: bytes) -> str:
    from hashlib import sha256

    return sha256(value).hexdigest()


def _ledger_targets(name: str) -> list[str]:
    return list(LEDGER_TARGETS.get(name, []))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root used to locate thin prompt assets (default: cwd).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{SERVER_NAME} {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return MCPServer(repo_root=args.repo_root).serve()


if __name__ == "__main__":
    raise SystemExit(main())
