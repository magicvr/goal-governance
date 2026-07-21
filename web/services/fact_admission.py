"""R-002 fact-admission validation (pure functions; no I/O, no AI runtime).

Implements the design freeze in GOAL-009 attachments/r-002-verification-package.md
for FA-001..FA-006. Does not write canonical workspace files.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Iterable, Mapping

SOURCE_KINDS = frozenset(
    {
        "user-provided",
        "ai-retrieval",
        "ai-knowledge",
        "ai-derivation",
        "shared-material",
    }
)
SOURCE_USER = "user-provided"

# Statuses that may attempt confirm / proposal_requested.
ACTIVE_REVIEW_STATUSES = frozenset({"submitted", "under_review", "proposal_requested"})

# Candidate statuses that must never render as canonical fact without a label.
UNCONFIRMED_STATUSES = frozenset(
    {"draft", "submitted", "under_review", "rejected", "withdrawn", "proposal_requested"}
)

ERR_FA_MISSING_SOURCE_KIND = "ERR_FA_MISSING_SOURCE_KIND"
ERR_FA_MISSING_SOURCE_STATEMENT = "ERR_FA_MISSING_SOURCE_STATEMENT"
ERR_FA_SOURCE_KIND_DISGUISE = "ERR_FA_SOURCE_KIND_DISGUISE"
ERR_FA_RENDER_CANONICAL_UNCONFIRMED = "ERR_FA_RENDER_CANONICAL_UNCONFIRMED"
ERR_FA_DIGEST_STALE = "ERR_FA_DIGEST_STALE"
ERR_FA_SOURCE_KIND_MUTATION = "ERR_FA_SOURCE_KIND_MUTATION"
ERR_FA_INVALID_SOURCE_KIND = "ERR_FA_INVALID_SOURCE_KIND"
ERR_FA_MISSING_SCOPE = "ERR_FA_MISSING_SCOPE"


@dataclass(frozen=True)
class FactAdmissionError(Exception):
    code: str
    message: str

    def __str__(self) -> str:  # pragma: no cover - convenience
        return f"{self.code}: {self.message}"


@dataclass(frozen=True)
class CandidateSnapshot:
    """Immutable candidate view for admission checks (not a DB row)."""

    candidate_id: str
    revision: int
    workspace_id: str
    goal_id: str
    source_kind: str | None
    source_statement: str | None
    content: str
    content_digest: str
    status: str
    tool_call_ids: tuple[str, ...] = ()
    retrieval_refs: tuple[str, ...] = ()
    produced_by_ai: bool = False
    derivation_chain: tuple[str, ...] = ()
    material_id: str | None = None
    material_version: str | None = None
    material_sha256: str | None = None

    def with_mutations(self, **kwargs: object) -> CandidateSnapshot:
        data = {
            "candidate_id": self.candidate_id,
            "revision": self.revision,
            "workspace_id": self.workspace_id,
            "goal_id": self.goal_id,
            "source_kind": self.source_kind,
            "source_statement": self.source_statement,
            "content": self.content,
            "content_digest": self.content_digest,
            "status": self.status,
            "tool_call_ids": self.tool_call_ids,
            "retrieval_refs": self.retrieval_refs,
            "produced_by_ai": self.produced_by_ai,
            "derivation_chain": self.derivation_chain,
            "material_id": self.material_id,
            "material_version": self.material_version,
            "material_sha256": self.material_sha256,
        }
        data.update(kwargs)
        return CandidateSnapshot(**data)  # type: ignore[arg-type]


@dataclass(frozen=True)
class RenderItem:
    """View-model row for FA-004 render contract (pure; not HTML)."""

    zone: str  # "canonical_fact" | "candidate_panel" | "computed_view"
    object_kind: str  # "CanonicalFact" | "Candidate" | "ComputedView"
    status: str | None
    labeled_as_candidate: bool = False
    labeled_as_computed: bool = False
    content_preview: str = ""


@dataclass(frozen=True)
class AdmissionResult:
    ok: bool
    code: str | None = None
    message: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)

    @classmethod
    def success(cls, **details: object) -> AdmissionResult:
        return cls(ok=True, details=details)

    @classmethod
    def failure(cls, code: str, message: str, **details: object) -> AdmissionResult:
        return cls(ok=False, code=code, message=message, details=details)


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def digest_text(text: str) -> str:
    normalized = normalize_text(text).encode("utf-8")
    return "sha256:" + hashlib.sha256(normalized).hexdigest()


def compute_content_digest(content: str) -> str:
    return digest_text(content)


def _is_blank(value: str | None) -> bool:
    return value is None or not str(value).strip()


def has_ai_or_tool_origin(cand: CandidateSnapshot) -> bool:
    """True when payload signals AI/tool production (cannot claim user-provided alone)."""
    if cand.produced_by_ai:
        return True
    if cand.tool_call_ids:
        return True
    if cand.retrieval_refs:
        return True
    if cand.derivation_chain:
        return True
    if cand.source_kind in {"ai-retrieval", "ai-knowledge", "ai-derivation"}:
        return True
    return False


def validate_source_kind_present(cand: CandidateSnapshot) -> AdmissionResult:
    """FA-001: missing / empty / null source_kind blocks confirm and proposal."""
    if _is_blank(cand.source_kind):
        return AdmissionResult.failure(
            ERR_FA_MISSING_SOURCE_KIND,
            "source_kind is required for confirm or proposal_requested",
            candidate_id=cand.candidate_id,
            revision=cand.revision,
        )
    if cand.source_kind not in SOURCE_KINDS:
        return AdmissionResult.failure(
            ERR_FA_INVALID_SOURCE_KIND,
            f"source_kind must be one of {sorted(SOURCE_KINDS)}",
            source_kind=cand.source_kind,
        )
    return AdmissionResult.success()


def validate_source_statement_present(cand: CandidateSnapshot) -> AdmissionResult:
    """FA-002: missing / empty source_statement blocks confirm and proposal."""
    if _is_blank(cand.source_statement):
        return AdmissionResult.failure(
            ERR_FA_MISSING_SOURCE_STATEMENT,
            "source_statement is required for confirm or proposal_requested",
            candidate_id=cand.candidate_id,
            revision=cand.revision,
        )
    return AdmissionResult.success()


def validate_no_source_disguise(cand: CandidateSnapshot) -> AdmissionResult:
    """FA-003: AI/retrieval/tool origin must not be labeled user-provided."""
    if cand.source_kind != SOURCE_USER:
        return AdmissionResult.success()
    # user-provided must not carry AI/tool provenance signals (disguise).
    if (
        cand.produced_by_ai
        or cand.tool_call_ids
        or cand.retrieval_refs
        or cand.derivation_chain
    ):
        return AdmissionResult.failure(
            ERR_FA_SOURCE_KIND_DISGUISE,
            "AI/tool/retrieval origin must not be claimed as user-provided",
            source_kind=cand.source_kind,
            produced_by_ai=cand.produced_by_ai,
            tool_call_ids=list(cand.tool_call_ids),
            retrieval_refs=list(cand.retrieval_refs),
        )
    return AdmissionResult.success()


def validate_content_digest_binding(
    cand: CandidateSnapshot,
    bound_digest: str,
    *,
    content_after_source_change: str | None = None,
) -> AdmissionResult:
    """FA-005: confirm/proposal must bind current content_digest; stale digest rejects.

    If content_after_source_change is provided, digest must match that content,
    not a previous revision's digest.
    """
    expected_content = (
        content_after_source_change if content_after_source_change is not None else cand.content
    )
    live = digest_text(expected_content)
    if bound_digest != live:
        return AdmissionResult.failure(
            ERR_FA_DIGEST_STALE,
            "bound content_digest does not match current content; require new revision",
            bound_digest=bound_digest,
            live_digest=live,
            candidate_id=cand.candidate_id,
            revision=cand.revision,
        )
    if cand.content_digest != live and content_after_source_change is None:
        return AdmissionResult.failure(
            ERR_FA_DIGEST_STALE,
            "candidate.content_digest is stale relative to content",
            candidate_digest=cand.content_digest,
            live_digest=live,
        )
    return AdmissionResult.success(content_digest=live)


def validate_source_kind_immutability(
    stored: CandidateSnapshot,
    attempted: CandidateSnapshot,
) -> AdmissionResult:
    """FA-006: source_kind may not change silently at same revision after submit."""
    if stored.revision != attempted.revision:
        return AdmissionResult.success(reason="new_revision_allowed")
    if stored.status in {"draft"}:
        # draft may still be edited at same revision before submit
        return AdmissionResult.success(reason="draft_mutable")
    if stored.source_kind != attempted.source_kind:
        return AdmissionResult.failure(
            ERR_FA_SOURCE_KIND_MUTATION,
            "source_kind cannot change without incrementing revision after submit",
            stored_source_kind=stored.source_kind,
            attempted_source_kind=attempted.source_kind,
            revision=stored.revision,
            status=stored.status,
        )
    return AdmissionResult.success()


def validate_render_contract(items: Iterable[RenderItem]) -> AdmissionResult:
    """FA-004: unconfirmed candidates must not appear in canonical_fact zone unlabeled.

    Pure view-model contract — not a full browser E2E. Residual R-F002-1 covers UI merge.
    """
    for item in items:
        if item.zone != "canonical_fact":
            continue
        if item.object_kind == "Candidate":
            if item.status in UNCONFIRMED_STATUSES and not item.labeled_as_candidate:
                return AdmissionResult.failure(
                    ERR_FA_RENDER_CANONICAL_UNCONFIRMED,
                    "unconfirmed Candidate in canonical_fact zone without candidate label",
                    status=item.status,
                    content_preview=item.content_preview[:80],
                )
        if item.object_kind == "ComputedView" and not item.labeled_as_computed:
            return AdmissionResult.failure(
                ERR_FA_RENDER_CANONICAL_UNCONFIRMED,
                "ComputedView in canonical_fact zone without computed label",
                content_preview=item.content_preview[:80],
            )
    return AdmissionResult.success()


def validate_confirm_or_proposal(cand: CandidateSnapshot, bound_digest: str) -> AdmissionResult:
    """Gate for confirm and proposal_requested (FA-001, FA-002, FA-003, FA-005)."""
    if _is_blank(cand.workspace_id) or _is_blank(cand.goal_id):
        return AdmissionResult.failure(
            ERR_FA_MISSING_SCOPE,
            "workspace_id and goal_id are required",
        )
    for step in (
        validate_source_kind_present,
        validate_source_statement_present,
        validate_no_source_disguise,
    ):
        result = step(cand)
        if not result.ok:
            return result
    return validate_content_digest_binding(cand, bound_digest)


def can_confirm(cand: CandidateSnapshot, bound_digest: str) -> bool:
    return validate_confirm_or_proposal(cand, bound_digest).ok


def can_request_proposal(cand: CandidateSnapshot, bound_digest: str) -> bool:
    return validate_confirm_or_proposal(cand, bound_digest).ok


_ERROR_CODE_RE = re.compile(r"^ERR_FA_[A-Z0-9_]+$")


def is_fa_error_code(code: str | None) -> bool:
    return bool(code and _ERROR_CODE_RE.match(code))
