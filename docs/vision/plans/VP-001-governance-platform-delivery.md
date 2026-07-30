---
doc_type: vision-plan
id: VP-001-governance-platform-delivery
title: 治理协议与 Skills 可复用交付（Web 冻结）
status: active
vision_ref: vision-goal-governance@0.2.0
lead_workspace: workspace-001-goal-governance
created: 2026-07-28
updated: 2026-07-31
version: 0.2.0
---

# VP-001 · 治理协议与 Skills 可复用交付（Web 冻结）

## 意图

在现行 Charter（`vision-goal-governance@0.2.0`）下，持续交付并加固 **可复用治理协议** 与 **Skills 消费适配器**，使协议可在文档-only 与 AI/Git 协作中一致使用，并随**实际项目**中发现的问题回流演进。

交付面优先级：

1. **核心方法论、文档协议与 canonical 模板**（含工作区、共享资料与愿景体系）——权威与可复制性。
2. **Skills 消费适配器**（安装、编排、审计、愿景入口、发布一致性）——现行主消费路径。
3. **人类 Web 工作台**——阶段 6 **有界成果保留**为本仓 **冻结参考实现**（`web/`）；**不**作为本 VP 的产品推进面；扩展 residual（如 R-009-X）保持 accepted，不假装终态、也不假装在投。远期人类 UI 预期挂接通用 Web 基架（Charter **H-WEB-01**）。

本规划是 **primary 工作区** 当前意图：把「可复用治理」保持在可对外启用与可维护状态，焦点为协议质量与 Skills 在真实使用中的可靠性，而不把 Charter 本身标为可完成目标，也不以本仓 FastAPI 终态为成功条件。

## 方向级退出判据

在同时满足下列方向时，本 VP **可以**有界或完整关门（证据必须在工作区目标内，本文件只做纲领确认）：

1. 核心协议（含愿景/工作区/资料边界）可独立复制使用，且 dogfood 工作区对齐链完整。
2. Skills 主路径按既有发布门禁可验证：实现层 `/govern`、Goal 交叉审 `/audit`、决策层 `/vision`、独立 Vision Review `/vision-audit`，以及安装与发布约定（默认四入口面）。
3. **本仓 Web**：阶段 6 有界交付已记录；实现定位为 **frozen reference**；未关闭的扩展 residual 已显式点名；**不**以「Web 产品终态」或「继续深化本仓 FastAPI」为退出必要条件。
4. 无未处理的、阻断本规划退出的 required 协议缺口（或已用户书面接受 residual）。
5. （方向）演进叙事以实际项目 / 消费方问题驱动协议与 Skills 回流，而非本仓 Web backlog。

完整产品「Web 终态宣称」**不是**本 VP 的退出条件。若仅有界退出，须在关门记录中列出 residual → 区/目标。

## 工作区绑定

| workspace_id | root_goal | role | joined | notes |
|--------------|-----------|------|--------|-------|
| workspace-001-goal-governance | GOAL-001-main-vision | lead | 2026-07-28 | Primary dogfood；现行全部 GOAL-* 过程树；2026-07-31 re-align 至 Charter 0.2.0 |

> 未列入的工作区不推进本 VP。允许多区并行时在本表追加 `support` 行，并建议保持 `lead_workspace`。

## 关门记录

（仅 `closed` / `abandoned` 时填写。当前 `active`，无关门记录。）

| date | outcome | summary | evidence_links | residuals |
|------|---------|---------|----------------|-----------|
| — | — | — | — | — |

## 规划修订短史

| date | change |
|------|--------|
| 2026-07-31 | **strategic 对齐 Charter 0.2.0**：意图改为协议 + Skills 主交付；本仓 Web 冻结参考；退出判据去掉 Web 产品路径；`vision_ref` → `vision-goal-governance@0.2.0`；version **0.2.0**。 |
| 2026-07-30 | **editorial**（V-F-007 fixed）：退出判据 §2 Skills 主路径补全 `/vision`、`/vision-audit`；不改意图/退出边界实质；`vision_ref` 仍 `vision-goal-governance@0.1.0`。 |
| 2026-07-28 | 初创；承接 Root 长期交付意图，作为 Charter v0.1.0 下首个 active VP（当时三面含 Web 产品路径）。 |
