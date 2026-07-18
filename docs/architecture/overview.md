---
title: 架构概览
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.2.0
---

# 架构概览

## 目标

用「核心协议为规范、目标文档为真相、Skills 与 Web 为消费适配器」的方式，支撑目标治理闭环：

```text
目标 (Goal)
  ├── 决策 (Decision)
  ├── 执行 (Execution)
  └── 审计 (Audit)
```

## 逻辑架构

```text
┌──────────────────────────────────────────────────────┐
│ 核心方法论与文档协议                                  │
│ docs/README.md + docs/architecture/ + docs/templates/ │
└───────────────────────┬──────────────────────────────┘
                        │ 规范结构与生命周期
             ┌──────────┴──────────┐
             ▼                     ▼
   ┌──────────────────┐  ┌──────────────────┐
   │ Skills / 提示词   │  │ Web 人类工作台    │
   │ AI/Agent 适配器   │  │ 当前只读/诊断     │
   └─────────┬────────┘  └─────────┬────────┘
             │ 读写                 │ 读取
             └──────────┬───────────┘
                        ▼
             ┌──────────────────────┐
             │ docs/goals/ 目标实例  │  ← runtime source of truth
             │ goal-tree.md          │
             └──────────────────────┘
```

## 仓库布局

| 路径 | 职责 |
|------|------|
| `docs/goals/` | 目标与过程记录（扁平） |
| `docs/templates/` | 核心 canonical 文档模板 |
| `docs/architecture/` | 技术与架构约定、[治理原则](principles.md) |
| `docs/_index/` | 预留索引/术语 |
| `skills/` | AI/Agent 消费适配器、安装包与模板分发镜像 |
| `web/` | FastAPI Web 应用 |
| `AGENTS.md` | AI 强制规则 |

## 当前阶段（v0）

- GOAL-001 已通过 D-007 重基线为“三层交付、一个真相源”；核心 canonical 模板位于 `docs/templates/goal-folder/`。
- 文档体系规则与 GOAL-002/003/004/005 已建立；GOAL-003/005 已交付 Skills 的**单一编排主入口**（`/govern`）、交叉入口（`/audit`）、原语与多宿主安装基线。
- 治理原则 [principles.md](principles.md) 已含 P-001～P-004；`skills/templates/goal-folder/` 作为核心模板的离线分发镜像继续随包安装。
- GOAL-004 阶段 A～D 已完成：领域模型、读取服务、可恢复 Create/Update 服务与只读 Web 接入见 [domain-model-and-storage.md](../goals/GOAL-004-core-data-model/attachments/domain-model-and-storage.md)。
- Web 首页和 `/goals/{goal_id}` 已通过 `GoalsRepository` 读取 Markdown 真相源，展示目标、详情与 tree/document 诊断；UI 写入不在当前 Web 交付边界。

## 演进方向（未实现，仅规划）

1. 核心方法论、文档协议和 canonical 模板的独立产品化与版本化（GOAL-001 阶段 4）。
2. Skills 对核心协议、模板镜像和安装产物的一致性验收（阶段 5）。
3. Web 继续以只读浏览与诊断为第一阶段；任何写入能力另立目标并遵守相同事务与审计约束（阶段 6）。
4. 三个交付面的兼容性、漂移检测与发布验收（阶段 7）。

细节技术选型见 [tech-stack.md](tech-stack.md)。
