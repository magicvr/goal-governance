---
id: GOAL-017-on-demand-governance-context
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-03
updated: 2026-11-03
version: 0.1.0
---

# E-003 · S2 实施与可复核验证

方案 checkpoint `228bd81`（S1 冻结、结构/链接/树与父级核对、git diff --check）已创建；本条不把 checkpoint 当审计通过证据。

- canonical 新增完整指南与最小入口模板；principles/alignment/checklist/standalone 明确按需加载与 MUST。stage 生成三份消费常驻规则和 core 模板/指南，43 对一致。
- 消费常驻入口为 17 行 / 1374 UTF-8 bytes（未渲染模板），旧 Claude/Copilot 分别 32317/32300 bytes，缩减约 96%；不宣称实际 token 数。生产仓根保留维护规则。
- 28 个治理提示词/四宿主入口接入根预检后的全文加载；普通 `/commit` 便利入口保持原行为，不触发治理全文。16 份 dogfood 入口已与分发源同步。
- 两种安装器增加指南/入口模板完整性检查；Copilot 改用受管块合并。update 识别旧整文件的准确渲染，dry-run 不预先写入；在备份后迁移，失败恢复 AGENTS/Copilot 原字节与新添指南缺失状态。
- MCP 薄壳与 role guidance 同步最小按需加载，不增加 lifecycle 的写路径；缺指南时宿主按 guidance 停止并补装 core，不声称服务器硬拦截。
- 可核对结果：Skills 全部 103 tests OK，docs 76 tests OK；迁移/merge/update/standalone 50 tests OK（含新增 8 个按需/真实新装/重复安装/长块与整文件升级/碰撞/回滚/打包测试）；focused stage/pack/orchestrator 65 tests OK（1 平台跳过）。实际日志在本目标 attachments 的 s2-*.txt。
- 仍未满足发布门禁：改变 behaviorSources 后旧 v0.13.8 运行证据过期，S3/S4 必须重新捕获；尚无独立审计结论、未 PR/tag/发布。I-003/I-004 不标 verified。

S2 已完成；S3 进行中，active / 50%（2/4）。Root progress 67% 不变。后续交叉审计使用用户指定 Grok Build CLI（Grok 4.7 / xhigh），干净会话，仅正式命令。
