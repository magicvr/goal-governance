---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: audit
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 1.4.0
---

# 审计 · GOAL-008

## 信息就绪核对

| ID | 级别 | 状态 | 影响门禁 | 当前证据 | 结论 |
|----|------|------|----------|----------|------|
| I-001 | required | verified | 方案与发布范围冻结 | [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；[A-002](#a-002--i-001-契约实现与验证复审2026-07-19) | 已创建 canonical schema/manifest、镜像、正反 fixtures 与安装/bootstrapping 契约测试；此门禁已通过 |
| I-002 | required | collecting | 受影响实施与兼容验收 | [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)、[D-005](01-decision.md#d-005--重启完整发布一致性关门路径2026-07-19)、[D-006](01-decision.md#d-006--候选验证状态与发行身份分层2026-07-19)、[D-008](01-decision.md#d-008--候选运行时证据契约与宿主配置边界2026-07-19)；canonical matrix、negative fixtures、机读 runtime evidence 与当前 compatibility report | Claude/Grok 的 `/govern`、`/audit` 四个单元已验证；Copilot 两个入口与 Web parser CI replay 共 3 个 candidate 单元仍未关闭 |
| I-003 | required | collecting | 阶段 5 发布验收、F-005 关闭和阶段 7 输入 | [D-005](01-decision.md#d-005--重启完整发布一致性关门路径2026-07-19)、[D-006](01-decision.md#d-006--候选验证状态与发行身份分层2026-07-19)；`.github/workflows/ci.yml`、`scripts/`、`docs/releases/`、`CHANGELOG.md` 与 rehearsal | CI/报告/发行身份工具链已实现；当前仍无 ready coverage、干净可重放 CI 归档或与 matrix `candidateRevision` 绑定的 annotated release tag，不可通过阶段 5 发布验收 |

当前没有用户接受的 residual risk；D-004 的历史延期已由 D-005 解除，I-002、I-003 当前均按开放 required 处理。

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
- 已按 D-008 建立机读 runtime evidence schema、捕获器、freshness/digest/timeout/脱敏 transcript 回归，并将 Claude/Grok 的 `/govern`、`/audit` 四个候选单元验证为 `runtime-verified`。

### 偏差与注意点

- 本次已实施 I-001 协议契约及其测试、完成 I-002 初始范围冻结并取得三宿主的历史 `/govern` current 运行时证据；D-005 后又建立 compatibility matrix、negative fixtures、Ubuntu/Windows CI、兼容/发行报告工具、CHANGELOG 与本地 rehearsal。Claude/Grok 的候选双入口 runtime 已取得；Copilot 双入口、Web CI replay、ready coverage、干净 CI 归档及 tag/release 仍未取得。
- 目标为 `active / 20%`；I-001 已通过，不得把该局部门禁通过写成跨宿主兼容验收、阶段 5 实施完成或发布范围已全面冻结。

### 建议

- 先由用户在新鲜 VS Code Copilot Chat 会话中分别运行 `/govern GOAL-008` 与 `/audit GOAL-008` 并归档版本/输入/输出/截图；再以一次实际 CI replay 将 Web parser 单元从 `pending-ci-replay` 更新为可核对状态。未通过单元保持 pending/blocked。
- coverage ready 且用户授权版本/tag 后，将 matrix `candidateRevision` 同步为 annotated tag，生成 release-candidate 证据；随后进行阶段 self 审计并建议 independent finding-closure 复审。

## 审计结论

> A-001～A-012 是按时间追加的历史审视；其中的 `collecting`、`deferred`、`open / required` 表示各自审计时点。当前状态以本文件顶部信息台账和最新响应 A-013 为准。

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

## A-009 · 重启完整发布一致性关门门禁响应（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：response / 响应 A-008、D-004 的延期状态，并审视 D-005 对 I-002、I-003、GOAL-001 F-005 与阶段 5→6 顺序的影响；不作阶段 5 关门审计。
- **verdict**：conditional

### 范围与区间

用户已书面要求完整关门 GOAL-008，并指定当前机器的 Claude Code、Grok Build 与 VS Code 内置 GitHub Copilot 版本作为首个支持基线。本条只核对恢复门禁、边界与证据计划是否真实落盘；不把历史 `/govern` 证据、尚未创建的 CI 或尚未授权的 tag/release 写成完成。

### 成果（有证据）

- [D-005](01-decision.md#d-005--重启完整发布一致性关门路径2026-07-19) 已将 I-002、I-003 与 F-005 从延期路径恢复为 `collecting / required`，无 residual risk 接受。
- 当前机器的 Claude `2.1.215`、Grok `0.2.103 (89c3d36fb6)`、VS Code `1.129.1` / commit 与内置 Copilot Chat `0.57.0` build `1` 已在 [02-execution.md](02-execution.md) 留下可核对发现事实；完整 runtime 证据仍待候选发行物产生。
- `previousSupportedProtocol: null` 保持为 D-003 的首个基线事实；D-005 要求以显式 N/A 和负例验证该事实，不伪造不存在的前一版本。

### 关闭证据与仍开放项

| finding / I-00N | 状态 | 关闭所需证据 |
|-----------------|------|--------------|
| I-002 | collecting / required | canonical 兼容矩阵、current/negative fixtures、三宿主 `/govern` 与 `/audit` runtime 证据、Web parser 回归与未覆盖范围报告 |
| I-003 | collecting / required | CI 产物、canonical/mirror digest、测试/兼容报告、变更日志、发行物身份和 annotated tag/release 或等价可追溯演练 |
| GOAL-001 F-005 | open / required | I-002、I-003 的关闭证据及根目标响应记录；未关闭前不得阶段 5 发布验收或 GOAL-008 关门 |

### Findings

本条没有新增 F-00N。I-002、I-003 与 F-005 是已恢复的 required 门禁；它们的未完成状态使本条为 `conditional`，不构成状态变更或关门放行。

### P-004 与建议下一步

既有独立 A-006 / 自审 A-007 的 F-005 结论同向，当前没有 verdict 或必改项冲突，也不存在“只有 independent、没有 self”的未决情形。下一步先实现兼容矩阵、fixtures、CI 与发行证据自动化；完成候选发行物后，再向用户索取三宿主 `/govern` / `/audit` 的真实运行时结果，并以阶段 self 审计和建议的 independent 复审判断是否进入 close-out。

## A-010 · 独立交叉审计：当前状态、执行事实与门禁（2026-07-19）

- **source**：independent
- **auditor**：Grok Build `/audit`
- **类型 / scope**：ad-hoc · execution-facts · design-plan / GOAL-008 当前整体状态：范围与成功标准、P-005 信息门禁、D-005 重启后的实施与证据、I-002/I-003 与上游 F-005 是否可放行；**不作** `status: done` 关门放行。
- **verdict**：conditional

### 范围与区间

| 项 | 内容 |
|----|------|
| 目标 | `GOAL-008-skills-consumer-adapter-release-consistency` |
| 只读依据 | `00-meta` / `01-decision` / `02-execution` / `03-audit`（至 A-009）；`goal-tree.md`；`docs/contracts/*` 与 `skills/contracts/*` 镜像；`.github/workflows/ci.yml`；`scripts/compatibility_report.py` / `release_evidence.py`；`artifacts/*.json`；runtime 截图附件 SHA-256 |
| 排除 | 不改 `status`/`progress`/goal-tree；不重新审计 GOAL-001 全文；不把 rehearsal 证据写成 release |

### 成果（有证据）

1. **目标定义与门禁纪律（通过面）**
   - 范围、排除项、成功标准、阶段 A–D 路线图与 D-001～D-005 链条完整；D-005 明确恢复 I-002 / I-003 / F-005 为 `collecting / required`，**未**接受 residual risk。
   - 目标保持 `active / 20%`，与“完整发布一致性未完成”一致；goal-tree 同步为 active 20%。
   - I-001：`docs/contracts/` canonical schema/manifest + `skills/contracts/` 镜像 + 正反 fixtures 与契约测试路径仍在；A-002 对该门禁的 `pass` 有可回指证据。

2. **历史 `/govern` runtime 证据（有界通过）**
   - 三张归档截图哈希与执行记录一致（本轮复算）：
     - Claude：`5B6D05DCC5555AE888EBADA8382A9A728505C59AF44095DC782E758AA46BE791`
     - Grok：`A3123997316830338985233E0A94C4F160D0D0BE3234225E3A9DB39400C22531`
     - Copilot：`BE9E28996BD4BB39DA75FA226B6225BB0C6462F33CD462F1F83B82B0601BA713`
   - A-007 将其限定为固定版本 `0.1.0` **current `/govern` dispatch**，不扩到 `/audit`、完整矩阵或 release——该边界在自审中写清。

3. **D-005 之后的仓库实施产物（存在，但 ledger 未同步）**
   - Canonical 兼容矩阵：`docs/contracts/skills-consumer-compatibility-matrix.json`（与 `skills/contracts/` 镜像 SHA-256 一致：`E9DFB033BF6076529B5D2538DE1F2BE5E3397EB03113C1CCE903BB23E537351C`）。
   - 矩阵诚实标注：三宿主 `govern`/`audit` 均为 `pending-runtime-validation`；`/audit` 的 `evidence` 为空数组；Web 行为 `pending-ci-replay` 的非 adapter 行；`previous: null` + negative fixtures 路径已登记。
   - 自动化：`scripts/compatibility_report.py`、`scripts/release_evidence.py`、`scripts/tests/test_release_evidence.py`、`.github/workflows/ci.yml`（ubuntu + windows 生成 rehearsal 产物）。
   - 本地产物：`artifacts/compatibility-report.json` 的 `coverage.status = pending`（7 个 uncovered 单元）；`artifacts/release-evidence.json` 的 `releaseStatus = rehearsal`、`annotatedTag = null`、`workingTree.clean = false`。
   - 契约测试侧已有 `test_candidate_compatibility_matrix_keeps_pending_runtime_evidence_visible`，把 matrix pending 与 manifest 历史 `verified` 分层——实现意图正确。

### 对照成功标准

| 成功标准 | 文档勾选 | 仓库事实（本轮核对） | 判断 |
|----------|----------|----------------------|------|
| 唯一机读协议/模板版本与兼容声明 | [x] | schema/manifest/fixtures/镜像/测试存在 | **已完成**（I-001） |
| 兼容矩阵（core/Skills/三宿主/Web；当前+上一协议） | [ ] | 矩阵文件存在；previous 为 N/A；单元全 pending | **部分**：结构有，验收未过 |
| current/previous fixtures + 跨宿主测试 + 区分未覆盖 | [ ] | negative fixtures + matrix uncovered 列表有；宿主 runtime 未重验 | **部分** |
| CI 漂移校验、报告、变更日志、发行物身份 | [ ] | workflow/scripts/CHANGELOG/rehearsal 证据存在且未提交干净 | **部分**：工具链有，I-003 未关闭 |
| 可追溯 tag/release 或等价演练 | [ ] | 无 `v*` tag；仅 rehearsal | **未完成** |

### Findings

#### F-001 · required · high · 执行台账与仓库事实漂移

- **现象**：仓库已具备 D-005 规划中的矩阵、负例 fixtures、CI workflow、兼容/发行脚本、rehearsal 产物与 CHANGELOG；但 `02-execution.md` 末条仍写「尚未…创建 CI、tag 或 release」，`00-meta` 成功标准 2–5 仍全空，路线图 B/C/D 仍写「进行中/待实施」且未引用上述路径，`03-audit` 顶部「阶段性复盘」仍沿用 D-004 延期建议。
- **为何必改**：AGENTS §5 要求执行只记事实；未落盘的实施会使编排器与后续审计误判进度，也可能在未记账情况下继续堆叠实现。
- **关闭证据建议**：在 `02-execution` 追加时间线条目，逐项列出路径、命令、产物与**明确未覆盖项**；同步 `00-meta` 成功标准勾选（仅勾可证据支持的部分）与路线图状态；刷新 `03-audit` 信息就绪表与阶段性摘要中的过时延期措辞。

#### F-002 · required · high · I-002 候选发行物 runtime 未关闭（含零 `/audit`）

- **现象**：矩阵 6 个宿主入口全部 `pending-runtime-validation`；三宿主 `audit.evidence = []`。历史 `/govern` 截图仅作参考证据挂在 govern 行下，且 `evidenceScope` 写明候选发行物须重新验证。
- **对照 D-005**：要求三宿主在 `0.1.0` 上对 `/govern` **与** `/audit` 分别取得可观察 dispatch。
- **关联**：canonical manifest 三条 adapter 仍为 `verificationStatus: verified`（A-007 历史子范围）；与矩阵 pending 并存依赖读者理解分层。skills README 有说明，但 goal 台账未把「候选重验」写成当前阻塞事实清单。
- **关闭证据建议**：在固定基线版本上为 Claude / Grok / Copilot 各取得 `/govern` 与 `/audit` 可观察证据（版本+环境+输出/截图哈希），更新矩阵单元状态与 uncovered 列表；未通过单元保持 pending/blocked，不得抬 `coverage.status`。

#### F-003 · required · high · I-003 / 上游 F-005 发行门禁未满足

- **现象**：`release-evidence` 仅为 `rehearsal`；无 annotated SemVer tag；工作树脏且大量发布相关路径仍为 untracked（`?? .github/workflows/`、`?? scripts/`、`?? docs/contracts/skills-consumer-compatibility-matrix*.json` 等）；`coverage.status = pending`。
- **对照**：阶段 5 发布验收与 GOAL-001 F-005 要求可重复 CI、digest、报告、变更日志、发行物身份与可追溯 tag/release。rehearsal 证明工具链可跑，**不等于** release 通过。
- **关闭证据建议**：干净可重放的 CI 结果、canonical/mirror digest 一致报告、CHANGELOG 版本节、维护者授权的 annotated tag（或文档定义的等价演练）且 `coverage` 达 ready 后再生成非 rehearsal 证据；tag/release 操作须用户授权。

#### F-004 · recommended · medium · 双层 `verified` 语义的误读风险

- **现象**：contract adapter `verificationStatus: verified` 与 matrix entrypoint `pending-runtime-validation` / report `coverage.pending` 并存；测试已锁定该分层，但合同字段名仍易被外部读者读成「宿主全面验证通过」。
- **建议**：在 contract schema/README 或 manifest 旁注中固化「contract verified = 历史有界子范围；发布以 matrix + coverage 为准」；或在候选发行物通过前将 contract 状态改回更保守的枚举（若协议允许）——由 `/govern` 选型，本意见不改 manifest。

#### F-005 · recommended · low · 摘要区过时指引

- **现象**：`00-meta` P-005 导语仍写 I-002/I-003「改为 deferred」；`03-audit`「阶段性复盘 · 建议」仍写「当前不扩展…首次对外时再复核」。D-005/A-009 已在后文纠正，但顶部摘要仍可能误导快速扫描。
- **建议**：与 F-001 一并清理，使「当前真相」只出现在最新台账与最新 A-00N。

### 必改项汇总

| ID | 级别 | 阻断 |
|----|------|------|
| **F-001** | required · high | 推进前须先对齐执行/meta 台账与仓库事实；否则后续事实审计不可信 |
| **F-002** | required · high | 阻断 I-002 兼容验收；关联 `/govern`+`/audit` 候选 runtime |
| **F-003** | required · high | 阻断 I-003、GOAL-001 F-005、阶段 5 发布验收与 GOAL-008 关门 |
| F-004 | recommended | 降低误读；不单独构成关门放行条件 |
| F-005 | recommended | 文档卫生；建议与 F-001 同批处理 |
| 上游 **GOAL-001 F-005** | open / required | 依赖本目标 I-002/I-003 关闭证据后由根目标响应 |

**无用户书面 residual 接受**；不得将 rehearsal 或历史 `/govern` 最低可用写成发布验收通过。

### 与既有意见的异同

| 既有 | 关系 |
|------|------|
| A-002 pass（I-001） | **同意**；本轮未发现 I-001 回归到未验证 |
| A-007 pass（三宿主 current `/govern`） | **同意其有界结论**；不同意将其扩大为 I-002 全关或候选发行物通过 |
| A-008 / A-009（延期→重启） | **同意** D-005 恢复 required 的方向；指出 A-009 之后**仓库已前进、goal 台账未跟** |
| GOAL-001 A-006 independent F-005 | **同向**：发布一致性 required 仍开放；本条补充 GOAL-008 本地 F-001～F-003 作为关闭路径上的具体阻塞 |

本目标此前 A-001～A-009 均为 `source: self`；**本条为 GOAL-008 首条 independent 意见**。与 self 在「不得虚假关门」上同向，**无 verdict 冲突**；差异在于强调 **ledger 滞后于实现** 与 **`/audit` 零证据**。

### 信息就绪（P-005）核对

| ID | 台账状态 | 本轮判断 | 受影响门禁 |
|----|----------|----------|------------|
| I-001 | verified | **维持 verified**（证据仍在） | 方案冻结：可通过 |
| I-002 | collecting | **仍开放 required**（矩阵结构有，runtime 未关） | 兼容验收：阻断 |
| I-003 | collecting | **仍开放 required**（rehearsal ≠ release） | 阶段 5 发布验收 / F-005：阻断 |

### 结论 + 建议给编排器/用户的下一步

**conditional**：GOAL-008 未假装完成，门禁语义总体正确，I-001 与有界历史 `/govern` 证据可核对；但 D-005 后的实现已超前于目标五件套记录，且 I-002/I-003 与上游 F-005 的关闭证据仍不足。
**不得**推进阶段 5 发布验收、GOAL-008 `done`、阶段 6 Web 深化或根目标关门。

建议 `/govern`：

1. **先响应 F-001**：把矩阵/CI/脚本/rehearsal/负例 fixtures 写入 `02-execution`，对齐 `00-meta` 与路线图（不抬 progress 到暗示验收完成的程度，除非有新的可核证据）。
2. **再推进 F-002**：向用户收集/执行三宿主 `/govern`+`/audit` 候选 runtime，更新矩阵与报告。
3. **F-003**：在覆盖就绪且用户授权后做 tag/release 演练；CI 路径纳入版本控制后再谈可重复发行证据。
4. 阶段 self 审计关闭本地 required findings 后，可再 `/audit` 做 finding-closure 复审。

### 声明

本意见 `source: independent`，**不修改**目标 `status` / `progress` / 方案正文 / goal-tree 状态列。响应、修正与推进由 **`/govern`** 处理。

## A-011 · 响应 A-010：对齐执行台账并收紧候选证据（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：response / 响应 A-010 F-001～F-005；核对 D-005 后的实施事实、候选验证语义与 rehearsal 可信度。不作 I-002/I-003 兼容或发布验收，不调整 status/progress。
- **verdict**：conditional

### 范围与区间

本响应只关闭已有仓库证据足以关闭的本地台账与语义问题；三宿主候选 runtime、CI 归档、ready coverage、annotated tag/release 仍缺外部或后续证据，继续作为 required 门禁。

### 已实施响应（有证据）

- `00-meta.md`、`02-execution.md` 和本文件顶部摘要现已登记 compatibility matrix、两类 negative fixtures、Ubuntu/Windows CI、兼容/发行报告工具、CHANGELOG、rehearsal 与 7 个 uncovered 单元；路线图 B/C/D 改为“部分实施/进行中”，不再写作延期或待实施。
- [D-006](01-decision.md#d-006--候选验证状态与发行身份分层2026-07-19) 将 contract manifest 的历史 `verified` 限定为固定版本 current `/govern` 子范围，候选 readiness 改由 matrix entrypoint 状态与 report coverage 判定；`skills/README.md` 与 matrix `evidenceScope` 同步该边界。
- `release_evidence.py` 不再接受调用方注入 checks；所有模式的外部 compatibility report 都必须与当前 HEAD 重新生成的 source、contract、matrix、mirror 和 coverage 完全一致。
- matrix `candidateRevision` schema 只允许 `unreleased`、完整 commit 或 `v` 前缀 SemVer tag；release-candidate 必须使其等于指向 HEAD 的 annotated tag，并在 evidence 中显式记录。
- `git diff --check` 已从 A-010 段落的行尾空格失败修复为通过；发行工具 19 项、Skills 31 项、standalone 3 项、Web 20 项（1 项 Windows symlink 权限跳过）均通过。最终完整 rehearsal 的 5 个内部固定 checks 全部通过，仍诚实记录 7 个 uncovered、`candidateRevision: unreleased` 与脏工作树。

### 关闭证据与仍开放项

| A-010 finding / 信息项 | 状态 | 证据与边界 |
|------------------------|------|------------|
| F-001 · 执行台账漂移 | **closed** | `00-meta.md` 路线图/信息台账、`02-execution.md` 两条新事实、顶部阶段摘要均与仓库产物及 7 个 uncovered 单元对齐；progress 保持 20%。 |
| F-002 · 候选 runtime 未关闭 | **open / required** | 三宿主 `/govern` / `/audit` 6 单元仍为 `pending-runtime-validation`；Claude headless 无充分 dispatch 输出，Grok headless provider 502，Copilot 无可替代 UI 的 CLI 路径。 |
| F-003 · I-003 / F-005 发行门禁 | **open / required** | 当前仍是 rehearsal、coverage pending、无 clean release commit 和 annotated tag；正式发布动作须维护者授权。 |
| F-004 · 双层 verified 误读 | **closed** | D-006；matrix `evidenceScope`；`skills/README.md`；候选 readiness 的 schema/工具门禁与回归测试。 |
| F-005 · 摘要过时 | **closed** | `00-meta.md` P-005 导语、本文件阶段性偏差/建议与审计结论导语均已改为 D-005 之后的当前事实。 |
| I-002 | **collecting / required** | 矩阵/fixtures/报告结构已形成；7 个 candidate 单元未覆盖，不能验收。 |
| I-003 / GOAL-001 F-005 | **collecting/open / required** | 工具链已形成；release-candidate/tag 与可重放 CI 证据未形成，不能放行。 |

### P-004 核对

A-010 与既有 self 意见在“不得虚假关门”及 F-002/F-003 门禁上同向，没有 verdict 或必改项冲突；本目标已有覆盖同 scope 的 self 审视与本响应，因此无需再次询问是否自审。D-006 是对 A-010 recommended F-004 的实现取舍，不构成 residual risk 接受。

### 结论 + 建议下一步

**conditional**：A-010 F-001、F-004、F-005 已由可核对改动关闭，执行 ledger 与证据工具可信度已对齐。A-010 F-002、F-003、I-002、I-003 与 GOAL-001 F-005 仍为开放 required；不得推进阶段 5 发布验收、GOAL-008 `done`、阶段 6 Web 深化或根目标关门。

下一步仅有两条证据链：先取得三宿主六个入口和一次 Web CI replay 的候选证据，使 coverage ready；再由维护者决定并授权版本/tag，将 matrix `candidateRevision` 绑定该 annotated tag，生成 release-candidate 并进入阶段 self/independent 复审。

## A-012 · 自审：Grok headless provider/model 防漂移修复（2026-07-19）

- **source**：self
- **auditor**：Codex
- **类型 / scope**：response / 用户要求修复 `unknown provider for model grok-build` 的未来测试误用路径；核对根规则、I-002 fixture、静态防漂移测试及历史失败证据。不作 Grok 候选 runtime 兼容验收。
- **verdict**：conditional

### 成果与证据

- 根目录 `AGENTS.md` 已规定 `grok-build-cli` 只表示适配器 ID；Grok headless 测试必须显式使用当前记录的 `--model grok-4.5`；`unknown provider`、模型相关 5xx 或无法确认 model 时必须保持 `blocked`，不能由 exit `0` 或 prompt 回显覆盖。
- `attachments/i-002-runtime-fixture-2026-07-19.md` 的可重放命令已加入 `--model grok-4.5`，并明确 endpoint/model 变更前必须同步规则、断言和环境证据。
- `scripts/tests/test_grok_runtime_fixture.py` 已对命令模型、适配器/model 区分和历史 502 保留做静态断言。

### 边界与未关闭项

- 历史 `502 Bad Gateway: unknown provider for model grok-build` 未被改写，仍是旧 headless 调用配置的 blocked 证据。
- 本次没有重新调用 Grok，也没有取得新的 `/govern` 或 `/audit` 候选 runtime 证据；I-002/F-002 仍为开放 required，不能据此推进兼容验收或关门。
- 本次未修改 `status`、`progress` 或 `goal-tree.md`，因为目标状态事实没有变化。

## A-013 · 响应 A-010 F-002：Claude/Grok 候选 runtime 部分关闭（2026-07-19）

- **source**：self
- **auditor**：Codex `/govern`
- **类型 / scope**：response + execution-facts / 响应 A-010 F-002 与 A-012 的后续事实；核对 runtime evidence 契约、Claude/Grok 四个候选入口、Grok 辅助 502 边界及根规则配置范围。不作 I-002 完整验收、I-003 发布验收或 close-out。
- **verdict**：conditional

### 范围与区间

本条只关闭已有机读证据充分覆盖的 Claude Code 与 Grok Build 单元。Copilot 与 Web CI 仍依赖外部/后续证据，release 仍依赖 ready coverage、干净候选和维护者授权的 annotated tag。

### 成果（有证据）

- `docs/contracts/runtime-evidence.schema.json` 与 Skills 镜像定义单元、环境、行为源、调用、退出/marker、stdout/stderr 摘要和截图；`scripts/compatibility_report.py` 会重新核对 JSON schema、unit/protocol、行为源与输出摘要，只接受 `verdict: pass`。
- `scripts/capture_runtime_evidence.py` 为探针增加有界 timeout；Claude stream-json 使用脱敏 transcript，Grok 保留可诊断 stdout/stderr 并脱敏本机 `Request URL`。`scripts/tests/test_runtime_evidence.py` 覆盖 schema/capture、timeout、行为源陈旧、stdout/stderr 篡改、URL 脱敏与 `runtime-verified` JSON 门禁。
- Claude Code `2.1.215` 的 [govern evidence](attachments/runtime/claude-code-cli-govern-2026-07-19.json) 与 [audit evidence](attachments/runtime/claude-code-cli-audit-2026-07-19.json) 均记录只读工具白名单、实际 skill/prompt/目标读取、marker 和 process success；transcript 不含 thinking/signature 或完整工具结果正文。
- Grok Build `0.2.103` 的 [govern evidence](attachments/runtime/grok-build-cli-govern-2026-07-19.json) 与 [audit evidence](attachments/runtime/grok-build-cli-audit-2026-07-19.json) 均记录主 `grok-4.5` 调用成功；可选 session-title alias `grok-build` 的 502 作为 warning 保留，不改变主单元 pass。
- D-008 修正 A-012/D-007 的配置范围：具体 endpoint/model 只留在本目标 runtime 附件，根 `AGENTS.md` 保持通用；静态测试验证两者没有混淆。
- 矩阵与报告现仅列 Copilot `/govern`、Copilot `/audit`、Web parser `pending-ci-replay` 三个 uncovered；完整 rehearsal 5/5 checks 通过，coverage 仍为 `pending`。

### 关闭证据与仍开放项

| finding / 信息项 | 状态 | 证据与边界 |
|------------------|------|------------|
| A-010 F-002 · Claude `/govern` / `/audit` | **closed（本单元）** | 两份 Claude machine evidence；sanitized transcript；matrix `runtime-verified`。 |
| A-010 F-002 · Grok `/govern` / `/audit` | **closed（本单元）** | 两份 Grok machine evidence；主 marker/exit pass；辅助 502 warning 保留。 |
| A-010 F-002 / I-002 | **open / required** | Copilot 两个入口与 Web CI replay 共 3 个单元仍 uncovered，不能通过完整兼容验收。 |
| A-010 F-003 / I-003 | **open / required** | 当前仍为 rehearsal、coverage pending、工作树不干净且无 annotated tag/release。 |
| GOAL-001 F-005 | **open / required** | 继续依赖 I-002、I-003 全部关闭及根目标响应。 |

### P-004 核对

A-010 independent 与本条 self response 对 required 门禁同向，没有 verdict 或必改项冲突；不存在需要重新询问“是否自审”的情形。本条不接受 residual risk，也不将部分单元通过扩大为 I-002 或发布验收通过。

### 结论 + 建议下一步

**conditional**：Claude/Grok 四个候选 runtime 单元已由可重复机读证据关闭，A-010 F-002 的范围缩小但未整体关闭。GOAL-008 继续 `active / 20%`；不得推进阶段 5 发布验收、GOAL-008 `done`、阶段 6 Web 深化或根目标关门。

下一步由用户提供新鲜 Copilot `/govern` 与 `/audit` 证据；实际 CI replay 关闭 Web parser 单元后，coverage 才可能 ready。随后仍须维护者授权版本/tag，并形成 clean release-candidate 证据与阶段复审。
