---
id: GOAL-011-standalone-bootstrap-distribution
title: 修复 issue #24：独立启用说明的消费分发与引用
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
progress: 67%
---

# GOAL-011 · 独立启用说明的消费分发与引用

## 概述

承接 [GitHub issue #24](https://github.com/magicvr/goal-governance/issues/24)，修复已分发规则和 Skills 入口对未分发 `standalone-bootstrap.md` 的引用，使消费仓能够核对完整安装规则。用户已明确要求在工作区 2 建子目标、解决问题后关闭 issue。服务父目标 R3 与 VP-002 的真实消费反馈闭环；方案 A 与 Codex independent provider 已经用户确认（D-002）。

## 成功标准

- [x] 消费包中的相关引用在实际分发与安装布局中可用，一致性规则可核对。
- [x] canonical、stage 镜像、打包与安装路径一致；有隔离消费验证和防回归覆盖。
- [x] self 与指定 provider 的 independent 意见已落盘，相关 required findings 合法闭合。
- [ ] 修复已交付至 GitHub，issue #24 已关闭且状态经回读确认。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| S1 | 信息核对与方案冻结 | 完成 | 明确分发与门禁方案、审计 provider、验证及交付边界，关闭 I-001～I-003 |
| S2 | 修复与消费验证 | 完成 | canonical 与分发/安装实现完成，stage --check、相关回归、隔离消费验证通过 |
| S3 | 审计、交付与 issue 关闭 | 进行中 | cross 意见响应完成、GitHub 修复可核对、issue closed 回读成功 |

S1 → S2 → S3 串行。范围涉及文档协议与分发/安装两个表面，按 P-001 保留路线图。`progress: 67%` = 已完成阶段 2/3，等权，四舍五入；不作为放行依据。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | issue 内容、根因与工作区绑定是否可核对 | S1 方案冻结 | S1 | GitHub REST、canonical、stage 与 pack 代码核对 | verified | 新证据出现时复核 | E-001；attachments/issue-24.json |
| I-002 | required | 随包分发还是固定版本外链；说明是否进入 MUST 门禁 | 方案冻结与实施 | S1 | 展示互斥选项，由用户裁决 | verified | 改变方案时复核 | 用户选择 A；D-002 |
| I-003 | required | cross 的 independent provider | 实施与审计 | S1 | 用户指定可用 provider | verified | provider 不可用时回流 | 用户指定 Codex 独立子代理；D-002 |
| I-004 | required | 修复后的包内容、安装链接与规则是否一致 | 验收与关门 | S2/S3 | stage、打包、回归与隔离安装验证 | verified | 分发或安装路径变化时复核 | E-003、A-001；真实 ZIP / 安装 / 升级验证 |
| I-005 | required | GitHub 写入认证与 issue 最终关闭结果 | 交付与关门 | S3 | 恢复授权会话后交付并回读 issue | open | GitHub 写入前复核 | 授权宿主 gh 可回读 OPEN（E-002）；最终关闭结果待 S3 |

## 审计模式

`cross`：涉及消费分发契约及完整安装规则表述，需 self + 至少一个用户指定 provider 的 independent。provider = 用户指定 Codex 独立子代理（干净上下文，L0）。A-001 self 与 A-002 independent 均 pass；A-003 响应 F-001 fixed，开放 required/recommended = 0。最终交付/关闭仍待 S3。

## 父目标与证据

- [Root](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)：R3 持续演进，Root 保持 active / 67%。
- [D-001](01-decision/D-001-issue-scope.md)：已授权立项与初始边界。
- [E-001](02-execution/E-001-intake-and-scan.md)：只读扫描与证据。
