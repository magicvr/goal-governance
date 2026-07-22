"""Product shared-materials store (GOAL-016 stage B).

Design freeze: GOAL-016 attachments/r-016-a-shared-materials-boundary.md (R-016-A).
Layout under {data_root}/shared-materials/:
  objects/{material_id}/{version}/{sha256[:2]}/blob
  index/materials.json
  refs/{workspace_id}.json
  history/deletes.jsonl

Uses shared_materials.py validators (SM-001..006). No Web UI (stage C).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import re
import uuid
from pathlib import Path
from typing import Any, Mapping

from services.shared_materials import (
    ERR_SM_DELETE_WITHOUT_REF_CHECK,
    ERR_SM_GOAL_PATH_VIA_MATERIALS,
    MaterialRef,
    MaterialsResult,
    digest_bytes,
    normalize_sha256,
    validate_delete_precheck,
    validate_material_hash,
    validate_material_ref_complete,
    validate_material_ref_workspace,
    validate_materials_api_path,
)

ERR_MS_NO_ROOT = "ERR_MS_NO_ROOT"
ERR_MS_NOT_FOUND = "ERR_MS_NOT_FOUND"
ERR_MS_INVALID_ID = "ERR_MS_INVALID_ID"
ERR_MS_CONFLICT = "ERR_MS_CONFLICT"
ERR_MS_IO = "ERR_MS_IO"

_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$")
_VERSION_RE = re.compile(r"^v\d+$")


@dataclass(frozen=True)
class StoreResult:
    ok: bool
    code: str | None = None
    message: str | None = None
    details: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls, **details: Any) -> StoreResult:
        return cls(ok=True, details=details)

    @classmethod
    def failure(cls, code: str, message: str, **details: Any) -> StoreResult:
        return cls(ok=False, code=code, message=message, details=details)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_id(value: str, *, kind: str) -> str | None:
    v = value.strip()
    if not _ID_RE.match(v):
        return None
    if ".." in v or "/" in v or "\\" in v:
        return None
    if kind == "material" and v.startswith("GOAL-"):
        return None
    return v


def _atomic_write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


@dataclass
class MaterialRecord:
    material_id: str
    display_name: str
    created_at: str
    current_version: str | None
    versions: list[dict[str, Any]]  # MaterialVersion dicts
    deleted: bool = False

    def to_public(self) -> dict[str, Any]:
        return {
            "material_id": self.material_id,
            "display_name": self.display_name,
            "created_at": self.created_at,
            "current_version": self.current_version,
            "version_count": len(self.versions),
            "deleted": self.deleted,
        }


class SharedMaterialsStore:
    """Filesystem-backed materials + per-workspace refs under product data_root."""

    def __init__(self, data_root: Path) -> None:
        self.data_root = data_root.resolve()
        self.materials_root = self.data_root / "shared-materials"
        self.objects_root = self.materials_root / "objects"
        self.index_path = self.materials_root / "index" / "materials.json"
        self.refs_dir = self.materials_root / "refs"
        self.history_path = self.materials_root / "history" / "deletes.jsonl"

    def ensure_layout(self) -> StoreResult:
        if not self.data_root.is_dir():
            return StoreResult.failure(ERR_MS_NO_ROOT, f"data_root missing: {self.data_root}")
        try:
            self.objects_root.mkdir(parents=True, exist_ok=True)
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            self.refs_dir.mkdir(parents=True, exist_ok=True)
            self.history_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.index_path.is_file():
                _atomic_write_json(self.index_path, {"schema": "materials-index/v1", "materials": {}})
        except OSError as exc:
            return StoreResult.failure(ERR_MS_IO, str(exc))
        return StoreResult.success(materials_root=str(self.materials_root))

    def _load_index(self) -> dict[str, Any]:
        raw = _read_json(self.index_path, {"schema": "materials-index/v1", "materials": {}})
        if not isinstance(raw, dict):
            return {"schema": "materials-index/v1", "materials": {}}
        mats = raw.get("materials")
        if not isinstance(mats, dict):
            raw["materials"] = {}
        return raw

    def _save_index(self, index: dict[str, Any]) -> None:
        _atomic_write_json(self.index_path, index)

    def _blob_path(self, material_id: str, version: str, sha256: str) -> Path:
        return (
            self.objects_root
            / material_id
            / version
            / sha256[:2]
            / "blob"
        )

    def _next_version(self, record: dict[str, Any] | None) -> str:
        if not record:
            return "v1"
        versions = record.get("versions") or []
        n = 0
        for v in versions:
            ver = str(v.get("version") or "")
            m = re.match(r"^v(\d+)$", ver)
            if m:
                n = max(n, int(m.group(1)))
        return f"v{n + 1}"

    def put_bytes(
        self,
        *,
        data: bytes,
        display_name: str,
        material_id: str | None = None,
    ) -> StoreResult:
        """Create material or append immutable version. Returns metadata (no goal paths)."""
        layout = self.ensure_layout()
        if not layout.ok:
            return layout

        mid = material_id
        if mid is None:
            mid = f"mat-{uuid.uuid4().hex[:12]}"
        mid_s = _safe_id(mid, kind="material")
        if not mid_s:
            return StoreResult.failure(ERR_MS_INVALID_ID, "invalid material_id")

        sha = digest_bytes(data)
        index = self._load_index()
        materials: dict[str, Any] = index["materials"]
        existing = materials.get(mid_s)
        if existing and existing.get("deleted"):
            return StoreResult.failure(
                ERR_MS_CONFLICT,
                "material is deleted; create a new material_id",
                material_id=mid_s,
            )

        version = self._next_version(existing if isinstance(existing, dict) else None)
        blob = self._blob_path(mid_s, version, sha)
        # Refuse path escape
        try:
            blob.resolve().relative_to(self.objects_root.resolve())
        except ValueError:
            return StoreResult.failure(ERR_MS_IO, "blob path escapes objects root")

        if blob.is_file():
            # Same content already stored for this version path — treat as conflict
            return StoreResult.failure(ERR_MS_CONFLICT, "blob already exists for version")

        try:
            blob.parent.mkdir(parents=True, exist_ok=True)
            blob.write_bytes(data)
        except OSError as exc:
            return StoreResult.failure(ERR_MS_IO, f"write blob failed: {exc}")

        # Verify hash after write
        written = blob.read_bytes()
        if digest_bytes(written) != sha:
            return StoreResult.failure(ERR_MS_IO, "post-write sha256 mismatch")

        now = _utc_now()
        ver_rec = {
            "material_id": mid_s,
            "version": version,
            "sha256": sha,
            "byte_size": len(data),
            "storage_path": str(blob.relative_to(self.materials_root)).replace("\\", "/"),
            "created_at": now,
        }
        if not existing:
            materials[mid_s] = {
                "material_id": mid_s,
                "display_name": (display_name or mid_s).strip(),
                "created_at": now,
                "current_version": version,
                "versions": [ver_rec],
                "deleted": False,
            }
        else:
            existing["versions"] = list(existing.get("versions") or []) + [ver_rec]
            existing["current_version"] = version
            if display_name.strip():
                existing["display_name"] = display_name.strip()
            materials[mid_s] = existing

        self._save_index(index)
        return StoreResult.success(
            material_id=mid_s,
            version=version,
            sha256=sha,
            byte_size=len(data),
            display_name=materials[mid_s]["display_name"],
        )

    def list_materials(self, *, include_deleted: bool = False) -> StoreResult:
        layout = self.ensure_layout()
        if not layout.ok:
            return layout
        index = self._load_index()
        rows: list[dict[str, Any]] = []
        for mid, rec in sorted((index.get("materials") or {}).items()):
            if not isinstance(rec, dict):
                continue
            if rec.get("deleted") and not include_deleted:
                continue
            rows.append(
                {
                    "material_id": mid,
                    "display_name": rec.get("display_name") or mid,
                    "created_at": rec.get("created_at"),
                    "current_version": rec.get("current_version"),
                    "version_count": len(rec.get("versions") or []),
                    "deleted": bool(rec.get("deleted")),
                }
            )
        return StoreResult.success(materials=rows, count=len(rows))

    def get_version(
        self,
        material_id: str,
        version: str | None = None,
        *,
        read_bytes: bool = False,
    ) -> StoreResult:
        layout = self.ensure_layout()
        if not layout.ok:
            return layout
        mid = _safe_id(material_id, kind="material")
        if not mid:
            return StoreResult.failure(ERR_MS_INVALID_ID, "invalid material_id")
        index = self._load_index()
        rec = (index.get("materials") or {}).get(mid)
        if not isinstance(rec, dict) or rec.get("deleted"):
            return StoreResult.failure(ERR_MS_NOT_FOUND, "material not found", material_id=mid)
        ver = version or rec.get("current_version")
        if not ver:
            return StoreResult.failure(ERR_MS_NOT_FOUND, "no version", material_id=mid)
        ver_rec = None
        for v in rec.get("versions") or []:
            if str(v.get("version")) == str(ver):
                ver_rec = v
                break
        if not ver_rec:
            return StoreResult.failure(
                ERR_MS_NOT_FOUND,
                "version not found",
                material_id=mid,
                version=ver,
            )
        sha = normalize_sha256(str(ver_rec.get("sha256") or ""))
        blob = self._blob_path(mid, str(ver), sha)
        meta = {
            "material_id": mid,
            "display_name": rec.get("display_name"),
            "version": ver,
            "sha256": sha,
            "byte_size": ver_rec.get("byte_size"),
            "created_at": ver_rec.get("created_at"),
        }
        if not read_bytes:
            return StoreResult.success(**meta, has_blob=blob.is_file())
        if not blob.is_file():
            return StoreResult.failure(ERR_MS_NOT_FOUND, "blob missing", **meta)
        data = blob.read_bytes()
        # SM-002
        ref = MaterialRef(
            reference_id="internal",
            workspace_id="store",
            material_id=mid,
            version=str(ver),
            sha256=sha,
        )
        hr = validate_material_hash(ref, data)
        if not hr.ok:
            return StoreResult.failure(hr.code or ERR_MS_IO, hr.message or "hash mismatch")
        return StoreResult.success(**meta, data=data)

    def _refs_path(self, workspace_id: str) -> Path:
        safe = _safe_id(workspace_id, kind="workspace") or "invalid"
        return self.refs_dir / f"{safe}.json"

    def _load_refs(self, workspace_id: str) -> list[dict[str, Any]]:
        raw = _read_json(self._refs_path(workspace_id), {"schema": "material-refs/v1", "refs": []})
        refs = raw.get("refs") if isinstance(raw, dict) else []
        return list(refs) if isinstance(refs, list) else []

    def _save_refs(self, workspace_id: str, refs: list[dict[str, Any]]) -> None:
        _atomic_write_json(
            self._refs_path(workspace_id),
            {"schema": "material-refs/v1", "workspace_id": workspace_id, "refs": refs},
        )

    def attach_ref(
        self,
        *,
        workspace_id: str,
        material_id: str,
        version: str | None = None,
        purpose: str | None = None,
        reference_id: str | None = None,
    ) -> StoreResult:
        """Attach MaterialRef for workspace; fail closed on incomplete/hash/workspace."""
        layout = self.ensure_layout()
        if not layout.ok:
            return layout
        ws = _safe_id(workspace_id, kind="workspace")
        mid = _safe_id(material_id, kind="material")
        if not ws or not mid:
            return StoreResult.failure(ERR_MS_INVALID_ID, "invalid workspace_id or material_id")

        got = self.get_version(mid, version, read_bytes=True)
        if not got.ok:
            return got
        sha = str(got.details["sha256"])
        ver = str(got.details["version"])
        data = got.details.get("data")
        if not isinstance(data, bytes):
            return StoreResult.failure(ERR_MS_NOT_FOUND, "blob unavailable")

        ref_id = (reference_id or f"ref-{uuid.uuid4().hex[:10]}").strip()
        ref = MaterialRef(
            reference_id=ref_id,
            workspace_id=ws,
            material_id=mid,
            version=ver,
            sha256=sha,
            purpose=purpose or "none",
            local_record="none",
            status="active",
        )
        for check in (
            validate_material_ref_complete(ref),
            validate_material_hash(ref, data),
            validate_material_ref_workspace(ref, ws),
        ):
            if not check.ok:
                return StoreResult.failure(
                    check.code or ERR_MS_INVALID_ID,
                    check.message or "ref validation failed",
                    **dict(check.details),
                )

        refs = self._load_refs(ws)
        # Replace same reference_id if present
        refs = [r for r in refs if str(r.get("reference_id")) != ref_id]
        refs.append(
            {
                "reference_id": ref.reference_id,
                "workspace_id": ref.workspace_id,
                "material_id": ref.material_id,
                "version": ref.version,
                "sha256": normalize_sha256(ref.sha256 or ""),
                "purpose": ref.purpose,
                "local_record": ref.local_record,
                "status": ref.status,
            }
        )
        self._save_refs(ws, refs)
        return StoreResult.success(
            reference_id=ref_id,
            workspace_id=ws,
            material_id=mid,
            version=ver,
            sha256=sha,
        )

    def list_refs(self, workspace_id: str, *, include_withdrawn: bool = False) -> StoreResult:
        layout = self.ensure_layout()
        if not layout.ok:
            return layout
        ws = _safe_id(workspace_id, kind="workspace")
        if not ws:
            return StoreResult.failure(ERR_MS_INVALID_ID, "invalid workspace_id")
        refs = self._load_refs(ws)
        if not include_withdrawn:
            refs = [r for r in refs if str(r.get("status") or "active") == "active"]
        return StoreResult.success(workspace_id=ws, refs=refs, count=len(refs))

    def withdraw_ref(self, workspace_id: str, reference_id: str) -> StoreResult:
        layout = self.ensure_layout()
        if not layout.ok:
            return layout
        ws = _safe_id(workspace_id, kind="workspace")
        if not ws:
            return StoreResult.failure(ERR_MS_INVALID_ID, "invalid workspace_id")
        refs = self._load_refs(ws)
        found = False
        for r in refs:
            if str(r.get("reference_id")) == reference_id:
                r["status"] = "withdrawn"
                found = True
        if not found:
            return StoreResult.failure(ERR_MS_NOT_FOUND, "reference not found")
        self._save_refs(ws, refs)
        return StoreResult.success(reference_id=reference_id, status="withdrawn")

    def find_refs_for_material(self, material_id: str) -> list[MaterialRef]:
        mid = _safe_id(material_id, kind="material")
        if not mid:
            return []
        out: list[MaterialRef] = []
        if not self.refs_dir.is_dir():
            return out
        for path in sorted(self.refs_dir.glob("*.json")):
            raw = _read_json(path, {})
            for r in raw.get("refs") or []:
                if not isinstance(r, dict):
                    continue
                if str(r.get("material_id")) != mid:
                    continue
                if str(r.get("status") or "active") != "active":
                    continue
                out.append(
                    MaterialRef(
                        reference_id=str(r.get("reference_id") or ""),
                        workspace_id=str(r.get("workspace_id") or ""),
                        material_id=str(r.get("material_id") or ""),
                        version=str(r.get("version") or ""),
                        sha256=str(r.get("sha256") or ""),
                        purpose=str(r.get("purpose") or "none"),
                        local_record=str(r.get("local_record") or "none"),
                        status=str(r.get("status") or "active"),
                    )
                )
        return out

    def delete_material(
        self,
        material_id: str,
        *,
        user_confirmed: bool,
        force_skip_ref_check: bool = False,
    ) -> StoreResult:
        """Soft-delete material; SM-005 requires ref check unless force (tests only)."""
        layout = self.ensure_layout()
        if not layout.ok:
            return layout
        mid = _safe_id(material_id, kind="material")
        if not mid:
            return StoreResult.failure(ERR_MS_INVALID_ID, "invalid material_id")

        affected = self.find_refs_for_material(mid)
        if force_skip_ref_check:
            # Explicitly illegal path for tests of SM-005
            pre = validate_delete_precheck(
                material_id=mid,
                affected_refs=affected,
                ref_check_performed=False,
                user_confirmed_delete=user_confirmed,
            )
        else:
            pre = validate_delete_precheck(
                material_id=mid,
                affected_refs=affected,
                ref_check_performed=True,
                user_confirmed_delete=user_confirmed,
            )
        if not pre.ok:
            return StoreResult.failure(
                pre.code or ERR_SM_DELETE_WITHOUT_REF_CHECK,
                pre.message or "delete blocked",
                **dict(pre.details),
            )

        index = self._load_index()
        rec = (index.get("materials") or {}).get(mid)
        if not isinstance(rec, dict):
            return StoreResult.failure(ERR_MS_NOT_FOUND, "material not found", material_id=mid)
        rec["deleted"] = True
        rec["deleted_at"] = _utc_now()
        index["materials"][mid] = rec
        self._save_index(index)

        # History tombstone (keep blobs for traceability in stage B)
        try:
            self.history_path.parent.mkdir(parents=True, exist_ok=True)
            line = json.dumps(
                {
                    "event": "delete",
                    "material_id": mid,
                    "at": rec["deleted_at"],
                    "affected_refs": [r.reference_id for r in affected],
                },
                ensure_ascii=False,
            )
            with self.history_path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError as exc:
            return StoreResult.failure(ERR_MS_IO, f"history write failed: {exc}")

        return StoreResult.success(
            material_id=mid,
            deleted=True,
            affected_count=len(affected),
            blobs_retained=True,
        )

    def assert_materials_path(
        self,
        requested_path: str,
        *,
        goal_workspace_roots: list[str] | None = None,
    ) -> StoreResult:
        """SM-006 wrapper for product API path checks."""
        roots = goal_workspace_roots or []
        # Always include data_root workspace children as known goal roots if present
        if self.data_root.is_dir():
            for child in self.data_root.iterdir():
                if child.is_dir() and (
                    child.name.startswith("workspace-") or (child / "goal-tree.md").is_file()
                ):
                    roots.append(str(child.resolve()))
        r = validate_materials_api_path(
            requested_path=requested_path,
            shared_materials_root=str(self.materials_root.resolve()),
            goal_workspace_roots=roots,
        )
        if not r.ok:
            return StoreResult.failure(
                r.code or ERR_SM_GOAL_PATH_VIA_MATERIALS,
                r.message or "path rejected",
                **dict(r.details),
            )
        return StoreResult.success(path=requested_path)
