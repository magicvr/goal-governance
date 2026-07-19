---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: audit
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.6.0
---

# 审计 · GOAL-008

## 信息就绪核对

| ID | 级别 | 状态 | 影响门禁 | 当前证据 | 结论 |
|----|------|------|----------|----------|------|
| I-001 | required | verified | 方案与发布范围冻结 | [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；[A-002](#a-002--i-001-契约实现与验证复审2026-07-19) | 已创建 canonical schema/manifest、镜像、正反 fixtures 与安装/bootstrapping 契约测试；此门禁已通过 |
| I-002 | required | collecting | 受影响实施与兼容验收 | [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)；[I-002 宿主与契约证据](attachments/i-002-host-compatibility-evidence-2026-07-19.md)；canonical manifest 已声明三行 adapter，但均为 `unverified` | 初始范围冻结子问题已关闭；实际 host release / runtime fixture 未关闭，不可通过兼容验收 |
| I-003 | required | collecting | 阶段 5 发布验收、F-005 关闭和阶段 7 输入 | D-010；当前尚无 release tag 和可重放发行证据 | 未关闭；不可通过阶段 5 发布验收 |

当前没有用户接受的 residual risk；`collecting` 不等同于 `verified`。

## 上游审计意见与开放门禁

以下意见属于 GOAL-001 的阶段 5 立项审计范围，本目标只引用其门禁，不重新编号或冒充新的独立审计：

| 上游意见 | source | verdict | 相关状态 |
|----------|--------|---------|----------|
| [A-006](../GOAL-001-main-vision/03-audit.md) | independent | conditional | `F-005 open / required`；`F-006 open / recommended` |
| [A-007](../GOAL-001-main-vision/03-audit.md) | self | conditional | 与 A-006 同向确认开放门禁 |
| [A-008](../GOAL-001-main-vision/03-audit.md#a-008--合并响应-a-006--a-007-与阶段-5-立项门禁2026-07-19) | self | conditional | 允许立项；I-001～I-003 collecting，F-005 仍开放必改 |

## 阶段性复盘

### 成果

- 已按 D-010 建立 GOAL-008 五件套、信息台账和路线图。
- 已将上游的范围边界、开放 required 门禁和非阻断 recommended 项写入本目标可追踪记录。
- 已收集并审视 I-001 的 SemVer、JSON Schema 和行为测试实践，形成 D-002 与可核对的 [调研附件](attachments/i-001-industry-practice-research-2026-07-19.md)。
- 已实现 D-002 的 canonical schema/manifest、Skills 镜像、正反 fixtures 与安装/standalone bootstrap 断言，并以 A-002 复审 I-001。
- 已收集 I-002 的仓库安装/解析证据与宿主公开资料，形成 [I-002 宿主与契约证据](attachments/i-002-host-compatibility-evidence-2026-07-19.md)；D-003 已据此冻结 `0.1.0` 首个基线、无上一版本、三宿主的声明/承诺层级及 Web 只读边界，但未越过宿主运行时证据边界。

### 偏差与注意点

- 本次已实施 I-001 协议契约及其测试，并完成 I-002 初始范围冻结；尚没有精确外部宿主 release 的运行时矩阵、跨宿主 fixture、CI 或发行演练，不能据此关闭 I-002、I-003 或 `F-005`。
- 目标为 `active / 20%`；I-001 已通过，不得把该局部门禁通过写成跨宿主兼容验收、阶段 5 实施完成或发布范围已全面冻结。

### 建议

- D-003 已裁决初始/上一协议基线、声明/承诺层级和 Web 边界；下一步以精确 Claude Code CLI、Grok Build CLI 和 Copilot VS Code 环境执行 current/negative fixture，记录实际结果并保留无上一版本的事实。
- 在阶段验收前形成 I-003 所需的可重放 CI、报告、变更日志与 tag/release 证据，并邀请阶段审计复核 `F-005`。

## 审计结论

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
