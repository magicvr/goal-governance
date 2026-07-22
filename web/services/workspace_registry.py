"""N1 workspace registry / discovery + isolation helpers (GOAL-015 stage B).

Design freeze: GOAL-015 attachments/r-015-a-n1-navigation-boundary.md (R-015-A).
Service layer only — no Web UI (stage C). Registry is a non-canonical navigation
index; Markdown workspace.md + goal tree remain authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from pathlib import Path
from typing import Any, Mapping

import frontmatter

from services.workspace_isolation import (
    AccessRequest,
    DiskRootFact,
    N1_ALLOWED_FIELDS,
    WorkspaceBinding,
    validate_canonical_scope,
    validate_cross_workspace_access,
    validate_n1_list_row,
    validate_root_goal_binding,
)

REGISTRY_SCHEMA = "n1-workspace-registry/v1"
REGISTRY_RELATIVE = Path("workspaces") / "registry.json"

ERR_REG_NO_DATA_ROOT = "ERR_REG_NO_DATA_ROOT"
ERR_REG_NOT_FOUND = "ERR_REG_NOT_FOUND"
ERR_REG_INVALID = "ERR_REG_INVALID"
ERR_REG_ID_CONFLICT = "ERR_REG_ID_CONFLICT"
ERR_REG_CREATE_FAILED = "ERR_REG_CREATE_FAILED"
ERR_REG_CROSS_WORKSPACE = "ERR_REG_CROSS_WORKSPACE"
ERR_REG_N1_CONTRACT = "ERR_REG_N1_CONTRACT"

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_WS_ID_RE = re.compile(r"^workspace-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")
_GOAL_DIR_RE = re.compile(r"^GOAL-\d{3}-")


@dataclass(frozen=True)
class RegistryResult:
    ok: bool
    code: str | None = None
    message: str | None = None
    details: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls, **details: Any) -> RegistryResult:
        return cls(ok=True, details=details)

    @classmethod
    def failure(cls, code: str, message: str, **details: Any) -> RegistryResult:
        return cls(ok=False, code=code, message=message, details=details)


@dataclass(frozen=True)
class DiscoveredWorkspace:
    """Internal discovery record (may include path; not N1 list payload)."""

    workspace_id: str
    display_name: str
    root_goal: str
    status: str  # active | archived
    path: Path
    valid: bool
    error: str | None = None
    validation_code: str | None = None

    def to_n1_dict(self) -> dict[str, str]:
        """Strict N1 whitelist row (WS-004)."""
        return {
            "workspace_id": self.workspace_id,
            "display_name": self.display_name,
            "root_goal": self.root_goal,
            "status": self.status,
        }


def n1_public_row(row: Mapping[str, object]) -> RegistryResult:
    """Validate and return a strict N1 dict (strips unknown keys first)."""
    cleaned = {
        k: row[k]
        for k in ("workspace_id", "display_name", "root_goal", "status")
        if k in row
    }
    check = validate_n1_list_row(cleaned)
    if not check.ok:
        return RegistryResult.failure(
            ERR_REG_N1_CONTRACT,
            check.message or "N1 contract failed",
            isolation_code=check.code,
            **dict(check.details),
        )
    return RegistryResult.success(row=cleaned)


def assert_workspace_access(
    *,
    bound_workspace_id: str,
    target_workspace_id: str,
    action: str = "read",
    target_path: str = "",
) -> RegistryResult:
    """Service-level WS-003 wrapper: refuse cross-workspace access."""
    r = validate_cross_workspace_access(
        AccessRequest(
            bound_workspace_id=bound_workspace_id,
            target_workspace_id=target_workspace_id,
            target_path=target_path,
            action=action,
        )
    )
    if not r.ok:
        details = dict(r.details)
        details.setdefault("leaked_body", False)
        details["isolation_code"] = r.code
        return RegistryResult.failure(
            ERR_REG_CROSS_WORKSPACE,
            r.message or "cross-workspace access denied",
            **details,
        )
    return RegistryResult.success()


def _read_frontmatter(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        post = frontmatter.loads(path.read_text(encoding="utf-8"))
        return dict(post.metadata or {})
    except Exception:
        return {}


def _disk_root_goal_ids(workspace_root: Path) -> tuple[str, ...]:
    roots: list[str] = []
    if not workspace_root.is_dir():
        return ()
    for child in sorted(workspace_root.iterdir()):
        if not child.is_dir() or not _GOAL_DIR_RE.match(child.name):
            continue
        meta = _read_frontmatter(child / "00-meta.md")
        parent = meta.get("parent")
        goal_id = str(meta.get("id") or child.name)
        if parent is None or parent == "null" or parent == "":
            roots.append(goal_id)
    return tuple(roots)


def _load_workspace_md(workspace_root: Path) -> dict[str, Any]:
    return _read_frontmatter(workspace_root / "workspace.md")


def _validate_disk_workspace(
    workspace_root: Path,
    *,
    declared_status: str | None = None,
    other_roots: tuple[str, ...] = (),
) -> DiscoveredWorkspace:
    """Load workspace.md + disk Root; apply WS-001/002."""
    path = workspace_root.resolve()
    meta = _load_workspace_md(path)
    if not meta:
        return DiscoveredWorkspace(
            workspace_id=path.name,
            display_name=path.name,
            root_goal="",
            status="active",
            path=path,
            valid=False,
            error="missing or unreadable workspace.md",
            validation_code=ERR_REG_INVALID,
        )

    ws_id = str(meta.get("id") or path.name).strip()
    display = str(meta.get("title") or ws_id).strip()
    root_goal = str(meta.get("root_goal") or "").strip()
    # Prefer registry/nav status override; else workspace.md status if active|archived.
    md_status = str(meta.get("status") or "active").strip().lower()
    if declared_status in {"active", "archived"}:
        status = declared_status
    elif md_status in {"active", "archived"}:
        status = md_status
    else:
        status = "active"

    # canonical_scope in md may be relative "."; bind to actual path for checks.
    scope_raw = str(meta.get("canonical_scope") or ".").strip()
    if scope_raw in {".", "./", ""}:
        scope_for_check = str(path)
    else:
        scope_path = Path(scope_raw)
        if not scope_path.is_absolute():
            scope_path = (path / scope_path).resolve()
        else:
            scope_path = scope_path.resolve()
        scope_for_check = str(scope_path)

    disk = DiskRootFact(
        root_goal_ids=_disk_root_goal_ids(path),
        actual_root_path=str(path),
    )
    binding = WorkspaceBinding(
        workspace_id=ws_id,
        root_goal=root_goal,
        canonical_scope=scope_for_check,
        workspace_root=path,
    )
    rg = validate_root_goal_binding(binding, disk)
    if not rg.ok:
        return DiscoveredWorkspace(
            workspace_id=ws_id,
            display_name=display,
            root_goal=root_goal,
            status=status,
            path=path,
            valid=False,
            error=rg.message,
            validation_code=rg.code,
        )
    sc = validate_canonical_scope(binding, disk, other_workspace_roots=other_roots)
    if not sc.ok:
        return DiscoveredWorkspace(
            workspace_id=ws_id,
            display_name=display,
            root_goal=root_goal,
            status=status,
            path=path,
            valid=False,
            error=sc.message,
            validation_code=sc.code,
        )
    return DiscoveredWorkspace(
        workspace_id=ws_id,
        display_name=display,
        root_goal=root_goal,
        status=status,
        path=path,
        valid=True,
        error=None,
        validation_code=None,
    )


def _default_registry() -> dict[str, Any]:
    return {"schema": REGISTRY_SCHEMA, "version": 1, "workspaces": []}


class WorkspaceRegistryService:
    """Discover / register / list N1 workspaces under a product data root."""

    def __init__(self, data_root: Path) -> None:
        self.data_root = data_root.resolve()
        self.registry_path = self.data_root / REGISTRY_RELATIVE

    def ensure_data_root(self) -> RegistryResult:
        if not self.data_root.is_dir():
            return RegistryResult.failure(
                ERR_REG_NO_DATA_ROOT,
                f"data root does not exist: {self.data_root}",
            )
        return RegistryResult.success(data_root=str(self.data_root))

    def load_registry_file(self) -> dict[str, Any]:
        if not self.registry_path.is_file():
            return _default_registry()
        try:
            raw = json.loads(self.registry_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return _default_registry()
        if not isinstance(raw, dict):
            return _default_registry()
        workspaces = raw.get("workspaces")
        if not isinstance(workspaces, list):
            raw = _default_registry()
        else:
            raw.setdefault("schema", REGISTRY_SCHEMA)
            raw.setdefault("version", 1)
        return raw

    def save_registry_file(self, data: dict[str, Any]) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema": REGISTRY_SCHEMA,
            "version": int(data.get("version") or 1),
            "workspaces": list(data.get("workspaces") or []),
        }
        tmp = self.registry_path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        tmp.replace(self.registry_path)

    def _candidate_paths(self) -> list[tuple[Path, str | None]]:
        """Return (path, registry_status_override) without scanning monorepo git root."""
        found: dict[str, tuple[Path, str | None]] = {}
        reg = self.load_registry_file()
        for entry in reg.get("workspaces") or []:
            if not isinstance(entry, dict):
                continue
            rel = str(entry.get("path") or "").strip()
            if not rel:
                continue
            p = Path(rel)
            if not p.is_absolute():
                p = (self.data_root / p).resolve()
            else:
                p = p.resolve()
            # Refuse paths outside data_root (path escape).
            try:
                p.relative_to(self.data_root)
            except ValueError:
                continue
            st = entry.get("status")
            status = st if st in {"active", "archived"} else None
            found[str(p)] = (p, status)

        if self.data_root.is_dir():
            if (self.data_root / "workspace.md").is_file() and (
                self.data_root / "goal-tree.md"
            ).is_file():
                key = str(self.data_root.resolve())
                if key not in found:
                    found[key] = (self.data_root.resolve(), None)
            for child in sorted(self.data_root.iterdir()):
                if not child.is_dir():
                    continue
                if not (
                    child.name.startswith("workspace-")
                    or (child / "workspace.md").is_file()
                ):
                    continue
                if not (child / "workspace.md").is_file():
                    continue
                key = str(child.resolve())
                if key not in found:
                    found[key] = (child.resolve(), None)

        return list(found.values())

    def discover(self, *, include_invalid: bool = False) -> list[DiscoveredWorkspace]:
        check = self.ensure_data_root()
        if not check.ok:
            return []

        candidates = self._candidate_paths()
        # First pass paths for other_roots scope checks
        all_paths = tuple(str(p.resolve()) for p, _ in candidates)
        results: list[DiscoveredWorkspace] = []
        for path, status_override in candidates:
            others = tuple(x for x in all_paths if x != str(path.resolve()))
            disc = _validate_disk_workspace(
                path,
                declared_status=status_override,
                other_roots=others,
            )
            if disc.valid or include_invalid:
                results.append(disc)
        # Stable sort: active first, then id
        results.sort(key=lambda d: (0 if d.status == "active" else 1, d.workspace_id))
        return results

    def list_n1(
        self,
        *,
        include_archived: bool = False,
        include_invalid: bool = False,
    ) -> RegistryResult:
        """List workspaces as strict N1 rows only."""
        check = self.ensure_data_root()
        if not check.ok:
            return check

        rows: list[dict[str, str]] = []
        invalid: list[dict[str, str]] = []
        for disc in self.discover(include_invalid=True):
            if not disc.valid:
                invalid.append(
                    {
                        "workspace_id": disc.workspace_id,
                        "error": disc.error or "invalid",
                        "code": disc.validation_code or ERR_REG_INVALID,
                    }
                )
                if include_invalid:
                    continue
                continue
            if disc.status == "archived" and not include_archived:
                continue
            n1 = disc.to_n1_dict()
            vr = n1_public_row(n1)
            if not vr.ok:
                invalid.append(
                    {
                        "workspace_id": disc.workspace_id,
                        "error": vr.message or "n1",
                        "code": vr.code or ERR_REG_N1_CONTRACT,
                    }
                )
                continue
            rows.append(vr.details["row"])  # type: ignore[index]

        # Ensure no forbidden keys leaked
        for row in rows:
            assert set(row.keys()) <= N1_ALLOWED_FIELDS

        return RegistryResult.success(
            workspaces=rows,
            invalid=invalid,
            count=len(rows),
        )

    def get(
        self,
        workspace_id: str,
        *,
        include_archived: bool = True,
    ) -> RegistryResult:
        for disc in self.discover(include_invalid=True):
            if disc.workspace_id != workspace_id:
                continue
            if not disc.valid:
                return RegistryResult.failure(
                    ERR_REG_INVALID,
                    disc.error or "workspace invalid",
                    workspace_id=workspace_id,
                    validation_code=disc.validation_code,
                    path=str(disc.path),
                )
            if disc.status == "archived" and not include_archived:
                return RegistryResult.failure(
                    ERR_REG_NOT_FOUND,
                    "workspace is archived",
                    workspace_id=workspace_id,
                )
            n1 = disc.to_n1_dict()
            vr = n1_public_row(n1)
            if not vr.ok:
                return vr
            return RegistryResult.success(
                workspace=vr.details["row"],
                path=str(disc.path),
                status=disc.status,
            )
        return RegistryResult.failure(
            ERR_REG_NOT_FOUND,
            f"workspace not found: {workspace_id}",
            workspace_id=workspace_id,
        )

    def resolve_path(self, workspace_id: str) -> RegistryResult:
        r = self.get(workspace_id, include_archived=True)
        if not r.ok:
            return r
        return RegistryResult.success(
            workspace_id=workspace_id,
            path=r.details["path"],
        )

    def register_existing(self, workspace_path: Path, *, status: str = "active") -> RegistryResult:
        """Add or update a path under data_root in the registry index."""
        check = self.ensure_data_root()
        if not check.ok:
            return check
        path = workspace_path.resolve()
        try:
            rel = path.relative_to(self.data_root)
        except ValueError:
            return RegistryResult.failure(
                ERR_REG_INVALID,
                "workspace path must be under data_root",
                path=str(path),
                data_root=str(self.data_root),
            )
        if status not in {"active", "archived"}:
            return RegistryResult.failure(ERR_REG_INVALID, "status must be active|archived")

        disc = _validate_disk_workspace(path, declared_status=status)
        if not disc.valid:
            return RegistryResult.failure(
                ERR_REG_INVALID,
                disc.error or "invalid workspace",
                validation_code=disc.validation_code,
            )

        reg = self.load_registry_file()
        entries: list[dict[str, Any]] = list(reg.get("workspaces") or [])
        rel_s = rel.as_posix()
        updated = False
        for e in entries:
            if not isinstance(e, dict):
                continue
            ep = str(e.get("path") or "")
            if ep == rel_s or e.get("workspace_id") == disc.workspace_id:
                e["workspace_id"] = disc.workspace_id
                e["path"] = rel_s
                e["status"] = status
                updated = True
                break
        if not updated:
            # conflict id different path?
            for e in entries:
                if isinstance(e, dict) and e.get("workspace_id") == disc.workspace_id:
                    return RegistryResult.failure(
                        ERR_REG_ID_CONFLICT,
                        "workspace_id already registered to another path",
                        workspace_id=disc.workspace_id,
                    )
            entries.append(
                {
                    "workspace_id": disc.workspace_id,
                    "path": rel_s,
                    "status": status,
                }
            )
        reg["workspaces"] = entries
        self.save_registry_file(reg)
        return RegistryResult.success(
            workspace_id=disc.workspace_id,
            path=str(path),
            status=status,
        )

    def set_status(self, workspace_id: str, status: str) -> RegistryResult:
        """Archive / unarchive via registry (does not delete canonical)."""
        if status not in {"active", "archived"}:
            return RegistryResult.failure(ERR_REG_INVALID, "status must be active|archived")
        got = self.get(workspace_id, include_archived=True)
        if not got.ok:
            return got
        path = Path(str(got.details["path"]))
        return self.register_existing(path, status=status)

    def create_workspace(
        self,
        *,
        workspace_id: str,
        title: str | None = None,
        root_goal_slug: str = "root",
        root_goal_title: str = "Root Goal",
    ) -> RegistryResult:
        """Bounded create: directory + workspace.md + Root skeleton + goal-tree."""
        check = self.ensure_data_root()
        if not check.ok:
            return check

        raw_id = workspace_id.strip()
        if _WS_ID_RE.match(raw_id):
            ws_id = raw_id
        elif _SLUG_RE.match(raw_id):
            # Assign next number under data_root
            n = 1
            for child in self.data_root.iterdir() if self.data_root.is_dir() else []:
                m = re.match(r"workspace-(\d+)-", child.name)
                if m:
                    n = max(n, int(m.group(1)) + 1)
            ws_id = f"workspace-{n:03d}-{raw_id}"
        else:
            return RegistryResult.failure(
                ERR_REG_CREATE_FAILED,
                "workspace_id must be workspace-NNN-slug or lowercase-slug",
                workspace_id=raw_id,
            )

        existing = self.get(ws_id, include_archived=True)
        if existing.ok:
            return RegistryResult.failure(
                ERR_REG_ID_CONFLICT,
                "workspace_id already exists",
                workspace_id=ws_id,
            )

        target = (self.data_root / ws_id).resolve()
        try:
            target.relative_to(self.data_root)
        except ValueError:
            return RegistryResult.failure(ERR_REG_CREATE_FAILED, "path escape")

        if target.exists():
            return RegistryResult.failure(
                ERR_REG_CREATE_FAILED,
                "target directory already exists",
                path=str(target),
            )

        if not _SLUG_RE.match(root_goal_slug):
            return RegistryResult.failure(
                ERR_REG_CREATE_FAILED,
                "root_goal_slug must be lowercase-hyphen slug",
            )
        root_goal_id = f"GOAL-001-{root_goal_slug}"
        display = (title or ws_id).strip()
        today = __import__("datetime").date.today().isoformat()

        goal_dir = target / root_goal_id
        try:
            goal_dir.mkdir(parents=True)
            (goal_dir / "attachments").mkdir()
            (goal_dir / "00-meta.md").write_text(
                f"""---
