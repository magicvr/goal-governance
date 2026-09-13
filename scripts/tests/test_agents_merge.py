"""GOAL-008 S4: root AGENTS.md managed-block merge (consumer coexistence).

Model A (user ruling): the consumer repo owns root ``AGENTS.md``; the framework
rules live inside a delimited managed block. ``managed_file_pairs`` no longer
treats root AGENTS.md as a fully-managed destination, so a consumer's own rules
in the same file survive install and update.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"
sys.path.insert(0, str(SKILLS))

import agents_merge  # noqa: E402
import update as skills_update  # noqa: E402


def sample_source() -> str:
    return (
        "# Framework rules\n\n"
        f"{agents_merge.MANAGED_BEGIN}\n"
        "## Goal governance rules\n"
        "- read docs/architecture/principles.md\n"
        f"{agents_merge.MANAGED_END}\n"
    )


class AgentsMergeUnitTests(unittest.TestCase):
    def test_fresh_target_becomes_managed_block(self) -> None:
        merged, changed = agents_merge.merge_agents_text("", sample_source())
        self.assertTrue(changed)
        self.assertTrue(merged.startswith(agents_merge.MANAGED_BEGIN))
        self.assertIn("Goal governance rules", merged)

    def test_consumer_content_outside_block_is_preserved(self) -> None:
        consumer = "# My rules\n\n- use tabs\n\n"
        merged, changed = agents_merge.merge_agents_text(consumer, sample_source())
        self.assertTrue(changed)
        self.assertTrue(merged.startswith(consumer))
        self.assertIn(agents_merge.MANAGED_BEGIN, merged)
        # Idempotent: merging again changes nothing.
        merged_again, changed_again = agents_merge.merge_agents_text(merged, sample_source())
        self.assertFalse(changed_again)
        self.assertEqual(merged, merged_again)

    def test_all_pre_s4_shapes_keep_bytes_outside_the_markers(self) -> None:
        """GOAL-008 S6 (v0.13.3): the promise is about bytes *outside* the markers.

        Enumerates the pre-S4 and marked shapes and asserts that whatever the
        consumer owns outside the managed region survives verbatim. Text *inside*
        the markers is framework-managed and is replaced by design.
        """
        begin, end = agents_merge.MANAGED_BEGIN, agents_merge.MANAGED_END
        shipped = f"{begin}\n# AGENTS.md\n\n## 1. Rules\n\n- framework rules\n{end}\n"
        before = "## Consumer rules (before)\n\n- keep me\n\n"
        after = "\n## Consumer rules (after)\n\n- keep me too\n"
        shapes = {
            "whole-file legacy install (nothing outside)": shipped,
            "legacy + own rules after the block": shipped + after,
            "legacy + own rules before the block": before + shipped,
            "legacy + own rules on both sides": before + shipped + after,
        }
        for label, target in shapes.items():
            with self.subTest(shape=label):
                merged, _changed = agents_merge.merge_agents_text(target, shipped)
                self.assertEqual(
                    merged.count(begin),
                    merged.count(end),
                    msg=f"unbalanced markers for {label}",
                )
                self.assertIn("## 1. Rules", merged, msg=f"framework rules lost for {label}")
                self.assertIn("framework rules", merged, msg=f"framework rules lost for {label}")
                if before.strip() in target:
                    self.assertIn(
                        "## Consumer rules (before)",
                        merged,
                        msg=f"consumer prefix lost for {label}",
                    )
                if after.strip() in target:
                    self.assertIn(
                        "## Consumer rules (after)",
                        merged,
                        msg=f"consumer suffix lost for {label}",
                    )

    def test_repeated_merge_never_touches_a_converged_file(self) -> None:
        """A converged file must be byte-stable on every later merge."""
        begin, end = agents_merge.MANAGED_BEGIN, agents_merge.MANAGED_END
        shipped = f"{begin}\n# AGENTS.md\n\n- framework rules\n{end}\n"
        target = "## Consumer rules\n\n- mine\n\n" + shipped
        merged, changed = agents_merge.merge_agents_text(target, shipped)
        self.assertFalse(changed, msg="already-converged file must not be rewritten")
        self.assertEqual(merged, target)
        # And the file the installer would write stays stable afterwards.
        first, _ = agents_merge.merge_agents_text("", shipped)
        second, changed_again = agents_merge.merge_agents_text(first, shipped)
        self.assertFalse(changed_again)
        self.assertEqual(first, second)

    def test_consumer_edits_inside_block_are_refreshed_but_outside_kept(self) -> None:
        consumer = "# My rules\n"
        first, _ = agents_merge.merge_agents_text(consumer, sample_source())
        edited = first.replace("## Goal governance rules", "## Hand edit")
        self.assertIn("## Hand edit", edited)
        merged, changed = agents_merge.merge_agents_text(edited, sample_source())
        self.assertTrue(changed)
        self.assertIn("## Goal governance rules", merged)
        self.assertNotIn("## Hand edit", merged)
        self.assertTrue(merged.startswith("# My rules\n"))

    def test_legacy_whole_file_install_is_wrapped_equivalently(self) -> None:
        # A pre-S4 consumer install was the whole rule file with no markers at
        # all. Migrating it must wrap those rules in one managed block without
        # dropping or reordering any text.
        rules = "## 1. 文档真相来源\n\n- 目标记录在 workspace 根\n"
        legacy = rules
        source = f"{agents_merge.MANAGED_BEGIN}\n{rules}{agents_merge.MANAGED_END}\n"
        merged, changed = agents_merge.merge_agents_text(legacy, source)
        self.assertTrue(changed)
        self.assertTrue(merged.startswith(agents_merge.MANAGED_BEGIN))
        self.assertIn(rules.strip(), merged)
        self.assertEqual(
            merged.count(agents_merge.MANAGED_BEGIN),
            merged.count(agents_merge.MANAGED_END),
        )
        # Idempotent afterwards.
        again, changed_again = agents_merge.merge_agents_text(merged, source)
        self.assertFalse(changed_again)
        self.assertEqual(merged, again)

    def test_legacy_install_with_rule_pair_is_migrated_in_place(self) -> None:
        # Pre-S4 shipped rule faces carried a rule-level marker pair inside the
        # file. A pre-S4 consumer install kept that frame; migrating it must swap
        # only the markers while keeping the surrounding bytes (the intro the
        # consumer saw before) in place.
        rules = (
            "## rules\n\n"
            f"{agents_merge.MANAGED_BEGIN}\npayload\n{agents_merge.MANAGED_END}\n"
        )
        legacy = f"## 1. 文档真相来源\n\n- x\n\n{rules}"
        source = f"{agents_merge.MANAGED_BEGIN}\n{rules}{agents_merge.MANAGED_END}\n"
        merged, changed = agents_merge.merge_agents_text(legacy, source)
        self.assertTrue(changed)
        self.assertEqual(
            merged.count(agents_merge.MANAGED_BEGIN),
            merged.count(agents_merge.MANAGED_END),
        )
        self.assertIn("payload", merged)
        # Bytes outside the old frame survive.
        self.assertTrue(merged.startswith("## 1. 文档真相来源\n\n- x\n\n"))
        self.assertIn("## 1. 文档真相来源", merged)
        # Idempotent afterwards.
        again, changed_again = agents_merge.merge_agents_text(merged, source)
        self.assertFalse(changed_again)
        self.assertEqual(merged, again)

    def test_half_written_markers_fail_closed(self) -> None:
        with self.assertRaises(agents_merge.MergeError):
            agents_merge.merge_agents_text(
                f"consumer\n{agents_merge.MANAGED_BEGIN}\n", sample_source()
            )
        with self.assertRaises(agents_merge.MergeError):
            agents_merge.merge_agents_text(
                f"consumer\n{agents_merge.MANAGED_END}\n", sample_source()
            )

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "AGENTS.source.md"
            target = root / "AGENTS.md"
            source.write_text(sample_source(), encoding="utf-8")
            target.write_text("# consumer\n", encoding="utf-8")
            result = agents_merge.merge_agents_file(source, target, dry_run=True)
            self.assertEqual(result["status"], "would-merge")
            self.assertEqual(target.read_text(encoding="utf-8"), "# consumer\n")

    def test_cli_reports_fail_closed_on_malformed_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "AGENTS.source.md"
            target = root / "AGENTS.md"
            source.write_text(sample_source(), encoding="utf-8")
            target.write_text(f"x\n{agents_merge.MANAGED_BEGIN}\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SKILLS / "agents_merge.py"),
                    "--source",
                    str(source),
                    "--target",
                    str(target),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 1)
            self.assertIn("fail closed", completed.stderr)


class RootAgentsNotFullyManagedTests(unittest.TestCase):
    def test_managed_pairs_exclude_root_agents(self) -> None:
        pairs = skills_update.managed_file_pairs(SKILLS, Path("."))
        destinations = {str(destination).replace("\\", "/") for _src, destination in pairs}
        self.assertNotIn("AGENTS.md", destinations)

    def _stage_consumer(self, tmp: str) -> Path:
        target = Path(tmp) / "consumer"
        target.mkdir()
        (target / "install" / "claude").mkdir(parents=True)
        shutil.copy2(
            SKILLS / "install" / "claude" / "AGENTS.md",
            target / "install" / "claude" / "AGENTS.md",
        )
        return target

    def test_consumer_edited_agents_is_not_a_managed_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = self._stage_consumer(tmp)
            source_text = (SKILLS / "install" / "claude" / "AGENTS.md").read_text(
                encoding="utf-8"
            )
            merged, _ = agents_merge.merge_agents_text(
                "# consumer own rules\n", source_text
            )
            (target / "AGENTS.md").write_text(merged, encoding="utf-8")
            self.assertIsNone(
                skills_update.agents_managed_conflict(SKILLS, target),
                msg="consumer content next to the managed block must not be a conflict",
            )

    def test_hand_edited_block_is_a_managed_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = self._stage_consumer(tmp)
            source_text = (SKILLS / "install" / "claude" / "AGENTS.md").read_text(
                encoding="utf-8"
            )
            merged, _ = agents_merge.merge_agents_text("", source_text)
            tampered = merged.replace(
                agents_merge.MANAGED_END,
                "hand edit\n" + agents_merge.MANAGED_END,
            )
            (target / "AGENTS.md").write_text(tampered, encoding="utf-8")
            self.assertIsNotNone(skills_update.agents_managed_conflict(SKILLS, target))

    def test_merge_root_agents_preserves_consumer_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = self._stage_consumer(tmp)
            consumer = "# consumer rules\n\n- keep me\n"
            (target / "AGENTS.md").write_text(consumer, encoding="utf-8")
            status = skills_update.merge_root_agents(SKILLS, target)
            self.assertEqual(status, "merged")
            text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith(consumer))
            self.assertIn(agents_merge.MANAGED_BEGIN, text)
            # Second merge is a no-op.
            self.assertEqual(skills_update.merge_root_agents(SKILLS, target), "unchanged")


if __name__ == "__main__":
    unittest.main()
