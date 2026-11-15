---
id: GOAL-020-goal-drift-detection
title: 父子目标漂移的漏审根因、防护与发布
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
progress: 75%
---

# GOAL-020 · 父子目标漂移的漏审根因、防护与发布

## 概述

用户报告：父目标拆出子目标后，子目标推进发生显著目标漂移，审计未发现。调查协议与消费入口的原因，在立项、路线图、变更、实施和审计中补齐可验证防护，在 dev 修改，PR 合入 main 后发布新版本资产。

## 成功标准

- [x] C1：用源码出处与可重放反例说明漏审机制；区分用户反馈、已证实规则缺口与未知历史实例。
- [x] C2：canonical 方法论、模板、Skills 与 MCP 消费一致要求父级贡献、授权基线/变更与实际交付对照；发现漂移阻断受影响门禁。
- [x] C3：反例可识别漂移，合法分阶段子集/授权调整不误判；回归、受影响宿主证据与 cross 审计通过，无开放 required。证据A-002/A-003；仅实施不符案为required阻断，不计作模型漂移分类。
- [ ] C4：dev → PR → main CI → annotated 新版本 → 正式资产、隔离安装与容器验收可核对。

## 父级贡献与初始授权

父级 [Root](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md) 的 R3「持续闭环与长期演进」及成功标准 1/2：将真实反馈修成可审计、可安装的协议与 Skills。证据基点：Root version 0.14.45、D-008 长期治理决策、Git `81913d2`；不改变 Root/VP/Charter 成功边界。本目标只交付一次有界修复及发布，不声称 Root/R3/VP 已完成。原始授权保留在 [D-001](01-decision/D-001-scope-and-baseline.md)。

## 纲领路线图

| 阶段 | 内容 | 状态 | 退出证据 |
|------|------|------|----------|
| S1 | 根因调查与契约冻结 | 完成 | I-001 verified；D-001、root-cause.md |
| S2 | canonical、模板与消费入口修正 | 完成 | E-002：stage44对、Skills113/docs76 |
| S3 | 行为验证、宿主证据与 cross 审计 | 完成 | I-002 verified；A-002/A-003、无开放 required |
| S4 | PR/main/正式发布及验收 | 进行中 | I-003 verified；正式收据与关门审计 |

S1 → S2 → S3 → S4；阶段内独立验证可并行。progress = 已完成阶段/4，当前 3/4。

## 信息需求

| ID | 级别 | 问题 | 影响门禁 | 最晚阶段 | 收集动作 | 状态 | 延期/复核 | 证据/结论 |
|----|------|------|----------|----------|----------|------|-----------|-----------|
| I-001 | required | 漏审机制与最小修正契约是什么？ | 方案冻结 | S1退出 | 权威及入口逐项对照、反例设计 | verified | 不延期 | D-001、attachments/root-cause.md、E-002 |
| I-002 | required | 修正是否识别漂移并保留合法阶段子集？ | 实施验收 | S3退出 | 静态回归、隔离真实宿主反例/正例、指定 provider 审计 | verified | 不延期 | E-003、A-002/A-003、attachments/semantic-results.md；验收替代/无关产物被写成漂移，仅实施不符只计required阻断 |
| I-003 | required | 发布资产是否绑定通过验证的源码？ | 关门 | S4退出 | PR/main CI、release evidence、摘要、安装与容器验收 | open | 不延期 | 待发布产生证据 |
| I-004 | non-blocking | 用户原始漂移实例的具体台账是什么？ | 根因结论外推范围 | 获得实例时 | 用户补充后按同一对照复核 | open | 实例到达即复核，责任人主代理 | 当前无具体项目材料；不编造历史漏审结论 |

## 审计与交付边界

元协议变更采用 cross；配置来源 `.goal-governance.json`：Grok Build / grok-4.7 / xhigh。自动正式输入仅 `/audit workspace-002 goal-020`，干净会话。Codex CLI 取证显式 `--model gpt-6-luna`。候选版本 v0.16.0，最终以受门禁保护的 annotated tag/Release 为准；L0 规范与行为证据不宣称系统级语义拦截。
