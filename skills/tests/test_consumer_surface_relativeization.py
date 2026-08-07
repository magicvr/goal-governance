"""GOAL-006 S2: consumer-surface path relativeization guard (F-006 / R-001).

Ensures the distributed consumer surface (governance prompts, AGENTS template,
MCP thin shell) carries no bare ``docs/`` protocol-path references, and that
canonical R-001 sweep files do not regress into protocol-semantic ``docs/``
prefixes (directory trees and monorepo-internal paths are allowed).
"""
from __future__ import annotations

import pathlib
import re
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"

# Package-internal mirror path (real directory); excluded from the guard.
BARE_DOCS = re.compile(r"(?<!core/)docs/")

# Protocol-semantic prefixes that must stay relativeized in canonical files.
# The core/ lookbehind keeps package-internal mirror paths (skills/core/docs/*).
PROTOCOL_PREFIXES = (
    "docs/workspace-",
    "docs/shared-materials/",
    "docs/architecture/",
    "docs/templates/",
    "docs/contracts/",
    "docs/vision/",
    "docs/goals/",
    "docs/_index/",
    "docs/README.md",
)
PROMPTS = [
    "00-govern-orchestrator.md",
    "05-independent-audit.md",
    "06-vision-orchestrator.md",
    "07-independent-vision-review.md",
    "01-create-new-goal.md",
    "02-record-decision.md",
    "03-update-execution.md",
    "04-write-audit.md",
]

# Files fully relativeized: no bare docs/ allowed at all.
FULLY_RELATIVEIZED = [
    *[f"prompts/{name}" for name in PROMPTS],
    "AGENTS.template.md",
    "../mcp/lifecycle.py",
]

# Installed-surface copies (GOAL-006 S2): AGENTS template copies and SKILL.md
# shells shipped inside the package plus repo-root dogfood installs.
INSTALLED_SURFACE = [
    "install/claude/AGENTS.md",
    "install/copilot/copilot-instructions.md",
    "install/claude/skills/audit/SKILL.md",
    "install/claude/skills/govern/SKILL.md",
    "install/claude/skills/vision/SKILL.md",
    "install/claude/skills/vision-audit/SKILL.md",
    "install/codex/skills/audit/SKILL.md",
    "install/codex/skills/govern/SKILL.md",
    "install/codex/skills/vision/SKILL.md",
    "install/codex/skills/vision-audit/SKILL.md",
    "install/grok/skills/audit/SKILL.md",
    "install/grok/skills/govern/SKILL.md",
    "install/grok/skills/vision/SKILL.md",
    "install/grok/skills/vision-audit/SKILL.md",
    "install/copilot/prompts/audit.md",
    "install/copilot/prompts/govern.md",
    "install/copilot/prompts/new-goal.md",
    "install/copilot/prompts/vision-audit.md",
    "install/copilot/prompts/vision.md",
]

# Repo-root dogfood installs (tracked): same rule as installed shells.
DOGFOOD = [
    ".grok/skills/audit/SKILL.md",
    ".grok/skills/govern/SKILL.md",
    ".grok/skills/vision/SKILL.md",
    ".grok/skills/vision-audit/SKILL.md",
    ".claude/skills/audit/SKILL.md",
    ".claude/skills/govern/SKILL.md",
    ".claude/skills/vision/SKILL.md",
    ".claude/skills/vision-audit/SKILL.md",
    ".agents/skills/audit/SKILL.md",
    ".agents/skills/govern/SKILL.md",
    ".agents/skills/vision/SKILL.md",
    ".agents/skills/vision-audit/SKILL.md",
    ".github/prompts/audit.prompt.md",
    ".github/prompts/govern.prompt.md",
    ".github/prompts/vision-audit.prompt.md",
    ".github/prompts/vision.prompt.md",
]

# R-001 sweep files: protocol-semantic prefixes forbidden; layout trees kept.
SWEEP_FILES = [
    "docs/README.md",
    "docs/architecture/overview.md",
    "docs/architecture/directory-layout.md",
]


class ConsumerSurfaceRelativeizationTests(unittest.TestCase):
    maxDiff = None

    def test_prompts_template_lifecycle_have_no_bare_docs(self) -> None:
        for rel in FULLY_RELATIVEIZED:
            path = (SKILLS / rel).resolve() if rel != "../mcp/lifecycle.py" else (
                REPO_ROOT / "mcp" / "lifecycle.py"
            )
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                text = path.read_text(encoding="utf-8")
                matches = BARE_DOCS.findall(text)
                self.assertEqual(
                    matches,
                    [],
                    f"bare docs/ references must be relativeized (F-006): "
                    f"{len(matches)} found",
                )

    def test_installed_surface_and_dogfood_have_no_bare_docs(self) -> None:
        for rel in [*INSTALLED_SURFACE, *DOGFOOD]:
            path = SKILLS / rel if rel.startswith("install/") else REPO_ROOT / rel
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                text = path.read_text(encoding="utf-8")
                matches = BARE_DOCS.findall(text)
                self.assertEqual(
                    matches,
                    [],
                    f"installed/dogfood surface must stay relativeized (F-006): "
                    f"{len(matches)} found",
                )

    def test_template_carries_governance_root_placeholder(self) -> None:
        template = (SKILLS / "AGENTS.template.md").read_text(encoding="utf-8")
        self.assertIn("{{GOVERNANCE_ROOT}}", template)
        self.assertIn("governance_root", template)

    def test_prompts_carry_governance_root_literal(self) -> None:
        for name in PROMPTS:
            text = (SKILLS / "prompts" / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("{governance_root}", text)

    def test_r001_sweep_files_have_no_protocol_semantic_docs_prefix(self) -> None:
        for rel in SWEEP_FILES:
            path = REPO_ROOT / rel
            text = path.read_text(encoding="utf-8")
            for prefix in PROTOCOL_PREFIXES:
                with self.subTest(file=rel, prefix=prefix):
                    pattern = re.compile(r"(?<!core/)" + re.escape(prefix))
                    self.assertIsNone(
                        pattern.search(text),
                        f"protocol-semantic prefix must stay relativeized (R-001): {prefix}",
                    )


if __name__ == "__main__":
    unittest.main()
