from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS = REPO_ROOT / "AGENTS.md"
FIXTURE = (
    REPO_ROOT
    / "docs/goals/GOAL-008-skills-consumer-adapter-release-consistency/attachments"
    / "i-002-runtime-fixture-2026-07-19.md"
)


class GrokRuntimeFixtureTests(unittest.TestCase):
    def test_replay_command_uses_api_model_not_adapter_id(self) -> None:
        fixture = FIXTURE.read_text(encoding="utf-8")
        commands = re.findall(r"(?m)^grok -p .+$", fixture)

        self.assertTrue(commands, "fixture must contain a Grok headless replay command")
        for command in commands:
            self.assertIn("--model grok-4.5", command)
            self.assertNotRegex(
                command,
                r"--model\s+(?:grok-build|grok-build-cli)(?:\s|$)",
            )
            self.assertNotRegex(
                command,
                r"(?:^|\s)-m\s+(?:grok-build|grok-build-cli)(?:\s|$)",
            )

    def test_runtime_attachment_scopes_adapter_id_and_model_failure(self) -> None:
        repository_policy = AGENTS.read_text(encoding="utf-8")
        fixture = FIXTURE.read_text(encoding="utf-8")

        self.assertNotIn("GROK_MODELS_BASE_URL", repository_policy)
        self.assertNotIn("[model.grok-build]", repository_policy)
        self.assertIn("`grok-build-cli` 只表示兼容矩阵中的宿主适配器 ID", fixture)
        self.assertIn("`grok-build` 作为 API model", fixture)
        self.assertIn("`--model grok-4.5`", fixture)
        self.assertIn("[model.grok-build]", fixture)
        self.assertIn('model = "grok-4.5"', fixture)
        self.assertIn('base_url = "${GROK_MODELS_BASE_URL}"', fixture)
        self.assertIn("unknown provider", fixture)
        self.assertIn("exit `0`", fixture)

    def test_historical_provider_failure_remains_explicit(self) -> None:
        fixture = FIXTURE.read_text(encoding="utf-8")

        self.assertIn("unknown provider for model grok-build", fixture)
        self.assertIn("headless provider 配置仍为 `blocked`", fixture)
        self.assertIn("以 Responses API 错误为准", fixture)


if __name__ == "__main__":
    unittest.main()
