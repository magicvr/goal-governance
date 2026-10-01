---
id: A-002
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: audit
title: v0.13.4 发布候选独立审计
source: independent
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# A-002 · v0.13.4 发布候选独立审计（independent）

| 项 | 值 |
|----|-----|
| source | `independent` |
| provider | 本地 grok build CLI · 模型 `grok-4.6`（用户 2026-10-01 书面改派，见 [D-002](../01-decision/D-002-independent-audit-provider-and-scope.md) §provider 变更） |
| scope | 发布候选完整审计 |
| 日期 | 2026-10-01 |
| verdict | **pass** |
| 开放 required | **0**（recommended 5） |

> 以下为独立审计者的原话落盘（编排器代贴，未改写结论与 finding 编号）。
> 审计对象：`dev` 的 HEAD `d30abb346c40d30b408425fe2b9ff161d0388150` + 本轮未提交的 v0.13.4 候选工作树。

## scope

对仓库 `C:\Users\magicvr\Documents\Code\goal-governance` 分支 `dev`（HEAD `d30abb346c40d30b408425fe2b9ff161d0388150`，工作树含未提交的 v0.13.4 候选）做发布候选完整审计：12 格 L3 证据是否真实且被矩阵引用；CHANGELOG / 矩阵 `candidateRevision` / 安装 pin 是否一致；所列回归与发布门禁在本机是否转绿；`test_init_workspace_refuses_existing_path` 是否仍验证二次 init 拒绝；GOAL-010 台账是否齐全。未重跑宿主探针，未核 GitHub CI，未核 S4（PR / merge / tag / 资产）。

## 实际执行与核对（命令 + 结果）

