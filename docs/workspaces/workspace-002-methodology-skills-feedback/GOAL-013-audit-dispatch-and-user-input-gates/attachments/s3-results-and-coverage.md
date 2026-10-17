---
title: S3 运行证据与验收覆盖
status: active
created: 2026-10-17
updated: 2026-10-17
parent: GOAL-013-audit-dispatch-and-user-input-gates
version: 0.2.0
---

# S3 运行证据与验收覆盖

本记录是执行事实及缺口清单，不是正式 self/independent 审计。S1 冻结计划不改写；路径 A 是规则与现有入口规范化，不提供不可绕过的代码解析器。静态规则、合成宿主运行、真实界面操作、真实用户答复分别计证。

## 当前入口证据

三宿主 × 四入口共 12 格，Claude Code 2.1.301、Grok Build 1.0.60（01a8e1c591c0）、GitHub Copilot CLI 1.0.75；另有四宿主只读目录角色探针（Codex CLI 0.163.0）。[当前目录](../../../../releases/runtime/goal-013-s3-2026-10-17-current/) 共 16 个 producer envelope，全部 exit 0 / pass，来源和 stdout/stderr 摘要一致。兼容矩阵引用其中 12 格，CI 一致性门禁检查 16 份。

初轮捕获时间为 UTC 2026-10-16 16:32～16:52，上海日期为 2026-10-17；恢复后的新入口取证使用 2026-10-17 UTC 时间，原时间均保留。12 格文件加日期后缀只移动文件名，不改变内容；11 份此前有效 envelope 的路径迁移保留原捕获时间、来源摘要和原输出，分别见 `s3-evidence-relocation-2026-10-17.json`、`s3-evidence-filename-relocation-2026-10-17.json`。旧目录、失败和超时记录保留，不重算旧哈希冒充通过。

测试驱动为 [s3-host-probes.py](s3-host-probes.py)，不属于生产 runner。每次建立合成消费仓和新会话，仅安装发货规则、入口与合成目标/代码。审计输入文件严格只有 `/audit 002 013` 或 `/vision-audit 002`，不附加 marker、scope、预期 finding 或生产工作区历史。宿主服务仍使用各自现行供应商配置，不宣称 OS 级完全隔离。合成 A/VRev 的 verdict 不属于生产 GOAL-013。

四个目录探针先实际启动本地 MCP stdio 并调用四工具，再由宿主读取实际目录结果判断入口角色；它们不证明原生宿主 MCP 自动连接，也不扩大 Codex 的矩阵支持承诺。Codex 默认模型与账户不兼容，单次使用 `gpt-6.1-sol` 覆盖后成功，用户配置未修改。

## 发现与修正

| 实测偏差 | 修正与复测 | 边界 |
|----------|------------|------|
| Claude wait03 只在聊天停下，Goal 仍 active | canonical 与全部入口明确待答持久化是已授权暂停收尾、无需另次确认；wait04 写 blocked、E-001、执行索引和树，counter 未变 | headless 文本路径，非卡片答复 |
| Grok audit-c08 新旧布局冲突后仍审目标并写 A | core05 和四宿主 audit 明确解析失败即返回、不读 Goal 正文/分配 A；c08-fixed 无改动、无 Goal 正文 read_file | 混合布局一例，不代替全部非法路径组合 |
| Copilot audit 额外创建非审计目录 .gitkeep | 收紧 Copilot audit 写边界；final-r2 仅 A 与索引 | 不修复合成仓其他目录 |

## 22 条用例的证据与剩余范围

“部分”表示仍不能把整条标记为通过；未覆盖变体继续归 I-004。

