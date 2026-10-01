---
id: GOAL-010-release-gate-recapture-and-v0-13-4
title: 发布门禁转绿与 v0.13.4 正式发布
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.2.0
progress: 75%
---

# GOAL-010 · 发布门禁转绿与 v0.13.4 正式发布

## 概述

`dev` 顶端的**发布门禁是红的**：v0.13.3 的 12 格宿主 runtime 证据在 `d1256eb` 改根 `AGENTS.md` 与编排提示之后全部过期，`scripts/compatibility_report.py`、`scripts/release_evidence.py --mode rehearsal` 与 `scripts/tests/test_release_evidence.py`（4 failures / 12 errors）随之失败。发布工作流的 publish job 以 `release_evidence --mode release` 为第一步，因此在证据刷新之前**任何 tag 都不可能产出资产**。

本目标把门禁重新转绿，并完成一次正式发布：对当前树重捕获 **3 宿主 × 4 治理入口 = 12 格** L3 证据（矩阵消费者为 claude-code-cli / grok-build-cli / github-copilot-cli；codex 仍只是 install surface，不入矩阵），修掉与本轮 containment 规则不一致的 Windows 安装器测试，同步版本清单（CHANGELOG / 兼容矩阵 / 三处安装 pin），走 `dev` → PR → `main` 合并 → annotated tag `v0.13.4` → Release 资产。

本目标属于 Root 纲领 **R3（持续闭环与长期演进）**，沿用 GOAL-008（v0.13.3）建立的发布纪律：tag 只指向已合并 `main` 的 merge commit，发布身份由 merged-main ancestry + annotated tag + strict release evidence 共同建立。

## 成功标准

- [x] 12 格 L3 宿主证据在 `docs/releases/runtime/v0.13.4/` 重捕获，全部 `verdict: pass`，`capture_runtime_evidence.py --check` 12/12 一致
- [x] 兼容矩阵 `candidateRevision = v0.13.4`，三宿主 12 格 `runtime-verified`，`evidence` 指向新目录
- [x] `scripts/compatibility_report.py` 与 `release_evidence.py --mode rehearsal --run-checks` 通过；`scripts/tests`、`skills/tests`、`docs/tests` 全绿
- [x] 与本轮 containment 规则不一致的 Windows 安装器测试已修，保留原判定语义
- [x] 版本清单一致：CHANGELOG 有 `0.13.4` 节（标注为发布候选）、三处安装 pin 指向 `v0.13.4`
- [ ] PR 合入 `main` 后 annotated tag `v0.13.4` 指向该 merge commit，publish job 经 Environment `release` 审批发布 9 项资产且 zip 摘要与 sidecar 一致

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 门禁缺口核对与发布范围冻结 | 已完成（2026-10-01） | 缺口可复现（命令 + 失败计数 + 文件行），版本号与发布纪律冻结；不改代码。证据：[D-001](01-decision/D-001-scope-freeze-v0-13-4.md) |
| **S2** | 证据重捕获与清单修正 | 已完成（2026-10-01） | 12 格证据重捕获并全部 `pass`；矩阵改指新目录；CHANGELOG 与三处 pin 同步；containment 测试修好。证据：[E-001](02-execution/E-001-recapture-12-cells.md)、[E-002](02-execution/E-002-test-realignment-and-manifest.md) |
| **S3** | 回归、门禁与 independent 发布候选审计 | 已完成（2026-10-01） | 三套测试全绿、镜像 0 漂移、`--require-ready` 与 rehearsal 通过；independent 审计落盘（A-002 `pass`，开放 required = 0）且 5 条 recommended 已闭合。证据：[E-003](02-execution/E-003-regression-gates-and-release.md)、[A-002](03-audit/A-002-independent-release-candidate.md)、[A-003](03-audit/A-003-response-a002.md) |
| **S4** | PR、合并、tag 与资产核对 | 进行中 | PR 绿后合入 `main`；annotated tag 指向 merge commit；publish 经 Environment 审批；9 项资产核对完成 |

