"""Remove provider-only reasoning fields; preserve actual public/tool events.

Post-capture representation processing, not another host run or a verdict edit.
Keep before/after digests and refresh only hashes of the processed representation.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "scripts/capture_runtime_evidence.py").is_file())
REMOVED = {"reasoningText", "thinking", "thought", "signature"}


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k not in REMOVED}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def sha(data):
    return hashlib.sha256(data).hexdigest()


changes = []
for path in sorted((HERE / "s3-runtime").glob("*/stdout.jsonl")):
    before = path.read_bytes()
    events = [json.loads(line) for line in before.decode("utf-8").splitlines() if line.strip()]
    result = [clean(event) for event in events]
    if result == events:
        continue
    after = ("".join(json.dumps(event, ensure_ascii=False) + "\n" for event in result)).encode("utf-8")
    path.write_bytes(after)
    obs_path = path.parent / "observation.json"
    obs = json.loads(obs_path.read_text(encoding="utf-8"))
    obs["stdoutSha256"] = sha(after)
    obs["representationProcessing"] = "Removed provider-only reasoningText/thinking/thought/signature JSON fields; public content and tool events unchanged"
    obs_path.write_text(json.dumps(obs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    changes.append(dict(path=path.relative_to(ROOT).as_posix(), originalSha256=sha(before), sanitizedSha256=sha(after), removedFields=sorted(REMOVED)))
    for envelope in sorted((ROOT / "docs/releases/runtime/v0.16.0").glob("*.json")):
        payload = json.loads(envelope.read_text(encoding="utf-8"))
        if path.parent.relative_to(ROOT).as_posix() not in payload["invocation"]["inputSummary"]:
            continue
        raw = ROOT / payload["result"]["stdoutPath"]
        assert raw.resolve().is_relative_to(ROOT.resolve())
        raw.write_bytes(after)
        payload["result"]["stdoutSha256"] = sha(after)
        payload["result"]["warnings"].append(obs["representationProcessing"])
        payload["behaviorSources"].append(dict(path=Path(__file__).relative_to(ROOT).as_posix(), sha256=sha(Path(__file__).read_bytes().replace(b"\r\n", b"\n"))))
        envelope.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
receipt = HERE / "s3-representation-processing.json"
if changes:
    assert not receipt.exists(), "Preserve the previous processing receipt"
    receipt.write_text(json.dumps(dict(scope="Archive-only field removal; no host invocation or audit verdict changed", files=changes), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"Processed {len(changes)} archived streams")
