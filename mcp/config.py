"""Configurable governance root (VP-004 R3).

``governance_root`` defaults to ``docs`` and may be pinned to any other
repo-relative directory via the committable project config
``.goal-governance.json``. Resolution is fail-closed: absolute paths,
``..`` escapes, and paths resolving outside the repository root are rejected
with explicit errors. The internal layout under the root (``vision/``,
``workspaces/workspace-*``, ``goal-tree.md``, the goal five-piece shape)
is frozen — only the root prefix is configurable. Direct child
``workspace-*`` folders are legacy migration inputs and never canonical
write targets.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DEFAULT_GOVERNANCE_ROOT = "docs"
CONFIG_FILENAME = ".goal-governance.json"
WORKSPACES_DIRNAME = "workspaces"
WORKSPACE_GLOB = "workspace-*"
AUDIT_EFFORTS = {
    "codex": ("minimal", "low", "medium", "high", "xhigh"),
    "claude": ("low", "medium", "high", "max"),
    "grok": ("low", "medium", "high", "xhigh"),
}


def validate_independent_audit(value: Any) -> dict[str, str]:
    """Validate one complete CLI profile; never coerce or mix providers."""
    fields = {"provider", "model", "reasoning_effort"}
    if not isinstance(value, dict) or set(value) != fields:
        raise GovernanceRootError(
            "independent_audit must contain exactly provider, model, reasoning_effort"
        )
    provider = value["provider"]
    if not isinstance(provider, str) or provider not in AUDIT_EFFORTS:
        raise GovernanceRootError("independent_audit.provider must be codex, claude or grok")
    model = value["model"]
    if not isinstance(model, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*", model):
        raise GovernanceRootError("independent_audit.model must be a non-empty model identifier")
    effort = value["reasoning_effort"]
    if not isinstance(effort, str) or effort not in AUDIT_EFFORTS[provider]:
        raise GovernanceRootError(
            f"independent_audit.reasoning_effort is invalid for {provider}"
        )
    return dict(value)


def resolve_independent_audit(
    repo_root: Path, *, override: dict[str, Any] | None = None,
) -> dict[str, str] | None:
    """Explicit session profile wins; a valid project profile persists across sessions."""
    project = load_project_config(repo_root)
    if override is not None:
        return validate_independent_audit(override)
    if project is None or "independent_audit" not in project:
        return None
    return validate_independent_audit(project["independent_audit"])


def independent_audit_argv(profile: dict[str, Any]) -> list[str]:
    """Return model/effort argv only; callers add the formal command, never a shell."""
    item = validate_independent_audit(profile)
    provider, model, effort = (item[key] for key in ("provider", "model", "reasoning_effort"))
    if provider == "codex":
        return ["codex", "exec", "--model", model, "-c", f'model_reasoning_effort="{effort}"']
    flag = "--effort" if provider == "claude" else "--reasoning-effort"
    return [provider, "--model", model, flag, effort]


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
    if not config_path.exists() and not config_path.is_symlink():
        return None
    if not config_path.is_file() or not config_path.resolve().is_relative_to(repo_root.resolve()):
        raise GovernanceRootError(f"{CONFIG_FILENAME} must be a readable file inside the repository")
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError, OSError) as error:
        raise GovernanceRootError(
            f"{CONFIG_FILENAME} is not valid JSON: {error}"
        ) from error
    if not isinstance(payload, dict):
        raise GovernanceRootError(f"{CONFIG_FILENAME} must be a JSON object")
    unknown = set(payload) - {"governance_root", "independent_audit"}
    if unknown:
        raise GovernanceRootError(f"{CONFIG_FILENAME} has unknown fields: {', '.join(sorted(unknown))}")
    if "governance_root" in payload:
        _validate_root_name(repo_root, payload["governance_root"])
    if "independent_audit" in payload:
        validate_independent_audit(payload["independent_audit"])
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


def workspace_layout_report(governance_root: Path) -> dict[str, Any]:
    """Describe canonical and legacy explicit workspace layouts without writes."""
    root = governance_root.resolve()
    canonical_parent = root / WORKSPACES_DIRNAME
    canonical = sorted(
        path.parent.name
        for path in canonical_parent.glob(f"{WORKSPACE_GLOB}/workspace.md")
        if path.is_file()
    )
    legacy = sorted(
        path.parent.name
        for path in root.glob(f"{WORKSPACE_GLOB}/workspace.md")
        if path.is_file()
    )
    if canonical and legacy:
        state = "mixed"
    elif legacy:
        state = "legacy"
    elif canonical:
        state = "canonical"
    else:
        state = "empty"
    return {
        "state": state,
        "canonicalRoot": WORKSPACES_DIRNAME,
        "canonical": canonical,
        "legacy": legacy,
    }
