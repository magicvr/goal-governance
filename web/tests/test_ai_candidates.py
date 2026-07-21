"""GOAL-014 stage C: AI candidate confirm/reject + FA gate."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from services.ai_broker import AiBroker, FakeTransport
from services.ai_candidates import (
    ERR_AI_CANDIDATE_NOT_FOUND,
    ERR_AI_FA_REJECTED,
    AiCandidateService,
)
from services.ai_config import resolve_ai_config
from services.controlled_change import ControlledChangeService
from services.goals_repo import GoalsRepository

FIXTURE = Path(__file__).parent / "fixtures" / "r004" / "workspace-ok"
GOAL_ID = "GOAL-001-fixture-target"


def _ready_env() -> dict[str, str]:
    return {
        "GOAL_GOVERNANCE_AI_ENABLED": "true",
        "GOAL_GOVERNANCE_AI_PROVIDER": "openai-compatible",
        "GOAL_GOVERNANCE_AI_BASE_URL": "https://api.example.com/v1",
        "GOAL_GOVERNANCE_AI_API_KEY": "sk-test",
        "GOAL_GOVERNANCE_AI_MODEL": "gpt-test",
    }


class AiCandidateServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "ws"
        shutil.copytree(FIXTURE, self.root)
        self.repo = GoalsRepository(self.root)
        self.change = ControlledChangeService(
            repository=self.repo,
            workspace_id=self.root.name,
            test_authorized=True,
        )
        self.broker = AiBroker(
            config=resolve_ai_config(_ready_env()),
            transport=FakeTransport("AI drafted execution fact line."),
        )
        self.svc = AiCandidateService(broker=self.broker)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_suggest_stores_candidate(self) -> None:
        stored, result = self.svc.suggest(
            prompt="Suggest a fact",
            workspace_id=self.root.name,
            goal_id=GOAL_ID,
        )
        self.assertTrue(result.ok)
        self.assertIsNotNone(stored)
        assert stored is not None
        self.assertEqual(stored.source_kind, "ai-knowledge")
        self.assertEqual(stored.status, "submitted")
        self.assertIs(self.svc.get(stored.candidate_id), stored)

    def test_reject_marks_status(self) -> None:
        stored, _ = self.svc.suggest(
            prompt="x", workspace_id=self.root.name, goal_id=GOAL_ID
        )
        assert stored is not None
        out = self.svc.reject(stored.candidate_id)
        assert out is not None
        self.assertEqual(out.status, "rejected")

    def test_confirm_builds_proposal_via_fa(self) -> None:
        stored, _ = self.svc.suggest(
            prompt="x", workspace_id=self.root.name, goal_id=GOAL_ID
        )
        assert stored is not None
        cand, prop, err, msg = self.svc.confirm_for_proposal(
            candidate_id=stored.candidate_id,
            bound_digest=stored.content_digest,
            change_svc=self.change,
        )
        self.assertIsNone(err, msg)
        self.assertIsNotNone(prop)
        assert prop is not None
        self.assertEqual(cand.status if cand else None, "proposal_requested")
        self.assertIn("ai-knowledge", prop.append_block)

    def test_confirm_stale_digest_fails_fa(self) -> None:
        stored, _ = self.svc.suggest(
            prompt="x", workspace_id=self.root.name, goal_id=GOAL_ID
        )
        assert stored is not None
        _, prop, err, _ = self.svc.confirm_for_proposal(
            candidate_id=stored.candidate_id,
            bound_digest="sha256:deadbeef",
            change_svc=self.change,
        )
        self.assertIsNone(prop)
        self.assertEqual(err, "ERR_FA_DIGEST_STALE")

    def test_confirm_unknown_candidate(self) -> None:
        _, prop, err, _ = self.svc.confirm_for_proposal(
            candidate_id="missing",
            bound_digest="sha256:x",
            change_svc=self.change,
        )
        self.assertIsNone(prop)
        self.assertEqual(err, ERR_AI_CANDIDATE_NOT_FOUND)

    def test_disabled_ai_no_store(self) -> None:
        broker = AiBroker(environ={})
        svc = AiCandidateService(broker=broker)
        stored, result = svc.suggest(
            prompt="x", workspace_id=self.root.name, goal_id=GOAL_ID
        )
        self.assertFalse(result.ok)
        self.assertIsNone(stored)


if __name__ == "__main__":
    unittest.main()
