"""GOAL-014 stage B: AI config resolve (fail closed, no key in public dict)."""

from __future__ import annotations

import unittest

from services.ai_config import (
    ERR_AI_CONFIG_INCOMPLETE,
    ERR_AI_DISABLED,
    resolve_ai_config,
)


class AiConfigTests(unittest.TestCase):
    def test_disabled_by_default(self) -> None:
        cfg = resolve_ai_config({})
        self.assertFalse(cfg.enabled)
        self.assertFalse(cfg.ready)
        self.assertEqual(cfg.error_code, ERR_AI_DISABLED)

    def test_enabled_incomplete(self) -> None:
        cfg = resolve_ai_config(
            {
                "GOAL_GOVERNANCE_AI_ENABLED": "true",
                "GOAL_GOVERNANCE_AI_PROVIDER": "openai-compatible",
            }
        )
        self.assertTrue(cfg.enabled)
        self.assertFalse(cfg.ready)
        self.assertEqual(cfg.error_code, ERR_AI_CONFIG_INCOMPLETE)
        self.assertIn("GOAL_GOVERNANCE_AI_BASE_URL", cfg.error_message or "")

    def test_ready_when_complete(self) -> None:
        cfg = resolve_ai_config(
            {
                "GOAL_GOVERNANCE_AI_ENABLED": "true",
                "GOAL_GOVERNANCE_AI_PROVIDER": "openai-compatible",
                "GOAL_GOVERNANCE_AI_BASE_URL": "https://api.example.com/v1",
                "GOAL_GOVERNANCE_AI_API_KEY": "sk-secret-test-key",
                "GOAL_GOVERNANCE_AI_MODEL": "gpt-test",
                "GOAL_GOVERNANCE_AI_REQUEST_TIMEOUT_SECONDS": "12",
                "GOAL_GOVERNANCE_AI_TEMPERATURE": "0.2",
                "GOAL_GOVERNANCE_AI_MAX_OUTPUT_TOKENS": "256",
            }
        )
        self.assertTrue(cfg.ready)
        self.assertIsNone(cfg.error_code)
        self.assertEqual(cfg.timeout_seconds, 12.0)
        self.assertEqual(cfg.temperature, 0.2)
        self.assertEqual(cfg.max_output_tokens, 256)
        self.assertEqual(cfg.api_key, "sk-secret-test-key")

    def test_public_dict_never_contains_api_key(self) -> None:
        cfg = resolve_ai_config(
            {
                "GOAL_GOVERNANCE_AI_ENABLED": "true",
                "GOAL_GOVERNANCE_AI_PROVIDER": "openai-compatible",
                "GOAL_GOVERNANCE_AI_BASE_URL": "https://api.example.com/v1",
                "GOAL_GOVERNANCE_AI_API_KEY": "sk-secret-must-not-leak",
                "GOAL_GOVERNANCE_AI_MODEL": "gpt-test",
            }
        )
        public = cfg.public_dict()
        blob = str(public)
        self.assertNotIn("sk-secret", blob)
        self.assertNotIn("api_key", public)  # only api_key_set boolean
        self.assertTrue(public["api_key_set"])
        self.assertTrue(public["ready"])
        redacted = cfg.redacted_debug()
        self.assertEqual(redacted["api_key"], "***")
        self.assertNotIn("sk-secret", str(redacted))


if __name__ == "__main__":
    unittest.main()
