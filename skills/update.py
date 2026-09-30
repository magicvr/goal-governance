#!/usr/bin/env python3
"""Transactional updater for an installed Goal Governance Skills package."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen
import zipfile

try:  # package-relative import (skills package) with script fallback
    from skills.agents_merge import (
        MergeError,
        has_managed_block,
        managed_block_equivalent,
        merge_agents_text,
        read_preserved_text,
        write_preserved_text,
    )
    from skills.render_managed import (
        assert_separate_install_dirs,
        install_token,
        list_managed_pairs,
        render_managed_bytes,
        render_managed_text,
    )
except ImportError:  # pragma: no cover - direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from agents_merge import (  # type: ignore[no-redef]
        MergeError,
        has_managed_block,
        managed_block_equivalent,
        merge_agents_text,
        read_preserved_text,
        write_preserved_text,
    )
    from render_managed import (  # type: ignore[no-redef]
        assert_separate_install_dirs,
        install_token,
        list_managed_pairs,
        render_managed_bytes,
        render_managed_text,
    )


SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


class UpdateError(RuntimeError):
    pass


def normalize_version(raw: str) -> str:
    value = (raw or "").strip()
    if value[:1].lower() == "v":
        value = value[1:]
    if not SEMVER_RE.fullmatch(value):
        raise UpdateError(f"invalid SemVer version: {raw!r}")
    return value


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_digest(sidecar: Path, zip_name: str) -> str:
    match = re.fullmatch(
        r"([0-9a-fA-F]{64})[ \t]+(\S+)\s*",
        sidecar.read_text(encoding="utf-8").strip(),
    )
    if not match:
        raise UpdateError("invalid SHA-256 sidecar; expected '<hex>  <filename>'")
    if Path(match.group(2)).name != zip_name:
        raise UpdateError("SHA-256 sidecar filename does not match archive")
    return match.group(1).lower()


def verify_archive(zip_path: Path, sidecar: Path) -> str:
    expected = expected_digest(sidecar, zip_path.name)
    actual = file_sha256(zip_path)
    if actual != expected:
        raise UpdateError(f"SHA-256 mismatch: expected {expected}, got {actual}")
    return actual


def safe_extract(zip_path: Path, destination: Path) -> Path:
    roots: set[str] = set()
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            pure = PurePosixPath(info.filename)
            if pure.is_absolute() or not pure.parts or ".." in pure.parts:
                raise UpdateError(f"unsafe archive member: {info.filename}")
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise UpdateError(f"archive symlink is not allowed: {info.filename}")
            roots.add(pure.parts[0])
        if len(roots) != 1:
            raise UpdateError("archive must contain exactly one top-level package directory")
        root_name = next(iter(roots))
        for info in archive.infolist():
            target = (destination / PurePosixPath(info.filename)).resolve()
            try:
                target.relative_to(destination.resolve())
            except ValueError as error:
                raise UpdateError(f"archive member escapes extraction root: {info.filename}") from error
        archive.extractall(destination)
    package = destination / root_name
    required = (
        package / "install.ps1",
        package / "install.sh",
        package / "contracts" / "skills-consumer-contract.json",
        package / "contracts" / "skills-consumer-contract.schema.json",
        package / "core" / "docs" / "architecture" / "principles.md",
    )
    missing = [str(path.relative_to(package)) for path in required if not path.is_file()]
    if missing:
        raise UpdateError("incomplete Skills package: " + ", ".join(missing))
    return package


def read_contract(package: Path) -> dict[str, object]:
    path = package / "contracts" / "skills-consumer-contract.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise UpdateError(f"cannot read consumer contract: {path}") from error
    if not isinstance(payload, dict):
        raise UpdateError("consumer contract root must be an object")
    return payload


def protocol_version(contract: dict[str, object]) -> str:
    protocol = contract.get("protocol")
    if not isinstance(protocol, dict):
        raise UpdateError("consumer contract is missing protocol")
    return normalize_version(str(protocol.get("version") or ""))


def assert_protocol_compatible(current: str, incoming: str, allow_upgrade: bool) -> None:
    current_parts = tuple(int(part) for part in normalize_version(current).split(".")[:2])
    incoming_parts = tuple(int(part) for part in normalize_version(incoming).split(".")[:2])
    if current_parts != incoming_parts and not allow_upgrade:
        raise UpdateError(
            f"protocol boundary change {current} -> {incoming}; pass --allow-protocol-upgrade after review"
        )


def latest_version(repo: str) -> str:
    request = Request(
        f"https://api.github.com/repos/{repo}/releases/latest",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "goal-governance-updater"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except Exception as error:  # urllib surfaces several transport-specific subclasses
        raise UpdateError(f"latest release discovery failed: {error}") from error
    if not isinstance(payload, dict) or not payload.get("tag_name"):
        raise UpdateError("latest release response is missing tag_name")
    return normalize_version(str(payload["tag_name"]))


def download(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "goal-governance-updater"})
    try:
        with urlopen(request, timeout=60) as response, destination.open("wb") as output:
            shutil.copyfileobj(response, output)
    except Exception as error:
        raise UpdateError(f"download failed: {url}: {error}") from error


def _install_tokens(target: Path, methodology_dir: str, skills_dir: str) -> tuple[str, str]:
    try:
        methodology = install_token(methodology_dir, target)
        skills = install_token(skills_dir, target)
        assert_separate_install_dirs(methodology, skills)
        return methodology, skills
    except ValueError as error:
        raise UpdateError(str(error)) from error


def _managed_bytes_match(source: Path, destination: Path, methodology: str, skills: str) -> bool:
    """True when destination is the package bytes or this install's rendering.

    The previous installer's unsubstituted copy is not a hand edit. The rendered
    copy is not a hand edit. Anything else still fails closed.
    """
    raw = source.read_bytes()
    current = destination.read_bytes()
    if current == raw:
        return True
    return current == render_managed_bytes(raw, methodology, skills)


def _agents_block_matches(consumer: str, source_text: str, methodology: str, skills: str) -> bool:
    rendered = render_managed_text(source_text, methodology, skills)
    variants = (rendered, source_text) if rendered != source_text else (source_text,)
    for variant in variants:
        if managed_block_equivalent(consumer, variant):
            return True
    return False


def managed_file_pairs(
    package: Path,
    target: Path,
    methodology_dir: str = "docs",
) -> list[tuple[Path, Path]]:
    # GOAL-008 S4: root AGENTS.md is deliberately NOT a fully-managed destination.
    # It is merged through the managed block (see agents_modification / merge_agents_text)
    # so consumer-owned rules in the same file survive updates.
    methodology = install_token(methodology_dir, target)
    return list_managed_pairs(package, target, methodology)


def agents_managed_conflict(
    package: Path,
    target: Path,
    incoming_package: Path | None = None,
    *,
    methodology_dir: str = "docs",
    skills_dir: str = "skills",
) -> Path | None:
    """Return root AGENTS.md when its content would need review before merging.

    Managed-block semantics (GOAL-008 S4): the destination is *not* a conflict
    just because the consumer wrote their own rules next to the block — those
    bytes are preserved. It is a conflict only when the existing block was
    hand-edited away from what either the current or the incoming package
    declares (``--force-managed`` then replaces just the block). A block that
    matches this install's rendered placeholders is the installer output, not
    a hand edit. The unsubstituted package block remains valid too.
    """
    destination = target / "AGENTS.md"
    if not destination.is_file():
        return None
    text = read_preserved_text(destination)
    methodology, skills = _install_tokens(target, methodology_dir, skills_dir)
    candidates = [
        package / "install" / "claude" / "AGENTS.md",
        (incoming_package / "install" / "claude" / "AGENTS.md")
        if incoming_package is not None
        else None,
    ]
    for source in candidates:
        if source is None or not source.is_file():
            continue
        try:
            if _agents_block_matches(text, source.read_text(encoding="utf-8"), methodology, skills):
                return None
        except MergeError:
            return destination
    return destination


def merge_root_agents(
    package: Path,
    target: Path,
    *,
    methodology_dir: str = "docs",
    skills_dir: str = "skills",
) -> str:
    """Merge the package's managed block into the consumer root AGENTS.md."""
    source = package / "install" / "claude" / "AGENTS.md"
    destination = target / "AGENTS.md"
    if not source.is_file():
        return "skipped-no-source"
    text = read_preserved_text(destination) if destination.is_file() else ""
    methodology, skills = _install_tokens(target, methodology_dir, skills_dir)
    source_text = render_managed_text(read_preserved_text(source), methodology, skills)
    try:
        merged, changed = merge_agents_text(text, source_text)
    except MergeError as error:
        raise UpdateError(f"AGENTS.md managed block is malformed: {error}") from error
    if not changed:
        return "unchanged"
    write_preserved_text(destination, merged)
    return "merged"


