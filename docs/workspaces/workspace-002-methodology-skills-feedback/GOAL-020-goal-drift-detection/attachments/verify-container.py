"""Verify the actual published image digest, version and read-only MCP guidance."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

parser = argparse.ArgumentParser()
parser.add_argument("--consumer-dir", type=Path, required=True)
parser.add_argument("--expected-digest", required=True)
parser.add_argument("--receipt", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve()
repo = next(p for p in root.parents if (p / "scripts/pack_skills_release.py").is_file())
consumer = args.consumer_dir.resolve()
assert consumer.is_dir() and consumer.is_relative_to((repo / "artifacts").resolve())
image = "ghcr.io/magicvr/goal-governance-mcp-server"
tag = "0.16.0"
assert args.expected_digest.startswith("sha256:") and len(args.expected_digest) == 71
pull = subprocess.run(["docker", "pull", f"{image}:{tag}"], capture_output=True)
assert pull.returncode == 0, pull.stderr.decode(errors="replace")
actual = json.loads(subprocess.check_output(["docker", "image", "inspect", f"{image}:{tag}"]))[0]
assert f"{image}@{args.expected_digest}" in actual["RepoDigests"]
requests = [
    dict(jsonrpc="2.0", id=1, method="initialize", params=dict(protocolVersion="2025-03-26", capabilities={}, clientInfo=dict(name="goal020-release-acceptance", version="1.0.0"))),
    dict(jsonrpc="2.0", id=2, method="tools/list", params={}),
    dict(jsonrpc="2.0", id=3, method="tools/call", params=dict(name="audit", arguments=dict(task="/audit workspace-002 goal-020", goal_id="GOAL-020-goal-drift-detection"))),
    dict(jsonrpc="2.0", id=4, method="tools/call", params=dict(name="govern", arguments=dict(task="Inspect current goal guidance"))),
]
before = {p.relative_to(consumer).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in consumer.rglob("*") if p.is_file()}
command = ["docker", "run", "--rm", "-i", "--mount", f"type=bind,source={consumer},target=/workspace,readonly", f"{image}@{args.expected_digest}"]
proc = subprocess.run(command, input="".join(json.dumps(r) + "\n" for r in requests).encode(), capture_output=True)
assert proc.returncode == 0, proc.stderr.decode(errors="replace")
responses = [json.loads(line) for line in proc.stdout.decode("utf-8").splitlines() if line.strip()]
assert len(responses) == 4 and all("error" not in r for r in responses)
assert responses[0]["result"]["serverInfo"]["version"] == tag
assert {"govern", "audit", "vision", "vision-audit"}.issubset({t["name"] for t in responses[1]["result"]["tools"]})
for response in responses[2:]:
    data = response["result"]["structuredContent"]
    assert data["status"] == "ok" and "GD-01～GD-08" in data["guidance"]
    assert "principles.md#goal-drift" in data["guidance"]
after = {p.relative_to(consumer).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in consumer.rglob("*") if p.is_file()}
assert before == after
receipt = dict(verifiedAt=datetime.now(timezone.utc).isoformat(), image=image, tag=tag,
               expectedDigestFromWorkflowLog=args.expected_digest, pulledRepoDigests=actual["RepoDigests"],
               command=command, readOnlyConsumerMount=True, consumerBytesUnchanged=True,
               exitCode=proc.returncode, serverVersion=tag, requests=requests, responses=responses,
               stdoutSha256=hashlib.sha256(proc.stdout).hexdigest(), stderrSha256=hashlib.sha256(proc.stderr).hexdigest(),
               scope="Published GHCR artifact digest/version and read-only MCP catalog/guidance; no independent audit execution or Goal state write")
args.receipt.parent.mkdir(parents=True, exist_ok=True)
args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(dict(digest=args.expected_digest, version=tag, exitCode=proc.returncode, readOnlyConsumerMount=True)))
