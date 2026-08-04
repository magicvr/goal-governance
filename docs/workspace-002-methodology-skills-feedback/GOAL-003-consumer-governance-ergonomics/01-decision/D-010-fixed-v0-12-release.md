---
id: GOAL-003-consumer-governance-ergonomics
doc: decision-entry
record_id: D-010
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# D-010 · A-004 F-001 采用 fixed 与 v0.12.0 受控发布切片

## 触发

A-004 独立复核把“已安装 Skills 可升级”解释为正式消费版本能力，确认 `v0.11.0` 不含 updater，且当前 `compatibility_report.py --require-ready` 因行为源陈旧失败。用户明确要求优先按 `fixed` 建立新版本冻结、兼容证据与正式 Release 闭环。

## 决定

1. 采纳 A-004 的正式消费边界；D-009 的历史关门事实保留，但其无条件 close-out 口径在 F-001 范围内被本决策后继修正。
2. 以 **`0.12.0` / `v0.12.0`** 作为新 minor：本切片首次正式交付事务 updater、consumer-only evidence profile、ledger / audit / checkpoint 行为变化，不回写或改造已发布 `v0.11.0`。
3. fixed 关闭条件保持完整：冻结 matrix / CHANGELOG / 安装 pin；对 Claude、Grok、Copilot 四入口重采 12 份 runtime evidence；通过 `compatibility_report.py --require-ready` 与 strict release evidence；创建并推送 annotated tag，经受控 workflow 生成 GitHub Release；从正式资产核对 updater、指南与 producer-only 排除；完成一次真实消费仓更新。
4. 在上述证据完成前，GOAL-003 恢复 `active`，S7 恢复整改中，派生 progress 为 6/7 = 86%；Root R2 同步恢复整改中，Root progress 为 1/3 = 33%。
5. release / compatibility 属高影响门禁，采用 `independent` 模式。沿用本目标 D-005 已授权的 Grok Build provider 做 fixed 后复核；provider 不可用或无可核对输出时不降级。
6. 新 runtime evidence 固化到根级发行证据路径 `docs/releases/runtime/v0.12.0/`；不改写 `docs/workspace-001-goal-governance/GOAL-008-skills-consumer-adapter-release-consistency/` 的历史捕获物或 lifecycle 状态。
7. A-004 F-002/F-003 继续作为 recommended 跟踪，不升级为本次正式 Release 的 required 门禁。

## 理由

- updater 与消费证据边界是向消费方新增的可见能力，minor 比 patch 更符合 SemVer 语义。
- fresh runtime evidence 与正式 Release 资产共同证明“源码实现”已经进入可安装版本；仅更新摘要或 README 不能证明宿主行为与正式包。
- 暂时恢复 lifecycle 能让 `status`、S7、Root R2 与开放 required finding 一致，不用历史 `progress: 100%` 掩盖门禁。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 只更新旧 runtime JSON 的 behaviorSource 摘要 | 行为源发生实质协议变化，摘要替换不能证明真实宿主 dispatch |
| 发布 `v0.11.1` | 本切片包含新的消费功能与治理行为，不是纯 bugfix |
| 接受 residual / 驳回 A-004 | 用户明确选择 fixed |
| 手工创建 Release 绕过 Environment / strict evidence | 会削弱既有生产发布门禁，不能合法关闭 F-001 |

## 后续动作

1. 固化 `v0.12.0` runtime / compatibility / changelog / pin 候选并执行全量验证。
2. 创建 release-candidate checkpoint 与 annotated tag，推送后等待受控 workflow。
3. 核对正式资产并运行真实消费更新；记录 E / A 响应与 independent 复核后再恢复关门。
