"""governance_root resolution tests (VP-004 R3).

Drives the REAL resolver (mcp/config.py) against temp repositories:
default ``docs``, project-config override, fail-closed on absolute paths and
``..`` escapes, invalid JSON, and frozen internal layout.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(REPO_ROOT / "skills"))

import mcp.config as config  # noqa: E402


class GovernanceRootConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()

    def _write_config(self, payload: object) -> None:
        (self.repo / config.CONFIG_FILENAME).write_text(
            json.dumps(payload), encoding="utf-8"
        )

    def test_default_is_docs(self) -> None:
        self.assertEqual(config.resolve_governance_root(self.repo), "docs")

    def test_project_config_overrides_root(self) -> None:
        self._write_config({"governance_root": "governance"})
        self.assertEqual(config.resolve_governance_root(self.repo), "governance")
        root_dir = config.governance_root_dir(self.repo)
        self.assertEqual(root_dir, (self.repo / "governance").resolve())
        # Explicit config wins over the on-disk file.
        self.assertEqual(
            config.resolve_governance_root(self.repo, {"governance_root": "alt"}),
            "alt",
        )

    def test_internal_layout_is_frozen_under_configured_root(self) -> None:
        """R3: only the root prefix changes; vision/workspace shape is fixed."""
        self._write_config({"governance_root": "governance"})
        root_dir = config.governance_root_dir(self.repo)
        (root_dir / "vision").mkdir(parents=True)
        (root_dir / "workspace-001-demo").mkdir()
        (root_dir / "goal-tree.md").write_text("# goal-tree\n", encoding="utf-8")
        goal_dir = root_dir / "workspace-001-demo" / "GOAL-001-demo-root"
        goal_dir.mkdir()
        for name in ("00-meta.md", "01-decision.md", "02-execution.md", "03-audit.md"):
            (goal_dir / name).write_text(f"# {name}\n", encoding="utf-8")
        for ledger in ("01-decision", "02-execution", "03-audit", "attachments"):
            (goal_dir / ledger).mkdir()
        # The resolved root carries the frozen layout.
        self.assertTrue((root_dir / "vision").is_dir())
        self.assertTrue((root_dir / "goal-tree.md").is_file())
        self.assertTrue((root_dir / "workspace-001-demo").is_dir())
        self.assertTrue(
            all((goal_dir / f"{n}.md").is_file() for n in ("00-meta", "01-decision", "02-execution", "03-audit"))
        )

    def test_configured_root_has_no_docs_fallback(self) -> None:
        """Negative: with a configured root, the resolver must NOT fall back to
        the default docs/ layout (single root, frozen layout)."""
        self._write_config({"governance_root": "governance"})
        self.assertEqual(config.resolve_governance_root(self.repo), "governance")
        # The default docs/ location is NOT used for governance paths.
        self.assertFalse((self.repo / "docs" / "goal-tree.md").exists())
        (self.repo / "docs").mkdir(exist_ok=True)
        (self.repo / "docs" / "goal-tree.md").write_text("# fake\n", encoding="utf-8")
        root_dir = config.governance_root_dir(self.repo)
        self.assertEqual(root_dir, (self.repo / "governance").resolve())
        self.assertNotEqual(root_dir, (self.repo / "docs").resolve())

    def test_absolute_path_fails_closed(self) -> None:
        for bad in ("/abs/path", "\\abs\\path", "C:/abs", "C:\\abs"):
            self._write_config({"governance_root": bad})
            with self.assertRaises(config.GovernanceRootError, msg=bad):
                config.resolve_governance_root(self.repo)

    def test_escape_fails_closed(self) -> None:
        for bad in ("../outside", "a/../../outside", "..", "a/.."):
            self._write_config({"governance_root": bad})
            with self.assertRaises(config.GovernanceRootError, msg=bad):
                config.resolve_governance_root(self.repo)

    def test_invalid_json_fails_closed(self) -> None:
        (self.repo / config.CONFIG_FILENAME).write_text("{not json", encoding="utf-8")
        with self.assertRaises(config.GovernanceRootError):
            config.resolve_governance_root(self.repo)

    def test_non_object_config_fails_closed(self) -> None:
        self._write_config(["docs"])
        with self.assertRaises(config.GovernanceRootError):
            config.resolve_governance_root(self.repo)

    def test_empty_root_name_fails_closed(self) -> None:
        self._write_config({"governance_root": ""})
        with self.assertRaises(config.GovernanceRootError):
            config.resolve_governance_root(self.repo)

    def test_schema_validates_pin_and_rejects_escape(self) -> None:
        from jsonschema import Draft202012Validator, FormatChecker

        schema = json.loads(
            (REPO_ROOT / "mcp" / "governance-root.schema.json").read_text(
                encoding="utf-8"
            )
        )
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertFalse(list(validator.iter_errors({"governance_root": "governance"})))
        self.assertFalse(list(validator.iter_errors({"governance_root": "docs"})))
        self.assertTrue(list(validator.iter_errors({"governance_root": "../outside"})))
        self.assertTrue(list(validator.iter_errors({"governance_root": "/abs"})))
        self.assertTrue(list(validator.iter_errors({"governance_root": "a/../b"})))
        self.assertTrue(list(validator.iter_errors({"governance_root": ""})))

    def test_doctor_reports_governance_root_error(self) -> None:
        """R-004: doctor surfaces a resolution failure as ok=False + error."""
        import mcp.doctor as doctor  # noqa: E402

        (self.repo / config.CONFIG_FILENAME).write_text("{bad json", encoding="utf-8")
        report = doctor.doctor(self.repo)
        self.assertFalse(report["ok"])
        self.assertTrue(report["governanceRootError"])
        self.assertIn("not valid JSON", report["governanceRootError"])
        self.assertTrue(
            any("governance_root" in issue for issue in report["issues"])
        )

    def test_doctor_uses_configured_root_for_contract_check(self) -> None:
        import mcp.doctor as doctor  # noqa: E402

        self._write_config({"governance_root": "governance"})
        contracts = self.repo / "governance" / "contracts"
        contracts.mkdir(parents=True)
        (contracts / "skills-consumer-contract.json").write_text("{}", encoding="utf-8")
        report = doctor.doctor(self.repo)
        self.assertEqual(report["governanceRoot"], "governance")
        self.assertTrue(report["contract"]["present"])
        self.assertIn("governance", report["contract"]["path"][0])


if __name__ == "__main__":
    unittest.main()
