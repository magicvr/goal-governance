"""GOAL-015 stage B: workspace registry / discovery / isolation service."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from services.workspace_isolation import (
    ERR_WS_CROSS_WORKSPACE_ACCESS,
    ERR_WS_N1_FIELD_CONTRACT,
    N1_ALLOWED_FIELDS,
)
from services.workspace_registry import (
    ERR_REG_CROSS_WORKSPACE,
    ERR_REG_ID_CONFLICT,
    ERR_REG_N1_CONTRACT,
    ERR_REG_NO_DATA_ROOT,
    ERR_REG_NOT_FOUND,
    WorkspaceRegistryService,
    assert_workspace_access,
    n1_public_row,
)

R004_FIXTURE = Path(__file__).parent / "fixtures" / "r004" / "workspace-ok"


def _write_ws(
    root: Path,
    *,
    ws_id: str,
    title: str,
    root_goal: str,
    status: str = "active",
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "workspace.md").write_text(
        f"""---
id: {ws_id}
title: {title}
status: {status}
root_goal: {root_goal}
canonical_scope: .
created: 2026-07-22
updated: 2026-07-22
version: 0.1.0
---

# {title}
""",
        encoding="utf-8",
    )
    (root / "goal-tree.md").write_text("# tree\n", encoding="utf-8")
    goal_dir = root / root_goal
    goal_dir.mkdir(parents=True, exist_ok=True)
    (goal_dir / "attachments").mkdir(exist_ok=True)
    (goal_dir / "00-meta.md").write_text(
        f"""---
id: {root_goal}
title: Root
status: active
parent: null
created: 2026-07-22
updated: 2026-07-22
version: 0.1.0
---
""",
        encoding="utf-8",
    )
    return root


class N1ContractTests(unittest.TestCase):
    def test_n1_whitelist_only(self) -> None:
        ok = n1_public_row(
            {
                "workspace_id": "workspace-001-a",
                "display_name": "A",
                "root_goal": "GOAL-001-a",
                "status": "active",
                "progress": "50%",  # stripped then forbidden if kept
            }
        )
        # progress is stripped by cleaner — only known keys kept
        self.assertTrue(ok.ok)
        row = ok.details["row"]
        self.assertEqual(set(row.keys()), N1_ALLOWED_FIELDS)

    def test_n1_rejects_forbidden_if_present(self) -> None:
        bad = n1_public_row(
            {
                "workspace_id": "w",
                "display_name": "A",
                "root_goal": "GOAL-001-a",
                "status": "active",
                "progress": "1",
            }
        )
        # cleaner drops progress — so this is ok. Force raw validate via extra only path:
        from services.workspace_isolation import validate_n1_list_row

        r = validate_n1_list_row(
            {
                "workspace_id": "w",
                "display_name": "A",
                "root_goal": "GOAL-001-a",
                "status": "active",
                "progress": "1",
            }
        )
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_WS_N1_FIELD_CONTRACT)


class IsolationWrapperTests(unittest.TestCase):
    def test_cross_workspace_denied_no_body(self) -> None:
        r = assert_workspace_access(
            bound_workspace_id="ws-a",
            target_workspace_id="ws-b",
            action="read",
            target_path="GOAL-001-x/00-meta.md",
        )
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_REG_CROSS_WORKSPACE)
        self.assertFalse(r.details.get("leaked_body"))

    def test_same_workspace_ok(self) -> None:
        r = assert_workspace_access(
            bound_workspace_id="ws-a",
            target_workspace_id="ws-a",
            action="write",
        )
        self.assertTrue(r.ok)


class WorkspaceRegistryServiceTests(unittest.TestCase):
    def test_missing_data_root(self) -> None:
        svc = WorkspaceRegistryService(Path("/nonexistent-data-root-xyz-015"))
        r = svc.list_n1()
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_REG_NO_DATA_ROOT)

    def test_discover_and_list_two_workspaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_ws(
                root / "workspace-001-alpha",
                ws_id="workspace-001-alpha",
                title="Alpha",
                root_goal="GOAL-001-alpha-root",
            )
            _write_ws(
                root / "workspace-002-beta",
                ws_id="workspace-002-beta",
                title="Beta",
                root_goal="GOAL-001-beta-root",
            )
            svc = WorkspaceRegistryService(root)
            listed = svc.list_n1()
            self.assertTrue(listed.ok)
            rows = listed.details["workspaces"]
            self.assertEqual(len(rows), 2)
            ids = {r["workspace_id"] for r in rows}
            self.assertEqual(ids, {"workspace-001-alpha", "workspace-002-beta"})
            for row in rows:
                self.assertEqual(set(row.keys()), N1_ALLOWED_FIELDS)
                self.assertIn(row["status"], {"active", "archived"})

    def test_register_and_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ws = _write_ws(
                root / "workspace-001-alpha",
                ws_id="workspace-001-alpha",
                title="Alpha",
                root_goal="GOAL-001-alpha-root",
            )
            svc = WorkspaceRegistryService(root)
            reg = svc.register_existing(ws, status="active")
            self.assertTrue(reg.ok)
            self.assertTrue(svc.registry_path.is_file())

            arch = svc.set_status("workspace-001-alpha", "archived")
            self.assertTrue(arch.ok)
            listed = svc.list_n1(include_archived=False)
            self.assertEqual(listed.details["count"], 0)
            listed2 = svc.list_n1(include_archived=True)
            self.assertEqual(listed2.details["count"], 1)
            self.assertEqual(listed2.details["workspaces"][0]["status"], "archived")

            # Canonical not deleted
            self.assertTrue((ws / "workspace.md").is_file())
            self.assertTrue((ws / "GOAL-001-alpha-root" / "00-meta.md").is_file())

    def test_create_workspace_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            svc = WorkspaceRegistryService(root)
            created = svc.create_workspace(
                workspace_id="demo",
                title="Demo WS",
                root_goal_slug="demo-root",
                root_goal_title="Demo Root",
            )
            self.assertTrue(created.ok, msg=created.message)
            ws_id = created.details["workspace_id"]
            self.assertTrue(ws_id.startswith("workspace-"))
            path = Path(str(created.details["path"]))
            self.assertTrue((path / "workspace.md").is_file())
            self.assertTrue((path / "goal-tree.md").is_file())
            self.assertTrue((path / "GOAL-001-demo-root" / "00-meta.md").is_file())
            n1 = created.details["n1"]
            self.assertEqual(set(n1.keys()), N1_ALLOWED_FIELDS)

            listed = svc.list_n1()
            self.assertEqual(listed.details["count"], 1)
            self.assertEqual(listed.details["workspaces"][0]["workspace_id"], ws_id)

            # Conflict on second create same id
            again = svc.create_workspace(workspace_id=ws_id)
            self.assertFalse(again.ok)
            self.assertEqual(again.code, ERR_REG_ID_CONFLICT)

    def test_resolve_and_get(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_ws(
                root / "workspace-001-alpha",
                ws_id="workspace-001-alpha",
                title="Alpha",
                root_goal="GOAL-001-alpha-root",
            )
            svc = WorkspaceRegistryService(root)
            got = svc.get("workspace-001-alpha")
            self.assertTrue(got.ok)
            path = svc.resolve_path("workspace-001-alpha")
            self.assertTrue(path.ok)
            missing = svc.get("workspace-999-none")
            self.assertFalse(missing.ok)
            self.assertEqual(missing.code, ERR_REG_NOT_FOUND)

    def test_invalid_root_goal_excluded_from_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad = root / "workspace-001-bad"
            bad.mkdir()
            (bad / "workspace.md").write_text(
                """---
