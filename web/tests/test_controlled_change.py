from __future__ import annotations

import json
import shutil
import tempfile
import threading
import unittest
from pathlib import Path

from services.controlled_change import (
    ControlledChangeError,
    ControlledChangeService,
    compose_appended_execution,
    digest_text,
    file_digest,
    normalize_text,
)
from services.goals_repo import GoalsRepository


FIXTURE_SRC = Path(__file__).parent / "fixtures" / "r004" / "workspace-ok"
GOAL_ID = "GOAL-001-fixture-target"


class ControlledChangeTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "workspace-ok"
        shutil.copytree(FIXTURE_SRC, self.root)
        self.repo = GoalsRepository(self.root)
        self.svc = ControlledChangeService(
            repository=self.repo,
            workspace_id="workspace-ok-fixture",
            test_authorized=True,
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_normalize_and_digest_crlf(self) -> None:
        body = "line1\r\nline2\r\n"
        self.assertEqual(normalize_text(body), "line1\nline2\n")
        self.assertEqual(digest_text(body), digest_text("line1\nline2\n"))

    def test_proposal_preview_body_matches_committed_write(self) -> None:
        """Diff/preview composition must equal bytes written on affirm (shared helper)."""
        exec_path = self.root / GOAL_ID / "02-execution.md"
        # Ensure file already ends with LF (common case that previously diverged).
        text = exec_path.read_text(encoding="utf-8")
        if not text.endswith("\n"):
            exec_path.write_text(text + "\n", encoding="utf-8")

        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="Preview must match write",
            source_statement="test",
        )
        prop = self.svc.build_proposal(candidate=cand)
        before = exec_path.read_text(encoding="utf-8")
        expected = compose_appended_execution(before, prop.append_block)
        # Unified diff is derived from the same proposed body.
        self.assertIn("Preview must match write", prop.unified_diff)

        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_preview_match_001",
        )
        self.assertEqual(receipt.result, "committed")
        after = exec_path.read_text(encoding="utf-8")
        self.assertEqual(normalize_text(after), normalize_text(expected))
        self.assertEqual(after, expected)

    def test_success_append_only_execution(self) -> None:
        paths = {
            "execution": self.root / GOAL_ID / "02-execution.md",
            "meta": self.root / GOAL_ID / "00-meta.md",
            "tree": self.root / "goal-tree.md",
            "audit": self.root / GOAL_ID / "03-audit.md",
        }
        meta_before = file_digest(paths["meta"])
        tree_before = file_digest(paths["tree"])
        audit_before = paths["audit"].read_text(encoding="utf-8")
        exec_before = paths["execution"].read_text(encoding="utf-8")

        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="Completed fixture append for CT success path.",
            source_statement="test operator",
        )
        prop = self.svc.build_proposal(candidate=cand)
        self.assertEqual(prop.expected_write_set, ("02-execution.md",))
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_success_001",
        )
        self.assertEqual(receipt.result, "committed")
        self.assertIsNone(receipt.error_code)

        exec_after = paths["execution"].read_text(encoding="utf-8")
        self.assertNotEqual(exec_before, exec_after)
        self.assertIn("Completed fixture append", exec_after)
        self.assertEqual(file_digest(paths["meta"]), meta_before)
        self.assertEqual(file_digest(paths["tree"]), tree_before)
        self.assertEqual(paths["audit"].read_text(encoding="utf-8"), audit_before)
        self.assertIn("F-TEST-OPEN", audit_before)
        self.assertIn("open", audit_before.lower())
        # receipt not in five-piece
        self.assertFalse((self.root / GOAL_ID / "ops").exists() or False)
        self.assertTrue((self.root / "ops" / "receipts" / "op_success_001.json").is_file())

    def test_missing_fields(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="x",
                source_statement="",
            )
        self.assertEqual(ctx.exception.code, "ERR_MISSING_FIELD")

    def test_invalid_source_kind_rejected(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="from ai",
                source_statement="model",
                source_kind="not-a-real-kind",
            )
        self.assertEqual(ctx.exception.code, "ERR_INVALID_SOURCE")

    def test_ai_knowledge_source_allowed_with_fa(self) -> None:
        """GOAL-014: confirmed AI kinds may enter prepare after FA (not disguised)."""
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="AI suggested execution note",
            source_statement="model knowledge via test; candidate only",
            source_kind="ai-knowledge",
        )
        self.assertEqual(cand.source_kind, "ai-knowledge")
        self.assertTrue(cand.produced_by_ai)

    def test_invalid_write_set(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="ok",
            source_statement="t",
        )
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.build_proposal(
                candidate=cand,
                expected_write_set=("02-execution.md", "00-meta.md"),
            )
        self.assertEqual(ctx.exception.code, "ERR_INVALID_WRITE_SET")

    def test_baseline_drift(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="will drift",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        exec_path = self.root / GOAL_ID / "02-execution.md"
        exec_path.write_text(exec_path.read_text(encoding="utf-8") + "\n- drift\n", encoding="utf-8")
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_drift_001",
        )
        self.assertEqual(receipt.result, "conflict")
        self.assertEqual(receipt.error_code, "ERR_BASELINE_DRIFT")

    def test_open_finding_append_keeps_finding(self) -> None:
        audit_path = self.root / GOAL_ID / "03-audit.md"
        before = audit_path.read_text(encoding="utf-8")
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="append while finding open",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_open_finding_001",
        )
        self.assertEqual(receipt.result, "committed")
        after = audit_path.read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertIn("F-TEST-OPEN", after)

    def test_split_execute_rejected(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="split",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        before = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_split_001",
            split_execute=True,
        )
        self.assertEqual(receipt.result, "rejected")
        self.assertEqual(receipt.error_code, "ERR_SPLIT_EXECUTE")
        after = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)

    def test_production_gate_blocks_without_authorization(self) -> None:
        gated = ControlledChangeService(
            repository=self.repo,
            workspace_id="workspace-ok-fixture",
            test_authorized=False,
            environ={},  # ALLOW default false → production path blocked
        )
        cand = gated.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="should not write",
            source_statement="t",
        )
        prop = gated.build_proposal(candidate=cand)
        before = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        receipt = gated.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_gate_001",
        )
        self.assertEqual(receipt.result, "rejected")
        self.assertEqual(receipt.error_code, "ERR_PRODUCT_GATE_OPEN")
        after = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)

    def test_idempotent_replay_returns_same_receipt(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="idempotent body",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        r1 = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_idem_001",
        )
        body_after_first = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        r2 = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_idem_001",
        )
        body_after_second = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(r1.result, "committed")
        self.assertEqual(r2.operation_id, r1.operation_id)
        self.assertEqual(body_after_first, body_after_second)
        self.assertEqual(body_after_first.count("idempotent body"), 1)

    def test_durable_idempotent_replay_new_service_instance(self) -> None:
        """CT-007 durable: new ControlledChangeService loads receipt from disk (GOAL-013 B)."""
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="durable idempotent body",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        r1 = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_durable_001",
        )
        self.assertEqual(r1.result, "committed")
        receipt_path = self.root / "ops" / "receipts" / "op_durable_001.json"
        self.assertTrue(receipt_path.is_file())
        body_after_first = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")

        # Fresh service instance: empty memory, no proposal cache (simulates process restart).
        svc2 = ControlledChangeService(
            repository=GoalsRepository(self.root),
            workspace_id="workspace-ok-fixture",
            test_authorized=True,
        )
        r2 = svc2.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_durable_001",
        )
        body_after_second = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(r2.result, "committed")
        self.assertEqual(r2.operation_id, r1.operation_id)
        self.assertEqual(r2.request_digest, r1.request_digest)
        self.assertEqual(body_after_first, body_after_second)
        self.assertEqual(body_after_first.count("durable idempotent body"), 1)
        loaded = svc2.get_receipt("op_durable_001")
        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded.result, "committed")

    def test_operation_id_conflict_different_proposal(self) -> None:
        """CT-008 partial: reusing operation_id with a different proposal_digest rejects."""
        c1 = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="first body",
            source_statement="t",
        )
        p1 = self.svc.build_proposal(candidate=c1)
        r1 = self.svc.decide_and_execute(
            proposal_digest=p1.proposal_digest,
            action="affirm",
            operation_id="op_conflict_001",
        )
        self.assertEqual(r1.result, "committed")
        body_before = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")

        c2 = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="second body different",
            source_statement="t",
        )
        p2 = self.svc.build_proposal(candidate=c2)
        r2 = self.svc.decide_and_execute(
            proposal_digest=p2.proposal_digest,
            action="affirm",
            operation_id="op_conflict_001",
        )
        body_after = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(r2.result, "conflict")
        self.assertEqual(r2.error_code, "ERR_IDEM_CONFLICT")
        self.assertEqual(body_before, body_after)
        self.assertNotIn("second body different", body_after)

    def test_digest_mismatch_caller(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="line\r\nwith crlf",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_digest_001",
            caller_content_digest="sha256:deadbeef",
        )
        self.assertEqual(receipt.result, "rejected")
        self.assertEqual(receipt.error_code, "ERR_DIGEST_MISMATCH")

    # --- GOAL-013 phase C: F-007 CT-001 / 003 / 006 / 012 / 014 / 015 ---

    def test_ct001_missing_goal_and_workspace(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id="",
                content="x",
                source_statement="t",
            )
        self.assertEqual(ctx.exception.code, "ERR_MISSING_FIELD")
        with self.assertRaises(ControlledChangeError) as ctx2:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="x",
                source_statement="t",
                workspace_id="",
            )
        self.assertEqual(ctx2.exception.code, "ERR_MISSING_FIELD")

    def test_ct001_content_digest_mismatch_on_proposal(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="ok body",
            source_statement="t",
        )
        # Tamper candidate content after digest was fixed (simulate CT-001 digest binding).
        from dataclasses import replace

        tampered = replace(cand, content="ok body CHANGED")
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.build_proposal(candidate=tampered)
        self.assertEqual(ctx.exception.code, "ERR_DIGEST_MISMATCH")

    def test_ct003_cross_workspace_rejected(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="cross ws",
                source_statement="t",
                workspace_id="other-workspace-id",
            )
        self.assertEqual(ctx.exception.code, "ERR_SCOPE_MISMATCH")
        self.assertNotIn("other workspace secrets", ctx.exception.message)

    def test_ct003_path_escape_goal_rejected(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id="../outside-goal",
                content="escape",
                source_statement="t",
            )
        self.assertEqual(ctx.exception.code, "ERR_SCOPE_MISMATCH")

    def test_ct006_expired_proposal_rejected(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="will expire",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand, expires_hours=-1)
        before = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_expire_001",
        )
        after = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(receipt.result, "rejected")
        self.assertEqual(receipt.error_code, "ERR_DECISION_EXPIRED")
        self.assertEqual(before, after)

    def test_ct006_reject_and_cancel_do_not_write(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="to reject",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        before = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        r1 = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="reject",
            operation_id="op_reject_001",
        )
        r2 = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="cancel",
            operation_id="op_cancel_001",
        )
        after = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(r1.result, "rejected")
        self.assertEqual(r1.error_code, "ERR_DECISION_INVALID")
        self.assertEqual(r2.result, "rejected")
        self.assertEqual(r2.error_code, "ERR_DECISION_CANCELLED")
        self.assertEqual(before, after)

    def test_ct006_unknown_proposal_digest(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.decide_and_execute(
                proposal_digest="sha256:deadbeef" + "0" * 56,
                action="affirm",
                operation_id="op_bad_prop_001",
            )
        self.assertEqual(ctx.exception.code, "ERR_DECISION_INVALID")

    def test_ct012_content_contract_script_and_path(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content='click <script>alert(1)</script>',
                source_statement="t",
            )
        self.assertEqual(ctx.exception.code, "ERR_CONTENT_CONTRACT")
        with self.assertRaises(ControlledChangeError) as ctx2:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="see ../../secret and 00-meta.md",
                source_statement="t",
            )
        self.assertEqual(ctx2.exception.code, "ERR_CONTENT_CONTRACT")

    def test_ct014_governance_mutation_payload_rejected(self) -> None:
        cases = [
            "status: done",
            "progress: 100%",
            "parent: GOAL-001-fixture-target",
            "id: GOAL-999-hack",
            "mark done and close required",
        ]
        for body in cases:
            with self.subTest(body=body):
                with self.assertRaises(ControlledChangeError) as ctx:
                    self.svc.prepare_candidate_revision(
                        goal_id=GOAL_ID,
                        content=body,
                        source_statement="t",
                    )
                self.assertEqual(ctx.exception.code, "ERR_CONTENT_CONTRACT")

    def test_ct015_external_trust_rejected(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="external attempt",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        before = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_trust_001",
            trust_context={
                "mode": "local-loopback-single-user",
                "external_access": True,
            },
        )
        after = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(receipt.result, "rejected")
        self.assertEqual(receipt.error_code, "ERR_TRUST_CONTEXT")
        self.assertEqual(before, after)

    def test_ct015_unsupported_trust_mode_rejected(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="bad mode",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_trust_002",
            trust_context={"mode": "public-internet", "external_access": False},
        )
        self.assertEqual(receipt.result, "rejected")
        self.assertEqual(receipt.error_code, "ERR_TRUST_CONTEXT")

    # --- GOAL-013 phase D: F-008 CT-008/009/010/011 ---

    def test_ct008_same_op_id_different_action_conflicts(self) -> None:
        """CT-008 full: same operation_id + different request_digest (action) → conflict."""
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="idem request body",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        r1 = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_ct008_full",
        )
        self.assertEqual(r1.result, "committed")
        body = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        r2 = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="reject",
            operation_id="op_ct008_full",
        )
        self.assertEqual(r2.result, "conflict")
        self.assertEqual(r2.error_code, "ERR_IDEM_CONFLICT")
        self.assertEqual(body, (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8"))
        # Committed receipt remains authoritative.
        loaded = self.svc.get_receipt("op_ct008_full")
        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded.result, "committed")

    def test_ct009_concurrent_write_conflict(self) -> None:
        """CT-009: second concurrent decide_and_execute loses non-blocking lock."""
        barrier = threading.Barrier(2)
        results: list[object] = []

        def hold_lock() -> None:
            lock = self.svc._workspace_lock()
            self.assertTrue(lock.acquire(blocking=False))
            try:
                barrier.wait(timeout=2)
                # Hold while other thread attempts decide_and_execute.
                barrier.wait(timeout=2)
            finally:
                lock.release()

        def attempt_write() -> None:
            cand = self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="concurrent body",
                source_statement="t",
            )
            prop = self.svc.build_proposal(candidate=cand)
            barrier.wait(timeout=2)
            receipt = self.svc.decide_and_execute(
                proposal_digest=prop.proposal_digest,
                action="affirm",
                operation_id="op_ct009_001",
            )
            results.append(receipt)
            barrier.wait(timeout=2)

        t1 = threading.Thread(target=hold_lock)
        t2 = threading.Thread(target=attempt_write)
        t1.start()
        t2.start()
        t1.join(timeout=5)
        t2.join(timeout=5)
        self.assertEqual(len(results), 1)
        receipt = results[0]
        self.assertEqual(receipt.result, "conflict")  # type: ignore[attr-defined]
        self.assertEqual(receipt.error_code, "ERR_CONCURRENT_WRITE")  # type: ignore[attr-defined]

    def test_ct010_recovery_pending_blocks_write(self) -> None:
        recovery = self.root / ".goal-write-recovery.json"
        recovery.write_text(json.dumps({"status": "pending"}), encoding="utf-8")
        state = self.svc.get_recovery_state()
        self.assertTrue(state["recovery_pending"])
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="blocked by recovery",
            source_statement="t",
        )
        prop = self.svc.build_proposal(candidate=cand)
        before = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_ct010_001",
        )
        after = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertEqual(receipt.result, "recovery_pending")
        self.assertEqual(receipt.error_code, "ERR_RECOVERY_PENDING")
        self.assertEqual(before, after)

    def test_ct011_unverifiable_receipt_not_success(self) -> None:
        """CT-011: incomplete committed receipt must not surface as success."""
        path = self.root / "ops" / "receipts"
        path.mkdir(parents=True, exist_ok=True)
        bad = {
            "schema": "r004-execution-receipt/v0",
            "operation_id": "op_ct011_bad",
            "workspace_id": "workspace-ok-fixture",
            "goal_id": GOAL_ID,
            "operation_kind": "append-execution-fact",
            "expected_write_set": ["02-execution.md"],
            "proposal_digest": "sha256:abc",
            "decision_digest": None,
            "request_digest": "",
            "pre_write_digest": None,
            "post_write_digest": None,
            "meta_digest_unchanged": None,
            "tree_digest_unchanged": None,
            "result": "committed",
            "error_code": None,
            "recovery_ref": None,
            "trust_context": {"mode": "local-loopback-single-user"},
            "created_at": "2026-07-21T00:00:00Z",
        }
        (path / "op_ct011_bad.json").write_text(json.dumps(bad), encoding="utf-8")
        loaded = self.svc.get_receipt("op_ct011_bad")
        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded.result, "failed")
        self.assertEqual(loaded.error_code, "ERR_RECEIPT_UNVERIFIABLE")

    def test_f026_hot_path_imports_fact_admission_ws_sm(self) -> None:
        """F-026: controlled_change composes FA / WS / SM modules (not test-only)."""
        import services.controlled_change as cc

        src = Path(cc.__file__).read_text(encoding="utf-8")
        self.assertIn("from services.fact_admission import", src)
        self.assertIn("from services.workspace_isolation import", src)
        self.assertIn("from services.shared_materials import", src)
        self.assertIn("_assert_fact_admission", src)
        self.assertIn("_assert_workspace_isolation_access", src)
        self.assertIn("_assert_sm_execution_write_boundary", src)

    def test_f026_fa_disguise_rejected_on_prepare(self) -> None:
        """F-026/FA-003: user-provided + AI signals rejected on prepare hot path."""
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="Looks user-typed but is AI",
                source_statement="claimed user",
                produced_by_ai=True,
            )
        self.assertEqual(ctx.exception.code, "ERR_FA_SOURCE_KIND_DISGUISE")

    def test_f026_ws_isolation_on_cross_workspace_prepare(self) -> None:
        """F-026/WS-003: foreign workspace_id rejected via isolation helper."""
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="cross workspace attempt",
                source_statement="test",
                workspace_id="other-workspace",
            )
        # Binding check may fire first (ERR_SCOPE_MISMATCH) or WS code; both refuse write.
        self.assertIn(ctx.exception.code, {"ERR_SCOPE_MISMATCH", "ERR_WS_CROSS_WORKSPACE_ACCESS"})

    def test_f026_happy_path_still_commits_with_hot_gates(self) -> None:
        cand = self.svc.prepare_candidate_revision(
            goal_id=GOAL_ID,
            content="F-026 hot path still allows honest user-provided",
            source_statement="operator",
        )
        prop = self.svc.build_proposal(candidate=cand)
        receipt = self.svc.decide_and_execute(
            proposal_digest=prop.proposal_digest,
            action="affirm",
            operation_id="op_f026_hot_001",
        )
        self.assertEqual(receipt.result, "committed")
        body = (self.root / GOAL_ID / "02-execution.md").read_text(encoding="utf-8")
        self.assertIn("F-026 hot path still allows honest user-provided", body)


if __name__ == "__main__":
    unittest.main()
