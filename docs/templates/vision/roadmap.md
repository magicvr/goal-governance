---
doc_type: vision-roadmap
title: 愿景规划索引
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
---

# 愿景规划索引（组合编排）

> 复制为 `{governance_root}/vision/roadmap.md`（默认 `docs/vision/roadmap.md`）。
> 本表是愿景级 **组合编排**（VP 波次索引），**不是**目标层「纲领路线图」，也**不是** progress%。
> 每个 VP（**意图**）的权威正文在 `plans/`；**状态与跟踪权威在 VP 文件 frontmatter**（`status` / `vision_ref` / `lead_workspace`）。
> 不在此维护审计意见或 Goal finding；不得把 VP 当目标节点或 `parent`。
> 判定谓词见 `{governance_root}/architecture/principles.md` §6.4。

| id | title | status（派生投影） | vision_ref | lead_workspace | detail |
|----|-------|--------------------|------------|----------------|--------|
| VP-001-example-intent | <意图标题> | planned | vision-example-project@0.1.0 | — | [plans/VP-001-example-intent.md](plans/VP-001-example-intent.md) |

> **`status` 列只是派生投影**：其权威是 `plans/VP-*.md` 的 frontmatter；本列不得用于任何门禁判定，
> 也不得作为第二权威。发现不一致时以 VP 文件为准并刷新本列。若无把握保持同步，可删除本列——
> 文件仍满足完整安装 MUST（该表要求的是文件存在，不是列集合）。

## 波次关系（YYYY-MM-DD）

```text
意图 1 <波次主题> → VP-001 <方向>
意图 2 <波次主题> → VP-002 <方向>
```

只写**先后/并行与 lead 区**，不写 per-VP 状态叙述、关门证据、residual 或 progress%。

## 使用说明

- 新建规划：新增 `plans/VP-NNN-slug.md`，再在本表追加一行。
- 未开工：VP `status: planned`，绑定工作区可为 0。
- `active` 且 0 区：遵守 `{governance_root}/vision/alignment.md` 的空转规则并告警，不静默当健康推进。
- 关门：先在 VP 文件写关门摘要与区证据链接，再刷新本表的投影列（不得反向：不以本表为准改 VP 状态）。
- 迁移：旧表若残留 `workspace_count`、无标注的 `status` 等列，按 legacy 提示处理——不用于门禁，也不因此判「不完整安装」。
