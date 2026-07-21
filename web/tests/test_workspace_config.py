from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from services.workspace_config import (
    DOGFOOD_WORKSPACE,
    ENV_DEV_DOGFOOD,
    ENV_WORKSPACE_DIR,
    controlled_write_authorized,
    production_product_gates_open,
    resolve_workspace_config,
)


R004_FIXTURE = Path(__file__).parent / "fixtures" / "r004" / "workspace-ok"


class WorkspaceConfigTests(unittest.TestCase):
    def test_no_config_fails_closed_without_dogfood(self) -> None:
        cfg = resolve_workspace_config({})
        self.assertFalse(cfg.configured)
        self.assertIsNone(cfg.workspace_dir)
        self.assertIsNotNone(cfg.error)
        self.assertIn("No workspace configured", cfg.error or "")
        # Must not silently equal monorepo dogfood
        self.assertNotEqual(cfg.workspace_dir, DOGFOOD_WORKSPACE)

    def test_explicit_workspace_dir_loads_fixture(self) -> None:
        cfg = resolve_workspace_config({ENV_WORKSPACE_DIR: str(R004_FIXTURE)})
        self.assertTrue(cfg.is_ready)
        assert cfg.workspace_dir is not None
        self.assertEqual(cfg.workspace_dir.resolve(), R004_FIXTURE.resolve())
        self.assertTrue((cfg.workspace_dir / "goal-tree.md").is_file())
        self.assertTrue((cfg.workspace_dir / "GOAL-001-fixture-target").is_dir())

    def test_missing_explicit_path_errors(self) -> None:
        cfg = resolve_workspace_config({ENV_WORKSPACE_DIR: str(Path("does-not-exist-xyz"))})
        self.assertTrue(cfg.configured)
        self.assertFalse(cfg.is_ready)
        self.assertIn("does not exist", cfg.error or "")

    def test_dev_dogfood_opt_in(self) -> None:
        if not DOGFOOD_WORKSPACE.is_dir():
            self.skipTest("dogfood workspace not present in checkout")
        cfg = resolve_workspace_config({ENV_DEV_DOGFOOD: "true"})
        self.assertTrue(cfg.is_ready)
        assert cfg.workspace_dir is not None
        self.assertEqual(cfg.workspace_dir.resolve(), DOGFOOD_WORKSPACE.resolve())
        self.assertTrue(cfg.dev_dogfood)

    def test_production_write_default_requires_allow_flag(self) -> None:
        """After A-030: planning latch defaults closed; ALLOW remains second latch."""
        self.assertFalse(production_product_gates_open({}))
        self.assertFalse(
            controlled_write_authorized(
                test_authorized=False,
                environ={},
            )
        )
        self.assertTrue(
            controlled_write_authorized(
                test_authorized=True,
                environ={},
            )
        )
        # Explicit re-open of planning latch still blocks production path.
        self.assertFalse(
            controlled_write_authorized(
                test_authorized=False,
                environ={
                    "GOAL_GOVERNANCE_PRODUCT_GATES_OPEN": "true",
                    "GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE": "true",
                },
            )
        )

    def test_production_write_requires_closed_gates_and_flag(self) -> None:
        env = {
            "GOAL_GOVERNANCE_PRODUCT_GATES_OPEN": "false",
            "GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE": "true",
        }
        self.assertFalse(production_product_gates_open(env))
        self.assertTrue(controlled_write_authorized(test_authorized=False, environ=env))
        # Default planning latch closed + ALLOW true is enough.
        self.assertTrue(
            controlled_write_authorized(
                test_authorized=False,
                environ={"GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE": "true"},
            )
        )


if __name__ == "__main__":
    unittest.main()