| 用例 | 已有证据 | 结论 / 剩余范围 |
|------|----------|------------------|
| C01 | 当前三宿主 audit：纯命令、唯一合成身份、A + 索引，发现 counter 误计空白 | 入口运行已覆盖 |
| C02 | workspace-protocol §2.7 与 core05 规范数字匹配；静态契约回归 | 无新增代码解析器；未做不补零的实际宿主变体 |
| C03 | 当前三宿主 vision-audit：纯命令、VRev + 索引、无 Goal 状态写入 | 入口运行已覆盖 |
| C04 | AD-01～06 / 静态反例；实际 input.txt 无 scope/额外提示 | 路径 A 规范与本次载荷可核对，不宣称恶意附言被程序硬拦截 |
| C05 | 驱动新临时仓、新会话、argv/input/source 清单；没有复制编排历史 | 本次派发边界已核对，不证明供应商隐藏系统上下文 |
| C06 | 协议列出非法编号、包装与多行；静态契约回归 | 无新增代码路径；未逐形态运行宿主负例 |
| C07 | grok-audit-c07 重复编号；Claude missing-goal-01 零匹配；id-mismatch-r2 用字段检索发现错误身份，未读目标正文/三索引、无写入 | 所列身份负例已实测；先前 id-mismatch-01 读了索引的失败保留 |
| C08 | grok-audit-c08-fixed；Claude root-escape-r2；workspace-junction 真实 Windows junction | 所列布局/根/逃逸负例停止，无 Goal/A 写入，外部合成目录摘要未变；junction 被 Glob 排除，不能扩大为手工越界 Read 也受 OS 阻断 |
| C09 | Claude 旧配置模型错误、初轮参数失败、240 秒超时均保留；不作为审计意见、不放行 | 失败不算通过；更新配置后的成功捕获另存 |
| C10 | core05/core07 人类直调与自动入口分离；MCP 既有 task/scope schema 回归 | 角色来源契约已覆盖 |
| U01 | Grok TUI dismiss03 真实卡片展示并等待；无答案前已 blocked | 展示/等待已覆盖，真实人类提交见 U11 缺口 |
| U02 | Grok c07 非交互 AskUserQuestion 只返回“无人可答/自行判断”包装后仍停止；Copilot SDK 合成空 callback 后仍等待 | 部分；{}、[]、null 等未逐种实测；SDK profile 见下 |
| U03 | Grok TUI dismiss03 实际 Shift+X 关闭后仍 blocked，无导出 | 关闭实测；没有原始工具返回，不能声称确切 declined payload；其他取消/超时变体未穷尽 |
| U04 | 当前对话实际同步卡片：用户澄清“已有预选”；各卡片在返回前已保存待答/blocked，未据预选填答案 | 当前 Codex desktop 会话已覆盖；用户观察证据，不外推后台 CLI。Grok shortcut02 自动输入仍不计人类答复 |
| U05 | Claude wait04、Copilot wait02 在无卡片模式持久化待答并停止 | 已覆盖所列 headless 模式；不泛化到所有 UI 配置 |
| U06 | 第一张多题卡片收到 JSON 及“后台 CLI 不可见、无法验证”反馈，未把反馈填成预选状态；逐题保存后换行符仍 open，快照保持 blocked | 实际部分信息/不匹配观察的处理已覆盖；逐题问答不伪称同一张卡片只返回半个 payload |
| U07 | Claude wait-u07；当前对话真实 JSON/LF 提交后，合成 I-001/I-002 verified，B-001 仍开放、Goal/tree blocked，counter 不变 | 实际来源与只解除相应未知项已覆盖，不自动清其他 blocker |
| U08 | Claude vp-only-r4 实际 Edit + 回读，VP 文件追加待答，status active，无 Goal | 无 Goal/只有 VP 待答已实测；r1/r2 只聊天、r3 虚称已写失败均保留 |
| U09 | Claude wait-u09 对 done、wait-cancelled-01 对 cancelled 均无修改；独立入口不改 Goal 状态 | 所列状态/角色边界已实测 |
| U10 | Claude wait-restart；readonly-fault-current 实际只读文件属性，工具多次 EPERM，原始错误另存，最终明确未持久成功并停止 | 故障/新会话读取已实测；旧 write-denied 仅无写工具，仍不计真实拒绝证据 |
| U11 | 修改后的本对话同步卡片实际返回 JSON、LF、已有预选；保存原题/回执、复核 B-001；生产待答全部解决后才恢复 active | 当前会话实际提交/门禁复核已覆盖，不直接 done，不冒充 CLI 人类输入 |
| U12 | SDK 工具 success + 空答案仍等待；Grok c07 的继续指令未被当答案；权限 trust y 未当选择 | 所列反例已覆盖，不把 exit 0 当人类答案 |