解释器：系统 `python` = **Python 3.11.9**。`PYTHONUTF8=1`。

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.4` | 0 | `evidence consistency ok (12 evidence file(s))` |
| `python scripts/compatibility_report.py --output artifacts/audit-compatibility.json` | 0 | `coverage status: ready-for-release-evidence`；`uncovered: []`；`candidateRevision: v0.13.4` |
| `python -m unittest skills/tests/test_skills_orchestrator.py` | 0 | `Ran 45 tests` OK |
| `python -m unittest discover -s docs/tests -p test_standalone_bootstrap.py` | 0 | `Ran 3 tests` OK |
| `python -m unittest discover -s scripts/tests -p test_*.py` | 0 | `Ran 145 tests` OK（`skipped=7`：bash / docker / symlink 环境跳过） |
| `python scripts/stage_skills_mirrors.py --check` | 0 | `ok: skills mirrors match docs/`（37 对） |
| `git diff --check` | 0 | 仅 CRLF→LF 工作副本提示，无空白错误 |
| 独立脚本复算 12 格 `behaviorSources` / stdout / stderr sha256，并按捕获器规则重评断言 | 0 | 12/12 哈希一致；12/12 `recomputed_would_pass=True` |
| canonical vs 镜像逐字节比较 | — | `docs/contracts/skills-consumer-compatibility-matrix.json` 与 `skills/contracts/...` **6758 bytes、sha256 `74d65e988be50963…` 逐字节相同** |
| `.venv\Scripts\python.exe` 空 `TemporaryDirectory().cleanup()` | — | Python **3.14.6** 在 `…\Temp\dsh-1pBC9U\...` 上报 `PermissionError: [WinError 5]`；同一目录下 3.11.9 `cleanup_ok`。**该现象我亲眼见到。** |
| `python scripts/release_evidence.py --mode rehearsal --run-checks …`（清单外加跑） | **1** | `release status: rehearsal`，`checksPassed: False`。原因是 `_python_with_imports` **优先选用 `.venv` 3.14**，三套 unittest 在 teardown 上出现 PermissionError（skills `errors=3` / docs `errors=1` / scripts `errors=93, skipped=3`）。`annotatedTag: null`。 |

`--check` 只核 `behaviorSources` 对当前树；stdout/stderr 哈希与断言是审计者另写只读脚本复算的，不是信任 `--check`。

## 独立复算的证据抽样

当前树（`_sha256_repo_text` = 文件字节 `\r\n`→`\n` 后再 sha256）：

- `AGENTS.md` = `e8afa1d414cb5f2a563aca2151edb6aa5d1a51468fa00a51991ec69a3daf642b`
- `skills/prompts/00-govern-orchestrator.md` = `222d37a7843a2b06be35c1c541beda11eade23d1ff94d7ed977dda3c959d6a4c`

12 格全部亲自复算（unit / verdict / marker / exit / 源哈希 / stdout·stderr 哈希 / 断言）：

| 格 | unit | verdict / exit / markerObserved | stdoutSha256（记录=复算） | marker 在 stdout |
|----|------|----------------------------------|---------------------------|------------------|
| claude govern | `claude-code-cli/govern/0.1.0` | pass / 0 / true | `ec27fb8f8cb4a8e5…` | `CLAUDE_GOVERN_DISPATCH_OK` |
| claude audit | `claude-code-cli/audit/0.1.0` | pass / 0 / true | `b64c03c148467536…` | `CLAUDE_AUDIT_DISPATCH_OK` |
| claude vision | `claude-code-cli/vision/0.1.0` | pass / 0 / true | `e3e0062bf44288de…` | `CLAUDE_VISION_DISPATCH_OK` |
| claude vision-audit | `claude-code-cli/vision-audit/0.1.0` | pass / 0 / true | `5c918a702009ffdf…` | `CLAUDE_VISION_AUDIT_DISPATCH_OK` |
| grok govern | `grok-build-cli/govern/0.1.0` | pass / 0 / true | `a3de51316661a824…` | `GROK_GOVERN_DISPATCH_OK` |
| grok audit | `grok-build-cli/audit/0.1.0` | pass / 0 / true | `6dd5a0b84bb221fb…` | `GROK_AUDIT_DISPATCH_OK` |
| grok vision | `grok-build-cli/vision/0.1.0` | pass / 0 / true | `6b06db4700c29c6b…` | `GROK_VISION_DISPATCH_OK` |
| grok vision-audit | `grok-build-cli/vision-audit/0.1.0` | pass / 0 / true | `8a799242fbd5fd67…` | `GROK_VISION_AUDIT_DISPATCH_OK` |
| copilot govern | `github-copilot-cli/govern/0.1.0` | pass / 0 / true | `536f131d7672d6c3…` | `COPILOT_CLI_GOVERN_DISPATCH_OK` |
| copilot audit | `github-copilot-cli/audit/0.1.0` | pass / 0 / true | `fe304257e7726bae…` | `COPILOT_CLI_AUDIT_DISPATCH_OK` |
| copilot vision | `github-copilot-cli/vision/0.1.0` | pass / 0 / true | `b627680fba4793e8…` | `COPILOT_CLI_VISION_DISPATCH_OK` |
| copilot vision-audit | `github-copilot-cli/vision-audit/0.1.0` | pass / 0 / true | `f07e9f2a5f24ef74…` | `COPILOT_CLI_VISION_AUDIT_DISPATCH_OK` |

每格 `behaviorSources` 两项均与上列当前树哈希一致。每格 3 条断言（`dispatch-marker` / `entrypoint-token` / `nontrivial-stdout@16`）记录值与按 stdout 重算值一致。Grok 4 格 `inputSha256` 与 GOAL-008 冻结 prompt 文件字节哈希一致。Claude govern 的 `inputSha256` 与 v0.13.3 同格相同（探针 corpus 未改）。抽样阅读 Claude govern / Grok govern / Copilot govern / Grok vision-audit stdout：均有加载对应 skill、读取编排提示、再输出 marker 的工具调用或叙述，不是只打印 marker。

**没有一格「标为 pass 但证据不支撑」。**

矩阵 12 条 `evidence` 路径全部存在、全部在 `docs/releases/runtime/v0.13.4/`、全部 `runtime-verified`。`capturedAt` 为 2026-09-30T17:58Z–18:56Z（UTC），文件名日期 2026-10-01 与 UTC+8 一致。

## findings

| ID | 级别 | 主张 | 证据 | 影响门禁 |
|----|------|------|------|----------|
| F-001 | recommended | Claude 4 格 `invocation.command` 引用工作区根 `.gg-probe-settings.json`，该文件现在不存在、未入库。这是本机代理 URL 的探针覆盖（去掉 `ANTHROPIC_BASE_URL` 末尾 `/v1`），**不构成 required「证据不可复现」**：L3 核的是落盘 stdout/stderr 与 behaviorSources，已独立复算 4 格哈希/marker/断言成立，且 stdout 含真实 Read/Glob 与 skill 正文。干净检出无法按记录命令原样重放这 4 格。 | 4 份 Claude JSON 的 `--settings …\.gg-probe-settings.json`；`Test-Path` = False；v0.13.3 同格 command 无 `--settings`；E-001 #1 / CHANGELOG「本机环境修正」已记载 | 不阻断发布候选。命令级重放需重建该覆盖文件 |
| F-002 | recommended | 当前树的 `release_evidence.py --mode rehearsal --run-checks` 在本机 `checksPassed: False`，因为 `_python_with_imports` 优先 `.venv` Python 3.14.6，tempfile 清理 PermissionError。同一套测试用系统 3.11.9 直接跑全绿。E-003 记载曾临时改解释器优先级再 `git checkout` 还原；该还原态下 rehearsal 包装器本机仍红。 | 审计者跑 rehearsal exit 1；`scripts/release_evidence.py:35-39` 候选顺序 `.venv` 先于 `sys.executable`；3.14 空 TemporaryDirectory cleanup 复现 WinError 5；3.11 unittest 45/3/145 OK | 不阻断：CI 用 3.11；清单内的直接测试已绿。确认 A-001 F-002 |
| F-003 | recommended | independent provider 台账未对齐：`01-decision/D-002` 与 `00-meta.md` I-004 已写改派本地 grok build CLI（`grok-4.6`）；`03-audit.md` 仍写 provider=本地 codex CLI，并写「已向用户申请改用其他 provider，A-002 待该裁决后落盘」；`goal-tree.md` 2026-10-01 GOAL-010 条仍写 provider=本地 codex CLI。 | 三处正文对照（D-002 已含「provider 变更」节） | 不阻断证据/测试门禁。编排器落盘 A-002 时须改 `03-audit.md`（本意见不代写） |
| F-004 | recommended | 根 `README.md`、`skills/README.md`、`docs/releases/README.md` 把 `v0.13.4` 写成「当前正式发布」pin；CHANGELOG `## 0.13.4` 节首句写「并完成一次正式发布」。`git tag --list v0.13.4` 为空；CHANGELOG `## Unreleased` 与 `docs/README.md` 正确写「发布候选、尚未打 tag」。 | tag 列表空；README「当前正式发布 pin `v0.13.4`」出现 2 次；`docs/releases/README.md:38`；CHANGELOG L11；Unreleased L7 | 不把 rehearsal 写成已发布（`releaseStatus: rehearsal`，`annotatedTag: null`）。安装示例会指向尚不存在的 Release URL，S4 打 tag 后自行成立 |
| F-005 | recommended | 「4 宿主 × 4 治理入口 = 12 格」算术与宿主计数错误。矩阵消费者是 3 个（claude / grok / copilot），3×4=12。 | `00-meta.md:18`、`D-001:44`、`CHANGELOG.md:21`；I-002 文案「四个宿主 CLI」同时只列了 3 个版本 | 不影响 12 格存在与 pass 事实 |

