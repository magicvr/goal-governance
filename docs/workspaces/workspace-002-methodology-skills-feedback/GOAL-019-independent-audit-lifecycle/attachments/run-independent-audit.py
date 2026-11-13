"""Invoke the registered formal auditor without an inherited scout cutoff.

The main session monitors this process. Only the exact AD command is sent;
no conversation, scope, file list or desired verdict is supplied.
"""
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
args = parser.parse_args()
if not args.attempt.isascii() or not args.attempt.replace("-", "").isalnum():
    raise SystemExit("attempt must be a simple ASCII label")
profile = resolve_independent_audit(ROOT)
if profile is None or profile["provider"] != "grok":
    raise SystemExit("Registered Grok profile required; no fallback")
out = HERE / "independent-captures" / args.attempt
out.mkdir(parents=True, exist_ok=False)
body = "/audit workspace-002 goal-019"
command = independent_audit_argv(profile)
command[0] = shutil.which(command[0]) or command[0]
command += ["--single", body, "--output-format", "streaming-json",
            "--permission-mode", "bypassPermissions", "--no-subagents",
            "--disable-web-search"]
spec = importlib.util.spec_from_file_location("goal019_probe", HERE / "s3-host-probes.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
env = os.environ.copy()
env.update(CI="1", NO_COLOR="1")
started = datetime.now(timezone.utc).isoformat()
proc = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, env=env)
record = dict(startedAt=started, configSource=".goal-governance.json",
              configSha256=hashlib.sha256((ROOT / ".goal-governance.json").read_bytes()).hexdigest(),
              profile=profile, command=command, body=body, pid=proc.pid,
              cleanConversation=True, copiedHistory=False,
              wallClockLimit=None, state="running")
def save_record():
    (out / "invocation.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
save_record()
print(json.dumps(dict(state="running", pid=proc.pid, profile=profile)), flush=True)
stdout, stderr = proc.communicate()
(out / "stdout.jsonl").write_text(
    module.grok_transcript(stdout.decode("utf-8", errors="replace")), encoding="utf-8")
(out / "stderr.txt").write_text(
    module._redact_request_urls(stderr.decode("utf-8", errors="replace")), encoding="utf-8")
record.update(finishedAt=datetime.now(timezone.utc).isoformat(),
              state="exited", exitCode=proc.returncode, timedOut=False)
save_record()
print(json.dumps(dict(state="exited", exitCode=proc.returncode,
                      timedOut=False)), flush=True)
raise SystemExit(proc.returncode)
