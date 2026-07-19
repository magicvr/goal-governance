from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DATE = "2026-07-19"
ROOT_ID = "GOAL-001-main-vision"
ROOT_TITLE = "独立核心根目标"


class StandaloneBootstrapTests(unittest.TestCase):
    def test_guide_declares_core_sources_and_boundaries(self) -> None:
        guide = (REPO_ROOT / "docs" / "standalone-bootstrap.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "docs/templates/",
            "docs/goals/goal-tree.md",
            "GOAL-001",
            "git init",
            "skills/",
            "web/",
            "来源",
            "生成路径",
            "核对结果",
            "P-005",
            "信息需求表",
        ):
            self.assertIn(phrase, guide)

    def test_docs_entry_declares_package_version_and_sync_ledger(self) -> None:
        entry = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        for phrase in (
            "核心包版本",
            "0.5.0",
            "canonical → Skills",
            "SHA-256",
            "docs/templates/goal-folder/",
            "skills/templates/goal-folder/",
        ):
            self.assertIn(phrase, entry)

    def test_empty_git_repo_can_bootstrap_core_root_without_adapters(self) -> None:
        if shutil.which("git") is None:
            self.skipTest("git is required for the independent bootstrap scenario")

        with tempfile.TemporaryDirectory(prefix="gg-core-bootstrap-") as tmp:
            target = Path(tmp)
            self._init_git_repo(target)
            self._copy_core_package(target)
            self._materialize_root(target)

            self._assert_root_shape(target)
            self.assertIn("P-005", (target / "AGENTS.md").read_text(encoding="utf-8"))
            principles = (target / "docs" / "architecture" / "principles.md").read_text(
                encoding="utf-8"
            )
            for phrase in (
                "P-005",
                "设立许可",
                "规划门禁",
                "实施门禁",
                "关门门禁",
                "accepted-residual",
                "子目标拆分",
                "required",
                "non-blocking",
                "deferred",
                "有界实验",
                "目标可以创建为 `draft` 或 `active`，即使信息表仍有开放项",
                "有界实验只能进入其明确的**信息收集范围**",
                "暂停受影响范围、记录事实，并回流到信息表、决策或路线图",
                "不是每个目标的固定两个子目标",
            ):
                self.assertIn(phrase, principles)
            self.assertIn(
                "信息就绪与未知项",
                (target / "docs" / "templates" / "goal-folder" / "00-meta.md").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertFalse((target / "skills").exists())
            self.assertFalse((target / "web").exists())
            result = subprocess.run(
                ["git", "-C", str(target), "rev-parse", "--is-inside-work-tree"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.stdout.strip(), "true")

    @staticmethod
    def _init_git_repo(target: Path) -> None:
        subprocess.run(
            ["git", "-C", str(target), "init"],
            check=True,
            capture_output=True,
            text=True,
        )

    @staticmethod
    def _copy_core_package(target: Path) -> None:
        source_docs = REPO_ROOT / "docs"
        (target / "docs").mkdir()
        shutil.copy2(REPO_ROOT / "AGENTS.md", target / "AGENTS.md")
        shutil.copy2(source_docs / "README.md", target / "docs" / "README.md")
        shutil.copytree(source_docs / "architecture", target / "docs" / "architecture")
        shutil.copytree(source_docs / "templates", target / "docs" / "templates")

    @staticmethod
    def _frontmatter(fields: dict[str, str], body: str) -> str:
        lines = ["---"]
        lines.extend(f"{key}: {value}" for key, value in fields.items())
        lines.extend(["---", "", body.rstrip(), ""])
        return "\n".join(lines)

    @classmethod
    def _materialize_root(cls, target: Path) -> None:
        goals = target / "docs" / "goals"
        root = goals / ROOT_ID
        goals.mkdir()
        root.mkdir()

        template = target / "docs" / "templates" / "goal-folder"
        for name in ("00-meta.md", "01-decision.md", "02-execution.md", "03-audit.md"):
            if not (template / name).is_file():
                raise AssertionError(f"canonical template missing: {name}")
            shutil.copy2(template / name, root / name)
        shutil.copytree(template / "attachments", root / "attachments")

        common = {
            "id": ROOT_ID,
            "status": "active",
            "created": DATE,
            "updated": DATE,
            "parent": "null",
            "version": "0.1.0",
        }
        (root / "00-meta.md").write_text(
            cls._frontmatter(
                {**common, "title": ROOT_TITLE, "progress": "0%"},
                f"# GOAL-001 · {ROOT_TITLE}\n\n## 概述\n独立核心包生成的 Root Goal。",
            ),
            encoding="utf-8",
        )
        (root / "01-decision.md").write_text(
            cls._frontmatter(
                {**common, "doc": "decision"},
                "# 决策记录 · GOAL-001\n\n## D-001 · 建立核心 Root\n\n按核心协议初始化。",
            ),
            encoding="utf-8",
        )
        (root / "02-execution.md").write_text(
            cls._frontmatter(
                {**common, "doc": "execution"},
                "# 执行记录 · GOAL-001\n\n## 时间线\n\n### 2026-07-19 · 初始化\n\n- 从 canonical 模板建立 Root。",
            ),
            encoding="utf-8",
        )
        (root / "03-audit.md").write_text(
            cls._frontmatter(
                {**common, "doc": "audit"},
                "# 审计 · GOAL-001\n\n## 审计状态\n\n尚未到达阶段性复盘节点。",
            ),
            encoding="utf-8",
        )

        (goals / "goal-tree.md").write_text(
            "\n".join(
                [
                    "---",
                    "title: Goal Tree · 目标树与进展总览",
                    "status: active",
                    f"created: {DATE}",
                    f"updated: {DATE}",
                    "parent: null",
                    "version: 0.1.0",
                    "---",
                    "",
                    "# Goal Tree",
                    "",
                    "```text",
                    f"{ROOT_ID} · {ROOT_TITLE} [active 0%]",
                    "```",
                    "",
                    "| ID | 标题 | Parent | Status | Progress | 路径 |",
                    "|----|------|--------|--------|----------|------|",
                    f"| {ROOT_ID} | {ROOT_TITLE} | — | active | 0% | {ROOT_ID}/ |",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _parse_frontmatter(path: Path) -> dict[str, str]:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if match is None:
            raise AssertionError(f"missing frontmatter: {path}")
        fields: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
        return fields

    def _assert_root_shape(self, target: Path) -> None:
        goals = target / "docs" / "goals"
        root = goals / ROOT_ID
        required = ("00-meta.md", "01-decision.md", "02-execution.md", "03-audit.md")
        self.assertTrue(root.is_dir())
        self.assertTrue((root / "attachments").is_dir())
        self.assertTrue((root / "attachments" / ".gitkeep").is_file())
        self.assertEqual(
            [path.name for path in goals.iterdir() if path.is_dir()],
            [ROOT_ID],
        )

        for name in required:
            path = root / name
            self.assertTrue(path.is_file(), f"missing root file: {path}")
            fields = self._parse_frontmatter(path)
            for key in ("status", "created", "updated", "parent", "version"):
                self.assertIn(key, fields, f"{name} missing {key}")
            self.assertEqual(fields["id"], ROOT_ID)
            self.assertEqual(fields["parent"], "null")

        meta = self._parse_frontmatter(root / "00-meta.md")
        self.assertEqual(meta["title"], ROOT_TITLE)
        self.assertEqual(meta["progress"], "0%")

        tree_path = goals / "goal-tree.md"
        tree_fields = self._parse_frontmatter(tree_path)
        for key in ("status", "created", "updated", "parent", "version"):
            self.assertIn(key, tree_fields, f"goal-tree missing {key}")
        self.assertEqual(tree_fields["parent"], "null")
        tree = tree_path.read_text(encoding="utf-8")
        self.assertIn(ROOT_ID, tree)
        self.assertIn("[active 0%]", tree)


if __name__ == "__main__":
    unittest.main()
