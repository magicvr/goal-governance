#!/usr/bin/env python3
"""Pack the skills/ delivery surface into a versioned zip + SHA-256 digest.

Does not create git tags, push remotes, or publish a GitHub Release.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_DIR = REPO_ROOT / "skills"

# SemVer core + optional pre-release / build (loose enough for 0.0.0-testpack).
VERSION_RE = re.compile(
    r"^(?P<version>"
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r")$"
)

# Directory / file names never included in the consumer archive.
EXCLUDED_DIR_NAMES = frozenset(
    {
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".git",
        ".venv",
        "node_modules",
    }
)
EXCLUDED_FILE_SUFFIXES = frozenset({".pyc", ".pyo", ".pyd"})
EXCLUDED_FILE_NAMES = frozenset({".DS_Store", "Thumbs.db"})


class PackSkillsError(ValueError):
    """Raised when packing inputs are invalid or the skills tree is incomplete."""


@dataclass(frozen=True)
class PackResult:
    version: str
    archive_root_name: str
    zip_path: Path
    sha256_path: Path
    sha256_hex: str
    member_count: int


def normalize_version(version: str) -> str:
    """Strip a single leading ``v`` / ``V`` and validate SemVer-like shape."""
    raw = (version or "").strip()
    if not raw:
        raise PackSkillsError("version must be non-empty")
    if raw[0] in "vV":
        raw = raw[1:]
    match = VERSION_RE.fullmatch(raw)
    if match is None:
        raise PackSkillsError(
            f"version must be SemVer-like (got {version!r}); "
            "examples: 0.7.0, v0.7.0, 0.0.0-testpack"
        )
    return match.group("version")


def archive_root_name(version: str) -> str:
    return f"goal-governance-skills-v{normalize_version(version)}"


def zip_filename(version: str) -> str:
    return f"{archive_root_name(version)}.zip"


def sha256_filename(version: str) -> str:
    return f"{archive_root_name(version)}.zip.sha256"


def should_exclude(relative: Path) -> bool:
    """Return True if a path relative to skills/ must not enter the zip."""
    parts = relative.parts
    if any(part in EXCLUDED_DIR_NAMES for part in parts):
        return True
    name = relative.name
    if name in EXCLUDED_FILE_NAMES:
        return True
    if relative.suffix in EXCLUDED_FILE_SUFFIXES:
        return True
    # Defense in depth: never ship monorepo process trees even if mis-rooted.
    joined = relative.as_posix()
    if "docs/workspace-" in joined or joined.startswith("web/") or joined.startswith(
        "artifacts/"
    ):
        return True
    return False


def inventoriable_files(skills_root: Path) -> list[Path]:
    """Sorted list of files under skills_root that belong in the archive."""
    root = skills_root.resolve()
    if not root.is_dir():
        raise PackSkillsError(f"skills root is not a directory: {root}")

    required = (
        root / "install.sh",
        root / "install.ps1",
        root / "prompts" / "00-govern-orchestrator.md",
        root / "contracts",
        # GOAL-019 D-004 core methodology mirror (co-required with Skills)
        root / "core" / "docs" / "README.md",
        root / "core" / "docs" / "architecture" / "principles.md",
        root / "core" / "docs" / "architecture" / "workspace-protocol.md",
        root / "core" / "docs" / "architecture" / "overview.md",
        root / "core" / "docs" / "architecture" / "directory-layout.md",
        root / "core" / "docs" / "templates" / "workspace-context.md",
        root / "core" / "docs" / "templates" / "goal-folder" / "00-meta.md",
    )
    missing = [str(p.relative_to(root)) for p in required if not p.exists()]
    if missing:
        raise PackSkillsError(
            "skills root is incomplete; missing: " + ", ".join(missing)
        )
    tech_stack = root / "core" / "docs" / "architecture" / "tech-stack.md"
    if tech_stack.is_file():
        raise PackSkillsError(
            "skills core mirror must not include tech-stack.md (GOAL-019 D-004)"
        )

    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if should_exclude(rel):
            continue
        # GOAL-021 F-003: refuse symlinks and path escape (do not follow into zip).
        if path.is_symlink():
            raise PackSkillsError(
                f"refusing symlink in skills pack: {rel.as_posix()}"
            )
        if not path.is_file():
            continue
        resolved = path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError as error:
            raise PackSkillsError(
                f"path escapes skills root after resolve: {rel.as_posix()} -> {resolved}"
            ) from error
        files.append(path)
    if not files:
        raise PackSkillsError(f"no files to pack under {root}")
    return files


def _zip_member_name(archive_root: str, relative: Path) -> str:
    # ZIP always uses forward slashes; deterministic for cross-platform digests of listing.
    return f"{archive_root}/{relative.as_posix()}"


def write_zip(
    skills_root: Path,
    zip_path: Path,
    version: str,
    *,
    files: list[Path] | None = None,
) -> tuple[str, int]:
    """Write the skills zip. Returns (archive_root_name, member_count)."""
    root = skills_root.resolve()
    selected = files if files is not None else inventoriable_files(root)
    arch_root = archive_root_name(version)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in selected:
            rel = path.relative_to(root)
            zf.write(path, arcname=_zip_member_name(arch_root, rel))
    return arch_root, len(selected)


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_sha256_sidecar(zip_path: Path, sha256_path: Path | None = None) -> tuple[str, Path]:
    """Write ``<hex>  <basename>`` sidecar next to the zip (or at sha256_path)."""
    digest = file_sha256(zip_path)
    out = sha256_path if sha256_path is not None else zip_path.with_suffix(
        zip_path.suffix + ".sha256"
    )
    # GNU coreutils sha256sum style: two spaces between hash and filename.
    line = f"{digest}  {zip_path.name}\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(line, encoding="utf-8", newline="\n")
    return digest, out


def pack_skills(
    *,
    version: str,
    output_dir: Path,
    skills_root: Path | None = None,
) -> PackResult:
    """Pack skills into output_dir as versioned zip + .sha256 sidecar."""
    ver = normalize_version(version)
    source = (skills_root if skills_root is not None else DEFAULT_SKILLS_DIR).resolve()
    files = inventoriable_files(source)
    out = output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    zip_path = out / zip_filename(ver)
    arch_root, count = write_zip(source, zip_path, ver, files=files)
    digest, sha_path = write_sha256_sidecar(zip_path, out / sha256_filename(ver))
    return PackResult(
        version=ver,
        archive_root_name=arch_root,
        zip_path=zip_path,
        sha256_path=sha_path,
        sha256_hex=digest,
        member_count=count,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Pack repository skills/ into goal-governance-skills-vX.Y.Z.zip "
            "plus a SHA-256 sidecar. Offline; does not publish releases."
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
        "--skills-dir",
        type=Path,
        default=None,
        help="Skills package root (default: <repo>/skills)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = pack_skills(
            version=args.version,
            output_dir=args.output_dir,
            skills_root=args.skills_dir,
        )
    except PackSkillsError as exc:
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
