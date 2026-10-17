"""GOAL-013 S3 isolated experiments; not a production provider runner.

No test event is a human answer. Audit bodies are exact formal commands.
Each experiment gets a fresh temporary consumer repository and conversation.
Run from the producer repository with --host and --case. Outputs remain in
this attachment's s3-runtime directory; temporary repositories are retained.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "scripts/capture_runtime_evidence.py").is_file())
sys.path.insert(0, str(ROOT / "scripts"))
from capture_runtime_evidence import (
    _sanitize_claude_stream, _redact_request_urls, _validate,
    build_default_assertions, evaluate_assertions, assertions_all_observed,
)

WS = "workspace-002-synthetic"
RG = "GOAL-001-synthetic-root"
GG = "GOAL-013-synthetic-counter"
VP = "VP-002-synthetic-counter"
TODAY = datetime.now().astimezone().date().isoformat()


def put(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def doc(body: str, **fields: object) -> str:
    values = dict(status="active", created=TODAY, updated=TODAY, parent=None, version="0.1.0")
    values.update(fields)
    return "---\n" + "".join(f"{k}: {'null' if v is None else v}\n" for k, v in values.items()) + "---\n\n" + body + "\n"


def fixture(mode: str) -> Path:
    target = Path(tempfile.mkdtemp(prefix="gg-goal013-s3-"))
    # Only standard installed rules/entrypoints accompany audit commands.
    shutil.copy2(ROOT / "skills/AGENTS.template.md", target / "AGENTS.md")
    text = (target / "AGENTS.md").read_text(encoding="utf-8")
    put(target / "AGENTS.md", text.replace("{{SKILLS_DIR}}", "skills").replace("{{GOVERNANCE_ROOT}}", "docs"))
    for folder in ("prompts", "templates", "contracts"):
        shutil.copytree(ROOT / "skills" / folder, target / "skills" / folder)
    shutil.copytree(ROOT / "skills/core/docs", target / "docs", dirs_exist_ok=True)
    for name in ("skills-consumer-contract.json", "skills-consumer-contract.schema.json"):
        destination = target / "docs/contracts" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "skills/contracts" / name, destination)
    for host, directory in (("claude", ".claude"), ("grok", ".grok"), ("codex", ".agents")):
        shutil.copytree(ROOT / f"skills/install/{host}/skills", target / directory / "skills")
    for entry in ("govern", "audit", "vision", "vision-audit"):
        shutil.copy2(ROOT / f"skills/install/copilot/prompts/{entry}.md", target / f"copilot-{entry}.md")
    (target / ".github/prompts").mkdir(parents=True)
    for entry in ("govern", "audit", "vision", "vision-audit"):
        shutil.copy2(target / f"copilot-{entry}.md", target / f".github/prompts/{entry}.prompt.md")
    shutil.copy2(ROOT / "skills/install/copilot/copilot-instructions.md", target / ".github/copilot-instructions.md")
    put(target / ".goal-governance.json", '{"governance_root":"docs"}\n')
    vr = target / "docs/vision"
    put(vr / "charter.md", doc("# Charter · 合成计数器实验\n\n## 目的陈述\n提供可解释的本地文本计数工具。\n\n## 方向级成功边界\n计数含义清楚；输出可复核；只处理本地文本。\n\n## 非目标\n云服务、账号系统和远程发布。\n\n## 原则\n遵循 P-001～P-006，未知项不伪装为结论。", doc_type="vision-charter", vision_id="vision-synthetic-counter", title="合成计数器实验", effective_date="2026-10-16", primary_workspace=WS))
    put(vr / f"plans/{VP}.md", doc(f"# {VP}\n\n## 意图\n建立含义明确、可复核的本地文本计数能力。\n\n## 方向级退出判据\n语义与结果可核对，相关用户选择可追溯。\n\n## 工作区绑定\n| workspace_id | root_goal | role | joined | notes |\n|---|---|---|---|---|\n| {WS} | {RG} | lead | 2026-10-16 | 合成隔离实验 |", doc_type="vision-plan", id=VP, title="本地计数能力", vision_ref="vision-synthetic-counter@0.1.0", lead_workspace=WS))
    for name, body in {
        "README": "# 合成愿景\n单一 Charter，VP 是意图权威，目标事实在工作区。",
        "roadmap": f"# 组合编排\n| VP | status | vision_ref | lead_workspace |\n|---|---|---|---|\n| [{VP}](plans/{VP}.md) | active | vision-synthetic-counter@0.1.0 | {WS} |\n列为 VP frontmatter 的派生投影。",
        "workspaces": f"# 工作区绑定\n[{WS}](../workspaces/{WS}/workspace.md) 服务 {VP}，role: primary。",
        "revisions": "# 修订\n2026-10-16 初建；无 strategic 修订或待 re-align。",
        "reviews": "# 愿景审视索引\n\n| ID | source | scope | verdict | open required | report |\n|---|---|---|---|---|---|\n\n暂无审视；未宣称方向已稳。",
    }.items():
        put(vr / f"{name}.md", doc(body))
    (vr / "reviews").mkdir(exist_ok=True)
    alignment = (vr / "alignment.md").read_text(encoding="utf-8")
    must_table = alignment.split("| 层级 | 路径 / 条件 | 级别 | 说明 |", 1)[1].split("**半安装**", 1)[0]
    put(vr / "consumer-checklist.md", doc("# 合成消费仓完整性核对\n\n完整安装唯一权威为 alignment §0.2；本表逐行引用该权威，不新增或放宽门禁。\n\n| 层级 | 路径 / 条件 | 级别 | 说明 |" + must_table))
    work = target / "docs/workspaces" / WS
    put(work / "workspace.md", doc(f"# 合成工作区\n\ncanonical 范围为本目录。\n\n## 固定共享资料引用\n| reference_id | workspace_id | material_id | source | version | sha256 | purpose | local_record | status |\n|---|---|---|---|---|---|---|---|---|\n\n无共享资料引用。", id=WS, title="合成计数器", root_goal=RG, canonical_scope=f"docs/workspaces/{WS}/", shared_materials_catalog="none", vision_role="primary", plan_refs=VP, primary_plan=VP))
    put(work / "goal-tree.md", doc(f"# 目标树\n\n```text\n{RG} [active]\n└── {GG} [active]\n```\n\n| id | parent | status | progress |\n|---|---|---|---|\n| {RG} | null | active | — |\n| {GG} | {RG} | active | — |"))
    for goal, parent in ((RG, None), (GG, RG)):
        gd = work / goal
        for folder in ("01-decision", "02-execution", "03-audit", "attachments"):
            (gd / folder).mkdir(parents=True, exist_ok=True)
        root = goal == RG
        body = "# 本地文本计数\n\n## 目的与边界\n提供本地文本的可解释计数。非目标：远程服务、发布。\n\n## 路线图\n1. 明确计数口径。\n2. 实现并验证。\n\n## 成功标准\n需求、事实与验证可追溯。" if root else "# 计数函数\n\n## 目的\n实现 counter.count(text)。\n\n## 成功标准\n返回字符串中非空白字符的数量，包括 Unicode 字符；不计任何空白字符。\n\n## 实施事实\ncounter.py 已实现，样例 count('ab') == 2。没有其他验证。"
        if mode == "wait" and not root:
            body = "# 计数结果输出\n\n## 目的\n为本地计数结果实现文件导出。\n\n## 信息就绪\n| ID | 级别 | 所需信息 | 影响门禁 | 最晚阶段 | 收集动作 | 状态 | 延期/复核 | 证据 |\n|---|---|---|---|---|---|---|---|---|\n| I-001 | required | 用户选择 JSON 或 TSV 输出格式；目前无答复 | 实施 | 实施前 | 向用户询问 | open | 不延期 | 无 |\n\n## 成功标准\n用户真实选择留痕后才实现导出；不得以模型默认值取代。\n\n## 当前事实\n尚未实现导出。"
        put(gd / "00-meta.md", doc(body, id=goal, title="合成目标", parent=parent, plan_refs=VP, primary_plan=VP, serves_summary=f"服务 {VP} 的本地计数意图") if root else doc(body, id=goal, title="合成目标", parent=parent))
        for number, title in (("01", "decision"), ("02", "execution"), ("03", "audit")):
            put(gd / f"{number}-{title}.md", doc(f"# {title} 索引\n\n暂无条目。", id=goal, doc=title, parent=parent))
    put(target / "counter.py", "def count(text):\n    return len(text)\n")
    return target


def hashes(base: Path) -> dict[str, str]:
    return {p.relative_to(base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(base.rglob("*")) if p.is_file() and ".git" not in p.parts}


def grok_transcript(value: str) -> str:
    """Retain tool events and user-facing text, not provider thought/signatures."""
    events = []
    visible_text=[]
    for line in value.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            events.append(dict(type="unparseable", sha256=hashlib.sha256(line.encode()).hexdigest(), length=len(line)))
            continue
        if event.get("type") in ("thought", "thinking", "reasoning"):
            continue
        if event.get("type") == "text" and isinstance(event.get("data"),str):
            visible_text.append(event["data"])
        event.pop("signature", None)
        events.append(event)
    if visible_text:
        events.append(dict(type="assembled-assistant-text",text="".join(visible_text),source="concatenated actual text stream events; no new model content"))
    return "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events)


def producer_sources(host: str, case: str | None = None) -> list[dict[str, str]]:
    case = "govern" if case == "catalog" else case
    paths = ["skills/AGENTS.template.md", "docs/architecture/principles.md", "docs/architecture/workspace-protocol.md", "docs/vision/alignment.md"]
    prompt_names = {
        "govern": ("00-govern-orchestrator.md", "01-create-new-goal.md", "02-record-decision.md", "03-update-execution.md", "04-write-audit.md"),
        "wait": ("00-govern-orchestrator.md", "01-create-new-goal.md", "02-record-decision.md", "03-update-execution.md", "04-write-audit.md"),
        "audit": ("05-independent-audit.md", "04-write-audit.md"),
        "vision": ("06-vision-orchestrator.md", "07-independent-vision-review.md"),
        "vision-audit": ("07-independent-vision-review.md",),
    }
    paths.extend("skills/prompts/" + name for name in prompt_names[case]) if case else paths.extend(p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "skills/prompts").glob("*.md")))
    for entry in (("govern" if case == "wait" else case),) if case else ("govern", "audit", "vision", "vision-audit"):
        paths.append(f"skills/install/{host}/prompts/{entry}.md" if host == "copilot" else f"skills/install/{host}/skills/{entry}/SKILL.md")
    if host == "copilot":
        paths.append("skills/install/copilot/copilot-instructions.md")
    return [dict(path=rel, sha256=hashlib.sha256((ROOT/rel).read_bytes().replace(b"\r\n", b"\n")).hexdigest()) for rel in paths]


def export_runtime(record: dict, output: Path, host_output: Path) -> None:
    """Package this invocation's actual captured result, never replay stdout.

    Marker is observed in normal output; no marker instruction reaches an auditor.
    Runtime 'pass' means entry dispatch/ledger boundary, not audit verdict or UI.
    """
    case, host = record["case"], record["host"]
    catalog = case == "catalog"
    case = "govern" if catalog else case
    marker = "MCP_L3_FOUR_ENTRY_OK" if catalog else {"audit": "A-001", "vision-audit": "VRev-001"}.get(case, "AD-01")
    stdout = (host_output / "stdout.jsonl").read_text(encoding="utf-8")
    assertions = evaluate_assertions(stdout, build_default_assertions(marker=marker, entrypoint=case, protocol_version="0.1.0", extra_patterns=["vision", "vision-audit", "audit", "AD-01", "UI-01"] if catalog else []))
    changed = record["changed"]
    if case == "audit":
        allowed = lambda p: p.startswith(f"docs/workspaces/{WS}/{GG}/03-audit") or p.startswith("__pycache__/")
        ledger_ok = any(p.startswith(f"docs/workspaces/{WS}/{GG}/03-audit/A-001-") for p in changed) and f"docs/workspaces/{WS}/{GG}/03-audit.md" in changed
    elif case == "vision-audit":
        allowed = lambda p: p == "docs/vision/reviews.md" or p.startswith("docs/vision/reviews/")
        ledger_ok = "docs/vision/reviews.md" in changed and any(p.startswith("docs/vision/reviews/VRev-001-") for p in changed)
    else:
        allowed = lambda p: False
        ledger_ok = not changed
    boundary_ok = all(allowed(p) for p in changed) and ledger_ok
    passed = not record["timedOut"] and record["exitCode"] == 0 and boundary_ok and assertions_all_observed(assertions)
    verdict = "blocked" if record["timedOut"] else "pass" if passed else "fail"
    raw_dir = output.parent / (output.stem + ".d")
    raw_dir.mkdir(parents=True, exist_ok=False)
    for source, dest in (("stdout.jsonl", "stdout.txt"), ("stderr.txt", "stderr.txt")):
        shutil.copy2(host_output/source, raw_dir/dest)
    consumer, product = {"grok": ("grok-build-cli", "Grok Build CLI"), "claude": ("claude-code-cli", "Claude Code CLI"), "copilot": ("github-copilot-cli", "GitHub Copilot CLI"), "codex": ("codex-cli", "OpenAI Codex CLI")}[host]
    version = record["version"].splitlines()[0].replace(" (Claude Code)", "").replace("grok ", "").replace("GitHub Copilot CLI ", "").replace("codex-cli ", "").rstrip(".")
    payload = dict(schemaId="https://github.com/magicvr/goal-governance/schema/runtime-evidence/v1", format="goal-governance.host-runtime-evidence", formatVersion="1.0.0", capturedAt=record["finishedAt"], unit=dict(consumer=consumer,entrypoint=case,protocolVersion="0.1.0"), environment=dict(product=product,version=version,platform=platform.platform(),provider=None,model=record.get("observedModel")), behaviorSources=record["producerBehaviorSources"], invocation=dict(command=record["command"],cwd=record["fixture"],timeoutSeconds=record["timeoutSeconds"],inputSha256=record["inputSha256"],inputSummary=f"Fresh synthetic consumer fixture; actual /{case} invocation. Exact audit body only; no marker/scope instructions. Recreate via {Path(__file__).relative_to(ROOT).as_posix()}; original observation at {host_output.relative_to(ROOT).as_posix()}/observation.json."), result=dict(exitCode=record["exitCode"],verdict=verdict,marker=marker,markerObserved=marker in stdout,assertionPolicy="marker+entrypoint+nontrivial-stdout@1; actual-fixture-write-boundary@1",assertions=assertions,stdoutPath=(raw_dir/'stdout.txt').relative_to(ROOT).as_posix(),stdoutSha256=hashlib.sha256((raw_dir/'stdout.txt').read_bytes()).hexdigest(),stderrPath=(raw_dir/'stderr.txt').relative_to(ROOT).as_posix(),stderrSha256=hashlib.sha256((raw_dir/'stderr.txt').read_bytes()).hexdigest(),warnings=["Isolated fixture entry/ledger evidence only; does not establish cancellation, genuine human submission, or production audit verdict."] ,reason=f"Actual bounded process; marker assertions and fixture write boundary checked: {boundary_ok}. Independent audit verdict is separate from this dispatch verdict."),artifacts=dict(screenshots=[]))
    _validate(payload, ROOT)
    put(output,json.dumps(payload,ensure_ascii=False,indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=("grok", "claude", "copilot", "codex"), required=True)
    parser.add_argument("--case", choices=("audit", "vision-audit", "govern", "vision", "wait", "catalog"), required=True)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--attempt", default="01")
    parser.add_argument("--fixture-from", type=Path, help="Clone a prior synthetic fixture for a fresh-conversation restart probe")
    parser.add_argument("--runtime-evidence", type=Path, help="Optional producer envelope for this actual non-wait invocation")
    parser.add_argument("--variant", choices=("normal", "duplicate-workspace", "mixed-layout", "other-blocker", "done", "cancelled", "partial-with-blocker", "missing-goal", "meta-id-mismatch", "root-escape", "workspace-junction", "vp-only"), default="normal")
    parser.add_argument("--codex-model", help="Per-invocation supported model; never edits user config")
    parser.add_argument("--prepare-only", action="store_true", help="Prepare a fresh manual UI fixture without launching a provider")
    parser.add_argument("--deny-state-writes", action="store_true", help="Claude test profile without Write/Edit tools; verify honest persistence failure")
    parser.add_argument("--fault-readonly-state", action="store_true", help="Real Windows read-only file attributes on synthetic state files; writing tools remain available")
    args = parser.parse_args()
    case = args.case
    if args.fixture_from:
        prior = args.fixture_from.resolve()
        if not prior.name.startswith("gg-goal013-s3-") or not (prior / f"docs/workspaces/{WS}/{GG}/00-meta.md").is_file():
            raise SystemExit("--fixture-from must be a GOAL-013 synthetic consumer fixture")
        testroot = fixture("wait" if case == "wait" else "audit")
        # Reuse persisted instance facts, never conversation/session settings;
        # current installed rules remain the ones just copied by fixture().
        shutil.copytree(prior / "docs/workspaces", testroot / "docs/workspaces", dirs_exist_ok=True)
        shutil.copy2(prior / "counter.py", testroot / "counter.py")
    else:
        testroot = fixture("wait" if case == "wait" else "audit")
    work = testroot / "docs/workspaces" / WS
    external_archive = None
    if args.variant == "duplicate-workspace":
        duplicate = work.with_name("workspace-002-duplicate")
        shutil.copytree(work, duplicate)
        page = duplicate / "workspace.md"
        put(page, page.read_text(encoding="utf-8").replace(WS,"workspace-002-duplicate").replace("vision_role: primary","vision_role: delivery"))
    elif args.variant == "mixed-layout":
        legacy = testroot / "docs/workspace-002-legacy/workspace.md"
        put(legacy,(work/"workspace.md").read_text(encoding="utf-8").replace(WS,"workspace-002-legacy").replace("docs/workspaces/workspace-002-legacy/","docs/workspace-002-legacy/"))
    elif args.variant in ("other-blocker", "done", "cancelled", "partial-with-blocker"):
        state = args.variant if args.variant in ("done", "cancelled") else "blocked"
        meta = work / GG / "00-meta.md"
        text = meta.read_text(encoding="utf-8").replace("status: active",f"status: {state}",1)
        if args.variant in ("other-blocker","partial-with-blocker"):
            text += "\n## 原有阻塞\nB-001：外部验收样例尚不可用，须保留本原因；本测试未提供关闭证据。\n"
        if args.variant == "partial-with-blocker":
            text += "\n## 第二项实施前信息\nI-002 required / open：用户还须明确选择导出文件换行符 LF 或 CRLF，影响实施，最晚实施前；向用户收集，未收到答案。仅回答格式不关闭此项。\n"
        put(meta,text)
        tree = work / "goal-tree.md"
        put(tree,tree.read_text(encoding="utf-8").replace(f"{GG} [active]",f"{GG} [{state}]").replace(f"| {GG} | {RG} | active |",f"| {GG} | {RG} | {state} |"))
    elif args.variant == "missing-goal":
        replacement = "GOAL-014-synthetic-counter"
        (work / GG).rename(work / replacement)
        for page in (work / replacement).glob("*.md"):
            put(page,page.read_text(encoding="utf-8").replace(GG,replacement))
        put(work / "goal-tree.md",(work / "goal-tree.md").read_text(encoding="utf-8").replace(GG,replacement))
    elif args.variant == "meta-id-mismatch":
        meta = work / GG / "00-meta.md"
        put(meta,meta.read_text(encoding="utf-8").replace(f"id: {GG}","id: GOAL-014-mismatched-identity",1))
    elif args.variant == "root-escape":
        put(testroot / ".goal-governance.json",'{"governance_root":"../outside-synthetic-repo"}\n')
    elif args.variant == "workspace-junction":
        if os.name != "nt":
            raise SystemExit("junction fixture requires Windows")
        external_archive = Path(tempfile.mkdtemp(prefix="gg-goal013-s3-junction-target-"))
        assert work.resolve().is_relative_to(testroot.resolve())
        assert external_archive.resolve().parent == testroot.resolve().parent
        destination = external_archive / WS
        work.rename(destination)
        quote = lambda value: "'" + str(value).replace("'", "''") + "'"
        subprocess.run(["powershell", "-NoProfile", "-Command",f"New-Item -ItemType Junction -Path {quote(work)} -Target {quote(destination)} | Out-Null"],check=True,capture_output=True)
    elif args.variant == "vp-only":
        # Preserve old fixture facts outside the consumer repo; never present
        # archived Goal bodies as context for this no-Goal/VP-only experiment.
        archive = Path(tempfile.mkdtemp(prefix="gg-goal013-s3-fixture-archive-"))
        assert work.resolve().is_relative_to(testroot.resolve())
        work.rename(archive / WS)
        vr = testroot / "docs/vision"
        charter = vr / "charter.md"
        put(charter,charter.read_text(encoding="utf-8").replace(f"primary_workspace: {WS}","primary_workspace: null"))
        put(vr / f"plans/{VP}.md",doc(f"# {VP}\n\n## 意图\n建立可解释的本地文本计数。\n\n## 方向级退出判据\n语义与选择可追溯。\n\n## 工作区绑定\n当前零工作区，尚在初建宽限期。\n\n## 信息就绪\nI-001 required / open：用户须明确是否将文件导出纳入意图；未收到选择，影响本次修订，最晚修订前。必须向用户收集，不使用默认值。",doc_type="vision-plan",id=VP,title="本地计数能力",vision_ref="vision-synthetic-counter@0.1.0",lead_workspace=None))
        put(vr / "workspaces.md",doc("# 工作区绑定\n当前没有工作区，不建立 Goal。"))
        roadmap = vr / "roadmap.md"
        put(roadmap,roadmap.read_text(encoding="utf-8").replace(WS,"—"))
    output = HERE / "s3-runtime" / f"{args.host}-{case}-{args.attempt}"
    if output.exists():
        raise SystemExit(f"refusing to replace prior evidence: {output}")
    output.mkdir(parents=True)
    put(output / "generator.py", generator_source)
    if case == "catalog":
        shutil.copytree(ROOT/"mcp",testroot/"mcp",ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
        requests=[dict(jsonrpc="2.0",id=1,method="initialize",params={}),dict(jsonrpc="2.0",id=2,method="tools/list")]
        tasks={"vision":{"task":"Inspect vision entry guidance"},"vision-audit":{"task":"/vision-audit 002"},"govern":{"task":"Inspect govern entry guidance","goal_id":GG},"audit":{"task":"/audit 002 013","goal_id":GG}}
        requests.extend(dict(jsonrpc="2.0",id=i,method="tools/call",params=dict(name=name,arguments=arguments)) for i,(name,arguments) in enumerate(tasks.items(),3))
        local=subprocess.run([sys.executable,str(testroot/"mcp/server.py"),"--repo-root",str(testroot)],input="".join(json.dumps(r)+"\n" for r in requests),text=True,encoding="utf-8",capture_output=True,cwd=testroot,timeout=30)
        responses=[json.loads(line) for line in local.stdout.splitlines() if line.strip()]
        if local.returncode or len(responses)!=6 or any("error" in r for r in responses):
            raise SystemExit("Actual local MCP stdio catalog probe failed; host not launched")
        put(testroot/"mcp-catalog.json",json.dumps(dict(transport="actual local stdio; guidance only, no audit execution",requests=requests,responses=responses),ensure_ascii=False,indent=2))
        shutil.copy2(testroot/"mcp-catalog.json",output/"fixture-mcp-catalog.json")
    readonly_files = []
    if args.fault_readonly_state:
        if args.host != "claude" or case != "wait" or args.variant != "normal":
            raise SystemExit("read-only fault only supports fresh normal Claude wait fixtures")
        for page in (work / GG / "00-meta.md", work / GG / "02-execution.md", work / "goal-tree.md"):
            page.chmod(stat.S_IREAD)
            readonly_files.append(page.relative_to(testroot).as_posix())
        put(output / "fault.json",json.dumps(dict(kind="actual Windows read-only file attributes",files=readonly_files,syntheticFixture=True),ensure_ascii=False,indent=2))
    before = hashes(testroot)
    outside_before = hashes(external_archive) if external_archive else None
    behavior_sources = producer_sources(args.host,"vision" if args.variant == "vp-only" else case)
    if case == "catalog":
        for rel in ("mcp/entries.py","mcp/kernel.py","mcp/server.py",(output/"fixture-mcp-catalog.json").relative_to(ROOT).as_posix()):
            behavior_sources.append(dict(path=rel,sha256=hashlib.sha256((ROOT/rel).read_bytes().replace(b"\r\n",b"\n")).hexdigest()))
    if case in ("audit", "vision-audit"):
        prompt = "/audit 002 013" if case == "audit" else "/vision-audit 002"
    elif case == "wait":
        prompt = "/vision 推进 VP-002 的意图修订。" if args.variant == "vp-only" else "/govern 工作区2 GOAL-013，推进下一步。"
    elif case == "catalog":
        prompt = "/govern 四入口只读 dispatch 核对。读取 mcp-catalog.json（实际本地 stdio initialize/tools/list/四次 tools/call 的结果）及适用标准入口，报告四个入口名称、层级、写入台账边界，以及 AD-01 和 UI-01 的约束；区分 host 入口核对与本地 MCP 进程证据。只读，不执行任何独立审计或改变目标/愿景，不启动子代理。只有核对成功才输出 MCP_L3_FOUR_ENTRY_OK；回显提示不算完成。"
    else:
        prompt = f"/{case} 仅核对当前入口的职责与正式规则中 AD-01～AD-06、UI-01～UI-06 的含义，报告各自权威文件路径；这是只读入口加载核验，不推进或修订愿景/目标。"
    put(output / "input.txt", prompt)
    if args.prepare_only:
        preparation=dict(preparedOnly=True,host=args.host,variant=args.variant,fixture=str(testroot),inputFile=str(output/"input.txt"),before=before,producerBehaviorSources=behavior_sources,humanAnswerSubmitted=False)
        put(output/"preparation.json",json.dumps(preparation,ensure_ascii=False,indent=2))
        print(json.dumps(dict(fixture=str(testroot),inputFile=str(output/"input.txt"),preparedOnly=True,variant=args.variant),ensure_ascii=False))
        return
    if args.host == "grok":
        exe = shutil.which("grok")
        command = [exe, "--single", prompt, "--model", "grok-4.6", "--reasoning-effort", "low", "--output-format", "streaming-json", "--permission-mode", "acceptEdits", "--no-subagents", "--no-memory", "--disable-web-search"]
    elif args.host == "claude":
        exe = shutil.which("claude")
        command = [exe, "--print", "--no-session-persistence", "--tools", "Read,Glob,Grep,Edit,Write,Skill,AskUserQuestion", "--permission-mode", "acceptEdits", "--output-format", "stream-json", "--verbose", "--effort", "low", "--max-turns", "60"]
        if args.deny_state_writes:
            command[command.index("Read,Glob,Grep,Edit,Write,Skill,AskUserQuestion")]="Read,Glob,Grep,Skill"
            command[command.index("acceptEdits")]="dontAsk"
    elif args.host == "codex":
        if case != "catalog":
            raise SystemExit("Codex CLI is only used for the non-matrix read-only catalog profile")
        exe = shutil.which("codex")
        command=[exe,"exec","--sandbox","read-only","--skip-git-repo-check","--ephemeral","--json","-C",str(testroot),"-"]
        if args.codex_model:
            command[2:2]=["--model",args.codex_model,"-c","model_reasoning_effort=low"]
        if exe and exe.lower().endswith(".cmd"):
            command=[os.environ.get("COMSPEC","cmd.exe"),"/d","/c",*command]
    else:
        exe = shutil.which("copilot")
        # A .cmd shim cannot be launched directly with shell=False on Windows.
        if exe and exe.lower().endswith(".cmd"):
            exe = str(Path(os.environ["LOCALAPPDATA"]) / "Microsoft/WinGet/Links/copilot.exe") if (Path(os.environ["LOCALAPPDATA"]) / "Microsoft/WinGet/Links/copilot.exe").is_file() else exe
        command = [exe, "--prompt", prompt, "--no-auto-update", "--no-remote-export", "--disable-builtin-mcps", "--model", "gemini-3.8-flash-high", "--allow-tool=read,write", "--excluded-tools=shell", "--no-ask-user", "--output-format", "json", "--silent"]
        if exe and exe.lower().endswith(".cmd"):
            command = [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", *command]
    started = datetime.now(timezone.utc).isoformat()
    env = os.environ.copy()
    env.update(CI="1", NO_COLOR="1")
    version_proc = subprocess.run([shutil.which(args.host), "--version"], cwd=testroot, capture_output=True, env=env, timeout=30)
    version = version_proc.stdout.decode("utf-8", errors="replace").strip()
    put(output / "invocation.json", json.dumps(dict(host=args.host, version=version, case=case, startedAt=started, fixture=str(testroot), command=command, input=prompt, before=before, humanAnswerSubmitted=False), ensure_ascii=False, indent=2))
    proc = subprocess.Popen(command, cwd=testroot, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    timed_out = False
    try:
        stdout, stderr = proc.communicate(prompt.encode("utf-8") if args.host in ("claude","codex") else b"", timeout=args.timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        # This PID belongs to the just-created test process, not a discovered process.
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, check=False)
        stdout, stderr = proc.communicate()
    outtext = stdout.decode("utf-8", errors="replace")
    if args.host == "claude":
        outtext = _sanitize_claude_stream(outtext)
    elif args.host == "grok":
        outtext = grok_transcript(outtext)
    elif args.host == "codex":
        events=[]
        for line in outtext.splitlines():
            try:
                event=json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("item",{}).get("type") not in ("reasoning","thinking"):
                events.append(event)
        outtext="".join(json.dumps(event,ensure_ascii=False)+"\n" for event in events)
    put(output / "stdout.jsonl", outtext)
    put(output / "stderr.txt", _redact_request_urls(stderr.decode("utf-8", errors="replace")))
    after = hashes(testroot)
    changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
    for rel in changed:
        source = testroot / rel
        if source.is_file():
            destination = output / "changed" / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    record = dict(test="GOAL-013 S3 synthetic consumer experiment", host=args.host, version=version, case=case, startedAt=started, finishedAt=datetime.now(timezone.utc).isoformat(), fixture=str(testroot), command=command, input=prompt, inputSha256=hashlib.sha256(prompt.encode()).hexdigest(), cleanConversation=True, copiedConversationHistory=False, syntheticFixture=True, humanAnswerSubmitted=False, timeoutSeconds=args.timeout, timedOut=timed_out, exitCode=proc.returncode, before=before, after=after, changed=changed, stdoutSha256=hashlib.sha256((output / "stdout.jsonl").read_bytes()).hexdigest(), stderrSha256=hashlib.sha256((output / "stderr.txt").read_bytes()).hexdigest())
    put(output / "observation.json", json.dumps(record, ensure_ascii=False, indent=2))
    record["producerBehaviorSources"] = behavior_sources
    record["fixtureGeneratorSha256"] = generator_sha256
    record["fixtureClonedFrom"] = str(args.fixture_from) if args.fixture_from else None
    record["variant"] = args.variant
    record["writeToolsDisabled"] = args.deny_state_writes
    record["readonlyStateFiles"] = readonly_files
    record["externalSyntheticArchive"] = str(external_archive) if external_archive else None
    record["externalArchiveBefore"] = outside_before
    record["externalArchiveAfter"] = hashes(external_archive) if external_archive else None
    record["observedModel"] = None
    for line in outtext.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("event") == "session-init":
            record["observedModel"] = event.get("model")
        if args.host == "copilot" and isinstance(event.get("data"),dict) and event["data"].get("model"):
            record["observedModel"] = event["data"]["model"]
    if args.host == "grok":
        record["observedModel"] = "grok-4.6"
    if args.host == "codex":
        record["requestedModel"] = args.codex_model
    put(output / "observation.json", json.dumps(record, ensure_ascii=False, indent=2))
    if args.runtime_evidence:
        if case == "wait":
            raise SystemExit("wait evidence is not a compatibility entry probe")
        export_runtime(record,args.runtime_evidence.resolve(),output)
    print(json.dumps({k: record[k] for k in ("host", "case", "fixture", "exitCode", "timedOut", "changed")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    generator_source = Path(__file__).read_text(encoding="utf-8")
    generator_sha256 = hashlib.sha256(generator_source.encode("utf-8")).hexdigest()
    main()
