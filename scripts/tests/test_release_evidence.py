from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
COMPATIBILITY = SCRIPTS / "compatibility_report.py"
RELEASE = SCRIPTS / "release_evidence.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
compatibility_report = _load_module("compatibility_report", COMPATIBILITY)
release_evidence = _load_module("release_evidence", RELEASE)


class ReleaseEvidenceToolTests(unittest.TestCase):
    maxDiff = None

    def _run(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def _copy_contract_surfaces(self, root: Path) -> None:
        for relative in (Path("docs/contracts"), Path("skills/contracts")):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(REPO_ROOT / relative, destination)

        copied: set[str] = set()

        def copy_repository_path(value: str) -> None:
            if value in copied:
                return
            source = REPO_ROOT / value
            destination = root / value
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            elif source.is_file():
                shutil.copy2(source, destination)
            copied.add(value)

        matrix = json.loads(
            (root / "docs/contracts/skills-consumer-compatibility-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        for consumer in matrix["consumers"]:
            for entrypoint in consumer["entrypoints"]:
                for evidence in entrypoint["evidence"]:
                    copy_repository_path(evidence)
                    source = REPO_ROOT / evidence
                    if source.suffix.lower() != ".json":
                        continue
                    payload = json.loads(source.read_text(encoding="utf-8"))
                    if payload.get("format") != "goal-governance.host-runtime-evidence":
                        continue
                    for behavior_source in payload["behaviorSources"]:
                        copy_repository_path(behavior_source["path"])
                    for label in ("stdout", "stderr"):
                        copy_repository_path(payload["result"][f"{label}Path"])
                    for screenshot in payload["artifacts"]["screenshots"]:
                        copy_repository_path(screenshot)

    def _init_contract_repo(self, root: Path) -> None:
        self._git(root, "init")
        self._git(root, "config", "user.name", "Goal Governance Tests")
        self._git(root, "config", "user.email", "tests@example.invalid")
        # Auto-gc can detach a background process writing .git/objects after
        # commit/tag, racing TemporaryDirectory cleanup (flaky CI: Errno 39
        # Directory not empty on Linux runners). Temp fixtures never need gc.
        self._git(root, "config", "gc.auto", "0")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "test contracts")

    @staticmethod
    def _git(root: Path, *args: str) -> str:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if proc.returncode != 0:
            raise AssertionError(proc.stderr)
        return proc.stdout.strip()

    def _init_release_repo(self, root: Path, version: str = "1.2.3") -> None:
        (root / "CHANGELOG.md").write_text(
            f"# Changelog\n\n## {version}\n\n- Release test.\n", encoding="utf-8"
        )
        self._git(root, "init")
        self._git(root, "config", "user.name", "Goal Governance Tests")
        self._git(root, "config", "user.email", "tests@example.invalid")
        # See _init_contract_repo: disable auto-gc so no background process
        # outlives the git command and races temp-dir cleanup.
        self._git(root, "config", "gc.auto", "0")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "test release")
        self._git(root, "tag", "-a", f"v{version}", "-m", f"release {version}")

    def _bind_report_to_root(
        self, report: dict[str, object], root: Path
    ) -> dict[str, object]:
        value = deepcopy(report)
        source = value["source"]
        assert isinstance(source, dict)
        source["commit"] = self._git(root, "rev-parse", "HEAD")
        source["branch"] = self._git(root, "branch", "--show-current") or None
        source["tagsAtHead"] = self._git(root, "tag", "--points-at", "HEAD").splitlines()
        return value

    @staticmethod
    def _passing_checks() -> list[dict[str, object]]:
        return [
            {
                "name": "fixture-check",
                "command": [sys.executable, "-c", "pass"],
                "cwd": ".",
                "exitCode": 0,
                "passed": True,
                "outputSha256": __import__("hashlib").sha256(b"").hexdigest(),
                "output": "",
                "outputTail": "",
            }
        ]

    @staticmethod
    def _ready_compatibility(
        report: dict[str, object], candidate_revision: str = "v1.2.3"
    ) -> dict[str, object]:
        value = deepcopy(report)
        coverage = value["coverage"]
        assert isinstance(coverage, dict)
        coverage["status"] = "ready-for-release-evidence"
        coverage["uncovered"] = []
        matrix = value["matrix"]
        assert isinstance(matrix, dict)
        matrix["candidateRevision"] = candidate_revision
        return value

    def test_compatibility_report_tracks_uncovered_candidate_runtime_cells(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-compatibility-report-") as tmp:
            output = Path(tmp) / "compatibility.json"
            proc = self._run(COMPATIBILITY, "--output", str(output))
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["reportFormat"], "goal-governance.compatibility-report")
        self.assertEqual(report["contract"]["protocolVersion"], "0.1.0")
        self.assertTrue(report["mirrorVerification"]["passed"])
        self.assertEqual(report["matrix"]["previousProtocol"], None)
        self.assertEqual(
            report["matrix"]["previousProtocolStatus"],
            "not-applicable-first-supported-protocol",
        )
        self.assertEqual(report["matrix"]["candidateRevision"], "v0.13.1")
        uncovered = {
            (cell["consumer"], cell["entrypoint"])
            for cell in report["coverage"]["uncovered"]
        }
        # Current candidate: four entrypoints x three hosts are pending until fresh evidence exists.
        # (govern/audit/vision/vision-audit); candidateRevision bound to annotated tag.
        # Codex install surface is shipped but not a matrix consumer.
        self.assertEqual(uncovered, set())
        self.assertEqual(
            {consumer["id"] for consumer in report["coverage"]["consumers"]},
            {"claude-code-cli", "grok-build-cli", "github-copilot-cli"},
        )
        self.assertEqual(report["coverage"]["status"], "ready-for-release-evidence")

    def test_compatibility_report_uses_supplied_root_for_mirrors(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-compatibility-root-") as tmp:
            root = Path(tmp)
            self._copy_contract_surfaces(root)
            self._init_contract_repo(root)
            mirror = root / "skills/contracts/skills-consumer-contract.json"
            mirror.write_text(mirror.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            report = compatibility_report.generate_report(root)
        self.assertFalse(report["mirrorVerification"]["passed"])

    def test_compatibility_report_rejects_a_fake_negative_fixture(self) -> None:
        contract = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-contract.json").read_text(
                encoding="utf-8"
            )
        )
        matrix = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-compatibility-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        matrix["negativeFixtures"][1]["path"] = (
            "docs/contracts/skills-consumer-contract.json"
        )
        with self.assertRaises(compatibility_report.ValidationError):
            compatibility_report.validate_inputs(contract, matrix, REPO_ROOT)

    def test_compatibility_report_rejects_evidence_path_escape(self) -> None:
        contract = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-contract.json").read_text(
                encoding="utf-8"
            )
        )
        matrix = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-compatibility-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        matrix["consumers"][0]["entrypoints"][0]["evidence"] = ["../outside.txt"]
        with self.assertRaisesRegex(
            compatibility_report.ValidationError, "must not escape"
        ):
            compatibility_report.validate_inputs(contract, matrix, REPO_ROOT)

    def test_rehearsal_evidence_never_claims_a_release(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-release-evidence-") as tmp:
            output = Path(tmp) / "release-evidence.json"
            proc = self._run(RELEASE, "--mode", "rehearsal", "--output", str(output))
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            evidence = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(evidence["releaseStatus"], "rehearsal")
        self.assertIsNone(evidence["source"]["annotatedTag"])
        self.assertIsNone(evidence["source"]["tagObject"])
        self.assertEqual(evidence["protocol"]["version"], "0.1.0")
        self.assertEqual(evidence["protocol"]["candidateRevision"], "v0.13.1")
        self.assertIn("checksPassed", evidence)
        schema = json.loads(
            (REPO_ROOT / "docs/releases/release-evidence.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(evidence)

    def test_matrix_matches_its_json_schema(self) -> None:
        schema = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-compatibility-matrix.schema.json").read_text(
                encoding="utf-8"
            )
        )
        matrix = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-compatibility-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema).validate(matrix)

    def test_matrix_rejects_an_unbound_candidate_revision(self) -> None:
        contract = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-contract.json").read_text(
                encoding="utf-8"
            )
        )
        matrix = json.loads(
            (REPO_ROOT / "docs/contracts/skills-consumer-compatibility-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        matrix["candidateRevision"] = "release-later"
        with self.assertRaisesRegex(
            compatibility_report.ValidationError, "candidateRevision"
        ):
            compatibility_report.validate_inputs(contract, matrix, REPO_ROOT)

    def test_release_mode_rejects_an_unverifiable_tag(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-release-evidence-") as tmp:
            output = Path(tmp) / "release-evidence.json"
            proc = self._run(
                RELEASE,
                "--mode",
                "release",
                "--run-checks",
                "--tag",
                "v-does-not-exist",
                "--output",
                str(output),
            )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("SemVer", proc.stderr)

    def test_release_mode_requires_ready_coverage(self) -> None:
        report = compatibility_report.generate_report(REPO_ROOT)
        with tempfile.TemporaryDirectory(prefix="gg-release-gate-") as tmp:
            root = Path(tmp)
            self._copy_contract_surfaces(root)
            (root / "payload.txt").write_text("payload\n", encoding="utf-8")
            for relative in (
                Path("docs/contracts/skills-consumer-compatibility-matrix.json"),
                Path("skills/contracts/skills-consumer-compatibility-matrix.json"),
            ):
                matrix_path = root / relative
                matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
                matrix["candidateRevision"] = "v1.2.3"
                for consumer in matrix["consumers"]:
                    if consumer["id"] == "claude-code-cli":
                        consumer["entrypoints"][0]["status"] = (
                            "pending-runtime-validation"
                        )
                matrix_path.write_text(
                    json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            schema_dir = root / "docs/releases"
            schema_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                REPO_ROOT / "docs/releases/release-evidence.schema.json",
                schema_dir / "release-evidence.schema.json",
            )
            self._init_release_repo(root)
            report = compatibility_report.generate_report(root)
            with self.assertRaisesRegex(
                release_evidence.ReleaseEvidenceError,
                "complete compatibility coverage",
            ):
                release_evidence.generate_evidence(
                    report,
                    "release",
                    "v1.2.3",
                    root,
                    run_checks=True,
                )

    def test_release_mode_rejects_dirty_tree_and_missing_changelog_version(self) -> None:
        report = self._ready_compatibility(
            compatibility_report.generate_report(REPO_ROOT)
        )
        with tempfile.TemporaryDirectory(prefix="gg-release-dirty-") as tmp:
            root = Path(tmp)
            self._copy_contract_surfaces(root)
            (root / "payload.txt").write_text("payload\n", encoding="utf-8")
            schema_dir = root / "docs/releases"
            schema_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                REPO_ROOT / "docs/releases/release-evidence.schema.json",
                schema_dir / "release-evidence.schema.json",
            )
            self._init_release_repo(root)
            report = self._bind_report_to_root(report, root)
            (root / "payload.txt").write_text("dirty\n", encoding="utf-8")
            with mock.patch.object(
                release_evidence.compatibility_report,
                "generate_report",
                return_value=report,
            ):
                with self.assertRaisesRegex(
                    release_evidence.ReleaseEvidenceError, "clean working tree"
                ):
                    release_evidence.generate_evidence(
                        report,
                        "release",
                        "v1.2.3",
                        root,
                        run_checks=True,
                    )

        with tempfile.TemporaryDirectory(
            prefix="gg-release-changelog-", ignore_cleanup_errors=True
        ) as tmp:
            root = Path(tmp)
            self._copy_contract_surfaces(root)
            (root / "payload.txt").write_text("payload\n", encoding="utf-8")
            schema_dir = root / "docs/releases"
            schema_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                REPO_ROOT / "docs/releases/release-evidence.schema.json",
                schema_dir / "release-evidence.schema.json",
            )
            self._init_release_repo(root, version="9.9.9")
            tag = "v9.9.9"
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## Unreleased\n", encoding="utf-8"
            )
            self._git(root, "add", "CHANGELOG.md")
            self._git(root, "commit", "-m", "remove release section")
            self._git(root, "tag", "-d", tag)
            self._git(root, "tag", "-a", tag, "-m", "release 9.9.9")
            report = self._bind_report_to_root(report, root)
            with mock.patch.object(
                release_evidence.compatibility_report,
                "generate_report",
                return_value=report,
            ):
                with self.assertRaisesRegex(
                    release_evidence.ReleaseEvidenceError, "no release section"
                ):
                    release_evidence.generate_evidence(
                        report,
                        "release",
                        tag,
                        root,
                        run_checks=True,
                    )

    def test_release_mode_accepts_annotated_semver_tag_when_gates_are_met(self) -> None:
        report = self._ready_compatibility(
            compatibility_report.generate_report(REPO_ROOT)
        )
        with tempfile.TemporaryDirectory(prefix="gg-release-pass-") as tmp:
            root = Path(tmp)
            self._copy_contract_surfaces(root)
            (root / "payload.txt").write_text("payload\n", encoding="utf-8")
            schema_dir = root / "docs/releases"
            schema_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                REPO_ROOT / "docs/releases/release-evidence.schema.json",
                schema_dir / "release-evidence.schema.json",
            )
            self._init_release_repo(root)
            report = self._bind_report_to_root(report, root)
            with mock.patch.object(
                release_evidence.compatibility_report,
                "generate_report",
                return_value=report,
            ), mock.patch.object(
                release_evidence,
                "_run_required_checks",
                return_value=self._passing_checks(),
            ):
                evidence = release_evidence.generate_evidence(
                    report,
                    "release",
                    "v1.2.3",
                    root,
                    run_checks=True,
                )
        self.assertEqual(evidence["releaseStatus"], "release-candidate")
        self.assertEqual(evidence["source"]["annotatedTag"], "v1.2.3")
        self.assertEqual(evidence["protocol"]["candidateRevision"], "v1.2.3")
        self.assertRegex(evidence["source"]["tagObject"], r"^[0-9a-f]{40}$")
        self.assertTrue(evidence["checksPassed"])
        self.assertTrue(evidence["workingTree"]["clean"])
        schema = json.loads(
            (REPO_ROOT / "docs/releases/release-evidence.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(evidence)

    def test_rehearsal_cli_fails_when_an_executed_check_fails(self) -> None:
        report = compatibility_report.generate_report(REPO_ROOT)
        failed = {
            "name": "forced-failure",
            "command": [sys.executable, "-c", "raise SystemExit(1)"],
            "cwd": ".",
            "exitCode": 1,
            "passed": False,
            "outputSha256": __import__("hashlib").sha256(b"forced failure").hexdigest(),
            "output": "forced failure",
            "outputTail": "forced failure",
        }
        with tempfile.TemporaryDirectory(prefix="gg-release-cli-failure-") as tmp:
            output = Path(tmp) / "evidence.json"
            check_results = [
                {**failed, "name": "skills-contract-tests"},
                {**failed, "name": "standalone-bootstrap-tests"},
                {**failed, "name": "release-evidence-tool-tests"},
                {**failed, "name": "diff-whitespace"},
            ]
            with mock.patch.object(
                release_evidence.compatibility_report,
                "generate_report",
                return_value=report,
            ), mock.patch.object(
                release_evidence,
                "_validate_evidence_schema",
                return_value=None,
            ), mock.patch.object(
                release_evidence,
                "_run_check",
                side_effect=check_results,
            ), contextlib.redirect_stderr(io.StringIO()) as captured:
                result = release_evidence.main(
                    ["--mode", "rehearsal", "--run-checks", "--output", str(output)]
                )
            evidence = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(result, 1)
        self.assertFalse(evidence["checksPassed"])
        # Failure diagnostics must name the failed check(s) with command and exit code.
        self.assertIn("failed check: skills-contract-tests", captured.getvalue())
        self.assertIn("failed check: diff-whitespace", captured.getvalue())
        self.assertIn("exitCode: 1", captured.getvalue())
        self.assertIn("forced failure", captured.getvalue())

    def test_malformed_compatibility_report_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-release-malformed-") as tmp:
            path = Path(tmp) / "bad.json"
            output = Path(tmp) / "evidence.json"
            path.write_text('{"reportFormat":"wrong"}\n', encoding="utf-8")
            proc = self._run(
                RELEASE,
                "--compatibility-report",
                str(path),
                "--output",
                str(output),
            )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("format is not canonical", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_release_rejects_stale_compatibility_report(self) -> None:
        report = compatibility_report.generate_report(REPO_ROOT)
        stale = deepcopy(report)
        stale["contract"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            release_evidence.ReleaseEvidenceError, "stale contract digest"
        ):
            release_evidence.generate_evidence(
                stale,
                "rehearsal",
                root=REPO_ROOT,
            )

    def test_rehearsal_rejects_stale_coverage(self) -> None:
        report = compatibility_report.generate_report(REPO_ROOT)
        stale = deepcopy(report)
        stale["coverage"]["status"] = "pending"
        stale["coverage"]["uncovered"] = [
            {
                "consumer": "claude-code-cli",
                "entrypoint": "govern",
                "status": "pending-runtime-validation",
            }
        ]
        with self.assertRaisesRegex(
            release_evidence.ReleaseEvidenceError, "coverage is stale"
        ):
            release_evidence.generate_evidence(
                stale,
                "rehearsal",
                root=REPO_ROOT,
            )

    def test_rehearsal_rejects_stale_mirror_result(self) -> None:
        report = compatibility_report.generate_report(REPO_ROOT)
        stale = deepcopy(report)
        stale["mirrorVerification"]["passed"] = False
        with self.assertRaisesRegex(
            release_evidence.ReleaseEvidenceError, "mirror result is stale"
        ):
            release_evidence.generate_evidence(
                stale,
                "rehearsal",
                root=REPO_ROOT,
            )

    def test_rehearsal_checks_are_executed_internally(self) -> None:
        report = compatibility_report.generate_report(REPO_ROOT)
        passing = self._passing_checks()
        with mock.patch.object(
            release_evidence,
            "_run_required_checks",
            return_value=passing,
        ) as run_checks:
            evidence = release_evidence.generate_evidence(
                report,
                "rehearsal",
                root=REPO_ROOT,
                run_checks=True,
            )
        run_checks.assert_called_once_with(REPO_ROOT.resolve())
        self.assertTrue(evidence["checksPassed"])
        self.assertEqual(evidence["checks"], passing)

    def test_generate_evidence_does_not_accept_caller_supplied_checks(self) -> None:
        report = compatibility_report.generate_report(REPO_ROOT)
        with self.assertRaisesRegex(TypeError, "checks"):
            release_evidence.generate_evidence(
                report,
                "rehearsal",
                checks=self._passing_checks(),
            )

    def test_release_mode_requires_candidate_revision_to_match_tag(self) -> None:
        report = self._ready_compatibility(
            compatibility_report.generate_report(REPO_ROOT),
            candidate_revision="v9.9.9",
        )
        with tempfile.TemporaryDirectory(prefix="gg-release-revision-") as tmp:
            root = Path(tmp)
            self._copy_contract_surfaces(root)
            (root / "payload.txt").write_text("payload\n", encoding="utf-8")
            schema_dir = root / "docs/releases"
            schema_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                REPO_ROOT / "docs/releases/release-evidence.schema.json",
                schema_dir / "release-evidence.schema.json",
            )
            self._init_release_repo(root)
            report = self._bind_report_to_root(report, root)
            with mock.patch.object(
                release_evidence.compatibility_report,
                "generate_report",
                return_value=report,
            ):
                with self.assertRaisesRegex(
                    release_evidence.ReleaseEvidenceError,
                    "candidateRevision to equal the annotated tag",
                ):
                    release_evidence.generate_evidence(
                        report,
                        "release",
                        "v1.2.3",
                        root,
                        run_checks=True,
                    )


if __name__ == "__main__":
    unittest.main()
