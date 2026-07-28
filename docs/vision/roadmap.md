---
doc_type: vision-roadmap
title: 愿景规划索引
status: active
created: 2026-07-28
updated: 2026-07-28
version: 0.1.0
---

# 愿景规划索引（Roadmap）

本表是纲领规划的**索引**；每个 VP 的权威正文在 [plans/](plans/)。  
不在此维护 progress% 或审计意见。

| id | title | status | vision_ref | lead_workspace | workspace_count | detail |
|----|-------|--------|------------|----------------|-----------------|--------|
| VP-001-governance-platform-delivery | 治理平台可复用交付（方法论 · Skills · Web） | active | vision-goal-governance@0.1.0 | workspace-001-goal-governance | 1 | [plans/VP-001-governance-platform-delivery.md](plans/VP-001-governance-platform-delivery.md) |

## 使用说明

- 新建规划：新增 `plans/VP-NNN-slug.md`，并在本表追加一行。
- 未开工：`status: planned`，绑定工作区可为 0（`workspace_count: 0`）。
- 多区并行：同一 VP 可挂多个工作区；推荐填写 `lead_workspace`。
- 关门：在 VP 文件写关门摘要与区证据链接，再更新本表 `status`。
