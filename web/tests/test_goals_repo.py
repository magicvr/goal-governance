from __future__ import annotations

from datetime import date
from pathlib import Path
import tempfile
import unittest

from services.goals_repo import (
    DOGFOOD_WORKSPACE_DIR,
    GoalRecoveryRequiredError,
    GoalValidationError,
    GoalWriteError,
    GoalsRepository,
)
from services.models import AuditConclusionState, GoalStatus, IssueSeverity
from services.workspace_config import ENV_WORKSPACE_DIR


FIXTURES = Path(__file__).parent / "fixtures"
VALID_FIXTURE = FIXTURES / "valid-goals"


class GoalsRepositoryTests(unittest.TestCase):
    def test_dogfood_path_exists_but_is_not_silent_default(self) -> None:
        self.assertEqual(DOGFOOD_WORKSPACE_DIR.name, "workspace-001-goal-governance")
        self.assertTrue((DOGFOOD_WORKSPACE_DIR / "workspace.md").is_file())
        self.assertTrue((DOGFOOD_WORKSPACE_DIR / "goal-tree.md").is_file())
        unconfigured = GoalsRepository.from_config({})
        self.assertFalse(unconfigured.is_configured)
        self.assertNotEqual(
            unconfigured.goals_dir.resolve() if unconfigured.goals_dir.exists() else unconfigured.goals_dir,
            DOGFOOD_WORKSPACE_DIR.resolve(),
        )

    def test_from_config_uses_explicit_workspace(self) -> None:
        repo = GoalsRepository.from_config({ENV_WORKSPACE_DIR: str(VALID_FIXTURE)})
        self.assertTrue(repo.is_configured)
        self.assertEqual(repo.goals_dir.resolve(), VALID_FIXTURE.resolve())

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

    def test_create_and_update_keep_tree_and_unknown_metadata_in_sync(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_complete_goal(root / "GOAL-001-root", "GOAL-001-root", None)
            repo = GoalsRepository(root)

            created = repo.create_goal(
                "Child Goal",
                "child-goal",
                "GOAL-001-root",
                status=GoalStatus.ACTIVE,
                progress="0%",
                body_markdown="## 概述\nCreated from the service.\n",
                section_bodies={"decision": "## D-001 · Start\n"},
                on_date=date(2026, 7, 20),
            )
            self.assertIsNotNone(created.goal)
            assert created.goal is not None
            self.assertEqual(created.goal.id, "GOAL-002-child-goal")
            created_dir = root / "GOAL-002-child-goal"
            self.assertTrue((created_dir / "attachments").is_dir())
            self.assertTrue(all((created_dir / name).is_file() for name in (
                "00-meta.md",
                "01-decision.md",
                "02-execution.md",
                "03-audit.md",
            )))
            self.assertTrue(all((created_dir / name).is_dir() for name in (
                "01-decision",
                "02-execution",
                "03-audit",
            )))

            meta_path = created_dir / "00-meta.md"
            meta_path.write_text(
                meta_path.read_text(encoding="utf-8").replace(
                    "version: 0.1.0\n",
                    "version: 0.1.0\ncustom_key: keep-me\n",
                ),
                encoding="utf-8",
            )
            updated = repo.update_goal(
                "GOAL-002-child-goal",
                title="Renamed Child",
                status=GoalStatus.DONE,
                progress="100%",
                body_markdown="## 概述\nUpdated through the service.\n",
                section_bodies={"execution": "### 2026-07-21 · Finished\n"},
                on_date=date(2026, 7, 21),
            )

            self.assertIsNotNone(updated.goal)
            assert updated.goal is not None
            self.assertEqual(updated.goal.title, "Renamed Child")
            self.assertEqual(updated.goal.status, GoalStatus.DONE)
            self.assertEqual(updated.goal.progress, "100%")
            self.assertEqual(updated.goal.meta.extra["custom_key"], "keep-me")
            self.assertIn("Updated through the service.", updated.goal.meta.body_markdown)
            self.assertIn("Finished", updated.goal.execution.body_markdown)
            self.assertEqual(updated.goal.decision.metadata["status"], "done")
            self.assertEqual(updated.goal.audit.metadata["status"], "done")
            self.assertEqual(updated.goal.decision.metadata["parent"], "GOAL-001-root")

            tree = repo.build_tree_index(repo.list_goals())
            self.assertFalse(tree.tree_drift)
            self.assertEqual(tree.root_ids, ("GOAL-001-root",))
            self.assertEqual(tree.nodes[0].children_ids, ("GOAL-002-child-goal",))
            tree_text = (root / "goal-tree.md").read_text(encoding="utf-8")
            self.assertIn("Renamed Child", tree_text)
            self.assertIn("100%", tree_text)
            self.assertIn("updated: 2026-07-21", tree_text)
            self.assertIn("GOAL-001-root · GOAL-001-root [active]", tree_text)
            self.assertIn(
                "└── GOAL-002-child-goal · Renamed Child [done 100%]",
                tree_text,
            )

    def test_ledger_directories_merge_with_legacy_inline_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            goal = root / "GOAL-001-root"
            _write_complete_goal(goal, "GOAL-001-root", None)
            (goal / "01-decision").mkdir()
            (goal / "01-decision" / "D-002-directory.md").write_text(
                "---\nid: GOAL-001-root\ndoc: decision-entry\nversion: 0.1.0\n---\n\n## D-002 · Directory decision\n",
                encoding="utf-8",
            )
            (goal / "02-execution").mkdir()
            (goal / "02-execution" / "E-001-directory.md").write_text(
                "---\nid: GOAL-001-root\ndoc: execution-entry\nversion: 0.1.0\n---\n\n### 2026-07-20 · Directory fact\n",
                encoding="utf-8",
            )
            (goal / "03-audit").mkdir()
            (goal / "03-audit" / "A-001-directory.md").write_text(
                "---\nid: GOAL-001-root\ndoc: audit-entry\nversion: 0.1.0\n---\n\n## 最终结论\n",
                encoding="utf-8",
            )

            result = GoalsRepository(root).get_goal("GOAL-001-root")
            self.assertIsNotNone(result.goal)
            assert result.goal is not None
            self.assertEqual(
                [entry.id for entry in result.goal.decision.entries],
                ["D-001", "D-002"],
            )
            self.assertEqual(
                [entry.title for entry in result.goal.execution.entries],
                ["Fact", "Directory fact"],
            )
            self.assertEqual(result.goal.audit.conclusion_state, AuditConclusionState.FINAL)
            self.assertNotIn("invalid_ledger_entry_name", _codes(result))

    def test_create_first_goal_as_the_only_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = GoalsRepository(root)

            created = repo.create_goal(
                "Root Goal",
                "root-goal",
                None,
                on_date=date(2026, 7, 20),
            )

            self.assertIsNotNone(created.goal)
            assert created.goal is not None
            self.assertEqual(created.goal.id, "GOAL-001-root-goal")
            self.assertIsNone(created.goal.parent_id)
            self.assertFalse(repo.build_tree_index(repo.list_goals()).tree_drift)
            with self.assertRaises(GoalValidationError):
                repo.create_goal("Second Root", "second-root", None)

    def test_section_only_update_leaves_goal_tree_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_complete_goal(root / "GOAL-001-root", "GOAL-001-root", None)
            repo = GoalsRepository(root)
            repo.repair_goal_tree(on_date=date(2026, 7, 20))
            tree_before = (root / "goal-tree.md").read_bytes()

            result = repo.update_goal(
                "GOAL-001-root",
                section_bodies={"audit": "### 结论\n阶段性记录。\n"},
                on_date=date(2026, 7, 21),
            )

            self.assertIsNotNone(result.goal)
            self.assertEqual((root / "goal-tree.md").read_bytes(), tree_before)
            assert result.goal is not None
            self.assertIn("阶段性记录", result.goal.audit.body_markdown)

    def test_write_validation_rejects_invalid_parent_cycle_and_slug_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_complete_goal(root / "GOAL-001-root", "GOAL-001-root", None)
            repo = GoalsRepository(root)
            repo.create_goal("Child", "child", "GOAL-001-root", on_date=date(2026, 7, 20))
            snapshot = _snapshot(root)

            with self.assertRaises(GoalValidationError):
                repo.update_goal("GOAL-002-child", parent_id="GOAL-999-missing")
            with self.assertRaises(GoalValidationError):
                repo.update_goal("GOAL-001-root", parent_id="GOAL-002-child")
            with self.assertRaises(GoalValidationError):
                repo.create_goal("Bad", "not a slug", "GOAL-001-root")

            self.assertEqual(snapshot, _snapshot(root))

    def test_tree_replacement_failure_compensates_all_written_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_complete_goal(root / "GOAL-001-root", "GOAL-001-root", None)
            repo = GoalsRepository(root)
            repo.repair_goal_tree(on_date=date(2026, 7, 20))
            snapshot = _snapshot(root)
            replace_file = repo._replace_file

            def fail_tree_replacement(source: Path, destination: Path) -> None:
                if destination == repo.goal_tree_file and source.name.endswith(".tmp"):
                    raise OSError("simulated goal-tree replacement failure")
                replace_file(source, destination)

            repo._replace_file = fail_tree_replacement  # type: ignore[method-assign]
            with self.assertRaises(GoalWriteError):
                repo.update_goal("GOAL-001-root", title="Changed Root")

            self.assertEqual(snapshot, _snapshot(root))
            self.assertFalse(repo.recovery_record_file.exists())

    def test_goal_file_replacement_failure_leaves_no_partial_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_complete_goal(root / "GOAL-001-root", "GOAL-001-root", None)
            repo = GoalsRepository(root)
            repo.repair_goal_tree(on_date=date(2026, 7, 20))
            snapshot = _snapshot(root)
            replace_file = repo._replace_file

            def fail_meta_replacement(source: Path, destination: Path) -> None:
                if destination.name == "00-meta.md" and source.name.endswith(".tmp"):
                    raise OSError("simulated goal metadata replacement failure")
                replace_file(source, destination)

            repo._replace_file = fail_meta_replacement  # type: ignore[method-assign]
            with self.assertRaises(GoalWriteError):
                repo.update_goal("GOAL-001-root", progress="50%")

            self.assertEqual(snapshot, _snapshot(root))
            self.assertFalse(repo.recovery_record_file.exists())

    def test_failed_compensation_blocks_writes_until_repair(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_complete_goal(root / "GOAL-001-root", "GOAL-001-root", None)
            repo = GoalsRepository(root)
            repo.repair_goal_tree(on_date=date(2026, 7, 20))
            replace_file = repo._replace_file

            def fail_commit_and_meta_restore(source: Path, destination: Path) -> None:
                if destination == repo.goal_tree_file and source.name.endswith(".tmp"):
                    raise OSError("simulated goal-tree replacement failure")
                if destination.name == "00-meta.md" and source.name.endswith(".bak"):
                    raise OSError("simulated compensation failure")
                replace_file(source, destination)

            repo._replace_file = fail_commit_and_meta_restore  # type: ignore[method-assign]
            with self.assertRaises(GoalRecoveryRequiredError):
                repo.update_goal("GOAL-001-root", title="Interrupted Root")
            self.assertTrue(repo.recovery_record_file.exists())

            with self.assertRaises(GoalRecoveryRequiredError):
                repo.update_goal("GOAL-001-root", progress="50%")

            repo._replace_file = replace_file  # type: ignore[method-assign]
            repaired = repo.repair_goal_tree(on_date=date(2026, 7, 21))
            self.assertFalse(repo.recovery_record_file.exists())
            self.assertFalse(repaired.tree_drift)
            self.assertEqual(repo.get_goal("GOAL-001-root").goal.title, "GOAL-001-root")


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
