#!/usr/bin/env python3
"""Rebuild the deterministic candidate inventory for shared materials."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from uuid import uuid4


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATERIALS_DIR = Path("docs/shared-materials")
DEFAULT_INDEX_NAME = "index.json"
_ROOT_CONTROL_FILES = {".gitignore", ".gitkeep", "README.md", DEFAULT_INDEX_NAME}
_EXCLUDED_DIRECTORY_NAMES = {".git", "__pycache__"}
_EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


class IndexBuildError(ValueError):
    """The requested material inventory cannot be built safely."""


def _inside(root: Path, candidate: Path, label: str) -> Path:
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as error:
        raise IndexBuildError(f"{label} must stay inside {resolved_root}: {candidate}") from error
    return resolved_candidate


def _repository_path(root: Path, value: str, label: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise IndexBuildError(f"{label} must be a repository-relative path: {value}")
    return _inside(root, root / relative, label)


def _is_excluded(relative: Path, index_relative: Path) -> bool:
    if relative == index_relative:
        return True
    if any(part in _EXCLUDED_DIRECTORY_NAMES or part.startswith(".") for part in relative.parts[:-1]):
        return True
    if relative.parent == Path(".") and relative.name in _ROOT_CONTROL_FILES:
        return True
    return relative.suffix.lower() in _EXCLUDED_SUFFIXES or relative.name.startswith(".")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_inventory(materials_dir: Path, output_path: Path | None = None) -> dict[str, object]:
    """Return a stable candidate inventory without interpreting material contents."""
    materials_dir = materials_dir.resolve()
    if not materials_dir.is_dir():
        raise IndexBuildError(f"materials directory does not exist: {materials_dir}")

    output_path = output_path.resolve() if output_path is not None else materials_dir / DEFAULT_INDEX_NAME
    _inside(materials_dir, output_path, "index output")
    index_relative = output_path.relative_to(materials_dir)
    files: list[dict[str, object]] = []

    for path in sorted(materials_dir.rglob("*"), key=lambda item: item.relative_to(materials_dir).as_posix()):
        relative = path.relative_to(materials_dir)
        if _is_excluded(relative, index_relative):
            continue
        if path.is_symlink():
            raise IndexBuildError(f"symbolic links are not allowed in shared materials: {relative.as_posix()}")
        _inside(materials_dir, path, "material")
        if not path.is_file():
            continue
        files.append(
            {
                "path": relative.as_posix(),
                "sizeBytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )

    return {
        "format": "goal-governance.shared-materials-inventory",
        "version": 1,
        "inventoryOnly": True,
        "files": files,
    }


def write_inventory(output_path: Path, payload: dict[str, object]) -> None:
    """Commit a complete inventory with one atomic replacement."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.parent / f".{output_path.name}.{uuid4().hex}.tmp"
    try:
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, output_path)
    finally:
        if temporary.exists():
            temporary.unlink()


def rebuild_index(materials_dir: Path, output_path: Path | None = None) -> dict[str, object]:
    output_path = output_path if output_path is not None else materials_dir / DEFAULT_INDEX_NAME
    payload = build_inventory(materials_dir, output_path)
    write_inventory(output_path, payload)
    return payload


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild the candidate inventory for docs/shared-materials."
    )
    parser.add_argument(
        "--repo-root",
        default=str(REPO_ROOT),
        help="repository root used to validate relative paths",
    )
    parser.add_argument(
        "--materials-dir",
        default=str(DEFAULT_MATERIALS_DIR),
        help="repository-relative shared materials directory",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_INDEX_NAME,
        help="path relative to the materials directory for the generated index",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    repo_root = Path(args.repo_root).resolve()
    materials_dir = _repository_path(repo_root, args.materials_dir, "materials directory")
    output_relative = Path(args.output)
    if output_relative.is_absolute() or ".." in output_relative.parts:
        raise IndexBuildError(f"index output must stay inside materials directory: {args.output}")
    output_path = _inside(materials_dir, materials_dir / output_relative, "index output")
    payload = rebuild_index(materials_dir, output_path)
    print(f"Rebuilt {output_path}: {len(payload['files'])} candidate file(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except IndexBuildError as error:
        raise SystemExit(f"error: {error}")
