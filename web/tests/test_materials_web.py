"""GOAL-016 stage C: materials Web list/upload/attach."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from main import app, get_goals_repository
from services.goals_repo import GoalsRepository
from services.workspace_config import COOKIE_FOCUS_WORKSPACE, ENV_DATA_ROOT


def _mk_ws(root: Path, ws_id: str) -> None:
    p = root / ws_id
    p.mkdir(parents=True)
    (p / "workspace.md").write_text(
        f"""---
id: {ws_id}
title: {ws_id}
status: active
root_goal: GOAL-001-a
canonical_scope: .
---
""",
        encoding="utf-8",
    )
    (p / "goal-tree.md").write_text("# t\n", encoding="utf-8")
    g = p / "GOAL-001-a"
    g.mkdir()
    (g / "00-meta.md").write_text(
        """---
id: GOAL-001-a
title: Root
status: active
parent: null
---
""",
        encoding="utf-8",
    )


class MaterialsWebTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _mk_ws(self.root, "workspace-001-a")
        self._prev = os.environ.get(ENV_DATA_ROOT)
        os.environ[ENV_DATA_ROOT] = str(self.root)
        app.dependency_overrides.clear()
        # Use real resolution so materials + focus work
        self.client = TestClient(app)
        self.client.cookies.set(COOKIE_FOCUS_WORKSPACE, "workspace-001-a")

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.clear()
        if self._prev is None:
            os.environ.pop(ENV_DATA_ROOT, None)
        else:
            os.environ[ENV_DATA_ROOT] = self._prev
        self._tmp.cleanup()

    def test_materials_page_and_upload_attach(self) -> None:
        page = self.client.get("/materials")
        self.assertEqual(page.status_code, 200)
        self.assertIn("资料库", page.text)
        self.assertIn("上传", page.text)

        up = self.client.post(
            "/materials/upload",
            data={"display_name": "Spec"},
            files={"file": ("spec.txt", b"stage-c material body", "text/plain")},
            follow_redirects=False,
        )
        self.assertIn(up.status_code, (303, 302))

        page2 = self.client.get("/materials")
        self.assertIn("Spec", page2.text)
        self.assertIn("mat-", page2.text)

        api = self.client.get("/api/materials")
        self.assertEqual(api.status_code, 200)
        body = api.json()
        self.assertTrue(body["ok"])
        self.assertGreaterEqual(len(body["materials"]), 1)
        mid = body["materials"][0]["material_id"]
        ver = body["materials"][0]["current_version"]

        att = self.client.post(
            "/materials/attach",
            data={"material_id": mid, "version": ver, "purpose": "pilot"},
            follow_redirects=False,
        )
        self.assertIn(att.status_code, (303, 302))

        api2 = self.client.get("/api/materials")
        self.assertEqual(len(api2.json()["refs"]), 1)
        self.assertEqual(api2.json()["refs"][0]["material_id"], mid)

        blob = self.client.get(f"/api/materials/{mid}/versions/{ver}/blob")
        self.assertEqual(blob.status_code, 200)
        self.assertEqual(blob.content, b"stage-c material body")
        self.assertIn("X-Material-Sha256", blob.headers)

        # Delete without confirm blocked when ref active
        bad = self.client.post(
            "/materials/delete",
            data={"material_id": mid, "confirm": ""},
        )
        self.assertEqual(bad.status_code, 400)

        ok = self.client.post(
            "/materials/delete",
            data={"material_id": mid, "confirm": "yes"},
            follow_redirects=False,
        )
        self.assertIn(ok.status_code, (303, 302))

    def test_upload_without_data_root(self) -> None:
        os.environ.pop(ENV_DATA_ROOT, None)
        r = self.client.post(
            "/materials/upload",
            data={"display_name": "X"},
            files={"file": ("a.txt", b"x", "text/plain")},
        )
        self.assertEqual(r.status_code, 400)

    def test_blob_rejects_goal_id(self) -> None:
        r = self.client.get("/api/materials/GOAL-001-a/versions/v1/blob")
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
