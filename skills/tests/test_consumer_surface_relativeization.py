"""GOAL-006 S2: consumer-surface path relativeization guard (F-006 / R-001).

Ensures the distributed consumer surface (governance prompts, AGENTS template,
MCP thin shell) carries no bare ``docs/`` protocol-path references, and that
canonical R-001 sweep files do not regress into protocol-semantic ``docs/``
prefixes (directory trees and monorepo-internal paths are allowed).
"""
from __future__ import annotations

import pathlib
import re
import tempfile
import unittest
from pathlib import Path

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
    # Copilot rule surface (independent audit F-001): unconfigured template copy.
    ".github/copilot-instructions.md",
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


class ConsumerSurfaceE2ETests(unittest.TestCase):
    """F-003: governance_root != docs consumer-scenario e2e.

    Materializes a simulated consumer repo whose governance root is a non-docs
    directory, installs the distributed surface (AGENTS template pinned at
    install time, SKILL.md shells), and asserts every rule path reference
    reads under the configured root with no docs/ leakage.
    """

    NON_DOCS_ROOT = "governance"  # non-default governance root for the scenario

    @staticmethod
    def _materialize_consumer(tmp: Path) -> Path:
        consumer = tmp / "consumer"
        (consumer / "governance").mkdir(parents=True)
        # Governance root config (R3 machinery): non-docs root.
        (consumer / ".goal-governance.json").write_text(
            '{"governance_root": "governance"}\n', encoding="utf-8"
        )
        # AGENTS.md: template copy with {{GOVERNANCE_ROOT}} pinned to the
        # consumer's actual root at install time (D-001 A+C).
        template = (SKILLS / "AGENTS.template.md").read_text(encoding="utf-8")
        agents = template.replace("{{GOVERNANCE_ROOT}}", ConsumerSurfaceE2ETests.NON_DOCS_ROOT)
        (consumer / "AGENTS.md").write_text(agents, encoding="utf-8")
        # Installed shells: prompts condensation with the literal placeholder.
        for name in ("govern", "audit", "vision", "vision-audit"):
            shell = (
                SKILLS / "install" / "claude" / "skills" / name / "SKILL.md"
            ).read_text(encoding="utf-8")
            dest = consumer / "governance" / "skills" / name / "SKILL.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(shell, encoding="utf-8")
        return consumer

    @staticmethod
    def _path_references(text: str) -> list[str]:
        """Extract backticked path-like references (relative root paths)."""
        return [
            token.strip("`").strip()
            for token in re.findall(r"`([^`]+)`", text)
            if re.match(r"^(?:governance|\{governance_root\})/", token)
        ]

    def test_pinned_agents_reads_paths_under_non_docs_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-e2e-agents-") as tmp:
            consumer = self._materialize_consumer(Path(tmp))
            agents = (consumer / "AGENTS.md").read_text(encoding="utf-8")
            # No bare docs/ anywhere in the installed rule file.
            self.assertEqual(BARE_DOCS.findall(agents), [])
            # Key protocol paths now read under the non-docs root.
            for fragment in (
                "governance/architecture/principles.md",
                "governance/workspace-<NNN>-<slug>/",
                "governance/vision/",
                "governance/templates/",
                "governance/goals/",
                "governance/README.md",
            ):
                self.assertIn(fragment, agents, msg=f"missing {fragment}")

    def test_installed_shells_read_paths_under_governance_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-e2e-shells-") as tmp:
            consumer = self._materialize_consumer(Path(tmp))
            for name in ("govern", "audit", "vision", "vision-audit"):
                shell = (consumer / "governance" / "skills" / name / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                with self.subTest(shell=name):
                    self.assertEqual(BARE_DOCS.findall(shell), [])
                    self.assertIn("{governance_root}/", shell)

    def test_all_path_references_resolve_under_configured_root(self) -> None:
        """Every rule path reference must resolve under the non-docs root."""
        with tempfile.TemporaryDirectory(prefix="gg-e2e-paths-") as tmp:
            consumer = self._materialize_consumer(Path(tmp))
            surfaces = [consumer / "AGENTS.md"]
            surfaces += sorted((consumer / "governance" / "skills").rglob("SKILL.md"))
            for path in surfaces:
                text = path.read_text(encoding="utf-8")
                refs = self._path_references(text)
                with self.subTest(path=str(path.relative_to(consumer))):
                    self.assertTrue(refs, "expected at least one path reference")
                    for ref in refs:
                        self.assertFalse(
                            ref.startswith("docs/"),
                            f"path reference must not leak docs/: {ref}",
                        )
                        self.assertTrue(
                            ref.startswith(self.NON_DOCS_ROOT)
                            or ref.startswith("{governance_root}"),
                            f"path reference must read under the configured root: {ref}",
                        )


if __name__ == "__main__":
    unittest.main()