id: workspace-001-bad
title: Bad
status: active
root_goal: GOAL-001-declared
canonical_scope: .
---
""",
                encoding="utf-8",
            )
            (bad / "goal-tree.md").write_text("# t\n", encoding="utf-8")
            # Disk root differs from declared
            g = bad / "GOAL-001-other"
            g.mkdir()
            (g / "00-meta.md").write_text(
                """---
id: GOAL-001-other
title: Other
status: active
parent: null
---
""",
                encoding="utf-8",
            )
            svc = WorkspaceRegistryService(root)
            listed = svc.list_n1()
            self.assertTrue(listed.ok)
            self.assertEqual(listed.details["count"], 0)
            self.assertTrue(len(listed.details["invalid"]) >= 1)

    def test_registry_refuses_path_outside_data_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "data"
            root.mkdir()
            outside = Path(tmp) / "outside-ws"
            _write_ws(
                outside,
                ws_id="workspace-001-out",
                title="Out",
                root_goal="GOAL-001-out",
            )
            svc = WorkspaceRegistryService(root)
            r = svc.register_existing(outside)
            self.assertFalse(r.ok)

    def test_r004_fixture_as_single_under_data_root_copy(self) -> None:
        """Copy synthetic fixture shape into data_root child and list."""
        if not R004_FIXTURE.is_dir():
            self.skipTest("r004 fixture missing")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = root / "workspace-ok-fixture"
            # minimal re-write using fixture's workspace id
            meta = (R004_FIXTURE / "workspace.md").read_text(encoding="utf-8")
            dest.mkdir()
            (dest / "workspace.md").write_text(meta, encoding="utf-8")
            (dest / "goal-tree.md").write_text(
                (R004_FIXTURE / "goal-tree.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            # copy goal folder
            import shutil

            shutil.copytree(
                R004_FIXTURE / "GOAL-001-fixture-target",
                dest / "GOAL-001-fixture-target",
            )
            svc = WorkspaceRegistryService(root)
            listed = svc.list_n1()
            self.assertTrue(listed.ok)
            self.assertEqual(listed.details["count"], 1)
            row = listed.details["workspaces"][0]
            self.assertEqual(row["workspace_id"], "workspace-ok-fixture")
            self.assertEqual(row["root_goal"], "GOAL-001-fixture-target")


if __name__ == "__main__":
    unittest.main()
