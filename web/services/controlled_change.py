"""R-004 first-slice controlled change: append-execution-fact only.

Production decide_and_execute is gated closed while product gates remain open.
Tests may pass test_authorized=True or set GOAL_GOVERNANCE_TEST_WRITE_MODE.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from typing import Any, Mapping
from uuid import uuid4

from services.fact_admission import (
    SOURCE_KINDS as FA_SOURCE_KINDS,
    CandidateSnapshot,
    validate_confirm_or_proposal,
)
from services.goals_repo import GoalsRepository
from services.shared_materials import ERR_SM_GOAL_PATH_VIA_MATERIALS
from services.workspace_config import controlled_write_authorized
from services.workspace_isolation import (
    AccessRequest,
    validate_cross_workspace_access,
)

OPERATION_KIND = "append-execution-fact"
SOURCE_USER = "user-provided"
SCHEMA_RECEIPT = "r004-execution-receipt/v0"
_RECOVERY_RECORD_NAME = ".goal-write-recovery.json"

# Per-workspace write locks for CT-009 (process-local; not a distributed lock).
_WORKSPACE_LOCKS: dict[str, threading.Lock] = {}
_WORKSPACE_LOCKS_GUARD = threading.Lock()

# Content contract (CT-012 / CT-014): reject governance mutation, path escape, script.
_FORBIDDEN_CONTENT = re.compile(
    r"(?is)("
    r"status\s*:\s*(done|cancelled|active|draft|blocked)|"
    r"progress\s*:\s*\d+\s*%|"
    r"parent\s*:\s*\S+|"
    r"\bid\s*:\s*GOAL-\d+|"
    r"</?\s*script|"
    r"javascript:|"
    r"关闭\s*finding|mark\s+done|close\s+required|"
    r"\.\./|\.\.\\|"
    r"00-meta\.md|goal-tree\.md|01-decision\.md|03-audit\.md"
    r")"
)


class ControlledChangeError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def normalize_text(text: str) -> str:
    """UTF-8/LF normalization before digests (CT-017)."""
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def digest_text(text: str) -> str:
    normalized = normalize_text(text).encode("utf-8")
    return "sha256:" + hashlib.sha256(normalized).hexdigest()


def digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def compose_appended_execution(current: str, entry_block: str) -> str:
    """Build full 02-execution.md after appending one timeline entry.

    Used for both proposal unified_diff and decide_and_execute writes so preview
    and committed bytes match. ``entry_block`` is the ``### …`` section body
    without a required leading blank line; this helper inserts separators.
    """
    base = normalize_text(current)
    if not base.endswith("\n"):
        base += "\n"
    entry = entry_block.lstrip("\n")
    # One blank line between prior content and the new ### heading.
    if base.endswith("\n\n"):
        return base + entry
    return base + "\n" + entry


def file_digest(path: Path) -> str:
    raw = path.read_bytes()
    # Normalize line endings for text-like files before hashing.
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return digest_bytes(raw)
    return digest_text(text)


@dataclass(frozen=True)
class CandidateRevision:
    candidate_id: str
    workspace_id: str
    goal_id: str
    source_kind: str
    source_statement: str
    content: str
    content_digest: str
    created_at: str
    # Provenance signals for FA-003 (default empty; α path must not set for user-provided).
    produced_by_ai: bool = False
    tool_call_ids: tuple[str, ...] = ()
    retrieval_refs: tuple[str, ...] = ()
    derivation_chain: tuple[str, ...] = ()


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    candidate_id: str
    candidate_digest: str
    workspace_id: str
    goal_id: str
    operation_kind: str
    expected_write_set: tuple[str, ...]
    unified_diff: str
    baseline_execution_digest: str
    meta_digest: str
    tree_digest: str
    proposal_digest: str
    expires_at: str
    append_block: str


@dataclass
class ExecutionReceipt:
    schema: str
    operation_id: str
    workspace_id: str
    goal_id: str
    operation_kind: str
    expected_write_set: list[str]
    proposal_digest: str
    decision_digest: str | None
    request_digest: str
    pre_write_digest: str | None
    post_write_digest: str | None
    meta_digest_unchanged: str | None
    tree_digest_unchanged: str | None
    result: str
    error_code: str | None
    recovery_ref: str | None
    trust_context: dict[str, Any]
    created_at: str
    receipt_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ControlledChangeService:
    """Service-level pipeline for the first vertical slice."""

    repository: GoalsRepository
    workspace_id: str = "configured-workspace"
    test_authorized: bool = False
    environ: Mapping[str, str] | None = None
    _candidates: dict[str, CandidateRevision] = field(default_factory=dict)
    _proposals: dict[str, Proposal] = field(default_factory=dict)
    _receipts_by_operation: dict[str, ExecutionReceipt] = field(default_factory=dict)

    @property
    def goals_dir(self) -> Path:
        return self.repository.goals_dir

    @property
    def ops_receipts_dir(self) -> Path:
        return self.goals_dir / "ops" / "receipts"

    def prepare_candidate_revision(
        self,
        *,
        goal_id: str,
        content: str,
        source_statement: str,
        source_kind: str = SOURCE_USER,
        workspace_id: str | None = None,
        candidate_id: str | None = None,
        produced_by_ai: bool = False,
        tool_call_ids: tuple[str, ...] = (),
        retrieval_refs: tuple[str, ...] = (),
        derivation_chain: tuple[str, ...] = (),
    ) -> CandidateRevision:
        ws = workspace_id if workspace_id is not None else self.workspace_id
        if not source_statement or not str(source_statement).strip():
            raise ControlledChangeError("ERR_MISSING_FIELD", "source_statement is required")
        if content is None or not str(content).strip():
            raise ControlledChangeError("ERR_MISSING_FIELD", "content is required")
        if not goal_id or not str(goal_id).strip():
            raise ControlledChangeError("ERR_MISSING_FIELD", "goal_id is required")
        if not ws or not str(ws).strip():
            raise ControlledChangeError("ERR_MISSING_FIELD", "workspace_id is required")
        if source_kind not in FA_SOURCE_KINDS:
            raise ControlledChangeError(
                "ERR_INVALID_SOURCE",
                f"source_kind must be one of {sorted(FA_SOURCE_KINDS)}",
            )
        # Honest AI kinds must not look like pure user-provided (FA-003).
        if source_kind.startswith("ai-"):
            produced_by_ai = True
        ws_s = str(ws).strip()
        goal_s = goal_id.strip()
        self._assert_workspace_binding(ws_s)
        self._assert_goal_in_scope(goal_s)
        self._assert_workspace_isolation_access(ws_s, goal_s, action="write")
        self._assert_content_contract(content)
        self._assert_sm_execution_write_boundary(goal_s)

        cid = candidate_id or f"cand_{uuid4().hex[:12]}"
        dig = digest_text(content)
        candidate = CandidateRevision(
            candidate_id=cid,
            workspace_id=ws_s,
            goal_id=goal_s,
            source_kind=source_kind,
            source_statement=source_statement.strip(),
            content=normalize_text(content),
            content_digest=dig,
            created_at=_utc_now(),
            produced_by_ai=produced_by_ai,
            tool_call_ids=tuple(tool_call_ids),
            retrieval_refs=tuple(retrieval_refs),
            derivation_chain=tuple(derivation_chain),
        )
        # F-026: FA admission on hot path (proposal gate).
        self._assert_fact_admission(candidate, status="proposal_requested")
        self._candidates[cid] = candidate
        return candidate

    def build_proposal(
        self,
        *,
        candidate_id: str | None = None,
        candidate: CandidateRevision | None = None,
        expected_write_set: tuple[str, ...] | None = None,
        operation_kind: str = OPERATION_KIND,
        expires_hours: int = 24,
    ) -> Proposal:
        cand = candidate or (self._candidates.get(candidate_id or "") if candidate_id else None)
        if cand is None:
            raise ControlledChangeError("ERR_MISSING_FIELD", "candidate is required")
        if digest_text(cand.content) != cand.content_digest:
            raise ControlledChangeError("ERR_DIGEST_MISMATCH", "candidate content_digest mismatch")

        write_set = expected_write_set if expected_write_set is not None else ("02-execution.md",)
        if operation_kind != OPERATION_KIND:
            raise ControlledChangeError(
                "ERR_INVALID_WRITE_SET",
                f"operation_kind must be {OPERATION_KIND!r}",
            )
        if write_set != ("02-execution.md",):
            raise ControlledChangeError(
                "ERR_INVALID_WRITE_SET",
                "expected_write_set must be exactly ['02-execution.md']",
            )

        self._assert_workspace_binding(cand.workspace_id)
        self._assert_goal_in_scope(cand.goal_id)
        self._assert_workspace_isolation_access(
            cand.workspace_id, cand.goal_id, action="write"
        )
        self._assert_sm_execution_write_boundary(cand.goal_id)
        # F-026: re-check FA at proposal build (digest/source binding).
        self._assert_fact_admission(cand, status="proposal_requested")
        paths = self._goal_paths(cand.goal_id)
        baseline = file_digest(paths["execution"])
        meta_d = file_digest(paths["meta"])
        tree_d = file_digest(paths["tree"])

        today = date.today().isoformat()
        title = "User-confirmed execution fact"
        # Entry body only; compose_appended_execution owns separators for diff+write.
        append_block = (
            f"### {today} · {title}\n\n"
            f"- {cand.content.strip()}\n"
            f"- source: {cand.source_kind} ({cand.source_statement})\n"
            f"- content_digest: {cand.content_digest}\n"
        )
        current = paths["execution"].read_text(encoding="utf-8")
        current_normalized = normalize_text(current)
        proposed = compose_appended_execution(current, append_block)

        unified = _simple_unified_diff(
            paths["execution"].name,
            current_normalized if current_normalized.endswith("\n") else current_normalized + "\n",
            proposed,
        )
        pid = f"prop_{uuid4().hex[:12]}"
        payload = {
            "proposal_id": pid,
            "candidate_id": cand.candidate_id,
            "candidate_digest": cand.content_digest,
            "workspace_id": cand.workspace_id,
            "goal_id": cand.goal_id,
            "operation_kind": operation_kind,
            "expected_write_set": list(write_set),
            "baseline_execution_digest": baseline,
            "meta_digest": meta_d,
            "tree_digest": tree_d,
            "append_block": append_block,
            "unified_diff": unified,
        }
        proposal = Proposal(
            proposal_id=pid,
            candidate_id=cand.candidate_id,
            candidate_digest=cand.content_digest,
            workspace_id=cand.workspace_id,
            goal_id=cand.goal_id,
            operation_kind=operation_kind,
            expected_write_set=write_set,
            unified_diff=unified,
            baseline_execution_digest=baseline,
            meta_digest=meta_d,
            tree_digest=tree_d,
            proposal_digest=digest_text(json.dumps(payload, sort_keys=True, ensure_ascii=False)),
            expires_at=_utc_plus_hours(expires_hours),
            append_block=append_block,
        )
        self._proposals[pid] = proposal
        # Also index by proposal_digest for lookup after rebuild
        self._proposals[proposal.proposal_digest] = proposal
        return proposal

    def decide_and_execute(
        self,
        *,
        proposal_digest: str,
        action: str,
        operation_id: str | None = None,
        trust_context: Mapping[str, Any] | None = None,
        split_execute: bool = False,
        caller_content_digest: str | None = None,
    ) -> ExecutionReceipt:
        """Single request affirm+execute (CT-018). Production path gated."""
        if split_execute:
            return self._reject_receipt(
                operation_id=operation_id or f"op_{uuid4().hex[:12]}",
                proposal_digest=proposal_digest,
                code="ERR_SPLIT_EXECUTE",
                message="affirm and execute must be the same request",
                workspace_id=self.workspace_id,
                goal_id="",
            )

        op_id = operation_id or f"op_{uuid4().hex[:12]}"
        trust = dict(trust_context or {"mode": "local-loopback-single-user", "external_access": False})

        decision_payload = {
            "action": action,
            "proposal_digest": proposal_digest,
            "operation_id": op_id,
            "trust_context": trust,
        }
        decision_digest = digest_text(json.dumps(decision_payload, sort_keys=True, ensure_ascii=False))
        request_digest = digest_text(
            json.dumps(
                {"proposal_digest": proposal_digest, "decision_digest": decision_digest, "operation_id": op_id},
                sort_keys=True,
            )
        )

        # CT-007 / CT-008: durable idempotency vs operation_id reuse with different request.
        prior = self._lookup_prior_receipt(op_id)
        if prior is not None:
            prior = self._normalize_loaded_receipt(prior)
            if prior.result == "committed" and prior.request_digest == request_digest:
                return prior
            if prior.request_digest and prior.request_digest == request_digest:
                return prior
            if prior.request_digest and prior.request_digest != request_digest:
                return self._reject_receipt(
                    operation_id=op_id,
                    proposal_digest=proposal_digest,
                    code="ERR_IDEM_CONFLICT",
                    message="operation_id already bound to a different request_digest",
                    workspace_id=prior.workspace_id or self.workspace_id,
                    goal_id=prior.goal_id or "",
                    decision_digest=decision_digest,
                    request_digest=request_digest,
                    trust=trust,
                    result="conflict",
                )
            # Legacy receipts without request_digest: fall back to proposal_digest equality.
            if prior.proposal_digest and prior.proposal_digest == proposal_digest:
                return prior
            if prior.proposal_digest and prior.proposal_digest != proposal_digest:
                return self._reject_receipt(
                    operation_id=op_id,
                    proposal_digest=proposal_digest,
                    code="ERR_IDEM_CONFLICT",
                    message="operation_id already bound to a different proposal_digest",
                    workspace_id=prior.workspace_id or self.workspace_id,
                    goal_id=prior.goal_id or "",
                    decision_digest=decision_digest,
                    request_digest=request_digest,
                    trust=trust,
                    result="conflict",
                )
            return prior

        proposal = self._proposals.get(proposal_digest)
        if proposal is None:
            # try scan by digest field
            proposal = next(
                (p for p in self._proposals.values() if p.proposal_digest == proposal_digest),
                None,
            )
        if proposal is None:
            raise ControlledChangeError("ERR_DECISION_INVALID", "unknown proposal_digest")

        # CT-003 + F-026: workspace isolation, SM write boundary, FA re-check on affirm path.
        try:
            self._assert_workspace_binding(proposal.workspace_id)
            self._assert_goal_in_scope(proposal.goal_id)
            self._assert_workspace_isolation_access(
                proposal.workspace_id, proposal.goal_id, action="write"
            )
            self._assert_sm_execution_write_boundary(proposal.goal_id)
            cand = self._candidates.get(proposal.candidate_id)
            if cand is not None:
                self._assert_fact_admission(cand, status="proposal_requested")
        except ControlledChangeError as exc:
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal_digest,
                code=exc.code,
                message=exc.message,
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
            )

        # CT-006: expired proposal cannot affirm.
        if _is_expired(proposal.expires_at):
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_DECISION_EXPIRED",
                message=f"proposal expired at {proposal.expires_at}",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
            )

        # CT-015: external access cannot inherit local loopback single-user trust.
        trust_err = _trust_context_error(trust)
        if trust_err is not None:
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_TRUST_CONTEXT",
                message=trust_err,
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
            )

        if action in {"reject", "cancel", "withdraw"}:
            receipt = ExecutionReceipt(
                schema=SCHEMA_RECEIPT,
                operation_id=op_id,
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                operation_kind=proposal.operation_kind,
                expected_write_set=list(proposal.expected_write_set),
                proposal_digest=proposal.proposal_digest,
                decision_digest=decision_digest,
                request_digest=request_digest,
                pre_write_digest=None,
                post_write_digest=None,
                meta_digest_unchanged=None,
                tree_digest_unchanged=None,
                result="rejected",
                error_code="ERR_DECISION_INVALID" if action == "reject" else "ERR_DECISION_CANCELLED",
                recovery_ref=None,
                trust_context=trust,
                created_at=_utc_now(),
            )
            self._store_receipt(receipt)
            return receipt

        if action != "affirm":
            raise ControlledChangeError("ERR_DECISION_INVALID", f"unsupported action: {action}")

        if not controlled_write_authorized(
            test_authorized=self.test_authorized,
            environ=dict(self.environ) if self.environ is not None else None,
        ):
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_PRODUCT_GATE_OPEN",
                message="production controlled write disabled while product gates open",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
            )

        # CT-010: GoalsRepository recovery record blocks controlled writes.
        if self._recovery_pending():
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_RECOVERY_PENDING",
                message="workspace recovery record is pending; controlled writes blocked",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
                result="recovery_pending",
                recovery_ref=str(self.recovery_record_path),
            )

        if caller_content_digest is not None:
            cand = self._candidates.get(proposal.candidate_id)
            if cand is not None and caller_content_digest != cand.content_digest:
                # Recompute from content for CT-017
                if caller_content_digest != digest_text(cand.content):
                    return self._reject_receipt(
                        operation_id=op_id,
                        proposal_digest=proposal.proposal_digest,
                        code="ERR_DIGEST_MISMATCH",
                        message="caller digest is not UTF-8/LF normalized content digest",
                        workspace_id=proposal.workspace_id,
                        goal_id=proposal.goal_id,
                        decision_digest=decision_digest,
                        request_digest=request_digest,
                        trust=trust,
                    )

        # CT-009: process-local non-blocking lock (serializes concurrent decide_and_execute).
        lock = self._workspace_lock()
        if not lock.acquire(blocking=False):
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_CONCURRENT_WRITE",
                message="another controlled write is in progress for this workspace",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
                result="conflict",
            )
        try:
            return self._affirm_under_lock(
                proposal=proposal,
                op_id=op_id,
                action=action,
                trust=trust,
                decision_digest=decision_digest,
                request_digest=request_digest,
                caller_content_digest=caller_content_digest,
            )
        finally:
            lock.release()

    def _affirm_under_lock(
        self,
        *,
        proposal: Proposal,
        op_id: str,
        action: str,
        trust: dict[str, Any],
        decision_digest: str,
        request_digest: str,
        caller_content_digest: str | None,
    ) -> ExecutionReceipt:
        del action, caller_content_digest  # already validated by caller
        paths = self._goal_paths(proposal.goal_id)
        pre = file_digest(paths["execution"])
        meta_now = file_digest(paths["meta"])
        tree_now = file_digest(paths["tree"])

        if pre != proposal.baseline_execution_digest:
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_BASELINE_DRIFT",
                message="execution baseline digest changed before affirm",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
                pre=pre,
                result="conflict",
            )
        if meta_now != proposal.meta_digest or tree_now != proposal.tree_digest:
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_BASELINE_DRIFT",
                message="meta or goal-tree digest changed before affirm",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
                pre=pre,
                result="conflict",
            )

        current_text = paths["execution"].read_text(encoding="utf-8")
        new_body = compose_appended_execution(current_text, proposal.append_block)

        self._atomic_write_text(paths["execution"], new_body)
        post = file_digest(paths["execution"])
        meta_after = file_digest(paths["meta"])
        tree_after = file_digest(paths["tree"])
        if meta_after != meta_now or tree_after != tree_now:
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_GOVERNANCE_MUTATION",
                message="meta or tree changed during append",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
                pre=pre,
            )

        # CT-011: re-read file so post digest is reproducible before claiming success.
        post_recheck = file_digest(paths["execution"])
        if post_recheck != post or not pre or not post:
            return self._reject_receipt(
                operation_id=op_id,
                proposal_digest=proposal.proposal_digest,
                code="ERR_RECEIPT_UNVERIFIABLE",
                message="receipt post_write_digest cannot be re-verified from disk",
                workspace_id=proposal.workspace_id,
                goal_id=proposal.goal_id,
                decision_digest=decision_digest,
                request_digest=request_digest,
                trust=trust,
                pre=pre,
                result="failed",
            )

        receipt = ExecutionReceipt(
            schema=SCHEMA_RECEIPT,
            operation_id=op_id,
            workspace_id=proposal.workspace_id,
            goal_id=proposal.goal_id,
            operation_kind=proposal.operation_kind,
            expected_write_set=list(proposal.expected_write_set),
            proposal_digest=proposal.proposal_digest,
            decision_digest=decision_digest,
            request_digest=request_digest,
            pre_write_digest=pre,
            post_write_digest=post,
            meta_digest_unchanged=meta_after,
            tree_digest_unchanged=tree_after,
            result="committed",
            error_code=None,
            recovery_ref=None,
            trust_context=trust,
            created_at=_utc_now(),
        )
        path = self._persist_receipt(receipt)
        receipt.receipt_path = str(path)
        self._store_receipt(receipt)
        return receipt

    def get_receipt(self, operation_id: str) -> ExecutionReceipt | None:
        prior = self._lookup_prior_receipt(operation_id)
        if prior is None:
            return None
        return self._normalize_loaded_receipt(prior)

    def get_recovery_state(self) -> dict[str, Any]:
        """CT-010: expose whether workspace recovery blocks controlled writes."""
        pending = self._recovery_pending()
        return {
            "workspace_id": self.workspace_id,
            "recovery_pending": pending,
            "recovery_ref": str(self.recovery_record_path) if pending else None,
        }

    def _receipt_file(self, operation_id: str) -> Path:
        return self.ops_receipts_dir / f"{operation_id}.json"

    @property
    def recovery_record_path(self) -> Path:
        return self.goals_dir / _RECOVERY_RECORD_NAME

    def _recovery_pending(self) -> bool:
        return self.recovery_record_path.is_file()

    def _workspace_lock(self) -> threading.Lock:
        key = str(self.goals_dir.resolve())
        with _WORKSPACE_LOCKS_GUARD:
            lock = _WORKSPACE_LOCKS.get(key)
            if lock is None:
                lock = threading.Lock()
                _WORKSPACE_LOCKS[key] = lock
            return lock

    def _lookup_prior_receipt(self, operation_id: str) -> ExecutionReceipt | None:
        """Return prior receipt from memory or durable ops/receipts/{operation_id}.json."""
        cached = self._receipts_by_operation.get(operation_id)
        if cached is not None:
            return cached
        path = self._receipt_file(operation_id)
        if not path.is_file():
            return None
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        try:
            receipt = ExecutionReceipt(
                schema=str(raw.get("schema") or SCHEMA_RECEIPT),
                operation_id=str(raw["operation_id"]),
                workspace_id=str(raw.get("workspace_id") or ""),
                goal_id=str(raw.get("goal_id") or ""),
                operation_kind=str(raw.get("operation_kind") or OPERATION_KIND),
                expected_write_set=list(raw.get("expected_write_set") or ["02-execution.md"]),
                proposal_digest=str(raw.get("proposal_digest") or ""),
                decision_digest=raw.get("decision_digest"),
                request_digest=str(raw.get("request_digest") or ""),
                pre_write_digest=raw.get("pre_write_digest"),
                post_write_digest=raw.get("post_write_digest"),
                meta_digest_unchanged=raw.get("meta_digest_unchanged"),
                tree_digest_unchanged=raw.get("tree_digest_unchanged"),
                result=str(raw.get("result") or "failed"),
                error_code=raw.get("error_code"),
                recovery_ref=raw.get("recovery_ref"),
                trust_context=dict(raw.get("trust_context") or {}),
                created_at=str(raw.get("created_at") or ""),
                receipt_path=str(raw.get("receipt_path") or path),
            )
        except (KeyError, TypeError, ValueError):
            return None
        self._receipts_by_operation[operation_id] = receipt
        return receipt

    def _normalize_loaded_receipt(self, receipt: ExecutionReceipt) -> ExecutionReceipt:
        """CT-011: never surface committed success if digests are not verifiable."""
        if receipt.result != "committed":
            return receipt
        if not receipt.pre_write_digest or not receipt.post_write_digest or not receipt.request_digest:
            receipt.result = "failed"
            receipt.error_code = "ERR_RECEIPT_UNVERIFIABLE"
            return receipt
        # If execution file still exists, post digest must match disk (when path known).
        if receipt.goal_id:
            exec_path = self.goals_dir / receipt.goal_id / "02-execution.md"
            if exec_path.is_file():
                try:
                    if file_digest(exec_path) != receipt.post_write_digest:
                        # File moved on after receipt; still treat original receipt as historical
                        # only if we are not claiming current success for a new write.
                        pass
                except OSError:
                    receipt.result = "failed"
                    receipt.error_code = "ERR_RECEIPT_UNVERIFIABLE"
        return receipt

    def _assert_workspace_binding(self, workspace_id: str) -> None:
        """CT-003: reject cross-workspace binding; do not leak other workspace content."""
        if workspace_id != self.workspace_id:
            raise ControlledChangeError(
                "ERR_SCOPE_MISMATCH",
                "workspace_id does not match the configured service workspace",
            )

    def _assert_workspace_isolation_access(
        self, workspace_id: str, goal_id: str, *, action: str
    ) -> None:
        """F-026 / WS-003: hot-path cross-workspace access check (workspace_isolation)."""
        req = AccessRequest(
            bound_workspace_id=self.workspace_id,
            target_workspace_id=workspace_id,
            target_path=f"{goal_id}/02-execution.md",
            action=action,
        )
        result = validate_cross_workspace_access(req)
        if not result.ok:
            raise ControlledChangeError(
                result.code or "ERR_WS_CROSS_WORKSPACE_ACCESS",
                result.message or "cross-workspace access denied",
            )

    def _assert_sm_execution_write_boundary(self, goal_id: str) -> None:
        """F-026 / SM-006 complement: controlled write targets goal files, never materials root."""
        target = (self.goals_dir / goal_id / "02-execution.md").resolve()
        root = self.goals_dir.resolve()
        if root not in target.parents and target != root:
            raise ControlledChangeError(
                "ERR_SCOPE_MISMATCH",
                "execution write target escapes workspace root",
            )
        # Refuse if target resolves under a sibling shared-materials tree.
        materials_candidates = (
            self.goals_dir.parent / "shared-materials",
            self.goals_dir / "shared-materials",
        )
        for materials_root in materials_candidates:
            try:
                resolved_sm = materials_root.resolve()
            except OSError:
                continue
            try:
                target.relative_to(resolved_sm)
            except ValueError:
                continue
            raise ControlledChangeError(
                ERR_SM_GOAL_PATH_VIA_MATERIALS,
                "controlled execution write must not target shared-materials paths",
            )

    def _assert_fact_admission(
        self, cand: CandidateRevision, *, status: str = "proposal_requested"
    ) -> None:
        """F-026: fact_admission validate_confirm_or_proposal on the write pipeline."""
        snap = CandidateSnapshot(
            candidate_id=cand.candidate_id,
            revision=1,
            workspace_id=cand.workspace_id,
            goal_id=cand.goal_id,
            source_kind=cand.source_kind,
            source_statement=cand.source_statement,
            content=cand.content,
            content_digest=cand.content_digest,
            status=status,
            produced_by_ai=cand.produced_by_ai,
            tool_call_ids=cand.tool_call_ids,
            retrieval_refs=cand.retrieval_refs,
            derivation_chain=cand.derivation_chain,
        )
        result = validate_confirm_or_proposal(snap, cand.content_digest)
        if not result.ok:
            raise ControlledChangeError(
                result.code or "ERR_FA_ADMISSION",
                result.message or "fact admission rejected",
            )

    def _assert_goal_in_scope(self, goal_id: str) -> None:
        # Reject path segments that could escape or address another tree (CT-003).
        if any(part in {".", ".."} for part in Path(goal_id).parts) or "/" in goal_id or "\\" in goal_id:
            raise ControlledChangeError("ERR_SCOPE_MISMATCH", "goal_id path escapes workspace scope")
        goal_dir = self.goals_dir / goal_id
        if not goal_dir.is_dir():
            raise ControlledChangeError("ERR_SCOPE_MISMATCH", f"goal not in workspace: {goal_id}")
        # Path traversal guard
        resolved = goal_dir.resolve()
        root = self.goals_dir.resolve()
        if root not in resolved.parents and resolved != root:
            raise ControlledChangeError("ERR_SCOPE_MISMATCH", "goal path escapes workspace")

    def _goal_paths(self, goal_id: str) -> dict[str, Path]:
        goal_dir = self.goals_dir / goal_id
        return {
            "meta": goal_dir / "00-meta.md",
            "execution": goal_dir / "02-execution.md",
            "audit": goal_dir / "03-audit.md",
            "tree": self.goals_dir / "goal-tree.md",
        }

    def _assert_content_contract(self, content: str) -> None:
        if _FORBIDDEN_CONTENT.search(content):
            raise ControlledChangeError(
                "ERR_CONTENT_CONTRACT",
                "content violates execution-fact contract",
            )
        if "```" in content and "<script" in content.lower():
            raise ControlledChangeError("ERR_CONTENT_CONTRACT", "disallowed markup in content")

    def _store_receipt(self, receipt: ExecutionReceipt) -> None:
        # Never clobber a committed receipt with a later conflict/reject for the same op id.
        existing = self._receipts_by_operation.get(receipt.operation_id)
        if existing is not None and existing.result == "committed" and receipt.result != "committed":
            return
        self._receipts_by_operation[receipt.operation_id] = receipt

    def _persist_receipt(self, receipt: ExecutionReceipt) -> Path:
        """Atomically write receipt JSON under workspace ops/receipts/ (non-canonical)."""
        self.ops_receipts_dir.mkdir(parents=True, exist_ok=True)
        path = self._receipt_file(receipt.operation_id)
        # Ensure path is recorded before serializing so reloads see receipt_path.
        receipt.receipt_path = str(path)
        payload = json.dumps(receipt.to_dict(), indent=2, ensure_ascii=False) + "\n"
        self._atomic_write_text(path, payload)
        return path

    def _atomic_write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = normalize_text(text).encode("utf-8")
        fd, tmp_name = tempfile.mkstemp(
            dir=str(path.parent),
            prefix=f".{path.name}.",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, path)
        finally:
            if os.path.exists(tmp_name):
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass

    def _reject_receipt(
        self,
        *,
        operation_id: str,
        proposal_digest: str,
        code: str,
        message: str,
        workspace_id: str,
        goal_id: str,
        decision_digest: str | None = None,
        request_digest: str | None = None,
        trust: dict[str, Any] | None = None,
        pre: str | None = None,
        result: str = "rejected",
        recovery_ref: str | None = None,
    ) -> ExecutionReceipt:
        receipt = ExecutionReceipt(
            schema=SCHEMA_RECEIPT,
            operation_id=operation_id,
            workspace_id=workspace_id,
            goal_id=goal_id,
            operation_kind=OPERATION_KIND,
            expected_write_set=["02-execution.md"],
            proposal_digest=proposal_digest,
            decision_digest=decision_digest,
            request_digest=request_digest or digest_text(code + message),
            pre_write_digest=pre,
            post_write_digest=None,
            meta_digest_unchanged=None,
            tree_digest_unchanged=None,
            result=result,
            error_code=code,
            recovery_ref=recovery_ref,
            trust_context=trust or {"mode": "local-loopback-single-user"},
            created_at=_utc_now(),
        )
        self._store_receipt(receipt)
        return receipt


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _utc_plus_hours(hours: int) -> str:
    from datetime import timedelta

    when = datetime.now(timezone.utc) + timedelta(hours=hours)
    return when.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _is_expired(expires_at: str) -> bool:
    """Return True when proposal expires_at is at or before now (CT-006)."""
    raw = (expires_at or "").strip()
    if not raw:
        return False
    try:
        if raw.endswith("Z"):
            exp = datetime.fromisoformat(raw[:-1] + "+00:00")
        else:
            exp = datetime.fromisoformat(raw)
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return datetime.now(timezone.utc) >= exp


def _trust_context_error(trust: Mapping[str, Any]) -> str | None:
    """CT-015: external access cannot inherit local loopback single-user trust."""
    mode = trust.get("mode", "local-loopback-single-user")
    external = trust.get("external_access", False)
    if external is True:
        return "external_access cannot use local-loopback single-user trust for first slice"
    if mode not in {"local-loopback-single-user"}:
        return f"unsupported trust mode for first slice: {mode!r}"
    return None


def _simple_unified_diff(name: str, before: str, after: str) -> str:
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    # Minimal diff: show only appended tail lines for readability.
    if after.startswith(before):
        added = after[len(before) :]
        added_lines = added.splitlines()
        body = "\n".join(f"+{line}" for line in added_lines)
        return f"--- a/{name}\n+++ b/{name}\n@@ append @@\n{body}\n"
    return f"--- a/{name}\n+++ b/{name}\n- (baseline replaced)\n+ (see append)\n"
