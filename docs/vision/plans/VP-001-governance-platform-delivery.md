---
doc_type: vision-plan
id: VP-001-governance-platform-delivery
title: 治理平台可复用交付（方法论 · Skills · Web）
status: active
vision_ref: vision-goal-governance@0.1.0
lead_workspace: workspace-001-goal-governance
created: 2026-07-28
updated: 2026-07-30
version: 0.1.1
---

# VP-001 · 治理平台可复用交付

## 意图

在现行 Charter（`vision-goal-governance@0.1.0`）下，持续交付并加固 Goal Governance 的三面能力：

1. 核心方法论、文档协议与 canonical 模板（含工作区、共享资料与本愿景体系）。
2. Skills 消费适配器（安装、编排、审计、发布一致性）。
3. 面向人的 AI 协助 Web 工作台（有界可用，扩展 residual 另跟踪）。

本规划是 **primary 工作区** 当前焦点：把「可复用治理平台」从已完成的基础阶段推进到可对外复用与可维护的产品形态，而不把 Charter 本身标为可完成目标。

## 方向级退出判据

在同时满足下列方向时，本 VP **可以**有界或完整关门（证据必须在工作区目标内，本文件只做纲领确认）：

1. 核心协议（含愿景/工作区/资料边界）可独立复制使用，且 dogfood 工作区对齐链完整。
2. Skills 主路径按既有发布门禁可验证：实现层 `/govern`、Goal 交叉审 `/audit`、决策层 `/vision`、独立 Vision Review `/vision-audit`，以及安装与发布约定（默认四入口面）。
3. Web 主路径在已接受的 residual 边界内可用；未关闭的扩展 residual 已显式点名，不假装终态。
4. 无未处理的、阻断本规划退出的 required 协议缺口（或已用户书面接受 residual）。

完整产品「终态宣称」**不是**本 VP 的默认退出条件；若仅有界退出，须在关门记录中列出 residual → 区/目标。

## 工作区绑定

| workspace_id | root_goal | role | joined | notes |
|--------------|-----------|------|--------|-------|
| workspace-001-goal-governance | GOAL-001-main-vision | lead | 2026-07-28 | Primary dogfood；现行全部 GOAL-* 过程树 |

> 未列入的工作区不推进本 VP。允许多区并行时在本表追加 `support` 行，并建议保持 `lead_workspace`。

## 关门记录

（仅 `closed` / `abandoned` 时填写。当前 `active`，无关门记录。）

| date | outcome | summary | evidence_links | residuals |
|------|---------|---------|----------------|-----------|
| — | — | — | — | — |

## 规划修订短史

| date | change |
|------|--------|
| 2026-07-30 | **editorial**（V-F-007 fixed）：退出判据 §2 Skills 主路径补全 `/vision`、`/vision-audit`；不改意图/退出边界实质；`vision_ref` 仍 `vision-goal-governance@0.1.0`。 |
| 2026-07-28 | 初创；承接 Root 长期交付意图，作为 Charter v0.1.0 下首个 active VP。 |
