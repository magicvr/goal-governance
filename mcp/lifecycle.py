"""MCP thin-shell lifecycle: install / upgrade / uninstall / managed markers.

VP-004 R2 productization:
- managed paths allowlist: only ``AGENTS.md`` (managed section) and
  ``.goal-governance/`` (tool state) may be written by lifecycle tools.
- default confirm-before-write: every write op requires ``confirm=True``.
- AGENTS.md governance content is wrapped in machine-parsable markers;
  update/uninstall touch ONLY the marker region, user content outside the
  markers stays byte-identical.

All write paths are validated against the allowlist and must stay inside the
repository root (absolute paths and ``..`` escapes fail closed).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MANAGED_BEGIN = "<!-- goal-governance:begin managed -->"
MANAGED_END = "<!-- goal-governance:end managed -->"
THIN_SHELL_DIR = ".goal-governance"
INSTALL_JSON = "install.json"
MANAGED_PATHS_ALLOWLIST = frozenset({"AGENTS.md", THIN_SHELL_DIR})

# Version of the thin shell managed content layout (bumps on breaking layout).
MANAGED_LAYOUT_VERSION = "1"


class LifecycleError(ValueError):
    """Raised when a lifecycle operation cannot be performed safely."""


@dataclass(frozen=True)
class WriteResult:
    """Outcome of a lifecycle write operation."""

    operation: str
    wrote: list[str]  # repo-relative paths written
    version: str
    channel: str
    notes: list[str] = field(default_factory=list)


def _repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise LifecycleError(
            f"path escapes repository root: {path}"
        ) from error


def _ensure_inside_repo(root: Path, candidate: Path | str) -> Path:
    """Validate a candidate path stays inside the repo root (fail closed)."""
    candidate = Path(candidate)
    root_resolved = root.resolve()
    if not candidate.is_absolute():
        candidate = root_resolved / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as error:
        raise LifecycleError(
            f"path escapes repository root (fail closed): {candidate}"
        ) from error
    return resolved


def _validate_allowlist(root: Path, relative_parts: list[str]) -> None:
    for part in relative_parts:
        first = Path(part).parts[0]
        if first not in MANAGED_PATHS_ALLOWLIST:
            raise LifecycleError(
                f"path outside managed paths allowlist: {part} "
                f"(allowlist: {sorted(MANAGED_PATHS_ALLOWLIST)})"
            )


# ---------------------------------------------------------------- markers
def managed_section(version: str) -> str:
    """The managed AGENTS.md section payload (markers inclusive)."""
    return (
        f"{MANAGED_BEGIN}\n"
        "<!-- goal-governance 薄壳 managed 段 · 更新/卸载只改本段 -->\n"
        f"- version: {version}\n"
        f"- layout: {MANAGED_LAYOUT_VERSION}\n"
        "- 治理记录树：`{governance_root}`（默认 `docs/`，可配置）\n"
        "- 实例真相在仓库内治理记录；MCP 不是权威状态库\n"
        "- 四治理入口：`vision` / `vision-audit` / `govern` / `audit`（`commit` 便利可选）\n"
        "- 规则全文：AGENTS.md §6/6b/6d/6e；`docs/architecture/principles.md`（必备）\n"
        f"{MANAGED_END}"
    )


def replace_managed_section(agents_text: str, version: str) -> str:
    """Insert/replace the managed section; everything outside markers is kept
    byte-identical."""
    section = managed_section(version)
    if MANAGED_BEGIN in agents_text:
        begin = agents_text.index(MANAGED_BEGIN)
        if MANAGED_END not in agents_text:
            raise LifecycleError("managed section is malformed: begin without end")
        end = agents_text.index(MANAGED_END) + len(MANAGED_END)
        return agents_text[:begin] + section + agents_text[end:]
    if MANAGED_END in agents_text:
        raise LifecycleError("managed section is malformed: end without begin")
    if agents_text and not agents_text.endswith("\n"):
        agents_text += "\n"
    return agents_text + section + "\n"


def remove_managed_section(agents_text: str) -> str:
    """Remove only the managed section (markers + content)."""
    if MANAGED_BEGIN not in agents_text and MANAGED_END not in agents_text:
        return agents_text
    if MANAGED_BEGIN in agents_text and MANAGED_END in agents_text:
        begin = agents_text.index(MANAGED_BEGIN)
        end = agents_text.index(MANAGED_END) + len(MANAGED_END)
        removed = agents_text[:begin] + agents_text[end:]
        # Clean up a dangling newline left by the removed block.
        while removed.endswith("\n\n"):
            removed = removed[:-1]
        return removed
    raise LifecycleError("managed section is malformed: begin/end markers mismatch")


def parse_managed_version(agents_text: str) -> str | None:
    """Extract the version line from the managed section (if present)."""
    if MANAGED_BEGIN not in agents_text or MANAGED_END not in agents_text:
        return None
    section = agents_text[
        agents_text.index(MANAGED_BEGIN) : agents_text.index(MANAGED_END)
    ]
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- version:"):
            return stripped.split(":", 1)[1].strip()
    return None


# ------------------------------------------------------------ state files
def write_install_state(root: Path, *, channel: str, version: str) -> Path:
    state_dir = _ensure_inside_repo(root, THIN_SHELL_DIR)
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / INSTALL_JSON
    payload = {
        "channel": channel,
        "version": version,
        "layout": MANAGED_LAYOUT_VERSION,
        "installedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
    state_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return state_file


def read_install_state(root: Path) -> dict[str, Any] | None:
    state_file = _ensure_inside_repo(root, THIN_SHELL_DIR) / INSTALL_JSON
    if not state_file.is_file():
        return None
    try:
        payload = json.loads(state_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"error": "install.json is not valid JSON"}
    if not isinstance(payload, dict):
        return {"error": "install.json must be an object"}
    return payload


# ------------------------------------------------------------- lifecycle
def install(
    root: Path,
    *,
    confirm: bool,
    version: str,
    channel: str = "mcp",
) -> WriteResult:
    if not confirm:
        raise LifecycleError(
            "write requires explicit confirmation: pass confirm=true "
            "(默认确认写盘)"
        )
    if not version:
        raise LifecycleError("version must be non-empty")
    root = root.resolve()
    if not root.is_dir():
        raise LifecycleError(f"repository root is not a directory: {root}")
    # Defense in depth: every write target must pass the allowlist gate.
    _validate_allowlist(root, ["AGENTS.md", THIN_SHELL_DIR])

    agents_path = _ensure_inside_repo(root, "AGENTS.md")
    original = (
        agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
    )
    updated = replace_managed_section(original, version)
    agents_path.parent.mkdir(parents=True, exist_ok=True)
    agents_path.write_text(updated, encoding="utf-8", newline="")
    state_file = write_install_state(root, channel=channel, version=version)
    return WriteResult(
        operation="install",
        wrote=[_repo_relative(root, agents_path), _repo_relative(root, state_file)],
        version=version,
        channel=channel,
    )


def upgrade(
    root: Path,
    *,
    confirm: bool,
    version: str,
) -> WriteResult:
    if not confirm:
        raise LifecycleError(
            "write requires explicit confirmation: pass confirm=true "
            "(默认确认写盘)"
        )
    if not version:
        raise LifecycleError("version must be non-empty")
    root = root.resolve()
    _validate_allowlist(root, ["AGENTS.md", THIN_SHELL_DIR])
    agents_path = _ensure_inside_repo(root, "AGENTS.md")
    if not agents_path.is_file():
        raise LifecycleError(
            "AGENTS.md not found; run install first (upgrade only rewrites "
            "the managed section)"
        )
    original = agents_path.read_text(encoding="utf-8")
    if MANAGED_BEGIN not in original:
        raise LifecycleError(
            "AGENTS.md has no managed section; run install first"
        )
    updated = replace_managed_section(original, version)
    agents_path.write_text(updated, encoding="utf-8", newline="")
    state_file = write_install_state(root, channel="mcp", version=version)
    return WriteResult(
        operation="upgrade",
        wrote=[_repo_relative(root, agents_path), _repo_relative(root, state_file)],
        version=version,
        channel="mcp",
    )


def uninstall(
    root: Path,
    *,
    confirm: bool,
) -> WriteResult:
    if not confirm:
        raise LifecycleError(
            "write requires explicit confirmation: pass confirm=true "
            "(默认确认写盘)"
        )
    root = root.resolve()
    _validate_allowlist(root, ["AGENTS.md", THIN_SHELL_DIR])
    wrote: list[str] = []
    agents_path = _ensure_inside_repo(root, "AGENTS.md")
    if agents_path.is_file():
        original = agents_path.read_text(encoding="utf-8")
        if MANAGED_BEGIN in original or MANAGED_END in original:
            updated = remove_managed_section(original)
            agents_path.write_text(updated, encoding="utf-8", newline="")
            wrote.append(_repo_relative(root, agents_path))

    state_dir = _ensure_inside_repo(root, THIN_SHELL_DIR)
    if state_dir.is_dir():
        for child in sorted(state_dir.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                try:
                    child.rmdir()
                except OSError:
                    pass
        try:
            state_dir.rmdir()
        except OSError:
            pass
        wrote.append(_repo_relative(root, state_dir))

    return WriteResult(
        operation="uninstall",
        wrote=wrote,
        version="",
        channel="",
    )


def build_parser() -> argparse.ArgumentParser:
    """CLI used by bootstrap -Channel mcp (single source of truth for markers)."""
    parser = argparse.ArgumentParser(
        description="MCP thin-shell lifecycle (install/upgrade/uninstall/state)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_p = subparsers.add_parser("install", help="Install thin shell (AGENTS managed + state).")
    install_p.add_argument("--root", type=Path, required=True)
    install_p.add_argument("--version", required=True)
    install_p.add_argument("--channel", default="mcp")
    install_p.add_argument("--confirm", action="store_true")

    upgrade_p = subparsers.add_parser("upgrade", help="Upgrade managed section + state.")
    upgrade_p.add_argument("--root", type=Path, required=True)
    upgrade_p.add_argument("--version", required=True)
    upgrade_p.add_argument("--confirm", action="store_true")

    uninstall_p = subparsers.add_parser("uninstall", help="Remove thin shell (managed section + state).")
    uninstall_p.add_argument("--root", type=Path, required=True)
    uninstall_p.add_argument("--confirm", action="store_true")

    state_p = subparsers.add_parser("state", help="Print thin-shell state JSON (read-only).")
    state_p.add_argument("--root", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "install":
            result = install(
                args.root, confirm=args.confirm, version=args.version, channel=args.channel
            )
        elif args.command == "upgrade":
            result = upgrade(args.root, confirm=args.confirm, version=args.version)
        elif args.command == "uninstall":
            result = uninstall(args.root, confirm=args.confirm)
        else:
            payload = read_install_state(args.root)
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
            return 0
    except LifecycleError as error:
        print(f"lifecycle error: {error}", file=sys.stderr)
        return 2
    print(json.dumps({"operation": result.operation, "wrote": result.wrote}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
