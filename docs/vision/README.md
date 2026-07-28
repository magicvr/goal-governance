---
doc_type: vision-index
title: 愿景体系入口
status: active
created: 2026-07-28
updated: 2026-07-28
version: 0.1.0
---

# 愿景体系 · `docs/vision/`

本目录是本仓库**唯一**的仓库级愿景体系根。它表达可演进的纲领（Charter）与可关门的愿景规划（VP），**不是**目标五件套，也**不是**第二套 goal-tree 或 progress 权威。

## 硬边界

1. Charter **不可**使用 Goal 生命周期的 `done`；仅 `active` 或整体 `superseded`。
2. 目标生命周期状态、进度与审计台账只存在于各 `docs/workspace-*/` 根内。
3. 愿景文档不汇总各区 progress%，不关闭 finding，不替代 `03-audit.md`。

## 文件地图

| 文件 | 职责 |
|------|------|
| [charter.md](charter.md) | 现行愿景正文（目的、边界、非目标） |
| [roadmap.md](roadmap.md) | 规划索引表 |
| [plans/](plans/) | 单个 `VP-*.md` 规划权威正文 |
| [revisions.md](revisions.md) | Charter 修订时间线 |
| [workspaces.md](workspaces.md) | 工作区贡献图（角色与意图，非进度） |
| [alignment.md](alignment.md) | 三层对齐契约与门禁（规则权威） |
| [consumer-checklist.md](consumer-checklist.md) | Skills / Web / 编排器检查映射 |

## 推荐读序

1. **日常推进**：`charter.md`（方向）→ 当前工作区 `primary_plan` 对应的 `plans/VP-*.md` → [alignment.md](alignment.md) 门禁。
2. **建区 / 新建 Root**：先读 alignment 与 roadmap，再写 `plan_refs` / `primary_plan`。
3. **修订愿景**：改 charter → 追加 [revisions.md](revisions.md) → 更新受影响 VP 的 `vision_ref` → 工作区 re-align。

## 三层对齐链

```text
Charter (vision_id@version)
    ↑
Vision Plan VP-NNN-slug
    ↑
Workspace / Root (plan_refs + primary_plan)
```

细则见 [alignment.md](alignment.md)。
