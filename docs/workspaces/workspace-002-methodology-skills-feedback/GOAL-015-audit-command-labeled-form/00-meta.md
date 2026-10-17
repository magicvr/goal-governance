---
id: GOAL-015-audit-command-labeled-form
title: 审计命令带标签形式修正（workspace-/goal-/vp-）
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.9.0
progress: 100%
---

# GOAL-015 · 审计命令带标签形式修正（workspace-/goal-/vp-）

## 概述

修正 GOAL-013 留下的形式偏差。用户 2026-10-16 的原始要求是自动派发只允许「形式审计命令」`/audit <工作区编号> <目标编号>` 或 `/vision-audit <vp编号>`（原话见 [GOAL-013 D-001](../GOAL-013-audit-dispatch-and-user-input-gates/01-decision/D-001-scope-and-roadmap.md)），但 GOAL-013 的契约把带标签编号改写成裸数字 `/audit NNN NNN`、`/vision-audit NNN`，并固化进 AD-01 与全部消费面。用户 2026-10-17 指出「误成了类似 `/audit 3 2` 的命令」，要求做一个小修正。

本轮把正式命令改为带标签形式：

- `/audit workspace-<NNN> goal-<NNN>`（例 `/audit workspace-002 goal-015`）
- `/vision-audit vp-<NNN>`（例 `/vision-audit vp-002`）

裸数字形式（`/audit 002 015`、`/vision-audit 002`）不再合法。本目标位于本区 Root 的 R3「持续闭环与长期演进」，经父目标服务 VP-002。范围与路线图见 [D-001](01-decision/D-001-scope-and-roadmap.md)，语法与拒绝面冻结见 [D-002](01-decision/D-002-labeled-command-contract.md)。

