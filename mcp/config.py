"""Configurable governance root (VP-004 R3).

``governance_root`` defaults to ``docs`` and may be pinned to any other
repo-relative directory via the committable project config
``.goal-governance.json``. Resolution is fail-closed: absolute paths,
``..`` escapes, and paths resolving outside the repository root are rejected
with explicit errors. The internal layout under the root (``vision/``,
``workspace-*``, ``goal-tree.md``, the goal five-piece shape) is frozen — only
the root prefix is configurable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_GOVERNANCE_ROOT = "docs"
CONFIG_FILENAME = ".goal-governance.json"


class GovernanceRootError(ValueError):
    """Raised when governance_root cannot be resolved safely."""


def _validate_root_name(repo_root: Path, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GovernanceRootError(
            "governance_root must be a non-empty string"
        )
    name = value.strip()
    if name in {".", ".."} or any(part in {"..", ""} for part in name.replace("\\", "/").split("/")):
        raise GovernanceRootError(
            f"governance_root must be a plain relative path (got {value!r}); "
            "absolute paths and '..' escapes fail closed"
        )
    candidate = Path(name)
    if candidate.is_absolute() or name.startswith(("/", "\\")) or len(name) > 1 and name[1] == ":":
        raise GovernanceRootError(
            f"governance_root must be relative to the repository root (got {value!r})"
        )
    root_resolved = repo_root.resolve()
    resolved = (root_resolved / name).resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as error:
        raise GovernanceRootError(
            f"governance_root escapes the repository root (fail closed): {value!r}"
        ) from error
    return name


def load_project_config(repo_root: Path) -> dict[str, Any] | None:
    """Read .goal-governance.json at the repository root (committable pin)."""
    config_path = repo_root / CONFIG_FILENAME
    if not config_path.is_file():
        return None
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise GovernanceRootError(
            f"{CONFIG_FILENAME} is not valid JSON: {error}"
        ) from error
    if not isinstance(payload, dict):
        raise GovernanceRootError(f"{CONFIG_FILENAME} must be a JSON object")
    return payload


def resolve_governance_root(
    repo_root: Path,
    config: dict[str, Any] | None = None,
) -> str:
    """Return the validated governance root name (default ``docs``).

    ``config`` may be passed explicitly (e.g. from a test or an MCP tool);
    when None, ``.goal-governance.json`` at ``repo_root`` is read.
    """
    repo_root = repo_root.resolve()
    if config is None:
        config = load_project_config(repo_root)
    if not config:
        return DEFAULT_GOVERNANCE_ROOT
    if "governance_root" not in config:
        return DEFAULT_GOVERNANCE_ROOT
    return _validate_root_name(repo_root, config["governance_root"])


def governance_root_dir(repo_root: Path, config: dict[str, Any] | None = None) -> Path:
    """Return the resolved root directory for the validated governance root."""
    name = resolve_governance_root(repo_root, config=config)
    return (repo_root / name).resolve()
