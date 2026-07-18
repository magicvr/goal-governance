#!/usr/bin/env python3
"""Structural contract tests for Skills primary orchestrator package.

Drives real shipped files under skills/ (prompts, wrappers, install scripts).
Run from repo root or skills/: python skills/tests/test_skills_orchestrator.py
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1]
PROMPTS = SKILLS_ROOT / "prompts"
COPILOT_PROMPTS = SKILLS_ROOT / "install" / "copilot" / "prompts"
INSTALL_SH = SKILLS_ROOT / "install.sh"
INSTALL_PS1 = SKILLS_ROOT / "install.ps1"
README = SKILLS_ROOT / "README.md"


class TestSkillsOrchestratorPackage(unittest.TestCase):
    def test_primary_orchestrator_file_exists(self) -> None:
        path = PROMPTS / "00-govern-orchestrator.md"
        self.assertTrue(path.is_file(), f"missing primary orchestrator: {path}")

    def test_orchestrator_encodes_lifecycle_and_classification(self) -> None:
        text = (PROMPTS / "00-govern-orchestrator.md").read_text(encoding="utf-8")
        # Lifecycle language
        self.assertIn("设立目标", text)
        self.assertIn("推进", text)
        self.assertRegex(text, r"审计|关门")
        # Classification / scan
        self.assertIn("goal-tree", text)
        self.assertRegex(text, r"S0|情境|分类")
        self.assertRegex(text, r"未关门|总目的")
        # Confirm before write + primitives
        self.assertRegex(text, r"确认")
        for name in (
            "01-create-new-goal",
            "02-record-decision",
            "03-update-execution",
            "04-write-audit",
        ):
            self.assertIn(name, text)
        # Primary role marker
        self.assertRegex(text, r"主入口|primary|单一")
        # Layout / project-nature must not be hard-coded to web/ or empty=non-code
        self.assertRegex(text, r"仓库根|普遍")
        self.assertRegex(text, r"先验|不得.*断定|问用户|由用户")
        self.assertRegex(text, r"web/")  # mentioned as non-universal / forbidden assumption

    def test_primitives_exist_and_marked(self) -> None:
        for fname in (
            "01-create-new-goal.md",
            "02-record-decision.md",
            "03-update-execution.md",
            "04-write-audit.md",
        ):
            path = PROMPTS / fname
            self.assertTrue(path.is_file(), f"missing primitive: {path}")
            body = path.read_text(encoding="utf-8")
            self.assertRegex(
                body,
                r"primitive|原语",
                msg=f"{fname} should label itself as primitive",
            )

    def test_prompts_readme_primary_vs_primitive(self) -> None:
        text = (PROMPTS / "README.md").read_text(encoding="utf-8")
        self.assertIn("00-govern-orchestrator", text)
        self.assertRegex(text, r"primary|主入口")
        self.assertRegex(text, r"primitive|原语")

    def test_copilot_govern_wrapper_is_primary(self) -> None:
        path = COPILOT_PROMPTS / "govern.md"
        self.assertTrue(path.is_file(), f"missing primary wrapper: {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("/govern", text)
        self.assertIn("00-govern-orchestrator", text)
        self.assertRegex(text, r"primary|主入口")

    def test_install_scripts_install_govern(self) -> None:
        sh = INSTALL_SH.read_text(encoding="utf-8")
        ps1 = INSTALL_PS1.read_text(encoding="utf-8")
        self.assertRegex(sh, r"govern")
        self.assertRegex(ps1, r"govern")
        self.assertRegex(sh, r"00-govern-orchestrator|/govern")
        self.assertRegex(ps1, r"00-govern-orchestrator|/govern")

    def test_install_default_slash_is_govern_only_opt_in_primitives(self) -> None:
        """Default install must not always ship four form-filling slash wrappers."""
        sh = INSTALL_SH.read_text(encoding="utf-8")
        ps1 = INSTALL_PS1.read_text(encoding="utf-8")
        self.assertIn("--with-primitives", sh)
        self.assertRegex(ps1, r"WithPrimitives|with-primitives")
        # Default list is govern-only; advanced names only under the opt-in flag path
        self.assertRegex(sh, r'WRAPPER_NAMES=\(govern\)|WRAPPER_NAMES=\("govern"\)|WRAPPER_NAMES=\(govern\)')
        self.assertIn("WRAPPER_NAMES=(govern)", sh)
        self.assertIn("$wrapperNames = @('govern')", ps1)
        self.assertIn("INSTALL_PRIMITIVE_WRAPPERS", sh)
        self.assertIn("$WithPrimitives", ps1)
        # Advanced names still exist as sources, but gated
        self.assertIn("new-goal", sh)
        self.assertIn("new-goal", ps1)
        self.assertRegex(sh, r"INSTALL_PRIMITIVE_WRAPPERS.*1|with-primitives")

    def test_agents_template_does_not_force_web_app_dir(self) -> None:
        text = (SKILLS_ROOT / "AGENTS.template.md").read_text(encoding="utf-8")
        self.assertIn("代码与文档边界", text)
        self.assertRegex(text, r"仓库根|普遍形态")
        self.assertRegex(text, r"禁止.*web/|不是.*通用|未约定")
        self.assertRegex(text, r"刚装|先验|用户决定")
        self.assertNotRegex(
            text,
            r"应用代码仅在 `\{\{APP_DIR\}\}`",
            msg="template must not force APP_DIR-only application code",
        )

    def test_portability_skills_pkg_and_optional_architecture(self) -> None:
        """Reusable package must not require ./skills name or architecture/."""
        template = (SKILLS_ROOT / "AGENTS.template.md").read_text(encoding="utf-8")
        orch = (PROMPTS / "00-govern-orchestrator.md").read_text(encoding="utf-8")
        govern = (COPILOT_PROMPTS / "govern.md").read_text(encoding="utf-8")
        for text, label in (
            (template, "AGENTS.template"),
            (orch, "orchestrator"),
            (govern, "govern wrapper"),
        ):
            self.assertRegex(
                text,
                r"SKILLS_PKG|改名|可能不是 `skills`|不是 `skills`",
                msg=f"{label} should allow renamed skills package",
            )
            self.assertRegex(
                text,
                r"architecture.*可选|不要求.*architecture|仅当存在|若存在",
                msg=f"{label} should treat architecture as optional",
            )
        self.assertNotIn("GOAL-001-main-vision", orch)
        self.assertNotIn("GOAL-001-main-vision", (PROMPTS / "01-create-new-goal.md").read_text(encoding="utf-8"))
        # Orchestrator must locate package by content, not hard-coded ./skills only
        self.assertIn("SKILLS_PKG", orch)
        self.assertRegex(orch, r"main-vision")

    def test_skills_readme_documents_single_primary_path(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("/govern", text)
        self.assertIn("00-govern-orchestrator", text)
        self.assertRegex(text, r"primary|主入口")
        self.assertRegex(text, r"primitive|原语|advanced")
        self.assertRegex(text, r"with-primitives|WithPrimitives")
        self.assertRegex(text, r"仅.*govern|默认.*govern|/govern.*only|只装", re.I)


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    # Allow `python test_skills_orchestrator.py` without -m
    raise SystemExit(main())
