#!/usr/bin/env python3
"""Pack the core methodology mirror into a versioned zip + SHA-256 digest.

GOAL-023: independent core-only asset alongside skills zip (which still embeds
core). Source is skills/core/ (stage-generated from docs/ in the monorepo).

Does not create git tags, push remotes, or publish a GitHub Release.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = _SCRIPTS_DIR.parent
DEFAULT_CORE_DIR = REPO_ROOT / "skills" / "core"
DEFAULT_SKILLS_DIR = REPO_ROOT / "skills"

if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from pack_skills_release import (  # noqa: E402
    PackSkillsError,
    _maybe_stage_mirrors,
    normalize_version,
    should_exclude,
    write_sha256_sidecar,
)


class PackCoreError(PackSkillsError):
    """Raised when core packing inputs are invalid or the core tree is incomplete."""


@dataclass(frozen=True)
class PackCoreResult:
    version: str
    archive_root_name: str
    zip_path: Path
    sha256_path: Path
    sha256_hex: str
    member_count: int


def archive_root_name(version: str) -> str:
    return f"goal-governance-core-v{normalize_version(version)}"


def zip_filename(version: str) -> str:
    return f"{archive_root_name(version)}.zip"


def sha256_filename(version: str) -> str:
    return f"{archive_root_name(version)}.zip.sha256"


def inventoriable_core_files(core_root: Path) -> list[Path]:
    """Sorted list of files under core_root that belong in the core-only archive."""
    root = core_root.resolve()
    if not root.is_dir():
        raise PackCoreError(f"core root is not a directory: {root}")

    required = (
        root / "README.md",
        root / "docs" / "README.md",
        root / "docs" / "architecture" / "principles.md",
        root / "docs" / "architecture" / "workspace-protocol.md",
        root / "docs" / "architecture" / "overview.md",
        root / "docs" / "architecture" / "directory-layout.md",
        root / "docs" / "templates" / "workspace-context.md",
        root / "docs" / "templates" / "goal-folder" / "00-meta.md",
    )
    missing = [str(p.relative_to(root)) for p in required if not p.exists()]
    if missing:
        raise PackCoreError(
            "core root is incomplete; missing: " + ", ".join(missing)
        )
    tech_stack = root / "docs" / "architecture" / "tech-stack.md"
    if tech_stack.is_file():
        raise PackCoreError(
            "core package must not include tech-stack.md (GOAL-019 D-004)"
        )

    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if should_exclude(rel):
            continue
        if path.is_symlink():
            raise PackCoreError(f"refusing symlink in core pack: {rel.as_posix()}")
        if not path.is_file():
            continue
        resolved = path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError as error:
            raise PackCoreError(
                f"path escapes core root after resolve: {rel.as_posix()} -> {resolved}"
            ) from error
        files.append(path)
    if not files:
        raise PackCoreError(f"no files to pack under {root}")
    return files


def _zip_member_name(archive_root: str, relative: Path) -> str:
    return f"{archive_root}/{relative.as_posix()}"


def write_core_zip(
    core_root: Path,
    zip_path: Path,
    version: str,
    *,
    files: list[Path] | None = None,
) -> tuple[str, int]:
    """Write the core zip. Returns (archive_root_name, member_count)."""
    root = core_root.resolve()
    selected = files if files is not None else inventoriable_core_files(root)
    arch_root = archive_root_name(version)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in selected:
            rel = path.relative_to(root)
            zf.write(path, arcname=_zip_member_name(arch_root, rel))
    return arch_root, len(selected)


def pack_core(
    *,
    version: str,
    output_dir: Path,
    core_root: Path | None = None,
    skills_root: Path | None = None,
    skip_stage: bool = False,
) -> PackCoreResult:
    """Pack skills/core into output_dir as versioned zip + .sha256 sidecar."""
    ver = normalize_version(version)
    skills = (skills_root if skills_root is not None else DEFAULT_SKILLS_DIR).resolve()
    if core_root is not None:
        source = core_root.resolve()
    else:
        source = (skills / "core").resolve()

    # Stage monorepo mirrors when packing the real skills tree (GOAL-022).
    if skills.is_dir() and (skills / "core").resolve() == source:
        _maybe_stage_mirrors(skills, skip_stage=skip_stage)

    files = inventoriable_core_files(source)
    out = output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    zip_path = out / zip_filename(ver)
    arch_root, count = write_core_zip(source, zip_path, ver, files=files)
    digest, sha_path = write_sha256_sidecar(zip_path, out / sha256_filename(ver))
    return PackCoreResult(
        version=ver,
        archive_root_name=arch_root,
        zip_path=zip_path,
        sha256_path=sha_path,
        sha256_hex=digest,
        member_count=count,
    )


def assert_core_subset_of_skills_core(
    core_zip: Path,
    skills_zip: Path,
    *,
    version: str,
) -> list[str]:
    """Assert every core-only member bytes-match skills zip under core/.

    Returns list of relative paths checked. Raises PackCoreError on mismatch.
    """
    ver = normalize_version(version)
    core_prefix = f"{archive_root_name(ver)}/"
    skills_core_prefix = f"goal-governance-skills-v{ver}/core/"

    with zipfile.ZipFile(core_zip) as cz, zipfile.ZipFile(skills_zip) as sz:
        core_names = [
            n for n in cz.namelist() if n.startswith(core_prefix) and not n.endswith("/")
        ]
        if not core_names:
            raise PackCoreError(f"no members under {core_prefix} in {core_zip}")
        skills_index = {n: sz.read(n) for n in sz.namelist() if not n.endswith("/")}
        checked: list[str] = []
        for name in core_names:
            rel = name[len(core_prefix) :]
            skills_name = f"{skills_core_prefix}{rel}"
            if skills_name not in skills_index:
                raise PackCoreError(
                    f"core member missing from skills zip: {rel} (expected {skills_name})"
                )
            if cz.read(name) != skills_index[skills_name]:
                raise PackCoreError(
                    f"byte mismatch for core member vs skills embedded core: {rel}"
                )
            checked.append(rel)
    return checked


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Pack repository skills/core into goal-governance-core-vX.Y.Z.zip "
            "plus a SHA-256 sidecar. Offline; does not publish releases. "
            "Skills zip still embeds the same core (GOAL-019 / GOAL-023)."
        )
    )
    parser.add_argument(
        "--version",
        required=True,
        help="SemVer version for the archive name (optional leading v)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for the zip and .sha256 files",
    )
    parser.add_argument(
        "--core-dir",
        type=Path,
        default=None,
        help="Core package root (default: <skills-dir>/core or <repo>/skills/core)",
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=None,
        help="Skills package root for stage wiring (default: <repo>/skills)",
    )
    parser.add_argument(
        "--skip-stage",
        action="store_true",
        help="Do not run scripts/stage_skills_mirrors.py before packing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = pack_core(
            version=args.version,
            output_dir=args.output_dir,
            core_root=args.core_dir,
            skills_root=args.skills_dir,
            skip_stage=args.skip_stage,
        )
    except (PackCoreError, PackSkillsError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"version: {result.version}")
    print(f"archive_root: {result.archive_root_name}")
    print(f"zip: {result.zip_path}")
    print(f"sha256_file: {result.sha256_path}")
    print(f"sha256: {result.sha256_hex}")
    print(f"members: {result.member_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
