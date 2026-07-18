---
title: 架构概览
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.1
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

- 文档体系规则与 GOAL-002/003/004 已建立；GOAL-003 Skills 以**单一编排主入口**（`00-govern-orchestrator` / `/govern`）+ 文档原语交付。
- Web 仅有模块路由与页面骨架，**未**连接文件系统/数据库读写目标。

## 演进方向（未实现，仅规划）

1. Web 读取/展示 `docs/goals`（或未来结构化存储）。
2. 校验工具：编号、parent、goal-tree 一致性。
3. Skills 编排质量与多宿主安装体验持续打磨。

细节技术选型见 [tech-stack.md](tech-stack.md)。
