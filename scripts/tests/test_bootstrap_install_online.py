"""Offline bootstrap tests for scripts/bootstrap/install-online.* (GOAL-023).

Drives the real PowerShell bootstrap entry point against a locally packed
skills zip. Bash bootstrap is exercised when bash is available; otherwise
a structural residual check documents the shipped script.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
BOOTSTRAP_PS1 = SCRIPTS / "bootstrap" / "install-online.ps1"
BOOTSTRAP_SH = SCRIPTS / "bootstrap" / "install-online.sh"
PACK_SCRIPT = SCRIPTS / "pack_skills_release.py"
REAL_SKILLS = REPO_ROOT / "skills"


def _load_pack():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("pack_skills_release", PACK_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["pack_skills_release"] = module
    spec.loader.exec_module(module)
    return module


pack = _load_pack()


def _powershell_exe() -> str | None:
    """Prefer pwsh (PowerShell 7+) on CI; fall back to Windows PowerShell 5.x."""
    for name in ("pwsh", "powershell"):
        found = shutil.which(name)
        if found:
            return found
    return None


MCP_IMAGE_TEST = "ghcr.io/magicvr/goal-governance-mcp-server:0.0.0-testpack"


@contextmanager
def _ephemeral_tempdir(prefix: str = "gg-mcp-e2e-") -> Iterator[str]:
    """Temp dir whose cleanup never fails the test.

    MCP channel e2e runs a docker container that writes the consumer tree as
    root. Prefer mkdtemp + shutil.rmtree(ignore_errors=True): silent onerror,
    no chmod/_resetperms path that re-raises PermissionError/EPERM on
    docker-owned files (CI flake class on Actions Python 3.11). Leftover
    root-owned files under system /tmp are harmless.
    """
    path = tempfile.mkdtemp(prefix=prefix)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _build_mcp_test_image() -> bool:
    """Build the local MCP image used by thin-shell bootstrap tests (R4: GHCR image is the MCP asset)."""
    if not shutil.which("docker"):
        return False
    proc = subprocess.run(
        ["docker", "build", "-t", MCP_IMAGE_TEST, str(REPO_ROOT / "mcp")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode == 0


def _powershell(
    *args: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    exe = _powershell_exe()
    if not exe:
        raise unittest.SkipTest("pwsh/powershell not on PATH (Linux hosts skip PS1 e2e)")
    return subprocess.run(
        [
            exe,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            *args,
        ],
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


class EphemeralTempdirCleanupTests(unittest.TestCase):
    """Regression: docker-root EPERM must not fail tests on cleanup (CI flake class)."""

    def test_ephemeral_tempdir_cleanup_never_raises_on_permission_denied_tree(self) -> None:
        """Drive the real helper: a non-writable nested tree must not raise on exit.

        Mirrors the CI failure shape (root-owned install.json under
        consumer/.goal-governance) without requiring docker: on POSIX, drop
        write bits so unlink fails; shutil.rmtree(ignore_errors=True) must
        still exit cleanly.
        """
        held: list[str] = []
        with _ephemeral_tempdir(prefix="gg-eperm-sim-") as tmp:
            held.append(tmp)
            nested = Path(tmp) / "consumer" / ".goal-governance"
            nested.mkdir(parents=True)
            install_json = nested / "install.json"
            install_json.write_text('{"channel":"mcp"}', encoding="utf-8")
            if os.name == "posix":
                os.chmod(install_json, 0o444)
                os.chmod(nested, 0o555)
                # Parent consumer dir also non-writable so rmtree cannot fix up.
                os.chmod(nested.parent, 0o555)
        # Context exit must not raise (this is the assertion: we got here).
        self.assertTrue(held)
        # Source pin: both MCP channel e2e bodies open via the helper; helper
        # teardown is shutil.rmtree(..., ignore_errors=True) after mkdtemp.
        source = Path(__file__).read_text(encoding="utf-8")
        self.assertGreaterEqual(source.count("with _ephemeral_tempdir()"), 2)
        self.assertIn("shutil.rmtree(path, ignore_errors=True)", source)
        self.assertIn("tempfile.mkdtemp", source)


class BootstrapOfflinePs1Tests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.assertTrue(BOOTSTRAP_PS1.is_file())
        self.assertTrue(REAL_SKILLS.is_dir())
        if not _powershell_exe():
            self.skipTest("pwsh/powershell not on PATH (Linux hosts skip PS1 e2e)")

    def _pack_skills(self, out: Path, version: str = "0.0.0-testpack") -> pack.PackResult:
        return pack.pack_skills(
            version=version,
            output_dir=out,
            skills_root=REAL_SKILLS,
            skip_stage=True,
        )

    def test_offline_bootstrap_success_installs_core_and_hosts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack_out = base / "pack"
            target = base / "consumer"
            target.mkdir()
            result = self._pack_skills(pack_out)
            proc = _powershell(
                "-File",
                str(BOOTSTRAP_PS1),
                "-Version",
                result.version,
                "-TargetDir",
                str(target),
                "-ZipPath",
                str(result.zip_path),
                "-Sha256Path",
                str(result.sha256_path),
                "-Force",
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            self.assertTrue(
                (target / "docs" / "architecture" / "principles.md").is_file(),
                msg=proc.stdout,
            )
            self.assertTrue((target / "skills" / "install.ps1").is_file())
            self.assertTrue(
                (target / ".claude" / "skills" / "govern" / "SKILL.md").is_file()
                or (target / ".grok" / "skills" / "govern" / "SKILL.md").is_file()
                or (target / ".github" / "prompts" / "govern.prompt.md").is_file(),
                msg=f"expected host install artifacts\n{proc.stdout}",
            )
            # Core must come from embedded package path, not a separate network core asset.
            self.assertIn("SHA-256 OK", proc.stdout)
            self.assertNotIn("goal-governance-core-v", proc.stdout)

    def test_offline_relative_zip_resolved_against_cwd_not_target(self) -> None:
        """Skeptic: -ZipPath relative to CWD when TargetDir is a different empty tree."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack_here = base / "pack-here"
            pack_here.mkdir()
            target = base / "consumer-empty"
            target.mkdir()
            result = self._pack_skills(pack_here)
            # CWD = pack-here parent (base); relative zip path as docs show.
            rel_zip = Path("pack-here") / result.zip_path.name
            rel_sha = Path("pack-here") / result.sha256_path.name
            self.assertTrue((base / rel_zip).is_file())
            proc = _powershell(
                "-File",
                str(BOOTSTRAP_PS1),
                "-Version",
                result.version,
                "-TargetDir",
                str(target),
                "-ZipPath",
                str(rel_zip),
                "-Sha256Path",
                str(rel_sha),
                "-Force",
                cwd=base,
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            self.assertTrue(
                (target / "docs" / "architecture" / "principles.md").is_file(),
                msg=proc.stdout,
            )
            # Must not have looked under TargetDir\pack-here
            self.assertFalse((target / "pack-here").exists())

    def test_offline_bootstrap_fail_closed_on_digest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack_out = base / "pack"
            target = base / "consumer"
            target.mkdir()
            result = self._pack_skills(pack_out)
            bad_sha = pack_out / "tampered.sha256"
            # Valid format but wrong digest — must not install.
            bad_sha.write_text(
                f"{'0' * 64}  {result.zip_path.name}\n",
                encoding="utf-8",
                newline="\n",
            )
            proc = _powershell(
                "-File",
                str(BOOTSTRAP_PS1),
                "-Version",
                result.version,
                "-TargetDir",
                str(target),
                "-ZipPath",
                str(result.zip_path),
                "-Sha256Path",
                str(bad_sha),
                "-Force",
            )
            self.assertNotEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            self.assertIn("SHA-256 mismatch", proc.stdout + proc.stderr)
            self.assertFalse(
                (target / "docs" / "architecture" / "principles.md").is_file(),
                msg="must not install docs from a digest-mismatched zip",
            )
            # Destination skills must not be left as a successful install surface.
            skills_dir = target / "skills"
            if skills_dir.is_dir():
                self.assertFalse(
                    (skills_dir / "install.ps1").is_file()
                    and (target / "docs" / "architecture" / "principles.md").is_file()
                )

    def test_mcp_channel_bootstrap_installs_thin_shell_only_and_preserves_user_agents(self) -> None:
        """VP-004 R2/R4 dual entry: -Channel mcp = thin shell via GHCR image; no File 大包, no mcp code."""
        if not _build_mcp_test_image():
            self.skipTest("docker not available for MCP image build")
        # Docker writes consumer tree as root; use cleanup that never fails the test.
        with _ephemeral_tempdir() as tmp:
            base = Path(tmp)
            pack_out = base / "pack"
            target = base / "consumer"
            target.mkdir()
            user_preamble = "# 用户自有规则\n- 中文提交\n"
            (target / "AGENTS.md").write_text(user_preamble, encoding="utf-8")
            result = self._pack_skills(pack_out)
            proc = _powershell(
                "-File",
                str(BOOTSTRAP_PS1),
                "-Version",
                result.version,
                "-Channel",
                "mcp",
                "-TargetDir",
                str(target),
                "-ZipPath",
                str(result.zip_path),
                "-Sha256Path",
                str(result.sha256_path),
                "-McpImage",
                MCP_IMAGE_TEST,
                "-Force",
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            # R4: channel assets separated — no MCP code materialized into the consumer repo.
            self.assertFalse((target / "skills" / "mcp").exists())
            self.assertTrue(
                (target / "skills" / "contracts" / "skills-consumer-contract.json").is_file()
            )
            # File 大包 NOT installed.
            self.assertFalse((target / "docs" / "architecture").exists())
            self.assertFalse((target / "skills" / "prompts").exists())
            self.assertFalse((target / "skills" / "install.ps1").exists())
            # Managed AGENTS section with version; user preamble preserved.
            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertTrue(agents.startswith(user_preamble))
            self.assertIn("<!-- goal-governance:begin managed -->", agents)
            self.assertIn("<!-- goal-governance:end managed -->", agents)
            self.assertIn(f"- version: {result.version}", agents)
            # Thin-shell state.
            state = json.loads(
                (target / ".goal-governance" / "install.json").read_text(encoding="utf-8")
            )
            self.assertEqual(state["channel"], "mcp")
            self.assertEqual(state["version"], result.version)
            # MCP client config guidance names the GHCR image (R4 asset).
            self.assertIn(MCP_IMAGE_TEST, proc.stdout)
            # 推荐 MCP 叙述同屏声明 File 仍一等（ps1 输出为英文，跨控制台代码页稳定）。
            self.assertIn("File channel remains a first-class release path", proc.stdout)
            self.assertIn("NOT sunset", proc.stdout)

    def test_files_channel_explicit_is_full_install(self) -> None:
        """VP-004 R2: -Channel files (explicit) keeps the full File install."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack_out = base / "pack"
            target = base / "consumer"
            target.mkdir()
            result = self._pack_skills(pack_out)
            proc = _powershell(
                "-File",
                str(BOOTSTRAP_PS1),
                "-Version",
                result.version,
                "-Channel",
                "files",
                "-TargetDir",
                str(target),
                "-ZipPath",
                str(result.zip_path),
                "-Sha256Path",
                str(result.sha256_path),
                "-Force",
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            self.assertTrue(
                (target / "docs" / "architecture" / "principles.md").is_file()
            )
            self.assertTrue((target / "skills" / "install.ps1").is_file())

    def test_mcp_channel_rejects_unknown_channel_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack_out = base / "pack"
            target = base / "consumer"
            target.mkdir()
            result = self._pack_skills(pack_out)
            proc = _powershell(
                "-File",
                str(BOOTSTRAP_PS1),
                "-Version",
                result.version,
                "-Channel",
                "bogus",
                "-TargetDir",
                str(target),
                "-ZipPath",
                str(result.zip_path),
                "-Sha256Path",
                str(result.sha256_path),
                "-Force",
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("Channel must be 'files' or 'mcp'", proc.stdout + proc.stderr)



class BootstrapShStructuralTests(unittest.TestCase):
    """bash bootstrap: full offline run when bash exists; else structural checks."""

    def test_bash_script_exists_and_declares_offline_flags(self) -> None:
        self.assertTrue(BOOTSTRAP_SH.is_file())
        text = BOOTSTRAP_SH.read_text(encoding="utf-8")
        self.assertIn("--zip-path", text)
        self.assertIn("assert_digest_match", text)
        self.assertIn("--all", text)
        self.assertIn("goal-governance-skills-v", text)
        # VP-004 R2 dual entry: bash bootstrap declares --channel files|mcp.
        self.assertIn("--channel", text)
        self.assertIn("Channel must be 'files' or 'mcp'", text)
        self.assertIn("File 通道仍为一等", text)
        # File-classic: default path must not require Docker or MCP runtime.
        self.assertNotIn("--docker", text.split("Usage:")[0])
        self.assertNotIn("docker run", text.split("Usage:")[0])
        # Must not require a separate core download for default path.
        self.assertNotIn("goal-governance-core-v", text.split("Usage:")[0])

    def test_bash_offline_when_available(self) -> None:
        bash = shutil.which("bash")
        if not bash:
            self.skipTest("bash not on PATH")
        probe = subprocess.run(
            [bash, "-c", "echo ok"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if probe.returncode != 0 or "ok" not in (probe.stdout or ""):
            self.skipTest(
                f"bash on PATH is not usable (e.g. WSL stub without distro): {probe.stderr!r}"
            )
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack_out = base / "pack"
            target = base / "consumer"
            target.mkdir()
            result = pack.pack_skills(
                version="0.0.0-testpack",
                output_dir=pack_out,
                skills_root=REAL_SKILLS,
                skip_stage=True,
            )
            # Convert paths for Git Bash on Windows if needed.
            zip_arg = str(result.zip_path).replace("\\", "/")
            sha_arg = str(result.sha256_path).replace("\\", "/")
            target_arg = str(target).replace("\\", "/")
            script_arg = str(BOOTSTRAP_SH).replace("\\", "/")
            proc = subprocess.run(
                [
                    bash,
                    script_arg,
                    "--version",
                    result.version,
                    "--target-dir",
                    target_arg,
                    "--zip-path",
                    zip_arg,
                    "--sha256-path",
                    sha_arg,
                    "--force",
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                env={**os.environ, "MSYS_NO_PATHCONV": "1"},
            )
            if proc.returncode != 0 and "Need unzip" in (proc.stderr + proc.stdout):
                self.skipTest("unzip not available in bash environment")
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            self.assertTrue(
                (target / "docs" / "architecture" / "principles.md").is_file(),
                msg=proc.stdout,
            )

    def test_bash_mcp_channel_when_available(self) -> None:
        """VP-004 R2/R4: bash --channel mcp installs the thin shell via GHCR image (PS 对等 e2e)."""
        bash = shutil.which("bash")
        if not bash:
            self.skipTest("bash not on PATH")
        if not _build_mcp_test_image():
            self.skipTest("docker not available for MCP image build")
        probe = subprocess.run(
            [bash, "-c", "echo ok"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if probe.returncode != 0 or "ok" not in (probe.stdout or ""):
            self.skipTest(f"bash on PATH is not usable: {probe.stderr!r}")
        # Same docker-root-safe cleanup as the PS mcp-channel e2e above.
        with _ephemeral_tempdir() as tmp:
            base = Path(tmp)
            pack_out = base / "pack"
            target = base / "consumer"
            target.mkdir()
            result = pack.pack_skills(
                version="0.0.0-testpack",
                output_dir=pack_out,
                skills_root=REAL_SKILLS,
                skip_stage=True,
            )
            zip_arg = str(result.zip_path).replace("\\", "/")
            sha_arg = str(result.sha256_path).replace("\\", "/")
            target_arg = str(target).replace("\\", "/")
            script_arg = str(BOOTSTRAP_SH).replace("\\", "/")
            proc = subprocess.run(
                [
                    bash,
                    script_arg,
                    "--version",
                    result.version,
                    "--channel",
                    "mcp",
                    "--target-dir",
                    target_arg,
                    "--zip-path",
                    zip_arg,
                    "--sha256-path",
                    sha_arg,
                    "--mcp-image",
                    MCP_IMAGE_TEST,
                    "--force",
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                env={**os.environ, "MSYS_NO_PATHCONV": "1"},
            )
            if proc.returncode != 0 and (
                "Need unzip" in (proc.stderr + proc.stdout)
                or "MCP channel requires docker" in (proc.stderr + proc.stdout)
            ):
                self.skipTest("unzip or docker unavailable in bash environment")
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            # R4: no MCP code materialized; contracts + lifecycle state come from the image.
            self.assertFalse((target / "skills" / "mcp").exists())
            self.assertTrue(
                (target / "skills" / "contracts" / "skills-consumer-contract.json").is_file()
            )
            self.assertFalse((target / "docs" / "architecture").exists())
            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("<!-- goal-governance:begin managed -->", agents)
            state = json.loads(
                (target / ".goal-governance" / "install.json").read_text(encoding="utf-8")
            )
            self.assertEqual(state["channel"], "mcp")
            self.assertIn(MCP_IMAGE_TEST, proc.stdout)
            self.assertIn("File 通道仍为一等", proc.stdout)

    def test_workflow_packs_core_and_bootstrap(self) -> None:
        workflow = (
            REPO_ROOT / ".github/workflows/skills-pack-release.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("pack_core_release.py", workflow)
        self.assertIn("goal-governance-core-v", workflow)
        self.assertIn("install-online.ps1", workflow)
        self.assertIn("install-online.sh", workflow)
        self.assertIn("pack_skills_release.py", workflow)

    def test_bootstrap_docs_declare_dual_entry_and_file_first_class(self) -> None:
        """VP-004 R2: bootstrap README recommends MCP with File-first-class disclaimer."""
        readme = (REPO_ROOT / "scripts" / "bootstrap" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("-Channel mcp", readme)
        self.assertIn("-Channel files", readme)
        self.assertIn("推荐", readme)
        self.assertIn("File 通道仍为一等", readme)
        self.assertIn("未被废除", readme)
        # ps1 declares the dual entry and the same-screen File disclaimer.
        ps1_text = BOOTSTRAP_PS1.read_text(encoding="utf-8-sig")
        self.assertIn("[string]$Channel = 'files'", ps1_text)
        self.assertIn("File channel remains a first-class release path", ps1_text)

    def test_root_readme_mentions_dual_entry_and_embedded_core(self) -> None:
        text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("install-online", text)
        self.assertIn("内嵌", text)
        # Default path must not instruct network fetch of core-only for skills install.
        self.assertNotRegex(
            text,
            r"install-online[^\n]{0,120}goal-governance-core",
        )


if __name__ == "__main__":
    unittest.main()
