"""R3 canonical governance_root tests (VP-004 R3 / V-F-013 车辆).

Asserts the authoritative surface (alignment / workspace-protocol / root
AGENTS / templates) no longer hardcodes "repository root docs/" without
exception: path narratives are governance_root-relative (default docs) with an
exception note, and the mirror stage stays clean (``stage_skills_mirrors.py
--check`` is enforced by CI and the stage test suite).
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


class GovernanceRootCanonicalTests(unittest.TestCase):
    """C4: canonical path narratives are governance_root-relative."""

    def _read(self, *parts: str) -> str:
        path = REPO_ROOT.joinpath(*parts)
        self.assertTrue(path.is_file(), msg=f"missing {path}")
        return path.read_text(encoding="utf-8")

    def test_alignment_defines_governance_root_and_exception(self) -> None:
        text = self._read("docs", "vision", "alignment.md")
        self.assertIn("治理根（`governance_root`", text)
        self.assertIn(".goal-governance.json", text)
        self.assertIn("fail closed", text)
        self.assertIn("monorepo 生产仓固定 `governance_root = docs`", text)

    def test_alignment_mci_table_is_governance_root_relative(self) -> None:
        text = self._read("docs", "vision", "alignment.md")
        for cell in (
            "| 文档入口 | `{governance_root}/README.md`",
            "| 愿景实例 | `{governance_root}/vision/charter.md`",
            "| 意图 | 至少一个 `{governance_root}/vision/plans/VP-*.md`",
            "| 工作区 | 显式 `{governance_root}/workspace-<NNN>-<slug>/workspace.md`",
        ):
            self.assertIn(cell, text, msg=f"alignment MCI row not relativized: {cell}")
        # 关键行不再以裸 docs/ 硬编码（MCI 权威表路径列）。
        self.assertNotIn("| `docs/README.md`", text)
        self.assertNotIn("| `docs/vision/charter.md`（`status: active`）", text)

    def test_workspace_protocol_defines_governance_root(self) -> None:
        text = self._read("docs", "architecture", "workspace-protocol.md")
        self.assertIn("治理根（`governance_root`", text)
        self.assertIn("{governance_root}/workspace-<NNN>-<slug>/", text)
        self.assertIn("{governance_root}/vision/plans/VP-*.md", text)
        self.assertIn("fail closed", text)

    def test_root_agents_defines_governance_root(self) -> None:
        text = self._read("AGENTS.md")
        self.assertIn("治理根（`governance_root`，默认 `docs`）", text)
        self.assertIn("{governance_root}/vision/", text)
        self.assertIn("{governance_root}/architecture/principles.md", text)
        self.assertIn("monorepo 生产仓固定 `governance_root = docs`", text)

    def test_templates_are_governance_root_relative(self) -> None:
        context = self._read("docs", "templates", "workspace-context.md")
        self.assertIn("{governance_root}/workspace-001-example/", context)
        self.assertIn("复制本模板为 `{governance_root}/workspace-001-example/workspace.md`", context)
        charter = self._read("docs", "templates", "vision", "charter.md")
        self.assertIn("{governance_root}/vision/charter.md", charter)
        plan = self._read("docs", "templates", "vision", "vision-plan.md")
        self.assertIn("{governance_root}/vision/plans/VP-NNN-slug.md", plan)

    def test_mcp_config_schema_ships_with_package(self) -> None:
        schema = REPO_ROOT / "mcp" / "governance-root.schema.json"
        self.assertTrue(schema.is_file())
        text = schema.read_text(encoding="utf-8")
        self.assertIn("governance_root", text)


if __name__ == "__main__":
    unittest.main()
