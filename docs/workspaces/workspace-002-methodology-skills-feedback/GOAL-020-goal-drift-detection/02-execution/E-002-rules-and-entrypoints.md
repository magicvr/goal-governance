---
id: E-002
goal: GOAL-020-goal-drift-detection
title: 根因确认与GD规则、模板和消费入口实施
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
---

# E-002 · S1/S2结果

已将源码缺口及推断边界写入 [root-cause.md](../attachments/root-cause.md)。原始实例仍未知；本次确认协议缺口，未改写历史审计。

canonical principles 新增 GD-01～GD-08，guide/alignment/AGENTS摘要引用；模板与 prompts00～05覆盖贡献/授权基线、路线图结果覆盖、授权变更、实际交付核对、A对照及required门禁。MCP govern/audit guidance同步，未改参数/schema或状态写入权限。显著漂移不因本地全绿通过；合法阶段子集/调查/已批准演进保留。

Skills113项、docs76项通过；新增5项静态契约回归，明确不冒充语义分类器。stage44对一致。八种合成夹具的本地样例均退出0，包括三个故意偏离的反例；尚须读真实宿主A意见证明语义结果。

首批Codex/gpt-6-luna调用exit0但未落盘，其中两个把合成仓可选Grok派发配置误用于直接审计而停止；一个在聊天识别实施偏离但无正式A。保留实际结果，不作为通过。为排除与本次语义无关的派发默认干扰，合成直接审计夹具改为仅governance_root配置；生产仓项目配置及正式Grok审计不变。后续调用须重采本版本harness来源。

S1/S2完成，I-001 verified；S3行为/兼容证据与cross进行中。尚未PR或发布。
