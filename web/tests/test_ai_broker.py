"""GOAL-014 stage B: AI broker gates + fake transport."""

from __future__ import annotations

import unittest

from services.ai_broker import (
    ERR_AI_CALL_FAILED,
    AiBroker,
    AiBrokerError,
    CompletionRequest,
    FakeTransport,
)
from services.ai_config import ERR_AI_CONFIG_INCOMPLETE, ERR_AI_DISABLED, resolve_ai_config


def _ready_env() -> dict[str, str]:
    return {
        "GOAL_GOVERNANCE_AI_ENABLED": "true",
        "GOAL_GOVERNANCE_AI_PROVIDER": "openai-compatible",
        "GOAL_GOVERNANCE_AI_BASE_URL": "https://api.example.com/v1",
        "GOAL_GOVERNANCE_AI_API_KEY": "sk-test-key-not-for-prod",
        "GOAL_GOVERNANCE_AI_MODEL": "gpt-test",
    }


class AiBrokerTests(unittest.TestCase):
    def test_complete_fails_when_disabled(self) -> None:
        broker = AiBroker(environ={})
        result = broker.complete(
            CompletionRequest(
                prompt="Hello",
                workspace_id="ws-1",
                goal_id="GOAL-001-x",
            )
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.code, ERR_AI_DISABLED)
        self.assertNotIn("sk-", str(result.public_dict()))

    def test_complete_fails_when_incomplete(self) -> None:
        broker = AiBroker(
            environ={
                "GOAL_GOVERNANCE_AI_ENABLED": "true",
                "GOAL_GOVERNANCE_AI_PROVIDER": "x",
            }
        )
        result = broker.complete(
            CompletionRequest(prompt="Hi", workspace_id="ws", goal_id="GOAL-001")
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.code, ERR_AI_CONFIG_INCOMPLETE)

    def test_fake_transport_happy_path_candidate_fields(self) -> None:
        transport = FakeTransport(response_text="Suggested next step for the goal.")
        broker = AiBroker(
            config=resolve_ai_config(_ready_env()),
            transport=transport,
        )
        result = broker.complete(
            CompletionRequest(
                prompt="What next?",
                workspace_id="product-workspace",
                goal_id="GOAL-001-fixture-target",
                context_blocks=("## meta\nstatus: active",),
            )
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.source_kind, "ai-knowledge")
        self.assertIn("model knowledge", result.source_statement or "")
        self.assertTrue(result.content_digest and result.content_digest.startswith("sha256:"))
        self.assertTrue(result.candidate_id and result.candidate_id.startswith("cand_ai_"))
        self.assertEqual(result.content, "Suggested next step for the goal.")
        self.assertEqual(len(transport.calls), 1)
        public = result.public_dict()
        self.assertNotIn("sk-test", str(public))
        self.assertNotIn("api_key", public)

    def test_transport_error_mapped(self) -> None:
        class BoomTransport:
            def complete(self, *, config, messages):  # type: ignore[no-untyped-def]
                raise AiBrokerError(ERR_AI_CALL_FAILED, "provider HTTP 500")

        broker = AiBroker(
            config=resolve_ai_config(_ready_env()),
            transport=BoomTransport(),
        )
        result = broker.complete(
            CompletionRequest(prompt="x", workspace_id="ws", goal_id="GOAL-001")
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.code, ERR_AI_CALL_FAILED)

    def test_status_matches_public_config(self) -> None:
        broker = AiBroker(environ=_ready_env())
        status = broker.status()
        self.assertTrue(status["ready"])
        self.assertTrue(status["api_key_set"])
        self.assertNotIn("api_key", status)
        self.assertNotIn("sk-test", str(status))


if __name__ == "__main__":
    unittest.main()
