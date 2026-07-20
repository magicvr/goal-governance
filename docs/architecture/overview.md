---
title: 架构概览
status: active
created: 2026-07-18
updated: 2026-07-20
parent: null
version: 0.6.0
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
│ docs/README.md + docs/architecture/ + docs/templates/ + docs/contracts/ │
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
             │ workspace-<NNN>-slug/ │  ← workspace runtime source of truth
             │ workspace.md + goal-tree.md │
             └──────────────────────┘

`workspace-<NNN>-slug/workspace.md` 绑定当前工作区的 Root Goal、canonical 范围和共享资料固定引用；它不保存目标生命周期状态，也不替代上图中的真相源。
```

## 仓库布局

| 路径 | 职责 |
|------|------|
| `docs/workspace-<NNN>-<slug>/` | 当前工作区的目标与过程记录（扁平） |
| `docs/workspace-<NNN>-<slug>/workspace.md` | 显式工作区绑定与共享资料固定引用；不保存目标状态 |
| `docs/shared-materials/` | 工作区外的共享资料候选库存；不保存目标状态 |
| `docs/templates/` | 核心 canonical 文档模板 |
| `docs/contracts/` | 消费适配器的 canonical 机读版本与兼容声明 |
| `docs/architecture/` | 技术与架构约定、[治理原则](principles.md) |
| `docs/_index/` | 预留索引/术语 |
| `skills/` | AI/Agent 消费适配器、安装包与模板/契约分发镜像 |
| `web/` | FastAPI Web 应用 |
| `AGENTS.md` | AI 强制规则 |

## 当前阶段（v0）

- GOAL-001 已通过 D-007 重基线为“三层交付、一个真相源”；核心 canonical 模板位于 `docs/templates/goal-folder/`。
- 文档体系规则与 GOAL-002/003/004/005 已建立；GOAL-003/005 已交付 Skills 的**单一编排主入口**（`/govern`）、交叉入口（`/audit`）、原语与多宿主安装基线。
- 治理原则 [principles.md](principles.md) 已含 P-001～P-005；P-005 允许带未知立项，并通过信息需求与阶段门禁避免把未知伪装成已知；`skills/templates/goal-folder/` 与 `skills/contracts/` 分别作为核心模板和消费适配器契约的离线分发镜像继续随包安装。
- GOAL-008 的 I-001 已交付 `docs/contracts/` canonical schema/manifest 与 `skills/contracts/` 镜像；实际宿主/版本支持矩阵仍由 I-002 按门禁推进。
- GOAL-010 正把工作区 Root Goal 绑定、串行阶段与共享资料固定引用纳入 core 协议，并先由 Skills 适配；它不放行 GOAL-009 的 Web 产品、存储或受控写入门禁。
- GOAL-004 阶段 A～D 已完成：领域模型、读取服务、可恢复 Create/Update 服务与只读 Web 接入见 [domain-model-and-storage.md](../workspace-001-goal-governance/GOAL-004-core-data-model/attachments/domain-model-and-storage.md)。
- Web 首页和 `/goals/{goal_id}` 已通过 `GoalsRepository` 读取 Markdown 真相源，展示目标、详情与 tree/document 诊断；UI 写入不在当前 Web 交付边界。

## 演进方向（未实现，仅规划）

1. 工作区与共享资料固定引用协议（GOAL-010）：先形成 core/Skills 共用边界，再由产品适配器验证运行时模型。
2. Web 继续以人机协作工作台的产品发现为当前阶段；任何读模型、资料访问或写入能力另立目标并遵守相同事务与审计约束（阶段 6）。
3. 三个交付面的兼容性、漂移检测与发布验收（阶段 7）。

细节技术选型见 [tech-stack.md](tech-stack.md)。
