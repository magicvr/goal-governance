"""Structural validation for docs/vision Charter → VP → Workspace alignment."""

from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = REPO_ROOT / "docs" / "vision"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "vision"

REQUIRED_VISION_FILES = (
    "README.md",
    "charter.md",
    "roadmap.md",
    "revisions.md",
    "reviews.md",
    "workspaces.md",
    "alignment.md",
    "consumer-checklist.md",
)

CHARTER_ALLOWED_STATUS = frozenset({"active", "superseded"})
VP_ALLOWED_STATUS = frozenset({"planned", "active", "closed", "abandoned"})
GOAL_FORBIDDEN_ON_CHARTER = frozenset(
    {"done", "draft", "blocked", "cancelled"}
)
VISION_ROLE_ALLOWED = frozenset({"primary", "delivery"})
VISION_REF_RE = re.compile(
    r"^(?P<vision_id>[a-z0-9-]+)@(?P<version>\d+\.\d+\.\d+)$"
)
VP_ID_RE = re.compile(r"^VP-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")
VREV_ID_RE = re.compile(r"^VRev-\d{3}$")
VREV_FILENAME_RE = re.compile(
    r"^(?P<id>VRev-\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)


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


def split_plan_refs(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def validate_charter(path: Path, *, require_active: bool = False) -> dict[str, str]:
    fields = parse_frontmatter(path)
    if fields.get("doc_type") != "vision-charter":
        raise ValueError("charter doc_type must be vision-charter")
    for key in ("vision_id", "version", "status"):
        if key not in fields or not fields[key]:
            raise ValueError(f"charter missing {key}")
    status = fields["status"]
    if status in GOAL_FORBIDDEN_ON_CHARTER or status == "done":
        raise ValueError("charter must not use Goal lifecycle done/status")
    if status not in CHARTER_ALLOWED_STATUS:
        raise ValueError(f"invalid charter status: {status}")
    # P-006 / GOAL-021 F-004: current-stack authority must be active (superseded only as history).
    if require_active and status != "active":
        raise ValueError("charter must be active for current vision stack")
    return fields


def validate_vision_plan(path: Path, charter: dict[str, str] | None = None) -> dict[str, str]:
    fields = parse_frontmatter(path)
    if fields.get("doc_type") != "vision-plan":
        raise ValueError("plan doc_type must be vision-plan")
    plan_id = fields.get("id", "")
    if not VP_ID_RE.fullmatch(plan_id):
        raise ValueError(f"invalid VP id: {plan_id}")
    if path.name != f"{plan_id}.md":
        raise ValueError("VP filename must equal id.md")
    status = fields.get("status", "")
    if status == "done" or status not in VP_ALLOWED_STATUS:
        raise ValueError(f"invalid VP status: {status}")
    vision_ref = fields.get("vision_ref", "")
    match = VISION_REF_RE.fullmatch(vision_ref)
    if match is None:
        raise ValueError(f"invalid vision_ref: {vision_ref}")
    if charter is not None:
        expected = f"{charter['vision_id']}@{charter['version']}"
        if vision_ref != expected:
            raise ValueError(
                f"vision_ref mismatch: got {vision_ref}, expected {expected}"
            )
    text = path.read_text(encoding="utf-8")
    if "| workspace_id |" not in text and "工作区绑定" not in text:
        raise ValueError("VP missing workspace binding section")
    return fields


def validate_workspace_vision_alignment(
    workspace_path: Path,
    *,
    vision_root: Path,
) -> dict[str, str]:
    fields = parse_frontmatter(workspace_path)
    role = fields.get("vision_role", "")
    if role not in VISION_ROLE_ALLOWED:
        raise ValueError(f"invalid vision_role: {role}")
    plan_refs_raw = fields.get("plan_refs", "").strip()
    primary = fields.get("primary_plan", "").strip()
    # P-006 / GOAL-021 F-004: all roles require plans; no require_plans opt-out.
    if not plan_refs_raw:
        raise ValueError("missing plan_refs")
    if not primary:
        raise ValueError("missing primary_plan")
    refs = split_plan_refs(plan_refs_raw)
    if primary not in refs:
        raise ValueError("primary_plan not in plan_refs")
    charter = validate_charter(vision_root / "charter.md", require_active=True)
    for ref in refs:
        if not VP_ID_RE.fullmatch(ref):
            raise ValueError(f"invalid plan ref: {ref}")
        plan_path = vision_root / "plans" / f"{ref}.md"
        if not plan_path.is_file():
            raise ValueError(f"missing VP file: {ref}")
        # Validate each plan_ref including vision_ref alignment to active Charter.
        validate_vision_plan(plan_path, charter)
    return fields


def validate_vision_review_ledger(vision_root: Path) -> set[str]:
    index_path = vision_root / "reviews.md"
    index_text = index_path.read_text(encoding="utf-8")
    if "| open required |" not in index_text:
        raise ValueError("reviews index missing open required projection")

    legacy_ids = set(
        re.findall(r"^### (VRev-\d{3})\b", index_text, re.MULTILINE)
    )
    report_ids: dict[str, Path] = {}
    reports_dir = vision_root / "reviews"
    if reports_dir.is_dir():
        for report_path in sorted(reports_dir.glob("VRev-*.md")):
            match = VREV_FILENAME_RE.fullmatch(report_path.name)
            if match is None:
                raise ValueError(f"invalid VRev filename: {report_path.name}")
            fields = parse_frontmatter(report_path)
            report_id = fields.get("id", "")
            if not VREV_ID_RE.fullmatch(report_id):
                raise ValueError(f"invalid VRev id: {report_id}")
            if report_id != match.group("id"):
                raise ValueError(
                    f"VRev filename/id mismatch: {report_path.name} != {report_id}"
                )
            if fields.get("doc_type") != "vision-review":
                raise ValueError(f"VRev doc_type must be vision-review: {report_path}")
            if fields.get("source") not in {"self", "independent"}:
                raise ValueError(f"invalid VRev source: {report_path}")
            if report_id in report_ids:
                raise ValueError(f"duplicate VRev report id: {report_id}")
            report_ids[report_id] = report_path

    duplicated = legacy_ids.intersection(report_ids)
    if duplicated:
        raise ValueError(
            "VRev ids duplicated across legacy inline and reports: "
            + ", ".join(sorted(duplicated))
        )

    index_rows: dict[str, str] = {}
    for line in index_text.splitlines():
        if not re.match(r"^\| VRev-\d{3} \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            raise ValueError(f"invalid VRev index row: {line}")
        review_id = cells[0]
        if review_id in index_rows:
            raise ValueError(f"duplicate VRev index id: {review_id}")
        if not re.fullmatch(r"\d+", cells[5]):
            raise ValueError(f"open required must be numeric: {review_id}")
        index_rows[review_id] = line

    ledger_ids = legacy_ids.union(report_ids)
    if set(index_rows) != ledger_ids:
        raise ValueError(
            "VRev index/report mismatch: "
            f"index={sorted(index_rows)}, ledger={sorted(ledger_ids)}"
        )
    for review_id, report_path in report_ids.items():
        relative = report_path.relative_to(vision_root).as_posix()
        if relative not in index_rows[review_id]:
            raise ValueError(f"VRev index missing report link: {review_id}")
    return ledger_ids


def validate_vision_stack(vision_root: Path) -> None:
    for name in REQUIRED_VISION_FILES:
        path = vision_root / name
        if not path.is_file():
            raise ValueError(f"missing vision file: {name}")
    charter = validate_charter(vision_root / "charter.md", require_active=True)
    plans_dir = vision_root / "plans"
    if not plans_dir.is_dir():
        raise ValueError("missing plans directory")
    plan_files = sorted(plans_dir.glob("VP-*.md"))
    if not plan_files:
        raise ValueError("at least one plans/VP-*.md required")
    for plan_path in plan_files:
        validate_vision_plan(plan_path, charter)
    validate_vision_review_ledger(vision_root)
    alignment = (vision_root / "alignment.md").read_text(encoding="utf-8")
    for phrase in (
        "fail closed",
        "plan_refs",
        "primary_plan",
        "progress",
        "goal-tree",
        "单愿景",
    ):
        if phrase not in alignment and phrase.replace("-", "") not in alignment:
            # allow Chinese equivalents already present; English keys required
            if phrase in {"plan_refs", "primary_plan", "fail closed", "单愿景"}:
                raise ValueError(f"alignment missing required phrase: {phrase}")


class VisionProtocolTests(unittest.TestCase):
    def _copy_valid_vision_fixture(self, tmp: str) -> Path:
        vision = Path(tmp) / "vision"
        shutil.copytree(FIXTURES / "valid-stack", vision)
        return vision

    def test_repo_vision_stack_is_complete_and_valid(self) -> None:
        validate_vision_stack(VISION_DIR)
        charter = validate_charter(VISION_DIR / "charter.md")
        self.assertEqual(charter["vision_id"], "vision-goal-governance")
        self.assertEqual(charter["status"], "active")
        self.assertNotEqual(charter["status"], "done")
        self.assertEqual(
            validate_vision_review_ledger(VISION_DIR),
            {f"VRev-{number:03d}" for number in range(1, 7)},
        )

    def test_vision_review_reports_have_unique_ids_and_index_links(self) -> None:
        review_ids = validate_vision_review_ledger(VISION_DIR)
        reports = sorted((VISION_DIR / "reviews").glob("VRev-*.md"))
        self.assertEqual(len(reports), len(review_ids))
        self.assertFalse(
            re.search(
                r"^### VRev-\d{3}\b",
                (VISION_DIR / "reviews.md").read_text(encoding="utf-8"),
                re.MULTILINE,
            )
        )

    def test_dogfood_workspace_and_root_align_to_vp(self) -> None:
        workspace = (
            REPO_ROOT
            / "docs"
            / "workspace-001-goal-governance"
            / "workspace.md"
        )
        root_meta = (
            REPO_ROOT
            / "docs"
            / "workspace-001-goal-governance"
            / "GOAL-001-main-vision"
            / "00-meta.md"
        )
        ws_fields = validate_workspace_vision_alignment(
            workspace, vision_root=VISION_DIR
        )
        self.assertEqual(ws_fields["vision_role"], "primary")
        self.assertEqual(
            ws_fields["primary_plan"], "VP-001-governance-platform-delivery"
        )
        root_fields = parse_frontmatter(root_meta)
        workspace_fields = parse_frontmatter(workspace)
        self.assertEqual(workspace_fields.get("status"), "archived")
        self.assertEqual(root_fields.get("status"), "done")
        self.assertEqual(
            root_fields.get("primary_plan"), ws_fields["primary_plan"]
        )
        self.assertEqual(
            root_fields.get("plan_refs"), ws_fields["plan_refs"]
        )
        plan = validate_vision_plan(
            VISION_DIR / "plans" / f"{ws_fields['primary_plan']}.md",
            validate_charter(VISION_DIR / "charter.md"),
        )
        self.assertEqual(plan["status"], "closed")

    def test_protocol_and_agents_document_three_layer_chain(self) -> None:
        protocol = (
            REPO_ROOT / "docs" / "architecture" / "workspace-protocol.md"
        ).read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        orchestrator = (
            REPO_ROOT / "skills" / "prompts" / "00-govern-orchestrator.md"
        ).read_text(encoding="utf-8")
        for text in (protocol, agents, orchestrator):
            self.assertIn("plan_refs", text)
            self.assertIn("primary_plan", text)
        self.assertIn("愿景", protocol)
        self.assertIn("docs/vision", agents)
        self.assertIn("docs/vision", orchestrator)
        alignment = (VISION_DIR / "alignment.md").read_text(encoding="utf-8")
        self.assertIn("fail closed", alignment)
        self.assertIn("progress", alignment.lower())
        self.assertIn("goal-tree", alignment)
        self.assertIn("Charter **没有 canonical `draft` 状态**", alignment)
        self.assertIn("战略假设/未知", alignment)

    def test_workspace_template_declares_vision_fields(self) -> None:
        template = REPO_ROOT / "docs" / "templates" / "workspace-context.md"
        fields = parse_frontmatter(template)
        for key in ("vision_role", "plan_refs", "primary_plan"):
            self.assertIn(key, fields)
        mirror = (
            REPO_ROOT / "skills" / "core" / "docs" / "templates" / "workspace-context.md"
        )
        self.assertEqual(
            template.read_text(encoding="utf-8"),
            mirror.read_text(encoding="utf-8"),
        )

    def test_fixture_valid_stack_passes(self) -> None:
        validate_vision_stack(FIXTURES / "valid-stack")

    def test_legacy_and_directory_reports_are_merged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vision = self._copy_valid_vision_fixture(tmp)
            index = vision / "reviews.md"
            text = index.read_text(encoding="utf-8")
            text += (
                "\n### VRev-002 · Legacy record\n\n"
                "Historical inline report retained for compatibility.\n"
                "\n| VRev-002 | 2026-07-29 | independent | legacy | pass | 0 | "
                "legacy record | reviews.md |\n"
            )
            index.write_text(text, encoding="utf-8")
            self.assertEqual(
                validate_vision_review_ledger(vision),
                {"VRev-001", "VRev-002"},
            )

    def test_duplicate_legacy_and_report_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vision = self._copy_valid_vision_fixture(tmp)
            index = vision / "reviews.md"
            index.write_text(
                index.read_text(encoding="utf-8")
                + "\n### VRev-001 · Duplicate legacy record\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicated across legacy"):
                validate_vision_review_ledger(vision)

    def test_duplicate_report_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vision = self._copy_valid_vision_fixture(tmp)
            shutil.copy2(
                vision / "reviews" / "VRev-001-charter-init.md",
                vision / "reviews" / "VRev-001-other.md",
            )
            with self.assertRaisesRegex(ValueError, "duplicate VRev report id"):
                validate_vision_review_ledger(vision)

    def test_report_filename_and_id_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vision = self._copy_valid_vision_fixture(tmp)
            report = vision / "reviews" / "VRev-001-charter-init.md"
            report.write_text(
                report.read_text(encoding="utf-8").replace("id: VRev-001", "id: VRev-002", 1),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "filename/id mismatch"):
                validate_vision_review_ledger(vision)

    def test_report_link_must_be_present_in_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vision = self._copy_valid_vision_fixture(tmp)
            index = vision / "reviews.md"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "reviews/VRev-001-charter-init.md",
                    "reviews/VRev-001-missing.md",
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing report link"):
                validate_vision_review_ledger(vision)

    def test_fixture_charter_done_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not use Goal lifecycle"):
            validate_charter(FIXTURES / "invalid-charter-done.md")

    def test_fixture_bad_vp_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "VP-001-sample.md"
            path.write_text(
                (FIXTURES / "invalid-vp-done.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid VP status"):
                validate_vision_plan(path)

    def test_missing_plan_refs_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing plan_refs"):
            validate_workspace_vision_alignment(
                FIXTURES / "invalid-workspace-missing-plans.md",
                vision_root=FIXTURES / "valid-stack",
            )

    def test_sandbox_role_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "workspace.md"
            path.write_text(
                "---\n"
                "id: ws-sandbox\n"
                "vision_role: sandbox\n"
                "plan_refs: VP-001-sample\n"
                "primary_plan: VP-001-sample\n"
                "---\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid vision_role"):
                validate_workspace_vision_alignment(
                    path, vision_root=FIXTURES / "valid-stack"
                )

    def test_agents_and_principles_document_p006(self) -> None:
        principles = (
            REPO_ROOT / "docs" / "architecture" / "principles.md"
        ).read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("P-006", principles)
        self.assertIn("单愿景", principles)
        self.assertIn("P-006", agents)
        self.assertIn("单愿景", agents)
        alignment = (VISION_DIR / "alignment.md").read_text(encoding="utf-8")
        self.assertIn("primary", alignment)
        self.assertIn("delivery", alignment)
        self.assertNotIn("vision_role: sandbox", alignment)
        self.assertNotIn("sandbox opt-out", alignment)

    def test_primary_plan_not_in_refs_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "workspace.md"
            path.write_text(
                "---\n"
                "id: ws-x\n"
                "vision_role: delivery\n"
                "plan_refs: VP-001-sample\n"
                "primary_plan: VP-999-missing\n"
                "---\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "primary_plan not in plan_refs"):
                validate_workspace_vision_alignment(
                    path, vision_root=FIXTURES / "valid-stack"
                )

    def test_vision_ref_mismatch_is_rejected(self) -> None:
        charter = {"vision_id": "vision-goal-governance", "version": "0.1.0"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "VP-001-sample.md"
            path.write_text(
                "---\n"
                "doc_type: vision-plan\n"
                "id: VP-001-sample\n"
                "status: active\n"
                "vision_ref: vision-goal-governance@9.9.9\n"
                "---\n\n## 工作区绑定\n\n| workspace_id |\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "vision_ref mismatch"):
                validate_vision_plan(path, charter)

    def test_superseded_charter_rejected_for_current_stack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "charter.md"
            path.write_text(
                "---\n"
                "doc_type: vision-charter\n"
                "vision_id: vision-goal-governance\n"
                "version: 0.1.0\n"
                "status: superseded\n"
                "---\n",
                encoding="utf-8",
            )
            # Historical status still parses without require_active.
            fields = validate_charter(path)
            self.assertEqual(fields["status"], "superseded")
            with self.assertRaisesRegex(ValueError, "must be active"):
                validate_charter(path, require_active=True)

    def test_workspace_plan_ref_vision_ref_is_checked(self) -> None:
        """Each plan_ref must validate vision_ref against active Charter (not file existence only)."""
        with tempfile.TemporaryDirectory() as tmp:
            vision = Path(tmp) / "vision"
            plans = vision / "plans"
            plans.mkdir(parents=True)
            (vision / "charter.md").write_text(
                "---\n"
                "doc_type: vision-charter\n"
                "vision_id: vision-goal-governance\n"
                "version: 0.1.0\n"
                "status: active\n"
                "---\n",
                encoding="utf-8",
            )
            (plans / "VP-001-sample.md").write_text(
                "---\n"
                "doc_type: vision-plan\n"
                "id: VP-001-sample\n"
                "status: active\n"
                "vision_ref: vision-goal-governance@9.9.9\n"
                "---\n\n## 工作区绑定\n\n| workspace_id |\n",
                encoding="utf-8",
            )
            ws = Path(tmp) / "workspace.md"
            ws.write_text(
                "---\n"
                "id: ws-x\n"
                "vision_role: delivery\n"
                "plan_refs: VP-001-sample\n"
                "primary_plan: VP-001-sample\n"
                "---\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "vision_ref mismatch"):
                validate_workspace_vision_alignment(ws, vision_root=vision)


if __name__ == "__main__":
    unittest.main()
