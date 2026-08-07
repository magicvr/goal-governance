---
id: workspace-003-mcp-file-dual-channel
title: 消费交付双通道（MCP + File）工作区
status: closed
root_goal: GOAL-001-mcp-file-dual-channel-delivery
canonical_scope: docs/workspace-003-mcp-file-dual-channel/
shared_materials_catalog: docs/shared-materials/
vision_role: delivery
plan_refs: VP-004-mcp-file-dual-channel-delivery
primary_plan: VP-004-mcp-file-dual-channel-delivery
created: 2026-08-07
updated: 2026-08-07
version: 0.2.0
---

# 工作区上下文 · 消费交付双通道（MCP + File）

本工作区承载 **VP-004** 的交付：File 与 MCP 双通道一等公民、四承诺宿主适配、可配置 `governance_root` 与最小共享测试内核。`goal-tree.md` 与所有 `GOAL-*` 文件夹直接位于本目录；它们是本工作区唯一的目标状态真相。

**奠基封存区**见 [workspace-001-goal-governance](../workspace-001-goal-governance/workspace.md)（`vision_role: primary`，Root done）。**方法论演进区**见 [workspace-002-methodology-skills-feedback](../workspace-002-methodology-skills-feedback/workspace.md)（VP-002）。本区为 **delivery**，不替代 monorepo primary 身份，也不改写 VP-002 的 primary_plan。

## 绑定

| 字段 | 当前值 | 说明 |
|------|--------|------|
| 工作区 ID | `workspace-003-mcp-file-dual-channel` | 共享资料引用的 `workspace_id` 必须一致。 |
| Root Goal | `GOAL-001-mcp-file-dual-channel-delivery` | `parent: null`。 |
| canonical 范围 | `docs/workspace-003-mcp-file-dual-channel/` | 本区唯一目标状态范围。 |
| 共享资料目录 | `docs/shared-materials/` | 工作区外的共同资料根；不保存目标状态。 |
| 愿景角色 | `delivery` | monorepo primary 仍为 workspace-001。 |
| 规划对齐 | `VP-004-mcp-file-dual-channel-delivery` | `primary_plan`；`vision_ref` 须匹配 Charter `vision-goal-governance@0.2.0`。 |
| 工作区 status | `active` | 2026-08-07 scaffold + Root 立项。 |

## 愿景对齐

完整治理下仓库**必有**唯一 [docs/vision/](../vision/) Charter。本工作区通过必填 `plan_refs` / `primary_plan` 对齐 [VP-004](../vision/plans/VP-004-mcp-file-dual-channel-delivery.md)；VP 再对齐 Charter `vision-goal-governance@0.2.0`。细则见 [vision/alignment.md](../vision/alignment.md) 与 P-006。
**不要**在本文件维护 progress% 或把愿景目录当作第二套目标树。

## 固定共享资料引用

> `shared-materials/index.json` 只能提供候选路径与摘要。缺 `material_id`、`source`、`version`、64 位十六进制 `sha256` 或匹配 `workspace_id` 的行无效，不能作为事实、证据或跨工作区上下文来源。

| reference_id | workspace_id | material_id | source | version | sha256 | purpose | local_record | status |
|--------------|--------------|-------------|--------|---------|--------|---------|--------------|--------|

## 边界

- 目标仅能由本工作区内的五件套和 `goal-tree.md` 表达；禁止跨区 `parent`。
- **禁止**把 workspace-001 已 done Root 或 workspace-002 的编号/状态当作本区真相。
- 跨区提及目标：文档默认 **Q2** 路径，对话默认 **Q3** 标签。
- 共享资料只按固定版本和哈希引用；内容须用户确认才可成事实或证据。
- 本区不把人类 UI / VP-003、DB 存储波次或废除 File 通道作为成功条件。
- 协议内容问题驱动演进主波次仍在 workspace-002 / VP-002；本区 R3 权威路径补丁须遵守 VP-004「R3 协议面变更车辆」。

## 备注

- 开区：用户 2026-08-07 `/govern` 确认新区 slug、Root slug、`delivery` 角色与「激活 VP-004 + scaffold + Root」。
- VP-004 自本区 scaffold 起结束「0 区」；`lead_workspace` 指向本区。
- **关门（2026-08-07）**：R1/R2/R3 全部完成（GOAL-002/003/004 `done`）；Root `GOAL-001-mcp-file-dual-channel-delivery` `done`（关门审计 A-007/A-008）；VP-004 `status: closed`（关门记录已填）。本区冻结，不再新开子目标。
