"""Request-scoped product workspace focus (GOAL-015 stage C).

Priority (R-015-A §5):
1. Explicit focus cookie / query workspace_id (validated against registry under DATA_ROOT)
2. Single active workspace under DATA_ROOT
3. α single WORKSPACE_DIR / DATA_ROOT single-path config (GoalsRepository.from_config)
4. Multi without focus → fail closed (not pretend a default)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from services.goals_repo import GoalsRepository
from services.workspace_config import (
    COOKIE_FOCUS_WORKSPACE,
    ENV_DATA_ROOT,
    ENV_WORKSPACE_DIR,
    resolve_data_root,
    resolve_workspace_config,
)
from services.workspace_registry import WorkspaceRegistryService


@dataclass(frozen=True)
class FocusState:
    """UI/API helper for N1 navigation chrome."""

    data_root: Path | None
    workspaces: tuple[dict[str, str], ...]  # N1 rows only
    focus_workspace_id: str | None
    multi_mode: bool
    needs_selection: bool
    selection_error: str | None = None

    def as_template_dict(self) -> dict[str, Any]:
        return {
            "n1_workspaces": list(self.workspaces),
            "focus_workspace_id": self.focus_workspace_id,
            "workspace_multi_mode": self.multi_mode,
            "workspace_needs_selection": self.needs_selection,
            "workspace_selection_error": self.selection_error,
            "data_root": str(self.data_root) if self.data_root else None,
        }


def _focus_id_from_request(request: Any | None) -> str | None:
    if request is None:
        return None
    # Query override (bookmarkable; still validated)
    try:
        q = request.query_params.get("workspace_id")
    except Exception:
        q = None
    if q and str(q).strip():
        return str(q).strip()
    try:
        c = request.cookies.get(COOKIE_FOCUS_WORKSPACE)
    except Exception:
        c = None
    if c and str(c).strip():
        return str(c).strip()
    return None


def build_focus_state(
    request: Any | None = None,
    environ: Mapping[str, str] | None = None,
) -> FocusState:
    env = dict(environ) if environ is not None else None
    data_root = resolve_data_root(env)
    if data_root is None:
        return FocusState(
            data_root=None,
            workspaces=(),
            focus_workspace_id=None,
            multi_mode=False,
            needs_selection=False,
        )

    svc = WorkspaceRegistryService(data_root)
    listed = svc.list_n1(include_archived=False)
    rows: list[dict[str, str]] = []
    if listed.ok:
        rows = list(listed.details.get("workspaces") or [])

    focus = _focus_id_from_request(request)
    multi = len(rows) > 1
    needs = False
    err: str | None = None

    if focus:
        got = svc.get(focus, include_archived=False)
        if not got.ok:
            err = got.message or f"invalid focus workspace: {focus}"
            focus = None
            if multi:
                needs = True
    elif multi:
        needs = True
        err = "多个工作区可用：请先选择当前工作区（不会默认猜测）。"
    elif len(rows) == 1:
        focus = rows[0]["workspace_id"]

    return FocusState(
        data_root=data_root,
        workspaces=tuple(rows),
        focus_workspace_id=focus,
        multi_mode=multi or bool(rows),
        needs_selection=needs,
        selection_error=err,
    )


def resolve_repository_for_request(
    request: Any | None = None,
    environ: Mapping[str, str] | None = None,
) -> GoalsRepository:
    """Build GoalsRepository for the focused product workspace."""
    env_map = dict(environ) if environ is not None else None
    state = build_focus_state(request, env_map)
    data_root = state.data_root

    # Multi / registry path when DATA_ROOT is set and we have N1 rows or multi intent.
    if data_root is not None and (state.workspaces or state.multi_mode):
        if state.needs_selection or not state.focus_workspace_id:
            return GoalsRepository(
                Path("__unconfigured_workspace__"),
                config_source="n1-focus",
                config_error=state.selection_error
                or "No workspace focus selected (multi-workspace fail closed).",
            )
        svc = WorkspaceRegistryService(data_root)
        path_r = svc.resolve_path(state.focus_workspace_id)
        if not path_r.ok:
            return GoalsRepository(
                Path("__unconfigured_workspace__"),
                config_source="n1-focus",
                config_error=path_r.message or "focus workspace path unresolved",
            )
        return GoalsRepository(
            Path(str(path_r.details["path"])),
            config_source=f"n1:{state.focus_workspace_id}",
            config_error=None,
        )

    # α / single-path config (WORKSPACE_DIR or DATA_ROOT single resolve).
    return GoalsRepository.from_config(env_map)


def validate_focus_workspace_id(
    workspace_id: str,
    environ: Mapping[str, str] | None = None,
) -> tuple[bool, str | None, str | None]:
    """Return (ok, path, error)."""
    data_root = resolve_data_root(dict(environ) if environ is not None else None)
    if data_root is None:
        # Allow selecting only when multi registry exists; α mode has no switcher ids.
        cfg = resolve_workspace_config(dict(environ) if environ is not None else None)
        if cfg.is_ready and cfg.workspace_dir is not None:
            # Single configured path — accept folder name or workspace.md id loosely.
            return True, str(cfg.workspace_dir), None
        return False, None, "DATA_ROOT not configured for multi-workspace selection"
    svc = WorkspaceRegistryService(data_root)
    got = svc.get(workspace_id.strip(), include_archived=False)
    if not got.ok:
        return False, None, got.message
    return True, str(got.details["path"]), None
