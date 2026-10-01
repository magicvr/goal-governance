---
id: D-011
goal: GOAL-001-methodology-skills-feedback-evolution
doc: decision
title: 承接发布门禁缺口，创建 GOAL-010 并冻结 v0.13.4 发布范围
status: accepted
parent: null
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# D-011 · 创建 GOAL-010 承接发布门禁缺口（2026-10-01）

**状态**：accepted

**触发**：用户要求推送 PR、确保 CI 全绿后合并 `main`、再打 tag 发布新资产。编排前的只读核对发现 `dev` 顶端的发布门禁是红的。

## 决定

1. 在 Root 纲领 **R3（持续闭环与长期演进）** 内创建 **`GOAL-010-release-gate-recapture-and-v0-13-4`**。
2. 编号使用区内下一可用 **GOAL-010**；`parent` = `GOAL-001-methodology-skills-feedback-evolution`。
3. 发布版本冻结为 **`v0.13.4`（patch）**；annotated tag 只指向已合并 `main` 的 merge commit；资产集合沿用 v0.13.3 的 9 项形态。
4. 缺口修复路径为**重捕获 12 格 runtime 证据**，**不是**回滚 `d1256eb`（该提交是 GOAL-009 已关门并已审计的 P-005 语义修正）。
5. independent 审计 provider = 本地 codex CLI（模型 `gpt-6.1-sol`，思考强度 `high`），scope = 发布候选完整审计。
6. Root / VP-002 保持 `active`；R3 保持进行中；Root `progress` 保持 **67%（2/3）**——本轮是发布与门禁修复，不改 Root 纲领阶段完成数。

## 为什么

- D-008 已确认按反馈随时立项。GOAL-009 已 `done`，下一编号为 GOAL-010。
- 缺口是 GOAL-009 改动的**副作用**（证据锚点过期），不是 GOAL-009 已关门范围的回归；用独立子目标承载发布与门禁修复，符合 P-001 的「独立可验收交付节点」判定。
- 发布是长期过程记录，必须落到目标台账（本区目标五件套 + `goal-tree.md`），不写在愿景目录。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 复用 GOAL-009 记账并在其内发布 | GOAL-009 已按用户书面决定「关门且不包含正式发布」；重开已关门目标会让那次裁决失去意义 |
| 只在 CHANGELOG / 契约里改版本，不建目标 | 发布是不可逆的长期动作；不建目标会让「谁授权了这次发布、依据什么门禁」无从追溯 |
| 回滚 `d1256eb` 让旧证据重新有效 | 会撤销已关门并已审计的 P-005 语义修正 |