## 界面和 SDK 证据限制

[dismiss03](s3-runtime/grok-tui-dismiss-03/ui-observation.json) 保存可见卡片片段、动作与文件前后摘要；rawToolResponseCaptured=false。首次 TUI 启动未可靠绑定临时 cwd，立即取消且无生产文件修改，记在 `grok-tui-cancel/isolation-failure.json`，排除验收。后续均使用宿主可见临时仓和显式 `--cwd`；自有 TUI 已退出。

[shortcut02](s3-runtime/grok-tui-cancel-02/ui-shortcut-observation.json) 的按键是自动化注入，确实提交了 JSON，不能当作真实用户选择。它仅属于合成试验，不影响本目标决策。

Copilot SDK empty 使用本地 SDK runtime 1.0.71，实际模型 gpt-5-mini，未加载当前 File govern/core；不是正式 CLI 1.0.75 包行为证明。它只说明该 SDK callback 的空 answer 可以与 tool success 同时出现、随后 agent 等待。不能填平当前发货入口或真实 UI 的缺口。

## 阶段结论

入口证据刷新、实际偏差整改、回归及当前会话真实交互完成，按 D-003 路径 A 的保证范围，I-004 verified，S3 完成；S4 未开始。22 条用例逐项保留证据层和未逐形态/跨版本扩大的限制，不把静态规范称为程序硬拦截。没有新增 required 信息缺口或 residual 接受；矩阵 ready 不是正式审计通过或发行授权。

## 恢复后的补证（2026-10-17）

用户要求继续后，E-006 未展示的安排题撤回，见 E-007。增加配置预检、身份 frontmatter 分阶段读取，以及无 Goal 待答实际写入/回读的操作指令，不改变架构既有 fail-closed/真实事实原则。全部四宿主入口及 core00/05/06/07 同步；更新源后的 16 份当前捕获位于本页所链 current 目录，旧 ready/r2 等保持历史。四份未受末轮改动影响的有效捕获只迁移原输出路径，见 s3-current-relocation.json，不改时间、来源或输出摘要。

详见 [负例逐次记录](s3-resumed-negative-results.json)。Claude audit-r4 错误报告目录不存在；r5 把临时仓名的下划线误写成连字符，实际 Read 被拒，未假装审计完成。这两次失败保留。驱动改用较短的十六进制临时仓名后，r6 完成正式入口和 A + 索引；不宣称已消除模型所有路径误写。合成 VP 表最初误用 lead 角色，已改为 primary；由此暂停的 vision-audit-r2 保留为 fixture 故障，修正后新会话成功。

readonly-fault-current/actual-filesystem-errors.json 保留来自原始 tool_result 的 EPERM 文本；过滤不保存普通工具内容或 provider 推理。新增生产仓契约回归测试依赖根 mcp，pack 排除该文件，避免 File-only 分发出现缺失 mcp 的测试导入。

## 真实卡片收尾与 S3 判定

[E-008](../02-execution/E-008-s3-real-card-interaction.md) 及 codex-wait-actual-card-current 的三份 card-answer 回执为本轮真实人类提交：JSON、LF、对本对话卡片的“已有预选”观察。第一份可见性反馈完整保留，并经限定当前卡片的补充提问澄清，不推定后台 CLI 可见。问题等待期间只保存暂停事实，提交后才填答案；中间部分信息和最后 B-001 保持 blocked 的摘要保留。

验收适用性：C02/C06 没有本包新增的代码解析器，按冻结计划以规范核对；C04/C05 核对实际派发载荷和干净会话，不为负例向审计员发送违规自编提示。U02 各种空字面形式未逐形态走完所有 GUI；本包没有独立答复解析 API，保证来自 UI-02 规范、实际无答案/关闭/空 callback 的代表记录与当前会话答复核对，不把 SDK profile 当作当前 File CLI 全覆盖。未支持或未运行的 UI/API 形态不被写成已实测；保留字段而不删例。S3 证明路径 A 的当前规范、入口、已列运行模式及门禁处理，不能承诺任意供应商/版本永不误读。新增控制、返回模式或实际偏差需重新取证；这是 D-003 已选保证范围，不是新增 residual 接受。
