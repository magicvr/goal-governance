"""Verify actual GOAL-019 candidate or downloaded formal File assets."""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "scripts/pack_core_release.py").is_file())
sys.path.insert(0, str(ROOT / "scripts"))
from pack_core_release import assert_core_subset_of_skills_core

parser = argparse.ArgumentParser()
parser.add_argument("--asset-dir", type=Path, required=True)
parser.add_argument("--consumer-dir", type=Path, required=True)
parser.add_argument("--receipt", type=Path, required=True)
parser.add_argument("--release-metadata", type=Path)
args = parser.parse_args()
assets, consumer = args.asset_dir.resolve(), args.consumer_dir.resolve()
if not consumer.is_relative_to((ROOT / "artifacts").resolve()) or consumer.exists():
    raise SystemExit("A fresh consumer directory within artifacts is required")
version, tag = "0.15.1", "v0.15.1"
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
skills = assets / f"goal-governance-skills-{tag}.zip"
core = assets / f"goal-governance-core-{tag}.zip"
zip_checks = []
for p in (skills, core):
    expected, basename = p.with_suffix(p.suffix + ".sha256").read_text(encoding="utf-8").strip().split()
    assert basename == p.name and digest(p) == expected
    zip_checks.append(dict(name=p.name, sha256=expected))
subset = assert_core_subset_of_skills_core(core, skills, version=version)
with zipfile.ZipFile(skills) as z:
    members = [n for n in z.namelist() if not n.endswith("/")]
    rule = z.read(f"goal-governance-skills-{tag}/core/docs/architecture/principles.md")
    assert b"audit-session-lifecycle" in rule
    assert not any("/workspaces/" in n or "/mcp/" in n for n in members)
formal_checks = []
if args.release_metadata:
    release = json.loads(args.release_metadata.read_text(encoding="utf-8"))
    assert release["tag_name"] == tag and not release["draft"] and not release["prerelease"]
    expected_assets = {p.name for p in (skills, core)} | {
        skills.name + ".sha256", core.name + ".sha256", "install-online.ps1",
        "install-online.sh", "bootstrap-README.md", "release-evidence.json",
        "compatibility-report.json"}
    assert {a["name"] for a in release["assets"]} == expected_assets
    for a in release["assets"]:
        p = assets / a["name"]
        assert p.stat().st_size == a["size"] and "sha256:" + digest(p) == a["digest"]
        formal_checks.append(dict(name=p.name, size=p.stat().st_size, sha256=digest(p)))
    evidence = json.loads((assets / "release-evidence.json").read_text(encoding="utf-8"))
    assert evidence["checksPassed"] and evidence["releaseStatus"] == "release-candidate"
    assert evidence["source"]["annotatedTag"] == tag
    assert evidence["protocol"]["candidateRevision"] == tag
    report = json.loads((assets / "compatibility-report.json").read_text(encoding="utf-8"))
    assert report["coverage"]["status"] == "ready-for-release-evidence"
consumer.mkdir(parents=True)
owned = b"# Consumer owned rules\r\n\r\nExploration agents are read-only scouts.\r\n"
config = b'{\r\n  "governance_root": "docs",\r\n  "independent_audit": {"provider":"grok","model":"grok-4.7","reasoning_effort":"xhigh"}\r\n}\r\n'
(consumer / "AGENTS.md").write_bytes(owned)
(consumer / ".goal-governance.json").write_bytes(config)
bootstrap = assets / "install-online.ps1"
if not bootstrap.is_file():
    if args.release_metadata:
        raise SystemExit("Formal bootstrap asset missing")
    bootstrap = ROOT / "scripts/bootstrap/install-online.ps1"
command = [shutil.which("powershell"), "-NoProfile", "-ExecutionPolicy", "Bypass",
           "-File", str(bootstrap), "-Version", version, "-TargetDir", str(consumer),
           "-ZipPath", str(skills), "-Force"]
proc = subprocess.run(command, cwd=ROOT, capture_output=True)
args.receipt.parent.mkdir(parents=True, exist_ok=True)
args.receipt.with_suffix(".stdout.txt").write_bytes(proc.stdout)
args.receipt.with_suffix(".stderr.txt").write_bytes(proc.stderr)
assert proc.returncode == 0, "Bootstrap failed; see receipt stdout/stderr"
assert (consumer / "AGENTS.md").read_bytes().startswith(owned)
assert (consumer / ".goal-governance.json").read_bytes() == config
assert b"audit-session-lifecycle" in (consumer / "docs/architecture/principles.md").read_bytes()
assert (consumer / "docs/architecture/governance-guide.md").is_file()
receipt = dict(verifiedAt=datetime.now(timezone.utc).isoformat(), tag=tag,
               formal=bool(args.release_metadata), assetDirectory=str(assets),
               zipChecks=zip_checks, formalAssets=formal_checks,
               skillsMembers=len(members), coreSubsetMembers=len(subset),
               coreSubsetByteEqual=True, consumer=str(consumer), command=command,
               exitCode=proc.returncode, ownedAgentsCRLFBytesPreserved=True,
               projectConfigBytePreserved=True, configSha256=digest(consumer / ".goal-governance.json"),
               originalAgentsBase64=base64.b64encode(owned).decode(),
               originalConfigBase64=base64.b64encode(config).decode(),
               lifecycleRuleInstalled=True)
args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: receipt[k] for k in ("formal", "skillsMembers", "coreSubsetMembers", "exitCode", "lifecycleRuleInstalled")}))
