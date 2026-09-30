#!/usr/bin/env python3
"""Render managed-file placeholders for one methodology directory and skills directory.

Installers and ``update.py`` both call this module. A file the installer wrote
matches update when its bytes equal either the package bytes or these rendered
bytes. Any other difference is a hand edit and stays fail closed.
"""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import sys


class RenderError(ValueError):
    """The install path is empty, absolute outside the project, or escapes it."""


def install_token(raw: str, target: Path | None = None) -> str:
    """Return the project-relative posix path written into placeholders.

    ``docs``, ``./docs`` and ``methodology`` stay relative. An absolute path is
    accepted only when it is inside ``target``. ``..`` is rejected.
    """
    text = (raw or "").strip()
    if not text:
        raise RenderError("install path is empty")
    candidate = Path(text)
    if candidate.is_absolute():
        if target is None:
            raise RenderError(f"install path must stay inside the project: {raw}")
        resolved = candidate.resolve()
        try:
            relative = resolved.relative_to(target.resolve())
        except ValueError as error:
            raise RenderError(f"install path must stay inside the project: {raw}") from error
        parts = list(relative.parts)
    else:
        normalized = text.replace("\\", "/")
        parts = [part for part in PurePosixPath(normalized).parts if part != "."]
    if not parts or any(part in ("", "..") for part in parts):
        raise RenderError(f"install path must stay inside the project: {raw}")
    return PurePosixPath(*parts).as_posix()


def render_managed_text(text: str, methodology_dir: str, skills_dir: str) -> str:
    """Replace managed placeholders. ``methodology_dir`` and ``skills_dir`` are tokens."""
    templates = f"{methodology_dir}/templates"
    return (
        text.replace("{{GOVERNANCE_ROOT}}", methodology_dir)
        .replace("{{CORE_TEMPLATES_DIR}}", templates)
        .replace("{{SKILLS_DIR}}", skills_dir)
        .replace("{governance_root}", methodology_dir)
    )


def render_managed_bytes(raw: bytes, methodology_dir: str, skills_dir: str) -> bytes:
    """Return ``raw`` with placeholders rendered, or ``raw`` when it is not UTF-8 text."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    rendered = render_managed_text(text, methodology_dir, skills_dir)
    if rendered == text:
        return raw
    return rendered.encode("utf-8")


def _render_file(path: Path, methodology_dir: str, skills_dir: str) -> None:
    raw = path.read_bytes()
    rendered = render_managed_bytes(raw, methodology_dir, skills_dir)
    if rendered != raw:
        path.write_bytes(rendered)


def _render_tree(root: Path, methodology_dir: str, skills_dir: str) -> None:
    if not root.is_dir():
        raise RenderError(f"managed tree not found: {root}")
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part.startswith(".") for part in path.relative_to(root).parts[:-1]):
            continue
        if path.name.startswith("."):
            continue
        _render_file(path, methodology_dir, skills_dir)


def _tokens(args: argparse.Namespace) -> tuple[str, str]:
    target = Path(args.target_dir).resolve() if args.target_dir else Path.cwd()
    if not args.methodology_dir or not args.skills_dir:
        raise RenderError("--methodology-dir and --skills-dir are required")
    return install_token(args.methodology_dir, target), install_token(args.skills_dir, target)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-dir", default=".")
    parser.add_argument("--path", help="path to print as an install token")
    parser.add_argument("--print-token", action="store_true")
    parser.add_argument("--methodology-dir")
    parser.add_argument("--skills-dir")
    parser.add_argument("--source")
    parser.add_argument("--dest")
    parser.add_argument("--tree", action="append", default=[])
    parser.add_argument("--in-place", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        if args.print_token:
            if not args.path:
                raise RenderError("--print-token requires --path")
            target = Path(args.target_dir).resolve()
            print(install_token(args.path, target))
            return 0
        methodology, skills = _tokens(args)
        if args.source or args.dest:
            if not args.source or not args.dest:
                raise RenderError("--source and --dest are required together")
            source = Path(args.source)
            dest = Path(args.dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(render_managed_bytes(source.read_bytes(), methodology, skills))
        for tree in args.tree:
            _render_tree(Path(tree), methodology, skills)
        for file_name in args.in_place:
            path = Path(file_name)
            if not path.is_file():
                raise RenderError(f"managed file not found: {path}")
            _render_file(path, methodology, skills)
    except (OSError, RenderError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
