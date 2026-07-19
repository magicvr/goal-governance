from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Literal, Mapping


class GoalStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


class IssueSeverity(str, Enum):
    WARNING = "warning"
    ERROR = "error"


class AuditConclusionState(str, Enum):
    NONE = "none"
    PROVISIONAL = "provisional"
    FINAL = "final"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: IssueSeverity
    path: Path
    message: str


@dataclass(frozen=True)
class GoalMeta:
    id: str
    title: str
    status: GoalStatus
    parent_id: str | None
    progress: str | None
    created: date
    updated: date
    version: str
    body_markdown: str
    extra: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class DecisionEntry:
    id: str
    title: str
    raw_markdown: str
    status: str | None = None
    decided: str | None = None
    rationale: str | None = None
    rejected: str | None = None


@dataclass(frozen=True)
class DecisionDoc:
    body_markdown: str
    entries: tuple[DecisionEntry, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionEntry:
    date: date
    title: str
    raw_markdown: str


@dataclass(frozen=True)
class ExecutionDoc:
    body_markdown: str
    entries: tuple[ExecutionEntry, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditDoc:
    body_markdown: str
    conclusion_state: AuditConclusionState = AuditConclusionState.NONE
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class AttachmentRef:
    name: str
    relative_path: Path
    media_type: str | None = None


@dataclass(frozen=True)
class Goal:
    folder_name: str
    path: Path
    meta: GoalMeta
    summary: str
    success_criteria: tuple[str, ...]
    roadmap_present: bool
    decision: DecisionDoc
    execution: ExecutionDoc
    audit: AuditDoc
    attachments: tuple[AttachmentRef, ...] = ()

    @property
    def id(self) -> str:
        return self.meta.id

    @property
    def title(self) -> str:
        return self.meta.title

    @property
    def status(self) -> GoalStatus:
        return self.meta.status

    @property
    def parent_id(self) -> str | None:
        return self.meta.parent_id

    @property
    def progress(self) -> str | None:
        return self.meta.progress

    @property
    def created(self) -> date:
        return self.meta.created

    @property
    def updated(self) -> date:
        return self.meta.updated

    @property
    def version(self) -> str:
        return self.meta.version


@dataclass(frozen=True)
class GoalLoadResult:
    goal: Goal | None
    path: Path
    raw_markdown: str | None
    issues: tuple[ValidationIssue, ...] = ()


@dataclass(frozen=True)
class FieldMismatch:
    goal_id: str
    field: Literal["title", "parent_id", "status", "progress"]
    disk_value: str | None
    tree_value: str | None


@dataclass(frozen=True)
class TreeValidationReport:
    missing_in_tree: tuple[str, ...] = ()
    missing_on_disk: tuple[str, ...] = ()
    field_mismatches: tuple[FieldMismatch, ...] = ()
    orphan_ids: tuple[str, ...] = ()
    cycle_ids: tuple[str, ...] = ()
    duplicate_number_ids: Mapping[int, tuple[str, ...]] = field(default_factory=dict)
    issues: tuple[ValidationIssue, ...] = ()


@dataclass(frozen=True)
class GoalTreeNode:
    id: str
    title: str
    parent_id: str | None
    status: GoalStatus
    progress: str | None
    path: Path
    depth: int | None
    children_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class GoalTreeIndex:
    nodes: tuple[GoalTreeNode, ...]
    root_ids: tuple[str, ...]
    generated_at: datetime
    source: Literal["directory_scan", "goal_tree_md", "merged"]
    tree_drift: bool
    validation_report: TreeValidationReport
