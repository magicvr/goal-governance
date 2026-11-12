---
id: GOAL-018-host-wait-and-audit-config
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-12
updated: 2026-11-12
version: 0.1.0
---

# D-002 · 宿主等待与审计项目配置契约冻结

S1 信息核验完成，采用如下契约推进 S2/S3：

1. 同步卡片实际调用并等待；无法持续挂起时组合宿主原生目标停止能力，严格遵守工具契约。Codex 的原生 blocked 有连续阻塞阈值、paused 需明确用户请求；不能用通用规则越过这些限制。没有合法能力时文本提问、停止本轮并如实提示用户原生暂停/中断，不宣称宿主已拦截。
2. 询问不自动改变治理 GOAL 的 blocked/active，不写暂停流水、执行索引/目标树/父级投影，不为了等待新造/组合治理或原生目标。会话保留原题和返回即可；真实决定、信息变化、实际交付阻塞仍按正常规则记载。
3. 项目可提交 independent_audit = {provider, model, reasoning_effort}；当前登记 Grok / grok-4.7 / xhigh，沿用 D-001 所引用户指定。显式会话完整覆盖优先于项目默认；合法默认跨会话复用，缺失才问。类型、枚举、字段和参数边界校验，非法/CLI失败不静默替换；安装升级字节保留。
4. MCP 读取并返回项目默认及来源，仍只读、不执行 CLI。File 入口按相同字段契约消费，不依赖 MCP 部署。配置与 CLI 参数映射有实现测试；不将模型名混进自动审计正文，正文仍只用正式命令。
5. 新版本候选 v0.15.0；新增配置不改变五件套、工作区、四入口及协议 0.1.0 的数据结构。producer 16格代表入口/台账运行证据需重采集；另做无人答复下不越过实施、不额外改治理状态的代表运行。证据明确区分 headless 退出与原生 /goal 挂起，未验证 UI 不声称通过。

依据：

- [Codex Using Goals](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)：目标为会话持久状态，/goal pause 由用户控制；实际工具定义提供 get_goal/update_goal 与 blocked/paused 前置条件。
- [Grok Modes and Commands](https://docs.x.ai/build/modes-and-commands)：/goal 跨轮持续，提供 pause/resume；[headless](https://docs.x.ai/build/cli/headless-scripting)未确立交互卡片挂起原生目标的普遍保证。
- [Claude CLI](https://code.claude.com/docs/en/cli-reference)与[交互模式](https://code.claude.com/docs/en/interactive-mode)：交互/print 和中断能力；未核实同名 /goal，不能照搬。
- 本地 mcp/config.py、schema、宿主入口与 GOAL-017 D-002 已核对；真实 CLI 版本见 E-001。S3 运行结果在取得后登记，不在此预写通过。

本轮用户已授权整改及发布；上述为范围内实现选择，不新增需用户裁决的 residual/overruled 或模式降级。保证等级 L0。
