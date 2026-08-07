"""L1 MCP lifecycle tests (VP-004 R2): real server + temp consumer repo.

Drives the REAL MCP server process against a temporary consumer repository to
verify the R2 thin-shell contract:

- managed paths allowlist: install/upgrade/uninstall write ONLY AGENTS.md
  (managed section) and .goal-governance/; other paths fail closed.
- default confirm-before-write: confirm=false refuses to write.
- AGENTS.md managed markers: update/uninstall touch only the marker region;
  user content outside markers stays byte-identical.
- doctor reports installation state correctly.
- gitignore fragment ships and ignores the thin shell.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_PY = REPO_ROOT / "mcp" / "server.py"
FRAGMENT = REPO_ROOT / "mcp" / "gitignore-fragment.txt"

MANAGED_BEGIN = "<!-- goal-governance:begin managed -->"
MANAGED_END = "<!-- goal-governance:end managed -->"
USER_PREAMBLE = (
    "# 我的项目规则（用户自有内容，必须逐字节保留）\n"
    "- 测试先于代码\n"
    "- 中文提交信息\n"
)


class McpServerProcess:
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
        return json.loads(line)

    def call_tool(self, name: str, arguments: dict[str, Any], request_id: int) -> dict[str, Any]:
        return self.request(
            "tools/call", {"name": name, "arguments": arguments}, request_id=request_id
        )

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


class McpLifecycleTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.consumer = Path(self.tmp.name) / "consumer"
        self.consumer.mkdir()
        self.server = McpServerProcess(self.consumer)
        self.addCleanup(self.server.close)
        init = self.server.request("initialize", {"protocolVersion": "2025-03-26"}, request_id=1)
        self.assertNotIn("error", init)

    def _call(self, name: str, arguments: dict[str, Any], request_id: int) -> dict[str, Any]:
        return self.server.call_tool(name, arguments, request_id)

    def _agents(self) -> str:
        path = self.consumer / "AGENTS.md"
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_install_requires_confirm_and_then_writes_allowlisted_paths(self) -> None:
        # Without confirm: refused, nothing written.
        refused = self._call("install", {"channel": "mcp"}, request_id=2)
        self.assertTrue(refused["result"]["isError"])
        self.assertIn("confirm", refused["result"]["structuredContent"]["message"])
        self.assertFalse((self.consumer / "AGENTS.md").exists())
        self.assertFalse((self.consumer / ".goal-governance").exists())

        # With confirm: writes only AGENTS.md managed section + .goal-governance.
        ok = self._call("install", {"confirm": True, "channel": "mcp"}, request_id=3)
        self.assertFalse(ok["result"]["isError"], msg=ok)
        wrote = ok["result"]["structuredContent"]["wrote"]
        self.assertEqual(sorted(wrote), [".goal-governance/install.json", "AGENTS.md"])
        agents = self._agents()
        self.assertIn(MANAGED_BEGIN, agents)
        self.assertIn(MANAGED_END, agents)
        state = json.loads(
            (self.consumer / ".goal-governance" / "install.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state["channel"], "mcp")
        self.assertEqual(state["layout"], "1")
        # Nothing else appeared in the consumer repo.
        self.assertEqual(
            sorted(p.name for p in self.consumer.iterdir()),
            [".goal-governance", "AGENTS.md"],
        )

    def test_uninstall_touches_only_managed_region_and_user_content_survives(self) -> None:
        agents_path = self.consumer / "AGENTS.md"
        agents_path.write_text(USER_PREAMBLE, encoding="utf-8")
        user_bytes_before = agents_path.read_bytes()
        ok = self._call("install", {"confirm": True}, request_id=2)
        self.assertFalse(ok["result"]["isError"])
        # User preamble survived install byte-identically.
        self.assertTrue(self._agents().startswith(USER_PREAMBLE))

        removed = self._call("uninstall", {"confirm": True}, request_id=3)
        self.assertFalse(removed["result"]["isError"])
        # After uninstall: managed markers gone; user content byte-identical.
        self.assertNotIn(MANAGED_BEGIN, self._agents())
        self.assertNotIn(MANAGED_END, self._agents())
        self.assertFalse((self.consumer / ".goal-governance").exists())
        final_text = self._agents()
        self.assertTrue(final_text.startswith(USER_PREAMBLE))
        self.assertEqual(
            final_text.replace(USER_PREAMBLE, "").strip(),
            "",
            msg="only user content may remain after uninstall",
        )
        # Byte-identity of user region: preamble with trailing newline preserved.
        self.assertIn(USER_PREAMBLE, final_text)

    def test_upgrade_rewrites_only_inside_markers(self) -> None:
        ok = self._call("install", {"confirm": True}, request_id=2)
        self.assertFalse(ok["result"]["isError"])
        agents = self._agents()
        before = agents[agents.index(MANAGED_BEGIN) :]
        # User content appended AFTER the managed block must survive upgrade.
        suffix = "\n## 用户附录\n自定义内容。\n"
        (self.consumer / "AGENTS.md").write_text(agents + suffix, encoding="utf-8")
        suffix_bytes_before = suffix.encode("utf-8")

        upgraded = self._call("upgrade", {"confirm": True}, request_id=3)
        self.assertFalse(upgraded["result"]["isError"])
        after = self._agents()
        # Suffix byte-identical.
        self.assertTrue(after.endswith(suffix))
        # Managed region still between the same markers.
        self.assertIn(MANAGED_BEGIN, after)
        self.assertIn(MANAGED_END, after)
        self.assertNotEqual(before, after[after.index(MANAGED_BEGIN) :], msg="version should update")
        state = json.loads(
            (self.consumer / ".goal-governance" / "install.json").read_text(encoding="utf-8")
        )
        self.assertTrue(state["version"])

    def test_allowlist_rejects_outside_paths(self) -> None:
        # A root that is not a directory fails closed.
        bad = self._call(
            "install",
            {"confirm": True, "root": str(self.consumer / "does-not-exist")},
            request_id=2,
        )
        self.assertTrue(bad["result"]["isError"])
        self.assertIn("not a directory", bad["result"]["structuredContent"]["message"])

        # A root that is a file (not a directory) fails closed.
        file_root = self.consumer / "a-file"
        file_root.write_text("x", encoding="utf-8")
        as_file = self._call(
            "install",
            {"confirm": True, "root": str(file_root)},
            request_id=3,
        )
        self.assertTrue(as_file["result"]["isError"])

        # Unit-level: allowlist rejects non-allowlisted path parts.
        import sys as _sys

        _sys.path.insert(0, str(REPO_ROOT / "skills"))
        import mcp.lifecycle as lifecycle  # noqa: E402

        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle._validate_allowlist(self.consumer, ["docs/architecture/principles.md"])
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle._validate_allowlist(self.consumer, ["mcp/server.py"])
        # Candidate escaping the repo root fails closed.
        with self.assertRaises(lifecycle.LifecycleError):
            lifecycle._ensure_inside_repo(self.consumer, "../outside.md")

    def test_doctor_reports_state_after_install_and_uninstall(self) -> None:
        before = self._call("doctor", {}, request_id=2)
        self.assertFalse(before["result"]["isError"])
        self.assertFalse(before["result"]["structuredContent"]["ok"])
        self.assertIn("not installed", "\n".join(before["result"]["structuredContent"]["issues"]))

        self._call("install", {"confirm": True}, request_id=3)
        after = self._call("doctor", {}, request_id=4)
        report = after["result"]["structuredContent"]
        self.assertTrue(report["ok"], msg=report["issues"])
        self.assertTrue(report["managedSection"]["present"])
        self.assertTrue(report["thinShell"]["present"])
        self.assertEqual(report["thinShell"]["channel"], "mcp")
        self.assertTrue(report["thinShell"]["version"])

        self._call("uninstall", {"confirm": True}, request_id=5)
        final = self._call("doctor", {}, request_id=6)
        self.assertFalse(final["result"]["structuredContent"]["ok"])

    def test_gitignore_fragment_ignores_thin_shell(self) -> None:
        self.assertTrue(FRAGMENT.is_file())
        fragment = FRAGMENT.read_text(encoding="utf-8")
        self.assertIn(".goal-governance/", fragment)
        gitignore = self.consumer / ".gitignore"
        gitignore.write_text(fragment, encoding="utf-8")
        doctor_report = self._call("doctor", {}, request_id=2)["result"]["structuredContent"]
        self.assertTrue(doctor_report["gitignore"]["thinShellIgnored"])


if __name__ == "__main__":
    unittest.main()
