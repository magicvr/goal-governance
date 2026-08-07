"""L1 File channel tests (VP-004 R1): drive the REAL File channel assets.

Evidence level L1 (files): each assertion drives the actual File-channel
artifacts — the four governance entry prompts, the host install surfaces, the
install/bootstrap scripts, the AGENTS template, and the consumer contract
``deliveryChannels[files]`` entry. NO MCP mock stands in for File evidence
(VP-004 R1: L1 File 与 L1 MCP 分列；禁止用 MCP mock 顶替厚 File 入口证据).
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"
PROMPTS = SKILLS / "prompts"
CONTRACTS = REPO_ROOT / "docs" / "contracts"

sys.path.insert(0, str(SKILLS / "mcp" / ".."))  # skills/ on path -> import mcp.*
import mcp.kernel as kernel  # noqa: E402

# Entry -> prompt file -> role frontmatter marker.
ENTRY_PROMPTS = {
    "vision": ("06-vision-orchestrator.md", "vision-decision"),
    "vision-audit": ("07-independent-vision-review.md", "independent-vision-review"),
    "govern": ("00-govern-orchestrator.md", "primary"),
    "audit": ("05-independent-audit.md", "independent-audit"),
}
HOST_SKILL_DIRS = ("claude", "grok", "codex")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise ValueError("missing frontmatter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


class FileChannelL1Tests(unittest.TestCase):
    """L1 File: four entry prompts + host surfaces + contract files entry."""

    def test_four_entry_prompts_exist_with_role_boundaries(self) -> None:
        for entry, (filename, role_marker) in ENTRY_PROMPTS.items():
            path = PROMPTS / filename
            self.assertTrue(path.is_file(), msg=f"missing File prompt: {path}")
            fields = parse_frontmatter(path.read_text(encoding="utf-8"))
            self.assertIn("role", fields, msg=f"{entry} prompt lacks role frontmatter")
            self.assertEqual(fields["role"], role_marker, msg=f"{entry} role marker")
            self.assertIn("status", fields)
            self.assertIn(fields["status"], {"active", "draft", "done", "cancelled", "blocked"})

    def test_host_install_surfaces_cover_all_four_entries(self) -> None:
        for host in HOST_SKILL_DIRS:
            for entry in kernel.ENTRYPOINT_NAMES:
                skill = SKILLS / "install" / host / "skills" / entry / "SKILL.md"
                self.assertTrue(skill.is_file(), msg=f"missing {host}/{entry} skill")

    def test_copilot_prompt_surface_covers_four_entries(self) -> None:
        for entry in kernel.ENTRYPOINT_NAMES:
            path = SKILLS / "install" / "copilot" / "prompts" / f"{entry}.md"
            self.assertTrue(path.is_file(), msg=f"missing copilot {entry} prompt")

    def test_install_and_bootstrap_scripts_exist(self) -> None:
        for rel in (
            "skills/install.sh",
            "skills/install.ps1",
            "skills/update.sh",
            "skills/update.ps1",
            "scripts/bootstrap/install-online.sh",
            "scripts/bootstrap/install-online.ps1",
            "skills/AGENTS.template.md",
        ):
            self.assertTrue((REPO_ROOT / rel).is_file(), msg=f"missing File asset: {rel}")

    def test_file_channel_description_is_backed_by_real_assets(self) -> None:
        file_desc = kernel.describe_file_channel(REPO_ROOT)
        self.assertEqual(file_desc.channel, "files")
        self.assertTrue(file_desc.file_self_bootstrap)
        for name in kernel.ENTRYPOINT_NAMES:
            spec = file_desc.entrypoints[name]
            self.assertTrue(spec["prompt_present"], msg=f"{name} not backed by a prompt")

    def test_consumer_contract_splits_files_channel_with_evidence_levels(self) -> None:
        contract = json.loads(
            (CONTRACTS / "skills-consumer-contract.json").read_text(encoding="utf-8")
        )
        channels = {item["channel"]: item for item in contract["deliveryChannels"]}
        self.assertIn("files", channels)
        files = channels["files"]
        self.assertEqual(files["status"], "first-class")
        self.assertEqual(set(files["evidenceLevels"]), {"L1", "L2", "L3"})
        self.assertEqual(set(files["entrypoints"]), set(kernel.ENTRYPOINT_NAMES))
        # File 通道不依赖 MCP 运行时：声明 File-classic（无 Docker / 无 MCP）可用。
        self.assertIn("File-classic", files["runtime"])
        self.assertNotIn("MCP stdio", files["runtime"])

    def test_contract_host_entrypoints_match_file_prompt_surface(self) -> None:
        contract = json.loads(
            (CONTRACTS / "skills-consumer-contract.json").read_text(encoding="utf-8")
        )
        host_entrypoints = set(contract["protocol"]["publicContract"]["hostEntrypoints"])
        self.assertEqual(host_entrypoints, set(kernel.ENTRYPOINT_NAMES))


if __name__ == "__main__":
    unittest.main()
