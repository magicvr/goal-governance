from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "workspace"
REQUIRED_CONTEXT_FIELDS = {
    "id",
    "title",
    "status",
    "root_goal",
    "canonical_scope",
    "shared_materials_catalog",
    "created",
    "updated",
    "version",
}
REFERENCE_FIELDS = (
    "reference_id",
    "workspace_id",
    "material_id",
    "source",
    "version",
    "sha256",
    "purpose",
    "local_record",
    "status",
)
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
WORKSPACE_SCOPE_RE = re.compile(r"^docs/workspace-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*/$")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise ValueError(f"missing frontmatter: {path}")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def parse_reference_rows(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header = "| reference_id | workspace_id | material_id | source | version | sha256 | purpose | local_record | status |"
    try:
        start = lines.index(header)
    except ValueError as exc:
        raise ValueError(f"missing reference table: {path}") from exc

    rows: list[dict[str, str]] = []
    for line in lines[start + 2 :]:
        if not line.startswith("|"):
            break
        values = [value.strip() for value in line.strip("|").split("|")]
        if len(values) != len(REFERENCE_FIELDS):
            raise ValueError(f"unexpected reference column count: {path}")
        rows.append(dict(zip(REFERENCE_FIELDS, values, strict=True)))
    return rows


def validate_workspace_context(path: Path) -> None:
    fields = parse_frontmatter(path)
    missing = REQUIRED_CONTEXT_FIELDS - fields.keys()
    if missing:
        raise ValueError(f"missing context fields: {sorted(missing)}")
    if not re.fullmatch(r"GOAL-001-[a-z0-9-]+", fields["root_goal"]):
        raise ValueError("root_goal must be a complete GOAL-001 id")
    if not WORKSPACE_SCOPE_RE.fullmatch(fields["canonical_scope"]):
        raise ValueError("canonical_scope must be a workspace root")

    references = parse_reference_rows(path)
    if fields["shared_materials_catalog"] == "none" and references:
        raise ValueError("none catalog cannot have references")
    reference_ids: set[str] = set()
    for reference in references:
        if reference["reference_id"] in reference_ids:
            raise ValueError("duplicate reference_id")
        reference_ids.add(reference["reference_id"])
        if reference["workspace_id"] != fields["id"]:
            raise ValueError("workspace_id mismatch")
        for key in ("material_id", "source", "version", "purpose"):
            if not reference[key] or reference[key] == "none":
                raise ValueError(f"missing {key}")
        if not SHA256_RE.fullmatch(reference["sha256"]):
            raise ValueError("invalid sha256")
        if reference["status"] not in {"active", "withdrawn", "invalid"}:
            raise ValueError("invalid reference status")


class WorkspaceProtocolTests(unittest.TestCase):
    def test_current_project_uses_one_explicit_workspace_root(self) -> None:
        workspace = REPO_ROOT / "docs" / "workspace-001-goal-governance"
        context = workspace / "workspace.md"

        self.assertTrue(workspace.is_dir())
        self.assertFalse((REPO_ROOT / "docs" / "goals").exists())
        validate_workspace_context(context)
        fields = parse_frontmatter(context)
        self.assertEqual(fields["root_goal"], "GOAL-001-main-vision")
        self.assertEqual(fields["canonical_scope"], "docs/workspace-001-goal-governance/")
        self.assertTrue((workspace / "goal-tree.md").is_file())
        self.assertTrue((workspace / fields["root_goal"]).is_dir())

    def test_protocol_has_core_and_legacy_boundaries(self) -> None:
        protocol = (
            REPO_ROOT / "docs" / "architecture" / "workspace-protocol.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "工作区根",
            "legacy 隐式单工作区",
            "Root Goal",
            "串行子目标",
            "fail-closed",
            "第二套状态",
            "GOAL-009 R-003",
            "Q2",
            "Q3",
            "文档落盘默认",
            "对话/编排回显默认",
            "把工作区编号嵌进 goal id",
        ):
            self.assertIn(phrase, protocol)

    def test_workspace_template_declares_the_required_context_contract(self) -> None:
        template = REPO_ROOT / "docs" / "templates" / "workspace-context.md"
        fields = parse_frontmatter(template)
        self.assertTrue(REQUIRED_CONTEXT_FIELDS.issubset(fields))
        text = template.read_text(encoding="utf-8")
        for field in REFERENCE_FIELDS:
            self.assertIn(field, text)

    def test_valid_workspace_reference_is_accepted(self) -> None:
        validate_workspace_context(FIXTURES / "valid-workspace.md")

    def test_workspace_reference_mismatch_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "workspace_id mismatch"):
            validate_workspace_context(FIXTURES / "invalid-workspace-reference.md")

    def test_unfixed_workspace_reference_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid sha256"):
            validate_workspace_context(FIXTURES / "invalid-workspace-sha256.md")

    def test_legacy_scope_cannot_be_declared_by_an_explicit_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "workspace.md"
            text = (FIXTURES / "valid-workspace.md").read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    "canonical_scope: docs/workspace-001-alpha/",
                    "canonical_scope: docs/goals/",
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "workspace root"):
                validate_workspace_context(path)


if __name__ == "__main__":
    unittest.main()
