"""Resolve the product workspace root for the Web adapter.

Configuration is explicit and fail-closed: without a configured workspace path
and without an explicit DEV dogfood opt-in, the monorepo process tree is not
loaded.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Mapping


# Environment keys (also documented in web/README.md and .env.example).
ENV_WORKSPACE_DIR = "GOAL_GOVERNANCE_WORKSPACE_DIR"
ENV_DATA_ROOT = "GOAL_GOVERNANCE_DATA_ROOT"
ENV_DEV_DOGFOOD = "GOAL_GOVERNANCE_DEV_DOGFOOD"
# Cookie / session focus for multi-workspace N1 (GOAL-015 stage C).
COOKIE_FOCUS_WORKSPACE = "gg_focus_workspace_id"
ENV_ALLOW_CONTROLLED_WRITE = "GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE"
ENV_TEST_WRITE_MODE = "GOAL_GOVERNANCE_TEST_WRITE_MODE"
ENV_PRODUCT_GATES_OPEN = "GOAL_GOVERNANCE_PRODUCT_GATES_OPEN"

# Dogfood path relative to repository root (web/ is one level under root).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_WEB_DIR = Path(__file__).resolve().parents[1]
DOGFOOD_WORKSPACE = _REPO_ROOT / "docs" / "workspace-001-goal-governance"
_ENV_LOADED = False


def load_web_dotenv(*, override: bool = False) -> Path | None:
    """Load web/.env into os.environ if present.

    Does not override keys already set in the process environment unless
    override=True. Safe no-op when the file is missing. Not used by unit tests
    that pass explicit environ= maps.
    """
    global _ENV_LOADED
    path = _WEB_DIR / ".env"
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        if override or key not in os.environ:
            os.environ[key] = value
    _ENV_LOADED = True
    return path


def _env_truthy(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class WorkspaceConfig:
    """Resolved workspace binding for one Web process."""

    workspace_dir: Path | None
    source: str
    dev_dogfood: bool
    configured: bool
    error: str | None = None

    @property
    def is_ready(self) -> bool:
        return self.configured and self.workspace_dir is not None and self.error is None


def resolve_data_root(environ: dict[str, str] | None = None) -> Path | None:
    """Product data root for multi-workspace registry (GOAL-015). None if unset/missing."""
    env = environ if environ is not None else os.environ
    raw = (env.get(ENV_DATA_ROOT) or "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (_REPO_ROOT / path).resolve()
    else:
        path = path.resolve()
    if not path.is_dir():
        return None
    return path


def resolve_workspace_config(
    environ: dict[str, str] | None = None,
) -> WorkspaceConfig:
    """Resolve workspace path from environment (or an injected mapping for tests)."""
    env = environ if environ is not None else os.environ
    dev_dogfood = _truthy_map(env, ENV_DEV_DOGFOOD, default=False)

    explicit = (env.get(ENV_WORKSPACE_DIR) or "").strip()
    data_root = (env.get(ENV_DATA_ROOT) or "").strip()

    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_absolute():
            path = (_REPO_ROOT / path).resolve()
        else:
            path = path.resolve()
        if not path.is_dir():
            return WorkspaceConfig(
                workspace_dir=path,
                source=ENV_WORKSPACE_DIR,
                dev_dogfood=dev_dogfood,
                configured=True,
                error=f"Configured workspace directory does not exist: {path}",
            )
        return WorkspaceConfig(
            workspace_dir=path,
            source=ENV_WORKSPACE_DIR,
            dev_dogfood=dev_dogfood,
            configured=True,
            error=None,
        )

    if data_root:
        root = Path(data_root).expanduser()
        if not root.is_absolute():
            root = (_REPO_ROOT / root).resolve()
        else:
            root = root.resolve()
        # Prefer an explicit workspace-* child if present; else use data_root itself
        # when it already looks like a workspace (has goal-tree.md).
        if (root / "goal-tree.md").is_file():
            return WorkspaceConfig(
                workspace_dir=root,
                source=ENV_DATA_ROOT,
                dev_dogfood=dev_dogfood,
                configured=True,
                error=None,
            )
        workspace_children = sorted(
            p for p in root.iterdir() if p.is_dir() and p.name.startswith("workspace-")
        ) if root.is_dir() else []
        if len(workspace_children) == 1:
            return WorkspaceConfig(
                workspace_dir=workspace_children[0].resolve(),
                source=ENV_DATA_ROOT,
                dev_dogfood=dev_dogfood,
                configured=True,
                error=None,
            )
        if not root.is_dir():
            return WorkspaceConfig(
                workspace_dir=root,
                source=ENV_DATA_ROOT,
                dev_dogfood=dev_dogfood,
                configured=True,
                error=f"Configured data root does not exist: {root}",
            )
        return WorkspaceConfig(
            workspace_dir=None,
            source=ENV_DATA_ROOT,
            dev_dogfood=dev_dogfood,
            configured=True,
            error=(
                "Data root is set but no single workspace could be resolved "
                f"(expected goal-tree.md or exactly one workspace-* child): {root}"
            ),
        )

    if dev_dogfood:
        dogfood = DOGFOOD_WORKSPACE.resolve()
        if not dogfood.is_dir():
            return WorkspaceConfig(
                workspace_dir=dogfood,
                source=ENV_DEV_DOGFOOD,
                dev_dogfood=True,
                configured=True,
                error=f"DEV dogfood workspace missing: {dogfood}",
            )
        return WorkspaceConfig(
            workspace_dir=dogfood,
            source=ENV_DEV_DOGFOOD,
            dev_dogfood=True,
            configured=True,
            error=None,
        )

    return WorkspaceConfig(
        workspace_dir=None,
        source="none",
        dev_dogfood=False,
        configured=False,
        error=(
            "No workspace configured. Set GOAL_GOVERNANCE_WORKSPACE_DIR "
            "(or GOAL_GOVERNANCE_DATA_ROOT), or set GOAL_GOVERNANCE_DEV_DOGFOOD=true "
            "to load this repository's process workspace for local development only."
        ),
    )


def _truthy_map(env: Mapping[str, str], name: str, default: bool = False) -> bool:
    raw = env.get(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}


def production_product_gates_open(environ: dict[str, str] | None = None) -> bool:
    """Whether the product planning-gate latch is open (open → production writes blocked).

    Default is False after GOAL-009 A-030 (F-007/F-008 closed; I-003/I-004/I-006 α verified).
    Production writes still require GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE=true, a product
    (non-dogfood) workspace root, and single-process residual scope (R-F008-1～3).
    Set GOAL_GOVERNANCE_PRODUCT_GATES_OPEN=true to re-block all production controlled writes.
    """
    env = environ if environ is not None else os.environ
    return _truthy_map(env, ENV_PRODUCT_GATES_OPEN, default=False)


def test_write_mode_enabled(environ: dict[str, str] | None = None) -> bool:
    env = environ if environ is not None else os.environ
    return _truthy_map(env, ENV_TEST_WRITE_MODE, default=False)


def production_controlled_write_allowed(environ: dict[str, str] | None = None) -> bool:
    """True only when product gates are closed AND explicit production write flag is set."""
    env = environ if environ is not None else os.environ
    if production_product_gates_open(env):
        return False
    return _truthy_map(env, ENV_ALLOW_CONTROLLED_WRITE, default=False)


def controlled_write_authorized(
    *,
    test_authorized: bool = False,
    environ: dict[str, str] | None = None,
) -> bool:
    """Whether decide_and_execute may mutate canonical files in this process."""
    if test_authorized or test_write_mode_enabled(environ):
        return True
    return production_controlled_write_allowed(environ)
