---
doc_type: vision-charter
vision_id: vision-goal-governance
title: Goal Governance 仓库愿景
status: active
version: 0.1.0
effective_date: 2026-07-28
primary_workspace: workspace-001-goal-governance
created: 2026-07-28
updated: 2026-07-28
---

# Charter · Goal Governance

## 目的陈述

建立一套**可复用、可审计**的目标治理方法论与文档协议，把「目标 → 决策 → 执行 → 审计」固化为可追踪、可复盘、可协作的工作流；并提供两类消费适配器——面向 AI / Git 仓库协作的 **Skills**，以及面向人的 **Web 工作台**——使同一协议可在文档-only、Agent 与人机界面中一致使用。

核心方法论与 canonical 模板必须能够**脱离**特定 AI 宿主和 Web 独立使用；具体项目的目标实例与过程事实只保存在已验证的工作区根内，作为运行时唯一目标状态真相源。

## 方向级成功边界

在本愿景仍为 `active` 的前提下，下列方向成立即视为仍在愿景内（**不是**可关门的验收 checklist）：

1. **协议可复制**：生命周期、P-001～P-005、五件套与工作区/共享资料边界有可独立启用的文档与模板。
2. **消费一致**：Skills 与 Web（及后续适配器）消费同一核心协议，不另立第二套目标状态。
3. **可审计闭环**：决策、执行事实与审计意见可落盘、可交叉审、可门禁；独立审计默认不直接改 status。
4. **工作区隔离**：多工作区时目标/候选/AI 上下文不混合；跨区默认 fail closed。
5. **愿景可对齐**：进行中与将开启的工作通过愿景规划（VP）挂接本 Charter，避免各区 Root 各自漂移。

## 非目标

本 Charter **不**要求、也**不**把下列事项写成愿景成功条件：

- 把 Web 建成「完善的只读浏览器」或与文档协议无关的独立状态库。
- 在愿景层维护 goal-tree、progress% 或审计台账。
- 一次穷尽所有未来产品阶段或客户场景。
- 自动裁决 P-004、静默关闭 required finding，或无人确认的跨区写入。
- 将共享资料正文直接当作已确认事实或关闭证据。

## 原则摘要

操作原则以 [docs/architecture/principles.md](../architecture/principles.md) 为准（P-001～P-005）。与本 Charter 直接相关的要点：

- 大范围先路线图再立项（P-001）；可执行细节在工作区 Root / 子目标，不在本文件堆进度。
- 事实与审计可指回证据（P-002 / P-003）；愿景规划关门只做纲领确认并链接区证据。
- 冲突与是否自审问用户（P-004）；信息门禁不可用「以后再说」绕过（P-005）。

## 与 Root Goal 的关系

- **本 Charter** 是仓库级北极星：演进、不可 `done`。
- **工作区 Root Goal**（如 `GOAL-001-main-vision`）是某一治理上下文中的最高**可治理**目标：可有区内路线图、子目标与审计闭环，并可长期 `active`。
- Root **通过愿景规划（VP）** 对齐本 Charter，而不是把本文件当作又一个 `GOAL-*`。
- 区内可执行阶段展开仍写在 Root `00-meta` / 决策中；纲领阶段与跨区编排写在 [roadmap.md](roadmap.md) 与 [plans/](plans/)。

## 现行版本

| 项 | 值 |
|----|-----|
| `vision_id` | `vision-goal-governance` |
| 版本 | `0.1.0` |
| 生效日 | 2026-07-28 |
| 状态 | `active` |
| Primary 工作区 | `workspace-001-goal-governance` |

修订史见 [revisions.md](revisions.md)。引用格式：`vision-goal-governance@0.1.0`。
