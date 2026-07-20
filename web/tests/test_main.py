from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import unittest

from fastapi.testclient import TestClient

from main import _tree_diagnostic_count, app, get_goals_repository
from services.goals_repo import GoalsRepository
from services.models import FieldMismatch, IssueSeverity, TreeValidationReport, ValidationIssue


VALID_FIXTURE = Path(__file__).parent / "fixtures" / "valid-goals"
R004_FIXTURE = Path(__file__).parent / "fixtures" / "r004" / "workspace-ok"


class GoalWebRoutesTests(unittest.TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_goals_repository] = lambda: GoalsRepository(VALID_FIXTURE)
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        self.client.close()

    def test_home_renders_real_goal_rows_and_diagnostics(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("工作区详情", response.text)
        self.assertIn("Root Goal", response.text)
        self.assertIn("Child Goal", response.text)
        self.assertIn("/goals/GOAL-001-root", response.text)
        self.assertIn("目标树", response.text)

    def test_unconfigured_workspace_fail_closed(self) -> None:
        app.dependency_overrides[get_goals_repository] = lambda: GoalsRepository.from_config({})
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("工作区未配置", response.text)
        self.assertIn("fail closed", response.text)
        self.assertNotIn("GOAL-001-main-vision", response.text)

    def test_health_reports_gate_state(self) -> None:
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["ok"])
        self.assertIn("controlled_write_enabled", payload)
        self.assertIn("product_gates_open", payload)

    def test_proposal_preview_on_fixture_workspace(self) -> None:
        app.dependency_overrides[get_goals_repository] = lambda: GoalsRepository(R004_FIXTURE)
        response = self.client.post(
            "/goals/GOAL-001-fixture-target/proposal",
            data={
                "content": "Preview only fact",
                "source_statement": "web form",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("提案 digest", response.text)
        self.assertIn("02-execution.md", response.text)

    def test_decide_http_rejects_when_product_gates_open(self) -> None:
        """HTTP decide path must surface ERR_PRODUCT_GATE_OPEN (GOAL-012 A-001 F-004)."""
        import re
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace-ok"
            shutil.copytree(R004_FIXTURE, root)
            app.dependency_overrides[get_goals_repository] = lambda: GoalsRepository(root)
            proposal = self.client.post(
                "/goals/GOAL-001-fixture-target/proposal",
                data={
                    "content": "Must not commit under open product gates",
                    "source_statement": "http decide gate test",
                },
            )
            self.assertEqual(proposal.status_code, 200)
            match = re.search(r"sha256:[0-9a-f]{64}", proposal.text)
            self.assertIsNotNone(match, "proposal digest missing from preview HTML")
            digest = match.group(0)
            exec_before = (root / "GOAL-001-fixture-target" / "02-execution.md").read_text(
                encoding="utf-8"
            )
            decide = self.client.post(
                "/goals/GOAL-001-fixture-target/decide",
                data={"proposal_digest": digest, "action": "affirm"},
            )
            self.assertEqual(decide.status_code, 200)
            self.assertIn("rejected", decide.text)
            self.assertIn("ERR_PRODUCT_GATE_OPEN", decide.text)
            exec_after = (root / "GOAL-001-fixture-target" / "02-execution.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(exec_before, exec_after)

    def test_goal_detail_renders_decision_execution_and_audit(self) -> None:
        response = self.client.get("/goals/GOAL-002-child")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Child Goal", response.text)
        self.assertIn("Child decision", response.text)
        self.assertIn("Done", response.text)
        self.assertIn("阶段范围通过", response.text)
        self.assertIn('data-tab="audit"', response.text)

    def test_unknown_goal_returns_not_found(self) -> None:
        response = self.client.get("/goals/GOAL-999-missing")

        self.assertEqual(response.status_code, 404)

    def test_legacy_module_routes_redirect_to_goal_workspace(self) -> None:
        for path in ("/decision", "/execution", "/audit"):
            response = self.client.get(path, follow_redirects=False)

            self.assertEqual(response.status_code, 307)
            self.assertTrue(response.headers["location"].endswith("/"))

    def test_home_renders_duplicate_number_diagnostic(self) -> None:
        repository = GoalsRepository(VALID_FIXTURE)
        results = repository.list_goals()
        tree = repository.build_tree_index(results)
        report = replace(
            tree.validation_report,
            duplicate_number_ids={
                2: ("GOAL-002-child", "GOAL-002-duplicate"),
            },
        )
        app.dependency_overrides[get_goals_repository] = lambda: _StaticRepository(
            results, replace(tree, tree_drift=True, validation_report=report)
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("GOAL-002", response.text)
        self.assertIn("编号重复", response.text)

    def test_tree_diagnostic_count_covers_all_report_categories(self) -> None:
        report = TreeValidationReport(
            missing_in_tree=("GOAL-006-missing",),
            missing_on_disk=("GOAL-007-removed",),
            field_mismatches=(
                FieldMismatch(
                    goal_id="GOAL-001-root",
                    field="title",
                    disk_value="Root Goal",
                    tree_value="Old Root Goal",
                ),
            ),
            orphan_ids=("GOAL-008-orphan",),
            cycle_ids=("GOAL-009-cycle",),
            duplicate_number_ids={10: ("GOAL-010-first", "GOAL-010-second")},
            issues=(
                ValidationIssue(
                    code="tree.parse_error",
                    severity=IssueSeverity.WARNING,
                    path=Path("goal-tree.md"),
                    message="Tree projection could not be parsed.",
                ),
            ),
        )

        self.assertEqual(_tree_diagnostic_count(report), 7)


class _StaticRepository:
    def __init__(self, results: tuple[object, ...], tree: object) -> None:
        self._results = results
        self._tree = tree
        self.goals_dir = VALID_FIXTURE
        self.config_error = None
        self.config_source = "explicit"

    @property
    def is_configured(self) -> bool:
        return True

    def list_goals(self) -> tuple[object, ...]:
        return self._results

    def build_tree_index(self, _results: tuple[object, ...]) -> object:
        return self._tree


if __name__ == "__main__":
    unittest.main()
