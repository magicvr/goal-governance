from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone
import json
from pathlib import Path
import mimetypes
import os
import re
from typing import Iterable, Mapping
from uuid import uuid4

import frontmatter
import yaml

from services.models import (
    AttachmentRef,
    AuditDoc,
    DecisionDoc,
    FieldMismatch,
    Goal,
    GoalLoadResult,
    GoalStatus,
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
    parse_frontmatter,
    parse_goal_meta,
    parse_section_document,
)

DEFAULT_WORKSPACE_DIR = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "workspace-001-goal-governance"
)
# The repository API keeps its historical goals_dir parameter name; the scope is now a workspace root.
DEFAULT_GOALS_DIR = DEFAULT_WORKSPACE_DIR
_GOAL_NUMBER_RE = re.compile(r"^GOAL-(\d+)-")
_TREE_HEADER_RE = re.compile(r"^\|\s*ID\s*\|", re.IGNORECASE)
_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SECTION_FILES = {
    "decision": "01-decision.md",
    "execution": "02-execution.md",
    "audit": "03-audit.md",
}
_SECTION_DOC_TYPES = {
    "decision": "decision",
    "execution": "execution",
    "audit": "audit",
}
_RECOVERY_RECORD_NAME = ".goal-write-recovery.json"
_UNSET = object()


class GoalWriteError(RuntimeError):
    """A write could not complete without leaving a recoverable state."""


class GoalValidationError(GoalWriteError):
    """A proposed document change violates the goal-storage contract."""


class GoalRecoveryRequiredError(GoalWriteError):
    """A prior failed transaction must be repaired before ordinary writes."""


