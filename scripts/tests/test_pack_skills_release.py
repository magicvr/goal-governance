"""Unit tests for scripts/pack_skills_release.py (real pack functions, temp trees)."""

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
PACK_SCRIPT = SCRIPTS / "pack_skills_release.py"
REAL_SKILLS = REPO_ROOT / "skills"


def _load_pack_module():
    spec = importlib.util.spec_from_file_location("pack_skills_release", PACK_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PACK_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pack_skills_release"] = module
    spec.loader.exec_module(module)
    return module


pack = _load_pack_module()


def _write(path: Path, text: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _minimal_skills_tree(root: Path) -> Path:
    skills = root / "skills"
    _write(skills / "install.sh", "#!/bin/sh\n")
    _write(skills / "install.ps1", "Write-Host ok\n")
    _write(skills / "README.md", "# skills\n")
    _write(
        skills / "prompts" / "00-govern-orchestrator.md",
        "# orchestrator\n",
    )
    _write(skills / "contracts" / "skills-consumer-contract.json", "{}\n")
    _write(skills / "templates" / "goal-folder" / "00-meta.md", "# meta\n")
    # GOAL-019 D-004 core mirror (required for pack completeness)
    _write(skills / "core" / "docs" / "README.md", "# docs\n")
    _write(skills / "core" / "docs" / "architecture" / "principles.md", "# p\n")
    _write(
        skills / "core" / "docs" / "architecture" / "workspace-protocol.md",
        "# wp\n",
    )
    _write(skills / "core" / "docs" / "architecture" / "overview.md", "# o\n")
    _write(
        skills / "core" / "docs" / "architecture" / "directory-layout.md",
        "# d\n",
    )
    _write(
        skills / "core" / "docs" / "templates" / "workspace-context.md",
        "# w\n",
    )
    _write(
        skills / "core" / "docs" / "templates" / "goal-folder" / "00-meta.md",
        "# m\n",
    )
    # Noise that must be excluded
    _write(skills / "prompts" / "__pycache__" / "x.pyc", "cache")
    _write(skills / "tests" / "__pycache__" / "t.cpython-311.pyc", "cache")
    _write(skills / "tests" / "foo.pyc", "bytecode")
    return skills


class PackSkillsReleaseTests(unittest.TestCase):
    maxDiff = None

    def test_normalize_version_strips_v_and_rejects_empty(self) -> None:
        self.assertEqual(pack.normalize_version("v0.7.0"), "0.7.0")
        self.assertEqual(pack.normalize_version("0.0.0-testpack"), "0.0.0-testpack")
        with self.assertRaises(pack.PackSkillsError):
            pack.normalize_version("")
        with self.assertRaises(pack.PackSkillsError):
            pack.normalize_version("not-a-version")

    def test_should_exclude_caches_and_forbidden_prefixes(self) -> None:
        self.assertTrue(pack.should_exclude(Path("__pycache__") / "a.pyc"))
        self.assertTrue(pack.should_exclude(Path("tests") / "x.pyc"))
        self.assertTrue(pack.should_exclude(Path("docs") / "workspace-001-x" / "a.md"))
        self.assertTrue(pack.should_exclude(Path("contracts") / "runtime-evidence.schema.json"))
        self.assertTrue(
            pack.should_exclude(Path("contracts") / "skills-consumer-compatibility-matrix.json")
        )
        self.assertFalse(
            pack.should_exclude(Path("contracts") / "skills-consumer-contract.json")
        )
        self.assertFalse(pack.should_exclude(Path("prompts") / "00-govern-orchestrator.md"))

    def test_pack_skills_on_temp_tree_excludes_caches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            skills = _minimal_skills_tree(base)
            out = base / "out"
            result = pack.pack_skills(
                version="0.0.0-testpack",
                output_dir=out,
                skills_root=skills,
            )
            self.assertTrue(result.zip_path.is_file())
            self.assertTrue(result.sha256_path.is_file())
            self.assertEqual(
                result.zip_path.name,
                "goal-governance-skills-v0.0.0-testpack.zip",
            )
            expected = sha256(result.zip_path.read_bytes()).hexdigest()
            self.assertEqual(result.sha256_hex, expected)
            sidecar = result.sha256_path.read_text(encoding="utf-8")
            self.assertIn(expected, sidecar)
            self.assertIn(result.zip_path.name, sidecar)

            with zipfile.ZipFile(result.zip_path) as zf:
                names = zf.namelist()
            root = "goal-governance-skills-v0.0.0-testpack"
            self.assertIn(f"{root}/install.sh", names)
            self.assertIn(f"{root}/install.ps1", names)
            self.assertIn(f"{root}/prompts/00-govern-orchestrator.md", names)
            self.assertIn(f"{root}/core/docs/architecture/principles.md", names)
            self.assertTrue(any(n.startswith(f"{root}/contracts/") for n in names))
            joined = "\n".join(names)
            self.assertNotIn("__pycache__", joined)
            self.assertNotIn(".pyc", joined)
            self.assertNotIn("docs/workspace-", joined)
            self.assertNotIn("/web/", joined)
            self.assertNotIn("artifacts/", joined)
            self.assertNotIn("tech-stack.md", joined)
            self.assertNotIn("runtime-evidence.schema.json", joined)
            self.assertNotIn("skills-consumer-compatibility-matrix.json", joined)

    def test_pack_skills_rejects_incomplete_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skills = Path(tmp) / "skills"
            _write(skills / "README.md", "only readme\n")
            with self.assertRaises(pack.PackSkillsError):
                pack.pack_skills(
                    version="1.0.0",
                    output_dir=Path(tmp) / "out",
                    skills_root=skills,
                )

    def test_pack_skills_rejects_symlink(self) -> None:
        """GOAL-021 F-003: symlink members must not enter the zip (escape risk)."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            skills = _minimal_skills_tree(base)
            target = base / "outside-secret.txt"
            target.write_text("secret\n", encoding="utf-8")
            link = skills / "leaked-via-symlink.txt"
            try:
                link.symlink_to(target)
            except OSError as exc:
                self.skipTest(f"symlink creation not permitted: {exc}")
            with self.assertRaisesRegex(pack.PackSkillsError, "symlink"):
                pack.inventoriable_files(skills)

    def test_cli_packs_real_skills_tree(self) -> None:
        """Drive the shipped CLI entry point against the real repository skills/."""
        self.assertTrue(REAL_SKILLS.is_dir())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pack-out"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(PACK_SCRIPT),
                    "--version",
                    "0.0.0-testpack",
                    "--output-dir",
                    str(out),
                    "--skills-dir",
                    str(REAL_SKILLS),
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
            zip_path = out / "goal-governance-skills-v0.0.0-testpack.zip"
            sha_path = out / "goal-governance-skills-v0.0.0-testpack.zip.sha256"
            self.assertTrue(zip_path.is_file(), msg=proc.stdout)
            self.assertTrue(sha_path.is_file(), msg=proc.stdout)
            digest = sha256(zip_path.read_bytes()).hexdigest()
            self.assertIn(digest, sha_path.read_text(encoding="utf-8"))
            self.assertRegex(proc.stdout, re.compile(r"sha256:\s*" + re.escape(digest)))

            with zipfile.ZipFile(zip_path) as zf:
                names = set(zf.namelist())
            root = "goal-governance-skills-v0.0.0-testpack"
            self.assertIn(f"{root}/install.sh", names)
            self.assertIn(f"{root}/install.ps1", names)
            self.assertIn(f"{root}/prompts/00-govern-orchestrator.md", names)
            self.assertIn(f"{root}/core/docs/architecture/principles.md", names)
            self.assertIn(f"{root}/core/docs/architecture/workspace-protocol.md", names)
            self.assertTrue(any(n.startswith(f"{root}/contracts/") for n in names))
            self.assertIn(f"{root}/contracts/skills-consumer-contract.json", names)
            self.assertIn(f"{root}/contracts/skills-consumer-contract.schema.json", names)
            self.assertNotIn(f"{root}/contracts/runtime-evidence.schema.json", names)
            self.assertNotIn(
                f"{root}/contracts/skills-consumer-compatibility-matrix.json", names
            )
            self.assertIn(f"{root}/update.py", names)
            for bad in (
                "__pycache__",
                "docs/workspace-",
                "/web/",
                "artifacts/",
                "tech-stack.md",
                # VP-004 R4: MCP implementation lives at repo root mcp/ (channel
                # asset separation); the File zip must never contain it.
                f"{root}/mcp/",
                "/mcp/server.py",
            ):
                self.assertFalse(
                    any(bad in n for n in names),
                    msg=f"forbidden path fragment {bad!r} in archive",
                )


class SkillsPackWorkflowContractTests(unittest.TestCase):
    """Structural contract for the tag pack/publish workflow (no network)."""

    def test_publish_job_is_environment_gated_and_fail_closed(self) -> None:
        workflow = (REPO_ROOT / ".github/workflows/skills-pack-release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("environment: release", workflow)
        self.assertIn("gh release create", workflow)
        self.assertIn("gh release upload", workflow)
        self.assertIn("--mode release", workflow)
        self.assertIn("release_evidence.py", workflow)
        # Must not soft-continue past the hard evidence gate.
        self.assertNotRegex(
            workflow,
            r"Hard release-evidence gate[\s\S]{0,200}continue-on-error:\s*true",
        )
        # Pack job must not require Environment approval.
        pack_block = workflow.split("publish:")[0]
        self.assertNotIn("environment: release", pack_block)


if __name__ == "__main__":
    unittest.main()
