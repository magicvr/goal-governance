"""GOAL-015 stage D: archive UX + cross-workspace negative matrix (HTTP/service)."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from main import app, get_goals_repository
from services.workspace_config import COOKIE_FOCUS_WORKSPACE, ENV_DATA_ROOT
from services.workspace_isolation import N1_ALLOWED_FIELDS, validate_n1_list_row
from services.workspace_registry import (
    WorkspaceRegistryService,
    assert_workspace_access,
)


def _mk_ws(root: Path, ws_id: str, root_goal: str, *, marker: str = "") -> Path:
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
    (p / "goal-tree.md").write_text(
        f"""---
title: Goal Tree
status: active
---

# Goal Tree

| ID | 标题 | Parent | Status | Progress |
|----|------|--------|--------|----------|
| {root_goal} | Root | — | active | 0% |
""",
        encoding="utf-8",
    )
    g = p / root_goal
    g.mkdir()
    (g / "attachments").mkdir()
    body = f"SECRET_MARKER_{marker}" if marker else "root body"
    (g / "00-meta.md").write_text(
        f"""---
id: {root_goal}
title: Root {marker or ws_id}
status: active
parent: null
created: 2026-07-22
updated: 2026-07-22
version: 0.1.0
---

# {root_goal}

{body}
""",
        encoding="utf-8",
    )
    for name, doc in (
        ("01-decision.md", "decision"),
        ("02-execution.md", "execution"),
        ("03-audit.md", "audit"),
    ):
        (g / name).write_text(
            f"""---
id: {root_goal}
doc: {doc}
status: active
parent: null
---

# {doc}
""",
            encoding="utf-8",
        )
    return p


class StageDArchiveAndIsolationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._prev_data = os.environ.get(ENV_DATA_ROOT)
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _mk_ws(self.root, "workspace-001-a", "GOAL-001-a", marker="AAA")
        _mk_ws(self.root, "workspace-002-b", "GOAL-001-b", marker="BBB")
        os.environ[ENV_DATA_ROOT] = str(self.root)
        app.dependency_overrides.clear()
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.clear()
        if self._prev_data is None:
            os.environ.pop(ENV_DATA_ROOT, None)
        else:
            os.environ[ENV_DATA_ROOT] = self._prev_data
        self._tmp.cleanup()

    def test_archive_hides_from_default_list_keeps_files(self) -> None:
        page = self.client.get("/workspaces")
        self.assertEqual(page.status_code, 200)
        self.assertIn("workspace-001-a", page.text)
        self.assertIn("归档", page.text)

        arch = self.client.post(
            "/workspaces/status",
            data={"workspace_id": "workspace-001-a", "status": "archived"},
            follow_redirects=False,
        )
        self.assertIn(arch.status_code, (303, 302))

        page2 = self.client.get("/workspaces")
        self.assertEqual(page2.status_code, 200)
        # Active section should not offer select for archived; archived section lists it
        self.assertIn("已归档", page2.text)
        self.assertIn("取消归档", page2.text)

        # Canonical retained
        meta = self.root / "workspace-001-a" / "GOAL-001-a" / "00-meta.md"
        self.assertTrue(meta.is_file())
        self.assertIn("SECRET_MARKER_AAA", meta.read_text(encoding="utf-8"))

        # Cannot select archived as focus
        bad = self.client.post(
            "/workspaces/select",
            data={"workspace_id": "workspace-001-a"},
            follow_redirects=False,
        )
        self.assertEqual(bad.status_code, 400)

        # Unarchive
        un = self.client.post(
            "/workspaces/status",
            data={"workspace_id": "workspace-001-a", "status": "active"},
            follow_redirects=False,
        )
        self.assertIn(un.status_code, (303, 302))
        ok = self.client.post(
            "/workspaces/select",
            data={"workspace_id": "workspace-001-a"},
            follow_redirects=False,
        )
        self.assertIn(ok.status_code, (303, 302))

    def test_archive_clears_focus_cookie(self) -> None:
        self.client.cookies.set(COOKIE_FOCUS_WORKSPACE, "workspace-001-a")
        arch = self.client.post(
            "/workspaces/status",
            data={"workspace_id": "workspace-001-a", "status": "archived"},
            follow_redirects=False,
        )
        self.assertIn(arch.status_code, (303, 302))
        # Starlette TestClient: deleted cookie often empty
        # Home should fail closed (multi remains with only B active — auto focus B)
        home = self.client.get("/")
        self.assertEqual(home.status_code, 200)
        # Must not show AAA secret when focused elsewhere or auto B
        # After archive A, only B is active → auto focus B
        self.assertNotIn("SECRET_MARKER_AAA", home.text)

    def test_cross_workspace_goal_not_leaked_via_http(self) -> None:
        """Focus A: request B's goal id → 404; response must not contain B marker."""
        self.client.cookies.set(COOKIE_FOCUS_WORKSPACE, "workspace-001-a")
        resp = self.client.get("/goals/GOAL-001-b")
        self.assertEqual(resp.status_code, 404)
        self.assertNotIn("SECRET_MARKER_BBB", resp.text)
        self.assertNotIn("SECRET_MARKER_AAA", resp.text)

        # Focus A can load its own goal
        ok = self.client.get("/goals/GOAL-001-a")
        self.assertEqual(ok.status_code, 200)
        self.assertIn("SECRET_MARKER_AAA", ok.text)
        self.assertNotIn("SECRET_MARKER_BBB", ok.text)

    def test_api_n1_no_forbidden_fields(self) -> None:
        api = self.client.get("/api/workspaces?include_archived=true")
        self.assertEqual(api.status_code, 200)
        body = api.json()
        self.assertTrue(body["ok"])
        for row in body.get("workspaces") or []:
            self.assertEqual(set(row.keys()), N1_ALLOWED_FIELDS)
            self.assertTrue(validate_n1_list_row(row).ok)
        for row in body.get("archived") or []:
            self.assertEqual(set(row.keys()), N1_ALLOWED_FIELDS)

    def test_service_cross_workspace_matrix(self) -> None:
        cases = [
            ("ws-a", "ws-a", "read", True),
            ("ws-a", "ws-b", "read", False),
            ("ws-a", "ws-b", "write", False),
            ("ws-b", "ws-a", "write", False),
        ]
        for bound, target, action, expect_ok in cases:
            r = assert_workspace_access(
                bound_workspace_id=bound,
                target_workspace_id=target,
                action=action,
                target_path=f"GOAL-001-x/00-meta.md",
            )
            self.assertEqual(r.ok, expect_ok, msg=(bound, target, action))
            if not r.ok:
                self.assertFalse(r.details.get("leaked_body", True))

    def test_status_without_data_root_rejected(self) -> None:
        os.environ.pop(ENV_DATA_ROOT, None)
        r = self.client.post(
            "/workspaces/status",
            data={"workspace_id": "workspace-001-a", "status": "archived"},
        )
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
