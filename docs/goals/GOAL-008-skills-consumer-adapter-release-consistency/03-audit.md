---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: audit
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 1.0.0
---

# 审计 · GOAL-008

## 信息就绪核对

| ID | 级别 | 状态 | 影响门禁 | 当前证据 | 结论 |
|----|------|------|----------|----------|------|
| I-001 | required | verified | 方案与发布范围冻结 | [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；[A-002](#a-002--i-001-契约实现与验证复审2026-07-19) | 已创建 canonical schema/manifest、镜像、正反 fixtures 与安装/bootstrapping 契约测试；此门禁已通过 |
| I-002 | required | deferred | 受影响实施与兼容验收 | [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)、[D-004](01-decision.md#d-004--当前最低可用基线与发布一致性延期2026-07-19)；[runtime fixture 结果](attachments/i-002-runtime-fixture-2026-07-19.md) | Claude `2.1.215`、Grok `0.2.103` 与 Copilot VS Code `1.129.1` / `copilot-chat 0.57.0` 都已有 current `/govern` 可观察 dispatch，三条 adapter 为 `verified`；完整矩阵、其他入口与兼容验收延期至首次支持新宿主/版本或首次对外/可复现发布 |
| I-003 | required | deferred | 阶段 5 发布验收、F-005 关闭和阶段 7 输入 | [D-004](01-decision.md#d-004--当前最低可用基线与发布一致性延期2026-07-19)；当前尚无 release tag 和可重放发行证据 | 延期至首次对外/可复现发布；在触发前不可通过阶段 5 发布验收 |

当前没有用户接受的 residual risk；`deferred required` 不等同于 `verified`，在复核触发或受影响门禁到达时按开放 required 处理。

## 上游审计意见与开放门禁

以下意见属于 GOAL-001 的阶段 5 立项审计范围，本目标只引用其门禁，不重新编号或冒充新的独立审计：

| 上游意见 | source | verdict | 相关状态 |
|----------|--------|---------|----------|
| [A-006](../GOAL-001-main-vision/03-audit.md) | independent | conditional | `F-005 open / required`；`F-006 open / recommended` |
| [A-007](../GOAL-001-main-vision/03-audit.md) | self | conditional | 与 A-006 同向确认开放门禁 |
| [A-008](../GOAL-001-main-vision/03-audit.md#a-008--合并响应-a-006--a-007-与阶段-5-立项门禁2026-07-19) | self | conditional | 允许立项；I-001～I-003 collecting，F-005 仍开放必改 |
| [A-009](../GOAL-001-main-vision/03-audit.md) | self | conditional | 当前最低可用范围通过；F-005 与 I-002 / I-003 保持 `deferred required`，不关门 |

## 阶段性复盘

### 成果

- 已按 D-010 建立 GOAL-008 五件套、信息台账和路线图。
- 已将上游的范围边界、开放 required 门禁和非阻断 recommended 项写入本目标可追踪记录。
- 已收集并审视 I-001 的 SemVer、JSON Schema 和行为测试实践，形成 D-002 与可核对的 [调研附件](attachments/i-001-industry-practice-research-2026-07-19.md)。
- 已实现 D-002 的 canonical schema/manifest、Skills 镜像、正反 fixtures 与安装/standalone bootstrap 断言，并以 A-002 复审 I-001。
- 已收集 I-002 的仓库安装/解析证据与宿主公开资料，形成 [I-002 宿主与契约证据](attachments/i-002-host-compatibility-evidence-2026-07-19.md)；D-003 已据此冻结 `0.1.0` 首个基线、无上一版本、三宿主的声明/承诺层级及 Web 只读边界，但未越过宿主运行时证据边界。
- 已执行并补齐 [版本固定 runtime fixture](attachments/i-002-runtime-fixture-2026-07-19.md)：Claude Code `2.1.215`、Grok Build `0.2.103` 与 Copilot VS Code `1.129.1` / built-in `copilot-chat 0.57.0` 的实际 `/govern` dispatch 均有归档证据；Web 20 项解析测试通过、1 项 Windows symlink 测试跳过。

### 偏差与注意点

- 本次已实施 I-001 协议契约及其测试、完成 I-002 初始范围冻结并取得三宿主的 `/govern` current 运行时证据；这仍不是 `/audit`、manifest 解析、完整矩阵、CI 或发行演练。用户已将这些发布一致性工作记录为 `deferred required`，未将其关闭。
- 目标为 `active / 20%`；I-001 已通过，不得把该局部门禁通过写成跨宿主兼容验收、阶段 5 实施完成或发布范围已全面冻结。

### 建议

- 当前不扩展未覆盖入口、自动化重放或发布演练；首次支持新宿主/版本或首次对外/可复现发布时，先复核 I-002，再恢复相应的兼容性收集。
- 首次对外/可复现发布前，形成 I-003 所需的可重放 CI、报告、变更日志与 tag/release 证据，并邀请阶段审计复核 `F-005`。

## 审计结论

> A-001～A-007 是按时间追加的历史审视；其中的 `collecting`、`open / required` 表示各自审计时点。当前状态以本文件顶部信息台账和 [A-008](#a-008--当前最低可用裁决与发布一致性延期响应2026-07-19) 为准。

## A-001 · I-001 行业实践收集与方案前审视（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：stage / 阶段 A 的 I-001 位置、字段与兼容语义；不审 I-002 矩阵、I-003 发行证据或 schema 实现。
- **verdict**：conditional

### 范围与区间

审视覆盖用户要求的公开行业实践调研、D-002 设计取舍以及该取舍相对 I-001 门禁的充分性。

### 成果（有证据）

- [调研附件](attachments/i-001-industry-practice-research-2026-07-19.md) 保留了三个权威来源、关键规范含义和最小声明模型。
- [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19) 已确定 single canonical source、schema 标识、业务版本字段、兼容区间和 I-002/I-003 的范围边界。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 唯一机读协议/模板版本与兼容声明 | 部分 | 位置和字段已决定；schema/manifest 与验证尚未实现。 |
| 兼容矩阵与上一版本支持范围 | 未开始 | 属于 I-002。 |
| 跨宿主/跨版本 fixtures 与消费测试 | 未开始 | 尚未创建。 |
| CI 漂移校验、报告与发行物身份 | 未开始 | 属于后续 I-003 / 阶段 C。 |
| tag/release 或等价演练 | 未开始 | 属于 I-003 / 阶段 D。 |

### Findings

本次没有新增本目标范围的 F-00N。已继承且仍相关的必改项是 [GOAL-001 F-005](../GOAL-001-main-vision/03-audit.md)：它保持 `open / required`。I-001 仍是 `required / collecting`，不能把设计决定误写为验证完成。

### 必改项汇总

- `GOAL-001 F-005`：`open / required`；继续阻断阶段 5 发布验收及其上游关门门禁。
- `I-001`：`required / collecting`；继续阻断阶段 5 方案与发布范围冻结，直到 D-002 被 schema、fixtures 和适配器契约测试证实。

### 结论 + 建议下一步

I-001 的未知已收敛为可实施的单一契约方案，但尚不具备放行证据。下一步应实现 D-002 的 canonical schema/manifest 与镜像同步，并以正反例和适配器契约测试复审 I-001；在完成前不得冻结范围。

## A-002 · I-001 契约实现与验证复审（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：stage / D-002 的 canonical schema/manifest、镜像同步、正反 fixtures 与安装分发证据；仅核对 I-001。
- **verdict**：pass

### 范围与区间

本次仅复审 I-001 所影响的方案与发布范围冻结门禁。I-002 的实际支持矩阵和 I-003 的发行证据不在 scope 内，仍按各自 required 门禁保持开放。

### 成果（有证据）

- `docs/contracts/skills-consumer-contract.schema.json` 定义 JSON Schema 2020-12 dialect、canonical `$id`、manifest 字段、SemVer 范围和 `I-002-pending` 状态约束；`docs/contracts/skills-consumer-contract.json` 是唯一 canonical 声明。
- `skills/contracts/` 是逐字节镜像；`skills/install.ps1`、`skills/install.sh` 的 `-All/--all` 路径复制该目录；[docs/README.md](../../README.md) 保留 schema/manifest 的 SHA-256 台账。
- 正反 fixtures、29 项 Skills 契约测试、3 项 standalone bootstrap 测试、PowerShell 与 Git Bash 安装脚本语法检查均在本次执行中通过，具体命令和结果见 [02-execution.md](02-execution.md)。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 唯一机读协议/模板版本与兼容声明 | 已完成 | canonical schema/manifest、镜像、正反 fixtures 与安装断言。 |
| 兼容矩阵与上一版本支持范围 | 未开始 | I-002，不在本次 scope。 |
| 跨宿主/跨版本 fixtures 与消费测试 | 未开始 | I-002，不在本次 scope。 |
| CI 漂移校验、报告与发行物身份 | 未开始 | I-003 / 阶段 C。 |
| tag/release 或等价演练 | 未开始 | I-003 / 阶段 D。 |

### Findings

本次 scope 内没有开放 required finding。I-001 已由上述实现与证据关闭。`GOAL-001 F-005` 仍为 `open / required`，但它约束阶段 5 发布验收，不否定本次 I-001 局部门禁的 `pass`。

### 必改项汇总

- I-001：`verified`；方案与发布范围冻结门禁已具备该项所需证据。
- I-002：`required / collecting`；仍阻断受影响实施。
- I-003 与 `GOAL-001 F-005`：仍分别阻断阶段 5 发布验收及上游关门。

### 结论 + 建议下一步

I-001 可放行其影响的方案与发布范围冻结门禁；这不是对 I-002 实施或 I-003 验收的放行。下一步用 `/govern GOAL-008，先收集并审视 I-002` 继续阶段 A。

## A-003 · I-002 宿主兼容证据收集与阶段审视（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：stage / I-002 的三类宿主 wrapper、Web 只读解析器、当前/上一协议版本边界，以及兼容矩阵与 fixtures 的可验证范围；不审 I-003 发布证据。
- **verdict**：conditional

### 范围与边界

本次审视只评估“已证明什么、尚缺什么”。安装脚本、Markdown wrapper 和本地 Web 测试属于仓库产物或本地消费者证据；它们不等同于外部宿主已经在某个产品版本中发现并执行相同语义。

### 成果（有证据）

- [证据附件](attachments/i-002-host-compatibility-evidence-2026-07-19.md) 汇总了仓库路径、公开来源、访问日期、关键事实和来源限制。
- Claude Code 的官方 Skills 文档支持 project skill 的 `.claude/skills/<skill-name>/SKILL.md` 位置；GitHub Copilot 的官方文档支持 `.github/copilot-instructions.md`、`AGENTS.md` 与 `.github/prompts/*.prompt.md`，但 prompt files 仍为仅限指定 IDE 的 public preview。
- Web 具有可运行的本地只读解析/渲染测试；当前 contract manifest 仍为 `adapterCompatibilityStatus: I-002-pending`，没有任何 adapter 被声明或验证。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 明确三类宿主/wrapper 与 Web 的候选矩阵行 | 部分 | 仓库安装面、Web 解析器与一手资料已登记；Grok Build 的官方宿主资料仍缺失 |
| 明确当前及上一协议版本支持范围 | 未完成 | 当前仅有 `0.1.0`；不存在可追溯的上一协议产物，策略待裁决 |
| 当前/上一版本 fixtures 与跨宿主测试 | 未开始 | 已给出 fixture 类别和真实运行时证据要求，未实施或执行 |
| 区分已验证与未覆盖范围 | 已完成（本次 scope） | 附件和本条审视均将结构/安装/Web 测试与外部宿主运行时证据分开 |

### Findings

本次未新增 GOAL-008 范围内的 F-00N。以下是 I-002 本身仍待关闭的 required 信息，不能被本轮资料替代：目标宿主及其实际版本基线、上一协议版本策略、Grok Build 的可核对发现语义，以及每个候选矩阵单元的真实运行时验证结果。

### 必改项汇总

- I-002：`required / collecting`，继续阻断受影响实施与兼容验收。
- I-003 与 `GOAL-001 F-005`：保持开放，继续阻断阶段 5 发布验收及上游关门。

### 结论 + 建议下一步

资料收集已足以提出可审计的矩阵设计，但不足以冻结支持承诺。建议由用户先裁决：`0.1.0` 是否作为首个支持基线且“上一版本”为无、哪些 Claude/Copilot/Grok 版本或环境纳入承诺、以及 Web 是否必须直接消费 manifest；随后再以 D-003 固化边界并实施 fixtures/运行时测试。

## A-004 · Grok Build 仓库 Skills 证据更正复核（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：ad-hoc / 用户提供的 xAI Grok Build 公告及官方 Skills 文档是否证明本仓库 `.grok/skills/` 的发现与 user-invocable slash-command 语义；不审固定 release 的运行时兼容。
- **verdict**：pass

### 范围与边界

本条仅更正 A-003 中“未取得 Grok Build 官方发现资料”的证据缺口。它确认 source-level discovery capability，不把一手产品文档误写成已对本仓库、固定 Grok Build 版本和具体协议 fixture 完成端到端验证。

### 成果（有证据）

- [Introducing Grok Build](https://x.ai/news/grok-build-cli) 宣布 Grok Build CLI，并说明 `AGENTS.md`、plugins、hooks、skills 和 MCP servers “work out of the box”。
- [Grok Build Skills, Plugins & Marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces) 明确列出 `./.grok/skills/` 会向上遍历至 repo root，且 user-invocable skills 出现为 `/<skill-name>` 斜杠命令；同页说明 Grok 读取从 cwd 到 repo root 的 `AGENTS.md`。
- 本仓库的 `skills/install/grok/skills/govern/SKILL.md` 和 `audit/SKILL.md` 均位于该官方项目 skills 根下，且使用 user-invocable skill 形态；因此“Grok Build 缺乏官方发现语义”的 A-003 子结论被本条取代。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 官方证明仓库内 Grok skills 的发现路径 | 已完成 | `./.grok/skills/` 向 repo root 遍历 |
| 官方证明 user-invocable skills 的 slash-command 行为 | 已完成 | `/<skill-name>` 说明 |
| 本包在固定 Grok Build release 中运行并消费 `0.1.0` contract | 未开始 | 仍需版本、环境、fixture 与实际运行记录 |

### Findings

本次没有新增 F-00N。A-003 中关于 Grok Build 官方发现资料缺失的表述已被本条和 [I-002 证据附件](attachments/i-002-host-compatibility-evidence-2026-07-19.md) 更正；I-002 的剩余 required 信息是实际 release 基线、协议前一版本策略和跨宿主运行时验证，而不是发现路径本身。

### 必改项汇总

- I-002：保持 `required / collecting`，因为 source-level capability 不等于 `consumer-verified`。
- I-003 与 `GOAL-001 F-005`：保持开放，未受本条影响。

### 结论 + 建议下一步

Grok Build 应继续作为 I-002 候选矩阵行，而非“无官方支持资料”的未知项。建议 D-003 为 Grok 行指定目标 Grok Build release/环境以及 current/previous/negative fixtures，再执行真实 `grok` 调用验证；在此之前不把 manifest 的 `I-002-pending` 改为已验证适配器。

## A-005 · D-003 I-002 范围冻结响应复核（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：response / 响应 A-003、A-004 中关于首个/上一协议、Grok Build 声明范围、宿主承诺层级与 Web 消费边界的裁决；不审精确 host release 的运行时通过、I-003 发行证据或阶段 5 关门。
- **verdict**：conditional

### 范围与区间

本条复核用户的 D-003 已被写入决策、信息台账与 canonical 契约，且不把范围冻结误写为外部宿主的运行时验收。审视涵盖 `0.1.0` 首个基线、无上一版本、三条 adapter 记录及 Web 只读解析器排除；不涵盖尚未执行的 current/negative runtime fixture。

### 成果（有证据）

- [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19) 保留了用户的四项书面裁决、未选方案和开放门禁。
- `docs/contracts/skills-consumer-contract.schema.json` 新增 `supportBaseline` 与 adapter `supportCommitment`；canonical manifest 声明 `firstSupportedProtocol: 0.1.0`、`previousSupportedProtocol: null`，并把 Claude Code CLI / GitHub Copilot VS Code 标为 `committed`、Grok Build CLI 标为 `declared`。
- [I-002 证据附件](attachments/i-002-host-compatibility-evidence-2026-07-19.md) 现将 declared、committed 和 verified 证据层分开，并将 Web 限定为独立的目标文档解析器。
- `python -m unittest skills/tests/test_skills_orchestrator.py -v` 通过 30 项，`python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v` 通过 3 项；9 个 contract/schema/fixture 镜像文件逐字节一致，`git diff --check` 无空白错误。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 兼容矩阵的三宿主 / Web 范围 | 部分 | D-003 已冻结三条 adapter 和 Web 非 adapter 边界；尚无精确 host release 矩阵单元。 |
| 当前及上一协议版本支持范围 | 部分 | `0.1.0` 首个基线、上一版本为 `null` 已声明；不需要伪造 previous fixture，但 current/negative runtime fixture 尚待执行。 |
| 跨宿主/跨版本 fixtures 与消费测试 | 未开始 | schema/manifest contract fixtures 不等于 Claude/Grok/Copilot 的实际产品运行。 |
| CI 漂移校验、报告与发行物身份 | 未开始 | I-003 / 阶段 C。 |
| tag/release 或等价演练 | 未开始 | I-003 / 阶段 D。 |

### Findings

本次没有新增本目标范围的 F-00N。D-003 已关闭的只是 I-002 的范围冻结子问题；I-002 作为 required 信息项仍开放，因为全部 adapter 的 `verificationStatus` 都是 `unverified`，且没有精确宿主 release、运行环境或实际 fixture 输出。

### 关闭证据与仍开放项

| finding / I-00N | 状态 | 证据 |
|-----------------|------|------|
| I-002：首个/上一协议策略 | 本 scope 已关闭 | D-003；`supportBaseline` 的 `0.1.0` / `null`。 |
| I-002：声明/承诺宿主范围 | 本 scope 已关闭 | D-003；canonical manifest 的 `claude-code-cli`、`grok-build-cli`、`github-copilot-vscode`。 |
| I-002：Web 是否为 adapter | 本 scope 已关闭 | D-003；I-002 附件的 Web 行。 |
| I-002：实际 host release / runtime fixture | open / required | 三个 adapter 均 `unverified`；尚无可重放调用证据。 |
| I-003 与 `GOAL-001 F-005` | open / required | 本次未产生 CI、发行物身份或 tag/release 证据。 |

### 必改项汇总

- I-002：`required / collecting`，仅范围冻结子问题关闭；运行时兼容验收仍被阻断。
- I-003 与 `GOAL-001 F-005`：保持 `open / required`，继续阻断阶段 5 发布验收和上游关门。

### 结论 + 建议下一步

D-003 的声明/承诺边界已可作为范围内实施输入，但不能作为 host runtime pass。下一步应为 Claude Code CLI、Grok Build CLI 和 GitHub Copilot VS Code 分别记录精确版本与环境，执行 `0.1.0` current / negative fixture；Web 只运行其目标文档解析测试。随后再以阶段审视核对 I-002 是否具备兼容验收证据。

## A-006 · I-002 版本固定 Runtime Fixture 阶段复核（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：stage / D-003 冻结范围内的 Claude Code CLI、Grok Build CLI、GitHub Copilot VS Code 与 Web 目标文档解析器的 `0.1.0` current/negative runtime evidence；不审 I-003 发布证据或阶段 5 关门。
- **verdict**：conditional

### 范围与区间

本条核对本轮是否取得精确宿主版本、安装 source、fixture 输入和实际结果，并区分 CLI 成功退出、模型的 prompt-directed 回答、provider 失败、用户人工发现和 Web parser 测试。协议首个基线为 `0.1.0`；`previousSupportedProtocol: null`，所以没有 previous fixture。

### 成果（有证据）

- [runtime fixture 结果](attachments/i-002-runtime-fixture-2026-07-19.md) 记录 Windows 11 环境、manifest/schema/installed-skill SHA-256、Claude `2.1.215`、Grok `0.2.103`、VS Code `1.129.1` 的实际信息与可重放命令。
- Claude 的 current 与 negative headless `/govern` 调用都以 `plan` 权限完成并返回预期边界文本；没有写入工作区。
- Grok current 调用到达其 Responses API，但得到 `502 Bad Gateway: unknown provider for model grok-build`；此失败被保留为阻断证据，而非被 exit code `0` 掩盖。
- 用户提供的 [Copilot VS Code Chat screenshot](attachments/copilot-vscode-govern-runtime-2026-07-19.png) 显示 `/GOVERN GOAL-008` 的实际输出；该证据仍未给出 Copilot 扩展版本。
- Web 使用仓库 `web/.venv` 的规范命令通过 20 项测试，1 项因为 Windows symlink 权限跳过；它仍不作为 manifest adapter。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 覆盖三宿主与 Web 的兼容矩阵 | 部分 | 三条 adapter 与 Web 均已有版本/事实行，但 Copilot 环境指纹和 Grok 成功运行仍缺失。 |
| 当前/上一协议 fixtures 与跨宿主消费测试 | 部分 | `0.1.0` current 与无 predecessor negative 语义已执行/记录；没有 previous fixture，Claude 输出尚非可观察 dispatch 证据，Grok 未成功执行。 |
| 区分已验证与未覆盖范围 | 已完成（本次 scope） | attachment 将 Claude probe、Grok blocked、Copilot manual-discovery、Web parser 结果与 canonical `unverified` 分开。 |
| CI 漂移校验、报告与发行物身份 | 未开始 | I-003 / 阶段 C。 |

### Findings

本次没有新增 F-00N。I-002 的 required 信息仍开放：

- Claude current/negative 的返回内容受 prompt 指定，尚缺能够观察项目 skill 实际 dispatch 的独立断言。
- Grok 的 provider 配置使实际 fixture 无法完成。
- Copilot 已有 `/GOVERN GOAL-008` 的可观察 dispatch 与 VS Code `1.129.1` 工作区截图，但仍缺精确 Copilot extension 版本。

### 必改项汇总

- I-002：`required / collecting`；三个 adapter 继续保持 manifest `unverified`，兼容验收仍被阻断。
- I-003 与 `GOAL-001 F-005`：保持 `open / required`，未受本轮影响。

### 结论 + 建议下一步

本轮成功把“没有运行时事实”缩小为可复现的三类缺口，没有产生任何虚假的 `verified`。Copilot slash dispatch 已有实际 screenshot，下一步只需补齐其 extension 版本；同时在可用 Grok provider 上重跑，并对 Claude 使用可观察的 skill-dispatch 机制（例如宿主公开的 skill-load event 或不依赖模型复述的受控 marker）后，再考虑更新对应 adapter 状态。

## A-007 · I-002 三宿主 `/govern` Runtime Dispatch 复核（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：stage / D-003 的 `0.1.0` current `/govern` fixture；仅核对 Claude Code CLI、Grok Build CLI 与 GitHub Copilot VS Code 是否在固定版本环境中实际调度主入口。
- **verdict**：pass

### 范围与区间

本条响应 A-006 的三个可观察 dispatch 缺口。它不重写 A-006 当时的事实：Grok headless provider 502 仍是该调用配置的失败记录；本次核对的是用户补充的交互式宿主证据，以及本机补齐的 Copilot built-in package 指纹。`previousSupportedProtocol: null` 保持不变，没有 previous fixture。

### 成果（有证据）

- [Claude Code screenshot](attachments/claude-code-govern-runtime-2026-07-19.png)（SHA-256 `5B6D05DCC5555AE888EBADA8382A9A728505C59AF44095DC782E758AA46BE791`）显示 Claude Code `2.1.215` 在本仓库运行 `/govern` 后检索 `**/03-audit.md`。
- [Grok Build screenshot](attachments/grok-build-govern-runtime-2026-07-19.png)（SHA-256 `A3123997316830338985233E0A94C4F160D0D0BE3234225E3A9DB39400C22531`）显示 Grok Build `0.2.103 (89c3d36fb6)` 的仓库 `/govern` 正在输出实际扫描结果。
- [Copilot runtime screenshot](attachments/copilot-vscode-govern-runtime-2026-07-19.png) 记录 VS Code 中 `/GOVERN GOAL-008` 的实际输出；VS Code `1.129.1` 的 built-in `GitHub / copilot-chat` package manifest 记录版本 `0.57.0`、build `1`、SHA-256 `4304D865FF058792AE0AA5304014534FA61447C08D966429FB4AD38A0CC17AC0`。
- canonical manifest 和 Skills mirror 的三条 adapter `verificationStatus` 已同步为 `verified`；契约仍保持 `adapterCompatibilityStatus: declared`，因为 I-002 的完整矩阵/验收并未完成。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 三宿主固定版本的 current `/govern` runtime fixture | 已完成（本 scope） | 三张归档 runtime screenshot、版本/环境指纹与 [runtime fixture 结果](attachments/i-002-runtime-fixture-2026-07-19.md)。 |
| 当前/上一协议 fixtures 与跨宿主消费测试 | 部分 | `0.1.0` current 的 `/govern` 已验证；previous 明确不适用；`/audit` 与自动化重放未覆盖。 |
| 区分已验证与未覆盖范围 | 已完成（本 scope） | manifest `verified` 明确限定为 current `/govern`，未扩大为 parser、CI、release 或完整兼容验收。 |
| CI 漂移校验、报告与发行物身份 | 未开始 | I-003 / 阶段 C。 |

### Findings

本次 scope 内无新的 F-00N。I-002 仍是 `required / collecting`，因为全量 compatibility matrix 和重放证据尚未完成；这不是已关闭的 I-002 被重新打开。

### 必改项汇总

- I-002：current `/govern` 子范围已通过；完整兼容验收仍为 `required / collecting`。
- I-003 与 `GOAL-001 F-005`：保持 `open / required`，未受本条影响。

### 结论 + 建议下一步

三个已声明 adapter 的固定版本 `/govern` 运行时证据已足以将对应 manifest 行标为 `verified`。下一步应针对未覆盖入口和自动化重放扩展 I-002，而不是将本条局部通过误写为阶段 5 发布验收。

## A-008 · 当前最低可用裁决与发布一致性延期响应（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：response / 响应上游 A-006 / A-007 / A-008 的 F-005 门禁，并审视 D-004 对当前最低可用范围、I-002、I-003 的影响；不作阶段 5 关门审计。
- **verdict**：conditional

### 范围与区间

用户确认当前交付只主张三宿主固定版本的 `0.1.0` current `/govern` 最低可用，不主张 `/audit` 运行时、完整兼容矩阵、manifest 解析、自动化重放、CI 或 release。该裁决延期的是发布一致性工作，不是接受 residual risk，也不是关闭 required 门禁。

### 成果（有证据）

- I-001 的 canonical schema/manifest、镜像、fixtures 与契约测试保持 `verified`。
- [A-007](#a-007--i-002-三宿主-govern-runtime-dispatch-复核2026-07-19) 已留下 Claude Code `2.1.215`、Grok Build `0.2.103`、Copilot VS Code `1.129.1` / `copilot-chat 0.57.0` 的 current `/govern` 实际 dispatch 证据。
- [D-004](01-decision.md#d-004--当前最低可用基线与发布一致性延期2026-07-19) 记录用户书面取舍、责任人与复核触发；[GOAL-001 D-011](../GOAL-001-main-vision/01-decision.md) 同步上游 F-005 的状态。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 当前三宿主 current `/govern` 最低可用 | 已完成（本 scope） | A-007 与 runtime fixture 归档证据。 |
| 完整兼容矩阵、未覆盖入口与自动化重放 | deferred / required | I-002；首次支持新宿主/版本或首次对外/可复现发布时复核。 |
| CI、测试报告、发行物身份与 tag/release | deferred / required | I-003；首次对外/可复现发布时复核。 |
| 阶段 5 发布验收与 F-005 关闭 | 未完成 | F-005 保持 open / required（deferred），不放行阶段 7 或根目标关门。 |

### 关闭证据与仍开放项

| finding / I-00N | 状态 | 证据 |
|-----------------|------|------|
| 当前最低可用范围 | 本 scope 通过 | I-001 `verified`；A-007 三宿主 current `/govern` dispatch。 |
| I-002 | deferred / required | D-004；触发为首次支持新宿主/版本或首次对外/可复现发布。 |
| I-003 | deferred / required | D-004；触发为首次对外/可复现发布。 |
| GOAL-001 F-005 | open / required（deferred） | GOAL-001 D-011 / A-009；触发为首次对外/可复现发布。 |

### Findings

本次没有新增 F-00N。F-005 未关闭；其延期不会将当前最低可用主张扩大为发布一致性结论。

### 必改项汇总

- I-002、I-003 与 F-005 保持 `required`；在各自触发到来前不安排进一步工作，到达触发时必须先复核并按开放 required 推进。

### 结论 + 建议下一步

**conditional**：当前最低可用范围有充分证据，GOAL-008 保持 `active / 20%`；完整发布一致性仍未完成且已正式延期。下一步不是关门，而是在首次支持新宿主/版本或首次对外/可复现发布时重新进入 `/govern GOAL-008`，按台账恢复对应门禁。
