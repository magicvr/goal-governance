---
id: GOAL-004-frozen-web-asset-retirement
title: 移除冻结 Web 资产并挂起 VP-003
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
plan_refs: VP-002-methodology-skills-feedback-evolution
primary_plan: VP-002-methodology-skills-feedback-evolution
serves_summary: VP-002 R3 的一次性仓库卫生与退出准备；退役冻结 Web 实现，不激活 VP-003
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
progress: 25%
---

# GOAL-004 · 移除冻结 Web 资产并挂起 VP-003

## 概述

彻底移除本仓已冻结的 FastAPI Web 资产及其专属回归、兼容和发行门禁，消除每次全量测试与审计中的无效注意力成本；同时把 VP-003 明确维持为 `planned` 且正式挂起。未来人类 UI 方向仍在 Charter 内，但不得从本次退役资产自动恢复。

本目标属于 VP-002 Root 的 **R3 有界闭环验证与退出准备**：它是 producer 仓库卫生和投资面收束，不是 VP-003 产品实施，也不发布新的方法论或 Skills 资产。

## 成功标准

- [ ] 仓库中不再存在 `web/`，且现行 CI、release workflow 与 release-evidence 不再安装或执行 Web 专属依赖/测试。
- [ ] compatibility matrix 只保留 canonical Skills host adapters；Web parser consumer 与专属校验已删除，schema 与其余 readiness 门禁保持有效。
- [ ] 根入口、现行架构说明、Charter / VP / roadmap 和两个工作区的现时摘要均准确描述“资产已退役、VP-003 挂起”；历史 ledgers 不批量改写。
- [ ] `docs/architecture/principles.md`、`workspace-protocol.md`、`docs/templates/**`、`skills/prompts/**`、`skills/install/**`、`skills/core/**` 相对基线无变化。
- [ ] canonical-to-Skills stage、定向测试、完整非 Web 回归与 `git diff --check` 通过；唯一允许的 Skills 内容变化是生成的 compatibility matrix 镜像。
- [ ] independent close-out audit 为 `pass`，开放 required finding = 0；目标与 goal-tree 同步为 `done / 100%`。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 决策、库存与边界冻结 | **完成**（2026-08-04） | workspace-001 D-029、VP-003 挂起、I-001～I-003 verified、删除与保护边界固定 |
| **S2** | Web 资产与主动依赖移除 | 未开始 | `web/`、CI/release Web check、matrix Web consumer 与对应测试清除 |
| **S3** | 现行叙事收束与完整验证 | 未开始 | 当前入口无失效 Web 路径；stage/mirror、核心与 Skills 边界、非 Web 回归通过 |
| **S4** | independent 复核与关门 | 未开始 | 正式 A-001 落盘、开放 required = 0、目标和 Root/goal-tree 同步 |

## 派生进度展示

`progress: 25%` = S1～S4 中已完成 **1 / 4**（等权）。它只表示决策与边界已冻结，不代表删除、验证或关门完成。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 冻结 Web 的物理资产和主动依赖边界是什么 | S2 实施 | S1 | `git ls-files web` + 全仓 active reference scan | **verified**（2026-08-04） | 新引用出现则回流 | 63 个 tracked `web/` 文件；主动依赖集中于 CI、release workflow、release-evidence、compatibility matrix/report 及对应测试；历史工作区记录保留 |
| I-002 | required | VP “挂起”如何使用合法状态表达 | 愿景写入 | S1 | 核对 VP 状态枚举与现有 VP-003 | **verified**（2026-08-04） | 状态 schema 变化时复核 | 保持 `status: planned`，正文写正式挂起、无排期/无绑定/恢复须新书面决策 |
| I-003 | required | 哪些核心/Skills 路径必须保持不变，matrix 镜像如何处理 | S3 验证与关门 | S1 | 固定 Git 基线并对照 stage 白名单 | **verified**（2026-08-04） | 任一受保护路径出现 diff 即 fail closed | 基线 `e7a49bef173389f1fbcf5774d65ad3d8c74ed3b8`；只改 canonical matrix 后运行 stage；仅 `skills/contracts/...matrix.json` 允许生成变化 |

## 审计模式

**independent**。理由：物理删除可由 Git 恢复，但改动触及 producer CI / compatibility / release evidence 门禁；不改 P-001～P-006 或 Skills 行为，因此不需要 cross。独立 provider 只写意见，状态响应仍由 `/govern` 完成。

## 父目标与跨区授权

- 父目标：[GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)
- 封存区后置授权（Q2）：[workspace-001 GOAL-001 D-029](../../workspace-001-goal-governance/GOAL-001-main-vision/01-decision/D-029-retire-frozen-web-assets.md)
- 对应愿景：[VP-003-human-ui-workbench-deferred](../../vision/plans/VP-003-human-ui-workbench-deferred.md)（仍 `planned`，不作为本目标 `primary_plan`）

## 台账布局

新记录从 `01-decision/`、`02-execution/`、`03-audit/` 平铺 ledger 写入；`attachments/` 只保存必要证据。
