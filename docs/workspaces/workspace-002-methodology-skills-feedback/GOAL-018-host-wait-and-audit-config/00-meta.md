---
id: GOAL-018-host-wait-and-audit-config
title: 宿主原生目标待答停止与独立审计 CLI 项目配置
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-12
updated: 2026-11-12
version: 0.1.1
progress: 100%
---

# GOAL-018 · 宿主原生目标待答停止与独立审计 CLI 项目配置

## 概述

承接用户本轮反馈：反馈 1、2 合并为一个问题——等待用户答复应控制 Codex / Claude Code / Grok Build 等宿主原生 `/goal` 的自动续跑；修改治理 GOAL 的 blocked 状态不能替代执行控制，也不应为每次询问触发 meta、执行索引、目标树和父级投影写入。反馈 3 为外部独立审计 CLI 的工具、模型、思考强度登记到仓库根 `.goal-governance.json`，以后会话直接复用。

服务父 Root 的 R3 与 [VP-002](../../../vision/plans/VP-002-methodology-skills-feedback-evolution.md) 的真实反馈演进方向。用户已授权整改、通过 PR 合并 main、发布并验收新版本资产。

## 成功标准

- [x] 规范与所有分发入口区分宿主原生目标和治理 GOAL；等待答复不自动改变治理状态或追加暂停流水。
- [x] 询问和原生执行停止按实际宿主能力衔接；空答、取消和续跑不得变成用户答复；不编造宿主能力或绕过其状态工具约束。
- [x] `.goal-governance.json` 可登记独立审计 CLI、模型与思考强度，提供校验、消费与失败路径；已有项目设置跨会话复用，显式会话覆盖优先。
- [x] canonical、Skills 镜像、宿主入口、MCP guidance、安装升级及测试一致；对应运行证据与 cross 审计通过，开放 required 为 0。
- [x] PR 经 CI 合入 main，新版本由受保护发布流程生成，正式资产摘要、安装与 GHCR 核验有据，最终审计后结项（E-005/E-006、A-003/A-004、D-003）。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| S1 | 信息核验与契约冻结 | 完成 | 明确宿主等待控制边界与项目审计配置契约；I-001/I-002 有证据 |
| S2 | 规范与实现整改 | 完成 | canonical 先行；解析、入口、镜像和回归通过 |
| S3 | 运行验证与 cross 审计 | 完成 | 当前版本真实运行证据、兼容矩阵、自审及指定 provider 独立审计；required 合法闭合 |
| S4 | PR 合并、发布与验收 | 完成 | main CI、annotated tag、正式资产和容器核验、关门结论齐全 |

S1 → S2 → S3 → S4 串行；同阶段独立扫描可并行。本目标覆盖两项整改和发布，不提前新造更多子目标。progress 唯一来源为上述四个等权阶段完成数，当前 4/4。

## 信息需求与阶段门禁

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 各宿主原生目标和阻塞问答可用机制、工具约束与不可保证的边界 | S1 契约冻结 | S1 | 官方资料、实际工具说明与代表运行核对 | verified | 宿主升级时复核 | D-002/E-002/E-003：UI-01～UI-06 已改为真实同步卡片与合法宿主执行停止，不因询问改治理 GOAL；L0 不推导原生 /goal 停启已实测 |
| I-002 | required | CLI 项目配置形状、优先级、校验、升级保留与默认 provider 来源 | S1 配置冻结 | S1 | 读取 config/schema、现有参数与最近用户指定记录 | verified | 配置/CLI 变更时复核 | D-002/E-002/E-006：项目已登记 Grok Build / grok-4.7 / xhigh；完整会话指定优先，其次项目配置、缺失才询问；严格校验、安全 argv 与安装字节保留通过 |
| I-003 | required | 当前代码的运行行为、兼容性与审计结果 | S3 验收 | S3 退出 | 回归、真实宿主运行、证据采集、self + independent | verified | 修订入口后重新采集 | E-003/E-004、A-001/A-002：当前运行、回归与cross通过 |
| I-004 | required | 新版本可用性、发布门禁和正式资产一致性 | S4 验收 / 关门 | S4 退出 | 查远端版本、CI/Release、摘要/安装/GHCR验收 | verified | 资产或发布修订时复核 | E-005/E-006：v0.15.0正式发布，9资产摘要、隔离安装与GHCR通过；A-003/A-004 cross通过、两条recommended fixed |

## 审计与边界

- 模式：cross（治理元规则、宿主边界及发布）；self 由编排侧完成，independent 使用项目登记的外部 Grok Build CLI（grok-4.7 / xhigh），来源为最近用户明确指定且本轮要求持久复用。
- 自动正文仅 `/audit workspace-002 goal-018`，干净会话、不追加 scope 或编排提示；模型/强度是调用配置。失败不换工具、不降级。
- 不改 Charter/VP 边界，不重开历史目标；现有治理 blocked 仍可表达实际交付阻塞，本次只移除“因为发问而自动改 blocked”的规则。
- baseline 工作树干净，分支 `codex/goal-018-host-wait-audit-config`；只提交本任务 owned paths。
