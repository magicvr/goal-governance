"""L1 MCP channel tests (VP-004 R1): drive the REAL MCP stdio server process.

Evidence level L1 (mcp): deterministic mock-free verification of the thin
shell — tool names and key parameter boundaries (I-001), read-only dispatch
role boundaries, and requirement that ``commit`` is NOT exposed. The server is
launched as a real subprocess speaking the MCP stdio transport
(newline-delimited JSON-RPC 2.0).

These tests are the MCP-channel half of the L2 shared kernel consumer; the
shared assertions themselves live in mcp/kernel.py and are exercised by
docs/tests/test_dual_channel_l2.py.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_PY = REPO_ROOT / "mcp" / "server.py"

ENTRY_LAYERS = {
    "vision": "decision",
    "vision-audit": "decision",
    "govern": "implementation",
    "audit": "implementation",
}
READONLY_ENTRIES = {"vision-audit", "audit"}
REQUIRED_PARAMS = {
    "vision": ["task"],
    "vision-audit": ["task"],
    "govern": ["task"],
    "audit": ["task", "goal_id"],
}


class McpServerProcess:
    """Thin wrapper over the real MCP server subprocess (stdio transport)."""

    def __init__(self, repo_root: Path) -> None:
        self.proc = subprocess.Popen(
            [sys.executable, str(SERVER_PY), "--repo-root", str(repo_root)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(repo_root),
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def request(self, method: str, params: dict[str, Any] | None = None, request_id: int = 1) -> dict[str, Any]:
        assert self.proc.stdin is not None and self.proc.stdout is not None
        message = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        self.proc.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            stderr = self.proc.stderr.read() if self.proc.stderr else ""
            raise AssertionError(f"MCP server exited without response; stderr: {stderr}")
        payload = json.loads(line)
        return payload

    def close(self) -> None:
        if self.proc.stdin:
            try:
                self.proc.stdin.close()
            except BrokenPipeError:
                pass
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=10)


class McpL1Tests(unittest.TestCase):
    """L1 MCP: real process, tools/list + read-only tools/call per entry."""

    def setUp(self) -> None:
        self.assertTrue(SERVER_PY.is_file(), f"missing MCP server: {SERVER_PY}")
        self.server = McpServerProcess(REPO_ROOT)
        self.addCleanup(self.server.close)
        init = self.server.request("initialize", {"protocolVersion": "2025-03-26"}, request_id=1)
        self.assertNotIn("error", init)
        self.assertEqual(init["result"]["serverInfo"]["name"], "goal-governance-mcp")

    def _tools_list(self) -> list[dict[str, Any]]:
        response = self.server.request("tools/list", request_id=2)
        self.assertNotIn("error", response)
        tools = response["result"]["tools"]
        self.assertIsInstance(tools, list)
        return tools

    def _call_tool(self, name: str, arguments: dict[str, Any], request_id: int) -> dict[str, Any]:
        return self.server.request(
            "tools/call",
            {"name": name, "arguments": arguments},
            request_id=request_id,
        )

    def test_tools_list_exposes_four_governance_tools_with_boundaries(self) -> None:
        tools = self._tools_list()
        by_name = {tool["name"]: tool for tool in tools}
        governance_names = {"vision", "vision-audit", "govern", "audit"}
        self.assertTrue(
            governance_names.issubset(set(by_name)),
            msg="four governance tools must be exposed",
        )
        self.assertNotIn(
            "commit",
            by_name,
            msg="commit must NOT be exposed (convenience, orthogonal to governance)",
        )
        for name, required in REQUIRED_PARAMS.items():
            schema = by_name[name]["inputSchema"]
            self.assertEqual(
                sorted(schema["required"]),
                sorted(required),
                msg=f"{name} required parameter boundary drifted",
            )
            for param in required:
                self.assertIn(param, schema["properties"], msg=f"{name} missing {param}")
            # Unknown parameters are refused by the recorded boundary.
            self.assertFalse(schema.get("additionalProperties", False))

    def test_tools_list_exposes_r2_lifecycle_tools(self) -> None:
        tools = self._tools_list()
        by_name = {tool["name"]: tool for tool in tools}
        for name in ("install", "upgrade", "uninstall", "doctor"):
            self.assertIn(name, by_name, msg=f"missing lifecycle tool {name}")
            self.assertIn("inputSchema", by_name[name])

    def test_dispatch_roles_match_recorded_boundaries(self) -> None:
        """Read-only tools/call per entry: layer + role + readonly flags."""
        expectations = {
            "vision": (False, "决策层"),
            "vision-audit": (True, "只写意见"),
            "govern": (False, "实现编排"),
            "audit": (True, "只出意见"),
        }
        arguments = {
            "vision": {"task": "请核对决策层入口"},
            "vision-audit": {"task": "请核对独立 Vision Review 入口"},
            "govern": {"task": "请核对实现编排入口"},
            "audit": {"task": "请核对交叉审计入口", "goal_id": "GOAL-002-r1-mcp-equivalence-kernel"},
        }
        for index, (name, (readonly, role_keyword)) in enumerate(expectations.items(), start=3):
            response = self._call_tool(name, arguments[name], request_id=index)
            self.assertNotIn("error", response, msg=response)
            structured = response["result"]["structuredContent"]
            self.assertEqual(structured["entrypoint"], name)
            self.assertEqual(structured["layer"], ENTRY_LAYERS[name])
            self.assertEqual(structured["readonly"], readonly, msg=f"{name} readonly flag")
            self.assertIn(role_keyword, structured["role"], msg=f"{name} role text")
            self.assertTrue(
                structured["promptPath"].startswith("prompts/"),
                msg=f"{name} prompt path",
            )
            self.assertEqual(structured["status"], "ok")
            # Ledger boundary: independent entries only reach their own ledger.
            writes_to = "\n".join(structured["writesTo"])
            if name == "vision-audit":
                self.assertIn("vision/reviews", writes_to)
                self.assertNotIn("03-audit", writes_to)
            elif name == "audit":
                self.assertIn("03-audit", writes_to)
                self.assertNotIn("vision", writes_to)
            elif name == "govern":
                self.assertIn("goal-tree.md", writes_to)
                self.assertNotIn("vision/reviews", writes_to)

    def test_missing_required_parameter_is_refused(self) -> None:
        response = self._call_tool(
            "audit", {"task": "缺 goal_id 必须拒绝"}, request_id=99
        )
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("goal_id", response["error"]["message"])

    def test_unknown_tool_is_refused(self) -> None:
        response = self._call_tool("commit", {"task": "nope"}, request_id=100)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)

    def test_two_consecutive_runs_are_identical(self) -> None:
        """Deterministic channel: same requests -> byte-identical transcript."""
        def transcript() -> list[str]:
            server = McpServerProcess(REPO_ROOT)
            try:
                lines: list[str] = []
                lines.append(
                    json.dumps(server.request("initialize", request_id=1), sort_keys=True)
                )
                lines.append(json.dumps(server.request("tools/list", request_id=2), sort_keys=True))
                for entry in ("vision", "audit"):
                    arguments = (
                        {"task": "x", "goal_id": "GOAL-002-r1-mcp-equivalence-kernel"}
                        if entry == "audit"
                        else {"task": "x"}
                    )
                    lines.append(
                        json.dumps(
                            server.request("tools/call", {"name": entry, "arguments": arguments}, request_id=3),
                            sort_keys=True,
                        )
                    )
                return lines
            finally:
                server.close()

        first = transcript()
        second = transcript()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
