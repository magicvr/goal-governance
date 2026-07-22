"""R-003 WS-001..WS-006 executable cases (pure / service-layer)."""

from __future__ import annotations

import unittest

from services.workspace_isolation import (
    ERR_WS_CANONICAL_SCOPE_MISMATCH,
    ERR_WS_CROSS_WORKSPACE_ACCESS,
    ERR_WS_DOGFOOD_DEFAULT,
    ERR_WS_INDEX_CANONICAL_CONFLICT,
    ERR_WS_N1_FIELD_CONTRACT,
    ERR_WS_ROOT_GOAL_MISMATCH,
    AccessRequest,
    DiskRootFact,
    IndexGoalRow,
    WorkspaceBinding,
    resolve_index_vs_canonical,
    validate_canonical_scope,
    validate_cross_workspace_access,
    validate_n1_list_row,
    validate_root_goal_binding,
    validate_workspace_load_policy,
)


class WorkspaceIsolationWSTests(unittest.TestCase):
    def test_ws001_root_goal_mismatch(self) -> None:
        binding = WorkspaceBinding(
            workspace_id="ws-a",
            root_goal="GOAL-001-main-vision",
            canonical_scope="data/ws-a",
        )
        disk = DiskRootFact(
            root_goal_ids=("GOAL-001-other-root",),
            actual_root_path="data/ws-a",
        )
        r = validate_root_goal_binding(binding, disk)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_WS_ROOT_GOAL_MISMATCH)

        ok_disk = DiskRootFact(
            root_goal_ids=("GOAL-001-main-vision",),
            actual_root_path="data/ws-a",
        )
        self.assertTrue(validate_root_goal_binding(binding, ok_disk).ok)

        multi = DiskRootFact(
            root_goal_ids=("GOAL-001-a", "GOAL-001-b"),
            actual_root_path="data/ws-a",
        )
        self.assertEqual(validate_root_goal_binding(binding, multi).code, ERR_WS_ROOT_GOAL_MISMATCH)

    def test_ws002_canonical_scope_mismatch_and_other_ws(self) -> None:
        binding = WorkspaceBinding(
            workspace_id="ws-a",
            root_goal="GOAL-001-a",
            canonical_scope="data/ws-b",
        )
        disk = DiskRootFact(root_goal_ids=("GOAL-001-a",), actual_root_path="data/ws-a")
        r = validate_canonical_scope(binding, disk)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_WS_CANONICAL_SCOPE_MISMATCH)

        binding2 = WorkspaceBinding(
            workspace_id="ws-a",
            root_goal="GOAL-001-a",
            canonical_scope="data/ws-a",
        )
        # Scope equals actual but equals another listed root (same path identity only ok once)
        r2 = validate_canonical_scope(
            WorkspaceBinding(
                workspace_id="ws-a",
                root_goal="GOAL-001-a",
                canonical_scope="data/ws-other",
            ),
            DiskRootFact(root_goal_ids=("GOAL-001-a",), actual_root_path="data/ws-other"),
            other_workspace_roots=("data/ws-other",),  # same as actual — not "other"
        )
        self.assertTrue(r2.ok)

        r3 = validate_canonical_scope(
            WorkspaceBinding(
                workspace_id="ws-a",
                root_goal="GOAL-001-a",
                canonical_scope="data/ws-evil",
            ),
            DiskRootFact(root_goal_ids=("GOAL-001-a",), actual_root_path="data/ws-a"),
            other_workspace_roots=("data/ws-evil",),
        )
        self.assertEqual(r3.code, ERR_WS_CANONICAL_SCOPE_MISMATCH)

        self.assertTrue(
            validate_canonical_scope(
                binding2,
                DiskRootFact(root_goal_ids=("GOAL-001-a",), actual_root_path="data/ws-a"),
                other_workspace_roots=("data/ws-b",),
            ).ok
        )

    def test_ws003_cross_workspace_access_denied_no_leak(self) -> None:
        bad = AccessRequest(
            bound_workspace_id="ws-a",
            target_workspace_id="ws-b",
            target_path="GOAL-001-x/02-execution.md",
            action="read",
        )
        r = validate_cross_workspace_access(bad)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_WS_CROSS_WORKSPACE_ACCESS)
        self.assertFalse(r.details.get("leaked_body"))

        good = AccessRequest(
            bound_workspace_id="ws-a",
            target_workspace_id="ws-a",
            target_path="GOAL-001-x/02-execution.md",
            action="write",
        )
        self.assertTrue(validate_cross_workspace_access(good).ok)

    def test_ws004_n1_forbidden_fields(self) -> None:
        bad = {
            "workspace_id": "ws-a",
            "display_name": "A",
            "root_goal": "GOAL-001-a",
            "status": "active",
            "progress": "50%",
        }
        r = validate_n1_list_row(bad)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_WS_N1_FIELD_CONTRACT)

        bad2 = {
            "workspace_id": "ws-a",
            "display_name": "A",
            "root_goal": "GOAL-001-a",
            "status": "active",
            "findings": ["F-001"],
        }
        self.assertEqual(validate_n1_list_row(bad2).code, ERR_WS_N1_FIELD_CONTRACT)

        ok = {
            "workspace_id": "ws-a",
            "display_name": "A",
            "root_goal": "GOAL-001-a",
            "status": "archived",
        }
        self.assertTrue(validate_n1_list_row(ok).ok)

    def test_ws005_dogfood_default_refused(self) -> None:
        r = validate_workspace_load_policy(
            workspace_configured=False,
            dev_dogfood=False,
            would_load_dogfood_default=True,
        )
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_WS_DOGFOOD_DEFAULT)

        ok_opt_in = validate_workspace_load_policy(
            workspace_configured=False,
            dev_dogfood=True,
            would_load_dogfood_default=True,
        )
        self.assertTrue(ok_opt_in.ok)

        idle = validate_workspace_load_policy(
            workspace_configured=False,
            dev_dogfood=False,
            would_load_dogfood_default=False,
        )
        self.assertTrue(idle.ok)

    def test_ws006_index_conflict_markdown_wins(self) -> None:
        r = resolve_index_vs_canonical(
            index_rows=(IndexGoalRow(goal_id="GOAL-009-x", status="done"),),
            canonical_status_by_goal={"GOAL-009-x": "active"},
        )
        self.assertTrue(r.ok)  # continue with canonical
        self.assertEqual(r.index_status, "invalid")
        self.assertEqual(r.code, ERR_WS_INDEX_CANONICAL_CONFLICT)

        ok = resolve_index_vs_canonical(
            index_rows=(IndexGoalRow(goal_id="GOAL-009-x", status="active"),),
            canonical_status_by_goal={"GOAL-009-x": "active"},
        )
        self.assertEqual(ok.index_status, "valid")
        self.assertIsNone(ok.code)


if __name__ == "__main__":
    unittest.main()
