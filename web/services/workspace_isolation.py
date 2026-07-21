"""R-003 workspace isolation validation (WS-001..WS-006 pure / service-layer).

Design freeze: GOAL-009 attachments/r-003-verification-package.md.
No canonical writes; no multi-workspace product UI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping

# N1 allowlist (D-011 / R-003).
N1_ALLOWED_FIELDS = frozenset(
    {
        "workspace_id",
        "display_name",
        "root_goal",
        "status",  # active | archived only at N1
    }
)
N1_FORBIDDEN_FIELDS = frozenset(
    {
        "progress",
        "finding",
        "findings",
        "candidate",
        "candidates",
        "ai_draft",
        "ai_drafts",
        "material_body",
        "material_content",
        "goal_tree",
        "goal_body",
        "execution_body",
        "audit_body",
    }
)

ERR_WS_ROOT_GOAL_MISMATCH = "ERR_WS_ROOT_GOAL_MISMATCH"
ERR_WS_CANONICAL_SCOPE_MISMATCH = "ERR_WS_CANONICAL_SCOPE_MISMATCH"
ERR_WS_CROSS_WORKSPACE_ACCESS = "ERR_WS_CROSS_WORKSPACE_ACCESS"
ERR_WS_N1_FIELD_CONTRACT = "ERR_WS_N1_FIELD_CONTRACT"
ERR_WS_DOGFOOD_DEFAULT = "ERR_WS_DOGFOOD_DEFAULT"
ERR_WS_INDEX_CANONICAL_CONFLICT = "ERR_WS_INDEX_CANONICAL_CONFLICT"


@dataclass(frozen=True)
class IsolationResult:
    ok: bool
    code: str | None = None
    message: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)
    # When index conflicts with markdown, markdown wins and index is invalid.
    index_status: str | None = None  # "valid" | "invalid" | None

    @classmethod
    def success(cls, **details: object) -> IsolationResult:
        return cls(ok=True, details=details)

    @classmethod
    def failure(cls, code: str, message: str, **details: object) -> IsolationResult:
        return cls(ok=False, code=code, message=message, details=details)


@dataclass(frozen=True)
class WorkspaceBinding:
    """Declared binding for one product workspace."""

    workspace_id: str
    root_goal: str
    canonical_scope: str  # path or logical scope string
    workspace_root: Path | None = None  # actual root on disk when known


@dataclass(frozen=True)
class DiskRootFact:
    """Observed facts from a workspace directory (test-supplied; no I/O here)."""

    root_goal_ids: tuple[str, ...]  # parent:null goals found
    actual_root_path: str  # normalized path string for scope compare


@dataclass(frozen=True)
class AccessRequest:
    """Attempt to read/write a goal path under a workspace."""

    bound_workspace_id: str
    target_workspace_id: str
    target_path: str  # e.g. GOAL-001-x/02-execution.md
    action: str  # "read" | "write"


@dataclass(frozen=True)
class IndexGoalRow:
    goal_id: str
    status: str | None  # e.g. "done"


def _norm_path(p: str) -> str:
    return str(Path(p).as_posix()).rstrip("/").lower()


def validate_root_goal_binding(
    binding: WorkspaceBinding,
    disk: DiskRootFact,
) -> IsolationResult:
    """WS-001: root_goal must match the unique disk Root."""
    roots = tuple(g for g in disk.root_goal_ids if g)
    if len(roots) != 1:
        return IsolationResult.failure(
            ERR_WS_ROOT_GOAL_MISMATCH,
            "workspace must have exactly one parent:null Root Goal on disk",
            root_goal_ids=list(roots),
            declared=binding.root_goal,
        )
    if roots[0] != binding.root_goal:
        return IsolationResult.failure(
            ERR_WS_ROOT_GOAL_MISMATCH,
            "declared root_goal does not match disk Root",
            declared=binding.root_goal,
            disk_root=roots[0],
        )
    return IsolationResult.success(root_goal=binding.root_goal)


def validate_canonical_scope(
    binding: WorkspaceBinding,
    disk: DiskRootFact,
    *,
    other_workspace_roots: Iterable[str] = (),
) -> IsolationResult:
    """WS-002: canonical_scope must match actual root; must not point at another WS."""
    declared = _norm_path(binding.canonical_scope)
    actual = _norm_path(disk.actual_root_path)
    if declared != actual:
        return IsolationResult.failure(
            ERR_WS_CANONICAL_SCOPE_MISMATCH,
            "canonical_scope does not match actual workspace root",
            declared=binding.canonical_scope,
            actual=disk.actual_root_path,
        )
    for other in other_workspace_roots:
        other_n = _norm_path(other)
        if other_n and other_n != actual and (
            declared == other_n
            or declared.startswith(other_n + "/")
            or other_n.startswith(declared + "/")
        ):
            # Pointing at or nested under another product workspace root.
            if declared == other_n or declared.startswith(other_n + "/"):
                return IsolationResult.failure(
                    ERR_WS_CANONICAL_SCOPE_MISMATCH,
                    "canonical_scope points at another product workspace",
                    declared=binding.canonical_scope,
                    other=other,
                )
    return IsolationResult.success(canonical_scope=binding.canonical_scope)


def validate_cross_workspace_access(req: AccessRequest) -> IsolationResult:
    """WS-003: refuse read/write of another product workspace goal tree."""
    if req.bound_workspace_id != req.target_workspace_id:
        return IsolationResult.failure(
            ERR_WS_CROSS_WORKSPACE_ACCESS,
            "cross-workspace goal access denied; no foreign body returned",
            bound=req.bound_workspace_id,
            target=req.target_workspace_id,
            action=req.action,
            leaked_body=False,
        )
    return IsolationResult.success()


def validate_n1_list_row(row: Mapping[str, object]) -> IsolationResult:
    """WS-004: N1 rows must not include forbidden progress/finding/candidate/body fields."""
    keys = set(row.keys())
    forbidden = keys & N1_FORBIDDEN_FIELDS
    if forbidden:
        return IsolationResult.failure(
            ERR_WS_N1_FIELD_CONTRACT,
            "N1 list row contains forbidden fields",
            forbidden=sorted(forbidden),
        )
    # Unknown fields beyond allowlist are also rejected for strict contract.
    extra = keys - N1_ALLOWED_FIELDS
    if extra:
        return IsolationResult.failure(
            ERR_WS_N1_FIELD_CONTRACT,
            "N1 list row contains non-N1 fields",
            extra=sorted(extra),
        )
    status = row.get("status")
    if status is not None and status not in {"active", "archived"}:
        return IsolationResult.failure(
            ERR_WS_N1_FIELD_CONTRACT,
            "N1 status must be active or archived",
            status=status,
        )
    return IsolationResult.success()


def validate_workspace_load_policy(
    *,
    workspace_configured: bool,
    dev_dogfood: bool,
    would_load_dogfood_default: bool,
) -> IsolationResult:
    """WS-005: without config, do not default-load monorepo dogfood unless DEV_DOGFOOD."""
    if would_load_dogfood_default and not workspace_configured and not dev_dogfood:
        return IsolationResult.failure(
            ERR_WS_DOGFOOD_DEFAULT,
            "refuse default dogfood load without explicit config or DEV_DOGFOOD",
        )
    if would_load_dogfood_default and not workspace_configured and dev_dogfood:
        return IsolationResult.success(mode="dev_dogfood_opt_in")
    if not workspace_configured and not dev_dogfood:
        # Fail closed idle — ok for isolation policy (no load).
        return IsolationResult.success(mode="idle_fail_closed")
    return IsolationResult.success(mode="configured")


def resolve_index_vs_canonical(
    index_rows: Iterable[IndexGoalRow],
    canonical_status_by_goal: Mapping[str, str],
) -> IsolationResult:
    """WS-006: on conflict, Markdown/canonical wins; mark index invalid (do not trust index)."""
    conflicts: list[dict[str, str]] = []
    for row in index_rows:
        canon = canonical_status_by_goal.get(row.goal_id)
        if canon is None:
            continue
        if row.status is not None and row.status != canon:
            conflicts.append(
                {
                    "goal_id": row.goal_id,
                    "index_status": str(row.status),
                    "canonical_status": canon,
                }
            )
    if conflicts:
        return IsolationResult(
            ok=True,  # operation may continue using canonical
            code=ERR_WS_INDEX_CANONICAL_CONFLICT,
            message="index conflicts with canonical; use Markdown, mark index invalid",
            details={"conflicts": conflicts},
            index_status="invalid",
        )
    return IsolationResult(ok=True, index_status="valid", details={})
