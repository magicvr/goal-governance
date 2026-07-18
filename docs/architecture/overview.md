---
title: 架构概览
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.2
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
- 治理原则 [principles.md](principles.md) 已含 P-001～P-004（闭环、交叉审计、用户裁决）；GOAL-005 阶段 A 完成，阶段 B 起改提示词。
- GOAL-004 阶段 A 已完成：领域模型与存储约定见 [domain-model-and-storage.md](../goals/GOAL-004-core-data-model/attachments/domain-model-and-storage.md)。
- Web 仅有模块路由与页面骨架，**未**连接文件系统读写目标（阶段 B 起实现）。

## 演进方向（未实现，仅规划）

1. Web 读取/展示 `docs/goals`（GOAL-004 B–D；模型见上附设计）。
2. 校验工具：编号、parent、goal-tree 一致性。
3. Skills：GOAL-005 编排门禁/交叉审计提示词与 `/audit` 入口落地。

细节技术选型见 [tech-stack.md](tech-stack.md)。
