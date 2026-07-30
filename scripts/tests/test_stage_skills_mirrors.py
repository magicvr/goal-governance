"""Unit tests for scripts/stage_skills_mirrors.py."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STAGE_SCRIPT = REPO_ROOT / "scripts" / "stage_skills_mirrors.py"


def _load_stage_module():
    spec = importlib.util.spec_from_file_location("stage_skills_mirrors", STAGE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STAGE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["stage_skills_mirrors"] = module
    spec.loader.exec_module(module)
    return module


stage = _load_stage_module()


def _write(path: Path, text: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _mini_repo(base: Path) -> Path:
    docs = base / "docs"
    skills = base / "skills"
    for name in (
        "principles.md",
        "workspace-protocol.md",
        "overview.md",
        "directory-layout.md",
    ):
        _write(docs / "architecture" / name, f"# {name}\n")
    _write(docs / "architecture" / "tech-stack.md", "# tech\n")
    _write(docs / "templates" / "goal-folder" / "00-meta.md", "# meta\n")
    _write(docs / "templates" / "workspace-context.md", "# ws\n")
    _write(docs / "templates" / "README.md", "# tmpl\n")
    _write(docs / "vision" / "alignment.md", "# align\n")
    _write(docs / "contracts" / "skills-consumer-contract.json", "{}\n")
    # Hand-maintained consumer files required by stage
    _write(skills / "core" / "docs" / "README.md", "# slim\n")
    _write(skills / "core" / "docs" / "vision" / "README.md", "# vision slim\n")
    # Legacy third copy that stage must remove
    _write(skills / "templates" / "goal-folder" / "00-meta.md", "# stale\n")
    _write(skills / "templates" / "workspace-context.md", "# stale ws\n")
    return base


class StageSkillsMirrorsTests(unittest.TestCase):
    def test_stage_copies_and_strips_legacy_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _mini_repo(Path(tmp))
            result = stage.stage_skills_mirrors(root, check=False, dry_run=False)
            self.assertGreaterEqual(result.copied, 1)
            self.assertFalse((root / "skills" / "templates" / "goal-folder").exists())
            self.assertTrue((root / "skills" / "templates" / "README.md").is_file())
            self.assertEqual(
                (root / "docs" / "architecture" / "principles.md").read_bytes(),
                (root / "skills" / "core" / "docs" / "architecture" / "principles.md").read_bytes(),
            )
            self.assertEqual(
                (root / "docs" / "contracts" / "skills-consumer-contract.json").read_bytes(),
                (root / "skills" / "contracts" / "skills-consumer-contract.json").read_bytes(),
            )
            self.assertFalse(
                (root / "skills" / "core" / "docs" / "architecture" / "tech-stack.md").is_file()
            )
            # protected slim readme not overwritten by monorepo
            self.assertEqual(
                (root / "skills" / "core" / "docs" / "README.md").read_text(encoding="utf-8"),
                "# slim\n",
            )
            check = stage.stage_skills_mirrors(root, check=True, dry_run=False)
            self.assertEqual(check.mode, "check")

    def test_check_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _mini_repo(Path(tmp))
            stage.stage_skills_mirrors(root, check=False, dry_run=False)
            mirror = root / "skills" / "core" / "docs" / "architecture" / "principles.md"
            mirror.write_text("# drifted\n", encoding="utf-8")
            with self.assertRaises(stage.StageSkillsError):
                stage.stage_skills_mirrors(root, check=True, dry_run=False)

    def test_repo_root_stage_check_clean_after_write(self) -> None:
        if not (REPO_ROOT / "docs" / "architecture" / "principles.md").is_file():
            self.skipTest("not a full monorepo checkout")
        stage.stage_skills_mirrors(REPO_ROOT, check=False, dry_run=False)
        stage.stage_skills_mirrors(REPO_ROOT, check=True, dry_run=False)


if __name__ == "__main__":
    unittest.main()
