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
CLAUDE_GOVERN_SKILL = (
    SKILLS_ROOT / "install" / "claude" / "skills" / "govern" / "SKILL.md"
)
CLAUDE_AUDIT_SKILL = (
    SKILLS_ROOT / "install" / "claude" / "skills" / "audit" / "SKILL.md"
)
GROK_GOVERN_SKILL = SKILLS_ROOT / "install" / "grok" / "skills" / "govern" / "SKILL.md"
GROK_AUDIT_SKILL = SKILLS_ROOT / "install" / "grok" / "skills" / "audit" / "SKILL.md"
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
        # Defaults / confirm-with-user (positive framing)
        self.assertRegex(text, r"仓库根")
        self.assertRegex(text, r"默认策略|待确认|问用户")
        self.assertRegex(text, r"web/")  # as optional project convention example
        self.assertRegex(text, r"完成标准|硬约束")
        # GOAL-005 phase B: opinion ledger + user gates
        self.assertRegex(text, r"意见台账|P-004|开放必改")
        self.assertRegex(text, r"independent|交叉")
        self.assertRegex(text, r"S4|审计响应")
        self.assertIn("05-independent-audit", text)

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
        audit04 = (PROMPTS / "04-write-audit.md").read_text(encoding="utf-8")
        self.assertRegex(audit04, r"source")
        self.assertRegex(audit04, r"verdict")
        self.assertRegex(audit04, r"independent|self")

    def test_independent_audit_prompt_exists(self) -> None:
        path = PROMPTS / "05-independent-audit.md"
        self.assertTrue(path.is_file(), f"missing independent audit core: {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("independent", text)
        self.assertRegex(text, r"03-audit")
        self.assertRegex(text, r"status|progress")
        self.assertRegex(text, r"govern|/govern")

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

    def test_install_default_slash_is_govern_and_audit_opt_in_primitives(self) -> None:
        """Default install: /govern + /audit; form-fill primitives stay opt-in."""
        sh = INSTALL_SH.read_text(encoding="utf-8")
        ps1 = INSTALL_PS1.read_text(encoding="utf-8")
        self.assertIn("--with-primitives", sh)
        self.assertRegex(ps1, r"WithPrimitives|with-primitives")
        self.assertIn("WRAPPER_NAMES=(govern audit)", sh)
        self.assertIn("$wrapperNames = @('govern', 'audit')", ps1)
        self.assertIn("INSTALL_PRIMITIVE_WRAPPERS", sh)
        self.assertIn("$WithPrimitives", ps1)
        self.assertIn("new-goal", sh)
        self.assertIn("new-goal", ps1)
        self.assertRegex(sh, r"skills/audit|audit/SKILL")
        self.assertRegex(ps1, r"skills\\audit|audit\\SKILL")
        self.assertRegex(sh, r"INSTALL_PRIMITIVE_WRAPPERS.*1|with-primitives")

    def test_agents_template_does_not_force_web_app_dir(self) -> None:
        text = (SKILLS_ROOT / "AGENTS.template.md").read_text(encoding="utf-8")
        self.assertIn("代码与文档边界", text)
        self.assertRegex(text, r"仓库根")
        self.assertRegex(text, r"默认策略|问用户|待确认")
        self.assertRegex(text, r"web/")
        self.assertRegex(text, r"正确做法|硬约束")
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
                r"SKILLS_PKG|改名|也可改名|其他名字|其他名",
                msg=f"{label} should allow renamed skills package",
            )
        self.assertRegex(template, r"architecture 可选|architecture.*可选|有 architecture")
        self.assertRegex(orch, r"若存在|一并参考|architecture")
        self.assertRegex(govern, r"若存在|architecture")
        self.assertNotIn("GOAL-001-main-vision", orch)
        self.assertNotIn("GOAL-001-main-vision", (PROMPTS / "01-create-new-goal.md").read_text(encoding="utf-8"))
        self.assertIn("SKILLS_PKG", orch)
        # Prefer positive defaults over long ban-lists
        ban_hits = len(__import__("re").findall(r"^[-*]\s*禁止", orch, flags=__import__("re").M))
        self.assertLessEqual(ban_hits, 2, "orchestrator should not be a ban-list prompt")

    def test_skills_readme_documents_primary_and_audit_paths(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("/govern", text)
        self.assertIn("/audit", text)
        self.assertIn("00-govern-orchestrator", text)
        self.assertIn("05-independent-audit", text)
        self.assertRegex(text, r"primary|主入口")
        self.assertRegex(text, r"primitive|原语|advanced")
        self.assertRegex(text, r"with-primitives|WithPrimitives")
        self.assertRegex(text, r"Claude|\.claude")
        self.assertRegex(text, r"Grok|\.grok")
        self.assertIn("SKILL.md", text)

    def test_skills_readme_default_install_documents_govern_and_audit(self) -> None:
        """F-017 guard: README manual/script sections must match default govern+audit surface."""
        text = README.read_text(encoding="utf-8")
        norm = text.replace("\\", "/")
        # Manual install: both skills/paths for each host family
        self.assertIn(".claude/skills/audit", norm)
        self.assertIn(".grok/skills/audit", norm)
        self.assertRegex(text, r"audit\.prompt\.md|prompts/audit")
        self.assertIn("skills/audit/SKILL.md", norm)
        # Must not revive the old "Copilot = only govern prompt" claim
        self.assertNotIn("仅** govern prompt", text)
        self.assertNotIn("**仅** govern prompt", text)
        self.assertNotRegex(text, r"(?i)--copilot[^\n]{0,80}仅\s*govern\s*prompt")
        # Explicit default surface language
        self.assertRegex(text, r"`/govern`\s*\+\s*`/audit`")
        self.assertRegex(text, r"--claude[^\n]*audit", re.I)
        self.assertRegex(text, r"--grok[^\n]*audit", re.I)
        self.assertRegex(text, r"--copilot[^\n]*(audit|默认双入口)", re.I)

    def _assert_primary_govern_skill(self, path: Path, host_label: str) -> None:
        self.assertTrue(path.is_file(), f"missing {host_label} skill: {path}")
        text = path.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^name:\s*govern\s*$")
        self.assertRegex(text, r"description:")
        self.assertIn("00-govern-orchestrator", text)
        self.assertRegex(text, r"SKILLS_PKG|prompts/00-govern")
        self.assertRegex(text, r"设立目标|set-goal|推进|lifecycle|生命周期")
        self.assertRegex(text, r"primary|主入口|单一")
        # Must not present four form ops as the default product surface
        self.assertNotRegex(
            text,
            r"(?i)default.*(new-goal|log-decision|四选一|填表菜单)",
        )

    def test_claude_govern_skill_source(self) -> None:
        self._assert_primary_govern_skill(CLAUDE_GOVERN_SKILL, "Claude Code")

    def test_grok_govern_skill_source(self) -> None:
        self._assert_primary_govern_skill(GROK_GOVERN_SKILL, "Grok Build")

    def _assert_audit_skill(self, path: Path, host_label: str) -> None:
        self.assertTrue(path.is_file(), f"missing {host_label} audit skill: {path}")
        text = path.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^name:\s*audit\s*$")
        self.assertIn("05-independent-audit", text)
        self.assertRegex(text, r"independent|交叉")
        self.assertRegex(text, r"status|progress")

    def test_claude_audit_skill_source(self) -> None:
        self._assert_audit_skill(CLAUDE_AUDIT_SKILL, "Claude Code")

    def test_grok_audit_skill_source(self) -> None:
        self._assert_audit_skill(GROK_AUDIT_SKILL, "Grok Build")

    def test_copilot_audit_wrapper(self) -> None:
        path = COPILOT_PROMPTS / "audit.md"
        self.assertTrue(path.is_file(), f"missing audit wrapper: {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("/audit", text)
        self.assertIn("05-independent-audit", text)
        self.assertRegex(text, r"independent|交叉")

    def test_install_scripts_wire_claude_and_grok_skills(self) -> None:
        sh = INSTALL_SH.read_text(encoding="utf-8")
        ps1 = INSTALL_PS1.read_text(encoding="utf-8")
        for text, label in ((sh, "install.sh"), (ps1, "install.ps1")):
            self.assertRegex(text, r"--grok|-Grok", msg=f"{label} needs grok flag")
            self.assertIn(".claude/skills/govern", text.replace("\\", "/"))
            self.assertIn(".grok/skills/govern", text.replace("\\", "/"))
            self.assertIn("audit", text)
            self.assertIn("SKILL.md", text)
            self.assertRegex(text, r"00-govern-orchestrator")
            self.assertRegex(text, r"05-independent-audit")


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    # Allow `python test_skills_orchestrator.py` without -m
    raise SystemExit(main())
