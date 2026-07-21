"""AI runtime configuration (GOAL-014 stage B · R-014-A §3).

Fail-closed: AI calls require AI_ENABLED=true and complete provider fields.
Never expose API keys in public summaries, health JSON, or logs helpers.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any, Mapping


ENV_AI_ENABLED = "GOAL_GOVERNANCE_AI_ENABLED"
ENV_AI_PROVIDER = "GOAL_GOVERNANCE_AI_PROVIDER"
ENV_AI_BASE_URL = "GOAL_GOVERNANCE_AI_BASE_URL"
ENV_AI_API_KEY = "GOAL_GOVERNANCE_AI_API_KEY"
ENV_AI_MODEL = "GOAL_GOVERNANCE_AI_MODEL"
ENV_AI_TIMEOUT = "GOAL_GOVERNANCE_AI_REQUEST_TIMEOUT_SECONDS"
ENV_AI_TEMPERATURE = "GOAL_GOVERNANCE_AI_TEMPERATURE"
ENV_AI_MAX_TOKENS = "GOAL_GOVERNANCE_AI_MAX_OUTPUT_TOKENS"

ERR_AI_DISABLED = "ERR_AI_DISABLED"
ERR_AI_CONFIG_INCOMPLETE = "ERR_AI_CONFIG_INCOMPLETE"


def _truthy(env: Mapping[str, str], name: str, default: bool = False) -> bool:
    raw = env.get(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}


def _strip(env: Mapping[str, str], name: str) -> str:
    return str(env.get(name) or "").strip()


@dataclass(frozen=True)
class AiConfig:
    """Resolved AI settings for one process (may be disabled / incomplete)."""

    enabled: bool
    provider: str
    base_url: str
    api_key: str
    model: str
    timeout_seconds: float
    temperature: float | None
    max_output_tokens: int | None
    ready: bool
    error_code: str | None
    error_message: str | None

    def public_dict(self) -> dict[str, Any]:
        """Safe for health/UI — never includes api_key."""
        return {
            "enabled": self.enabled,
            "ready": self.ready,
            "provider": self.provider or None,
            "base_url_set": bool(self.base_url),
            "model": self.model or None,
            "timeout_seconds": self.timeout_seconds,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "api_key_set": bool(self.api_key),
        }

    def redacted_debug(self) -> dict[str, Any]:
        """Debug view with key redacted."""
        d = self.public_dict()
        d["api_key"] = "***" if self.api_key else ""
        return d


def resolve_ai_config(environ: Mapping[str, str] | None = None) -> AiConfig:
    """Resolve AI config from environment (injectable for tests)."""
    env = environ if environ is not None else os.environ
    enabled = _truthy(env, ENV_AI_ENABLED, default=False)
    provider = _strip(env, ENV_AI_PROVIDER)
    base_url = _strip(env, ENV_AI_BASE_URL)
    api_key = _strip(env, ENV_AI_API_KEY)
    model = _strip(env, ENV_AI_MODEL)

    timeout_raw = _strip(env, ENV_AI_TIMEOUT) or "30"
    try:
        timeout_seconds = float(timeout_raw)
    except ValueError:
        timeout_seconds = 30.0
    if timeout_seconds <= 0:
        timeout_seconds = 30.0

    temp_raw = _strip(env, ENV_AI_TEMPERATURE)
    temperature: float | None
    if temp_raw == "":
        temperature = None
    else:
        try:
            temperature = float(temp_raw)
        except ValueError:
            temperature = None

    max_raw = _strip(env, ENV_AI_MAX_TOKENS)
    max_output_tokens: int | None
    if max_raw == "":
        max_output_tokens = None
    else:
        try:
            max_output_tokens = int(max_raw)
        except ValueError:
            max_output_tokens = None

    if not enabled:
        return AiConfig(
            enabled=False,
            provider=provider,
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            ready=False,
            error_code=ERR_AI_DISABLED,
            error_message="AI is disabled (GOAL_GOVERNANCE_AI_ENABLED is not true)",
        )

    missing: list[str] = []
    if not provider:
        missing.append(ENV_AI_PROVIDER)
    if not base_url:
        missing.append(ENV_AI_BASE_URL)
    if not api_key:
        missing.append(ENV_AI_API_KEY)
    if not model:
        missing.append(ENV_AI_MODEL)
    if missing:
        return AiConfig(
            enabled=True,
            provider=provider,
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            ready=False,
            error_code=ERR_AI_CONFIG_INCOMPLETE,
            error_message="AI enabled but incomplete config: " + ", ".join(missing),
        )

    return AiConfig(
        enabled=True,
        provider=provider,
        base_url=base_url.rstrip("/"),
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        ready=True,
        error_code=None,
        error_message=None,
    )
