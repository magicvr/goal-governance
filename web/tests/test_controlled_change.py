from __future__ import annotations

import json
import shutil
import tempfile
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

    def test_non_user_source_rejected(self) -> None:
        with self.assertRaises(ControlledChangeError) as ctx:
            self.svc.prepare_candidate_revision(
                goal_id=GOAL_ID,
                content="from ai",
                source_statement="model",
                source_kind="ai-retrieval",
            )
        self.assertEqual(ctx.exception.code, "ERR_INVALID_SOURCE")

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
        self.assertEqual(receipt.result, "rejected")
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
            environ={},  # product gates open by default
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


if __name__ == "__main__":
    unittest.main()
