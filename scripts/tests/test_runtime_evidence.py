from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


capture_runtime_evidence = _load_module(
    "capture_runtime_evidence",
    SCRIPTS / "capture_runtime_evidence.py",
)
compatibility_report = _load_module(
    "runtime_compatibility_report",
    SCRIPTS / "compatibility_report.py",
)


class RuntimeEvidenceTests(unittest.TestCase):
    maxDiff = None

    @staticmethod
    def _prepare_capture_root(root: Path) -> None:
        schema_dir = root / "docs/contracts"
        schema_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            REPO_ROOT / "docs/contracts/runtime-evidence.schema.json",
            schema_dir / "runtime-evidence.schema.json",
        )
        (root / "behavior.md").write_text("behavior source\n", encoding="utf-8")

    @staticmethod
    def _capture(
        root: Path,
        *,
        marker: str = "RUNTIME_MARKER",
        script: str | None = None,
        output_name: str = "runtime.json",
        timeout_seconds: float = 120,
    ) -> tuple[Path, dict[str, object]]:
        command_script = script or (
            "import sys; sys.stdin.read(); "
            "print('RUNTIME_MARKER'); print('runtime warning', file=sys.stderr)"
        )
        output = root / output_name
        payload = capture_runtime_evidence.capture(
            consumer="test-host",
            entrypoint="govern",
            protocol_version="0.1.0",
            product="Test Host",
            product_version="1.0.0",
            provider=None,
            model=None,
            prompt="/govern test\n",
            marker=marker,
            behavior_sources=["behavior.md"],
            command=[sys.executable, "-c", command_script],
            output=output,
            root=root,
            timeout_seconds=timeout_seconds,
        )
        return output, payload

    @staticmethod
    def _runtime_schema(root: Path) -> dict[str, object]:
        return json.loads(
            (root / "docs/contracts/runtime-evidence.schema.json").read_text(
                encoding="utf-8"
            )
        )

    @staticmethod
    def _matrix_fixture(root: Path) -> tuple[dict[str, object], dict[str, object]]:
        destination = root / "docs/contracts"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(REPO_ROOT / "docs/contracts", destination)
        contract = json.loads(
            (destination / "skills-consumer-contract.json").read_text(encoding="utf-8")
        )
        matrix = json.loads(
            (destination / "skills-consumer-compatibility-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        for consumer in matrix["consumers"]:
            for entrypoint in consumer["entrypoints"]:
                entrypoint["evidence"] = []
                if consumer["kind"] == "host-adapter":
                    entrypoint["status"] = "pending-runtime-validation"
                else:
                    entrypoint["status"] = "pending-ci-replay"
        return contract, matrix

    def test_cli_accepts_vision_entrypoint_choice(self) -> None:
        """Shipped capture CLI must accept unit.entrypoint=vision (P-006 decision layer)."""
        # Drive real argparse path: vision is a legal choice; missing files yield return 1.
        code = capture_runtime_evidence.main(
            [
                "--consumer",
                "test",
                "--entrypoint",
                "vision",
                "--protocol-version",
                "0.1.0",
                "--product",
                "Test",
                "--product-version",
                "1",
                "--prompt-file",
                "missing-prompt.txt",
                "--marker",
                "M",
                "--behavior-source",
                "missing.md",
                "--output",
                "out.json",
                "--",
                sys.executable,
                "-c",
                "pass",
            ]
        )
        self.assertEqual(code, 1)

    def test_capture_api_accepts_vision_entrypoint_and_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-runtime-vision-") as tmp:
            root = Path(tmp)
            self._prepare_capture_root(root)
            output = root / "vision.json"
            payload = capture_runtime_evidence.capture(
                consumer="test-host",
                entrypoint="vision",
                protocol_version="0.1.0",
                product="Test Host",
                product_version="1.0.0",
                provider=None,
                model=None,
                prompt="/vision test\n",
                marker="VISION_MARKER",
                behavior_sources=["behavior.md"],
                command=[
                    sys.executable,
                    "-c",
                    "import sys; sys.stdin.read(); print('VISION_MARKER')",
                ],
                output=output,
                root=root,
            )
            self.assertEqual(payload["unit"]["entrypoint"], "vision")
            self.assertEqual(payload["result"]["verdict"], "pass")
            Draft202012Validator(
                self._runtime_schema(root),
                format_checker=FormatChecker(),
            ).validate(payload)

    def test_cli_accepts_vision_audit_entrypoint_choice(self) -> None:
        """Shipped capture CLI must accept the independent vision-audit entrypoint."""
        # Drive the real argparse path: the accepted choice then fails only on the missing input.
        code = capture_runtime_evidence.main(
            [
                "--consumer",
                "test",
                "--entrypoint",
                "vision-audit",
                "--protocol-version",
                "0.1.0",
                "--product",
                "Test",
                "--product-version",
                "1",
                "--prompt-file",
                "missing-prompt.txt",
                "--marker",
                "M",
                "--behavior-source",
                "missing.md",
                "--output",
                "out.json",
                "--",
                sys.executable,
                "-c",
                "pass",
            ]
        )
        self.assertEqual(code, 1)

    def test_capture_api_accepts_vision_audit_entrypoint_and_validates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-runtime-vision-audit-") as tmp:
            root = Path(tmp)
            self._prepare_capture_root(root)
            output = root / "vision-audit.json"
            payload = capture_runtime_evidence.capture(
                consumer="test-host",
                entrypoint="vision-audit",
                protocol_version="0.1.0",
                product="Test Host",
                product_version="1.0.0",
                provider=None,
                model=None,
                prompt="/vision-audit alignment\n",
                marker="VISION_AUDIT_MARKER",
                behavior_sources=["behavior.md"],
                command=[
                    sys.executable,
                    "-c",
                    "import sys; sys.stdin.read(); print('VISION_AUDIT_MARKER')",
                ],
                output=output,
                root=root,
            )
            self.assertEqual(payload["unit"]["entrypoint"], "vision-audit")
            self.assertEqual(payload["result"]["verdict"], "pass")
            Draft202012Validator(
                self._runtime_schema(root),
                format_checker=FormatChecker(),
            ).validate(payload)

    def test_capture_writes_schema_valid_payload_and_raw_digests(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-runtime-capture-") as tmp:
            root = Path(tmp)
            self._prepare_capture_root(root)
            output, payload = self._capture(root)
            persisted = json.loads(output.read_text(encoding="utf-8"))
            schema = self._runtime_schema(root)

            Draft202012Validator(
                schema,
                format_checker=FormatChecker(),
            ).validate(persisted)
            self.assertEqual(payload, persisted)
            self.assertEqual(persisted["invocation"]["command"][0], "python")
            self.assertEqual(persisted["invocation"]["timeoutSeconds"], 120)
            self.assertEqual(persisted["result"]["verdict"], "pass")
            self.assertEqual(persisted["result"]["stdoutMode"], "raw")
            self.assertEqual(persisted["result"]["stderrMode"], "raw")
            for label in ("stdout", "stderr"):
                raw_path = root / persisted["result"][f"{label}Path"]
                self.assertTrue(raw_path.is_file())
                self.assertEqual(
                    persisted["result"][f"{label}Sha256"],
                    sha256(raw_path.read_bytes()).hexdigest(),
                )

    def test_capture_records_fail_without_required_exit_and_marker(self) -> None:
        cases = (
            ("missing marker", "import sys; sys.stdin.read(); print('other')", 0, False),
            (
                "nonzero exit",
                "import sys; sys.stdin.read(); print('RUNTIME_MARKER'); raise SystemExit(3)",
                3,
                True,
            ),
        )
        for label, script, exit_code, marker_observed in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix="gg-runtime-fail-"
            ) as tmp:
                root = Path(tmp)
                self._prepare_capture_root(root)
                _, payload = self._capture(root, script=script)
                self.assertEqual(payload["result"]["verdict"], "fail")
                self.assertEqual(payload["result"]["exitCode"], exit_code)
                self.assertEqual(
                    payload["result"]["markerObserved"], marker_observed
                )

    def test_capture_records_blocked_timeout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-runtime-timeout-") as tmp:
            root = Path(tmp)
            self._prepare_capture_root(root)
            _, payload = self._capture(
                root,
                script="import time; time.sleep(2)",
                timeout_seconds=0.05,
            )

            self.assertEqual(payload["result"]["verdict"], "blocked")
            self.assertEqual(payload["result"]["exitCode"], 124)
            self.assertFalse(payload["result"]["markerObserved"])
            self.assertIn("timed out", payload["result"]["warnings"][0])

    def test_claude_stream_sanitizer_omits_thinking_and_tool_result_content(self) -> None:
        events = [
            {
                "type": "system",
                "subtype": "init",
                "session_id": "session-1",
                "cwd": ".",
                "tools": ["Read"],
                "model": "test-model",
                "permissionMode": "plan",
                "slash_commands": ["govern"],
                "claude_code_version": "2.1.215",
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "thinking", "thinking": "private", "signature": "secret"},
                        {
                            "type": "tool_use",
                            "id": "tool-1",
                            "name": "Read",
                            "input": {"file_path": "AGENTS.md"},
                        },
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "tool-1",
                            "content": "full private file content",
                        }
                    ]
                },
                "tool_use_result": {"numLines": 10, "content": "also private"},
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "CLAUDE_GOVERN_DISPATCH_OK"}
                    ]
                },
            },
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "duration_ms": 10,
                "num_turns": 1,
                "result": "CLAUDE_GOVERN_DISPATCH_OK",
                "stop_reason": "end_turn",
                "terminal_reason": "completed",
                "permission_denials": [],
            },
        ]
        raw = "".join(json.dumps(event) + "\n" for event in events)

        sanitized = capture_runtime_evidence._sanitize_claude_stream(raw)
        transcript = [json.loads(line) for line in sanitized.splitlines()]

        self.assertNotIn("private", sanitized)
        self.assertNotIn("signature", sanitized)
        self.assertEqual(transcript[0]["event"], "session-init")
        self.assertEqual(transcript[1]["event"], "tool-call")
        self.assertEqual(transcript[2]["event"], "tool-result")
        self.assertEqual(transcript[2]["metadata"], {"numLines": 10})
        self.assertEqual(transcript[-1]["event"], "process-result")
        self.assertIn("CLAUDE_GOVERN_DISPATCH_OK", sanitized)

    def test_request_url_redaction_preserves_error_without_private_endpoint(self) -> None:
        stderr = (
            "unknown provider for model grok-build\n\n"
            "Request URL: http://192.168.1.50:8317/v1/responses\n"
            "Response headers:\n"
        )

        redacted = capture_runtime_evidence._redact_request_urls(stderr)

        self.assertIn("unknown provider for model grok-build", redacted)
        self.assertIn("Request URL: <redacted>", redacted)
        self.assertNotIn("192.168.1.50", redacted)

    def test_behavior_source_digest_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-runtime-source-") as tmp:
            root = Path(tmp)
            self._prepare_capture_root(root)
            output, _ = self._capture(root)
            (root / "behavior.md").write_text("changed behavior\n", encoding="utf-8")

            with self.assertRaisesRegex(
                compatibility_report.ValidationError,
                "behavior source is stale",
            ):
                compatibility_report._validate_runtime_evidence(
                    root,
                    output,
                    self._runtime_schema(root),
                    "test-host",
                    "govern",
                    "0.1.0",
                )

    def test_raw_output_digest_tampering_is_rejected(self) -> None:
        for label in ("stdout", "stderr"):
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix=f"gg-runtime-{label}-"
            ) as tmp:
                root = Path(tmp)
                self._prepare_capture_root(root)
                output, payload = self._capture(root)
                raw_path = root / payload["result"][f"{label}Path"]
                raw_path.write_text(
                    raw_path.read_text(encoding="utf-8") + "tampered\n",
                    encoding="utf-8",
                )

                with self.assertRaisesRegex(
                    compatibility_report.ValidationError,
                    f"{label} digest is stale",
                ):
                    compatibility_report._validate_runtime_evidence(
                        root,
                        output,
                        self._runtime_schema(root),
                        "test-host",
                        "govern",
                        "0.1.0",
                    )

    def test_runtime_verified_requires_valid_machine_readable_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-runtime-matrix-") as tmp:
            root = Path(tmp)
            contract, matrix = self._matrix_fixture(root)
            target = matrix["consumers"][0]["entrypoints"][0]
            target["status"] = "runtime-verified"
            target["evidence"] = ["runtime/invalid.json"]
            evidence = root / "runtime/invalid.json"
            evidence.parent.mkdir(parents=True, exist_ok=True)

            evidence.write_text("{not-json}\n", encoding="utf-8")
            with self.assertRaisesRegex(
                compatibility_report.ValidationError,
                "invalid JSON",
            ):
                compatibility_report.validate_inputs(contract, deepcopy(matrix), root)

            evidence.write_text(
                json.dumps({"format": "goal-governance.host-runtime-evidence"}) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                compatibility_report.ValidationError,
                "runtime evidence schema validation failed",
            ):
                compatibility_report.validate_inputs(contract, deepcopy(matrix), root)


if __name__ == "__main__":
    unittest.main()
