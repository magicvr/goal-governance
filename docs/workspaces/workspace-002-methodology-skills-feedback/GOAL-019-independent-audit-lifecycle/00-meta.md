---
id: GOAL-019-independent-audit-lifecycle
title: 独立审计与探索子代理的运行边界修正及发布
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-13
updated: 2026-11-13
version: 0.3.1
progress: 75%
---

# GOAL-019 · 独立审计与探索子代理的运行边界修正及发布

## 概述

消费仓自有 AGENTS.md 的探索子代理策略可能被助手扩大解释，导致正式独立审计被套用只读、固定时限或到时关闭规则而截断。明确正式审计会话的适用边界、派发方等待与中断责任，并在 dev 完成修正，经 PR 合入 main 后发布 v0.15.1 及验收资产。

本目标服务父目标 R3 与 VP-002；不改变 Charter 的目的、边界或非目标。S1～S3完成，A-003正式Grok independent/pass、开放required0；PR#43已合入main fbc2d2f、两平台CI绿，annotated v0.15.1已推送且CI pack验收通过。S4的受保护publish等待release Environment审批，正式Release/GHCR尚未发布验收。

## 成功标准

- [x] canonical 契约区分普通探索子代理与正式 `/audit`、`/vision-audit`，明确角色、写入范围、等待、完成及中断边界。
- [x] 派发方与审计方均经现有强制加载路径消费新规则；用户明确要求、权限与宿主硬限制仍有效，审计内部普通探子不获整体豁免。
- [x] 受影响的真实宿主证据重新采集、镜像和回归通过，cross 审计无开放 required。
- [ ] dev 的 PR 经 CI 合入 main，annotated v0.15.1 经受保护发布流程产出资产；摘要、双包一致性、隔离安装与 GHCR 可核对。
- [ ] 过程事实、审计响应和发布收据落盘，目标与 goal-tree 同步，关门结论有证据。

## 纲领路线图

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| S1 | 定义范围与证据策略 | 完成 | D-001；工作区/父级/VP 对齐、变更面及受影响证据已核对 |
| S2 | 契约修正与分发同步 | 完成 | E-002/A-001；镜像44对一致、Skills108/docs76通过 |
| S3 | 当前运行证据与 cross 审计 | 完成 | E-006/A-002/A-003/A-004；16项选用、完整回归、指定Grok independent/pass，开放required0 |
| S4 | PR、正式发布与关门验收 | 进行中 | main CI、annotated tag、受保护 Release、9 项资产及消费验收与关门审计完成 |

S1→S2→S3→S4 串行；同阶段的独立验证可并行。progress 仅按四个阶段等权派生，当前 3/4 = 75%，不构成发布验收通过或 done。

## 信息需求

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 规则最小同步面与 CLI/MCP 证据是否必须重采 | 方案冻结 | S1 | 核对入口加载、stage、矩阵 behaviorSources 与发布校验 | verified | 写集变化时复核 | D-001；12 CLI 与4 MCP 均固定了两份权威文件，16 格须重采；不改 prompts/wrappers |
| I-002 | required | cross independent provider 与 CLI 参数来源 | 派发 | S1 | 校验项目配置 | verified | 用户覆盖或配置变更时复核 | `.goal-governance.json`：grok / grok-4.7 / xhigh，按完整配置复用 |
| I-003 | required | 新规则下真实入口、台账边界及当前来源哈希是否通过 | S3 退出 | S3 | 隔离消费夹具真实采集、证据校验与 cross 审计 | verified | 当前工作树或入口变更时重查 | E-006、A-002/A-003/A-004：16项来源/原始摘要、台账边界、完整回归与cross通过 |
| I-004 | required | main/tag/Release 与正式资产是否一致、可安装 | S4 退出 / 关门 | S4 | CI、受保护发布、下载摘要/包内容/安装/GHCR 验收 | collecting | 发布完成或失败时复核 | E-008：PR#43、main CI、annotated tag与CI pack验收通过；publish待Environment审批，正式九资产/GHCR尚未验收 |

## 审计与执行约定

- 模式 cross：治理元规则及发布边界；self 由编排侧记录，independent 由项目指定 Grok CLI 在干净会话执行，仅输入 `/audit workspace-002 goal-019`。
- 正式审计不继承普通探索代理的十分钟强制收尾；按本次实际审计状态监测，单次 wait 超时不终止或算完成。用户取消、明确审计预算及实际宿主故障照实处理，未完成时门禁不满足。
- 基线 dev `1b73adfc5434f422f0c660e173e97d357c5db046`，工作树干净，dev/origin/dev/origin/main 一致。默认启用显式 owned paths 的 Git checkpoint。
- 旧 v0.15.0 采集作为历史保留；新采集写入 v0.15.1，不改写旧哈希或伪造新采集日期。保证等级 L0。

## 父目标

[GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)；工作区 `workspace-002-methodology-skills-feedback`，canonical 范围为本区根。
