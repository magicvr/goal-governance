#!/usr/bin/env python3
"""Generate tagged-release or rehearsal evidence without publishing anything."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

import compatibility_report
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


REPO_ROOT = Path(__file__).resolve().parents[1]
RELEASE_EVIDENCE_SCHEMA_ID = (
    "https://github.com/magicvr/goal-governance/schema/release-evidence/v1"
)
COMPATIBILITY_REPORT_FORMAT = "goal-governance.compatibility-report"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_TAG_RE = re.compile(
    r"^v(?P<version>(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?)$"
)


def _python_with_imports(root: Path, modules: tuple[str, ...]) -> str:
    candidates = [
        root / ".venv" / "Scripts" / "python.exe",
        root / ".venv" / "bin" / "python",
        Path(sys.executable),
    ]
    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in seen or not candidate.is_file():
            continue
        seen.add(candidate)
        proc = subprocess.run(
            [str(candidate), "-c", "; ".join(f"import {module}" for module in modules)],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return str(candidate)
    raise ReleaseEvidenceError(
        "no Python interpreter can import required modules: " + ", ".join(modules)
    )


class ReleaseEvidenceError(ValueError):
    """Raised when requested release evidence would overclaim its inputs."""


def _git(root: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return proc.returncode, proc.stdout.strip()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _run_check(
    name: str,
    command: list[str],
    cwd: Path | None = None,
    root: Path = REPO_ROOT,
) -> dict[str, Any]:
    check_cwd = (cwd or root).resolve()
    proc = subprocess.run(
        command,
        cwd=check_cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = (proc.stdout or "") + ("\n" if proc.stdout and proc.stderr else "") + (proc.stderr or "")
    recorded_command = list(command)
    if recorded_command and Path(recorded_command[0]).name.lower().startswith("python"):
        recorded_command[0] = "python"
    return {
        "name": name,
        "command": recorded_command,
        "cwd": (
            str(check_cwd.relative_to(root.resolve())).replace("\\", "/") or "."
            if check_cwd.is_relative_to(root.resolve())
            else str(check_cwd)
        ),
        "exitCode": proc.returncode,
        "passed": proc.returncode == 0,
        "outputSha256": sha256(output.encode("utf-8")).hexdigest(),
        "output": output,
        "outputTail": output[-4000:],
    }


def _run_required_checks(
    root: Path, *, include_tool_tests: bool = True
) -> list[dict[str, Any]]:
    core_python = _python_with_imports(root, ("jsonschema",))
    checks = [
        _run_check(
            "skills-contract-tests",
            [core_python, "-m", "unittest", "skills/tests/test_skills_orchestrator.py", "-v"],
            root=root,
        ),
        _run_check(
            "standalone-bootstrap-tests",
            [
                core_python,
                "-m",
                "unittest",
                "discover",
                "-s",
                "docs/tests",
                "-p",
                "test_standalone_bootstrap.py",
                "-v",
            ],
            root=root,
        ),
        _run_check("diff-whitespace", ["git", "diff", "--check"], root=root),
    ]
    if include_tool_tests:
        checks.insert(
            2,
            _run_check(
                "release-evidence-tool-tests",
                [
                    core_python,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "scripts/tests",
                    "-p",
                    "test_*.py",
                    "-v",
                ],
                root=root,
            ),
        )
    return checks


def _collect_digests(root: Path) -> list[dict[str, str]]:
    targets: list[Path] = []
    for directory in (
        root / "docs" / "contracts",
        root / "skills" / "contracts",
        root / "docs" / "templates" / "goal-folder",
        root / "skills" / "templates" / "goal-folder",
        root / "skills",
        root / "scripts",
        root / "docs" / "releases",
    ):
        if directory.is_dir():
            targets.extend(
                path
                for path in directory.rglob("*")
                if path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix not in {".pyc", ".pyo"}
            )
    for path in (
        root / "skills" / "install.ps1",
        root / "skills" / "install.sh",
        root / ".github" / "workflows" / "ci.yml",
        root / "CHANGELOG.md",
    ):
        if path.is_file():
            targets.append(path)
    return [
        {
            "path": str(path.relative_to(root)).replace("\\", "/"),
            "sha256": _sha256(path),
        }
        for path in sorted(set(targets))
    ]


def _tag_version(tag: str) -> str:
    match = SEMVER_TAG_RE.fullmatch(tag)
    if match is None:
        raise ReleaseEvidenceError(f"release tag must be SemVer with a v prefix: {tag!r}")
    return match.group("version")


def _annotated_tag_at_head(tag: str, root: Path) -> bool:
    code, tag_type = _git(root, "cat-file", "-t", f"refs/tags/{tag}")
    if code != 0 or tag_type != "tag":
        return False
    code, tagged_commit = _git(root, "rev-list", "-n", "1", tag)
    code_head, head = _git(root, "rev-parse", "HEAD")
    return code == 0 and code_head == 0 and tagged_commit == head


def _release_tag_or_error(tag: str | None, root: Path) -> str:
    if tag is None:
        code, tags = _git(root, "tag", "--points-at", "HEAD")
        if code == 0:
            for candidate in tags.splitlines():
                if SEMVER_TAG_RE.fullmatch(candidate) and _annotated_tag_at_head(candidate, root):
                    return candidate
        raise ReleaseEvidenceError("release-candidate mode requires an annotated tag at HEAD or --tag")
    _tag_version(tag)
    if not _annotated_tag_at_head(tag, root):
        raise ReleaseEvidenceError(f"{tag!r} is not an annotated tag pointing at HEAD")
    return tag


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReleaseEvidenceError(f"{label} must be an object")
    return value


def _validate_compatibility_report(compatibility: dict[str, Any]) -> None:
    if compatibility.get("reportFormat") != COMPATIBILITY_REPORT_FORMAT:
        raise ReleaseEvidenceError("compatibility report format is not canonical")
    if compatibility.get("reportFormatVersion") != "1.0.0":
        raise ReleaseEvidenceError("unsupported compatibility report version")
    contract = _require_mapping(compatibility.get("contract"), "compatibility contract")
    matrix = _require_mapping(compatibility.get("matrix"), "compatibility matrix")
    mirrors = _require_mapping(
        compatibility.get("mirrorVerification"), "compatibility mirrorVerification"
    )
    coverage = _require_mapping(compatibility.get("coverage"), "compatibility coverage")
    source = _require_mapping(compatibility.get("source"), "compatibility source")
    if not isinstance(source.get("commit"), str) or COMMIT_RE.fullmatch(source["commit"]) is None:
        raise ReleaseEvidenceError("compatibility source commit is not a full commit id")
    if contract.get("path") != "docs/contracts/skills-consumer-contract.json":
        raise ReleaseEvidenceError("compatibility contract path is not canonical")
    if matrix.get("path") != "docs/contracts/skills-consumer-compatibility-matrix.json":
        raise ReleaseEvidenceError("compatibility matrix path is not canonical")
    candidate_revision = matrix.get("candidateRevision")
    if not isinstance(candidate_revision, str) or not (
        candidate_revision == "unreleased"
        or COMMIT_RE.fullmatch(candidate_revision)
        or SEMVER_TAG_RE.fullmatch(candidate_revision)
    ):
        raise ReleaseEvidenceError(
            "compatibility matrix candidateRevision must be 'unreleased', a full commit id, or a v-prefixed SemVer tag"
        )
    for label, digest in (
        ("contract.sha256", contract.get("sha256")),
        ("matrix.sha256", matrix.get("sha256")),
    ):
        if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
            raise ReleaseEvidenceError(f"compatibility {label} is not SHA-256")
    if not isinstance(contract.get("protocolVersion"), str):
        raise ReleaseEvidenceError("compatibility contract lacks protocolVersion")
    if not isinstance(mirrors.get("passed"), bool):
        raise ReleaseEvidenceError("compatibility mirror result is invalid")
    if coverage.get("status") not in {"pending", "ready-for-release-evidence"}:
        raise ReleaseEvidenceError("compatibility coverage status is invalid")
    if not isinstance(coverage.get("uncovered"), list):
        raise ReleaseEvidenceError("compatibility uncovered cells must be an array")


def _validate_checks(checks: list[dict[str, Any]]) -> None:
    names: set[str] = set()
    for check in checks:
        if not isinstance(check, dict):
            raise ReleaseEvidenceError("check result must be an object")
        name = check.get("name")
        if not isinstance(name, str) or not name or name in names:
            raise ReleaseEvidenceError("check names must be unique non-empty strings")
        names.add(name)
        if not isinstance(check.get("command"), list) or not check["command"]:
            raise ReleaseEvidenceError(f"check {name!r} lacks command")
        if not isinstance(check.get("cwd"), str) or not check["cwd"]:
            raise ReleaseEvidenceError(f"check {name!r} lacks cwd")
        if not isinstance(check.get("exitCode"), int) or not isinstance(check.get("passed"), bool):
            raise ReleaseEvidenceError(f"check {name!r} lacks exit status")
        if check["passed"] != (check["exitCode"] == 0):
            raise ReleaseEvidenceError(f"check {name!r} has inconsistent pass state")
        digest = check.get("outputSha256")
        if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
            raise ReleaseEvidenceError(f"check {name!r} output digest is invalid")
        if not isinstance(check.get("outputTail"), str):
            raise ReleaseEvidenceError(f"check {name!r} output tail is invalid")
        output = check.get("output")
        if not isinstance(output, str):
            raise ReleaseEvidenceError(f"check {name!r} full output is invalid")
        if sha256(output.encode("utf-8")).hexdigest() != digest:
            raise ReleaseEvidenceError(f"check {name!r} output digest does not match output")
        if check["outputTail"] != output[-4000:]:
            raise ReleaseEvidenceError(f"check {name!r} output tail does not match output")


def _reports_match(
    supplied: dict[str, Any], generated: dict[str, Any], root: Path
) -> None:
    code, head = _git(root, "rev-parse", "HEAD")
    if code != 0 or generated["source"]["commit"] != head:
        raise ReleaseEvidenceError("generated compatibility report is not bound to current HEAD")
    for label, section, key in (
        ("source commit", "source", "commit"),
        ("contract digest", "contract", "sha256"),
        ("matrix digest", "matrix", "sha256"),
    ):
        if supplied[section][key] != generated[section][key]:
            raise ReleaseEvidenceError(f"supplied compatibility report has stale {label}")
    if supplied["mirrorVerification"] != generated["mirrorVerification"]:
        raise ReleaseEvidenceError("supplied compatibility mirror result is stale")
    if supplied["coverage"] != generated["coverage"]:
        raise ReleaseEvidenceError("supplied compatibility coverage is stale")
    for label, section in (
        ("source metadata", "source"),
        ("contract metadata", "contract"),
        ("matrix metadata", "matrix"),
    ):
        if supplied[section] != generated[section]:
            raise ReleaseEvidenceError(f"supplied compatibility report has stale {label}")


def _changelog_mentions_version(root: Path, version: str) -> bool:
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return False
    text = changelog.read_text(encoding="utf-8")
    return re.search(rf"(?m)^##\s+\[?{re.escape(version)}\]?\b", text) is not None


def _validate_evidence_schema(evidence: dict[str, Any], root: Path) -> None:
    schema_path = root / "docs" / "releases" / "release-evidence.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ReleaseEvidenceError(f"cannot read release evidence schema: {error}") from error
    except json.JSONDecodeError as error:
        raise ReleaseEvidenceError(f"invalid release evidence schema JSON: {error}") from error
    if not isinstance(schema, dict):
        raise ReleaseEvidenceError("release evidence schema root must be an object")
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(evidence),
            key=lambda error: list(error.absolute_path),
        )
    except SchemaError as error:
        raise ReleaseEvidenceError(f"invalid release evidence schema: {error.message}") from error
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        raise ReleaseEvidenceError(
            f"release evidence schema validation failed at {location}: {error.message}"
        )


def generate_evidence(
    compatibility: dict[str, Any],
    mode: str,
    tag: str | None = None,
    root: Path = REPO_ROOT,
    *,
    run_checks: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    if mode not in {"rehearsal", "release"}:
        raise ReleaseEvidenceError(f"unknown mode: {mode}")
    if mode == "release" and not run_checks:
        raise ReleaseEvidenceError("release-candidate mode requires internally executed checks")
    _validate_compatibility_report(compatibility)
    current_compatibility = compatibility_report.generate_report(root)
    _reports_match(compatibility, current_compatibility, root)
    compatibility = current_compatibility
    release_tag = _release_tag_or_error(tag, root) if mode == "release" else None
    code, head = _git(root, "rev-parse", "HEAD")
    if code != 0:
        raise ReleaseEvidenceError("repository has no readable HEAD")
    if COMMIT_RE.fullmatch(head) is None:
        raise ReleaseEvidenceError("repository HEAD is not a full commit id")
    _, branch = _git(root, "branch", "--show-current")
    _, status = _git(root, "status", "--short")
    if mode == "release":
        assert release_tag is not None
        version = _tag_version(release_tag)
        if not _changelog_mentions_version(root, version):
            raise ReleaseEvidenceError(
                f"CHANGELOG.md has no release section for {version}"
            )
        if status:
            raise ReleaseEvidenceError("release-candidate mode requires a clean working tree")
        if compatibility["mirrorVerification"]["passed"] is not True:
            raise ReleaseEvidenceError("release-candidate mode requires canonical/mirror parity")
        if compatibility["coverage"]["status"] != "ready-for-release-evidence":
            raise ReleaseEvidenceError("release-candidate mode requires complete compatibility coverage")
        if compatibility["coverage"]["uncovered"]:
            raise ReleaseEvidenceError("release-candidate mode cannot contain uncovered cells")
        if compatibility["matrix"]["candidateRevision"] != release_tag:
            raise ReleaseEvidenceError(
                "release-candidate mode requires matrix candidateRevision to equal the annotated tag"
            )
        checks = _run_required_checks(root)
        _validate_checks(checks)
        if not checks:
            raise ReleaseEvidenceError("release-candidate mode requires executed checks")
        if not all(check["passed"] for check in checks):
            _print_failed_checks(checks)
            raise ReleaseEvidenceError("release-candidate mode requires every check to pass")
    else:
        checks = _run_required_checks(root) if run_checks else []
        _validate_checks(checks)
    all_passed = bool(checks) and all(check["passed"] for check in checks)
    evidence = {
        "schemaId": RELEASE_EVIDENCE_SCHEMA_ID,
        "format": "goal-governance.release-evidence",
        "formatVersion": "1.0.0",
        "generatedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "releaseStatus": "release-candidate" if release_tag else "rehearsal",
        "source": {
            "commit": head,
            "branch": branch or None,
            "annotatedTag": release_tag,
            "tagObject": (
                _git(root, "rev-parse", f"refs/tags/{release_tag}^{{tag}}")[1]
                if release_tag
                else None
            ),
        },
        "protocol": {
            "version": compatibility["contract"]["protocolVersion"],
            "contractSha256": compatibility["contract"]["sha256"],
            "matrixSha256": compatibility["matrix"]["sha256"],
            "candidateRevision": compatibility["matrix"]["candidateRevision"],
        },
        "compatibilityReport": {
            "coverageStatus": compatibility["coverage"]["status"],
            "uncovered": compatibility["coverage"]["uncovered"],
            "mirrorPassed": compatibility["mirrorVerification"]["passed"],
        },
        "checks": checks,
        "checksPassed": all_passed,
        "digests": _collect_digests(root),
        "workingTree": {"statusShort": status.splitlines(), "clean": not bool(status)},
    }
    _validate_evidence_schema(evidence, root)
    return evidence


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _print_failed_checks(checks: list[dict[str, Any]]) -> None:
    """Print per-check failure details to stderr (missing before: release mode
    raised without diagnostics, so CI failures were unactionable)."""
    for check in checks:
        if check.get("passed") is False:
            print(f"failed check: {check['name']}", file=sys.stderr)
            print(f"  command: {' '.join(check.get('command', []))}", file=sys.stderr)
            print(f"  exitCode: {check.get('exitCode')}", file=sys.stderr)
            tail = (check.get("outputTail") or "").strip()
            if tail:
                print("  output tail:", file=sys.stderr)
                for line in tail.splitlines()[-40:]:
                    print(f"    {line}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("rehearsal", "release"), default="rehearsal")
    parser.add_argument("--tag", help="required tag in release mode")
    parser.add_argument("--run-checks", action="store_true")
    parser.add_argument("--compatibility-report", type=Path)
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "artifacts" / "release-evidence.json",
    )
    args = parser.parse_args(argv)
    try:
        if args.mode == "release" and not args.run_checks:
            raise ReleaseEvidenceError("release mode requires --run-checks")
        generated_compatibility = compatibility_report.generate_report(args.root)
        if args.compatibility_report:
            compatibility = json.loads(args.compatibility_report.read_text(encoding="utf-8"))
            if not isinstance(compatibility, dict):
                raise ReleaseEvidenceError("compatibility report root must be an object")
            _validate_compatibility_report(compatibility)
            _reports_match(compatibility, generated_compatibility, args.root.resolve())
        else:
            compatibility = generated_compatibility
        evidence = generate_evidence(
            compatibility,
            args.mode,
            args.tag,
            args.root,
            run_checks=args.run_checks,
        )
        _write_json(args.output, evidence)
    except (OSError, json.JSONDecodeError, ReleaseEvidenceError, compatibility_report.ValidationError) as error:
        print(f"release evidence failed: {error}", file=sys.stderr)
        return 1
    print(f"wrote release evidence: {args.output}")
    print(f"release status: {evidence['releaseStatus']}")
    print(f"checks passed: {evidence['checksPassed']}")
    if args.run_checks and not evidence["checksPassed"]:
        print("release evidence failed: one or more checks failed", file=sys.stderr)
        _print_failed_checks(evidence.get("checks", []))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
