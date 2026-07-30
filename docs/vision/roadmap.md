---
doc_type: vision-roadmap
title: 愿景规划索引
status: active
created: 2026-07-28
updated: 2026-07-31
version: 0.3.0
---

# 愿景规划索引（组合编排）

本表是愿景级 **组合编排**（VP 波次索引），**不是**目标层「纲领路线图」，也**不是** progress%。  
每个 VP（**意图**）的权威正文在 [plans/](plans/)。不在此维护审计意见或 Goal finding。

| id | title | status | vision_ref | lead_workspace | workspace_count | detail |
|----|-------|--------|------------|----------------|-----------------|--------|
| VP-001-governance-platform-delivery | 治理协议与 Skills 可复用交付（奠基 · 有界关） | **closed** | vision-goal-governance@0.2.0 | workspace-001-goal-governance | 1 | [plans/VP-001-governance-platform-delivery.md](plans/VP-001-governance-platform-delivery.md) |
| VP-002-methodology-skills-feedback-evolution | 真实项目反馈驱动的协议与 Skills 演进 | **active** | vision-goal-governance@0.2.0 | —（待 workspace-002） | 0 | [plans/VP-002-methodology-skills-feedback-evolution.md](plans/VP-002-methodology-skills-feedback-evolution.md) |
| VP-003-human-ui-workbench-deferred | 人类 UI / Web 工作台（延期 · 待通用基架） | **planned** | vision-goal-governance@0.2.0 | — | 0 | [plans/VP-003-human-ui-workbench-deferred.md](plans/VP-003-human-ui-workbench-deferred.md) |

## 波次关系（2026-07-31）

```text
意图 1 奠基  → VP-001 closed（workspace-001 Root 有界 done）
意图 2 演进  → VP-002 active（空转至开 workspace-002；复核 ≤2026-08-14）
意图 3 人类 UI → VP-003 planned（冻结；H-WEB-01）
```

## 使用说明

- 新建规划：新增 `plans/VP-NNN-slug.md`，并在本表追加一行。
- 未开工：`status: planned`，绑定工作区可为 0。
- `active` 且 0 区：须遵守 alignment **空转 14 日**规则（见 VP-002 正文）。
- 关门：在 VP 文件写关门摘要与区证据链接，再更新本表 `status`。
