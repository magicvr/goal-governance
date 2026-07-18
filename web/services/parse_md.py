from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re
from typing import Mapping

import frontmatter

from services.models import (
    AuditConclusionState,
    DecisionEntry,
    ExecutionEntry,
    GoalMeta,
    GoalStatus,
    IssueSeverity,
    ValidationIssue,
)

GOAL_ID_RE = re.compile(r"^GOAL-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")
_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
_DECISION_HEADING_RE = re.compile(
    r"^(#{2,3})\s+(D-\d{3})\s*(?:[·.\-–—:：]\s*)?(.*)$", re.MULTILINE
)
_EXECUTION_HEADING_RE = re.compile(
    r"^#{2,4}\s+(\d{4}-\d{2}-\d{2})\s*[·\-–—:：]\s*(.+?)\s*$",
    re.MULTILINE,
)
_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class ParsedMarkdown:
    metadata: Mapping[str, object]
    body_markdown: str
    issues: tuple[ValidationIssue, ...]
    has_frontmatter: bool


def parse_frontmatter(
    text: str,
    path: Path,
    *,
    severity: IssueSeverity,
) -> ParsedMarkdown:
    if not _FRONTMATTER_RE.match(text.lstrip("﻿")):
        return ParsedMarkdown(
            metadata={},
            body_markdown=text,
            issues=(
                ValidationIssue(
                    code="invalid_frontmatter",
                    severity=severity,
                    path=path,
                    message="Document does not start with a complete frontmatter block.",
                ),
            ),
            has_frontmatter=False,
        )

    try:
        post = frontmatter.loads(text.lstrip("﻿"))
    except Exception as exc:  # python-frontmatter surfaces parser-specific exceptions
        return ParsedMarkdown(
            metadata={},
            body_markdown=text,
            issues=(
                ValidationIssue(
                    code="invalid_frontmatter",
                    severity=severity,
                    path=path,
                    message=f"Unable to parse frontmatter: {exc}",
                ),
            ),
            has_frontmatter=True,
        )

    return ParsedMarkdown(
        metadata=dict(post.metadata),
        body_markdown=post.content,
        issues=(),
        has_frontmatter=True,
    )


