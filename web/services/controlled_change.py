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
from typing import Any, Mapping
from uuid import uuid4

from services.goals_repo import GoalsRepository
from services.workspace_config import controlled_write_authorized

OPERATION_KIND = "append-execution-fact"
SOURCE_USER = "user-provided"
SCHEMA_RECEIPT = "r004-execution-receipt/v0"

# Content contract: reject governance-mutation and script-ish payloads.
_FORBIDDEN_CONTENT = re.compile(
    r"(?is)(status\s*:\s*done|progress\s*:\s*100%|"
    r"</?\s*script|javascript:|"
    r"关闭\s*finding|mark\s+done|close\s+required)",
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
    ) -> CandidateRevision:
        ws = workspace_id or self.workspace_id
        if not source_statement or not str(source_statement).strip():
            raise ControlledChangeError("ERR_MISSING_FIELD", "source_statement is required")
        if content is None or not str(content).strip():
            raise ControlledChangeError("ERR_MISSING_FIELD", "content is required")
        if not goal_id or not str(goal_id).strip():
            raise ControlledChangeError("ERR_MISSING_FIELD", "goal_id is required")
        if source_kind != SOURCE_USER:
            raise ControlledChangeError(
                "ERR_INVALID_SOURCE",
                f"source_kind must be {SOURCE_USER!r} for first slice",
            )
        self._assert_goal_in_scope(goal_id)
        self._assert_content_contract(content)

        cid = candidate_id or f"cand_{uuid4().hex[:12]}"
        dig = digest_text(content)
        candidate = CandidateRevision(
            candidate_id=cid,
            workspace_id=ws,
            goal_id=goal_id,
            source_kind=source_kind,
            source_statement=source_statement.strip(),
            content=normalize_text(content),
            content_digest=dig,
            created_at=_utc_now(),
        )
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

        self._assert_goal_in_scope(cand.goal_id)
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

        # Idempotent replay
        prior = self._receipts_by_operation.get(op_id)
        if prior is not None:
            # Same operation id: require same request digest semantics via stored receipt
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

        if action in {"reject", "cancel"}:
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
                error_code="ERR_DECISION_INVALID" if action == "reject" else None,
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
            )

        current_text = paths["execution"].read_text(encoding="utf-8")
        new_body = compose_appended_execution(current_text, proposal.append_block)

        self._atomic_write_text(paths["execution"], new_body)
        post = file_digest(paths["execution"])
        meta_after = file_digest(paths["meta"])
        tree_after = file_digest(paths["tree"])
        if meta_after != meta_now or tree_after != tree_now:
            # Should not happen for single-file write; report failed if it did.
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
        return self._receipts_by_operation.get(operation_id)

    def _assert_goal_in_scope(self, goal_id: str) -> None:
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
        self._receipts_by_operation[receipt.operation_id] = receipt

    def _persist_receipt(self, receipt: ExecutionReceipt) -> Path:
        self.ops_receipts_dir.mkdir(parents=True, exist_ok=True)
        path = self.ops_receipts_dir / f"{receipt.operation_id}.json"
        path.write_text(
            json.dumps(receipt.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
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
            result="rejected",
            error_code=code,
            recovery_ref=None,
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
