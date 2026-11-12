"""GOAL-018 evidence helper: use the registered Grok profile, exact AD body."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "mcp/config.py").is_file())
sys.path.insert(0, str(ROOT))
from mcp.config import resolve_independent_audit, independent_audit_argv

parser = argparse.ArgumentParser()
parser.add_argument("--attempt", required=True)
parser.add_argument("--timeout", type=int, default=600)
args = parser.parse_args()
if not args.attempt.isascii() or not args.attempt.replace("-", "").isalnum():
    raise SystemExit("attempt must be a simple ASCII label")
out = HERE / "independent-captures" / args.attempt
out.mkdir(parents=True, exist_ok=False)
profile = resolve_independent_audit(ROOT)
if profile is None or profile["provider"] != "grok":
    raise SystemExit("This goal evidence helper requires the registered Grok provider; no fallback")
body = "/audit workspace-002 goal-018"
command = independent_audit_argv(profile)
command[0] = shutil.which(command[0]) or command[0]
command += ["--single", body, "--output-format", "streaming-json", "--permission-mode", "bypassPermissions", "--no-subagents", "--disable-web-search"]
spec = importlib.util.spec_from_file_location("goal018_probe", HERE / "s3-host-probes.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
started = datetime.now(timezone.utc).isoformat()
env = os.environ.copy()
env.update(CI="1", NO_COLOR="1")
proc = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
timed_out = False
try:
    stdout, stderr = proc.communicate(timeout=args.timeout)
except subprocess.TimeoutExpired:
    timed_out = True
    subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, check=False)
    stdout, stderr = proc.communicate()
(out / "stdout.jsonl").write_text(module.grok_transcript(stdout.decode("utf-8", errors="replace")), encoding="utf-8")
(out / "stderr.txt").write_text(module._redact_request_urls(stderr.decode("utf-8", errors="replace")), encoding="utf-8")
record = dict(startedAt=started, finishedAt=datetime.now(timezone.utc).isoformat(), configSource=".goal-governance.json", configSha256=hashlib.sha256((ROOT / ".goal-governance.json").read_bytes()).hexdigest(), profile=profile, command=command, body=body, cleanConversation=True, copiedHistory=False, exitCode=proc.returncode, timedOut=timed_out)
(out / "invocation.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: record[k] for k in ("profile", "exitCode", "timedOut")}), flush=True)
raise SystemExit(1 if timed_out else proc.returncode)