def parse_goal_meta(
    text: str,
    path: Path,
    folder_name: str,
) -> tuple[GoalMeta | None, str, tuple[ValidationIssue, ...]]:
    parsed = parse_frontmatter(text, path, severity=IssueSeverity.ERROR)
    issues = list(parsed.issues)
    metadata = parsed.metadata

    if issues:
        return None, parsed.body_markdown, tuple(issues)

    required_fields = ("id", "title", "status", "parent", "created", "updated")
    for field_name in required_fields:
        if field_name not in metadata:
            issues.append(
                ValidationIssue(
                    code="missing_required_field",
                    severity=IssueSeverity.ERROR,
                    path=path,
                    message=f"Missing required frontmatter field: {field_name}",
                )
            )

    if "version" not in metadata or not str(metadata.get("version", "")).strip():
        issues.append(
            ValidationIssue(
                code="missing_version",
                severity=IssueSeverity.ERROR,
                path=path,
                message="Missing required frontmatter field: version",
            )
        )

    goal_id = str(metadata.get("id", "")).strip()
    if goal_id and not GOAL_ID_RE.fullmatch(goal_id):
        issues.append(
            ValidationIssue(
                code="invalid_goal_id",
                severity=IssueSeverity.ERROR,
                path=path,
                message=f"Goal id is not canonical: {goal_id}",
            )
        )
    if goal_id and goal_id != folder_name:
        issues.append(
            ValidationIssue(
                code="id_folder_mismatch",
                severity=IssueSeverity.ERROR,
                path=path,
                message=f"Goal id {goal_id!r} does not match folder {folder_name!r}.",
            )
        )

    title = str(metadata.get("title", "")).strip()
    if "title" in metadata and not title:
        issues.append(
            ValidationIssue(
                code="missing_required_field",
                severity=IssueSeverity.ERROR,
                path=path,
                message="Goal title must not be empty.",
            )
        )

    status_value = str(metadata.get("status", "")).strip()
    try:
        status = GoalStatus(status_value)
    except ValueError:
        status = None
        if "status" in metadata:
            issues.append(
                ValidationIssue(
                    code="invalid_status",
                    severity=IssueSeverity.ERROR,
                    path=path,
                    message=f"Unsupported goal status: {status_value!r}",
                )
            )

    parent_value = metadata.get("parent")
    parent_id: str | None
    if parent_value is None:
        parent_id = None
        if goal_id and not goal_id.startswith("GOAL-001-"):
            issues.append(
                ValidationIssue(
                    code="invalid_parent",
                    severity=IssueSeverity.ERROR,
                    path=path,
                    message="Only GOAL-001 may have a null parent.",
                )
            )
    else:
        parent_id = str(parent_value).strip()
        if not GOAL_ID_RE.fullmatch(parent_id):
            issues.append(
                ValidationIssue(
                    code="invalid_parent",
                    severity=IssueSeverity.ERROR,
                    path=path,
                    message=f"Parent id is not canonical: {parent_id!r}",
                )
            )
        if goal_id.startswith("GOAL-001-"):
            issues.append(
                ValidationIssue(
                    code="invalid_parent",
                    severity=IssueSeverity.ERROR,
                    path=path,
                    message="GOAL-001 must have a null parent.",
                )
            )

    created = _parse_date(metadata.get("created"), path, "created", issues)
    updated = _parse_date(metadata.get("updated"), path, "updated", issues)

    if any(issue.severity is IssueSeverity.ERROR for issue in issues):
        return None, parsed.body_markdown, tuple(issues)

    known_fields = {
        "id",
        "title",
        "status",
        "parent",
        "created",
        "updated",
        "version",
        "progress",
    }
    extra = {key: value for key, value in metadata.items() if key not in known_fields}
    progress_value = metadata.get("progress")
    progress = None if progress_value is None else str(progress_value).strip()

    return (
        GoalMeta(
            id=goal_id,
            title=title,
            status=status,
            parent_id=parent_id,
            progress=progress or None,
            created=created,
            updated=updated,
            version=str(metadata["version"]).strip(),
            body_markdown=parsed.body_markdown,
            extra=extra,
        ),
        parsed.body_markdown,
        tuple(issues),
    )


def parse_section_document(text: str, path: Path) -> ParsedMarkdown:
    parsed = parse_frontmatter(text, path, severity=IssueSeverity.WARNING)
    issues = list(parsed.issues)
    if parsed.has_frontmatter:
        if "version" not in parsed.metadata or not str(parsed.metadata.get("version", "")).strip():
            issues.append(
                ValidationIssue(
                    code="missing_version",
                    severity=IssueSeverity.WARNING,
                    path=path,
                    message="Section document is missing required version metadata.",
                )
            )
    return ParsedMarkdown(
        metadata=parsed.metadata,
        body_markdown=parsed.body_markdown,
        issues=tuple(issues),
        has_frontmatter=parsed.has_frontmatter,
    )


def parse_decision_entries(body_markdown: str) -> tuple[DecisionEntry, ...]:
    matches = list(_DECISION_HEADING_RE.finditer(body_markdown))
    entries: list[DecisionEntry] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body_markdown)
        raw = body_markdown[match.start():end].rstrip()
        title = match.group(3).strip() or match.group(2)
        entries.append(
            DecisionEntry(
                id=match.group(2),
                title=title,
                raw_markdown=raw,
                status=_extract_labeled_value(raw, "状态"),
                decided=_extract_section_or_label(raw, ("决定", "决定了什么")),
                rationale=_extract_section_or_label(raw, ("为什么", "理由")),
                rejected=_extract_section_or_label(raw, ("未选方案", "未选")),
            )
        )
    return tuple(entries)