S1 先做且已完成。S2、S3 已完成。S3 的 independent 审计结论为 `pass` 且开放 required 为 0，故放行 S4。`progress` 只来自本表：已完成阶段数 / 4。

## 派生进度展示

`progress: 75%` = 上表 4 个阶段完成 **3 / 4**。progress 只展示。它不放行阶段、不关闭 finding、不覆盖信息门禁，也不推导 `status: done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 门禁为何在 `dev` 顶端是红的；修复路径是重捕获还是回滚 `AGENTS.md` 变更 | S1 范围冻结 | S1 | 在临时 worktree 对 `4d35623`（证据录制点）与 `d30abb3`（`dev` 顶端）跑同一测试对照 | **verified**（2026-10-01） | — | 录制点通过、顶端失败 → 变更是**正确**的、证据过期是唯一缺口；回滚会撤销 GOAL-009 的 P-005 条文。见 [D-001](01-decision/D-001-scope-freeze-v0-13-4.md) |
| I-002 | required | 本机三个矩阵宿主 CLI（claude / grok / copilot）能否对当前树产出 `pass` 证据；任一失败该格如何处置 | S2 证据重捕获 | S2 | 逐宿主跑探针；失败保留原样、不静默降级、不冒充通过 | **verified**（2026-10-01） | — | 三宿主 12 格全部 `pass`（claude 2.1.285 / grok 1.0.44 / copilot 1.0.75）；过程偏差见 [E-001](02-execution/E-001-recapture-12-cells.md) |
| I-003 | required | 发布版本号与发布纪律（tag 指向何处、资产集合） | S1 范围冻结 | S1 | 用户裁决 + 沿用 GOAL-008 纪律 | **verified**（2026-10-01） | — | 用户选定 **`v0.13.4`（patch）**；annotated tag 指向已合并 `main` 的 merge commit，资产集合沿用 v0.13.3 的 9 项形态。见 [D-001](01-decision/D-001-scope-freeze-v0-13-4.md) |
| I-004 | required | 发布属 `release` / `compatibility` 高影响门禁，independent 审计的 provider 与 scope | S3 审计 | S3 前 | 用户书面指定；provider 失败不降级、不由编排器冒充 | **verified**（2026-10-01） | CLI 不能给出可核对意见时，门禁回到未满足 | 用户书面指定 **scope = 发布候选完整审计**；provider 最初为本地 codex CLI，因该 CLI 在本机沙箱下无法初始化（`failed to initialize in-process app-server client: os error 5`）而经用户书面**改派为本地 grok build CLI（`grok-4.6`）**；A-002 已由该 provider 落盘（`pass`，开放 required = 0）。见 [D-002](01-decision/D-002-independent-audit-provider-and-scope.md) |
| I-005 | non-blocking | 与本轮 containment 规则不一致的 Windows 安装器测试是否纳入本轮修复 | S2 实施 | S2 | 用户裁决 | **verified**（2026-10-01） | — | 用户选择**修测试**：让它在新的 containment 规则下成立，同时保留「拒绝二次 init」的原意。见 [D-003](01-decision/D-003-containment-test-realignment.md) |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)（R3 纲领阶段内子目标）

## 台账布局

本目标使用平铺 ledger：`01-decision/`、`02-execution/`、`03-audit/`。索引文件只登记条目。

## 备注

- 本轮不新增架构规则；`docs/architecture/`、`docs/templates/`、`docs/vision/alignment.md` 的 canonical 正文**不改**，因此镜像 stage 只作为一致性守卫运行。
- `docs/contracts/**` 改动会进 stage 白名单，必须同一任务内 stage 并提交镜像（AGENTS §8c）。
- 证据文件是本目标的**产品**：`docs/releases/runtime/v0.13.4/` 的 12 份 JSON 与各自 `.d/` 原始 stdout/stderr 都要入库。
