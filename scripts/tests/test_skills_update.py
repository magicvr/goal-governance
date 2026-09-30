from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
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
render = _load("skills_render_managed", SKILLS / "render_managed.py")
pack = _load("pack_skills_release_for_update", SCRIPTS / "pack_skills_release.py")


def _args(target: Path, result, **overrides):
    values = {
        "version": result.version,
        "latest": False,
        "target_dir": str(target),
        "skills_dir": "skills",
        "methodology_dir": "docs",
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

            def fail_after_new_write(
                package: Path,
                consumer: Path,
                *,
                methodology_dir: str,
                skills_dir: str,
            ) -> None:
                if methodology_dir != "docs" or skills_dir != "skills":
                    raise AssertionError(
                        f"unexpected installer tokens: {methodology_dir!r} {skills_dir!r}"
                    )
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

    def test_rendered_bytes_match_and_a_hand_edit_still_conflicts(self) -> None:
        """Update accepts the rendered bytes this module would write, and nothing else."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            package = target / "skills"
            source = SKILLS / "core" / "docs" / "architecture" / "principles.md"
            destination_source = package / "core" / "docs" / "architecture" / "principles.md"
            destination_source.parent.mkdir(parents=True)
            shutil.copy2(source, destination_source)
            installed = target / "methodology" / "architecture" / "principles.md"
            installed.parent.mkdir(parents=True)
            installed.write_bytes(
                render.render_managed_bytes(source.read_bytes(), "methodology", "my-skills")
            )

            clean = update.modified_managed_files(
                package,
                target,
                methodology_dir="methodology",
                skills_dir="my-skills",
            )
            self.assertNotIn(installed, clean)
            self.assertNotIn(b"{governance_root}", installed.read_bytes())

            installed.write_bytes(installed.read_bytes() + b"\nhand edit\n")
            modified = update.modified_managed_files(
                package,
                target,
                methodology_dir="methodology",
                skills_dir="my-skills",
            )
            self.assertIn(installed, modified)

    def _working_bash(self) -> str | None:
        candidates: list[str] = []
        found = shutil.which("bash")
        if found:
            candidates.append(found)
        for extra in (
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files\Git\usr\bin\bash.exe",
        ):
            if Path(extra).is_file() and extra not in candidates:
                candidates.append(extra)
        for candidate in candidates:
            try:
                proc = subprocess.run(
                    [candidate, "-c", "echo ok"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=15,
                )
            except (OSError, subprocess.TimeoutExpired):
                continue
            if proc.returncode == 0 and "ok" in (proc.stdout or ""):
                return candidate
        return None

    def _assert_real_install_then_update(self, kind: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "consumer"
            target.mkdir()
            note = target / "methodology" / "notes" / "mine.md"
            note.parent.mkdir(parents=True)
            note_bytes = "see {governance_root}\n".encode("utf-8")
            note.write_bytes(note_bytes)
            custom = target / ".claude" / "skills" / "local-only" / "SKILL.md"
            custom.parent.mkdir(parents=True)
            custom_bytes = "local {{SKILLS_DIR}}\n".encode("utf-8")
            custom.write_bytes(custom_bytes)
            if kind == "ps1":
                executable = shutil.which("powershell") or shutil.which("pwsh")
                self.assertIsNotNone(executable)
                command = [
                    executable,
                    "-NoProfile",
                    "-NonInteractive",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(SKILLS / "install.ps1"),
                    "-All",
                    "-NonInteractive",
                    "-Force",
                    "-MethodologyDir",
                    "methodology",
                    "-SkillsDir",
                    "my-skills",
                ]
            else:
                executable = self._working_bash()
                if executable is None:
                    self.skipTest("bash cannot execute install.sh")
                command = [
                    executable,
                    str(SKILLS / "install.sh"),
                    "--all",
                    "--non-interactive",
                    "--force",
                    "--methodology-dir",
                    "methodology",
                    "--skills-dir",
                    "my-skills",
                ]
            proc = subprocess.run(
                command,
                cwd=target,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                env={**os.environ, "TERM": "dumb"},
            )
            combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
            self.assertEqual(proc.returncode, 0, msg=combined)

            principles_src = SKILLS / "core" / "docs" / "architecture" / "principles.md"
            principles = target / "methodology" / "architecture" / "principles.md"
            agents = target / "AGENTS.md"
            self.assertTrue(principles.is_file(), msg=combined)
            self.assertEqual(
                principles.read_bytes(),
                render.render_managed_bytes(
                    principles_src.read_bytes(), "methodology", "my-skills"
                ),
            )
            agents_text = agents.read_text(encoding="utf-8")
            self.assertIn("methodology/architecture", agents_text)
            self.assertIn("my-skills", agents_text)
            self.assertNotIn("{{GOVERNANCE_ROOT}}", agents_text)
            self.assertNotIn("{{SKILLS_DIR}}", agents_text)
            self.assertNotIn("{governance_root}", principles.read_text(encoding="utf-8"))
            self.assertEqual(note.read_bytes(), note_bytes)
            self.assertEqual(custom.read_bytes(), custom_bytes)

            result = pack.pack_skills(
                version="0.0.0-testupdate",
                output_dir=Path(tmp) / "dist",
                skills_root=SKILLS,
                skip_stage=True,
            )
            report = update.update_package(
                _args(
                    target,
                    result,
                    skills_dir="my-skills",
                    methodology_dir="methodology",
                    dry_run=True,
                )
            )
            self.assertEqual(report["result"], "dry-run")
            self.assertEqual(report["managed_conflicts"], [])

            principles.write_bytes(principles.read_bytes() + b"\nhand edit\n")
            with self.assertRaisesRegex(update.UpdateError, "managed files have local changes"):
                update.update_package(
                    _args(
                        target,
                        result,
                        skills_dir="my-skills",
                        methodology_dir="methodology",
                        dry_run=True,
                    )
                )

    @unittest.skipUnless(sys.platform.startswith("win"), "install.ps1 is the Windows update path")
    def test_install_ps1_rendered_placeholders_survive_update(self) -> None:
        self._assert_real_install_then_update("ps1")

    def test_install_sh_rendered_placeholders_survive_update(self) -> None:
        self._assert_real_install_then_update("sh")

    def test_nested_dirs_are_rejected_by_update(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "docs" / "skills").mkdir(parents=True)
            with self.assertRaisesRegex(update.UpdateError, "outside the methodology"):
                update.modified_managed_files(
                    SKILLS,
                    target,
                    methodology_dir="docs",
                    skills_dir="docs/skills",
                )

    def test_case_alias_nest_follows_platform_path_identity(self) -> None:
        self.assertFalse(render.install_dirs_nest("docs", "docs-extra"))
        alias_nested = render.install_dirs_nest("SKILLS/core/docs", "skills")
        if not sys.platform.startswith("win"):
            self.assertFalse(alias_nested)
            return
        self.assertTrue(alias_nested)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            principles = target / "skills" / "core" / "docs" / "architecture" / "principles.md"
            principles.parent.mkdir(parents=True)
            original = "keep {governance_root}\n".encode("utf-8")
            principles.write_bytes(original)
            with self.assertRaisesRegex(update.UpdateError, "outside the methodology"):
                update.modified_managed_files(
                    SKILLS,
                    target,
                    methodology_dir="SKILLS/core/docs",
                    skills_dir="skills",
                )
            with self.assertRaisesRegex(render.RenderError, "outside the methodology"):
                render.render_managed_pairs(SKILLS, target, "SKILLS/core/docs", "skills")
            self.assertEqual(principles.read_bytes(), original)

    def test_methodology_inside_skills_is_rejected_before_render(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            principles = target / "skills" / "core" / "docs" / "architecture" / "principles.md"
            principles.parent.mkdir(parents=True)
            original = "keep {governance_root}\n".encode("utf-8")
            principles.write_bytes(original)
            with self.assertRaisesRegex(update.UpdateError, "outside the methodology"):
                update.modified_managed_files(
                    SKILLS,
                    target,
                    methodology_dir="skills/core/docs",
                    skills_dir="skills",
                )
            with self.assertRaisesRegex(render.RenderError, "outside the methodology"):
                render.render_managed_pairs(SKILLS, target, "skills/core/docs", "skills")
            self.assertEqual(principles.read_bytes(), original)
            with self.assertRaisesRegex(update.UpdateError, "outside the methodology"):
                update.modified_managed_files(
                    SKILLS,
                    target,
                    methodology_dir="docs",
                    skills_dir="docs",
                )

    def _assert_nested_install_writes_nothing(self, kind: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "consumer"
            target.mkdir()
            marker = target / "methodology" / "my-skills" / "KEEP"
            marker.parent.mkdir(parents=True)
            marker.write_text("keep\n", encoding="utf-8")
            if kind == "ps1":
                executable = shutil.which("powershell") or shutil.which("pwsh")
                self.assertIsNotNone(executable)
                command = [
                    executable,
                    "-NoProfile",
                    "-NonInteractive",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(SKILLS / "install.ps1"),
                    "-All",
                    "-NonInteractive",
                    "-Force",
                    "-MethodologyDir",
                    "methodology",
                    "-SkillsDir",
                    "methodology/my-skills",
                ]
            else:
                executable = self._working_bash()
                if executable is None:
                    self.skipTest("bash cannot execute install.sh")
                command = [
                    executable,
                    str(SKILLS / "install.sh"),
                    "--all",
                    "--non-interactive",
                    "--force",
                    "--methodology-dir",
                    "methodology",
                    "--skills-dir",
                    "methodology/my-skills",
                ]
            proc = subprocess.run(
                command,
                cwd=target,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                env={**os.environ, "TERM": "dumb"},
            )
            combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
            self.assertNotEqual(proc.returncode, 0, msg=combined)
            self.assertIn("outside the methodology", combined)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep\n")
            self.assertFalse((target / "methodology" / "architecture" / "principles.md").exists())

    @unittest.skipUnless(sys.platform.startswith("win"), "install.ps1 is the Windows update path")
    def test_install_ps1_rejects_nested_skills_before_write(self) -> None:
        self._assert_nested_install_writes_nothing("ps1")

    def test_install_sh_rejects_nested_skills_before_write(self) -> None:
        self._assert_nested_install_writes_nothing("sh")


if __name__ == "__main__":
    unittest.main()