def modified_managed_files(
    package: Path,
    target: Path,
    incoming_package: Path | None = None,
    *,
    methodology_dir: str = "docs",
    skills_dir: str = "skills",
) -> list[Path]:
    methodology, skills = _install_tokens(target, methodology_dir, skills_dir)
    current = {
        destination: source
        for source, destination in managed_file_pairs(package, target, methodology)
    }
    incoming = (
        {
            destination: source
            for source, destination in managed_file_pairs(incoming_package, target, methodology)
        }
        if incoming_package is not None
        else {}
    )
    modified: list[Path] = []
    for destination, source in current.items():
        if source.is_file() and destination.is_file() and not _managed_bytes_match(
            source, destination, methodology, skills
        ):
            modified.append(destination)
    for destination, source in incoming.items():
        if destination in current or not source.is_file() or not destination.is_file():
            continue
        if not _managed_bytes_match(source, destination, methodology, skills):
            modified.append(destination)
    agents_conflict = agents_managed_conflict(
        package,
        target,
        incoming_package,
        methodology_dir=methodology,
        skills_dir=skills,
    )
    if agents_conflict is not None:
        modified.append(agents_conflict)
    return sorted(set(modified))


def backup_external_files(
    package: Path,
    target: Path,
    backup: Path,
    incoming_package: Path | None = None,
    *,
    methodology_dir: str = "docs",
) -> list[str]:
    absent: list[str] = []
    project_backup = backup / "project"
    methodology = install_token(methodology_dir, target)
    destinations = {destination for _source, destination in managed_file_pairs(package, target, methodology)}
    if incoming_package is not None:
        destinations.update(
            destination
            for _source, destination in managed_file_pairs(incoming_package, target, methodology)
        )
    for destination in sorted(destinations):
        relative = destination.relative_to(target)
        if destination.is_file():
            saved = project_backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination, saved)
        else:
            absent.append(relative.as_posix())
    return absent


