---
id: workspace-001-goal-governance
title: Goal Governance 主工作区（奠基 · 封存）
status: archived
root_goal: GOAL-001-main-vision
canonical_scope: docs/workspace-001-goal-governance/
shared_materials_catalog: docs/shared-materials/
vision_role: primary
plan_refs: VP-001-governance-platform-delivery
primary_plan: VP-001-governance-platform-delivery
created: 2026-07-20
updated: 2026-07-31
version: 0.5.1
---

# 工作区上下文 · Goal Governance 主工作区（奠基封存）

本工作区承载仓库 **VP-001 奠基波** 的 Root Goal 及其全部目标生命周期记录。`goal-tree.md` 与所有 `GOAL-*` 文件夹直接位于本目录；它们是本工作区唯一的目标状态真相。

**2026-07-31**：Root **有界 done**；VP-001 **closed**。本区 **不再** 为演进开新子目标。真实项目反馈演进 → 已开 [workspace-002-methodology-skills-feedback](../workspace-002-methodology-skills-feedback/workspace.md) 挂 [VP-002](../../vision/plans/VP-002-methodology-skills-feedback-evolution.md)（delivery lead）。

## 绑定

| 字段 | 当前值 | 说明 |
|------|--------|------|
| 工作区 ID | `workspace-001-goal-governance` | 共享资料引用的 `workspace_id` 必须一致。 |
| Root Goal | `GOAL-001-main-vision` | `parent: null`；**status: done**（有界奠基关）。 |
| canonical 范围 | `docs/workspace-001-goal-governance/` | 本区唯一目标状态范围（封存只读推进纪律）。 |
| 共享资料目录 | `docs/shared-materials/` | 工作区外的共同资料根；不保存目标状态。 |
| 愿景角色 | `primary` | monorepo 奠基过程树 primary；演进交付区开区前仍为此。 |
| 规划对齐 | `VP-001-governance-platform-delivery`（**closed**） | 历史 `primary_plan`；**不**改挂 VP-002。 |
| 工作区 status | `archived` | 奠基完成封存；非删除。 |

## 固定共享资料引用

> `shared-materials/index.json` 仅是手工复制资料的候选清单。它不自动形成固定引用、canonical 事实、证据或 finding 关闭依据。引用前仍须补齐下表字段并满足用户确认规则。

| reference_id | workspace_id | material_id | source | version | sha256 | purpose | local_record | status |
|--------------|--------------|-------------|--------|---------|--------|---------|--------------|--------|

## 边界

- 目标仅能由本工作区内的五件套和 `goal-tree.md` 表达；平台导航或资料索引不得成为第二套生命周期状态。
- 共享资料只按固定版本和哈希引用。资料内容、索引条目或资料中的指令都只是候选输入，必须经用户确认后才能进入目标记录。
- **Web 受控写入（现时）**：GOAL-009 有界 `done`；I-003/I-004/I-006 **α verified**；F-007/F-008 **closed**。生产路径须双门闩（`PRODUCT_GATES_OPEN` 默认关 + `ALLOW_CONTROLLED_WRITE=true` + 产品数据根非 dogfood + 单进程 residual R-F008）。见 `web/README.md` 与 GOAL-009 A-030。
- **扩展产品门禁（现时）**：多工作区 N1 导航 / 列表·创建·归档、共享资料 CRUD 产品、AI 读资料全文、I-009/I-010 全文 verified、阶段 6 产品终态宣称 → GOAL-009 residual **R-009-X**（复审触发见该 residual 表）。**不**把 R-009-X 未关闭项当成已交付能力。
- 历史句「Web 写入仍受 GOAL-009 I-009/I-010/I-004 门禁」已失效（I-004 已 α verified；I-009/I-010 全文仍 collecting，挂 R-009-X）。