## 未发现问题的项

- 12 格全部 `verdict=pass`、`exitCode=0`、`markerObserved=true`，stdout 真有 marker，断言按 stdout 重算成立。无「标 pass 无支撑」。
- 矩阵 `candidateRevision = v0.13.4`，12 格 evidence 均指向本目录且文件存在；镜像与 canonical 逐字节相同。
- CHANGELOG 有 `## 0.13.4 - 2026-10-01`；`## Unreleased` 把它写成候选。三处安装 pin（`README.md` / `skills/README.md` / `scripts/bootstrap/README.md`）以及 `mcp/README.md`、`docs/releases/README.md` 均指向 `v0.13.4` / `0.13.4`；这三处 README 内 `v0.13.2`/`v0.13.3` 计数为 0。
- `test_init_workspace_refuses_existing_path` 仍断言：第一次 `returncode==0` 且 `workspace.md` 落盘；第二次非 0 且消息匹配 `already exists|refuse`。安装包复制到临时项目内、`-SkillsDir .\staged-skills`。45 项 skills 测试含该项，结果 OK。
- GOAL-010：`parent` = `GOAL-001-methodology-skills-feedback-evolution`；五件套 + `01-decision/`（D-001/D-002/D-003）+ `02-execution/`（E-001/E-002/E-003）+ `03-audit/`（A-001）齐全。`goal-tree.md` 树 / 状态表 / 编号表（最大 010、下一 GOAL-011）与 `00-meta.md` 的 id/status/progress 25%/parent 一致。GOAL-001 子目标表含 GOAL-010 `active`；R3 说明与 D-011 同步。
- `docs/releases/runtime/v0.13.4/` 仅 12 份 JSON + 各自 `.d/stdout.txt`、`.d/stderr.txt`，无临时脚本、无凭据文件、无额外非证据文件。证据正文无 API key / Bearer / `sk-` 匹配。
- 清单内的门禁命令（3.11 直接跑）全部退出码 0。未发现测试被 `skip` 掉 containment 原意、未发现把 fail 格写进矩阵。E-003 明确 S4 尚未发生。rehearsal JSON 的 `releaseStatus` 为 `rehearsal`。

## 不确定 / 无法核对的项（原话）

- 未重新调用 claude / grok / copilot 做现场探针；只核已落盘捕获。
- 未核 GitHub CI（含 `windows-install-surface`）与 `skills-pack-release.yml` publish。
- S4：PR、`main` 合并、annotated tag、Environment `release` 审批、9 项资产与 sidecar 摘要——尚未发生，无法核对。
- `.gg-probe-settings.json` 的历史字节无法核对（文件已删）。判定见 F-001。
- `GROK_HOME` / `COPILOT_HOME` 重定位未写入 `invocation.command`；E-001 有过程记载，未复现该环境。
- 仓库根未跟踪的 `.gg-codex-home/auth.json`、`.gg-grok-home/auth.json`（凭据）以及 `.gg-run-audit*.ps1` **不在**证据目录内；`.gitignore` 无 `.gg*` 规则。是否会误提交，本轮未看 git add 暂存区之外的操作。
- `00-meta.md` I-002 仍为 `collecting`（12 格已存在）。这是台账状态，不是证据缺口。
- 未做隔离消费仓安装/升级重放。
- `compatibility_report.py` 未加 `--require-ready`；报告 `coverage.status` 已是 `ready-for-release-evidence`。
