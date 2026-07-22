"""GOAL-015 stage C: request-scoped workspace focus binding."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from services.workspace_binding import (
    build_focus_state,
    resolve_repository_for_request,
)
from services.workspace_config import COOKIE_FOCUS_WORKSPACE, ENV_DATA_ROOT, ENV_WORKSPACE_DIR
from services.workspace_registry import WorkspaceRegistryService


def _mk_ws(root: Path, ws_id: str, root_goal: str) -> Path:
    p = root / ws_id
    p.mkdir(parents=True)
    (p / "workspace.md").write_text(
        f"""---
id: {ws_id}
title: {ws_id}
status: active
root_goal: {root_goal}
canonical_scope: .
---
""",
        encoding="utf-8",
    )
    (p / "goal-tree.md").write_text("# t\n", encoding="utf-8")
    g = p / root_goal
    g.mkdir()
    (g / "00-meta.md").write_text(
        f"""---
id: {root_goal}
title: Root
status: active
parent: null
---
""",
        encoding="utf-8",
    )
    return p


class FocusStateTests(unittest.TestCase):
    def test_multi_without_cookie_needs_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _mk_ws(root, "workspace-001-a", "GOAL-001-a")
            _mk_ws(root, "workspace-002-b", "GOAL-001-b")
            env = {ENV_DATA_ROOT: str(root)}
            req = MagicMock()
            req.query_params.get.return_value = None
            req.cookies.get.return_value = None
            state = build_focus_state(req, env)
            self.assertTrue(state.needs_selection)
            self.assertIsNone(state.focus_workspace_id)
            self.assertEqual(len(state.workspaces), 2)

            repo = resolve_repository_for_request(req, env)
            self.assertFalse(repo.is_configured)

    def test_cookie_selects_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = _mk_ws(root, "workspace-001-a", "GOAL-001-a")
            _mk_ws(root, "workspace-002-b", "GOAL-001-b")
            env = {ENV_DATA_ROOT: str(root)}
            req = MagicMock()
            req.query_params.get.return_value = None
            req.cookies.get.side_effect = lambda k: (
                "workspace-001-a" if k == COOKIE_FOCUS_WORKSPACE else None
            )
            state = build_focus_state(req, env)
            self.assertFalse(state.needs_selection)
            self.assertEqual(state.focus_workspace_id, "workspace-001-a")
            repo = resolve_repository_for_request(req, env)
            self.assertTrue(repo.is_configured)
            self.assertEqual(repo.goals_dir.resolve(), a.resolve())

    def test_single_auto_focus(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = _mk_ws(root, "workspace-001-a", "GOAL-001-a")
            env = {ENV_DATA_ROOT: str(root)}
            state = build_focus_state(None, env)
            self.assertEqual(state.focus_workspace_id, "workspace-001-a")
            repo = resolve_repository_for_request(None, env)
            self.assertTrue(repo.is_configured)
            self.assertEqual(repo.goals_dir.resolve(), a.resolve())

    def test_alpha_workspace_dir_without_data_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = _mk_ws(root, "workspace-001-a", "GOAL-001-a")
            env = {ENV_WORKSPACE_DIR: str(a)}
            repo = resolve_repository_for_request(None, env)
            self.assertTrue(repo.is_configured)
            self.assertEqual(repo.goals_dir.resolve(), a.resolve())