@dataclass(frozen=True)
class _TreeRecord:
    id: str
    title: str
    status: GoalStatus
    parent_id: str | None
    progress: str | None


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

    def create_goal(
        self,
        title: str,
        slug: str,
        parent_id: str | None,
        *,
        status: GoalStatus | str = GoalStatus.DRAFT,
        progress: str | None = None,
        body_markdown: str = "",
        section_bodies: Mapping[str, str] | None = None,
        on_date: date | None = None,
    ) -> GoalLoadResult:
        """Create a complete goal folder and its synchronized tree projection."""
        self._assert_writable()
        write_date = self._resolve_write_date(on_date)
        normalized_title = self._normalize_title(title)
        normalized_slug = self._normalize_slug(slug)
        normalized_status = self._coerce_status(status)
        normalized_progress = self._normalize_progress(progress)
        normalized_sections = self._normalize_section_bodies(section_bodies)
        goals = self._goals_for_write()
        records = self._tree_records(goals)

        number = self._next_goal_number()
        if number > 999:
            raise GoalValidationError("Goal numbering has reached the three-digit limit.")
        goal_id = f"GOAL-{number:03d}-{normalized_slug}"
        goal_dir = self.goals_dir / goal_id
        self._assert_write_path(goal_dir)
        if goal_dir.exists() or goal_id in records:
            raise GoalValidationError(f"Goal already exists: {goal_id}")

        if records and parent_id is None:
            raise GoalValidationError("Only the first goal may have a null parent.")
        normalized_parent = self._normalize_parent(parent_id)
        if normalized_parent is not None and normalized_parent not in records:
            raise GoalValidationError(f"Parent goal does not exist: {normalized_parent}")

        records[goal_id] = _TreeRecord(
            id=goal_id,
            title=normalized_title,
            status=normalized_status,
            parent_id=normalized_parent,
            progress=normalized_progress,
        )
        self._validate_tree_records(records)

        writes = {
            goal_dir / "00-meta.md": self._new_goal_meta_document(
                goal_id,
                normalized_title,
                normalized_status,
                normalized_parent,
                normalized_progress,
                body_markdown,
                write_date,
            ),
            self.goal_tree_file: self._render_goal_tree(records, write_date),
        }
        for section_name, filename in _SECTION_FILES.items():
            writes[goal_dir / filename] = self._new_section_document(
                goal_id,
                section_name,
                normalized_status,
                normalized_parent,
                normalized_sections.get(section_name, ""),
                write_date,
            )

        self._transactional_write(
            writes,
            created_directories=(goal_dir, goal_dir / "attachments"),
        )
        return self._written_goal(goal_id)

    def update_goal(
        self,
        goal_id: str,
        *,
        title: str | object = _UNSET,
        status: GoalStatus | str | object = _UNSET,
        parent_id: str | None | object = _UNSET,
        progress: str | None | object = _UNSET,
        body_markdown: str | object = _UNSET,
        section_bodies: Mapping[str, str] | None = None,
        on_date: date | None = None,
    ) -> GoalLoadResult:
        """Update one goal while synchronizing its tree projection when needed."""
        self._assert_writable()
        if not GOAL_ID_RE.fullmatch(goal_id):
            raise GoalValidationError(f"Goal id is not canonical: {goal_id!r}")
        normalized_sections = self._normalize_section_bodies(section_bodies)
        if all(value is _UNSET for value in (title, status, parent_id, progress, body_markdown)) and not normalized_sections:
            raise GoalValidationError("No goal fields or section bodies were supplied for update.")

        write_date = self._resolve_write_date(on_date)
        goals = self._goals_for_write()
        current = goals.get(goal_id)
        if current is None:
            raise GoalValidationError(f"Goal directory does not exist: {goal_id}")

        records = self._tree_records(goals)
        current_record = records[goal_id]
        updated_record = _TreeRecord(
            id=goal_id,
            title=current_record.title if title is _UNSET else self._normalize_title(title),
            status=current_record.status if status is _UNSET else self._coerce_status(status),
            parent_id=current_record.parent_id if parent_id is _UNSET else self._normalize_parent(parent_id),
            progress=current_record.progress if progress is _UNSET else self._normalize_progress(progress),
        )
        records[goal_id] = updated_record
        self._validate_tree_records(records)

        meta_path = current.path / "00-meta.md"
        meta_metadata, existing_meta_body = self._load_document_for_write(meta_path)
        meta_body = existing_meta_body if body_markdown is _UNSET else self._require_markdown_body(body_markdown)
        self._apply_meta_fields(meta_metadata, updated_record, current.created, write_date)
        writes: dict[Path, str] = {
            meta_path: self._serialize_document(meta_metadata, meta_body),
        }

        for section_name, section_body in normalized_sections.items():
            section_path = current.path / _SECTION_FILES[section_name]
            section_metadata, _existing_body = self._load_document_for_write(
                section_path,
                allow_missing=True,
            )
            self._apply_section_fields(
                section_metadata,
                goal_id,
                section_name,
                updated_record,
                current.created,
                write_date,
            )
            writes[section_path] = self._serialize_document(section_metadata, section_body)

        if (
            updated_record.status != current_record.status
            or updated_record.parent_id != current_record.parent_id
        ):
            for section_name, filename in _SECTION_FILES.items():
                if section_name in normalized_sections:
                    continue
                section_path = current.path / filename
                section_metadata, existing_section_body = self._load_document_for_write(
                    section_path,
                    allow_missing=True,
                )
                self._apply_section_fields(
                    section_metadata,
                    goal_id,
                    section_name,
                    updated_record,
                    current.created,
                    write_date,
                )
                writes[section_path] = self._serialize_document(
                    section_metadata,
                    existing_section_body,
                )

        if updated_record != current_record:
            writes[self.goal_tree_file] = self._render_goal_tree(records, write_date)

        self._transactional_write(writes)
        return self._written_goal(goal_id)

    def repair_goal_tree(self, *, on_date: date | None = None) -> GoalTreeIndex:
        """Restore a failed transaction when possible, then rebuild goal-tree from meta."""
        recovery_record = self._load_recovery_record()
        if recovery_record is not None:
            self._restore_recovery_record(recovery_record)

        write_date = self._resolve_write_date(on_date)
        goals = self._goals_for_write()
        records = self._tree_records(goals)
        self._validate_tree_records(records)
        self._transactional_write(
            {self.goal_tree_file: self._render_goal_tree(records, write_date)},
        )
        return self.build_tree_index(self.list_goals())

    @property
    def recovery_record_file(self) -> Path:
        return self.goals_dir / _RECOVERY_RECORD_NAME

    def _written_goal(self, goal_id: str) -> GoalLoadResult:
        result = self.get_goal(goal_id)
        if result.goal is None:
            raise GoalWriteError(
                f"Write completed but the resulting goal cannot be read: {goal_id}"
            )
        return result

    def _goals_for_write(self) -> dict[str, Goal]:
        results = self.list_goals()
        invalid_results = [
            result
            for result in results
            if result.goal is None
            or any(issue.severity is IssueSeverity.ERROR for issue in result.issues)
        ]
        if invalid_results:
            details = "; ".join(
                f"{result.path.name}: {', '.join(issue.code for issue in result.issues)}"
                for result in invalid_results
            )
            raise GoalValidationError(
                "Cannot write while goal documents have validation errors: " + details
            )
        return {result.goal.id: result.goal for result in results if result.goal is not None}

    @staticmethod
    def _tree_records(goals: Mapping[str, Goal]) -> dict[str, _TreeRecord]:
        return {
            goal_id: _TreeRecord(
                id=goal.id,
                title=goal.title,
                status=goal.status,
                parent_id=goal.parent_id,
                progress=goal.progress,
            )
            for goal_id, goal in goals.items()
        }

    def _next_goal_number(self) -> int:
        if not self.goals_dir.is_dir():
            raise GoalValidationError("Goals directory does not exist.")
        numbers = [
            _goal_number(path.name)
            for path in self.goals_dir.iterdir()
            if _GOAL_NUMBER_RE.match(path.name)
        ]
        return max(numbers, default=0) + 1

    @staticmethod
    def _normalize_title(value: object) -> str:
        if not isinstance(value, str):
            raise GoalValidationError("Goal title must be a string.")
        title = value.strip()
        if not title:
            raise GoalValidationError("Goal title must not be empty.")
        if "\n" in title or "\r" in title or "|" in title:
            raise GoalValidationError("Goal title cannot contain a newline or Markdown table separator.")
        return title

    @staticmethod
    def _normalize_slug(value: object) -> str:
        if not isinstance(value, str) or not _SLUG_RE.fullmatch(value):
            raise GoalValidationError(
                "Goal slug must use lowercase letters, digits, and single hyphens."
            )
        return value

    @staticmethod
    def _normalize_parent(value: object) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str) or not GOAL_ID_RE.fullmatch(value):
            raise GoalValidationError("Parent id must be null or a canonical goal id.")
        return value

    @staticmethod
    def _coerce_status(value: object) -> GoalStatus:
        if isinstance(value, GoalStatus):
            return value
        if isinstance(value, str):
            try:
                return GoalStatus(value.strip())
            except ValueError:
                pass
        raise GoalValidationError(f"Unsupported goal status: {value!r}")

    @staticmethod
    def _normalize_progress(value: object) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise GoalValidationError("Goal progress must be a string or null.")
        progress = value.strip()
        if not progress:
            return None
        if "\n" in progress or "\r" in progress or "|" in progress:
            raise GoalValidationError(
                "Goal progress cannot contain a newline or Markdown table separator."
            )
        return progress

    @staticmethod
    def _require_markdown_body(value: object) -> str:
        if not isinstance(value, str):
            raise GoalValidationError("Document body must be Markdown text.")
        return value

    @staticmethod
    def _normalize_section_bodies(
        section_bodies: Mapping[str, str] | None,
    ) -> dict[str, str]:
        if section_bodies is None:
            return {}
        if not isinstance(section_bodies, Mapping):
            raise GoalValidationError("Section bodies must be a mapping.")
        normalized: dict[str, str] = {}
        for section_name, body in section_bodies.items():
            if section_name not in _SECTION_FILES:
                raise GoalValidationError(f"Unsupported section: {section_name!r}")
            if not isinstance(body, str):
                raise GoalValidationError(f"Section body for {section_name!r} must be text.")
            normalized[section_name] = body
        return normalized

    @staticmethod
    def _resolve_write_date(value: date | None) -> date:
        if value is None:
            return date.today()
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        raise GoalValidationError("Write date must be a date.")

    @staticmethod
    def _apply_meta_fields(
        metadata: dict[str, object],
        record: _TreeRecord,
        created: date,
        updated: date,
    ) -> None:
        metadata["id"] = record.id
        metadata["title"] = record.title
        metadata["status"] = record.status.value
        metadata["parent"] = record.parent_id
        metadata["created"] = created
        metadata["updated"] = updated
        metadata.setdefault("version", "0.1.0")
        if record.progress is None:
            metadata.pop("progress", None)
        else:
            metadata["progress"] = record.progress

    @staticmethod
    def _apply_section_fields(
        metadata: dict[str, object],
        goal_id: str,
        section_name: str,
        record: _TreeRecord,
        created: date,
        updated: date,
    ) -> None:
        metadata["id"] = goal_id
        metadata["doc"] = _SECTION_DOC_TYPES[section_name]
        metadata["status"] = record.status.value
        metadata["parent"] = record.parent_id
        metadata.setdefault("created", created)
        metadata["updated"] = updated
        metadata.setdefault("version", "0.1.0")

    def _new_goal_meta_document(
        self,
        goal_id: str,
        title: str,
        status: GoalStatus,
        parent_id: str | None,
        progress: str | None,
        body_markdown: str,
        write_date: date,
    ) -> str:
        record = _TreeRecord(goal_id, title, status, parent_id, progress)
        metadata: dict[str, object] = {}
        self._apply_meta_fields(metadata, record, write_date, write_date)
        body = body_markdown or f"# {goal_id} · {title}\n\n## 概述\n"
        return self._serialize_document(metadata, self._require_markdown_body(body))

    def _new_section_document(
        self,
        goal_id: str,
        section_name: str,
        status: GoalStatus,
        parent_id: str | None,
        body_markdown: str,
        write_date: date,
    ) -> str:
        record = _TreeRecord(goal_id, goal_id, status, parent_id, None)
        metadata: dict[str, object] = {}
        self._apply_section_fields(
            metadata,
            goal_id,
            section_name,
            record,
            write_date,
            write_date,
        )
        default_titles = {
            "decision": "决策记录",
            "execution": "执行记录",
            "audit": "审计",
        }
        body = body_markdown or f"# {default_titles[section_name]} · {goal_id}\n"
        return self._serialize_document(metadata, self._require_markdown_body(body))

    def _load_document_for_write(
        self,
        path: Path,
        *,
        allow_missing: bool = False,
        allow_plain: bool = False,
    ) -> tuple[dict[str, object], str]:
        text, issue = self._read_text(path, IssueSeverity.ERROR)
        if issue is not None:
            if allow_missing and issue.code == "missing_required_file":
                return {}, ""
            raise GoalValidationError(issue.message)

        assert text is not None
        parsed = parse_frontmatter(text, path, severity=IssueSeverity.ERROR)
        if parsed.issues:
            if allow_plain and not text.lstrip("\ufeff").startswith("---"):
                return {}, text
            raise GoalValidationError(
                f"Cannot rewrite invalid frontmatter in {path.name}: {parsed.issues[0].message}"
            )
        try:
            post = frontmatter.loads(text.lstrip("\ufeff"))
        except Exception as exc:
            raise GoalValidationError(
                f"Cannot parse frontmatter in {path.name}: {exc}"
            ) from exc
        return dict(post.metadata), post.content

    @staticmethod
    def _serialize_document(metadata: Mapping[str, object], body_markdown: str) -> str:
        yaml_body = yaml.safe_dump(
            dict(metadata),
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=1000,
        ).strip()
        header = "---\n"
        if yaml_body:
            header += f"{yaml_body}\n"
        header += "---"
        body = body_markdown.lstrip("\r\n")
        if not body:
            return f"{header}\n"
        rendered = f"{header}\n\n{body}"
        return rendered if rendered.endswith("\n") else f"{rendered}\n"

    def _validate_tree_records(self, records: Mapping[str, _TreeRecord]) -> None:
        if not records:
            return

        numbers: dict[int, list[str]] = defaultdict(list)
        root_ids: list[str] = []
        for goal_id, record in records.items():
            if not GOAL_ID_RE.fullmatch(goal_id):
                raise GoalValidationError(f"Goal id is not canonical: {goal_id!r}")
            if record.id != goal_id:
                raise GoalValidationError(f"Goal id does not match its tree record: {goal_id!r}")
            self._normalize_title(record.title)
            self._normalize_progress(record.progress)
            numbers[_goal_number(goal_id)].append(goal_id)
            if record.parent_id is None:
                root_ids.append(goal_id)
            elif record.parent_id not in records:
                raise GoalValidationError(
                    f"Parent goal does not exist: {record.parent_id} for {goal_id}"
                )

        duplicate_numbers = [
            number for number, goal_ids in numbers.items() if len(goal_ids) > 1
        ]
        if duplicate_numbers:
            raise GoalValidationError(
                "Duplicate goal numbers are not writable: "
                + ", ".join(str(number) for number in sorted(duplicate_numbers))
            )
        if len(root_ids) != 1:
            raise GoalValidationError("The goal tree must contain exactly one root goal.")
        if not root_ids[0].startswith("GOAL-001-"):
            raise GoalValidationError("The root goal must use GOAL-001.")

        cycle_ids = _find_record_cycle_ids(records)
        if cycle_ids:
            raise GoalValidationError(
                "Parent links form a cycle: " + ", ".join(sorted(cycle_ids, key=_goal_sort_key))
            )

    def _render_goal_tree(
        self,
        records: Mapping[str, _TreeRecord],
        write_date: date,
    ) -> str:
        metadata, body = self._load_document_for_write(
            self.goal_tree_file,
            allow_missing=True,
            allow_plain=True,
        )
        metadata.setdefault("title", "Goal Tree")
        metadata.setdefault("status", "active")
        metadata.setdefault("created", write_date)
        metadata["updated"] = write_date
        metadata.setdefault("parent", None)
        metadata.setdefault("version", "0.1.0")
        rendered_body = self._replace_goal_tree_body(body, records)
        return self._serialize_document(metadata, rendered_body)

    def _replace_goal_tree_body(
        self,
        body_markdown: str,
        records: Mapping[str, _TreeRecord],
    ) -> str:
        lines = body_markdown.splitlines()
        tree_lines = self._tree_lines(records)
        table_lines = self._tree_table_lines(records)

        tree_heading = next(
            (index for index, line in enumerate(lines) if line.strip() == "## 树状结构"),
            None,
        )
        if tree_heading is not None:
            fence_start = next(
                (
                    index
                    for index in range(tree_heading + 1, len(lines))
                    if lines[index].strip() == "```text"
                ),
                None,
            )
            if fence_start is not None:
                fence_end = next(
                    (
                        index
                        for index in range(fence_start + 1, len(lines))
                        if lines[index].strip() == "```"
                    ),
                    None,
                )
                if fence_end is not None:
                    lines[fence_start + 1:fence_end] = tree_lines
                else:
                    lines[fence_start + 1:fence_start + 1] = tree_lines + ["```"]
            else:
                lines[tree_heading + 1:tree_heading + 1] = ["", "```text", *tree_lines, "```"]
        else:
            table_start = next(
                (index for index, line in enumerate(lines) if _TREE_HEADER_RE.match(line)),
                len(lines),
            )
            lines[table_start:table_start] = [
                "## 树状结构",
                "",
                "```text",
                *tree_lines,
                "```",
                "",
            ]

        table_start = next(
            (index for index, line in enumerate(lines) if _TREE_HEADER_RE.match(line)),
            None,
        )
        if table_start is None:
            if lines and lines[-1].strip():
                lines.append("")
            lines.extend(["## 状态总览", "", *table_lines])
        else:
            table_end = table_start
            while table_end < len(lines) and lines[table_end].lstrip().startswith("|"):
                table_end += 1
            lines[table_start:table_end] = table_lines
        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _tree_table_lines(records: Mapping[str, _TreeRecord]) -> list[str]:
        lines = [
            "| ID | 标题 | Parent | Status | Progress | 路径 |",
            "|----|------|--------|--------|----------|------|",
        ]
        for goal_id in sorted(records, key=_goal_sort_key):
            record = records[goal_id]
            parent = "—" if record.parent_id is None else record.parent_id
            progress = "—" if record.progress is None else record.progress
            lines.append(
                f"| {record.id} | {record.title} | {parent} | {record.status.value} | {progress} | [{record.id}/]({record.id}/) |"
            )
        return lines

    @staticmethod
    def _tree_lines(records: Mapping[str, _TreeRecord]) -> list[str]:
        children: dict[str, list[str]] = defaultdict(list)
        roots: list[str] = []
        for goal_id, record in records.items():
            if record.parent_id is None:
                roots.append(goal_id)
            else:
                children[record.parent_id].append(goal_id)
        for child_ids in children.values():
            child_ids.sort(key=_goal_sort_key)

        lines: list[str] = []

        def render(goal_id: str, prefix: str, is_last: bool, is_root: bool = False) -> None:
            record = records[goal_id]
            suffix = f"{record.status.value}"
            if record.progress is not None:
                suffix += f" {record.progress}"
            label = f"{record.id} · {record.title} [{suffix}]"
            if is_root:
                lines.append(label)
            else:
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}{label}")
            descendants = children.get(goal_id, [])
            for index, child_id in enumerate(descendants):
                child_prefix = prefix if is_root else prefix + ("    " if is_last else "│   ")
                render(child_id, child_prefix, index == len(descendants) - 1)

        for index, root_id in enumerate(sorted(roots, key=_goal_sort_key)):
            render(root_id, "", index == len(roots) - 1, is_root=True)
        return lines

    def _assert_writable(self) -> None:
        if self.recovery_record_file.exists():
            raise GoalRecoveryRequiredError(
                f"Recovery record exists: {self.recovery_record_file}. Run repair_goal_tree() first."
            )

    def _assert_write_path(self, path: Path) -> None:
        containment_issue = self._containment_issue(path, IssueSeverity.ERROR)
        if containment_issue is not None:
            raise GoalValidationError(containment_issue.message)

    def _transactional_write(
        self,
        writes: Mapping[Path, str],
        *,
        created_directories: tuple[Path, ...] = (),
    ) -> None:
        self._assert_writable()
        if not writes:
            return

        ordered_targets = sorted(
            writes,
            key=lambda path: (path == self.goal_tree_file, str(path)),
        )
        for target in ordered_targets:
            self._assert_write_path(target)
            if not isinstance(writes[target], str):
                raise GoalValidationError(f"Write payload for {target.name} must be text.")

        created: list[Path] = []
        temp_paths: dict[Path, Path] = {}
        backups: dict[Path, Path] = {}
        applied: list[Path] = []
        transaction_id = uuid4().hex
        try:
            created = self._prepare_directories(created_directories)
            for target in ordered_targets:
                temp_path = target.parent / f".{target.name}.{transaction_id}.tmp"
                self._write_temp_file(temp_path, writes[target])
                temp_paths[target] = temp_path

            for target in ordered_targets:
                if target.exists():
                    backup_path = target.parent / f".{target.name}.{transaction_id}.bak"
                    self._replace_file(target, backup_path)
                    backups[target] = backup_path
                self._replace_file(temp_paths[target], target)
                applied.append(target)
        except Exception as exc:
            rollback_succeeded = self._rollback_transaction(
                temp_paths,
                backups,
                applied,
                created,
            )
            if not rollback_succeeded:
                try:
                    self._write_recovery_record(backups, ordered_targets, created)
                except Exception as record_exc:
                    raise GoalRecoveryRequiredError(
                        "Write failed and rollback could not complete; recovery record creation also failed: "
                        f"{record_exc}"
                    ) from exc
                raise GoalRecoveryRequiredError(
                    "Write failed and rollback could not complete. Run repair_goal_tree() before writing again."
                ) from exc
            raise GoalWriteError(f"Unable to commit goal write: {exc}") from exc
        else:
            self._cleanup_paths(backups.values())
            self._cleanup_paths(temp_paths.values())

    def _prepare_directories(self, directories: Iterable[Path]) -> list[Path]:
        created: list[Path] = []
        for directory in sorted(set(directories), key=lambda path: len(path.parts)):
            self._assert_write_path(directory)
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=False)
                created.append(directory)
        return created

    @staticmethod
    def _write_temp_file(path: Path, text: str) -> None:
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())

    @staticmethod
    def _replace_file(source: Path, destination: Path) -> None:
        os.replace(source, destination)

    def _rollback_transaction(
        self,
        temp_paths: Mapping[Path, Path],
        backups: Mapping[Path, Path],
        applied: Iterable[Path],
        created_directories: Iterable[Path],
    ) -> bool:
        try:
            for target, backup_path in reversed(tuple(backups.items())):
                if backup_path.exists():
                    self._replace_file(backup_path, target)
            for target in reversed(tuple(applied)):
                if target not in backups and target.exists():
                    target.unlink()
            self._cleanup_paths(temp_paths.values())
            self._remove_empty_directories(created_directories)
            return True
        except OSError:
            return False

    @staticmethod
    def _cleanup_paths(paths: Iterable[Path]) -> None:
        for path in paths:
            try:
                if path.exists():
                    path.unlink()
            except OSError:
                pass

    @staticmethod
    def _remove_empty_directories(directories: Iterable[Path]) -> None:
        for directory in sorted(set(directories), key=lambda path: len(path.parts), reverse=True):
            try:
                directory.rmdir()
            except OSError:
                pass

    def _write_recovery_record(
        self,
        backups: Mapping[Path, Path],
        targets: Iterable[Path],
        created_directories: Iterable[Path],
    ) -> None:
        payload = {
            "version": 1,
            "backups": [
                {
                    "target": str(target.relative_to(self.goals_dir)),
                    "backup": str(backup_path.relative_to(self.goals_dir)),
                }
                for target, backup_path in backups.items()
            ],
            "new_targets": [
                str(target.relative_to(self.goals_dir))
                for target in targets
                if target not in backups
            ],
            "created_directories": [
                str(directory.relative_to(self.goals_dir))
                for directory in created_directories
            ],
        }
        temporary_record = self.goals_dir / f".{_RECOVERY_RECORD_NAME}.{uuid4().hex}.tmp"
        temporary_record.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary_record, self.recovery_record_file)

    def _load_recovery_record(self) -> dict[str, object] | None:
        if not self.recovery_record_file.exists():
            return None
        try:
            payload = json.loads(self.recovery_record_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise GoalRecoveryRequiredError(
                f"Cannot read recovery record: {self.recovery_record_file}"
            ) from exc
        if not isinstance(payload, dict):
            raise GoalRecoveryRequiredError("Recovery record has an invalid shape.")
        return payload

    def _restore_recovery_record(self, payload: Mapping[str, object]) -> None:
        backups = payload.get("backups")
        new_targets = payload.get("new_targets")
        created_directories = payload.get("created_directories")
        if not isinstance(backups, list) or not isinstance(new_targets, list) or not isinstance(created_directories, list):
            raise GoalRecoveryRequiredError("Recovery record has an invalid shape.")
        try:
            for item in reversed(backups):
                if not isinstance(item, dict):
                    raise GoalRecoveryRequiredError("Recovery record backup entry is invalid.")
                target = self._recovery_path(item.get("target"))
                backup_path = self._recovery_path(item.get("backup"))
                if backup_path.exists():
                    self._replace_file(backup_path, target)
                elif not target.exists():
                    raise GoalRecoveryRequiredError(
                        f"Recovery backup and target are both missing: {target}"
                    )
            for item in new_targets:
                target = self._recovery_path(item)
                if target.exists():
                    target.unlink()
            self._remove_empty_directories(
                self._recovery_path(item) for item in created_directories
            )
            self.recovery_record_file.unlink()
        except OSError as exc:
            raise GoalRecoveryRequiredError(
                "Recovery record could not be restored automatically."
            ) from exc

    def _recovery_path(self, value: object) -> Path:
        if not isinstance(value, str) or not value:
            raise GoalRecoveryRequiredError("Recovery record path is invalid.")
        path = self.goals_dir / value
        self._assert_write_path(path)
        return path

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


def create_goal(
    title: str,
    slug: str,
    parent_id: str | None,
    *,
    goals_dir: Path | None = None,
    **kwargs: object,
) -> GoalLoadResult:
    return GoalsRepository(goals_dir).create_goal(title, slug, parent_id, **kwargs)


def update_goal(
    goal_id: str,
    *,
    goals_dir: Path | None = None,
    **kwargs: object,
) -> GoalLoadResult:
    return GoalsRepository(goals_dir).update_goal(goal_id, **kwargs)


def repair_goal_tree(
    *,
    goals_dir: Path | None = None,
    **kwargs: object,
) -> GoalTreeIndex:
    return GoalsRepository(goals_dir).repair_goal_tree(**kwargs)


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


def _find_record_cycle_ids(records: Mapping[str, _TreeRecord]) -> set[str]:
    cycle_ids: set[str] = set()
    for start_id in records:
        chain: list[str] = []
        positions: dict[str, int] = {}
        current_id: str | None = start_id
        while (
            current_id is not None
            and current_id in records
            and current_id not in positions
        ):
            positions[current_id] = len(chain)
            chain.append(current_id)
            current_id = records[current_id].parent_id
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
