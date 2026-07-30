---
doc_type: vision-plan
id: VP-003-human-ui-workbench-deferred
title: 人类 UI / Web 工作台（延期 · 待通用基架）
status: planned
vision_ref: vision-goal-governance@0.2.0
lead_workspace: 
created: 2026-07-31
updated: 2026-07-31
version: 0.1.0
---

# VP-003 · 人类 UI / Web 工作台（延期）

## 意图

在协议与 Skills 经真实使用足够稳定、且**通用 Web 基架**可对接（或用户书面改回本仓投资）时，交付面向人的目标治理 UI，使同一协议可在人机界面一致使用。

**当前**：本仓 FastAPI `web/` 为 **VP-001 留下的冻结参考实现**；本 VP **planned**，**不**投入产品推进。  
战略假设：**H-WEB-01**（基架优先于本仓长期维护 FastAPI 面）。

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
| 本仓 `web/` | frozen reference；删除/重建另决 |

## 规划修订短史

| date | change |
|------|--------|
| 2026-07-31 | 初创 `planned`；组合编排意图 3；不激活、不挂区。 |
