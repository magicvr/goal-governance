"""R-003 shared-materials validation (SM-001..SM-006 pure / service-layer).

Design freeze: GOAL-009 attachments/r-003-verification-package.md (D-004 semantics).
Does not implement product CRUD storage or AI broker.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Iterable, Mapping

SHA256_HEX_RE = re.compile(r"^[0-9a-fA-F]{64}$")

ERR_SM_INCOMPLETE_REF = "ERR_SM_INCOMPLETE_REF"
ERR_SM_HASH_MISMATCH = "ERR_SM_HASH_MISMATCH"
ERR_SM_WORKSPACE_MISMATCH = "ERR_SM_WORKSPACE_MISMATCH"
ERR_SM_EXECUTE_FORBIDDEN = "ERR_SM_EXECUTE_FORBIDDEN"
ERR_SM_DELETE_WITHOUT_REF_CHECK = "ERR_SM_DELETE_WITHOUT_REF_CHECK"
ERR_SM_GOAL_PATH_VIA_MATERIALS = "ERR_SM_GOAL_PATH_VIA_MATERIALS"


@dataclass(frozen=True)
class MaterialsResult:
    ok: bool
    code: str | None = None
    message: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)
    # SM-004: content treated as data only
    treat_as_data: bool = False
    execute: bool = False
    exfiltrate: bool = False

    @classmethod
    def success(cls, **details: object) -> MaterialsResult:
        return cls(ok=True, details=details)

    @classmethod
    def failure(cls, code: str, message: str, **details: object) -> MaterialsResult:
        return cls(ok=False, code=code, message=message, details=details)


@dataclass(frozen=True)
class MaterialRef:
    """Fixed shared-material reference (workspace-protocol aligned)."""

    reference_id: str
    workspace_id: str
    material_id: str | None
    version: str | None
    sha256: str | None
    purpose: str | None = None
    local_record: str | None = "none"
    status: str = "active"


def _blank(value: str | None) -> bool:
    return value is None or not str(value).strip()


def normalize_sha256(value: str) -> str:
    v = value.strip().lower()
    if v.startswith("sha256:"):
        v = v[7:]
    return v


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_material_ref_complete(ref: MaterialRef) -> MaterialsResult:
    """SM-001: material_id, version, and valid sha256 are required."""
    missing: list[str] = []
    if _blank(ref.material_id):
        missing.append("material_id")
    if _blank(ref.version):
        missing.append("version")
    if _blank(ref.sha256):
        missing.append("sha256")
    elif not SHA256_HEX_RE.match(normalize_sha256(ref.sha256 or "")):
        return MaterialsResult.failure(
            ERR_SM_INCOMPLETE_REF,
            "sha256 must be 64 hex characters",
            sha256=ref.sha256,
        )
    if missing:
        return MaterialsResult.failure(
            ERR_SM_INCOMPLETE_REF,
            "material reference incomplete; cannot use as evidence",
            missing=missing,
            reference_id=ref.reference_id,
        )
    return MaterialsResult.success(reference_id=ref.reference_id)


def validate_material_hash(
    ref: MaterialRef,
    stored_bytes: bytes,
) -> MaterialsResult:
    """SM-002: sha256 must match stored material bytes."""
    complete = validate_material_ref_complete(ref)
    if not complete.ok:
        return complete
    expected = normalize_sha256(ref.sha256 or "")
    live = digest_bytes(stored_bytes)
    if expected != live:
        return MaterialsResult.failure(
            ERR_SM_HASH_MISMATCH,
            "material sha256 does not match stored bytes",
            expected=expected,
            live=live,
            material_id=ref.material_id,
            version=ref.version,
        )
    return MaterialsResult.success(sha256=live)


def validate_material_ref_workspace(
    ref: MaterialRef,
    current_workspace_id: str,
) -> MaterialsResult:
    """SM-003: reference workspace_id must match current workspace."""
    if _blank(ref.workspace_id) or ref.workspace_id != current_workspace_id:
        return MaterialsResult.failure(
            ERR_SM_WORKSPACE_MISMATCH,
            "material reference workspace_id does not match current workspace",
            ref_workspace_id=ref.workspace_id,
            current_workspace_id=current_workspace_id,
        )
    return MaterialsResult.success()


def evaluate_ai_material_use(
    *,
    content: str,
    intent: str,
) -> MaterialsResult:
    """SM-004: material body is data; AI must not execute or exfiltrate as instructions.

    intent: "read_as_data" | "execute_instructions" | "exfiltrate"
    """
    del content  # content may contain injection; we never execute it here
    if intent == "execute_instructions":
        return MaterialsResult(
            ok=False,
            code=ERR_SM_EXECUTE_FORBIDDEN,
            message="shared material must not be executed as instructions",
            treat_as_data=True,
            execute=False,
            exfiltrate=False,
        )
    if intent == "exfiltrate":
        return MaterialsResult(
            ok=False,
            code=ERR_SM_EXECUTE_FORBIDDEN,
            message="shared material must not be auto-exfiltrated",
            treat_as_data=True,
            execute=False,
            exfiltrate=False,
        )
    if intent == "read_as_data":
        return MaterialsResult(
            ok=True,
            treat_as_data=True,
            execute=False,
            exfiltrate=False,
            details={"intent": intent},
        )
    return MaterialsResult.failure(
        ERR_SM_EXECUTE_FORBIDDEN,
        f"unknown AI material intent: {intent}",
    )


def validate_delete_precheck(
    *,
    material_id: str,
    affected_refs: Iterable[MaterialRef],
    ref_check_performed: bool,
    user_confirmed_delete: bool,
) -> MaterialsResult:
    """SM-005: delete requires ref impact check; block if unchecked."""
    refs = list(affected_refs)
    if not ref_check_performed:
        return MaterialsResult.failure(
            ERR_SM_DELETE_WITHOUT_REF_CHECK,
            "delete blocked: affected references were not checked",
            material_id=material_id,
        )
    if refs and not user_confirmed_delete:
        return MaterialsResult.failure(
            ERR_SM_DELETE_WITHOUT_REF_CHECK,
            "delete blocked: affected references require user confirmation",
            material_id=material_id,
            affected_count=len(refs),
            affected_reference_ids=[r.reference_id for r in refs],
        )
    return MaterialsResult.success(
        material_id=material_id,
        affected_count=len(refs),
    )


def validate_materials_api_path(
    *,
    requested_path: str,
    shared_materials_root: str,
    goal_workspace_roots: Iterable[str],
) -> MaterialsResult:
    """SM-006: materials API must not read/write other workspace goal paths."""
    req = Pathish(requested_path)
    sm_root = Pathish(shared_materials_root)
    if req.is_under(sm_root):
        return MaterialsResult.success(path=requested_path)

    for root in goal_workspace_roots:
        if req.is_under(Pathish(root)) or req.contains_goal_segment():
            return MaterialsResult.failure(
                ERR_SM_GOAL_PATH_VIA_MATERIALS,
                "shared-materials API must not access workspace goal paths",
                requested_path=requested_path,
                blocked_root=root,
            )
    # Path outside SM root and not under known goal roots — still reject goal-like segments.
    if req.contains_goal_segment():
        return MaterialsResult.failure(
            ERR_SM_GOAL_PATH_VIA_MATERIALS,
            "shared-materials API must not access GOAL-* paths",
            requested_path=requested_path,
        )
    return MaterialsResult.failure(
        ERR_SM_GOAL_PATH_VIA_MATERIALS,
        "path outside shared materials root",
        requested_path=requested_path,
    )


class Pathish:
    """Minimal path helper without requiring filesystem existence."""

    def __init__(self, raw: str) -> None:
        normalized = raw.replace("\\", "/").rstrip("/")
        parts: list[str] = []
        for p in normalized.split("/"):
            if not p or p == ".":
                continue
            if p == "..":
                if parts:
                    parts.pop()
                continue
            parts.append(p)
        self.parts = parts
        self.raw = "/".join(parts)

    def is_under(self, root: Pathish) -> bool:
        if not root.parts:
            return False
        if len(self.parts) < len(root.parts):
            return False
        return self.parts[: len(root.parts)] == root.parts

    def contains_goal_segment(self) -> bool:
        return any(p.startswith("GOAL-") for p in self.parts)
