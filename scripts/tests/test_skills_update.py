from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"
SCRIPTS = REPO_ROOT / "scripts"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


update = _load("skills_update", SKILLS / "update.py")
pack = _load("pack_skills_release_for_update", SCRIPTS / "pack_skills_release.py")


def _args(target: Path, result, **overrides):
    values = {
        "version": result.version,
        "latest": False,
        "target_dir": str(target),
        "skills_dir": "skills",
        "zip_path": str(result.zip_path),
        "sha256_path": str(result.sha256_path),
        "repo": "magicvr/goal-governance",
        "release_tag": "",
        "allow_protocol_upgrade": False,
        "force_managed": False,
        "dry_run": False,
        "skip_install": True,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class SkillsUpdateTests(unittest.TestCase):
    def test_safe_extract_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("package/../../escape.txt", "bad")
            with self.assertRaisesRegex(update.UpdateError, "unsafe archive member"):
                update.safe_extract(archive, root / "extract")

    def test_offline_dry_run_verifies_digest_and_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "consumer"
            target.mkdir()
            shutil.copytree(SKILLS, target / "skills")
            result = pack.pack_skills(
                version="0.0.0-testupdate",
                output_dir=root / "dist",
                skills_root=SKILLS,
                skip_stage=True,
            )
            report = update.update_package(_args(target, result, dry_run=True))
            self.assertEqual(report["result"], "dry-run")
            self.assertEqual(report["current_protocol"], report["incoming_protocol"])
            self.assertEqual(len(report["archive_sha256"]), 64)

    def test_offline_update_writes_state_and_keeps_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "consumer"
            target.mkdir()
            shutil.copytree(SKILLS, target / "skills")
            (target / "skills" / "old-marker.txt").write_text("old\n", encoding="utf-8")
            result = pack.pack_skills(
                version="0.0.0-testupdate",
                output_dir=root / "dist",
                skills_root=SKILLS,
                skip_stage=True,
            )
            report = update.update_package(_args(target, result))
            self.assertEqual(report["result"], "updated")
            self.assertTrue((target / "skills" / ".goal-governance-install.json").is_file())
            rollback = Path(str(report["rollback_path"]))
            self.assertTrue((rollback / "skills" / "old-marker.txt").is_file())

    @unittest.skipUnless(sys.platform.startswith("win"), "real installer path is Windows-first")
    def test_offline_update_runs_real_consumer_installer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "consumer"
            target.mkdir()
            shutil.copytree(SKILLS, target / "skills")
            result = pack.pack_skills(
                version="0.0.0-testupdate",
                output_dir=root / "dist",
                skills_root=SKILLS,
                skip_stage=True,
            )

            report = update.update_package(_args(target, result, skip_install=False))

            self.assertEqual(report["result"], "updated")
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue(
                (target / ".agents" / "skills" / "govern" / "SKILL.md").is_file()
            )
            self.assertTrue(
                (target / "skills" / "contracts" / "skills-consumer-contract.json").is_file()
            )
            for producer_only in (
                "skills-consumer-compatibility-matrix.schema.json",
                "skills-consumer-compatibility-matrix.json",
                "runtime-evidence.schema.json",
            ):
                self.assertFalse(
                    (target / "skills" / "contracts" / producer_only).exists(),
                    msg=f"producer-only evidence shipped to consumer update: {producer_only}",
                )

    def test_install_failure_restores_previous_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "consumer"
            target.mkdir()
            shutil.copytree(SKILLS, target / "skills")
            marker = target / "skills" / "old-marker.txt"
            marker.write_text("old\n", encoding="utf-8")
            result = pack.pack_skills(
                version="0.0.0-testupdate",
                output_dir=root / "dist",
                skills_root=SKILLS,
                skip_stage=True,
            )
            with mock.patch.object(update, "run_installer", side_effect=update.UpdateError("boom")):
                with self.assertRaisesRegex(update.UpdateError, "boom"):
                    update.update_package(_args(target, result, skip_install=False))
            self.assertEqual(marker.read_text(encoding="utf-8"), "old\n")

    def test_new_managed_path_conflicts_and_rolls_back_when_install_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "consumer"
            target.mkdir()
            shutil.copytree(SKILLS, target / "skills")
            incoming_skills = root / "incoming-skills"
            shutil.copytree(SKILLS, incoming_skills)
            new_source = incoming_skills / "install" / "codex" / "skills" / "new-surface" / "SKILL.md"
            new_source.parent.mkdir(parents=True)
            new_source.write_text("incoming managed file\n", encoding="utf-8")
            new_destination = target / ".agents" / "skills" / "new-surface" / "SKILL.md"
            new_destination.parent.mkdir(parents=True)
            new_destination.write_text("local unmanaged file\n", encoding="utf-8")

            modified = update.modified_managed_files(
                target / "skills",
                target,
                incoming_skills,
            )
            self.assertIn(new_destination, modified)

            new_destination.unlink()
            result = pack.pack_skills(
                version="0.0.0-testupdate",
                output_dir=root / "dist",
                skills_root=incoming_skills,
                skip_stage=True,
            )

            def fail_after_new_write(package: Path, consumer: Path) -> None:
                written = consumer / ".agents" / "skills" / "new-surface" / "SKILL.md"
                written.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(
                    package / "install" / "codex" / "skills" / "new-surface" / "SKILL.md",
                    written,
                )
                raise update.UpdateError("boom after new managed write")

            with mock.patch.object(update, "run_installer", side_effect=fail_after_new_write):
                with self.assertRaisesRegex(update.UpdateError, "boom after new managed write"):
                    update.update_package(_args(target, result, skip_install=False))

            self.assertFalse(new_destination.exists())

    def test_managed_file_conflict_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            shutil.copytree(SKILLS, target / "skills")
            (target / "AGENTS.md").write_text("local customization\n", encoding="utf-8")
            modified = update.modified_managed_files(target / "skills", target)
            self.assertIn(target / "AGENTS.md", modified)


if __name__ == "__main__":
    unittest.main()
