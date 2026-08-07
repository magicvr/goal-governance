---
id: workspace-002-methodology-skills-feedback
title: 方法论与 Skills 反馈演进工作区
status: active
root_goal: GOAL-001-methodology-skills-feedback-evolution
canonical_scope: docs/workspace-002-methodology-skills-feedback/
shared_materials_catalog: docs/shared-materials/
vision_role: delivery
plan_refs: VP-002-methodology-skills-feedback-evolution
primary_plan: VP-002-methodology-skills-feedback-evolution
created: 2026-07-31
updated: 2026-08-08
version: 0.3.0
---

# 工作区上下文 · 方法论与 Skills 反馈演进

本工作区承载 **VP-002** 的交付：以真实项目 / 消费方使用中发现的问题为触发，持续修正核心方法论与 Skills。`goal-tree.md` 与所有 `GOAL-*` 文件夹直接位于本目录；它们是本工作区唯一的目标状态真相。

**奠基封存区**见 [workspace-001-goal-governance](../workspace-001-goal-governance/workspace.md)（`vision_role: primary`，Root done）。本区为 **delivery**，不替代 monorepo primary 身份。

## 绑定

| 字段 | 当前值 | 说明 |
|------|--------|------|
| 工作区 ID | `workspace-002-methodology-skills-feedback` | 共享资料引用的 `workspace_id` 必须一致。 |
| Root Goal | `GOAL-001-methodology-skills-feedback-evolution` | `parent: null`。 |
| canonical 范围 | `docs/workspace-002-methodology-skills-feedback/` | 本区唯一目标状态范围。 |
| 共享资料目录 | `docs/shared-materials/` | 工作区外的共同资料根；不保存目标状态。 |
| 愿景角色 | `delivery` | monorepo primary 仍为 workspace-001；本区交付 VP-002。 |
| 规划对齐 | `VP-002-methodology-skills-feedback-evolution` | `primary_plan`；`vision_ref` 须匹配 Charter `vision-goal-governance@0.2.0`。 |
| 工作区 status | `active` | 2026-07-31 scaffold + Root 立项。 |

## 愿景对齐

完整治理下仓库**必有**唯一 [docs/vision/](../vision/) Charter。本工作区通过必填 `plan_refs` / `primary_plan` 对齐 [VP-002](../vision/plans/VP-002-methodology-skills-feedback-evolution.md)；VP 再对齐 Charter `vision-goal-governance@0.2.0`。细则见 [vision/alignment.md](../vision/alignment.md) 与 P-006。  
**不要**在本文件维护 progress% 或把愿景目录当作第二套目标树。

## 固定共享资料引用

> `shared-materials/index.json` 只能提供候选路径与摘要。缺 `material_id`、`source`、`version`、64 位十六进制 `sha256` 或匹配 `workspace_id` 的行无效，不能作为事实、证据或跨工作区上下文来源。

| reference_id | workspace_id | material_id | source | version | sha256 | purpose | local_record | status |
|--------------|--------------|-------------|--------|---------|--------|---------|--------------|--------|

## 边界

- 目标仅能由本工作区内的五件套和 `goal-tree.md` 表达；禁止跨区 `parent`。
- **禁止**把 [workspace-001](../workspace-001-goal-governance/) 已 done Root 下的编号或状态当作本区真相。
- 跨区提及目标：文档默认 **Q2** 路径，对话默认 **Q3** 标签。
- 共享资料只按固定版本和哈希引用；内容须用户确认才可成事实或证据。
- 本区不把本仓 Web 产品终态作为成功条件（人类 UI 见 **VP-003**）；GOAL-004 只承接冻结资产退役和 producer 边界验证，不激活 VP-003。

## 备注

- 开区：用户 2026-07-31 `/govern` 确认 slug、Root、首子目标（Codex Skills 入口）与 `delivery` 角色。
- VP-002 原「0 区空转」自本区 scaffold 起结束；`lead_workspace` 指向本区。
- **长期持续治理（2026-08-08，D-008）**：用户确认本区与 VP-002 为长期持续治理项目，暂不关门——Root/VP-002 保持 `active`；R3 转为「持续闭环与长期演进」；退出判据挂起（核对结论留档于 Root 01-decision D-008）；新工作按反馈随时立项（GOAL-002～006 已 done，下一编号 GOAL-007）。