id: {root_goal_id}
title: {display if display == root_goal_title else root_goal_title}
status: active
parent: null
created: {today}
updated: {today}
version: 0.1.0
progress: 0%
---

# {root_goal_id} · {root_goal_title}

## 概述

新建工作区 Root Goal（有界骨架）。
""",
                encoding="utf-8",
            )
            for name, doc in (
                ("01-decision.md", "decision"),
                ("02-execution.md", "execution"),
                ("03-audit.md", "audit"),
            ):
                (goal_dir / name).write_text(
                    f"""---
id: {root_goal_id}
doc: {doc}
status: active
parent: null
created: {today}
updated: {today}
version: 0.1.0
---

# {doc} · {root_goal_id}
""",
                    encoding="utf-8",
                )

            (target / "workspace.md").write_text(
                f"""---
id: {ws_id}
title: {display}
status: active
root_goal: {root_goal_id}
canonical_scope: .
created: {today}
updated: {today}
version: 0.1.0
---

# 工作区 · {display}

产品工作区骨架（GOAL-015 有界创建）。
""",
                encoding="utf-8",
            )
            (target / "goal-tree.md").write_text(
                f"""---
title: Goal Tree
status: active
created: {today}
updated: {today}
version: 0.1.0
---

# Goal Tree

```text
{root_goal_id} · {root_goal_title} [active]
```

| ID | 标题 | Parent | Status | Progress |
|----|------|--------|--------|----------|
| {root_goal_id} | {root_goal_title} | — | active | 0% |
""",
                encoding="utf-8",
            )
        except OSError as exc:
            return RegistryResult.failure(
                ERR_REG_CREATE_FAILED,
                f"failed to write skeleton: {exc}",
                path=str(target),
            )

        reg = self.register_existing(target, status="active")
        if not reg.ok:
            return reg
        return RegistryResult.success(
            workspace_id=ws_id,
            path=str(target),
            root_goal=root_goal_id,
            n1={
                "workspace_id": ws_id,
                "display_name": display,
                "root_goal": root_goal_id,
                "status": "active",
            },
        )
