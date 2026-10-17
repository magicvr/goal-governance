---
title: S1 契约与宿主能力核对证据
status: active
created: 2026-10-16
updated: 2026-10-16
parent: GOAL-013-audit-dispatch-and-user-input-gates
version: 0.1.0
---

# S1 契约与宿主能力核对

## 核对范围和证据等级

焦点为 `[workspace-002-methodology-skills-feedback] GOAL-013-audit-dispatch-and-user-input-gates`。本附件记录调查事实与已知缺口，不是正式 independent 意见，不证明实现通过。未使用其他工作区目标事实作为本次判断依据。

源码快照见 [37 个文件的 SHA-256 清单](s1-source-manifest-2026-10-16.json)，本机版本与当前 Codex 工具声明见 [宿主观察](s1-host-observation-2026-10-16.json)。源码哈希仅固定本轮读取版本，不替代 runtime evidence。

## 审计派发现状

| 位置 | 可核对事实 | 对本目标的含义 |
|------|------------|----------------|
| `skills/prompts/00-govern-orchestrator.md:171`～185 | 风险模式与 provider 由 prompt 定义；provider 失败不满足门禁 | 已有职责隔离，无命令白名单与编号解析契约 |
| `skills/prompts/06-vision-orchestrator.md:202` | 允许另开会话用 `/vision-audit` | 有入口分离，无自动调用载荷限制 |
| `skills/prompts/05-independent-audit.md:44`～60 | 输入含目标、scope、audit_type、关注点；先读区与目标台账 | 两个数字不能仅靠现有输入模板确定性解析 |
| `skills/prompts/07-independent-vision-review.md:42`～52 | 输入含 scope、VP/VRev/finding 等关注对象 | 仅 VP 数字的匹配和自主定范围尚无明确规则 |
| `skills/install/{claude,grok,codex}/skills/{audit,vision-audit}/SKILL.md` | `argument-hint` 与执行段接受 scope/关注点 | 应区分人类直接表达意图与编排器自动派发；禁止后者附加范围 |
| `skills/install/copilot/prompts/audit.md:38`、`vision-audit.md:35` | 同样把附言视为 scope/关注对象 | Copilot 也在影响面内 |
| `mcp/entries.py:62`～80、`mcp/server.py:245`～288 | MCP audit 需要 task/goal_id、可选 scope；vision-audit 需要 task、可选 scope；server 返回角色与提示词路径，不启动审计模型、不写 Goal 状态 | MCP 是入口元数据分发，不是供应商进程管理器；现有 schema 不等于自动派发白名单 |
| `mcp/config.py:73`～130 | 已有治理根安全解析、canonical/legacy 布局检测；没有 Goal/VP 数字解析 | 规范化必须先定位真实 ID，数字只是入口选择器 |
| `scripts/capture_runtime_evidence.py:433` | subprocess 调用用于 runtime 探针采集 | 不是正式审计供应商统一派发入口，不能误作已有全局拦截点 |

结论：检索的生产代码没有统一 provider runner；当前主要保证是协议、prompt 与 host wrapper 的规范约束。单纯新增测试或正则只能验证受测路径，不能阻止编排器在别处发送自由文本。

## 编号与身份边界

`docs/architecture/workspace-protocol.md` §2.6（44～58 行）要求实际身份仍为 workspace.md.id + 完整 goal id；跨区不能仅用目录序号当身份。命令数字可以作为检索选择器，但解析后必须恢复 Q1 双字段，文档/对话仍按 Q2/Q3，不能将 `/audit 002 013` 本身当持久身份。

本区目录与 meta 可核对到 GOAL-013；S1 没有改变磁盘 ID、parent 或工作区绑定。多候选、元信息不符、越界、旧布局/混合布局、目标树不一致时都不能猜测目标。

## 四宿主询问能力

