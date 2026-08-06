---
id: D-001
goal_id: GOAL-001-mcp-file-dual-channel-delivery
title: 开区 workspace-003 + Root 服务 VP-004
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-001 · 开区 workspace-003 + Root 服务 VP-004（2026-08-07）

**状态**：accepted
**触发**：用户 `/govern 激活 VP-004 并挂`；结构选型确认「新区 + 激活 + scaffold + Root」

## 决定

1. Scaffold **`docs/workspace-003-mcp-file-dual-channel/`** 为 VP-004 主交付区（`lead`）。
2. Root = **`GOAL-001-mcp-file-dual-channel-delivery`**，`parent: null`，`primary_plan` = `VP-004-mcp-file-dual-channel-delivery`。
3. `vision_role` = **`delivery`**；**不**改 Charter `primary_workspace`；workspace-001 仍 monorepo **primary**；workspace-002 仍服务 VP-002。
4. 将 **VP-004** 从 `planned` 标为 **`active`**；`lead_workspace` = 本区；结束 0 区状态（直接挂区，空转不适用）。
5. Root 写入纲领 **R1→R2→R3**（对齐 VP-004）；本回合**不**创建子目标（下一步再立 R1 首刀）。
6. 沿用 VRev-007 已闭合结论：R3 协议车辆、P0/P1、Charter 叙事选择、入口等价检查点以 VP-004 v0.1.1 为准。

## 为什么

- VP-004 为独立交付波次（双通道 + governance_root），与 VP-002「协议内容反馈演进」可并行；独立 goal-tree 避免混树。
- workspace-001 Root 已 done，禁止在其下硬塞。
- 用户书面确认 workspace slug、一并激活 + scaffold + Root（推荐默认）。

## 未选方案

- **挂 workspace-002 作 support / 改其 primary_plan**：会搅混 VP-002 lead 语义与目标树边界。
- **只激活 VP-004 不挂区**：触发 14 日空转；用户明确要求 scaffold。
- **改 primary 到 003**：用户未要求；001 仍保留 monorepo primary 身份。
