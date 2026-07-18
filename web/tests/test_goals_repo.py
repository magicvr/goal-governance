from __future__ import annotations

from pathlib import Path
import os
import shutil
import tempfile
import unittest

from services.goals_repo import GoalsRepository
from services.models import AuditConclusionState, GoalStatus, IssueSeverity


FIXTURES = Path(__file__).parent / "fixtures"
VALID_FIXTURE = FIXTURES / "valid-goals"


class GoalsRepositoryTests(unittest.TestCase):
    def test_valid_list_get_parses_documents_and_attachments(self) -> None:
        repo = GoalsRepository(VALID_FIXTURE)

        results = repo.list_goals()
        self.assertEqual([result.goal.id for result in results if result.goal], [
            "GOAL-001-root",
            "GOAL-002-child",
        ])
        root = repo.get_goal("GOAL-001-root")
        self.assertIsNotNone(root.goal)
        assert root.goal is not None
        self.assertEqual(root.goal.meta.extra["custom_key"], "keep-me")
        self.assertEqual(root.goal.success_criteria, ("Parse the root", "Load the sections"))
        self.assertTrue(root.goal.roadmap_present)
        self.assertEqual([entry.id for entry in root.goal.decision.entries], ["D-002", "D-001"])
        self.assertEqual([entry.title for entry in root.goal.execution.entries], ["Started", "Continued"])
        self.assertEqual(root.goal.audit.conclusion_state, AuditConclusionState.NONE)
        self.assertEqual([ref.name for ref in root.goal.attachments], ["note.txt"])

        child = repo.get_goal("GOAL-002-child")
        self.assertIsNotNone(child.goal)
        assert child.goal is not None
        self.assertEqual(child.goal.audit.conclusion_state, AuditConclusionState.PROVISIONAL)
        self.assertEqual(child.goal.attachments, ())

        tree = repo.build_tree_index(results)
        self.assertEqual(tree.root_ids, ("GOAL-001-root",))
        self.assertFalse(tree.tree_drift)
        self.assertEqual(tree.validation_report.field_mismatches, ())
        self.assertEqual(tree.nodes[0].children_ids, ("GOAL-002-child",))
        self.assertEqual(
            [node.path for node in tree.nodes],
            [Path("GOAL-001-root"), Path("GOAL-002-child")],
        )

    def test_invalid_meta_and_partial_sections_are_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad = root / "GOAL-003-bad"
            bad.mkdir()
            bad_meta = bad / "00-meta.md"
            bad_meta.write_text("plain text without frontmatter\n", encoding="utf-8")

            missing_version = root / "GOAL-004-no-version"
            missing_version.mkdir()
            missing_version_meta = missing_version / "00-meta.md"
            missing_version_meta.write_text(_meta("GOAL-004-no-version", "GOAL-001-root", version=None), encoding="utf-8")

            partial = root / "GOAL-005-partial"
            partial.mkdir()
            (partial / "00-meta.md").write_text(_meta("GOAL-005-partial", "GOAL-001-root"), encoding="utf-8")
            (partial / "02-execution.md").write_text("body without frontmatter\n", encoding="utf-8")

            repo = GoalsRepository(root)
            results = {result.path.name: result for result in repo.list_goals()}

            self.assertIsNone(results["GOAL-003-bad"].goal)
            self.assertIn("invalid_frontmatter", _codes(results["GOAL-003-bad"]))
            self.assertIn("plain text", results["GOAL-003-bad"].raw_markdown or "")

            self.assertIsNone(results["GOAL-004-no-version"].goal)
            self.assertIn("missing_version", _codes(results["GOAL-004-no-version"]))
            self.assertEqual(missing_version_meta.read_text(encoding="utf-8"), _meta("GOAL-004-no-version", "GOAL-001-root", version=None))

            partial_result = results["GOAL-005-partial"]
            self.assertIsNotNone(partial_result.goal)
            self.assertIn("missing_required_file", _codes(partial_result))
            self.assertIn("invalid_frontmatter", _codes(partial_result))
            assert partial_result.goal is not None
            self.assertIn("body without frontmatter", partial_result.goal.execution.body_markdown)

    def test_hard_meta_validation_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = {
                "GOAL-006-bad-status": (
                    _meta("GOAL-006-bad-status", "GOAL-001-root").replace("status: active", "status: archived"),
                    "invalid_status",
                ),
                "GOAL-007-bad-date": (
                    _meta("GOAL-007-bad-date", "GOAL-001-root").replace("created: 2026-07-19", "created: yesterday"),
                    "invalid_date",
                ),
                "GOAL-008-bad-parent": (
                    _meta("GOAL-008-bad-parent", "GOAL-001-root").replace("parent: GOAL-001-root", "parent: ../root"),
                    "invalid_parent",
                ),
                "GOAL-009-folder": (
                    _meta("GOAL-009-other", "GOAL-001-root"),
                    "id_folder_mismatch",
                ),
            }
            for folder_name, (text, expected_code) in cases.items():
                goal_dir = root / folder_name
                goal_dir.mkdir()
                (goal_dir / "00-meta.md").write_text(text, encoding="utf-8")

            missing_meta = root / "GOAL-011-no-meta"
            missing_meta.mkdir()

            results = {result.path.name: result for result in GoalsRepository(root).list_goals()}
            for folder_name, (_text, expected_code) in cases.items():
                with self.subTest(folder_name=folder_name):
                    self.assertIsNone(results[folder_name].goal)
                    self.assertIn(expected_code, _codes(results[folder_name]))
            self.assertIn("missing_required_file", _codes(results["GOAL-011-no-meta"]))

    def test_invalid_id_not_found_and_read_is_side_effect_free(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            goal = root / "GOAL-001-root"
            _write_complete_goal(goal, "GOAL-001-root", None)
            repo = GoalsRepository(root)
            snapshot = _snapshot(root)

            invalid = repo.get_goal("../GOAL-001-root")
            self.assertIsNone(invalid.goal)
            self.assertIn("invalid_goal_id", _codes(invalid))

            missing = repo.get_goal("GOAL-999-missing")
            self.assertIsNone(missing.goal)
            self.assertIn("goal_not_found", _codes(missing))

            repo.list_goals()
            repo.get_goal("GOAL-001-root")
            self.assertEqual(snapshot, _snapshot(root))

    def test_tree_diagnostics_and_stable_duplicate_sorting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_complete_goal(root / "GOAL-001-root", "GOAL-001-root", None)
            _write_complete_goal(root / "GOAL-002-orphan", "GOAL-002-orphan", "GOAL-999-missing")
            _write_complete_goal(root / "GOAL-003-cycle-a", "GOAL-003-cycle-a", "GOAL-004-cycle-b")
            _write_complete_goal(root / "GOAL-004-cycle-b", "GOAL-004-cycle-b", "GOAL-003-cycle-a")
            _write_complete_goal(root / "GOAL-010-b", "GOAL-010-b", "GOAL-001-root")
            _write_complete_goal(root / "GOAL-010-a", "GOAL-010-a", "GOAL-001-root")
            (root / "goal-tree.md").write_text(
                _tree_table([
                    ("GOAL-001-root", "Different Root", "—", "active", "进行中"),
                    ("GOAL-010-a", "GOAL-010-a", "GOAL-999-missing", "done", "—"),
                    ("GOAL-999-extra", "Extra", "—", "done", "100%"),
                ]),
                encoding="utf-8",
            )

            repo = GoalsRepository(root)
            tree = repo.build_tree_index(repo.list_goals())
            report = tree.validation_report
            self.assertEqual(report.orphan_ids, ("GOAL-002-orphan",))
            self.assertEqual(set(report.cycle_ids), {"GOAL-003-cycle-a", "GOAL-004-cycle-b"})
            self.assertEqual(report.duplicate_number_ids[10], ("GOAL-010-a", "GOAL-010-b"))
            self.assertIn("GOAL-002-orphan", report.missing_in_tree)
            self.assertIn("GOAL-999-extra", report.missing_on_disk)
            self.assertTrue(any(m.field == "title" for m in report.field_mismatches))
            self.assertTrue(any(m.field == "progress" for m in report.field_mismatches))
            self.assertTrue(tree.tree_drift)

            ordered = [node.id for node in tree.nodes]
            self.assertEqual(
                ordered,
                [
                    "GOAL-001-root",
                    "GOAL-002-orphan",
                    "GOAL-003-cycle-a",
                    "GOAL-004-cycle-b",
                    "GOAL-010-a",
                    "GOAL-010-b",
                ],
            )
            for node in tree.nodes:
                if node.id in {"GOAL-002-orphan", "GOAL-003-cycle-a", "GOAL-004-cycle-b"}:
                    self.assertIsNone(node.depth)

    def test_escaping_symlink_is_rejected_when_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "goals"
            outside = Path(tmp) / "outside"
            root.mkdir()
            outside.mkdir()
            _write_complete_goal(outside / "GOAL-006-escape", "GOAL-006-escape", None)
            link = root / "GOAL-006-escape"
            try:
                link.symlink_to(outside / "GOAL-006-escape", target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")

            result = GoalsRepository(root).get_goal("GOAL-006-escape")
            self.assertIsNone(result.goal)
            self.assertIn("path_escapes_goals_dir", _codes(result))

    def test_missing_version_and_negative_audit_do_not_become_final(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            goal = root / "GOAL-001-root"
            _write_complete_goal(goal, "GOAL-001-root", None)
            (goal / "03-audit.md").write_text(
                "---\nid: GOAL-001-root\ndoc: audit\nversion: 0.1.0\n---\n\n不写最终结论。\n",
                encoding="utf-8",
            )
            result = GoalsRepository(root).get_goal("GOAL-001-root")
            self.assertIsNotNone(result.goal)
            assert result.goal is not None
            self.assertEqual(result.goal.audit.conclusion_state, AuditConclusionState.NONE)

            (goal / "01-decision.md").write_text(
                "---\nid: GOAL-001-root\ndoc: decision\n---\n\n## D-001 · Missing version\n",
                encoding="utf-8",
            )
            result = GoalsRepository(root).get_goal("GOAL-001-root")
            self.assertIn("missing_version", _codes(result))
            self.assertIsNotNone(result.goal)


def _meta(goal_id: str, parent: str | None, *, version: str | None = "0.1.0") -> str:
    parent_value = "null" if parent is None else parent
    version_line = "" if version is None else f"version: {version}\n"
    return (
        "---\n"
        f"id: {goal_id}\n"
        f"title: {goal_id}\n"
        "status: active\n"
        f"parent: {parent_value}\n"
        "created: 2026-07-19\n"
        "updated: 2026-07-19\n"
        f"{version_line}"
        "---\n\n## 概述\nFixture goal.\n"
    )


def _write_complete_goal(path: Path, goal_id: str, parent: str | None) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "00-meta.md").write_text(_meta(goal_id, parent), encoding="utf-8")
    (path / "01-decision.md").write_text(
        f"---\nid: {goal_id}\ndoc: decision\nversion: 0.1.0\n---\n\n## D-001 · Decision\n",
        encoding="utf-8",
    )
    (path / "02-execution.md").write_text(
        f"---\nid: {goal_id}\ndoc: execution\nversion: 0.1.0\n---\n\n### 2026-07-19 · Fact\n",
        encoding="utf-8",
    )
    (path / "03-audit.md").write_text(
        f"---\nid: {goal_id}\ndoc: audit\nversion: 0.1.0\n---\n\n### 结论\n",
        encoding="utf-8",
    )
    (path / "attachments").mkdir()


def _tree_table(rows: list[tuple[str, str, str, str, str]]) -> str:
    lines = [
        "# Goal Tree",
        "",
        "| ID | 标题 | Parent | Status | Progress | 路径 |",
        "|----|------|--------|--------|----------|------|",
    ]
    lines.extend(f"| {goal_id} | {title} | {parent} | {status} | {progress} | path |" for goal_id, title, parent, status, progress in rows)
    return "\n".join(lines) + "\n"


def _codes(result) -> set[str]:
    return {issue.code for issue in result.issues}


def _snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    snapshot = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            snapshot[str(path.relative_to(root))] = (path.read_bytes(), path.stat().st_mtime_ns)
    return snapshot


if __name__ == "__main__":
    unittest.main()
