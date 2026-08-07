#!/usr/bin/env python3
"""Minimal MCP stdio server for the four goal-governance entries (R1).

Speaks the MCP stdio transport: newline-delimited JSON-RPC 2.0 messages over
stdin/stdout (one JSON object per line; nothing else on stdout). No third-party
runtime required, so the channel works without Docker and without installing
the full File skills package (VP-004 R1: thin MCP channel).

Tools exposed (governance-mandatory set, VP-004 entry surface):
    vision / vision-audit / govern / audit
plus R2 lifecycle tools: install / upgrade / uninstall / doctor.
``commit`` is intentionally NOT exposed (convenience, orthogonal to governance).

Read-only dispatch contract: ``tools/call`` on the four governance entries
returns structured metadata (entrypoint, layer, role boundary, readonly flag,
prompt path, guidance) and never mutates repository state. Lifecycle tools
write ONLY to the managed paths allowlist (AGENTS.md managed section and
.goal-governance/) and require explicit ``confirm=true`` (default refuse).

Usage:  python mcp/server.py [--repo-root PATH] [--version]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:  # package context (python -m / import)
    from . import __version__
    from .doctor import doctor as doctor_report
    from .entries import LEDGER_TARGETS, entrypoint_specs, tool_definitions
    from .lifecycle import LifecycleError, install, uninstall, upgrade
except ImportError:  # plain script context (python mcp/server.py)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from __init__ import __version__  # type: ignore[no-redef]
    from doctor import doctor as doctor_report  # type: ignore[no-redef]
    from entries import (  # type: ignore[no-redef]
        LEDGER_TARGETS,
        entrypoint_specs,
        tool_definitions,
    )
    from lifecycle import (  # type: ignore[no-redef]
        LifecycleError,
        install,
        uninstall,
        upgrade,
    )

PROTOCOL_VERSION = "2025-03-26"
SERVER_NAME = "goal-governance-mcp"

# Lifecycle tools (VP-004 R2): thin-shell install/upgrade/uninstall + doctor.
LIFECYCLE_TOOLS: list[dict[str, Any]] = [
    {
        "name": "install",
        "description": (
            "安装 MCP 薄壳（VP-004 R2）：写 AGENTS.md managed 段 + .goal-governance/install.json；"
            "managed paths allowlist；默认确认写盘（confirm=true 才写）。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "description": "仓库根路径（默认 server --repo-root）"},
                "confirm": {"type": "boolean", "description": "确认写盘；默认 false 拒绝写入"},
                "channel": {"type": "string", "description": "安装通道标识（默认 mcp）"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "upgrade",
        "description": (
            "升级 MCP 薄壳 managed 段与 install.json 到当前 server 版本；只改标记内内容。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "description": "仓库根路径（默认 server --repo-root）"},
                "confirm": {"type": "boolean", "description": "确认写盘；默认 false 拒绝写入"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "uninstall",
        "description": (
            "卸载 MCP 薄壳：只移除 AGENTS.md managed 段与 .goal-governance/ 状态；"
            "标记外用户内容不动。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "description": "仓库根路径（默认 server --repo-root）"},
                "confirm": {"type": "boolean", "description": "确认写盘；默认 false 拒绝写入"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "doctor",
        "description": "只读安装状态报告（managed 段、薄壳状态、gitignore、governance_root）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "description": "仓库根路径（默认 server --repo-root）"},
            },
            "additionalProperties": False,
        },
    },
]


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
        return {"tools": tool_definitions() + LIFECYCLE_TOOLS}

    def _handle_lifecycle_call(
        self, name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        root_value = arguments.get("root")
        root = Path(root_value).resolve() if root_value else self.repo_root
        confirm = bool(arguments.get("confirm", False))
        if name in ("install", "upgrade", "uninstall"):
            try:
                if name == "install":
                    result = install(
                        root,
                        confirm=confirm,
                        version=__version__,
                        channel=str(arguments.get("channel") or "mcp"),
                    )
                elif name == "upgrade":
                    result = upgrade(root, confirm=confirm, version=__version__)
                else:
                    result = uninstall(root, confirm=confirm)
            except LifecycleError as error:
                return {
                    "content": [{"type": "text", "text": str(error)}],
                    "structuredContent": {
                        "tool": name,
                        "status": "error",
                        "message": str(error),
                    },
                    "isError": True,
                }
            structured = {
                "tool": name,
                "status": "ok",
                "wrote": result.wrote,
                "version": result.version,
                "channel": result.channel,
            }
            return {
                "content": [{"type": "text", "text": f"{name} ok: {', '.join(result.wrote)}"}],
                "structuredContent": structured,
                "isError": False,
            }
        # doctor: read-only
        report = doctor_report(root)
        return {
            "content": [{"type": "text", "text": json.dumps(report, ensure_ascii=False)}],
            "structuredContent": {"tool": "doctor", "status": "ok", **report},
            "isError": False,
        }

    def handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        name = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            raise MCPError(-32602, "Invalid params: arguments must be an object")
        specs = entrypoint_specs()
        if name in specs:
            return self._handle_governance_call(name, arguments)
        if name in {tool["name"] for tool in LIFECYCLE_TOOLS}:
            return self._handle_lifecycle_call(name, arguments)
        raise MCPError(-32602, f"Unknown tool: {name}")

    def _handle_governance_call(
        self, name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        specs = entrypoint_specs()
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
            + ("（仓内已存在，可核对 sha256）" if prompt_sha256 else "（仓内无 File 大包，用内置角色/台账边界 guidance）")
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
