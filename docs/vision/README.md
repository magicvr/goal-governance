---
doc_type: vision-index
title: 愿景体系入口
status: active
created: 2026-07-28
updated: 2026-07-29
version: 0.4.0
---

# 愿景体系 · `docs/vision/`

本目录是本仓库**唯一**的仓库级愿景体系根（**单愿景制**）。它表达可演进的纲领（Charter）与可关门的意图（VP），**不是**目标五件套，也**不是**第二套 goal-tree 或 progress 权威。

元原则：**P-006**（[principles.md](../architecture/principles.md)）；规则权威：[alignment.md](alignment.md)。

## 硬边界

1. **每项目有且仅有一个**现行 Charter（`active`）；禁止多愿景。换代用 `superseded`。
2. Charter **不可**使用 Goal 生命周期的 `done`。
3. 目标生命周期状态、进度与 Goal 审计台账只存在于各 `docs/workspace-*/` 根内。
4. 愿景文档不汇总各区 progress%，不关闭 Goal finding。
5. 完整安装**必含**本目录最小文件集（**MUST** 权威表：[alignment.md §0.2](alignment.md#02-完整安装与冷启动)）；缺 Charter 或缺任一愿景树 MUST 文件 = 不完整安装（仅引导补齐）。
6. 所有工作区必须挂 VP；`vision_role` 仅允许 `primary` / `delivery`，无 plan opt-out。

## 文件地图

| 文件 | 职责 |
|------|------|
| [charter.md](charter.md) | 现行愿景正文（目的、边界、非目标） |
| [roadmap.md](roadmap.md) | **组合编排**索引（VP 波次，非 progress%） |
| [plans/](plans/) | 单个 `VP-*.md` **意图**权威正文 |
| [revisions.md](revisions.md) | Charter 修订时间线（`VR-`） |
| [reviews.md](reviews.md) | **Vision Review** 台账（`VRev-00N`） |
| [workspaces.md](workspaces.md) | 工作区贡献图（角色与意图，非进度） |
| [alignment.md](alignment.md) | 对齐契约与门禁（规则权威） |
| [consumer-checklist.md](consumer-checklist.md) | Skills / Web / 编排器检查映射 |

## 推荐读序

1. **日常推进**：`charter.md` → 当前工作区 `primary_plan` 对应的 `plans/VP-*.md` → [alignment.md](alignment.md) 门禁。
2. **冷启动 / 建区**：Charter（最小完备）→ 首个 VP → 再写工作区 `plan_refs` / `primary_plan` 与 Root。
3. **修订愿景**：改 charter → [revisions.md](revisions.md) → Vision Review（strategic）→ 更新受影响 VP `vision_ref` → 工作区 re-align（宽阻断见 alignment）。

## 对齐递归（摘要）

```text
Charter (唯一源头)
    ↑
Vision Plan VP-NNN-slug（意图）
    ↑
Workspace / Root (plan_refs + primary_plan)
    ↑
子目标 (parent)
```

细则见 [alignment.md](alignment.md)。
