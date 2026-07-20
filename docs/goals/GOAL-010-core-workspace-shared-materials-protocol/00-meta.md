---
id: GOAL-010-core-workspace-shared-materials-protocol
title: 建立工作区与共享资料区核心协议，并完成 Skills 首先适配
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-20
version: 0.2.0
progress: 100%
---

# GOAL-010 · 建立工作区与共享资料区核心协议，并完成 Skills 首先适配

## 2026-07-20 · 关门结论

[D-002](01-decision.md) 已将 I-001～I-004 的验证结论、GOAL-009 交接范围和非目标边界留痕。canonical 协议、可复制模板、Skills 消费规则、宿主安装面与语义测试均已形成并通过复现；GOAL-010 以 `done / 100%` 关门。I-005 仍是 `non-blocking / open` 的下游产品实现问题，不是本目标已经实现或放行的能力。

## 概述

将“工作区”和“共享资料区”从 GOAL-009 的产品发现输入提升为可脱离 Web 使用的核心文档协议，并先由 Skills 消费该协议。一个工作区绑定一个独立 Root Goal 与 canonical 范围；同一项目的 MVP、后续阶段和扩展工作以该 Root Goal 的路线图与串行子目标承接，而非反复改写 Root Goal 或在立项时伪造完整远期计划。

共享资料区在本目标中定义为跨工作区可引用的资料边界：工作区只记录固定版本的引用、注释和派生记录，不以它读取、推理混合或写入其他工作区的目标状态。本目标只定义文档语义、引用约束和 Skills 行为，不实现共享资料物理存储、用户 CRUD、Web 页面、AI 服务或跨工作区运行时注册表。

## 成功标准

- [x] canonical 层明确工作区、Root Goal、串行阶段子目标和 canonical 范围的关系，并说明何时更新路线图、何时才应修改 Root Goal 本身。
- [x] 提供可独立复制的工作区上下文模板，定义 Root Goal 绑定、canonical 范围、共享资料目录指针及固定资料引用的最小字段。
- [x] canonical 层定义共享资料引用的版本、哈希、来源、适用工作区、注释/派生与拒绝条件；不把共享资料区变成第二套目标状态。
- [x] `/govern`、原语和 `/audit` 的 Skills 行为能识别工作区上下文、保留 legacy 单工作区兼容、拒绝跨工作区上下文混合，并把未确认资料内容与 canonical 事实区分开。
- [x] canonical 与 Skills 镜像、独立启用、安装分发和语义测试均可重复验证；验证结果可回指到本目标执行记录。
- [x] 向 GOAL-009 R-003 留下可核对的协议输入，但不将 F-003/F-004、I-009/I-010 或任何 Web 门禁误记为已关闭。

## 高层路线图

| 阶段 | 主题 | 状态 | 退出条件 |
|------|------|------|----------|
| A | 协议边界与信息就绪 | 已完成 | D-001/D-002 与协议明确工作区、Root Goal、串行阶段、legacy 路径和下游排除项。 |
| B | canonical 文档协议 | 已完成 | `workspace-protocol.md`、独立启用说明和 `workspace-context.md` 形成；资料字段与 fail-closed 规则由语义测试核对。 |
| C | Skills 首先适配 | 已完成 | 编排器、原语、独立审计及宿主规则镜像按 canonical 协议处理工作区和共享资料引用；未新增第二真相源。 |
| D | 验证、审视与交接 | 已完成 | 模板/镜像/安装/standalone/语义测试通过；A-001 无开放 required finding，GOAL-009 输入与未关闭门禁已在 A-008 交接。 |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 工作区如何绑定独立 Root Goal 与 canonical 范围；串行阶段何时更新路线图、何时才修改 Root Goal；现有单 Root 仓库如何保持兼容？ | 阶段 A 冻结与 canonical 协议 | 阶段 A 结束前 | 在 workspace protocol、模板和语义测试中对照 P-001、目标平铺规则及 legacy 单工作区路径。 | verified | 由 D-002 关门；无 residual。 | [workspace protocol](../../architecture/workspace-protocol.md) 第 2～4 节、模板和 `docs/tests/test_workspace_protocol.py` 的 legacy/Root/范围测试。 |
| I-002 | required | 共享资料引用最小需要哪些可验证字段，如何避免引用成为跨工作区目标状态通道，哪些物理存储/CRUD 事项必须留给下游？ | canonical 协议与 Skills 适配 | 阶段 B 结束前 | 以 GOAL-009 D-004 为已确认产品边界输入，定义逻辑引用协议、拒绝条件和下游排除项，并以模板/测试核对。 | verified | 由 D-002 关门；不把实现范围移入本目标。 | 协议第 5 节、模板固定引用表，以及 `test_workspace_protocol.py` 的有效/不匹配/无效摘要拒绝测试。 |
| I-003 | required | Skills 如何发现或校验工作区上下文、处理无 manifest 的 legacy 仓库、拒绝不匹配 Root Goal 与未固定共享资料引用？ | 阶段 C 适配 | 阶段 C 结束前 | 更新编排器、原语、审计提示与宿主规则镜像；以正反语义测试验证。 | verified | 由 D-002 关门；无 residual。 | `skills/prompts/00`～`05`、宿主规则镜像，以及 `skills/tests/test_skills_orchestrator.py` 的工作区协议表面和 fail-closed 断言。 |
| I-004 | required | 如何证明 canonical 与 Skills 镜像、安装分发和 standalone core 使用同一协议，且测试覆盖关键拒绝路径？ | 阶段 D 验证与关门 | 阶段 D 结束前 | 扩展 mirror、install、standalone 和语义测试；记录命令、结果与覆盖范围。 | verified | 由 D-002/A-001 关门；无 residual。 | 8 项 docs/standalone 测试、32 项 Skills 测试和 `skills/tests/test_install_ps1_isolated.ps1` 的 F-018 isolated install 通过。 |
| I-005 | non-blocking | 多工作区物理存储、共享资料用户 CRUD、AI 读取执行、跨工作区导航元数据和 Web 访问/安全模型如何实现？ | GOAL-009 路线图 B/D 与后续产品实现 | 下游目标立项前 | 保留给 GOAL-009 I-009/I-010/I-004 及后续实现目标；本目标只提供协议输入。 | open | 由 GOAL-009 R-003、I-009/I-010 在下游复核。 | [GOAL-009 A-008](../GOAL-009-ai-assisted-governance-workbench/03-audit.md) 已接收协议输入；不在本目标作为已实现能力或关门证据。 |

## 与 GOAL-009 的关系

- GOAL-010 是 GOAL-001 下的跨层协议与 Skills 适配目标，不是 GOAL-009 的 Web 实现子目标。
- 本目标可为 GOAL-009 R-003 提供工作区和共享资料引用的 canonical 语义；GOAL-009 仍须自行收集 I-009/I-010 的产品模型、访问/操作契约和正反验证。
- GOAL-010 不放行 GOAL-009 路线图 B/C，不关闭 F-003/F-004、I-009/I-010，也不引入多用户、角色、账号或 Web 写入。

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
