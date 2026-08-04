---
doc_type: vision-plan
id: VP-003-human-ui-workbench-deferred
title: 人类 UI / Web 工作台（挂起 · 待通用基架）
status: planned
vision_ref: vision-goal-governance@0.2.0
lead_workspace: 
created: 2026-07-31
updated: 2026-08-04
version: 0.2.0
---

# VP-003 · 人类 UI / Web 工作台（正式挂起）

## 意图

在协议与 Skills 经真实使用足够稳定、且**通用 Web 基架**可对接（或用户书面改回本仓投资）时，交付面向人的目标治理 UI，使同一协议可在人机界面一致使用。

**当前**：本仓 FastAPI `web/` 冻结资产已由 [GOAL-004-frozen-web-asset-retirement](../../workspace-002-methodology-skills-feedback/GOAL-004-frozen-web-asset-retirement/00-meta.md) 完成物理移除；本 VP 仍保持合法的 **`planned`** 状态并正式挂起，**不**投入产品推进。恢复只允许由新的书面决策重新定义产品边界、基架与工作区；不得把本次删除当作恢复或自动重建。
战略假设：**H-WEB-01**（基架优先于本仓长期维护 FastAPI 面）。

## 挂起决策（2026-08-04）

- **挂起含义**：本 VP 没有排期、没有绑定工作区，也不产生当前实现门禁；`status: planned` 是 VP 合法状态，不把 `paused` 写入状态枚举。
- **资产处置**：冻结 `web/` 资产及其专属 CI / parser evidence 已由 workspace-002 的 GOAL-004 一次性移除；历史目标、审计和发布记录保留为历史事实。
- **重新激活条件**：用户新的书面决策 + 通用基架对接边界（或明确推翻 H-WEB-01）+ 新工作区/目标与独立审计；本文件不会自行激活。

## 方向级退出判据（激活后适用）

1. 人类主路径可完成发现上下文 → 审查候选 → 确认受控写入（或用户书面收窄范围）。
2. 不另立第二套目标状态；fail closed 与 P-004 边界可验证。
3. 与当时现行协议/Skills 版本消费一致；R-009-X 等 residual 显式处理。
4. 实现路径：优先通用基架；恢复本仓 FastAPI 产品投资须用户书面推翻 H-WEB-01。

## 工作区绑定

| workspace_id | root_goal | role | joined | notes |
|--------------|-----------|------|--------|-------|
| — | — | — | — | 激活时另定；可与演进区分区或同区，须用户选型 |

## 关门记录

（当前 `planned`，无关门记录。）

| date | outcome | summary | evidence_links | residuals |
|------|---------|---------|----------------|-----------|
| — | — | — | — | — |

## 从 VP-001 继承的 residual 指针

| ID | 说明 |
|----|------|
| **R-009-X** | Web 产品终态 / I 全文 / 人手 UX 全文等；仍 accepted，不在 VP-001 关闭 |
| 本仓 `web/` | 已由 GOAL-004 物理退役；未来 UI 只能按新决策重建 |

## 规划修订短史

| date | change |
|------|--------|
| 2026-08-04 | 用户决定彻底移除冻结 Web 资产并正式挂起本 VP；保持 `planned`，不激活、不挂区，恢复须新书面决策。 |
| 2026-07-31 | 初创 `planned`；组合编排意图 3；不激活、不挂区。 |
