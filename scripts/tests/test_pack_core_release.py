"""Unit tests for scripts/pack_core_release.py (GOAL-023)."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from hashlib import sha256
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
CORE_PACK_SCRIPT = SCRIPTS / "pack_core_release.py"
SKILLS_PACK_SCRIPT = SCRIPTS / "pack_skills_release.py"
REAL_SKILLS = REPO_ROOT / "skills"


def _load_module(name: str, path: Path):
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


core_pack = _load_module("pack_core_release", CORE_PACK_SCRIPT)
skills_pack = _load_module("pack_skills_release", SKILLS_PACK_SCRIPT)


def _write(path: Path, text: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _minimal_core_tree(root: Path) -> Path:
    core = root / "skills" / "core"
    _write(core / "README.md", "# core\n")
    _write(core / "docs" / "README.md", "# docs\n")
    _write(core / "docs" / "architecture" / "principles.md", "# p\n")
    _write(core / "docs" / "architecture" / "workspace-protocol.md", "# wp\n")
    _write(core / "docs" / "architecture" / "overview.md", "# o\n")
    _write(core / "docs" / "architecture" / "directory-layout.md", "# d\n")
    _write(core / "docs" / "templates" / "workspace-context.md", "# w\n")
    _write(core / "docs" / "templates" / "goal-folder" / "00-meta.md", "# m\n")
    _write(core / "docs" / "vision" / "alignment.md", "# a\n")
    _write(core / "docs" / "vision" / "README.md", "# v\n")
    # Noise excluded
    _write(core / "docs" / "__pycache__" / "x.pyc", "cache")
    return core


def _minimal_skills_with_core(root: Path) -> Path:
    """Skills tree whose core/ matches _minimal_core_tree layout."""
    skills = root / "skills"
    core = _minimal_core_tree(root)
    assert core == skills / "core"
    _write(skills / "install.sh", "#!/bin/sh\n")
    _write(skills / "install.ps1", "Write-Host ok\n")
    _write(skills / "README.md", "# skills\n")
    _write(skills / "prompts" / "00-govern-orchestrator.md", "# orchestrator\n")
    _write(skills / "contracts" / "skills-consumer-contract.json", "{}\n")
    return skills


class PackCoreReleaseTests(unittest.TestCase):
    maxDiff = None

    def test_archive_names(self) -> None:
        self.assertEqual(
            core_pack.archive_root_name("v0.9.3"),
            "goal-governance-core-v0.9.3",
        )
        self.assertEqual(
            core_pack.zip_filename("0.0.0-testpack"),
            "goal-governance-core-v0.0.0-testpack.zip",
        )

    def test_pack_core_on_temp_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            core = _minimal_core_tree(base)
            out = base / "out"
            result = core_pack.pack_core(
                version="0.0.0-testpack",
                output_dir=out,
                core_root=core,
                skills_root=base / "skills",
                skip_stage=True,
            )
            self.assertTrue(result.zip_path.is_file())
            self.assertEqual(
                result.zip_path.name,
                "goal-governance-core-v0.0.0-testpack.zip",
            )
            expected = sha256(result.zip_path.read_bytes()).hexdigest()
            self.assertEqual(result.sha256_hex, expected)
            sidecar = result.sha256_path.read_text(encoding="utf-8")
            self.assertIn(expected, sidecar)

            with zipfile.ZipFile(result.zip_path) as zf:
                names = zf.namelist()
            root = "goal-governance-core-v0.0.0-testpack"
            self.assertIn(f"{root}/README.md", names)
            self.assertIn(f"{root}/docs/architecture/principles.md", names)
            self.assertIn(f"{root}/docs/templates/goal-folder/00-meta.md", names)
            joined = "\n".join(names)
            self.assertNotIn("__pycache__", joined)
            self.assertNotIn("tech-stack.md", joined)

    def test_pack_core_rejects_incomplete_and_tech_stack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            core = base / "core"
            _write(core / "README.md", "only\n")
            with self.assertRaises(core_pack.PackCoreError):
                core_pack.pack_core(
                    version="1.0.0",
                    output_dir=base / "out",
                    core_root=core,
                    skip_stage=True,
                )

            full = _minimal_core_tree(base)
            _write(full / "docs" / "architecture" / "tech-stack.md", "# no\n")
            with self.assertRaisesRegex(core_pack.PackCoreError, "tech-stack"):
                core_pack.inventoriable_core_files(full)

    def test_core_subset_matches_skills_embedded_core(self) -> None:
        """I-004: same version, core-only members ⊆ skills zip core/ byte-identical."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            skills = _minimal_skills_with_core(base)
            out = base / "out"
            ver = "0.0.0-testpack"
            skills_result = skills_pack.pack_skills(
                version=ver,
                output_dir=out,
                skills_root=skills,
                skip_stage=True,
            )
            core_result = core_pack.pack_core(
                version=ver,
                output_dir=out,
                core_root=skills / "core",
                skills_root=skills,
                skip_stage=True,
            )
            checked = core_pack.assert_core_subset_of_skills_core(
                core_result.zip_path,
                skills_result.zip_path,
                version=ver,
            )
            self.assertIn("docs/architecture/principles.md", checked)
            self.assertGreaterEqual(len(checked), 8)

    def test_cli_packs_real_core_tree(self) -> None:
        self.assertTrue((REAL_SKILLS / "core").is_dir())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pack-out"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(CORE_PACK_SCRIPT),
                    "--version",
                    "0.0.0-testpack",
                    "--output-dir",
                    str(out),
                    "--skills-dir",
                    str(REAL_SKILLS),
                    "--skip-stage",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            zip_path = out / "goal-governance-core-v0.0.0-testpack.zip"
            sha_path = out / "goal-governance-core-v0.0.0-testpack.zip.sha256"
            self.assertTrue(zip_path.is_file(), msg=proc.stdout)
            self.assertTrue(sha_path.is_file(), msg=proc.stdout)
            digest = sha256(zip_path.read_bytes()).hexdigest()
            self.assertIn(digest, sha_path.read_text(encoding="utf-8"))
            self.assertRegex(proc.stdout, re.compile(r"sha256:\s*" + re.escape(digest)))

            with zipfile.ZipFile(zip_path) as zf:
                names = set(zf.namelist())
            root = "goal-governance-core-v0.0.0-testpack"
            self.assertIn(f"{root}/docs/architecture/principles.md", names)
            self.assertFalse(any("tech-stack.md" in n for n in names))

    def test_real_core_subset_of_real_skills_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            ver = "0.0.0-testpack"
            skills_result = skills_pack.pack_skills(
                version=ver,
                output_dir=out,
                skills_root=REAL_SKILLS,
                skip_stage=True,
            )
            core_result = core_pack.pack_core(
                version=ver,
                output_dir=out,
                skills_root=REAL_SKILLS,
                skip_stage=True,
            )
            checked = core_pack.assert_core_subset_of_skills_core(
                core_result.zip_path,
                skills_result.zip_path,
                version=ver,
            )
            self.assertIn("docs/architecture/principles.md", checked)
            self.assertIn("docs/templates/goal-folder/00-meta.md", checked)


if __name__ == "__main__":
    unittest.main()
