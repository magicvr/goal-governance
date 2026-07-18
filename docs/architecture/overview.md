---
title: 架构概览
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.1.4
---

# 架构概览

## 目标

用「文档为源、应用为窗、Skills 为助手」的方式，支撑目标治理闭环：

```text
目标 (Goal)
  ├── 决策 (Decision)
  ├── 执行 (Execution)
  └── 审计 (Audit)
```

## 逻辑架构

```text
┌─────────────────────────────────────────────┐
│                 协作者 / AI                  │
└─────────────┬───────────────┬───────────────┘
              │               │
              ▼               ▼
     ┌────────────────┐  ┌────────────────┐
     │  Skills/提示词  │  │   Web 应用      │
     │  AGENTS.md 等  │  │   web/         │
     └────────┬───────┘  └────────┬───────┘
              │                   │
              └─────────┬─────────┘
                        ▼
              ┌────────────────────┐
              │  docs/goals 等文档  │  ← source of truth
              │  goal-tree.md      │
              └────────────────────┘
```

## 仓库布局

| 路径 | 职责 |
|------|------|
| `docs/goals/` | 目标与过程记录（扁平） |
| `docs/architecture/` | 技术与架构约定、[治理原则](principles.md) |
| `docs/_index/` | 预留索引/术语 |
| `web/` | FastAPI Web 应用 |
| `AGENTS.md` | AI 强制规则 |

## 当前阶段（v0）

- 文档体系规则与 GOAL-002/003/004/005 已建立；GOAL-003 Skills 以**单一编排主入口**（`00-govern-orchestrator` / `/govern`）+ 文档原语交付。
- 治理原则 [principles.md](principles.md) 已含 P-001～P-004（闭环、交叉审计、用户裁决）；GOAL-005 已完成编排门禁、`/audit` 交叉入口与关门确认。
- GOAL-004 阶段 A～D 已完成：领域模型、读取服务、可恢复 Create/Update 与只读 Web 接入见 [domain-model-and-storage.md](../goals/GOAL-004-core-data-model/attachments/domain-model-and-storage.md)。
- Web 首页和 `/goals/{goal_id}` 已通过 `GoalsRepository` 读取 Markdown 真相源，展示目标、详情与 tree/document 诊断；写入交互仍待后续阶段。

## 演进方向（未实现，仅规划）

1. Web 写入交互与文档体系联动（承接 GOAL-001 阶段 4）。
2. 校验工具：编号、parent、goal-tree 一致性。
3. Skills：GOAL-005 阶段 B 已落地编排门禁、`/audit` 交叉入口与 01～05 提示词；阶段 D 可再压测后关门。

细节技术选型见 [tech-stack.md](tech-stack.md)。
