from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import mimetypes
import re
from typing import Iterable

from services.models import (
    AttachmentRef,
    AuditDoc,
    DecisionDoc,
    FieldMismatch,
    Goal,
    GoalLoadResult,
    GoalTreeIndex,
    GoalTreeNode,
    IssueSeverity,
    ExecutionDoc,
    TreeValidationReport,
    ValidationIssue,
)
from services.parse_md import (
    GOAL_ID_RE,
    extract_success_criteria,
    extract_summary,
    has_roadmap,
    parse_audit_conclusion_state,
    parse_decision_entries,
    parse_execution_entries,
    parse_goal_meta,
    parse_section_document,
)

DEFAULT_GOALS_DIR = Path(__file__).resolve().parents[2] / "docs" / "goals"
_GOAL_NUMBER_RE = re.compile(r"^GOAL-(\d+)-")
_TREE_HEADER_RE = re.compile(r"^\|\s*ID\s*\|", re.IGNORECASE)


class GoalsRepository:
    def __init__(self, goals_dir: Path | None = None) -> None:
        self.goals_dir = Path(goals_dir) if goals_dir is not None else DEFAULT_GOALS_DIR
        self._resolved_goals_dir = self.goals_dir.resolve()
        self.goal_tree_file = self.goals_dir / "goal-tree.md"

    def list_goals(self) -> tuple[GoalLoadResult, ...]:
        if not self.goals_dir.is_dir():
            return (
                GoalLoadResult(
                    goal=None,
                    path=self.goals_dir,
                    raw_markdown=None,
                    issues=(
                        self._issue(
                            "goals_dir_not_found",
                            IssueSeverity.ERROR,
                            self.goals_dir,
                            "Goals directory does not exist.",
                        ),
                    ),
                ),
            )

        candidates = [
            path
            for path in self.goals_dir.iterdir()
            if path.name.startswith("GOAL-") and (path.is_dir() or path.is_symlink())
        ]
        return tuple(self._load_goal_dir(path) for path in sorted(candidates, key=lambda p: _goal_sort_key(p.name)))

    def get_goal(self, goal_id: str) -> GoalLoadResult:
        if not GOAL_ID_RE.fullmatch(goal_id):
            return GoalLoadResult(
                goal=None,
                path=self.goals_dir,
                raw_markdown=None,
                issues=(
                    self._issue(
                        "invalid_goal_id",
                        IssueSeverity.ERROR,
                        self.goals_dir,
                        f"Goal id is not canonical: {goal_id!r}",
                    ),
                ),
            )

        goal_dir = self.goals_dir / goal_id
        containment_issue = self._containment_issue(goal_dir, IssueSeverity.ERROR)
        if containment_issue:
            return GoalLoadResult(None, goal_dir, None, (containment_issue,))
        if not goal_dir.is_dir():
            return GoalLoadResult(
                goal=None,
                path=goal_dir,
                raw_markdown=None,
                issues=(
                    self._issue(
                        "goal_not_found",
                        IssueSeverity.ERROR,
                        goal_dir,
                        f"Goal directory does not exist: {goal_id}",
                    ),
                ),
            )
        return self._load_goal_dir(goal_dir)

    def build_tree_index(
        self,
        results: Iterable[GoalLoadResult],
    ) -> GoalTreeIndex:
        valid_goals = {
            result.goal.id: result.goal
            for result in results
            if result.goal is not None
        }
        sorted_ids = tuple(sorted(valid_goals, key=_goal_sort_key))

        duplicate_numbers: dict[int, tuple[str, ...]] = {}
        ids_by_number: dict[int, list[str]] = defaultdict(list)
        for goal_id in sorted_ids:
            ids_by_number[_goal_number(goal_id)].append(goal_id)
        for number, goal_ids in ids_by_number.items():
            if len(goal_ids) > 1:
                duplicate_numbers[number] = tuple(sorted(goal_ids))

        orphan_ids = tuple(
            sorted(
                (
                    goal_id
                    for goal_id, goal in valid_goals.items()
                    if goal.parent_id is not None and goal.parent_id not in valid_goals
                ),
                key=_goal_sort_key,
            )
        )
        cycle_ids = tuple(sorted(_find_cycle_ids(valid_goals), key=_goal_sort_key))
        cycle_set = set(cycle_ids)
        depth_by_id = {
            goal_id: _goal_depth(goal_id, valid_goals, cycle_set)
            for goal_id in sorted_ids
        }

        children_by_id: dict[str, list[str]] = defaultdict(list)
        for goal_id, goal in valid_goals.items():
            if (
                goal.parent_id in valid_goals
                and depth_by_id[goal_id] is not None
                and depth_by_id[goal.parent_id] is not None
            ):
                children_by_id[goal.parent_id].append(goal_id)

        nodes = tuple(
            GoalTreeNode(
                id=goal_id,
                title=valid_goals[goal_id].title,
                parent_id=valid_goals[goal_id].parent_id,
                status=valid_goals[goal_id].status,
                progress=valid_goals[goal_id].progress,
                path=Path(goal_id),
                depth=depth_by_id[goal_id],
                children_ids=tuple(sorted(children_by_id[goal_id], key=_goal_sort_key)),
            )
            for goal_id in sorted_ids
        )
        root_ids = tuple(
            goal_id
            for goal_id in sorted_ids
            if valid_goals[goal_id].parent_id is None and depth_by_id[goal_id] == 0
        )

        projection, projection_issues, projection_loaded = self._load_tree_projection()
        valid_id_set = set(valid_goals)
        projection_id_set = set(projection)
        disk_candidate_ids = self._disk_candidate_ids()
        missing_in_tree = tuple(sorted(valid_id_set - projection_id_set, key=_goal_sort_key))
        missing_on_disk = tuple(sorted(projection_id_set - disk_candidate_ids, key=_goal_sort_key))

        mismatches: list[FieldMismatch] = []
        for goal_id in sorted(valid_id_set & projection_id_set, key=_goal_sort_key):
            goal = valid_goals[goal_id]
            tree_row = projection[goal_id]
            comparisons = (
                ("title", goal.title, tree_row["title"]),
                ("parent_id", goal.parent_id, tree_row["parent_id"]),
                ("status", goal.status.value, tree_row["status"]),
                ("progress", goal.progress, tree_row["progress"]),
            )
            for field_name, disk_value, tree_value in comparisons:
                if disk_value != tree_value:
                    mismatches.append(
                        FieldMismatch(
                            goal_id=goal_id,
                            field=field_name,
                            disk_value=disk_value,
                            tree_value=tree_value,
                        )
                    )

        report = TreeValidationReport(
            missing_in_tree=missing_in_tree,
            missing_on_disk=missing_on_disk,
            field_mismatches=tuple(mismatches),
            orphan_ids=orphan_ids,
            cycle_ids=cycle_ids,
            duplicate_number_ids=duplicate_numbers,
            issues=tuple(projection_issues),
        )
        tree_drift = any(
            (
                report.missing_in_tree,
                report.missing_on_disk,
                report.field_mismatches,
                report.orphan_ids,
                report.cycle_ids,
                report.duplicate_number_ids,
                report.issues,
            )
        )
        return GoalTreeIndex(
            nodes=nodes,
            root_ids=root_ids,
            generated_at=datetime.now(timezone.utc),
            source="merged" if projection_loaded else "directory_scan",
            tree_drift=tree_drift,
            validation_report=report,
        )

    def _load_goal_dir(self, goal_dir: Path) -> GoalLoadResult:
        issues: list[ValidationIssue] = []
        containment_issue = self._containment_issue(goal_dir, IssueSeverity.ERROR)
        if containment_issue:
            return GoalLoadResult(None, goal_dir, None, (containment_issue,))

        meta_path = goal_dir / "00-meta.md"
        meta_text, read_issue = self._read_text(meta_path, IssueSeverity.ERROR)
        if read_issue:
            return GoalLoadResult(None, goal_dir, None, (read_issue,))

        meta, meta_body, meta_issues = parse_goal_meta(meta_text, meta_path, goal_dir.name)
        issues.extend(meta_issues)
        if meta is None:
            return GoalLoadResult(None, goal_dir, meta_text, tuple(issues))

        decision, decision_issues = self._load_decision(goal_dir / "01-decision.md")
        execution, execution_issues = self._load_execution(goal_dir / "02-execution.md")
        audit, audit_issues = self._load_audit(goal_dir / "03-audit.md")
        attachments, attachment_issues = self._load_attachments(goal_dir)
        issues.extend(decision_issues)
        issues.extend(execution_issues)
        issues.extend(audit_issues)
        issues.extend(attachment_issues)

        goal = Goal(
            folder_name=goal_dir.name,
            path=goal_dir,
            meta=meta,
            summary=extract_summary(meta_body),
            success_criteria=extract_success_criteria(meta_body),
            roadmap_present=has_roadmap(meta_body, decision.body_markdown),
            decision=decision,
            execution=execution,
            audit=audit,
            attachments=attachments,
        )
        return GoalLoadResult(goal, goal_dir, meta_text, tuple(issues))

    def _load_decision(self, path: Path) -> tuple[DecisionDoc, tuple[ValidationIssue, ...]]:
        text, issue = self._read_text(path, IssueSeverity.WARNING)
        if issue:
            return DecisionDoc(body_markdown=""), (issue,)
        parsed = parse_section_document(text, path)
        return (
            DecisionDoc(
                body_markdown=parsed.body_markdown,
                entries=parse_decision_entries(parsed.body_markdown),
                metadata=parsed.metadata,
            ),
            parsed.issues,
        )

    def _load_execution(self, path: Path) -> tuple[ExecutionDoc, tuple[ValidationIssue, ...]]:
        text, issue = self._read_text(path, IssueSeverity.WARNING)
        if issue:
            return ExecutionDoc(body_markdown=""), (issue,)
        parsed = parse_section_document(text, path)
        return (
            ExecutionDoc(
                body_markdown=parsed.body_markdown,
                entries=parse_execution_entries(parsed.body_markdown),
                metadata=parsed.metadata,
            ),
            parsed.issues,
        )

    def _load_audit(self, path: Path) -> tuple[AuditDoc, tuple[ValidationIssue, ...]]:
        text, issue = self._read_text(path, IssueSeverity.WARNING)
        if issue:
            return AuditDoc(body_markdown=""), (issue,)
        parsed = parse_section_document(text, path)
        return (
            AuditDoc(
                body_markdown=parsed.body_markdown,
                conclusion_state=parse_audit_conclusion_state(
                    parsed.body_markdown,
                    parsed.metadata,
                ),
                metadata=parsed.metadata,
            ),
            parsed.issues,
        )

    def _load_attachments(
        self,
        goal_dir: Path,
    ) -> tuple[tuple[AttachmentRef, ...], tuple[ValidationIssue, ...]]:
        attachments_dir = goal_dir / "attachments"
        containment_issue = self._containment_issue(attachments_dir, IssueSeverity.WARNING)
        if containment_issue:
            return (), (containment_issue,)
        if not attachments_dir.is_dir():
            return (), (
                self._issue(
                    "missing_required_file",
                    IssueSeverity.WARNING,
                    attachments_dir,
                    "Missing attachments directory.",
                ),
            )

        refs: list[AttachmentRef] = []
        issues: list[ValidationIssue] = []
        for path in sorted(attachments_dir.iterdir(), key=lambda candidate: candidate.name):
            if path.name.startswith(".") or path.is_dir():
                continue
            issue = self._containment_issue(path, IssueSeverity.WARNING)
            if issue:
                issues.append(issue)
                continue
            if not path.is_file():
                continue
            refs.append(
                AttachmentRef(
                    name=path.name,
                    relative_path=path.relative_to(goal_dir),
                    media_type=mimetypes.guess_type(path.name)[0],
                )
            )
        return tuple(refs), tuple(issues)

    def _read_text(
        self,
        path: Path,
        severity: IssueSeverity,
    ) -> tuple[str | None, ValidationIssue | None]:
        containment_issue = self._containment_issue(path, severity)
        if containment_issue:
            return None, containment_issue
        if not path.is_file():
            return None, self._issue(
                "missing_required_file",
                severity,
                path,
                f"Missing required file: {path.name}",
            )
        try:
            return path.read_text(encoding="utf-8"), None
        except (OSError, UnicodeError) as exc:
            return None, self._issue(
                "read_error",
                severity,
                path,
                f"Unable to read file: {exc}",
            )

    def _containment_issue(
        self,
        path: Path,
        severity: IssueSeverity,
    ) -> ValidationIssue | None:
        try:
            path.resolve().relative_to(self._resolved_goals_dir)
        except (OSError, ValueError):
            return self._issue(
                "path_escapes_goals_dir",
                severity,
                path,
                "Resolved path escapes the configured goals directory.",
            )
        return None

    def _load_tree_projection(
        self,
    ) -> tuple[dict[str, dict[str, str | None]], list[ValidationIssue], bool]:
        text, issue = self._read_text(self.goal_tree_file, IssueSeverity.WARNING)
        if issue:
            code = "goal_tree_not_found" if issue.code == "missing_required_file" else issue.code
            return {}, [
                ValidationIssue(code, issue.severity, issue.path, issue.message)
            ], False

        lines = text.splitlines()
        header_index = next((index for index, line in enumerate(lines) if _TREE_HEADER_RE.match(line)), None)
        if header_index is None:
            return {}, [
                self._issue(
                    "invalid_goal_tree",
                    IssueSeverity.WARNING,
                    self.goal_tree_file,
                    "Goal tree status table header was not found.",
                )
            ], True

        projection: dict[str, dict[str, str | None]] = {}
        issues: list[ValidationIssue] = []
        for line in lines[header_index + 2:]:
            if not line.lstrip().startswith("|"):
                break
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 6:
                issues.append(
                    self._issue(
                        "invalid_goal_tree",
                        IssueSeverity.WARNING,
                        self.goal_tree_file,
                        f"Malformed goal-tree row: {line}",
                    )
                )
                continue
            goal_id, title, parent, status, progress, _path = cells[:6]
            if not GOAL_ID_RE.fullmatch(goal_id):
                issues.append(
                    self._issue(
                        "invalid_goal_tree",
                        IssueSeverity.WARNING,
                        self.goal_tree_file,
                        f"Non-canonical goal id in tree table: {goal_id!r}",
                    )
                )
                continue
            projection[goal_id] = {
                "title": title,
                "parent_id": None if parent in {"", "—", "-", "null", "None"} else parent,
                "status": status,
                "progress": None if progress in {"", "—", "-", "null", "None"} else progress,
            }
        return projection, issues, True

    def _disk_candidate_ids(self) -> set[str]:
        if not self.goals_dir.is_dir():
            return set()
        return {
            path.name
            for path in self.goals_dir.iterdir()
            if GOAL_ID_RE.fullmatch(path.name) and (path.is_dir() or path.is_symlink())
        }

    @staticmethod
    def _issue(
        code: str,
        severity: IssueSeverity,
        path: Path,
        message: str,
    ) -> ValidationIssue:
        return ValidationIssue(code=code, severity=severity, path=path, message=message)