S1～S5 全部完成，当前 **active / 100%（5/5）**，关门待用户。S5（发布）已按 D-003 全链路完成：16 格运行证据重捕获 **16/16 pass**（一致性 `--check` 22 份、`compatibility_report` `ready-for-release-evidence`、uncovered 0）；清单与 CHANGELOG `0.13.7` 同步；本地门禁 skills 102 / docs 67 / scripts 147 全绿、strict rehearsal 与 strict 预检 `checks passed: True`；检查点 `8f1315f` → [PR #31](https://github.com/magicvr/goal-governance/pull/31) 双平台 CI 全绿 → merge `6ca04ee` → annotated tag `v0.13.7`（tag object `6197ed6e`）→ tag workflow [39034827440](https://github.com/magicvr/goal-governance/actions/runs/39034827440) 的 `pack` 与 gated publish 全绿（Environment `release` 由维护者 `magicvr` 人工审批，AI 未代批）。[Release v0.13.7](https://github.com/magicvr/goal-governance/releases/tag/v0.13.7) 于 2026-10-17T13:10:14Z 发布 9 项资产；逐项验收通过（双 ZIP 摘要与 sidecar 一致、Core 27 成员为 Skills 86 成员的逐字节子集、下载资产驱动的隔离消费安装 exit 0 且消费者自有规则保留、GHCR digest 与发布日志一致且内置版本 `0.13.7`），见 [asset-verification.json](attachments/asset-verification.json) 与 [E-008](02-execution/E-008-s5-release-and-asset-verification.md)。过程更正见 [E-006](02-execution/E-006-s5-evidence-recapture.md)（Copilot 首轮 401 系编排侧环境未继承 `COPILOT_PROVIDER_API_KEY`，非凭据失效）。S5 审计模式为 `independent`，仍需一条指定 provider 的独立意见后方可关门。

## 成功标准

- [x] canonical（`principles.md` AD-01/AD-02/示例、`workspace-protocol.md` §2.7、`vision/alignment.md` §9.3）统一表达带标签形式，裸数字明确判为非法
- [x] 根 `AGENTS.md`、Skills `prompts/00·04·05·06·07`、四宿主安装源与规则模板、MCP guidance、契约测试同改，全仓规则面无残留旧形式
- [x] Skills 镜像 `stage_skills_mirrors.py --check` 通过（38 对）；本仓 dogfood 副本与安装源逐字节一致（16 对）
- [x] 正反例与回归可核对；本次修正对既有 runtime/compatibility evidence 的影响已核实并记录（16/16 过期、24 个来源）；重捕获由 S5 承接，完成前不宣称发布就绪
- [x] cross 审计（self + 用户指定 Grok Build independent）落盘并响应，无未合法闭合 required 后完成关门审视（A-004 `pass`；2 条 recommended 保持 open 并带复审触发）
- [x] S5：16 格运行证据重捕获且 `capture_runtime_evidence --check` 一致、矩阵 `candidateRevision` 指向新版本、`compatibility_report --require-ready` 通过；版本清单与 strict rehearsal 通过；PR 经 Ubuntu/Windows CI 全绿后合入 `main`；annotated tag 指向 merge 且 tag workflow 的 pack 与 gated publish 全绿（Environment `release` 由用户人工审批）；Release 资产逐项验收（含隔离消费安装与 GHCR 核对）——事实见 [E-006](02-execution/E-006-s5-evidence-recapture.md)、[E-007](02-execution/E-007-s5-pr-ci-merge-tag.md)、[E-008](02-execution/E-008-s5-release-and-asset-verification.md)

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| S1 | 契约冻结与信息就绪 | 完成（2026-10-17） | D-002 冻结带标签语法、补零/拒绝面与写集；I-001～I-003 登记并取得 cross provider 指定（Grok Build） |
| S2 | 规范与全部消费面同步 | 完成（2026-10-17） | canonical、根 AGENTS、prompts、四宿主安装源、规则模板、MCP guidance 与契约测试同改；镜像 stage `--check` 38 对通过、16 份 dogfood 副本一致；事实见 E-002 |
| S3 | 验证与运行证据影响核对 | 完成（2026-10-17） | skills 102 / docs 67 回归 OK；scripts 147 红（4 failures / 12 errors）归因于 16/16 运行证据过期，重捕获归属明确；见 E-003 |
| S4 | cross 审计、响应与关门 | 完成（2026-10-17） | A-001 self + A-002 Grok Build independent 落盘并由 A-003 响应（开放 required 0，2 条 recommended 保持 open）；A-004 关门就绪审视 `pass`；见 E-004 |
| S5 | 发布：证据重捕获 → CI 全绿 → 合并 main → tag → 资产验收 | 完成（2026-10-17） | 16 格证据 16/16 pass、两门禁转绿；清单/CHANGELOG 同步；本地门禁与 strict rehearsal/预检 `checks passed: True`；PR #31 CI 全绿 → merge `6ca04ee` → annotated tag `v0.13.7` → tag run 39034827440 的 pack 与 gated publish 全绿（Environment 由维护者人工审批）→ Release 9 项资产；资产逐项验收通过（摘要/子集/隔离安装/GHCR）。S5 的 independent 审计待出具，关门待用户。见 [D-003](01-decision/D-003-scope-extension-s5-release.md)、[E-006](02-execution/E-006-s5-evidence-recapture.md)、[E-007](02-execution/E-007-s5-pr-ci-merge-tag.md)、[E-008](02-execution/E-008-s5-release-and-asset-verification.md) |

顺序为 S1 → S2 → S3 → S4 → S5；本目标为可直接执行的小目标，不批量拆子目标，S1/S2 在同一轮完成。派生 `progress` = 完成阶段 **5 / 5 = 100%**（等权检查点；S5 由 D-003 于 2026-10-17 追加并在同日完成）；progress 不代表关门决定，也不放行任何门禁——`status` 仍为 `active`，关门待用户。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 带标签命令的精确语法：前缀拼写与大小写、位数与补零、是否接受完整 id/slug、拒绝面边界 | 方案冻结 | S1 退出 | 对照用户原话、现行 AD-01 与 workspace-protocol §2.7，形成契约与正反例 | verified | 语法或前缀要变更时重新裁决 | [D-002](01-decision/D-002-labeled-command-contract.md)：小写固定前缀 + 1～3 位补零；拒绝裸数字、大小写/拼写不符前缀、完整 id/slug、顺序错误 |
| I-002 | required | 消费面写集是否完整（canonical / 根 AGENTS / prompts / 四宿主安装源 / 规则模板 / MCP / 测试 / 镜像 / dogfood） | 实施 | S2 退出 | 全仓检索旧形式与入口面清单，改后 `--check` 与副本一致性核对 | verified | 新增消费面时复核 | [E-002](02-execution/E-002-surface-implementation.md)：53 个文件 + 1 新目录；镜像 38 对 `--check` ok；16 对 dogfood 复制前 `SAME`、复制后测试一致；规则面无旧形式残留 |
| I-003 | required | 本目标 cross 审计的 independent provider | 审计与关门 | S4 进入前 | 同步卡片收集用户指定并核对本机入口 | verified | 实际审计前再核对服务可用性；失败不降级/换 provider | 用户 2026-10-17 同步卡片选择 **Grok Build**（沿用 GOAL-013/014），见 [D-001](01-decision/D-001-scope-and-roadmap.md#用户裁决留痕同步阻塞卡片2026-10-17)；同日实际派发成功（exit 0，421.1 s），A-002 independent 落盘，见 [E-004](02-execution/E-004-s4-cross-audit-and-response.md) 与 [invocation.json](attachments/s4-grok-independent-01/invocation.json)。首次派发因沙箱禁止 `~/.grok` 建会话失败，同 provider 放宽文件权限重跑成功，未降级 |
| I-004 | required | 本次修正是否使既有 runtime/compatibility evidence 过期；保证范围与重捕获归属 | 验收与关门 | S3 退出 | 核对 behaviorSources 摘要并运行证据检查脚本；明确不在本目标内的工作 | verified | 入口/行为源或宿主版本变动时复核 | [E-003](02-execution/E-003-verification-and-evidence-impact.md)：`capture_runtime_evidence --check` exit 1，16/16 记录过期、24 个来源变更；scripts 4 failures / 12 errors 全部归因于此。重捕获由 [D-003](01-decision/D-003-scope-extension-s5-release.md) 收回 **S5**（原为范围外） |
| I-005 | required | 发布版本号：patch `v0.13.7` 或 minor `v0.14.0`（影响 CHANGELOG、pin、矩阵 `candidateRevision`、tag 与资产身份） | 版本清单、tag 与资产验收 | S5 版本清单步骤前 | 同步卡片收集用户裁决，并核对 CHANGELOG / 矩阵既有版本约定 | verified | 版本要变更时重新裁决 | 用户 2026-10-17 答复 **patch `v0.13.7`**；矩阵 `candidateRevision`、安装/GHCR pin 与 CI 证据目录均已对齐，见 [E-006](02-execution/E-006-s5-evidence-recapture.md) |
| I-006 | required | GitHub Copilot CLI 探针的 provider 环境如何构造（初判为凭据失效，经用户质疑后核对） | S5 步骤 a 退出 | S5 步骤 a 退出前 | 核对 Process/User 作用域环境变量与 runner 注入；重取 5 格 | verified | 宿主 provider 变量来源或 runner 变更时复核 | **根因更正**：不是凭据失效——`COPILOT_PROVIDER_API_KEY` 在 User 作用域有（len=36）、Process 作用域为空（harness 进程启动早于该变量写入），驱动 `os.environ.copy()` 因此传给宿主一个无 key 的环境。runner 增加 User→Process 注入后以 `-r2` 重取，copilot 5 格全部 pass；见 [E-006](02-execution/E-006-s5-evidence-recapture.md) |
| I-007 | required | Environment `release` 的人工审批结果（tag workflow 39034827440 的 gated publish） | S5 步骤 e 退出与资产验收 | S5 步骤 e 退出前 | 维护者在 GitHub 审批；编排侧回读 run、Release 与资产事实 | verified | 未审批不得宣称已发布；审批方式或环境配置变化时复核 | 部署 `release`（id `7139921295`）状态链 waiting→queued→in_progress→success，creator 均为 **`magicvr`（人工）**，发布后 `pending_deployments` 为空；run completed success、[Release v0.13.7](https://github.com/magicvr/goal-governance/releases/tag/v0.13.7) 9 项资产已发布并逐项验收，见 [E-008](02-execution/E-008-s5-release-and-asset-verification.md) |

## 父目标与台账

- 父目标：[GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)。本区 `workspace-002-methodology-skills-feedback`，canonical 为 `docs/workspaces/workspace-002-methodology-skills-feedback/`。
- 决策、事实、审计分别写入 `01-decision/`、`02-execution/`、`03-audit/` 的平铺条目并维护对应索引。审计模式为 `cross`（改 P-003 审计派发元规则）；independent provider 由用户指定。
- 本目标包含 S1～S4 的规范/消费面修正与 S5 的发布链路（16 格运行证据重捕获、版本清单、PR/CI/merge、annotated tag、gated 发布与资产验收）；**不包含**宿主产品本身改造与用户询问 UI 契约（GOAL-013 已交付部分）。Environment `release` 审批始终由用户人工完成，AI 不代批、不改配置。
