"""AI candidate store + confirm/reject chain (GOAL-014 stage C · R-014-A §7).

Process-local non-canonical store. Confirm runs fact_admission then may build
an R-004 proposal (append-execution-fact) without writing until decide_and_execute.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from services.ai_broker import AiBroker, CompletionRequest, CompletionResult
from services.controlled_change import ControlledChangeService, Proposal
from services.fact_admission import (
    CandidateSnapshot,
    validate_confirm_or_proposal,
)

ERR_AI_CANDIDATE_NOT_FOUND = "ERR_AI_CANDIDATE_NOT_FOUND"
ERR_AI_CANDIDATE_STATE = "ERR_AI_CANDIDATE_STATE"
ERR_AI_FA_REJECTED = "ERR_AI_FA_REJECTED"


@dataclass
class StoredAiCandidate:
    candidate_id: str
    workspace_id: str
    goal_id: str
    content: str
    content_digest: str
    source_kind: str
    source_statement: str
    status: str  # submitted | rejected | withdrawn | proposal_requested
    provider: str | None = None
    model: str | None = None
    revision: int = 1

    def to_public(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "workspace_id": self.workspace_id,
            "goal_id": self.goal_id,
            "content": self.content,
            "content_digest": self.content_digest,
            "source_kind": self.source_kind,
            "source_statement": self.source_statement,
            "status": self.status,
            "provider": self.provider,
            "model": self.model,
            "revision": self.revision,
            "labeled_as_candidate": True,
        }


@dataclass
class AiCandidateService:
    """In-process candidate ledger keyed by candidate_id."""

    broker: AiBroker
    _store: dict[str, StoredAiCandidate] = field(default_factory=dict)

    def suggest(
        self,
        *,
        prompt: str,
        workspace_id: str,
        goal_id: str,
        context_blocks: tuple[str, ...] = (),
    ) -> tuple[StoredAiCandidate | None, CompletionResult]:
        result = self.broker.complete(
            CompletionRequest(
                prompt=prompt,
                workspace_id=workspace_id,
                goal_id=goal_id,
                context_blocks=context_blocks,
            )
        )
        if not result.ok or not result.content or not result.candidate_id:
            return None, result
        stored = StoredAiCandidate(
            candidate_id=result.candidate_id,
            workspace_id=workspace_id,
            goal_id=goal_id,
            content=result.content,
            content_digest=result.content_digest or "",
            source_kind=result.source_kind,
            source_statement=result.source_statement or "AI candidate",
            status="submitted",
            provider=result.provider,
            model=result.model,
        )
        self._store[stored.candidate_id] = stored
        return stored, result

    def get(self, candidate_id: str) -> StoredAiCandidate | None:
        return self._store.get(candidate_id)

    def reject(self, candidate_id: str) -> StoredAiCandidate | None:
        cand = self._store.get(candidate_id)
        if cand is None:
            return None
        if cand.status not in {"submitted", "under_review", "proposal_requested"}:
            return cand
        cand.status = "rejected"
        return cand

    def confirm_for_proposal(
        self,
        *,
        candidate_id: str,
        bound_digest: str,
        change_svc: ControlledChangeService,
    ) -> tuple[StoredAiCandidate | None, Proposal | None, str | None, str | None]:
        """FA gate + build R-004 proposal. Returns (cand, proposal, error_code, error_message)."""
        cand = self._store.get(candidate_id)
        if cand is None:
            return None, None, ERR_AI_CANDIDATE_NOT_FOUND, "unknown candidate_id"
        if cand.status in {"rejected", "withdrawn"}:
            return cand, None, ERR_AI_CANDIDATE_STATE, f"candidate status is {cand.status}"

        snap = CandidateSnapshot(
            candidate_id=cand.candidate_id,
            revision=cand.revision,
            workspace_id=cand.workspace_id,
            goal_id=cand.goal_id,
            source_kind=cand.source_kind,
            source_statement=cand.source_statement,
            content=cand.content,
            content_digest=cand.content_digest,
            status="proposal_requested",
            produced_by_ai=cand.source_kind.startswith("ai-"),
        )
        fa = validate_confirm_or_proposal(snap, bound_digest)
        if not fa.ok:
            return cand, None, fa.code or ERR_AI_FA_REJECTED, fa.message or "fact admission rejected"

        try:
            rev = change_svc.prepare_candidate_revision(
                goal_id=cand.goal_id,
                content=cand.content,
                source_statement=cand.source_statement,
                source_kind=cand.source_kind,
                workspace_id=cand.workspace_id,
                candidate_id=cand.candidate_id,
                produced_by_ai=cand.source_kind.startswith("ai-"),
            )
            proposal = change_svc.build_proposal(candidate=rev)
        except Exception as exc:  # ControlledChangeError
            code = getattr(exc, "code", "ERR_CONTROLLED_CHANGE")
            message = getattr(exc, "message", str(exc))
            return cand, None, code, message

        cand.status = "proposal_requested"
        return cand, proposal, None, None
