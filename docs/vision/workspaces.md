---
doc_type: vision-workspace-map
title: 工作区贡献图
status: active
created: 2026-07-28
updated: 2026-07-31
version: 0.3.0
---

# 工作区贡献图

> 只描述角色与意图，**不**复制 goal-tree 的 status/progress，**不**构成第二套生命周期状态。

| workspace_id | role | plan_refs | primary_plan | root_goal | map_status | serves |
|--------------|------|-----------|--------------|-----------|------------|--------|
| workspace-001-goal-governance | primary | VP-001-governance-platform-delivery | VP-001-governance-platform-delivery | GOAL-001-main-vision | active | Primary dogfood；服务 Charter `vision-goal-governance@0.2.0` 与 VP-001（协议 + Skills；本仓 Web 冻结参考） |

## 规则摘要

- 至多一个 `role: primary`。
- **所有**工作区必须有非空 `plan_refs` 与 `primary_plan`；`role` 仅允许 `primary` / `delivery`，无 plan opt-out（alignment 0.5 / P-006）。
- 多区服务同一 VP 时贡献图与 VP 正文应能指向 **lead** 工作区。
- `map_status` 仅为贡献图用（`active` \| `archived`），不是目标 progress。
