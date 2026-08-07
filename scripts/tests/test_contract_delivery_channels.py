"""Contract `deliveryChannel: files | mcp` split tests (VP-004 R1).

Validates that the consumer contract and compatibility matrix carry the
dual-channel split with L1/L2/L3 evidence levels, that both the existing File
assets and the new MCP assets validate against the updated schema, and that the
files/mcp split does not conflict with the pre-existing File contract shape
(protocol, adapters, supportBaseline semantics unchanged).
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = REPO_ROOT / "docs" / "contracts"
SKILLS_CONTRACTS = REPO_ROOT / "skills" / "contracts"

# Make `import mcp.kernel` resolve for entrypoint-name constants.
sys.path.insert(0, str(REPO_ROOT / "skills"))
import mcp.kernel as kernel  # noqa: E402


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator(schema_path: Path) -> Draft202012Validator:
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


class ContractDeliveryChannelsTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.contract = _load_json(CONTRACTS / "skills-consumer-contract.json")
        self.schema_path = CONTRACTS / "skills-consumer-contract.schema.json"
        self.matrix = _load_json(CONTRACTS / "skills-consumer-compatibility-matrix.json")
        self.matrix_schema_path = CONTRACTS / "skills-consumer-compatibility-matrix.schema.json"

    def _channels(self, payload: dict) -> dict[str, dict]:
        return {item["channel"]: item for item in payload["deliveryChannels"]}

    def test_contract_validates_and_splits_files_and_mcp(self) -> None:
        validator = _validator(self.schema_path)
        errors = sorted(validator.iter_errors(self.contract), key=lambda e: list(e.absolute_path))
        self.assertEqual(errors, [], msg=f"contract schema errors: {errors[:3]}")
        channels = self._channels(self.contract)
        self.assertEqual(set(channels), {"files", "mcp"})
        for channel, item in channels.items():
            self.assertEqual(item["status"], "first-class")
            self.assertEqual(set(item["evidenceLevels"]), {"L1", "L2", "L3"})
            self.assertEqual(set(item["entrypoints"]), set(kernel.ENTRYPOINT_NAMES))

    def test_format_version_bumped_for_split(self) -> None:
        self.assertEqual(self.contract["contractFormatVersion"], "0.4.0")

    def test_matrix_validates_and_splits_channels(self) -> None:
        validator = _validator(self.matrix_schema_path)
        errors = sorted(validator.iter_errors(self.matrix), key=lambda e: list(e.absolute_path))
        self.assertEqual(errors, [], msg=f"matrix schema errors: {errors[:3]}")
        channels = self._channels(self.matrix)
        self.assertEqual(set(channels), {"files", "mcp"})

    def test_contract_mirror_is_byte_identical(self) -> None:
        for name in (
            "skills-consumer-contract.json",
            "skills-consumer-contract.schema.json",
            "skills-consumer-compatibility-matrix.json",
            "skills-consumer-compatibility-matrix.schema.json",
        ):
            canonical = (CONTRACTS / name).read_bytes()
            mirror = (SKILLS_CONTRACTS / name).read_bytes()
            self.assertEqual(
                mirror, canonical, msg=f"skills/contracts mirror drift: {name}"
            )

    def test_legacy_file_contract_shape_unchanged(self) -> None:
        """Existing File contract semantics must not conflict with the split."""
        self.assertEqual(self.contract["contractFormat"], "goal-governance.skills-consumer-contract")
        self.assertEqual(self.contract["protocol"]["version"], "0.1.0")
        self.assertEqual(
            self.contract["supportBaseline"],
            {"firstSupportedProtocol": "0.1.0", "previousSupportedProtocol": None},
        )
        self.assertEqual(
            set(self.contract["protocol"]["publicContract"]["hostEntrypoints"]),
            set(kernel.ENTRYPOINT_NAMES),
        )
        self.assertTrue(self.contract["adapters"], msg="adapters must remain populated")

    def test_missing_delivery_channels_fails_schema(self) -> None:
        validator = _validator(self.schema_path)
        broken = copy.deepcopy(self.contract)
        del broken["deliveryChannels"]
        errors = list(validator.iter_errors(broken))
        self.assertTrue(errors, msg="schema must require deliveryChannels")

    def test_mcp_channel_rejects_docker_only_claim(self) -> None:
        """VP-004: MCP must not be Docker-only; stdio runtime must be declared."""
        mcp = self._channels(self.contract)["mcp"]
        runtime = mcp["runtime"].lower()
        self.assertIn("stdio", runtime)
        self.assertNotIn("docker-only", runtime)

    def test_valid_fixtures_still_validate_with_split(self) -> None:
        validator = _validator(self.schema_path)
        for name in ("manifest-0.1.0.json", "declared-adapter-0.1.0.json"):
            fixture = _load_json(CONTRACTS / "fixtures" / "valid" / name)
            errors = list(validator.iter_errors(fixture))
            self.assertEqual(errors, [], msg=f"{name} schema errors: {errors[:3]}")
            channels = self._channels(fixture)
            self.assertEqual(set(channels), {"files", "mcp"}, msg=name)


if __name__ == "__main__":
    unittest.main()
