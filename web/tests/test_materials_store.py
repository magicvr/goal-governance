"""GOAL-016 stage B: SharedMaterialsStore product paths."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from services.materials_store import (
    ERR_MS_NOT_FOUND,
    SharedMaterialsStore,
)
from services.shared_materials import (
    ERR_SM_DELETE_WITHOUT_REF_CHECK,
    ERR_SM_GOAL_PATH_VIA_MATERIALS,
    ERR_SM_INCOMPLETE_REF,
    ERR_SM_WORKSPACE_MISMATCH,
    digest_bytes,
)


class MaterialsStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        # Synthetic workspaces for isolation roots
        for name in ("workspace-001-a", "workspace-002-b"):
            p = self.root / name
            p.mkdir()
            (p / "goal-tree.md").write_text("# t\n", encoding="utf-8")
            (p / "GOAL-001-x").mkdir()
        self.store = SharedMaterialsStore(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_put_list_get_roundtrip(self) -> None:
        body = b"hello shared materials product"
        put = self.store.put_bytes(data=body, display_name="Hello")
        self.assertTrue(put.ok, msg=put.message)
        mid = str(put.details["material_id"])
        ver = str(put.details["version"])
        self.assertEqual(ver, "v1")
        self.assertEqual(put.details["sha256"], digest_bytes(body))

        listed = self.store.list_materials()
        self.assertTrue(listed.ok)
        self.assertEqual(listed.details["count"], 1)

        got = self.store.get_version(mid, ver, read_bytes=True)
        self.assertTrue(got.ok)
        self.assertEqual(got.details["data"], body)

        # Second version immutable
        put2 = self.store.put_bytes(data=b"v2 body", display_name="Hello", material_id=mid)
        self.assertTrue(put2.ok)
        self.assertEqual(put2.details["version"], "v2")
        old = self.store.get_version(mid, "v1", read_bytes=True)
        self.assertEqual(old.details["data"], body)

    def test_attach_ref_fail_closed_and_ok(self) -> None:
        put = self.store.put_bytes(data=b"ref-me", display_name="R")
        mid = str(put.details["material_id"])
        ver = str(put.details["version"])
        sha = str(put.details["sha256"])

        ok = self.store.attach_ref(
            workspace_id="workspace-001-a",
            material_id=mid,
            version=ver,
            purpose="evidence",
        )
        self.assertTrue(ok.ok, msg=ok.message)
        refs = self.store.list_refs("workspace-001-a")
        self.assertEqual(refs.details["count"], 1)
        row = refs.details["refs"][0]
        self.assertEqual(row["sha256"], sha)
        self.assertEqual(row["workspace_id"], "workspace-001-a")

        # Wrong workspace id in attach still uses param as authority; cross attach uses correct ws
        # Incomplete: material missing
        bad = self.store.attach_ref(workspace_id="workspace-001-a", material_id="no-such-mat")
        self.assertFalse(bad.ok)

    def test_delete_requires_ref_check_and_confirmation(self) -> None:
        put = self.store.put_bytes(data=b"to-delete", display_name="D")
        mid = str(put.details["material_id"])
        self.store.attach_ref(workspace_id="workspace-001-a", material_id=mid)

        # Unconfirmed with active refs
        blocked = self.store.delete_material(mid, user_confirmed=False)
        self.assertFalse(blocked.ok)
        self.assertEqual(blocked.code, ERR_SM_DELETE_WITHOUT_REF_CHECK)

        # Skip check explicitly fails SM-005
        skip = self.store.delete_material(
            mid, user_confirmed=True, force_skip_ref_check=True
        )
        self.assertFalse(skip.ok)
        self.assertEqual(skip.code, ERR_SM_DELETE_WITHOUT_REF_CHECK)

        # Confirmed after check
        done = self.store.delete_material(mid, user_confirmed=True)
        self.assertTrue(done.ok, msg=done.message)
        self.assertTrue(done.details.get("blobs_retained"))

        listed = self.store.list_materials()
        self.assertEqual(listed.details["count"], 0)
        # Blob still on disk for traceability
        got = self.store.get_version(mid, read_bytes=True)
        self.assertFalse(got.ok)  # soft-deleted hidden from get
        # History written
        self.assertTrue(self.store.history_path.is_file())

    def test_sm006_rejects_goal_path(self) -> None:
        goal_path = str((self.root / "workspace-001-a" / "GOAL-001-x" / "00-meta.md").resolve())
        r = self.store.assert_materials_path(goal_path)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_SM_GOAL_PATH_VIA_MATERIALS)

        # Path under materials root ok after ensure
        self.store.ensure_layout()
        sm_path = str((self.store.materials_root / "objects").resolve())
        ok = self.store.assert_materials_path(sm_path)
        self.assertTrue(ok.ok, msg=ok.message)

    def test_withdraw_ref(self) -> None:
        put = self.store.put_bytes(data=b"w", display_name="W")
        mid = str(put.details["material_id"])
        att = self.store.attach_ref(workspace_id="workspace-002-b", material_id=mid)
        rid = str(att.details["reference_id"])
        w = self.store.withdraw_ref("workspace-002-b", rid)
        self.assertTrue(w.ok)
        active = self.store.list_refs("workspace-002-b")
        self.assertEqual(active.details["count"], 0)
        all_refs = self.store.list_refs("workspace-002-b", include_withdrawn=True)
        self.assertEqual(all_refs.details["count"], 1)

    def test_missing_data_root(self) -> None:
        store = SharedMaterialsStore(Path("/nonexistent-ms-root-016"))
        r = store.put_bytes(data=b"x", display_name="x")
        self.assertFalse(r.ok)


if __name__ == "__main__":
    unittest.main()
