---
title: 架构概览
status: active
created: 2026-07-18
updated: 2026-07-28
parent: null
version: 0.7.0
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
┌──────────────────────────────────────────────────────────────┐
│ 核心方法论与文档协议                                           │
│ docs/README + architecture/ + templates/ + contracts/ + vision/ │
└──────────────────────────┬───────────────────────────────────┘
                           │ 规范结构与生命周期
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │ Skills / 提示词   │      │ Web 人类工作台    │
    │ AI/Agent 适配器   │      │ 有界受控写入      │
    └────────┬─────────┘      └────────┬─────────┘
             │ 读写                      │ 读 + 门禁后写
             └────────────┬─────────────┘
                          ▼
             ┌──────────────────────────┐
             │ workspace-<NNN>-slug/     │  ← 运行时目标真相源
             │ workspace.md + goal-tree │
             │ + 平铺 GOAL-* 五件套      │
             └──────────────────────────┘
```

`workspace.md` 绑定 Root Goal、canonical 范围、共享资料目录指针与（若有 vision）`plan_refs`/`primary_plan`；**不**保存目标生命周期状态。愿景目录 `docs/vision/` 对齐 Charter→VP，**不是** progress 或审计台账。

## 仓库布局

| 路径 | 职责 |
|------|------|
| `docs/workspace-<NNN>-<slug>/` | 当前工作区的目标与过程记录（扁平） |
| `docs/workspace-<NNN>-<slug>/workspace.md` | 显式工作区绑定与共享资料固定引用；不保存目标状态 |
| `docs/vision/` | Charter、VP、对齐契约；非 goal-tree |
| `docs/shared-materials/` | 工作区外的共享资料候选库存；不保存目标状态 |
| `docs/templates/` | 核心 canonical 文档模板 |
| `docs/contracts/` | 消费适配器的 canonical 机读版本与兼容声明 |
| `docs/architecture/` | 技术与架构约定、[治理原则](principles.md)、[工作区协议](workspace-protocol.md) |
| `docs/_index/` | 预留索引/术语 |
| `skills/` | AI/Agent 消费适配器、安装包与模板/契约分发镜像 |
| `web/` | FastAPI Web 应用（有界受控写入，默认门闩关闭） |
| `AGENTS.md` | AI 强制规则 |

## 当前阶段（现时）

- **真相源**：显式工作区 `docs/workspace-001-goal-governance/`（GOAL-011 已完成自 `docs/goals/` 迁移）；legacy 隐式单工作区仅兼容外部旧仓。
- **原则**：[principles.md](principles.md) P-001～P-005（含 finding 三路径闭合、P-004.1～4.4）；工作区/资料/愿景见 [workspace-protocol.md](workspace-protocol.md) 与 [../vision/alignment.md](../vision/alignment.md)。
- **Skills**：`/govern` 主入口、`/audit` 交叉入口、多宿主安装与契约镜像；发布一致性以 GOAL-008 惯例与 runtime evidence 为准。
- **Web**：阶段 6 **有界结项**（GOAL-009 及 012～017）；主路径可读 + 受控写（双门闩，见 `web/README.md`）。扩展能力挂 residual **R-009-X**，不假装产品终态。
- **Root**：`GOAL-001-main-vision` 保持 `active`，对齐 `VP-001-governance-platform-delivery` / `vision-goal-governance@0.1.0`。

细节以工作区 `goal-tree.md` 与各目标五件套为准；本页若与之冲突，以工作区记录为准。

## 演进方向（未实现或 residual，仅规划）

1. 多工作区 N1 导航、资料 CRUD 产品、AI 读资料全文等（R-009-X 与后续目标）。
2. 三交付面持续兼容性、漂移检测与发布验收加固。
3. 消费适配器对 finding residual / user-overruled 的机读字段（若产品需要）。

细节技术选型见 [tech-stack.md](tech-stack.md)。
