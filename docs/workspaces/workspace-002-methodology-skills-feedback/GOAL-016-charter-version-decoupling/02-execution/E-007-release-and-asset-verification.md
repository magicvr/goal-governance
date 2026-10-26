---
id: E-007
goal: GOAL-016-charter-version-decoupling
doc: execution-entry
title: v0.13.8 正式发布、资产验收与 issue #34 关闭
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

# E-007 · v0.13.8 正式发布、资产验收与 issue #34 关闭（2026-10-26）

## 发布事实

1. PR [#35](https://github.com/magicvr/goal-governance/pull/35) 的 `contract-and-report` 与 `windows-install-surface` CI 全绿；merge commit **`43467a36f024462c03b2a3c9d81789b3617c91e2`**（2026-10-26T15:29:43Z）。
2. 在 merge commit 上创建 annotated tag **`v0.13.8`**（tag object `d0289660de2b2723bd952d9d7604b1fc65adc94f`），本地 strict precheck `release_evidence --mode release --tag v0.13.8 --run-checks`：`release status: release-candidate`、`checks passed: True`、工作树 clean；随后 push tag。
3. Tag workflow [40350346249](https://github.com/magicvr/goal-governance/actions/runs/40350346249)：`pack` 成功；`Publish GitHub Release (gated)` 在 Environment `release` 等待，**用户 2026-10-26 通过同步卡片确认真实批准**；deployment `7336110432` 状态链 `waiting→queued→in_progress→success`（creator 均为 `magicvr`），发布后 `pending_deployments` 为空；AI 未代批、未改环境配置。publish job 成功（2026-10-26T15:38:17Z）。
4. [Release v0.13.8](https://github.com/magicvr/goal-governance/releases/tag/v0.13.8) 于 **2026-10-26T15:38:09Z** 发布，`isDraft=false` / `isPrerelease=false`，**9 项资产**。

## 资产验收（全部使用实际下载产物）

- 下载目录：`%TEMP%\gg-v0.13.8-assets\`。
- 双 ZIP SHA-256 与 sidecar 一致：skills `3b7da9c0…`、core `48f93f6e…`。
- Core 27 个成员在 Skills 86 成员的 `goal-governance-skills-v0.13.8/core/` 前缀下逐字节相同（missing 0 / diff 0）。
- 下载的 `release-evidence.json`：`releaseStatus=release-candidate`、`checksPassed=true`、`source.commit=43467a3…`、`annotatedTag=v0.13.8`、`tagObject=d0289660…`、工作树 clean、720 条 digest、4 项 checks。
- 下载的 `compatibility-report.json`：`coverage.status=ready-for-release-evidence`、`candidateRevision=v0.13.8`、`source.commit=43467a3…`。
- 隔离消费安装：解压下载的 skills ZIP 到临时 consumer，`install.ps1 -All -SkillsDir .\skills -MethodologyDir .\docs -NonInteractive -Force` exit 0；消费者自有规则 `KEEP-CONSUMER-RULE-138` 保留，`AGENTS.md` 有 managed 块，`docs/architecture/principles.md` 与 `.claude/skills/govern/SKILL.md` 均存在。
- GHCR：`ghcr.io/magicvr/goal-governance-mcp-server:0.13.8` digest `sha256:b4611d9bc65161ea4d6ce58bded01ca032496094288222d920296641634c7195`；容器内 `server.py --version` 输出 `goal-governance-mcp 0.13.8`。
- 结构化记录：[asset-verification.json](../attachments/asset-verification.json)。

## issue #34

GitHub issue [#34](https://github.com/magicvr/goal-governance/issues/34) 于 2026-10-26T15:45:12Z 关闭（`state=CLOSED`、`stateReason=COMPLETED`），评论链接 v0.13.8 Release 与本目标证据。

## 已知残余

- **R-016-001（low / recommended open；下一 patch 触发）**：矩阵 `host.version` 基线仍为 Claude Code CLI `2.1.301` / Grok Build `1.0.60`，本次证据实际在 `2.1.310` / `1.0.70` 上采集；兼容报告与发布证据均通过，证据 envelope 记录实际版本。下一次矩阵刷新对齐，不回写 v0.13.8 历史资产。

## 尚未完成

- 尚未进行 S5 关门审计（self + independent）与用户关门确认；GOAL-016 仍 `active / 80%`，不得据本条标 `done`。
- 未改写 v0.13.7 及更早的历史 Release/证据。
