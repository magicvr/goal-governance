---
id: GOAL-001-methodology-skills-feedback-evolution
title: 真实项目反馈驱动的协议与 Skills 演进
status: active
parent: null
plan_refs: VP-002-methodology-skills-feedback-evolution
primary_plan: VP-002-methodology-skills-feedback-evolution
serves_summary: delivery Root；服务 VP-002 / vision-goal-governance@0.2.0；承接真实项目与消费方反馈修正协议与 Skills
created: 2026-07-31
updated: 2026-07-31
version: 0.1.0
progress: 0%
---

# GOAL-001 · 真实项目反馈驱动的协议与 Skills 演进

## 概述

在 Charter `vision-goal-governance@0.2.0` 与 **VP-001 奠基有界关** 之后，以**真实项目 / 消费方使用中发现的问题**为触发，持续修正核心方法论与 Skills，使协议在实战中保持可复制、可审计、可安装。

本 Root 是 [workspace-002-methodology-skills-feedback](../workspace.md) 的唯一 `parent: null` 总目标；**不**以本仓 Web 产品清单驱动（人类 UI 见 VP-003）。

## 成功标准（Root 方向级 · 暂定）

- [ ] 至少完成 **一轮** 有界「反馈 → 协议/Skills 修正 → 可核对验证」闭环（子目标证据链完整）
- [ ] 修正后的协议/Skills 仍满足完整安装与发布门禁（或 residual 用户书面接受）
- [ ] 无阻断本波次退出的 required 协议缺口；未关闭项显式 residual
- [ ] **不**要求「永远修到完美」或关闭 Web 终态

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **R1** | 消费宿主补齐与入口一致 | **进行中** | 现有 claude / copilot / grok；本波首项：Codex Skills 入口（GOAL-002） |
| **R2** | 反馈驱动的协议 / Skills 修正 | 未开始 | 真实项目问题回流；按问题拆子目标，禁止无路线图堆细目标 |
| **R3** | 有界闭环验证与 VP 退出准备 | 未开始 | 对齐 VP-002 退出判据；证据可核对后才议 VP 关门 |

同一纲领阶段内可并行多个子目标；阶段间通常串行。

## 派生进度展示

`progress: 0%` = 纲领阶段 R1～R3 中已完成 0 / 3（等权）。progress **仅展示**，不放行阶段、不关闭 finding、不推导 `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | Codex CLI / 宿主如何发现并加载 project skills（路径、清单、与 AGENTS 关系） | GOAL-002 方案冻结 | R1 方案 | 读官方/宿主文档 + 对照现有 install 适配器 | open | — | 子目标 GOAL-002 收口 |
| I-002 | non-blocking | 下一轮真实项目反馈的首批问题清单 | R2 立项优先级 | R2 立项前 | dogfood / 用户提交 | open | 有反馈再填 | 未开始 |
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

## 备注

- 开区决策见 [01-decision.md](01-decision.md) D-001。
- 编号自 GOAL-001 起；**不**延续 workspace-001 的 GOAL-024+。
