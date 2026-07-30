#!/usr/bin/env python3
"""Stage Skills distribution mirrors from monorepo docs/ (GOAL-022).

Canonical truth lives under docs/. Byte-identical consumer mirrors are generated
into skills/core/docs (methodology subset) and skills/contracts.

Hand-maintained (never overwritten by stage):
  - skills/core/docs/README.md          (consumer slim entry)
  - skills/core/docs/vision/README.md   (consumer vision index)
  - skills/core/README.md               (core package explainer)

Does not ship tech-stack.md. Does not copy monorepo dogfood vision instances.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

ARCHITECTURE_FILES = (
    "principles.md",
    "workspace-protocol.md",
    "overview.md",
    "directory-layout.md",
)

# Relative to docs/ → relative destination under skills/
PROTECTED_CORE_RELATIVE = frozenset(
    {
        "README.md",
        "vision/README.md",
    }
)


class StageSkillsError(ValueError):
    """Raised when staging inputs are invalid or mirrors drift in --check mode."""


@dataclass(frozen=True)
class StageResult:
    copied: int
    checked: int
    removed: int
    mode: str


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _copy_file(src: Path, dest: Path, *, dry_run: bool) -> None:
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def _iter_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(path for path in root.rglob("*") if path.is_file())


def planned_pairs(repo_root: Path) -> list[tuple[Path, Path]]:
    """Return (canonical, mirror) pairs that stage owns (byte-identical)."""
    docs = repo_root / "docs"
    skills = repo_root / "skills"
    pairs: list[tuple[Path, Path]] = []

    for name in ARCHITECTURE_FILES:
        pairs.append(
            (
                docs / "architecture" / name,
                skills / "core" / "docs" / "architecture" / name,
            )
        )

    templates_src = docs / "templates"
    for src in _iter_files(templates_src):
        rel = src.relative_to(templates_src)
        pairs.append((src, skills / "core" / "docs" / "templates" / rel))

    pairs.append(
        (
            docs / "vision" / "alignment.md",
            skills / "core" / "docs" / "vision" / "alignment.md",
        )
    )

    contracts_src = docs / "contracts"
    for src in _iter_files(contracts_src):
        rel = src.relative_to(contracts_src)
        pairs.append((src, skills / "contracts" / rel))

    return pairs


def _assert_canonical_present(pairs: list[tuple[Path, Path]]) -> None:
    missing = [str(src) for src, _ in pairs if not src.is_file()]
    if missing:
        raise StageSkillsError(
            "canonical sources missing: " + ", ".join(missing[:12])
            + (" ..." if len(missing) > 12 else "")
        )


def _remove_legacy_skills_templates(skills: Path, *, dry_run: bool) -> int:
    """Drop hand-maintained skills/templates content except a pointer README.

    GOAL-022 I-002: distribution source is core/docs/templates only.
    """
    templates = skills / "templates"
    removed = 0
    if not templates.is_dir():
        return 0

    keep_readme = templates / "README.md"
    for path in sorted(templates.rglob("*"), reverse=True):
        if path == keep_readme:
            continue
        if path.is_file() or path.is_symlink():
            if not dry_run:
                path.unlink()
            removed += 1
        elif path.is_dir():
            try:
                if not dry_run:
                    path.rmdir()
            except OSError:
                pass

    pointer = """---
title: Skills templates pointer (not a second truth)
status: active
created: 2026-07-19
updated: 2026-07-30
parent: null
version: 0.3.0
---

# skills/templates · 已收敛

**GOAL-022**：包内模板分发源为 **`core/docs/templates/`**（由 monorepo `docs/templates/` stage 生成）。

本目录**不再**维护五件套或 `workspace-context.md` 副本。

| 需要 | 使用路径 |
|------|----------|
| 消费仓 install 默认落点 | `docs/templates/`（从 `core/docs/templates` 安装） |
| 包内离线模板 | `skills/core/docs/templates/goal-folder/` |
| monorepo 编辑 | **只改** `docs/templates/`，再运行 `python scripts/stage_skills_mirrors.py` |

遗留路径 `skills/templates/goal-folder` 若出现在旧文档中，请改读 `core/docs/templates/goal-folder`。
"""
    if not dry_run:
        templates.mkdir(parents=True, exist_ok=True)
        keep_readme.write_text(pointer.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return removed


def stage_skills_mirrors(
    repo_root: Path | None = None,
    *,
    check: bool = False,
    dry_run: bool = False,
) -> StageResult:
    """Copy or verify docs/ → skills mirrors. Returns counts."""
    root = (repo_root or REPO_ROOT).resolve()
    docs = root / "docs"
    skills = root / "skills"
    if not docs.is_dir():
        raise StageSkillsError(f"docs/ not found under {root}")
    if not skills.is_dir():
        raise StageSkillsError(f"skills/ not found under {root}")

    tech = skills / "core" / "docs" / "architecture" / "tech-stack.md"
    if tech.is_file() and not dry_run and not check:
        tech.unlink()

    pairs = planned_pairs(root)
    _assert_canonical_present(pairs)

    copied = 0
    checked = 0
    drifts: list[str] = []

    for src, dest in pairs:
        rel_core = None
        try:
            rel_core = dest.relative_to(skills / "core" / "docs").as_posix()
        except ValueError:
            rel_core = None
        if rel_core in PROTECTED_CORE_RELATIVE:
            continue

        checked += 1
        if check:
            if not dest.is_file() or _sha256(src) != _sha256(dest):
                drifts.append(f"{src.relative_to(root).as_posix()} -> {dest.relative_to(root).as_posix()}")
            continue

        if dest.is_file() and _sha256(src) == _sha256(dest):
            continue
        _copy_file(src, dest, dry_run=dry_run)
        copied += 1

    if check and drifts:
        raise StageSkillsError(
            "skills mirror drift (run: python scripts/stage_skills_mirrors.py):\n  "
            + "\n  ".join(drifts[:40])
            + (f"\n  ... +{len(drifts) - 40} more" if len(drifts) > 40 else "")
        )

    removed = 0
    if not check:
        removed = _remove_legacy_skills_templates(skills, dry_run=dry_run)
        # Ensure protected consumer files still exist (do not create long monorepo copies).
        slim_readme = skills / "core" / "docs" / "README.md"
        if not slim_readme.is_file() and not dry_run:
            raise StageSkillsError(
                "missing hand-maintained skills/core/docs/README.md "
                "(consumer slim entry; stage does not generate it)"
            )
        vision_readme = skills / "core" / "docs" / "vision" / "README.md"
        if not vision_readme.is_file() and not dry_run:
            raise StageSkillsError(
                "missing hand-maintained skills/core/docs/vision/README.md"
            )

    if tech.is_file() and check:
        raise StageSkillsError("skills core must not contain architecture/tech-stack.md")

    mode = "check" if check else ("dry-run" if dry_run else "write")
    return StageResult(copied=copied, checked=checked, removed=removed, mode=mode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Stage skills/core and skills/contracts mirrors from docs/ "
            "(GOAL-022 single source of truth)."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify mirrors match canonical; exit 1 on drift (no writes)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = stage_skills_mirrors(
            args.repo_root,
            check=args.check,
            dry_run=args.dry_run,
        )
    except StageSkillsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"mode: {result.mode}")
    print(f"checked_pairs: {result.checked}")
    print(f"copied: {result.copied}")
    print(f"removed_legacy_template_files: {result.removed}")
    if args.check:
        print("ok: skills mirrors match docs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
