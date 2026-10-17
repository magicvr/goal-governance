---
id: D-003
goal: GOAL-013-audit-dispatch-and-user-input-gates
doc: decision
title: 用户采纳路径 A、指定 Grok Build 与 S1 契约冻结
status: accepted
parent: GOAL-013-audit-dispatch-and-user-input-gates
created: 2026-10-16
updated: 2026-10-16
version: 0.1.0
---

# D-003 · S1 契约冻结与 Grok Build provider

## 真实用户答复

2026-10-16，通过同步 `functions.request_user_input` 收到：

| 问题 ID | 实际提交值 |
|---------|------------|
| s1_contract_path / Q-001 | `A 现有入口规范化 (Recommended)` |
| independent_provider / Q-002 | `Grok Build` |

两题均有对应的非空提交值；不是预选项推定，也不是工具空返回。[答复回执](../attachments/s1-user-answer-2026-10-16.json) 保留实际返回字段。问题完整提案见 [D-002](D-002-s1-contract-proposal.md)，卡片中 A 的说明明确“实际问答行为留待 S3 验证”。本记录只采纳实际答案，不把未选择的 Codex 推荐项写成用户选择。

## 决定

1. 采纳 D-002 的共同契约和路径 A；冻结命令白名单、三位输出/入口补零与唯一解析、自主审计范围、干净上下文、同步卡片优先、缺答暂停/blocked/恢复，以及现有入口规范化的实施边界。
2. 不选择 B 的新解析/派发接口；不新增 provider runner，不改变现有 MCP 参数 schema。MCP 仍须在既有 guidance 与消费规则中表达自动派发约束，不能把兼容 task/scope 当绕过条款。
3. 本目标 cross provider 为 **Grok Build**。本机版本 1.0.60 (01a8e1c591c0)，仓内 `.grok/skills/audit/SKILL.md` 与 `vision-audit/SKILL.md` 可读并指向正式 prompts。后续 Goal 独立审计输入只能 `/audit 002 013`；需要 VP 审视时仅使用对应 `/vision-audit NNN`。本轮未调用独立审计，不宣称 Grok 模型服务、认证或审计结果已经通过。实际调用失败时门禁保持未满足，不自动更换 provider。
4. S1 的宿主核对结论是“能力来源、已知限制、保守缺答处理契约与验证计划已明确”。I-001/I-002 只在该设计范围内 verified；各当前版本 UI 的取消、空返回、headless 和恢复事实仍开放在 I-004，须于 S3 验收前取得。该分层落实了用户选择 A 时明确的 S3 验证范围，不是 residual 接受、取消用例或把未验证事实写成 verified。
5. I-003（provider 指定）与 I-005（路径裁决）verified。Q-001/Q-002 的待答原因已解决，未发现其他当前阻塞；Goal 从 blocked 恢复 active。S1 完成，S2～S4 未开始，派生 progress 为 1/4 = 25%。
6. 用户本轮要求开展 S1；本记录只完成 S1 冻结与恢复，不推定已获继续 S2、正式发布或关门授权。下一步建议按冻结写集开展 S2。

## 未选方案与风险边界

| 方案 | 未选原因 / 当前约束 |
|------|---------------------|
| B 新增代码强制校验路径 | 用户选择 A；不扩大本轮实现与分发范围 |
| Codex / Claude Code provider | 用户明确指定 Grok Build，不能由编排器替换 |
| 直接声称卡片行为已验证 | 本轮只取得当前 Codex 的真实答复提交实例；没有其他宿主的完整 UI 空答复与恢复证据，I-004 继续阻断验收 |

File 路径主要是规范与 agent 遵守的保证，不承诺系统级强制拦截；这不削弱“自动派发只能输入正式命令”和“缺答必须停止”的行为要求。后续若证据不符或出现信息冲突，回到 P-004，不自动降低验收阈值。
