---
doc_type: vision-workspace-map
title: 工作区贡献图
status: active
created: 2026-07-28
updated: 2026-07-28
version: 0.1.0
---

# 工作区贡献图

> 只描述角色与意图，**不**复制 goal-tree 的 status/progress，**不**构成第二套生命周期状态。

| workspace_id | role | plan_refs | primary_plan | root_goal | map_status | serves |
|--------------|------|-----------|--------------|-----------|------------|--------|
| workspace-001-goal-governance | primary | VP-001-governance-platform-delivery | VP-001-governance-platform-delivery | GOAL-001-main-vision | active | 承载平台 dogfood 过程树与 Root 可执行路线图；推进 VP-001 |

## 规则摘要

- 至多一个 `role: primary`；primary **禁止** 无规划 opt-out。
- `sandbox` 可在 alignment 规则下 `plan_refs` 为空并留痕。
- `map_status` 仅为贡献图用（`active` \| `archived`），不是目标 progress。