def restore_external_files(target: Path, backup: Path, absent: list[str]) -> None:
    for relative in absent:
        path = target / PurePosixPath(relative)
        if path.is_file():
            path.unlink()
    project_backup = backup / "project"
    if project_backup.is_dir():
        for source in sorted(project_backup.rglob("*")):
            if source.is_file():
                destination = target / source.relative_to(project_backup)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)


def run_installer(
    package: Path,
    target: Path,
    *,
    methodology_dir: str = "docs",
    skills_dir: str = "skills",
) -> None:
    """Re-run the package installer with the same directory tokens install used."""
    if os.name == "nt":
        executable = shutil.which("powershell") or shutil.which("pwsh")
        if not executable:
            raise UpdateError("PowerShell is required to apply the update on Windows")
        command = [
            executable,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(package / "install.ps1"),
            "-All",
            "-NonInteractive",
            "-Force",
            "-MethodologyDir",
            methodology_dir,
            "-SkillsDir",
            skills_dir,
        ]
    else:
        bash = shutil.which("bash")
        if not bash:
            raise UpdateError("bash is required to apply the update on this platform")
        command = [
            bash,
            str(package / "install.sh"),
            "--all",
            "--non-interactive",
            "--force",
            "--methodology-dir",
            methodology_dir,
            "--skills-dir",
            skills_dir,
        ]
    result = subprocess.run(command, cwd=target, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise UpdateError(
            f"package install failed ({result.returncode})\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def update_package(args: argparse.Namespace) -> dict[str, object]:
    target = Path(args.target_dir).resolve()
    skills = (target / args.skills_dir).resolve() if not Path(args.skills_dir).is_absolute() else Path(args.skills_dir).resolve()
    try:
        skills.relative_to(target)
    except ValueError as error:
        raise UpdateError("skills directory must stay within target directory") from error
    if not skills.is_dir():
        raise UpdateError(f"installed Skills directory not found: {skills}")

    version = latest_version(args.repo) if args.latest else normalize_version(args.version)
    current_protocol = protocol_version(read_contract(skills))
    archive_name = f"goal-governance-skills-v{version}.zip"
    tag = args.release_tag or f"v{version}"

    with tempfile.TemporaryDirectory(prefix="goal-governance-update-") as temp_name:
        temp = Path(temp_name)
        if args.zip_path:
            archive = Path(args.zip_path).resolve()
            sidecar = Path(args.sha256_path).resolve() if args.sha256_path else Path(str(archive) + ".sha256")
        else:
            archive = temp / archive_name
            sidecar = temp / f"{archive_name}.sha256"
            base = f"https://github.com/{args.repo}/releases/download/{tag}"
            download(f"{base}/{archive_name}", archive)
            download(f"{base}/{archive_name}.sha256", sidecar)
        if not archive.is_file() or not sidecar.is_file():
            raise UpdateError("archive or SHA-256 sidecar does not exist")
        digest = verify_archive(archive, sidecar)
        incoming = safe_extract(archive, temp / "extract")
        incoming_protocol = protocol_version(read_contract(incoming))
        assert_protocol_compatible(current_protocol, incoming_protocol, args.allow_protocol_upgrade)

        methodology_dir = getattr(args, "methodology_dir", "docs")
        modified = modified_managed_files(
            skills,
            target,
            incoming,
            methodology_dir=methodology_dir,
            skills_dir=args.skills_dir,
        )
        if modified and not args.force_managed:
            shown = ", ".join(str(path.relative_to(target)) for path in modified[:8])
            raise UpdateError(f"managed files have local changes; review or pass --force-managed: {shown}")

        # GOAL-008 S4: normalize a legacy whole-file AGENTS.md into the managed
        # block before the package is swapped, then let the installer merge.
        agents = target / "AGENTS.md"
        if agents.is_file():
            existing = read_preserved_text(agents)
            if not has_managed_block(existing):
                legacy_source = skills / "install" / "claude" / "AGENTS.md"
                if legacy_source.is_file():
                    try:
                        converted, changed = merge_agents_text(
                            existing, read_preserved_text(legacy_source)
                        )
                    except MergeError:
                        changed = False
                    if changed:
                        write_preserved_text(agents, converted)

        plan = {
            "version": version,
            "current_protocol": current_protocol,
            "incoming_protocol": incoming_protocol,
            "archive_sha256": digest,
            "managed_conflicts": [str(path.relative_to(target)) for path in modified],
        }
        if args.dry_run:
            return {**plan, "result": "dry-run"}

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = target / ".goal-governance-updates" / f"{stamp}-v{version}"
        backup.mkdir(parents=True, exist_ok=False)
        absent = backup_external_files(
            skills, target, backup, incoming, methodology_dir=methodology_dir
        )
        old_skills = backup / "skills"
        shutil.move(str(skills), str(old_skills))
        try:
            shutil.move(str(incoming), str(skills))
            if not args.skip_install:
                run_installer(
                    skills,
                    target,
                    methodology_dir=methodology_dir,
                    skills_dir=args.skills_dir,
                )
            state = {
                "format": "goal-governance.skills-install-state/v1",
                "version": version,
                "protocol": incoming_protocol,
                "archiveSha256": digest,
                "source": str(archive) if args.zip_path else f"{args.repo}@{tag}",
                "installedAt": datetime.now(timezone.utc).isoformat(),
                "rollbackPath": str(backup),
            }
            (skills / ".goal-governance-install.json").write_text(
                json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except Exception:
            failed = backup / "failed-new-skills"
            if skills.exists():
                shutil.move(str(skills), str(failed))
            shutil.move(str(old_skills), str(skills))
            restore_external_files(target, backup, absent)
            raise
        return {**plan, "result": "updated", "rollback_path": str(backup)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    version = parser.add_mutually_exclusive_group(required=True)
    version.add_argument("--version", help="target SemVer (optional leading v)")
    version.add_argument("--latest", action="store_true", help="discover the latest GitHub Release")
    parser.add_argument("--target-dir", default=".", help="consumer project root")
    parser.add_argument("--skills-dir", default="skills", help="Skills path under target")
    parser.add_argument(
        "--methodology-dir",
        default="docs",
        help="methodology directory under target (default: docs)",
    )
    parser.add_argument("--zip-path", help="offline release zip")
    parser.add_argument("--sha256-path", help="offline SHA-256 sidecar")
    parser.add_argument("--repo", default="magicvr/goal-governance")
    parser.add_argument("--release-tag", default="")
    parser.add_argument("--allow-protocol-upgrade", action="store_true")
    parser.add_argument("--force-managed", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-install", action="store_true", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        result = update_package(build_parser().parse_args(argv))
    except UpdateError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
