---
doc_type: vision-roadmap
title: 愿景规划索引
status: active
created: 2026-07-28
updated: 2026-09-13
version: 0.8.0
---

# 愿景规划索引（组合编排）

本表是愿景级 **组合编排**（VP 波次索引），**不是**目标层「纲领路线图」，也**不是** progress%。  
每个 VP（**意图**）的权威正文在 [plans/](plans/)。不在此维护审计意见或 Goal finding。

**权威与投影（D-005 / alignment §0.3）**：VP 的 `status` / `vision_ref` / `lead_workspace` 权威在**该 VP 文件的 frontmatter**；下表对应列是**派生投影**——只供阅读，**不得用于任何门禁判定**（新建区、放行、VP 关门、发布）。不一致时以 VP 文件为准并刷新本表。遗留行/列（其他版本写入的）同样只作 legacy 提示，既不阻断推进，也不单独判「不完整安装」。

| id | title | status（派生投影） | vision_ref | lead_workspace | workspace_count | detail |
|----|-------|--------------------|------------|----------------|-----------------|--------|
| VP-001-governance-platform-delivery | 治理协议与 Skills 可复用交付（奠基 · 有界关） | **closed** | vision-goal-governance@0.2.0 | workspace-001-goal-governance | 1 | [plans/VP-001-governance-platform-delivery.md](plans/VP-001-governance-platform-delivery.md) |
| VP-002-methodology-skills-feedback-evolution | 真实项目反馈驱动的协议与 Skills 演进 | **active** | vision-goal-governance@0.2.0 | workspace-002-methodology-skills-feedback | 1 | [plans/VP-002-methodology-skills-feedback-evolution.md](plans/VP-002-methodology-skills-feedback-evolution.md) |
| VP-003-human-ui-workbench-deferred | 人类 UI / Web 工作台（挂起 · 待通用基架） | **planned** | vision-goal-governance@0.2.0 | — | 0 | [plans/VP-003-human-ui-workbench-deferred.md](plans/VP-003-human-ui-workbench-deferred.md) |
| VP-004-mcp-file-dual-channel-delivery | 消费交付双通道（MCP + File）与可配置治理根 | **closed** | vision-goal-governance@0.2.0 | workspace-003-mcp-file-dual-channel | 1 | [plans/VP-004-mcp-file-dual-channel-delivery.md](plans/VP-004-mcp-file-dual-channel-delivery.md) |

## 波次关系（2026-08-07）

```text
意图 1 奠基     → VP-001 closed（workspace-001 Root 有界 done）
意图 2 演进     → VP-002 active（lead = workspace-002-methodology-skills-feedback；空转已结束）
意图 3 人类 UI  → VP-003 planned（正式挂起；冻结资产退役；H-WEB-01）
意图 4 交付通道 → VP-004 closed（2026-08-07 复关；workspace-003-mcp-file-dual-channel 交付完成）
```

## 使用说明

- 新建规划：新增 `plans/VP-NNN-slug.md`，并在本表追加一行。
- 未开工：`status: planned`，绑定工作区可为 0。
- `active` 且 0 区：须遵守 alignment **空转 14 日**规则（见 VP-002 正文）。
- 关门：**先在 VP 文件写关门摘要与区证据链接并改其 frontmatter `status`**，再刷新本表投影列。顺序不可反：本表不是状态源。
- 列的去留：`workspace_count` 等自定义列可保留或删除；`status` 列若同步困难可删除，文件仍满足 MUST（该表只要求**文件存在**）。
