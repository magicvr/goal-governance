---
id: GOAL-014-release-v0-13-6
title: v0.13.6 正式发布与消费资产验收
progress: 100%
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.3.0
---

# GOAL-014 · v0.13.6 正式发布

## 概述

用户在 [GOAL-013](../GOAL-013-audit-dispatch-and-user-input-gates/00-meta.md) 关门后明确要求「提交 PR，确保 CI 全绿的前提下合并到 main 分支，并打 tag 发布新资产」。在同一 Root R3 内发布下一个兼容性 patch **v0.13.6**，把 GOAL-013 已关门的自动审计派发与缺答阻塞规则改进送进真实 Release；协议 `0.1.0`、consumer contract 数据结构、MUST 门禁与渠道边界保持。GOAL-013 的已完成源码范围不重开，发行另立本目标。

## 成功标准

- [x] 版本清单、矩阵 candidateRevision、安装与 GHCR pin 对齐 v0.13.6；runtime 证据经实际校验。
- [x] 本地 rehearsal、相关回归与指定 provider 的 independent 候选审计通过，无开放 required。
- [x] 发布 PR 经双平台 CI 全绿后合入 main，annotated v0.13.6 指向该 merge；现有 gated workflow 完成。Environment 回执为 magicvr 人工 `skipped`，AI 不代批、不改门禁配置。
- [x] Release 九项资产齐全，两个 ZIP 摘要与 sidecar 一致；解压、隔离安装与 MCP 镜像核对确认本次改进已进入发布资产。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| S1 | 范围与证据基线冻结 | 完成（2026-10-17） | 版本未占用、发布流程明确，现有 runtime 证据 `--check` 与 compatibility 通过 |
| S2 | 清单、预演与独立审计 | 完成（2026-10-17） | 版本清单与镜像 pin 一致，rehearsal/回归通过，指定 provider independent 意见落盘且无开放 required |
| S3 | PR、CI、main、tag 与 gated 发布 | 完成（2026-10-17） | PR 双平台 CI 全绿、合入 main、clean-tree strict 预检通过、tag 工作流完成发布 |
| S4 | 资产验收与关门 | 完成（2026-10-17） | 九项资产、双 ZIP digest、消费安装、镜像与证据身份核对通过，关门审视 pass |

S1 → S2 → S3 → S4 串行；不批量建立子目标。派生 `progress` = 完成阶段 4/4 = 100%（等权），不用于放行或关门。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 版本、发布范围与是否覆盖既有 Release | 方案冻结 | S1 退出 | 回读远端 tag/Release 与 dev 上待发布范围 | verified | 范围改变时复核 | [E-001](02-execution/E-001-baseline.md)：远端最新为 v0.13.5，v0.13.6 未占用；dev 待发布为 GOAL-013 的 e37cad3、f86b406 |
| I-002 | required | GOAL-013 S3 的现行 runtime 证据能否支撑 v0.13.6 | 证据基线 | S1/S2 | `capture_runtime_evidence --check` + compatibility report；清单变更后再核对 | verified | behaviorSources / protocol 变化时复核 | [E-001](02-execution/E-001-baseline.md)：`goal-013-s3-2026-10-17-current` 的 16 份证据 `--check` 通过，coverage `ready-for-release-evidence`；不复制改名、不伪造新捕获日期 |
| I-003 | required | 本目标 independent 审计 provider 是谁 | S2 独立审计 | S2 进入前 | 同步卡片收集用户指定并核对本机入口 | verified | 实际审计前再核对服务可用性；失败不降级、不换 provider | [D-002](01-decision/D-002-independent-provider.md)：用户 2026-10-17 通过阻塞卡片明确选择 **Grok Build CLI**；派发输入仅 `/audit 002 014` |
| I-004 | required | 候选清单、预演与独立审计是否通过 | PR / merge | S2 退出 | 测试、rehearsal、independent 审计 | verified | 候选实现变更时复核 | [E-002](02-execution/E-002-candidate-manifest-and-rehearsal.md)：清单检查点 `5de854d`；本地回归/rehearsal/strict release 预检均通过；[A-001](03-audit/A-001-independent-s1-s2-candidate.md) independent/pass、开放 required 0，F-001～F-003 由 [A-002](03-audit/A-002-findings-response.md) fixed；见 [E-003](02-execution/E-003-s2-independent-audit.md) |
| I-005 | required | GitHub PR CI、main merge、tag、审批与发布结果 | 发行完成 | S3 退出 | 实际工作流与 API 回读 | verified | 重发时复核 | [E-004](02-execution/E-004-release-receipt.md)：PR #29 CI 38999047596 双平台 pass → merge `97f6f1ea`；main CI 38999290522 success；annotated `v0.13.6`（tag object `a1224918`）→ tag run 39000107099 全绿；Environment 回执 magicvr 人工 `skipped` |
| I-006 | required | 九项资产、摘要、消费安装与镜像核对 | 关门 | S4 退出 | 下载真实资产逐项核对并隔离安装 | verified | 资产变化时复核 | [E-005](02-execution/E-005-published-asset-verification.md) 与 [asset-verification.json](attachments/asset-verification.json)：9 项资产、双摘要一致、Core 27 成员为 Skills 子集、消费安装 exit 0 且消费者规则保留、GHCR digest 与日志一致且内置版本 0.13.6 |

## 审计模式

**independent**：release / compatibility 高影响门禁，至少一个独立 provider 意见。provider 已由用户 2026-10-17 通过阻塞卡片指定为 **Grok Build**（I-003 verified，见 [D-002](01-decision/D-002-independent-provider.md)）；派发输入仅正式命令 `/audit 002 014`，编排器不自选、不附加 scope、不冒充；provider 失败时不静默降级。主代理负责实施、意见落盘与响应，不冒充 independent。

## 对齐

父目标 [Root](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)，R3 持续演进；服务 VP-002 / Charter vision-goal-governance@0.2.0。Root 与 VP 保持长期 `active`，Root `progress` 67%。

## 关门

已由 [D-003](01-decision/D-003-close-out.md) 收尾为 **done / 100%（S1～S4 4/4）**：[A-001](03-audit/A-001-independent-s1-s2-candidate.md) independent/pass（开放 required 0）与 [A-002](03-audit/A-002-findings-response.md) fixed 响应、[A-003](03-audit/A-003-release-close-out.md) 发布产出与关门审视 pass；I-001～I-006 全部 verified。真实发布身份：main merge `97f6f1ea`、annotated `v0.13.6`、tag run 39000107099 全绿、[Release](https://github.com/magicvr/goal-governance/releases/tag/v0.13.6) 9 项资产。回执提交随后合入 main；`v0.13.6` tag 固定在发行 merge，不为追加记录移动。
