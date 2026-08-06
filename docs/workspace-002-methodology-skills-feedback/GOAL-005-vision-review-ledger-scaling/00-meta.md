---
id: GOAL-005-vision-review-ledger-scaling
title: 愿景审视台账分片与正式发布
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
plan_refs: VP-002-methodology-skills-feedback-evolution
primary_plan: VP-002-methodology-skills-feedback-evolution
serves_summary: 在 Root R3 内修复 Vision Review 单文件增长缺口，并完成可安装、可审计、可发布的协议闭环
created: 2026-08-06
updated: 2026-08-06
version: 0.3.0
progress: 100%
---

# GOAL-005 · 愿景审视台账分片与正式发布

## 概述

把持续增长的 `docs/vision/reviews.md` 从“索引与全部正文同一文件”改造成稳定索引与平铺独立报告共同构成的正式台账；保留 legacy inline 历史兼容，迁移本仓现有 VRev，更新方法论、Skills、模板、安装与测试，并通过 PR 合入 `main` 后发布新版本资产。

本目标是 [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md) R3 内的协议缺口修正切片；它不自动关闭 Root R3 或 VP-002。

## 成功标准

- [x] canonical 方法论明确 `reviews.md` 稳定索引 + `reviews/VRev-NNN-<slug>.md` 平铺报告、编号、阈值、legacy 兼容与权威边界
- [x] 本仓现有 `VRev-001`～`VRev-006` 完成无重编号、无语义改写的迁移，索引链接与开放 required 投影可验证
- [x] `/vision`、`/vision-audit`、模板、bootstrap、安装/消费说明、Skills 镜像和自动化测试全部同步
- [x] 全量验证通过，self + independent cross audit 无开放 required finding
- [x] 变更经 PR 合入 `main`，新版本 annotated tag、GitHub Release、下载资产摘要与消费包边界验证完成

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 完成判据 |
|------|------|------|----------|
| **S1** | 协议与迁移契约冻结 | **完成**（2026-08-06） | D-001 固定终态、legacy 边界、响应投影、审计模式与发布边界 |
| **S2** | canonical 与现有台账迁移 | **完成**（2026-08-06） | 核心规范、模板与本仓 VRev 分片完成，兼容校验通过 |
| **S3** | Skills / 安装 / 测试同步 | **完成**（2026-08-06） | 提示词、镜像、bootstrap、consumer 与自动化覆盖一致 |
| **S4** | 全量验证与 cross close-out | **完成**（2026-08-06） | 全量测试、self 与 independent 意见闭环，开放 required = 0 |
| **S5** | PR、main 与正式 Release | **完成**（2026-08-06） | PR #11 合并、annotated `v0.13.0` tag、gated Actions run、9 项资产与消费验证完成 |

## 派生进度展示

`progress: 100%` = 5 个等权阶段 S1～S5 全部完成。该值只作展示，正式关门事实以 D-003 闭门决策与 A-005 闭门审计为准。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 当前 Vision Review 的编号、体量、inline/响应结构与历史语义边界 | S1 契约冻结 / S2 迁移 | S1 | 扫描 `reviews.md`、alignment、principles 与现有 finding 响应 | **verified**（2026-08-06） | 迁移前后重跑一致性校验 | `VRev-001`～`VRev-006`；30,473 bytes / 352 行；索引与正文同文件；见 D-001 / E-001 |
| I-002 | required | canonical、Skills、模板、bootstrap、安装与测试的完整受影响面 | S2 / S3 实施 | S2 前 | repository-wide `rg` + stage/check + docs/skills/scripts 测试 | **verified**（2026-08-06） | 后继 audit 发现新影响面时回流 | canonical/镜像、四宿主 wrappers、bootstrap、consumer 文档、模板、fixtures 与测试已同步；`32 + 42 + 72` 测试通过 |
| I-003 | required | 新版本号、当前 tag/Release、资产清单、main/Environment 门禁 | S5 发布 | S4 关门前 | 读取版本权威、workflow、compatibility/release tooling 与远端状态；绑定 fresh runtime evidence | **verified**（2026-08-06） | S5 已复核：正式 `v0.13.0` 身份确立（E-004 / D-003 / A-005）；owner: GOAL-005 | 正式 `v0.13.0`（merge `33934efc`、tag object `29d5b28c`、run `31073547050`）；9 项资产 digest 与隔离消费验证完成 |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)

## 审计模式

`cross`。本目标修改核心元规则、迁移愿景审计权威记录并进入正式发布边界：S4 至少需要一条 `source: self` 与一条由独立 Codex 子会话形成、可核对并落盘的 `source: independent` 意见。
