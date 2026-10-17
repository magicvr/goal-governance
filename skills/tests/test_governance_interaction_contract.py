"""Cross-surface contract regressions, not a simulated agent or question UI.

Protect the two independent-review routes, distributed/dogfood copies and thin
MCP guidance. Actual numeric resolution and user-question behavior belong to
host runtime evidence; these tests deliberately do not invent a new runner.
"""
from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from mcp.entries import tool_definitions
from mcp.server import MCPServer


ROOT = Path(__file__).resolve().parents[2]
ENTRIES = ("govern", "audit", "vision", "vision-audit")
HOST_DIRS = {"claude": ".claude", "grok": ".grok", "codex": ".agents"}


def surfaces():
    for host, target in HOST_DIRS.items():
        for entry in ENTRIES:
            yield (
                ROOT / f"skills/install/{host}/skills/{entry}/SKILL.md",
                ROOT / f"{target}/skills/{entry}/SKILL.md",
            )
    for entry in ENTRIES:
        yield (
            ROOT / f"skills/install/copilot/prompts/{entry}.md",
            ROOT / f".github/prompts/{entry}.prompt.md",
        )


class GovernanceInteractionContractTests(unittest.TestCase):
    def test_normative_rules_have_stable_unique_references(self):
        text = (ROOT / "docs/architecture/principles.md").read_text(encoding="utf-8")
        for anchor in ("audit-dispatch", "user-input-wait"):
            self.assertEqual(text.count(f'<a id="{anchor}"></a>'), 1)
        for family in ("AD", "UI"):
            rows = re.findall(rf"^\| {family}-(\d\d) · .+", text, re.MULTILINE)
            self.assertEqual(rows, [f"{number:02}" for number in range(1, 7)])

    def test_every_shipped_and_dogfood_entry_consumes_both_contracts(self):
        for source, installed in surfaces():
            for path in (source, installed):
                with self.subTest(path=path.relative_to(ROOT).as_posix()):
                    text = path.read_text(encoding="utf-8")
                    for contract in ("AD-01～AD-06", "UI-01～UI-06"):
                        self.assertIn(contract, text)
                    self.assertIn("{governance_root}/architecture/principles.md", text)
                    # S3 actual headless run stopped in chat but left meta
                    # active. Pause persistence must survive every wrapper.
                    self.assertIn("无需另次确认", text)
                    self.assertIn("配置存在时必须先读", text)
                    self.assertIn("不回退", text)
                    # An unconditional old wrapper instruction must not undo the
                    # automatic-input contract after the new guard paragraph.
                    self.assertNotRegex(text, r"(?m)^3\. 用户.*附带的文字视为.*scope")
                    self.assertNotRegex(text, r"(?m)^`/(?:vision-)?audit` 后的附言视为")

    def test_install_and_dogfood_copies_do_not_diverge(self):
        for source, installed in surfaces():
            with self.subTest(installed=installed.relative_to(ROOT).as_posix()):
                self.assertEqual(source.read_bytes(), installed.read_bytes())

    def test_automatic_audits_do_not_require_human_scope_forms(self):
        for file in ("05-independent-audit.md", "07-independent-vision-review.md"):
            with self.subTest(file=file):
                text = (ROOT / "skills/prompts" / file).read_text(encoding="utf-8")
                self.assertIn("# 人类直调输入（自动合法命令不要求填表）", text)
                self.assertIn("不要求", text)
                self.assertIn("自主", text)
                self.assertIn("UI-01～UI-06", text)
                self.assertLess(text.index("# 自动命令入口"), text.index("# 人类直调输入"))
        protocol = (ROOT / "docs/architecture/workspace-protocol.md").read_text(encoding="utf-8")
        for boundary in ("零匹配", "多匹配", "frontmatter id", "Q1", "Q2", "Q3", "符号链接逃逸"):
            self.assertIn(boundary, protocol)

    def test_rule_templates_preserve_configurable_root_and_wait_contract(self):
        for name in (
            "skills/AGENTS.template.md", "skills/install/claude/AGENTS.md",
            "skills/install/copilot/copilot-instructions.md", ".github/copilot-instructions.md",
        ):
            with self.subTest(path=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                rendered = text.replace("{{GOVERNANCE_ROOT}}", "governance")
                self.assertIn("governance/architecture/principles.md#audit-dispatch", rendered)
                self.assertIn("governance/architecture/principles.md#user-input-wait", rendered)
                for boundary in ("无 Goal", "VP 不改 blocked", "写盘失败", "真实答复", "其他阻塞"):
                    self.assertIn(boundary, rendered)

    def test_thin_mcp_returns_guardrails_without_file_prompts_or_state_writes(self):
        with tempfile.TemporaryDirectory(prefix="gg-interaction-") as tmp:
            repo = Path(tmp)
            sentinel = repo / "user-file.txt"
            sentinel.write_bytes(b"preserve user content\n")
            server = MCPServer(repo)
            server.handle_initialize({"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}})
            for name in ENTRIES:
                with self.subTest(entry=name):
                    # Existing human task/scope input remains compatible. This
                    # server supplies guidance; it is not a command validator.
                    args = {"task": "human direct request"}
                    if name == "audit":
                        args.update(goal_id="GOAL-001-fixture-root", scope="human scope")
                    elif name == "vision-audit":
                        args["scope"] = "human scope"
                    before = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
                    result = server.handle_tools_call({"name": name, "arguments": args})
                    structured = result["structuredContent"]
                    self.assertEqual(structured["status"], "ok")
                    self.assertIsNone(structured["promptSha256"])
                    for boundary in ("AD-01～AD-06", "UI-01～UI-06", "/audit NNN NNN", "/vision-audit NNN", "空返回", "预选未提交", "真实答复", "独立审计只返回待答事实"):
                        self.assertIn(boundary, structured["guidance"])
                    self.assertEqual(structured["readonly"], name in {"audit", "vision-audit"})
                    after = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
                    self.assertEqual(before, after)

    def test_guidance_update_keeps_existing_mcp_parameter_shape(self):
        expected = {
            "vision": ({"task", "workspace"}, ["task"]),
            "govern": ({"task", "workspace", "goal_id"}, ["task"]),
            "audit": ({"task", "goal_id", "scope"}, ["task", "goal_id"]),
            "vision-audit": ({"task", "scope"}, ["task"]),
        }
        for tool in tool_definitions():
            with self.subTest(entry=tool["name"]):
                fields, required = expected[tool["name"]]
                schema = tool["inputSchema"]
                self.assertEqual(set(schema["properties"]), fields)
                self.assertEqual(schema["required"], required)
                self.assertFalse(schema["additionalProperties"])
                self.assertTrue(all(p["type"] == "string" for p in schema["properties"].values()))

    def test_execution_template_retains_questions_and_real_answer_provenance(self):
        text = (ROOT / "docs/templates/goal-folder/02-execution.md").read_text(encoding="utf-8")
        for field in ("问题 ID", "原题 / 选项", "影响范围 / 门禁", "原有阻塞", "恢复条件", "真实答复来源 / 内容"):
            self.assertIn(field, text)
        self.assertIn("不补默认选择或伪造提交", text)


if __name__ == "__main__":
    unittest.main()
