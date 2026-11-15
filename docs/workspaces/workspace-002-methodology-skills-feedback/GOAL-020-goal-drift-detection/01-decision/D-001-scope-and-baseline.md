---
id: D-001
goal: GOAL-020-goal-drift-detection
title: 用户授权、初始基线与调查实施路径
doc: decision
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
---

# D-001 · 初始授权与有界路径

用户 2026-11-16 明确要求：工作区2新建子目标，重点审查父目标 A 拆出子目标 B 后推进漂移却未被审计发现的原因并修正，同时考虑目标/子目标及路线图设定如何预防；在 dev 修改，修复后 PR 合 main，再发布新版本资产。若调用 Codex CLI 取证，必须手动指定 gpt-6-luna。

初始承诺为 meta 的 C1～C4，顺序 S1～S4；该原始记录保留，不随 meta 调整覆盖。父级引用为同区 Root `GOAL-001-methodology-skills-feedback-evolution` 的 R3 与成功标准1/2，Git 81913d2、meta 0.14.45；父级 D-008 允许持续反馈治理，本次不关闭 R3/Root/VP。

## 方案

1. 先查漏审机制与授权/贡献/交付链缺口；用合成反例验证，不把缺少具体材料的用户历史实例伪装成已复现。
2. 先改 canonical architecture：立项给出父级结果贡献与可追溯授权基线；路线图检查阶段结果与覆盖；变更保留前后与批准来源；审计对照直接父级、原始/有效授权及实际交付，不能只验证当前本地清单。
3. 同步 templates、prompts 00～05 与 MCP guidance；不在适配器加入第二套状态，也不修改 AD 正式命令来提示审计结论。
4. 正例涵盖合法子集、信息收集阶段和已批准变更；反例涵盖验收替代、文档漂移及只改实际实施。按生产仓门禁重采受影响的16项兼容证据，并补本问题的语义行为验证。
5. cross = self + 已配置 Grok/grok-4.7/xhigh independent。候选 v0.16.0；完整回归与证据通过后走授权的 dev/PR/main/Release 路径，保留 release Environment 人工审查规则。

## 取舍

- 只增加“审计注意漂移”一句不能提供基准、可复核产物与处置路径，未采用。
- 仅以 parent/vision_ref 结构合法判断对齐，无法捕获贡献消失或验收对象替代，未采用。
- 不强加全仓历史重建/全树全文加载；沿当前目标父链按需追溯，缺证据登记 I/finding，不伪造基线。

风险：L0 提示消费不能保证模型每次识别任意语义漂移；测试与真实运行分别陈述保证范围。原始项目实例尚缺，不据此改写历史审计 verdict。