| 宿主 | 本机 / 本会话观察 | 官方或当前工具依据 | 已证实的边界 | 尚未证实 |
|------|-------------------|--------------------|--------------|----------|
| Claude Code | `claude --version` = 2.1.301 | [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input) 的 AskUserQuestion 输入与 response format；[CLI reference](https://code.claude.com/docs/en/cli-reference) 的 print 模式 | SDK 有 AskUserQuestion；answers 按问题文本映射用户选择/自由输入；UI 与收集由调用方实现；print 是非交互模式 | 当前本机 UI 的取消/空返回 payload、是否带 SDK 回调的实际行为；不能把权限批准当信息答复 |
| Grok Build | `grok --version` = 1.0.60 (01a8e1c591c0) | [官方 question card 文档](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/03-keyboard-shortcuts.md) Blocking cards / Question card；[Headless mode](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/14-headless-mode.md) | TUI 的 ask_user_question 卡片等待用户；官方同时说明 Shift+X 可关闭问题并让代理无答复继续，因此必须在返回后设置治理层门禁 | 当前版本的 exact payload、headless 的问题响应、实际恢复过程；main 分支文档不是本机版本的 UI 运行证明 |
| Copilot CLI | npm 包 @github/copilot = 1.0.71；探索时帮助探针遇 bundled extraction EPERM，主线程未重试 | [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) 的 ask_user 和 --no-ask-user | 官方存在 ask_user，且可被禁用；包版本不是该工具在当前安装可运行的证据 | 本机运行帮助/schema、卡片取消/空返回、非交互回传及恢复；不将本机故障写成产品不支持 |
| Codex 当前会话 | 当前暴露 functions.request_user_input 与 functions.request_user_input_async | 本会话工具声明；[OpenAI async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling) 的应用自定义询问工具说明 | 同步工具声明等待响应；异步工具立即返回，不能代替同步等待；可用性和允许用途受宿主/模式约束 | 本轮尚未做空答复实验；本会话工具声明不代表所有 Codex CLI/App 模式。官方配置页未提供精确同步空返回契约 |

以上官方页面由主线程实际打开核对，日期 2026-10-16；这里只摘要与本目标相关的行为，不将网页示例当作本机运行事实。OpenAI 官方说明中的异步示例不是本会话工具实现。

## 治理层必须补的行为

1. 工具成功返回、卡片关闭、SDK allow、进程 exit 0 均不自动证明用户答复存在。必须对应原问题检查真实提交内容。
2. 空对象、空列表、空白串、缺少本问题、cancel/dismiss/timeout、未提交预选、仅工具展示回执都不能补成默认答复。部分答复只解决已答问题，其余继续等待。
3. 同步工具不可用或不允许用于该问题时，文本提问并停止；不得用异步问完继续推进来模拟“阻塞”。
4. 有目标时由有权的治理编排侧记录问题、原因和恢复条件，并更新 meta、执行事实、goal-tree；无目标则保留任务待答状态。审计员若遇问题，不得借此违反只写意见的状态边界，应返回待答事实给编排侧处理。
5. Goal 已 done/cancelled、只读角色或写盘失败等边界不能偷偷 reopen、改状态或清空既有阻塞。无法写 blocked 时仍必须停止任务并报告记录未完成，不能假装已持久阻塞。
6. 有卡片不表示 headless 有可用交互；没有人能回答时，停止并返回待答问题，不能使用自动选择、伪造 stdin 或提示词中的代答。

## 验证基线与后续证据

本轮执行 `python -m unittest docs.tests.test_file_l1 skills.tests.test_mcp_l1 docs.tests.test_dual_channel_l2 -q`：32 tests，OK。既有 subprocess 测试出现 ResourceWarning（文件句柄未关闭），未导致失败。本轮没有修复这些外围警告。

这些测试仅支持现有入口、MCP 元数据和通道边界的基线；未验证本目标的新命令解析或问答门禁。相关落点：`docs/tests/test_file_l1.py:48`，`skills/tests/test_mcp_l1.py:156`，`docs/tests/test_dual_channel_l2.py:85`，`skills/tests/test_skills_orchestrator.py`。

`scripts/capture_runtime_evidence.py:318`～350 会重算 behaviorSources。例 `docs/releases/runtime/v0.13.4/grok-build-cli-audit-2026-10-01.json:18`～26 固定了 AGENTS.md 和 00 prompt 的哈希；变更后相应旧证据过期，不能更新日期/哈希来冒充重捕获。现有 marker 探针不覆盖卡片行为；S3 应分别记录入口重捕获和问答验证，不要求本目标未经授权发布 tag/Release。

## 调查提交时的待裁决与后续响应

方案与规则形状见 [D-002 提案](../01-decision/D-002-s1-contract-proposal.md)。自动输入命令化与缺答即停是用户已指定要求；当时待裁决的是实施路径及 provider，不把它们反写成原始需求存在歧义。随后用户通过同步卡片采纳 A 并指定 Grok Build，见 [D-003](../01-decision/D-003-s1-freeze-and-grok-provider.md)。S1 在真实答复留痕后完成，未因只完成调查就自动冻结。
