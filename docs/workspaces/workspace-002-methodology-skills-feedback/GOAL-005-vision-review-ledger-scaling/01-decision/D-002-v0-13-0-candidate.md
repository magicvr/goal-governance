---
id: D-002
goal: GOAL-005-vision-review-ledger-scaling
title: 冻结 0.13.0 候选身份与 fresh runtime evidence
status: accepted
created: 2026-08-06
updated: 2026-08-06
version: 0.1.0
---

# D-002 · 冻结 `0.13.0` 候选身份与 fresh runtime evidence

## 决定

1. 本次 Vision Review ledger 协议扩展以 SemVer minor 候选 **`0.13.0`** 发布；兼容矩阵、CHANGELOG、README 与 bootstrap 示例统一使用该候选身份。
2. `docs/contracts/skills-consumer-compatibility-matrix.json` 的 `candidateRevision` 固定为 `v0.13.0`；canonical 与 Skills mirror 逐字节一致。
3. Claude Code `2.1.223`、Grok Build `0.2.118`、GitHub Copilot CLI `1.0.75` 的四入口 fresh captures（2026-08-06）分别归档到 `docs/releases/runtime/v0.13.0/`，共 12 个 `runtime-verified` 单元。
4. 该候选身份不等于正式发布。只有 merged-main ancestry、annotated tag、release-mode evidence、Environment 审批、资产 digest 与消费包边界全部通过后，才可宣称 `v0.13.0` 正式 Release。

## 为什么

Vision Review 的权威写入契约、历史迁移和 Skills 消费 surface 同时变化，属于向后兼容的协议扩展；patch 版本不足以表达新报告目录、编号合并和响应投影规则。旧 `v0.12.1` runtime evidence 因行为源变化不能复用，fresh captures 是当前候选的必要证据。

## 门禁

- S4 self + independent cross audit 必须先形成且无开放 required finding。
- S5 必须从合并后的 `main` 创建 annotated `v0.13.0` tag，并由 release workflow 生成和核验正式资产。
