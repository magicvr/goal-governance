#!/usr/bin/env python3
"""Generate a reproducible Skills consumer compatibility report.

The canonical compatibility matrix is an evidence ledger, not a second protocol
source. This tool validates its relationship to the canonical contract and
records every uncovered required runtime cell explicitly.
"""

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

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_NAME = "skills-consumer-contract.json"
CONTRACT_SCHEMA_NAME = "skills-consumer-contract.schema.json"
MATRIX_NAME = "skills-consumer-compatibility-matrix.json"
MATRIX_SCHEMA_NAME = "skills-consumer-compatibility-matrix.schema.json"
RUNTIME_EVIDENCE_SCHEMA_NAME = "runtime-evidence.schema.json"
MATRIX_SCHEMA_ID = (
    "https://github.com/magicvr/goal-governance/schema/"
    "skills-consumer-compatibility-matrix/v1"
)
SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9][0-9]*)\.(?P<minor>0|[1-9][0-9]*)\."
    r"(?P<patch>0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_TAG_RE = re.compile(rf"^v{SEMVER_RE.pattern[1:-1]}$")


class ValidationError(ValueError):
    """Raised when a release-evidence input does not describe reality."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValidationError(f"cannot read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise ValidationError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"JSON root must be an object: {path}")
    return value


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _sha256_lf(path: Path) -> str:
    """Hash path bytes with CRLF normalized to LF (git text eol=lf)."""
    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _repo_path(root: Path, value: Any, label: str, *, directory_ok: bool = False) -> Path:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty repository-relative path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValidationError(f"{label} must not escape the repository: {value}")
    root = root.resolve()
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ValidationError(f"{label} must stay inside the repository: {value}") from error
    exists = resolved.exists() if directory_ok else resolved.is_file()
    if not exists:
        expected = "path" if directory_ok else "file"
        raise ValidationError(f"{label} {expected} is missing: {value}")
    return resolved


def _validate_json_schema(instance: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(instance),
            key=lambda error: list(error.absolute_path),
        )
    except SchemaError as error:
        raise ValidationError(f"invalid {label} schema: {error.message}") from error
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValidationError(f"{label} schema validation failed at {location}: {error.message}")


def _git(root: Path, *args: str) -> str | None:
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
        return None
    return proc.stdout.strip()


def _mirror_records(root: Path) -> list[dict[str, Any]]:
    contracts = root / "docs" / "contracts"
    skills_contracts = root / "skills" / "contracts"
    canonical_files = sorted(path for path in contracts.rglob("*") if path.is_file())
    records: list[dict[str, Any]] = []
    for canonical in canonical_files:
        relative = canonical.relative_to(contracts)
        mirror = skills_contracts / relative
        canonical_digest = _sha256(canonical)
        mirror_digest = _sha256(mirror) if mirror.is_file() else None
        records.append(
            {
                "path": str(relative).replace("\\", "/"),
                "canonicalSha256": canonical_digest,
                "mirrorSha256": mirror_digest,
                "matches": canonical_digest == mirror_digest,
            }
        )
    mirrored_relatives = {
        path.relative_to(skills_contracts)
        for path in skills_contracts.rglob("*")
        if path.is_file()
    }
    canonical_relatives = {path.relative_to(contracts) for path in canonical_files}
    for relative in sorted(mirrored_relatives - canonical_relatives):
        records.append(
            {
                "path": str(relative).replace("\\", "/"),
                "canonicalSha256": None,
                "mirrorSha256": _sha256(skills_contracts / relative),
                "matches": False,
            }
        )
    return records


def _semver_core(value: Any, label: str) -> tuple[int, int, int]:
    if not isinstance(value, str):
        raise ValidationError(f"{label} must be a SemVer string")
    match = SEMVER_RE.fullmatch(value)
    if match is None:
        raise ValidationError(f"{label} is not SemVer: {value!r}")
    return tuple(int(match.group(name)) for name in ("major", "minor", "patch"))


def _semver_range(value: Any, label: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    if not isinstance(value, dict) or set(value) != {"minInclusive", "maxExclusive"}:
        raise ValidationError(f"{label} must contain minInclusive/maxExclusive")
    minimum = _semver_core(value["minInclusive"], f"{label}.minInclusive")
    maximum = _semver_core(value["maxExclusive"], f"{label}.maxExclusive")
    if minimum >= maximum:
        raise ValidationError(f"{label} must not be empty or reversed")
    if minimum[0] == 0:
        if maximum != (0, minimum[1] + 1, 0):
            raise ValidationError(f"{label} must stay within one unstable 0.y protocol line")
    return minimum, maximum


def _range_contains(value: Any, version: tuple[int, int, int], label: str) -> bool:
    minimum, maximum = _semver_range(value, label)
    return minimum <= version < maximum


def _validate_negative_fixture(
    root: Path,
    fixture: dict[str, Any],
    canonical: dict[str, Any],
    adapters: list[dict[str, Any]],
) -> None:
    fixture_id = fixture.get("id")
    kind = fixture.get("kind")
    path_value = fixture.get("path")
    assertion = fixture.get("assertion")
    if not all(isinstance(value, str) and value for value in (fixture_id, kind, path_value, assertion)):
        raise ValidationError("matrix negative fixture requires id/kind/path/assertion")
    if not path_value.startswith("docs/contracts/fixtures/"):
        raise ValidationError(f"matrix fixture must live under docs/contracts/fixtures: {path_value}")
    fixture_path = _repo_path(root, path_value, f"fixture {fixture_id}")
    payload = _read_json(fixture_path)
    if kind == "unsupported-protocol":
        fixture_protocol = payload.get("protocol")
        if not isinstance(fixture_protocol, dict):
            raise ValidationError(f"{fixture_id} lacks protocol")
        version = _semver_core(fixture_protocol.get("version"), f"{fixture_id}.protocol.version")
        current = _semver_core(canonical["protocol"]["version"], "canonical protocol.version")
        if version == current:
            raise ValidationError(f"{fixture_id} does not describe an unsupported protocol")
        for adapter in adapters:
            if _range_contains(
                adapter.get("supportsProtocol"),
                version,
                f"adapter {adapter.get('id')} supportsProtocol",
            ):
                raise ValidationError(
                    f"{fixture_id} protocol is still supported by adapter {adapter.get('id')}"
                )
    elif kind == "fabricated-predecessor":
        canonical_baseline = canonical.get("supportBaseline")
        fixture_baseline = payload.get("supportBaseline")
        if not isinstance(canonical_baseline, dict) or not isinstance(fixture_baseline, dict):
            raise ValidationError(f"{fixture_id} lacks supportBaseline")
        if canonical_baseline.get("previousSupportedProtocol") is not None:
            raise ValidationError("fabricated-predecessor is only valid for a null canonical predecessor")
        predecessor = fixture_baseline.get("previousSupportedProtocol")
        if predecessor is None:
            raise ValidationError(f"{fixture_id} does not actually fabricate a predecessor")
        _semver_core(predecessor, f"{fixture_id}.previousSupportedProtocol")
        if payload.get("protocol") != canonical.get("protocol"):
            raise ValidationError(f"{fixture_id} must isolate predecessor fabrication")
    else:
        raise ValidationError(f"matrix negative fixture has unknown kind: {kind!r}")


def _entrypoint_map(consumer: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = consumer.get("entrypoints")
    if not isinstance(entries, list):
        raise ValidationError(f"consumer {consumer.get('id')!r} lacks entrypoints")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValidationError(f"consumer {consumer.get('id')!r} has invalid entrypoint")
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            raise ValidationError(f"consumer {consumer.get('id')!r} has unnamed entrypoint")
        if name in result:
            raise ValidationError(f"consumer {consumer.get('id')!r} duplicates {name!r}")
        result[name] = entry
    return result


def _validate_runtime_evidence(
    root: Path,
    evidence_path: Path,
    runtime_schema: dict[str, Any],
    consumer_id: str,
    entrypoint: str,
    current_protocol: str,
) -> None:
    evidence = _read_json(evidence_path)
    if evidence.get("format") != "goal-governance.host-runtime-evidence":
        raise ValidationError(f"runtime evidence has unknown format: {evidence_path}")
    _validate_json_schema(evidence, runtime_schema, "runtime evidence")
    unit = evidence["unit"]
    if unit.get("consumer") != consumer_id or unit.get("entrypoint") != entrypoint:
        raise ValidationError(
            f"runtime evidence unit differs from matrix cell {consumer_id}/{entrypoint}"
        )
    if unit.get("protocolVersion") != current_protocol:
        raise ValidationError(
            f"runtime evidence protocol differs from current protocol for {consumer_id}/{entrypoint}"
        )
    for source in evidence["behaviorSources"]:
        source_path = _repo_path(root, source["path"], "runtime behavior source")
        # Compare LF-normalized digests so Windows autocrlf working trees match
        # git text=eol=lf blobs and Linux CI checkouts.
        if _sha256_lf(source_path) != source["sha256"]:
            raise ValidationError(
                f"runtime evidence behavior source is stale: {source['path']}"
            )
    result = evidence["result"]
    for label in ("stdout", "stderr"):
        raw_path = _repo_path(root, result[f"{label}Path"], f"runtime {label}")
        if _sha256_lf(raw_path) != result[f"{label}Sha256"]:
            raise ValidationError(
                f"runtime evidence {label} digest is stale for {consumer_id}/{entrypoint}"
            )
    for screenshot in evidence["artifacts"]["screenshots"]:
        _repo_path(root, screenshot, "runtime screenshot")
    if result.get("verdict") != "pass":
        raise ValidationError(
            f"runtime evidence is not a pass for {consumer_id}/{entrypoint}"
        )
    # GOAL-021 F-002: re-evaluate structured assertions against stdout; do not trust
    # summary / stored observed flags / marker-only pass payloads.
    stdout_path = _repo_path(root, result["stdoutPath"], "runtime stdout")
    stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace").replace(
        "\r\n", "\n"
    )
    marker = result.get("marker")
    if not isinstance(marker, str) or not marker or marker not in stdout_text:
        raise ValidationError(
            f"runtime evidence marker missing from stdout for {consumer_id}/{entrypoint}"
        )
    assertions = result.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        # Legacy captures without assertions: reject marker-only / trivial stdout.
        remainder = stdout_text.replace(marker, "", 1)
        extra = "".join(remainder.split())
        if len(extra.encode("utf-8")) < 16:
            raise ValidationError(
                f"runtime evidence is marker-only or trivial for {consumer_id}/{entrypoint}"
            )
        if entrypoint not in stdout_text:
            raise ValidationError(
                f"runtime evidence stdout lacks entrypoint token for {consumer_id}/{entrypoint}"
            )
    else:
        failed: list[str] = []
        unit = evidence["unit"]
        for item in assertions:
            if not isinstance(item, dict):
                raise ValidationError(
                    f"runtime evidence assertion is not an object for {consumer_id}/{entrypoint}"
                )
            kind = item.get("kind", "substring")
            pattern = str(item.get("pattern", ""))
            if kind == "substring":
                observed = bool(pattern) and pattern in stdout_text
            elif kind == "min-extra-bytes":
                min_extra = int(item.get("minExtraBytes", 16))
                remainder = stdout_text.replace(pattern, "", 1) if pattern else stdout_text
                extra = "".join(remainder.split())
                observed = len(extra.encode("utf-8")) >= min_extra
            elif kind == "regex":
                observed = bool(pattern) and re.search(pattern, stdout_text) is not None
            else:
                raise ValidationError(
                    f"runtime evidence has unsupported assertion kind {kind!r}"
                )
            if not observed:
                failed.append(str(item.get("id", "?")))
            bound = item.get("bound") or {}
            if bound.get("entrypoint") != unit.get("entrypoint"):
                raise ValidationError(
                    f"runtime assertion bound entrypoint mismatch for {consumer_id}/{entrypoint}"
                )
            if bound.get("protocolVersion") != unit.get("protocolVersion"):
                raise ValidationError(
                    f"runtime assertion bound protocol mismatch for {consumer_id}/{entrypoint}"
                )
        if failed:
            raise ValidationError(
                f"runtime evidence assertions failed re-check for {consumer_id}/{entrypoint}: "
                + ", ".join(failed)
            )


def validate_inputs(
    contract: dict[str, Any], matrix: dict[str, Any], root: Path = REPO_ROOT
) -> None:
    if matrix.get("schemaId") != MATRIX_SCHEMA_ID:
        raise ValidationError("compatibility matrix schemaId is not canonical")
    if matrix.get("format") != "goal-governance.skills-consumer-compatibility-matrix":
        raise ValidationError("compatibility matrix format is not canonical")
    if matrix.get("canonicalContractPath") != "docs/contracts/skills-consumer-contract.json":
        raise ValidationError("compatibility matrix must point to canonical contract")
    _semver_core(matrix.get("formatVersion"), "matrix formatVersion")
    candidate_revision = matrix.get("candidateRevision")
    if not isinstance(candidate_revision, str) or not (
        candidate_revision == "unreleased"
        or COMMIT_RE.fullmatch(candidate_revision)
        or SEMVER_TAG_RE.fullmatch(candidate_revision)
    ):
        raise ValidationError(
            "matrix candidateRevision must be 'unreleased', a full commit id, or a v-prefixed SemVer tag"
        )

    protocol = contract.get("protocol")
    baseline = contract.get("supportBaseline")
    matrix_protocol = matrix.get("protocol")
    if not isinstance(protocol, dict) or not isinstance(baseline, dict):
        raise ValidationError("contract lacks protocol/supportBaseline objects")
    if not isinstance(matrix_protocol, dict):
        raise ValidationError("matrix lacks protocol object")
    if matrix_protocol.get("current") != protocol.get("version"):
        raise ValidationError("matrix current protocol differs from canonical contract")
    current_protocol = _semver_core(protocol.get("version"), "contract protocol.version")
    current_protocol_text = str(protocol.get("version"))
    first_supported = _semver_core(
        baseline.get("firstSupportedProtocol"), "supportBaseline.firstSupportedProtocol"
    )
    if first_supported > current_protocol:
        raise ValidationError("first supported protocol cannot be newer than current protocol")
    if matrix_protocol.get("previous") != baseline.get("previousSupportedProtocol"):
        raise ValidationError("matrix previous protocol differs from canonical contract")
    if baseline.get("previousSupportedProtocol") is None:
        if matrix_protocol.get("previousStatus") != "not-applicable-first-supported-protocol":
            raise ValidationError("null predecessor requires explicit not-applicable status")
    elif matrix_protocol.get("previousStatus") != "supported":
        raise ValidationError("declared predecessor requires supported status")

    public_contract = protocol.get("publicContract")
    if not isinstance(public_contract, dict):
        raise ValidationError("contract lacks public contract")
    required_entrypoints = matrix.get("requiredEntrypoints")
    if required_entrypoints != public_contract.get("hostEntrypoints"):
        raise ValidationError("matrix requiredEntrypoints must match contract hostEntrypoints")

    negative_fixtures = matrix.get("negativeFixtures")
    if not isinstance(negative_fixtures, list) or not negative_fixtures:
        raise ValidationError("matrix must name negative fixtures")
    negative_ids = [item.get("id") for item in negative_fixtures if isinstance(item, dict)]
    if len(negative_ids) != len(set(negative_ids)):
        raise ValidationError("matrix negative fixture ids must be unique")
    if {"unsupported-protocol-0.2.0", "no-fabricated-predecessor"} - set(negative_ids):
        raise ValidationError("matrix lacks required current-baseline negative fixtures")

    adapters = contract.get("adapters")
    consumers = matrix.get("consumers")
    if not isinstance(adapters, list) or not isinstance(consumers, list):
        raise ValidationError("contract/matrix adapters must be arrays")
    if any(not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in adapters):
        raise ValidationError("contract adapters must have string ids")
    if any(not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in consumers):
        raise ValidationError("matrix consumers must have string ids")
    adapter_ids = [str(item["id"]) for item in adapters]
    consumer_ids = [str(item["id"]) for item in consumers]
    if len(adapter_ids) != len(set(adapter_ids)):
        raise ValidationError("canonical adapter ids must be unique")
    if len(consumer_ids) != len(set(consumer_ids)):
        raise ValidationError("matrix consumer ids must be unique")
    adapters_by_id = {str(item["id"]): item for item in adapters}
    consumers_by_id = {str(item["id"]): item for item in consumers}
    host_consumer_ids = {
        consumer_id
        for consumer_id, consumer in consumers_by_id.items()
        if consumer.get("kind") == "host-adapter"
    }
    if set(adapters_by_id) != host_consumer_ids:
        raise ValidationError("matrix host adapters must exactly match canonical adapters")
    allowed_statuses = {
        "pending-runtime-validation",
        "runtime-verified",
        "blocked",
        "pending-ci-replay",
        "automated-verified",
        "not-applicable",
    }
    runtime_schema = _read_json(
        root / "docs" / "contracts" / RUNTIME_EVIDENCE_SCHEMA_NAME
    )
    try:
        Draft202012Validator.check_schema(runtime_schema)
    except SchemaError as error:
        raise ValidationError(
            f"invalid runtime evidence schema: {error.message}"
        ) from error
    adapter_list = list(adapters_by_id.values())
    negative_paths: list[str] = []
    for fixture in negative_fixtures:
        if not isinstance(fixture, dict):
            raise ValidationError("matrix negative fixture must be an object")
        path_value = fixture.get("path")
        if isinstance(path_value, str):
            negative_paths.append(path_value)
        _validate_negative_fixture(root, fixture, contract, adapter_list)
    if len(negative_paths) != len(set(negative_paths)):
        raise ValidationError("matrix negative fixture paths must be unique")

    for adapter_id, adapter in adapters_by_id.items():
        consumer = consumers_by_id[adapter_id]
        if consumer.get("kind") != "host-adapter":
            raise ValidationError(f"{adapter_id} must be a host-adapter")
        if consumer.get("supportsProtocol") != adapter.get("supportsProtocol"):
            raise ValidationError(f"{adapter_id} protocol range differs from canonical contract")
        if consumer.get("supportCommitment") != adapter.get("supportCommitment"):
            raise ValidationError(f"{adapter_id} commitment differs from canonical contract")
        if consumer.get("contractVerificationStatus") != adapter.get("verificationStatus"):
            raise ValidationError(
                f"{adapter_id} contract verification status differs from canonical contract"
            )
        if not _range_contains(
            consumer.get("supportsProtocol"),
            current_protocol,
            f"consumer {adapter_id} supportsProtocol",
        ):
            raise ValidationError(f"{adapter_id} does not support the current protocol")
        entrypoints = _entrypoint_map(consumer)
        expected = adapter.get("entrypoints")
        if set(entrypoints) != set(expected if isinstance(expected, list) else []):
            raise ValidationError(f"{adapter_id} entrypoints differ from canonical contract")
        for name, entry in entrypoints.items():
            status = entry.get("status")
            if status not in allowed_statuses:
                raise ValidationError(f"{adapter_id}/{name} has invalid status {status!r}")
            if not isinstance(entry.get("evidence"), list):
                raise ValidationError(f"{adapter_id}/{name} evidence must be an array")
            for evidence_path in entry["evidence"]:
                resolved_evidence = _repo_path(
                    root,
                    evidence_path,
                    f"{adapter_id}/{name} evidence",
                    directory_ok=True,
                )
                if resolved_evidence.suffix.lower() == ".json":
                    _validate_runtime_evidence(
                        root,
                        resolved_evidence,
                        runtime_schema,
                        adapter_id,
                        name,
                        current_protocol_text,
                    )
            if status in {"runtime-verified", "automated-verified"} and not entry["evidence"]:
                raise ValidationError(f"{adapter_id}/{name} verified status requires evidence")
            if status == "runtime-verified" and not any(
                str(path).lower().endswith(".json") for path in entry["evidence"]
            ):
                raise ValidationError(
                    f"{adapter_id}/{name} runtime-verified status requires machine-readable JSON evidence"
                )

def generate_report(root: Path = REPO_ROOT) -> dict[str, Any]:
    root = root.resolve()
    contract_path = root / "docs" / "contracts" / CONTRACT_NAME
    contract_schema_path = root / "docs" / "contracts" / CONTRACT_SCHEMA_NAME
    matrix_path = root / "docs" / "contracts" / MATRIX_NAME
    matrix_schema_path = root / "docs" / "contracts" / MATRIX_SCHEMA_NAME
    contract = _read_json(contract_path)
    contract_schema = _read_json(contract_schema_path)
    matrix = _read_json(matrix_path)
    matrix_schema = _read_json(matrix_schema_path)
    _validate_json_schema(contract, contract_schema, "contract")
    _validate_json_schema(matrix, matrix_schema, "compatibility matrix")
    validate_inputs(contract, matrix, root)
    commit = _git(root, "rev-parse", "HEAD")
    if commit is None or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ValidationError("compatibility report requires a readable Git commit")
    mirrors = _mirror_records(root)
    mirror_ok = all(record["matches"] for record in mirrors)
    uncovered: list[dict[str, str]] = []
    for consumer in matrix["consumers"]:
        assert isinstance(consumer, dict)
        for name, entry in _entrypoint_map(consumer).items():
            status = str(entry["status"])
            if status not in {"runtime-verified", "automated-verified", "not-applicable"}:
                uncovered.append(
                    {
                        "consumer": str(consumer["id"]),
                        "entrypoint": name,
                        "status": status,
                    }
                )
    return {
        "reportFormat": "goal-governance.compatibility-report",
        "reportFormatVersion": "1.0.0",
        "generatedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "source": {
            "commit": commit,
            "branch": _git(root, "branch", "--show-current"),
            "tagsAtHead": (_git(root, "tag", "--points-at", "HEAD") or "").splitlines(),
        },
        "contract": {
            "path": "docs/contracts/skills-consumer-contract.json",
            "protocolVersion": contract["protocol"]["version"],
            "sha256": _sha256(contract_path),
        },
        "matrix": {
            "path": "docs/contracts/skills-consumer-compatibility-matrix.json",
            "sha256": _sha256(matrix_path),
            "candidateRevision": matrix["candidateRevision"],
            "previousProtocol": matrix["protocol"]["previous"],
            "previousProtocolStatus": matrix["protocol"]["previousStatus"],
        },
        "mirrorVerification": {"passed": mirror_ok, "files": mirrors},
        "coverage": {
            "status": "ready-for-release-evidence" if mirror_ok and not uncovered else "pending",
            "requiredEntrypoints": matrix["requiredEntrypoints"],
            "consumers": matrix["consumers"],
            "uncovered": uncovered,
        },
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "artifacts" / "compatibility-report.json",
        help="JSON report path (default: artifacts/compatibility-report.json)",
    )
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="fail unless every required matrix cell is verified",
    )
    args = parser.parse_args(argv)
    try:
        report = generate_report(args.root)
        _write_json(args.output, report)
    except ValidationError as error:
        print(f"compatibility report failed: {error}", file=sys.stderr)
        return 1
    print(f"wrote compatibility report: {args.output}")
    print(f"coverage status: {report['coverage']['status']}")
    if not report["mirrorVerification"]["passed"]:
        print("compatibility report failed: canonical/mirror drift", file=sys.stderr)
        return 1
    if args.require_ready and report["coverage"]["status"] != "ready-for-release-evidence":
        print("compatibility report failed: required runtime cells remain uncovered", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
