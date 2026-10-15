---
id: GOAL-012-release-v0-13-5
title: v0.13.5 正式发布与消费资产验收
progress: 100%
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.2.0
---

# GOAL-012 · v0.13.5 正式发布

## 概述

用户在 GOAL-011 源码修复与 issue 关闭后明确要求“发布一下新版本资产”。在同一 Root R3 内发布下一个兼容性 patch v0.13.5，使独立启用说明的消费分发修复进入真实 Release；协议 0.1.0、consumer MUST 与渠道边界保持。GOAL-011 的已完成源码范围不重开，发行另立本目标。

## 成功标准

- [x] 版本清单、矩阵 candidateRevision、安装与 GHCR pin 对齐 v0.13.5；runtime 证据经实际校验。
- [x] 本地 rehearsal、相关回归与指定 provider 的 independent 候选审计通过，无开放 required。
- [x] 发布 PR 经双平台 CI 合入 main，annotated v0.13.5 指向该 merge；现有 gated workflow 完成。Environment 回执为 magicvr 人工 `skipped` 放行，非普通 approved；AI 未代批或改门禁。
- [x] Release 九项资产齐全，两个 ZIP 摘要与 sidecar 一致；解压与隔离安装核验本次修复已进入发布资产。

## 纲领路线图

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| S1 | 范围与证据基线冻结 | 完成 | 版本未占用、发布流程和 provider 明确，现有 runtime 校验通过 |
| S2 | 清单、预演与独立审计 | 完成 | 版本清单和镜像一致，rehearsal/回归/independent 意见完成 |
| S3 | PR、tag 与 gated 发布 | 完成 | PR CI 绿、main merge、strict 预检通过，tag 工作流完成发布 |
| S4 | 资产验收与关门 | 完成 | 九项资产、双 ZIP digest、消费安装及证据身份核对通过 |

S1 → S2 → S3 → S4 串行。progress 按完成阶段 4/4 = 100% 等权派生；不用于放行或关门。

## 信息需求

| ID | 级别 | 问题 | 影响门禁 | 最晚阶段 | 收集动作 | 状态 | 延期/复核 | 证据 |
|----|------|------|----------|----------|----------|------|-----------|------|
| I-001 | required | 版本、发布范围及审计 provider | 方案冻结 | S1 | 远端 Release/tag 与当前修复核对 | verified | 范围改变时复核 | D-001；最新 v0.13.4，v0.13.5 未占用；会话 provider=Codex 独立子代理 |
| I-002 | required | 既有 runtime 证据是否可复用 | S2 证据基线 | S1/S2 | capture --check + compatibility；变更清单后再核对 | verified | behaviorSources/protocol 变化时复核 | E-001：12+4 captures 校验成功、coverage ready；保持原捕获日期/路径，不伪造 v0.13.5 新采集 |
| I-003 | required | 候选清单、预演与审计是否通过 | PR/tag | S2 | 测试、rehearsal、independent 审计 | verified | 候选实现变更时复核 | E-002、A-001 independent pass、A-002 响应 |
| I-004 | required | GitHub CI、main、tag、审批与发布结果 | 发行完成 | S3 | 实际工作流及 API 回读 | verified | 重发时复核 | E-004；PR #27 / main CI success，annotated tag 指向 merge 1a6668e；run 38691121485 success；magicvr 的 Environment 回执为 skipped，AI 未操作审批或配置 |
| I-005 | required | 九项资产、摘要和消费安装结果 | 关门 | S4 | 下载真实资产、逐项核对与隔离安装 | verified | 资产变化时复核 | E-005；9 项资产、双摘要、27 个 core 子集成员、正式安装器隔离安装均 pass；MCP 镜像拉取与内置版本核对 pass |

## 审计模式

independent：发布/compatibility 高影响 scope；沿用用户在本会话指定的干净 Codex 独立子代理，L0。主代理负责实施、意见落盘/响应与最终验证，不冒充 independent。

## 对齐

父目标 [Root](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)，R3 持续演进；服务 VP-002 / Charter vision-goal-governance@0.2.0。Root 与 VP 保持长期 active，Root progress 67%。

## 关门

[A-003](03-audit/A-003-release-close-out.md) self close-out pass；A-001 independent / A-002 响应均 pass，无开放 required、无审计冲突、无 residual/overruled。按 [D-002](01-decision/D-002-close-out.md) 将本目标结项，发行身份与证据见 E-004/E-005 及附件。
