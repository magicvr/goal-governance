"""Regression of the shipped L0 drift-check contract, not an AI drift classifier.

Semantic outcomes are separately checked with actual isolated host invocations.
These tests prevent losing a lifecycle hook or bypassing it in the thin channel.
"""
from pathlib import Path
import re
import tempfile
import unittest

from mcp.server import MCPServer


ROOT = Path(__file__).resolve().parents[2]


class GoalDriftContractTests(unittest.TestCase):
    def test_canonical_contract_has_one_complete_rule_set(self):
        text = (ROOT / "docs/architecture/principles.md").read_text(encoding="utf-8")
        self.assertEqual(text.count('<a id="goal-drift"></a>'), 1)
        rows = re.findall(r"^\| GD-(\d\d) · .+", text, re.MULTILINE)
        self.assertEqual(rows, [f"{n:02}" for n in range(1, 9)])
        section = text.split('<a id="goal-drift"></a>', 1)[1].split("## P-002", 1)[0]
        for requirement in (
            "直接父目标", "原始用户授权", "原值→新值", "实际产物",
            "没有覆盖", "required finding", "合法子集", "禁止伪造", "L0",
        ):
            self.assertIn(requirement, section)

    def test_every_goal_lifecycle_primitive_consumes_drift_rules(self):
        names = ("00-govern-orchestrator.md", "01-create-new-goal.md",
                 "02-record-decision.md", "03-update-execution.md",
                 "04-write-audit.md", "05-independent-audit.md")
        for name in names:
            with self.subTest(prompt=name):
                text = (ROOT / "skills/prompts" / name).read_text(encoding="utf-8")
                self.assertIn("{governance_root}/architecture/principles.md#goal-drift", text)
                self.assertIn("GD-01～GD-08", text)
                self.assertIn("直接父目标", text)
        creation = (ROOT / "skills/prompts/01-create-new-goal.md").read_text(encoding="utf-8")
        self.assertLess(creation.index("2b. **GD"), creation.index("3. 创建"))
        decision = (ROOT / "skills/prompts/02-record-decision.md").read_text(encoding="utf-8")
        self.assertLess(decision.index("先取得对应范围用户明确裁决"), decision.index("再同步"))

    def test_audit_routes_require_evidence_comparison_and_keep_write_boundary(self):
        for name in ("04-write-audit.md", "05-independent-audit.md"):
            with self.subTest(prompt=name):
                text = (ROOT / "skills/prompts" / name).read_text(encoding="utf-8")
                for requirement in ("### 目标漂移对照", "父级条目/版本", "实际证据",
                                    "影响门禁", "证据不足", "required finding",
                                    "缺证据不能写无漂移 pass", "合法贡献子集"):
                    self.assertIn(requirement, text)
                verdict = text.split("# Verdict 尺度", 1)[1]
                self.assertIn("scope 内无未关闭 required", verdict)
                self.assertNotIn("无未关闭 high required", verdict)
        independent = (ROOT / "skills/prompts/05-independent-audit.md").read_text(encoding="utf-8")
        self.assertIn("身份门禁通过后，自主读取", independent)
        self.assertIn("不能改父级/子目标标准追认", independent)
        self.assertIn("不依赖编排器提示", independent)

    def test_goal_templates_preserve_authorization_and_delivery_chain(self):
        for name in ("00-meta.md", "01-decision.md", "02-execution.md", "03-audit.md"):
            with self.subTest(template=name):
                text = (ROOT / "docs/templates/goal-folder" / name).read_text(encoding="utf-8")
                self.assertIn("GD-01～GD-08", text)
                self.assertIn("principles.md#goal-drift", text)
                headings = re.findall(r"^## .+", text, re.MULTILINE)
                self.assertEqual(len(headings), len(set(headings)))

    def test_thin_channel_returns_same_check_without_mutating_instances(self):
        with tempfile.TemporaryDirectory(prefix="gg-drift-guidance-") as tmp:
            root = Path(tmp)
            sentinel = root / "user.txt"
            sentinel.write_bytes(b"unchanged\n")
            server = MCPServer(root)
            server.handle_initialize({"protocolVersion": "2024-11-05", "capabilities": {},
                                      "clientInfo": {"name": "test", "version": "1"}})
            for entry in ("govern", "audit"):
                with self.subTest(entry=entry):
                    args = {"task": "human request"}
                    if entry == "audit":
                        args["goal_id"] = "GOAL-002-test"
                    before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                    result = server.handle_tools_call({"name": entry, "arguments": args})["structuredContent"]
                    self.assertIsNone(result["promptSha256"])
                    for requirement in ("GD-01～GD-08", "principles.md#goal-drift", "直接父目标",
                                        "原始立项", "实际交付", "required", "合法贡献子集"):
                        self.assertIn(requirement, result["guidance"])
                    self.assertEqual(result["readonly"], entry == "audit")
                    self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()
