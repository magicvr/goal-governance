from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import unittest

from fastapi.testclient import TestClient

from main import _tree_diagnostic_count, app, get_goals_repository
from services.goals_repo import GoalsRepository
from services.models import FieldMismatch, IssueSeverity, TreeValidationReport, ValidationIssue


VALID_FIXTURE = Path(__file__).parent / "fixtures" / "valid-goals"


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
        self.assertIn("目标概览", response.text)
        self.assertIn("Root Goal", response.text)
        self.assertIn("Child Goal", response.text)
        self.assertIn("/goals/GOAL-001-root", response.text)
        self.assertIn("文档诊断", response.text)

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

    def list_goals(self) -> tuple[object, ...]:
        return self._results

    def build_tree_index(self, _results: tuple[object, ...]) -> object:
        return self._tree


if __name__ == "__main__":
    unittest.main()
