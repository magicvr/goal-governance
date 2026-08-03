---
id: GOAL-003-consumer-governance-ergonomics
doc: decision-entry
record_id: D-011
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# D-011 · v0.12.0 正式闭环并恢复 GOAL-003 关门

## 触发

D-010 的 fixed 条件全部发生：新版本冻结与 12 格 runtime 已提交；strict tagged evidence 通过；`v0.12.0` 经 Environment `release` 生成正式 GitHub Release；资产/digest/consumer-only profile 已核对；真实消费 dry-run + update 产生 manifest 与 rollback。A-006 independent `pass` 并判定 F-001 `fixed`，A-007 响应后开放 required = 0。

## 决定

1. A-004 F-001 以 **`fixed`** 合法闭合；不采用 `accepted-residual` 或 `user-overruled`。
2. GOAL-003 的 S7 恢复完成，I-007 为 verified，派生 progress `7/7 = 100%`，status 恢复 `done`。
3. 父 Root R2 恢复完成，Root progress 派生为 `2/3 = 67%`；Root 保持 `active`，R3 仍未开始。
4. A-004 F-002/F-003 继续作为 recommended/open 与复审触发，不升级为 required，不据此重开已通过目标。
5. 本次消费事务是首个 updater 版本的 `v0.12.0 -> v0.12.0` 正式资产验证；不宣称跨版本 e2e。后续实际版本升级可补该证据，但不是本次 F-001 的开放门禁。
6. release tag 固定在 `0748c8d`；本 D/E/A lifecycle 响应发生在正式发布之后，不回写 tag 内容或伪称属于 Release asset。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 因没有跨版本 updater e2e 保持 F-001 open | A-004/D-010 要求一次正式消费更新；`v0.11.0` 没有 updater，A-006 已独立确认首版本同版本事务满足本次边界 |
| 把 F-002/F-003 作为 residual 接受 | 它们是 recommended，不解除 required 门禁；用户也未书面接受 residual |
| 同时启动 R3 或关闭 Root / VP | 超出本次 A-004 F-001 fixed 响应范围 |
