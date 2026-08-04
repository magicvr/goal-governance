---
id: GOAL-001-methodology-skills-feedback-evolution
title: 真实项目反馈驱动的协议与 Skills 演进
status: active
parent: null
plan_refs: VP-002-methodology-skills-feedback-evolution
primary_plan: VP-002-methodology-skills-feedback-evolution
serves_summary: delivery Root；服务 VP-002 / vision-goal-governance@0.2.0；承接真实项目与消费方反馈修正协议与 Skills
created: 2026-07-31
updated: 2026-08-04
version: 0.6.0
progress: 67%
---

# GOAL-001 · 真实项目反馈驱动的协议与 Skills 演进

## 概述

在 Charter `vision-goal-governance@0.2.0` 与 **VP-001 奠基有界关** 之后，以**真实项目 / 消费方使用中发现的问题**为触发，持续修正核心方法论与 Skills，使协议在实战中保持可复制、可审计、可安装。

本 Root 是 [workspace-002-methodology-skills-feedback](../workspace.md) 的唯一 `parent: null` 总目标；**不**以本仓 Web 产品清单驱动（人类 UI 见 VP-003）。

## 成功标准（Root 方向级 · 暂定）

- [x] 至少完成 **一轮** 有界「反馈 → 协议/Skills 修正 → 可核对验证」闭环（子目标证据链完整）
- [x] 修正后的协议/Skills 仍满足完整安装与发布门禁（GOAL-003 `v0.12.0` formal Release；A-004 F-001 fixed）
- [ ] 无阻断本波次退出的 required 协议缺口；未关闭项显式 residual
- [ ] **不**要求「永远修到完美」或关闭 Web 终态

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **R1** | 消费宿主补齐与入口一致 | **完成**（2026-07-31） | claude / copilot / grok 既有；Codex 经 [GOAL-002](../GOAL-002-codex-skills-entry/) 补齐（install 面 + 主入口 runtime）；用户 `/govern` 确认收口（D-003） |
| **R2** | 反馈驱动的协议 / Skills 修正 | **完成**（2026-08-04） | [GOAL-003](../GOAL-003-consumer-governance-ergonomics/) `v0.12.0` 正式 Release / consumer update / A-006 independent pass；F-001 fixed，开放 required = 0 |
| **R3** | 有界闭环验证与 VP 退出准备 | 未开始 | 对齐 VP-002 退出判据；证据可核对后才议 VP 关门 |

同一纲领阶段内可并行多个子目标；阶段间通常串行。

## 派生进度展示

`progress: 67%` = 纲领阶段 R1～R3 中已完成 **2 / 3**（等权：R1/R2 完成，四舍五入）。R2 恢复完成的依据是 GOAL-003 D-011 与 A-006/A-007；progress **仅展示**，不启动 R3、不推导 Root `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | Codex CLI / 宿主如何发现并加载 project skills（路径、清单、与 AGENTS 关系） | GOAL-002 方案冻结 | R1 方案 | 读官方/宿主文档 + 对照现有 install 适配器 | **verified**（2026-07-31） | 官方路径变更时复核 | 子目标 [GOAL-002](../GOAL-002-codex-skills-entry/)：I-001/I-002 verified + D-002；证据 [i-001-i-002-…](../GOAL-002-codex-skills-entry/attachments/i-001-i-002-codex-skills-loading-2026-07-31.md)；关门 A-001/A-002 pass（A-002 F-004 触发本台账同步） |
| I-002 | non-blocking | 下一轮真实项目反馈的首批问题清单 | R2 立项优先级 | R2 立项前 | dogfood / 用户提交 | **verified**（2026-08-03） | 新一批反馈出现时追加 | 用户本轮提交 FB-001～FB-005；见 [GOAL-003 D-001](../GOAL-003-consumer-governance-ergonomics/01-decision.md#d-001--将五项实战摩擦纳入同一-r2-大目标2026-08-03) |
| I-003 | non-blocking | 是否需要将 Charter `primary_workspace` 迁到本区 | 叙事一致性 | 用户要求时 | P-004 | open | 用户本轮确认：**001 仍 primary** | 2026-07-31 确认 |

## 愿景对齐

| 项 | 值 |
|----|-----|
| Charter | `vision-goal-governance@0.2.0` |
| primary_plan | [VP-002-methodology-skills-feedback-evolution](../../vision/plans/VP-002-methodology-skills-feedback-evolution.md) |
| workspace | `workspace-002-methodology-skills-feedback` · `vision_role: delivery` |
| 奠基区 | [workspace-001](../../workspace-001-goal-governance/) · primary · Root done（只读指针） |

## 子目标

| id | title | status |
|----|-------|--------|
| [GOAL-002-codex-skills-entry](../GOAL-002-codex-skills-entry/00-meta.md) | 添加 Codex 可用的 Skills 入口 | done |
| [GOAL-003-consumer-governance-ergonomics](../GOAL-003-consumer-governance-ergonomics/00-meta.md) | 修复消费仓门禁与长流程治理摩擦 | done |

## 备注

- 开区决策见 [01-decision.md](01-decision.md) D-001；R1 收口见 **D-003**；R2 启动见 **D-004**。
- 编号自 GOAL-001 起；**不**延续 workspace-001 的 GOAL-024+。
- R1 收口 **不**等于 Root 成功标准全勾、**不**等于 VP-002 可关门；GOAL-002 I-003（矩阵 committed）仍 non-blocking residual，不阻断 R1。