def parse_execution_entries(body_markdown: str) -> tuple[ExecutionEntry, ...]:
    matches = list(_EXECUTION_HEADING_RE.finditer(body_markdown))
    entries: list[ExecutionEntry] = []
    for index, match in enumerate(matches):
        try:
            entry_date = date.fromisoformat(match.group(1))
        except ValueError:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body_markdown)
        entries.append(
            ExecutionEntry(
                date=entry_date,
                title=match.group(2).strip(),
                raw_markdown=body_markdown[match.start():end].rstrip(),
            )
        )
    return tuple(entries)


def parse_audit_conclusion_state(
    body_markdown: str,
    metadata: Mapping[str, object] | None = None,
) -> AuditConclusionState:
    if metadata and "conclusion_state" in metadata:
        try:
            return AuditConclusionState(str(metadata["conclusion_state"]).strip())
        except ValueError:
            return AuditConclusionState.UNKNOWN

    headings = [match.group(1).strip().lower() for match in _HEADING_RE.finditer(body_markdown)]
    conclusion_headings = [
        heading
        for heading in headings
        if "结论" in heading or "verdict" in heading or "关门判定" in heading
    ]
    if not conclusion_headings:
        return AuditConclusionState.NONE
    if any(
        marker in heading
        for heading in conclusion_headings
        for marker in ("最终结论", "正式结项", "close-out", "关门判定", "final verdict")
    ):
        return AuditConclusionState.FINAL
    if any(
        marker in heading
        for heading in conclusion_headings
        for marker in ("阶段结论", "阶段 a 结论", "阶段 b 结论", "provisional")
    ):
        return AuditConclusionState.PROVISIONAL
    return AuditConclusionState.UNKNOWN


def extract_summary(body_markdown: str, limit: int = 240) -> str:
    section = _extract_heading_section(body_markdown, ("概述",))
    source = section if section is not None else body_markdown
    lines = []
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "|", "```", ">")):
            continue
        cleaned = re.sub(r"[*_`\[\]]", "", stripped)
        lines.append(cleaned)
        if len(" ".join(lines)) >= limit:
            break
    return " ".join(lines)[:limit].strip()


def extract_success_criteria(body_markdown: str) -> tuple[str, ...]:
    section = _extract_heading_section(body_markdown, ("成功标准",))
    if section is None:
        return ()
    criteria = []
    for line in section.splitlines():
        match = re.match(r"^\s*[-*]\s+(?:\[[ xX]\]\s*)?(.+?)\s*$", line)
        if match:
            criteria.append(match.group(1).strip())
    return tuple(criteria)


def has_roadmap(*bodies: str) -> bool:
    return any(re.search(r"^#{1,6}\s+.*高层路线图.*$", body, re.MULTILINE) for body in bodies)


def _parse_date(
    value: object,
    path: Path,
    field_name: str,
    issues: list[ValidationIssue],
) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            pass
    issues.append(
        ValidationIssue(
            code="invalid_date",
            severity=IssueSeverity.ERROR,
            path=path,
            message=f"Invalid {field_name} date: {value!r}",
        )
    )
    return None


def _extract_labeled_value(raw: str, label: str) -> str | None:
    pattern = re.compile(rf"(?:^|\n)\s*(?:-\s*)?\*\*{re.escape(label)}\*\*\s*[：:]\s*(.+)")
    match = pattern.search(raw)
    return match.group(1).strip() if match else None


def _extract_section_or_label(raw: str, labels: tuple[str, ...]) -> str | None:
    for label in labels:
        value = _extract_labeled_value(raw, label)
        if value:
            return value
        section = _extract_heading_section(raw, (label,))
        if section:
            return section.strip()
    return None


def _extract_heading_section(body: str, titles: tuple[str, ...]) -> str | None:
    matches = list(_HEADING_RE.finditer(body))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        if any(title in heading for title in titles):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
            return body[match.end():end].strip()
    return None
