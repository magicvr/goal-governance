"""Consumer loading, real installation and transactional long-rule upgrades."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock
import zipfile

from scripts.tests.test_skills_update import update, render, pack, SKILLS, REPO_ROOT
from skills.agents_merge import MANAGED_BEGIN, MANAGED_END, extract_managed_block


class OnDemandGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="gg-on-demand-")
        cls.archive = pack.pack_skills(
            version="0.0.0-on-demand", output_dir=Path(cls.temp.name),
            skills_root=SKILLS, skip_stage=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def args(self, target, **kwargs):
        values = dict(version=self.archive.version, latest=False, target_dir=str(target),
                      skills_dir="tooling/gov", methodology_dir="governance",
                      zip_path=str(self.archive.zip_path), sha256_path=str(self.archive.sha256_path),
                      repo="magicvr/goal-governance", release_tag="", allow_protocol_upgrade=False,
                      force_managed=False, dry_run=False, skip_install=False)
        values.update(kwargs)
        return argparse.Namespace(**values)

    def legacy(self, target, *, marked):
        package = target / "tooling/gov"
        shutil.copytree(SKILLS, package)
        # A known old package face with long rules and install placeholders.
        body = "# Legacy {{GOVERNANCE_ROOT}} {{SKILLS_DIR}}\n" + "old governance rule\n" * 2000
        source = f"{MANAGED_BEGIN}\n{body}{MANAGED_END}\n" if marked else body
        originals = {}
        for source_rel, destination_rel in update.RULE_FACES:
            (package / source_rel).write_text(source, encoding="utf-8")
            rendered = render.render_managed_text(source, "governance", "tooling/gov")
            raw = rendered.encode()
            if marked:
                raw = b"KEEP-CONSUMER\r\n" + raw.rstrip(b"\n") + b"\r\nKEEP-SUFFIX"
            destination = target / destination_rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
            originals[destination_rel] = raw
        (package / "core/docs/architecture/governance-guide.md").unlink()
        (package / "core/docs/templates/governance-entry.md").unlink()
        return originals

    def test_entry_budget_and_all_rule_faces_share_canonical(self):
        canonical = (REPO_ROOT / "docs/templates/governance-entry.md").read_bytes()
        for rel in ("AGENTS.template.md", "install/claude/AGENTS.md",
                    "install/copilot/copilot-instructions.md", "core/docs/templates/governance-entry.md"):
            self.assertEqual((SKILLS / rel).read_bytes(), canonical, rel)
        for token in ("docs", "governance", "my project/methodology"):
            entry = render.render_managed_bytes(canonical, token, "tooling/gov")
            self.assertLessEqual(len(entry), 4096)
            self.assertLessEqual(len(entry.splitlines()), 40)
            self.assertIn(f"{token}/architecture/governance-guide.md".encode(), entry)
        text = canonical.decode()
        for trigger in ("/govern", "/audit", "/vision", "/vision-audit", "治理记录", "普通业务", "不可读"):
            self.assertIn(trigger, text)

    def test_every_governance_entry_explicitly_loads_after_root_check(self):
        entries = list((SKILLS / "prompts").glob("[0-9][0-9]-*.md"))
        entries += list((SKILLS / "install").glob("*/skills/*/SKILL.md"))
        entries += list((SKILLS / "install/copilot/prompts").glob("*.md"))
        entries = [path for path in entries if path.stem != "commit" and path.parent.name != "commit"]
        self.assertGreaterEqual(len(entries), 28)
        for path in entries:
            text = path.read_text(encoding="utf-8")
            self.assertLess(text.index("治理根预检："), text.index("按需加载："), str(path))
            self.assertIn("必须完整读取 `{governance_root}/architecture/governance-guide.md`", text, str(path))
            self.assertIn("缺失/不可读时停止", text, str(path))

    def test_new_install_and_repeat_preserve_user_rules_and_custom_paths(self):
        with tempfile.TemporaryDirectory(prefix="gg-entry-install-") as tmp:
            target = Path(tmp)
            project_config = b'{\r\n  "governance_root": "governance", "independent_audit": {"provider": "codex", "model": "gpt-6.1-sol", "reasoning_effort": "high"}\r\n}\r\n'
            (target / ".goal-governance.json").write_bytes(project_config)
            for rel in ("AGENTS.md", ".github/copilot-instructions.md"):
                path = target / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"KEEP-CONSUMER\r\n")
            for _ in range(2):
                update.run_installer(SKILLS, target, methodology_dir="governance", skills_dir="tooling/gov")
                self.assertEqual((target / ".goal-governance.json").read_bytes(), project_config)
                for rel in ("AGENTS.md", ".github/copilot-instructions.md"):
                    raw = (target / rel).read_bytes()
                    self.assertTrue(raw.startswith(b"KEEP-CONSUMER\r\n"), rel)
                    self.assertEqual(raw.count(MANAGED_BEGIN.encode()), 1, rel)
                    self.assertLess(len(extract_managed_block(raw.decode()).encode()), 4096)
                    self.assertIn(b"governance/architecture/governance-guide.md", raw)
            guide = target / "governance/architecture/governance-guide.md"
            self.assertTrue(guide.is_file())
            self.assertNotIn("{governance_root}", guide.read_text(encoding="utf-8"))
            self.assertIn("governance/architecture/governance-guide.md",
                          (target / ".agents/skills/govern/SKILL.md").read_text(encoding="utf-8"))

    def test_real_upgrade_replaces_long_blocks_and_retains_external_bytes(self):
        with tempfile.TemporaryDirectory(prefix="gg-long-upgrade-") as tmp:
            target = Path(tmp)
            originals = self.legacy(target, marked=True)
            project_config = b'{ "governance_root": "governance", "independent_audit": {"provider":"claude","model":"opus","reasoning_effort":"max"} }\r\n'
            (target / ".goal-governance.json").write_bytes(project_config)
            report = update.update_package(self.args(target))
            self.assertEqual(report["result"], "updated")
            self.assertEqual((target / ".goal-governance.json").read_bytes(), project_config)
            for rel, raw in originals.items():
                actual = (target / rel).read_bytes()
                self.assertTrue(actual.startswith(b"KEEP-CONSUMER\r\n"))
                self.assertTrue(actual.endswith(b"\r\nKEEP-SUFFIX"))
                self.assertNotIn(b"old governance rule", actual)
                self.assertLess(len(actual), 4096)
                self.assertEqual((Path(report["rollback_path"]) / "project" / rel).read_bytes(), raw)

    def test_unmarked_custom_root_upgrade_and_dry_run(self):
        with tempfile.TemporaryDirectory(prefix="gg-unmarked-upgrade-") as tmp:
            target = Path(tmp)
            originals = self.legacy(target, marked=False)
            report = update.update_package(self.args(target, dry_run=True))
            self.assertEqual(report["result"], "dry-run")
            for rel, raw in originals.items():
                self.assertEqual((target / rel).read_bytes(), raw)
            self.assertFalse((target / ".goal-governance-updates").exists())
            report = update.update_package(self.args(target))
            self.assertEqual(report["result"], "updated")
            for rel in originals:
                actual = (target / rel).read_bytes()
                self.assertNotIn(b"old governance rule", actual)
                self.assertEqual(actual.count(MANAGED_BEGIN.encode()), 1)
                self.assertLess(len(actual), 4096)

    def test_failed_upgrade_restores_both_rule_faces_and_missing_guide(self):
        with tempfile.TemporaryDirectory(prefix="gg-rollback-entry-") as tmp:
            target = Path(tmp)
            originals = self.legacy(target, marked=False)
            def fail(*args, **kwargs):
                (target / "AGENTS.md").write_text("half installed", encoding="utf-8")
                (target / ".github/copilot-instructions.md").write_text("half installed", encoding="utf-8")
                guide = target / "governance/architecture/governance-guide.md"
                guide.parent.mkdir(parents=True, exist_ok=True)
                guide.write_text("half installed", encoding="utf-8")
                raise update.UpdateError("injected install failure")
            with mock.patch.object(update, "run_installer", side_effect=fail):
                with self.assertRaisesRegex(update.UpdateError, "injected"):
                    update.update_package(self.args(target))
            for rel, raw in originals.items():
                self.assertEqual((target / rel).read_bytes(), raw)
            self.assertFalse((target / "governance/architecture/governance-guide.md").exists())

    def test_new_guide_collision_requires_review(self):
        with tempfile.TemporaryDirectory(prefix="gg-guide-collision-") as tmp:
            target = Path(tmp)
            self.legacy(target, marked=True)
            guide = target / "governance/architecture/governance-guide.md"
            guide.parent.mkdir(parents=True, exist_ok=True)
            guide.write_text("user-authored document", encoding="utf-8")
            with self.assertRaisesRegex(update.UpdateError, "managed files have local changes"):
                update.update_package(self.args(target))
            self.assertEqual(guide.read_text(encoding="utf-8"), "user-authored document")

    def test_release_archive_contains_guide_and_core_only_entry_template(self):
        with zipfile.ZipFile(self.archive.zip_path) as archive:
            names = archive.namelist()
            for relative in ("core/docs/architecture/governance-guide.md", "core/docs/templates/governance-entry.md"):
                self.assertTrue(any(name.endswith("/" + relative) for name in names), relative)


if __name__ == "__main__":
    unittest.main()
