"""L2 shared equivalence kernel tests (VP-004 R1).

The SAME assertion set (mcp/kernel.py::check_equivalence, backed by the
ten V-F-016 checkpoints) runs over BOTH channel descriptions:
  - File channel: derived from the REAL repository File assets.
  - MCP channel: derived from the REAL MCP server process tools/list payload.

No MCP mock stands in for File evidence, and no File description is invented:
both descriptions come from real artifacts. The dual-channel fixture under
fixtures/dual-channel provides the minimal workspace shape the L2 assertions
use for instance-truth / ledger / five-piece checks.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
MCP_PKG = REPO_ROOT / "mcp"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "dual-channel"

sys.path.insert(0, str(MCP_PKG.parent))  # make `import mcp.kernel` resolve

import mcp.kernel as kernel  # noqa: E402


def _mcp_tools_payload(repo_root: Path) -> list[dict[str, Any]]:
    """Launch the REAL MCP server and return its tools/list payload."""
    server_py = repo_root / "mcp" / "server.py"
    proc = subprocess.Popen(
        [sys.executable, str(server_py), "--repo-root", str(repo_root)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(repo_root),
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        assert proc.stdin is not None and proc.stdout is not None
        proc.stdin.write(
            json.dumps(
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
            )
            + "\n"
        )
        proc.stdin.write(
            json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}) + "\n"
        )
        proc.stdin.flush()
        responses = [json.loads(proc.stdout.readline()), json.loads(proc.stdout.readline())]
        for response in responses:
            assert "error" not in response, response
        return responses[1]["result"]["tools"]
    finally:
        if proc.stdin:
            try:
                proc.stdin.close()
            except BrokenPipeError:
                pass
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)


class DualChannelL2Tests(unittest.TestCase):
    """L2 shared: the same assertions drive File and MCP channel descriptions."""

    def test_checkpoints_are_the_ten_vf016_items(self) -> None:
        checkpoints = kernel.EQUIVALENCE_CHECKPOINTS
        self.assertEqual(len(checkpoints), 10)
        self.assertEqual([item["id"] for item in checkpoints], [str(i) for i in range(1, 11)])
        for item in checkpoints:
            self.assertTrue(item["name"])
            self.assertTrue(item["description"])

    def test_equivalence_holds_for_both_channels(self) -> None:
        file_desc = kernel.describe_file_channel(REPO_ROOT)
        tools = _mcp_tools_payload(REPO_ROOT)
        mcp_desc = kernel.describe_mcp_channel(tools)

        results = kernel.check_equivalence(file_desc, mcp_desc)
        self.assertEqual(len(results), 10)
        failures = [item for item in results if not item["ok"]]
        self.assertEqual(
            failures,
            [],
            msg="L2 equivalence failures: "
            + "; ".join(f"#{item['checkpoint']} {item['detail']}" for item in failures),
        )

    def test_both_channel_descriptions_are_backed_by_real_artifacts(self) -> None:
        file_desc = kernel.describe_file_channel(REPO_ROOT)
        tools = _mcp_tools_payload(REPO_ROOT)
        mcp_desc = kernel.describe_mcp_channel(tools)

        for name in kernel.ENTRYPOINT_NAMES:
            self.assertTrue(
                file_desc.entrypoints[name]["prompt_present"],
                msg=f"File channel missing prompt backing for {name}",
            )
            self.assertTrue(
                mcp_desc.entrypoints[name]["tool_present"],
                msg=f"MCP channel missing tool backing for {name}",
            )

    def test_audit_and_vision_audit_are_readonly_in_both_channels(self) -> None:
        file_desc = kernel.describe_file_channel(REPO_ROOT)
        tools = _mcp_tools_payload(REPO_ROOT)
        mcp_desc = kernel.describe_mcp_channel(tools)
        for name in kernel.READONLY_DISPATCH_ENTRIES:
            self.assertTrue(file_desc.entrypoints[name]["readonly_dispatch"])
            self.assertTrue(mcp_desc.entrypoints[name]["readonly_dispatch"])

    def test_dual_channel_fixture_has_canonical_goal_shape(self) -> None:
        """Checkpoint 5 concretely: fixture matches the canonical five-piece shape."""
        goal_dir = FIXTURE / "GOAL-001-fixture-root"
        for name in ("00-meta.md", "01-decision.md", "02-execution.md", "03-audit.md"):
            self.assertTrue((goal_dir / name).is_file(), msg=f"missing {name}")
        for ledger in ("01-decision", "02-execution", "03-audit"):
            self.assertTrue((goal_dir / ledger).is_dir(), msg=f"missing ledger {ledger}")
        self.assertTrue((goal_dir / "attachments").is_dir())
        meta = (goal_dir / "00-meta.md").read_text(encoding="utf-8")
        self.assertIn("id: GOAL-001-fixture-root", meta)
        self.assertIn("parent: null", meta)
        self.assertTrue((FIXTURE / "goal-tree.md").is_file())


if __name__ == "__main__":
    unittest.main()
