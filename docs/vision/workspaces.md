---
doc_type: vision-workspace-map
title: 工作区贡献图
status: active
created: 2026-07-28
updated: 2026-07-31
version: 0.4.0
---

# 工作区贡献图

> 只描述角色与意图，**不**复制 goal-tree 的 status/progress，**不**构成第二套生命周期状态。

| workspace_id | role | plan_refs | primary_plan | root_goal | map_status | serves |
|--------------|------|-----------|--------------|-----------|------------|--------|
| workspace-001-goal-governance | primary | VP-001-governance-platform-delivery | VP-001-governance-platform-delivery | GOAL-001-main-vision | **archived** | 奠基 dogfood 封存；Root **done**；服务已关 VP-001；**不**挂 VP-002 演进 |
| workspace-002-（待建） | delivery（预计） | VP-002-methodology-skills-feedback-evolution | VP-002-methodology-skills-feedback-evolution | GOAL-001-（待确认 slug） | planned | 真实项目反馈演进；开区时用户确认 slug 与 Root |

## 规则摘要

- 至多一个 `role: primary`。workspace-001 在 Root 有界 done 后仍保留 **primary** 身份作 monorepo 奠基过程树权威，直至用户书面改 primary 至新区。
- **所有**已存在工作区必须有非空 `plan_refs` 与 `primary_plan`；`role` 仅 `primary` / `delivery`。
- 多区服务同一 VP 时须能指向 **lead**。
- `map_status`：`active` \| `archived` \| 表内 `planned` 仅表示「尚未 scaffold 的预期行」，**不是**磁盘上的工作区。
- **禁止**在 workspace-001 已 done Root 下为 VP-002 开子目标；演进必须新开 `docs/workspace-002-<slug>/`。
