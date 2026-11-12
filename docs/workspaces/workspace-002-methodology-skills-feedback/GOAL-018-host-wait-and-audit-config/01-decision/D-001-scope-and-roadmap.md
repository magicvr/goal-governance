---
id: GOAL-018-host-wait-and-audit-config
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-12
updated: 2026-11-12
version: 0.1.0
---

# D-001 · 反馈合并、范围与交付路径

用户明确要求在工作区 2 新增子目标、完成整改、PR 合入 main 并发布新版本资产。本目标挂当前 Root R3；反馈 1、2 按维护者判断合并，另保留独立审计 CLI 配置这一交付面。

先核验原生 `/goal` 的状态控制与阻塞问答能力，再改 canonical UI 契约，随后实现配置解析、消费入口、测试及镜像。不得只改“blocked”的名称而继续用治理写盘冒充宿主执行控制；不得为了询问创建或组合治理目标，也不得新造原生目标。

项目审计默认值沿用 [GOAL-017 D-002](../../GOAL-017-on-demand-governance-context/01-decision/D-002-audit-provider.md) 中用户最近指定的 Grok Build CLI、grok-4.7、xhigh。用户本轮要求将此类配置持久化；新会话按项目配置取值，显式会话要求覆盖，非法或执行失败不静默替换。模式按风险为 cross；不把持久默认当作已通过审计。

采用新的 `codex/goal-018-host-wait-audit-config` 分支，基于与 dev 相同的 origin/main；分阶段 checkpoint。下一 minor 候选为 v0.15.0（新增可复用项目配置并纠正 UI 行为）；协议消费契约的版本是否需要变化在 S1 依实际影响决定。

未选：继续自动维护治理 blocked（无法控制原生续跑，且用户明确拒绝）；每会话重问同一审计工具（违背本轮反馈）；绕过受保护发布（仍按仓库现有 CI/Environment 门禁）。本记录只确认立项和工作路径，不虚构实现、运行或发布成功。