def list_goals(goals_dir: Path | None = None) -> tuple[GoalLoadResult, ...]:
    return GoalsRepository(goals_dir).list_goals()


def get_goal(goal_id: str, goals_dir: Path | None = None) -> GoalLoadResult:
    return GoalsRepository(goals_dir).get_goal(goal_id)


def _goal_number(goal_id: str) -> int:
    match = _GOAL_NUMBER_RE.match(goal_id)
    return int(match.group(1)) if match else 10**9


def _goal_sort_key(goal_id: str) -> tuple[int, str]:
    return _goal_number(goal_id), goal_id


def _find_cycle_ids(goals: dict[str, Goal]) -> set[str]:
    cycle_ids: set[str] = set()
    for start_id in goals:
        chain: list[str] = []
        positions: dict[str, int] = {}
        current_id: str | None = start_id
        while current_id is not None and current_id in goals and current_id not in positions:
            positions[current_id] = len(chain)
            chain.append(current_id)
            current_id = goals[current_id].parent_id
        if current_id is not None and current_id in positions:
            cycle_ids.update(chain[positions[current_id]:])
    return cycle_ids


def _goal_depth(
    goal_id: str,
    goals: dict[str, Goal],
    cycle_ids: set[str],
) -> int | None:
    if goal_id in cycle_ids:
        return None
    chain: list[str] = []
    current_id: str | None = goal_id
    seen: set[str] = set()
    while current_id is not None:
        if current_id in cycle_ids or current_id in seen or current_id not in goals:
            return None
        seen.add(current_id)
        chain.append(current_id)
        current_id = goals[current_id].parent_id
    return len(chain) - 1
