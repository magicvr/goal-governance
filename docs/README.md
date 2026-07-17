---
title: 文档体系说明
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
---

# docs/ · 文档体系

本目录是 **Goal Governance** 的真相来源（source of truth）：目标、决策、执行、审计与架构说明均以 Markdown 维护。

## 目录结构

```text
docs/
├── README.md                 # 本文件：文档架构与使用规范
├── goals/                    # 目标（扁平存放）
│   ├── goal-tree.md          # 树状结构与进展总览（必维护）
│   ├── GOAL-001-main-vision/
│   │   ├── 00-meta.md
│   │   ├── 01-decision.md
│   │   ├── 02-execution.md
│   │   ├── 03-audit.md
│   │   └── attachments/
│   └── GOAL-002-.../
├── architecture/             # 架构与技术约定
│   ├── overview.md
│   └── tech-stack.md
└── _index/                   # 预留：索引、术语等（可扩展）
```

## 核心规则

1. **目标平铺**：所有目标直接放在 `docs/goals/` 下，**禁止**用嵌套文件夹表达层级。
2. **GOAL-001 为总目标**：`GOAL-001-main-vision` 是 Root Goal；`parent` 必须为 `null`。
3. **顺序编号**：新目标从 `GOAL-002` 起递增，不可跳号占用、不可复用已取消编号作新含义（可标注 cancelled）。
4. **层级字段**：父子关系只写在各目标 `00-meta.md` 的 `parent` 中。
5. **总览同步**：任何新建/完成/改 parent/改状态，必须更新 [goals/goal-tree.md](goals/goal-tree.md)。
6. **标准五件套**：每个目标文件夹必须包含：
   - `00-meta.md` — 元信息与概述
   - `01-decision.md` — 决策（写清「为什么」）
   - `02-execution.md` — 执行（时间线、事实）
   - `03-audit.md` — 审计/复盘
   - `attachments/` — 附件（可为空，保留目录）

## Frontmatter 约定

每个文档建议至少包含：

```yaml
---
status: active          # draft | active | blocked | done | cancelled
created: YYYY-MM-DD
updated: YYYY-MM-DD
parent: null            # 或父目标 ID，如 GOAL-001-main-vision
version: 0.1.0
---
```

目标类文件另含 `id`；决策/执行/审计可用 `doc: decision|execution|audit`。

## 如何新增目标

1. 查看 [goals/goal-tree.md](goals/goal-tree.md) 确定下一个编号。
2. 在 `docs/goals/` 创建 `GOAL-NNN-short-slug/`。
3. 写入五件套，并设置正确的 `parent`。
4. 更新 `goal-tree.md` 的树与表格。
5. 如影响架构，同步更新 `architecture/`。

## 与 Web / Skills 的关系

| 形态 | 职责 | 路径 |
|------|------|------|
| 文档（本目录） | 目标与过程的权威记录 | `docs/` |
| Web 应用 | 浏览与操作（当前为骨架） | `web/` |
| Skills / 提示词 | AI 按规则读写与推进目标 | 根目录 `AGENTS.md` 等 |

## 推荐阅读顺序

1. [goals/goal-tree.md](goals/goal-tree.md) — 全局进展  
2. [goals/GOAL-001-main-vision/00-meta.md](goals/GOAL-001-main-vision/00-meta.md) — 总目标  
3. [architecture/overview.md](architecture/overview.md) — 架构概览  
4. 仓库根 [AGENTS.md](../AGENTS.md) — AI 协作强制规则  
