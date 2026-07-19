---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 1.1.0
---

# 执行记录 · GOAL-008

## 时间线

### 2026-07-19 · 按 D-010 创建目标

- 用户明确要求按 GOAL-001 D-010 创建 GOAL-008。
- 创建 `docs/goals/GOAL-008-skills-consumer-adapter-release-consistency/` 及完整五件套，并将 `parent` 设置为 `GOAL-001-main-vision`。
- 将 D-010 的阶段 5 范围、排除项和 I-001～I-003 信息需求移交本目标；三项仍为 `required / collecting`，没有 residual risk 接受。
- 同步 [goal-tree.md](../goal-tree.md) 的文本树、状态表和编号提示；本目标保持 `draft / 0%`。

### 2026-07-19 · 收集 I-001 行业实践并完成设计审视

- 直接核对 [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)：其要求声明 public API，并以 MAJOR / MINOR / PATCH 分别表达不兼容变更、向后兼容新增和向后兼容修复。
- 直接核对 [JSON Schema Core 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html)：验证 schema 的 `$schema` 标识 dialect，`$id` 标识 schema resource 的 canonical URI；普通 manifest 以 `contractSchemaId` 引用该 schema，三者都不能替代业务协议版本。
- 直接核对 [JSON Schema Test Suite](https://github.com/json-schema-org/JSON-Schema-Test-Suite)：其以按版本组织的有效/无效实例验证规范行为，而不把字段存在检查当作充分证据。
- 将来源、关键原文、取舍和最小字段模型落盘至 [I-001 行业调研附件](attachments/i-001-industry-practice-research-2026-07-19.md)，并记录 [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19)。
- 结论：已确定未来 canonical 位置、声明字段和兼容语义；尚未创建 schema/manifest、镜像或 fixtures。I-001 保持 `required / collecting`，没有冻结受影响范围或进入实施。

### 2026-07-19 · 实现并验证 I-001 契约

- 在 `docs/contracts/` 新增 `skills-consumer-contract.schema.json`、canonical manifest 及正反 SemVer / 适配器状态 fixtures；schema 将 JSON Schema 的 `$schema` / `$id` 与普通 manifest 的 `contractSchemaId` 分离。
- 将上述 files 逐字节同步到 `skills/contracts/`，并将 `-All/--all` 安装器扩展为复制 `contracts/`；core standalone bootstrap 同步复制 `docs/contracts/`，避免契约在独立核心包中缺失。
- 在 `skills/tests/test_skills_orchestrator.py` 增加 schema 结构、manifest 语义、正反 fixtures、canonical/mirror、哈希台账和隔离安装输出验证；更新 `docs/tests/test_standalone_bootstrap.py` 覆盖 canonical contracts。
- 运行 `python -m unittest skills/tests/test_skills_orchestrator.py -v`，29 项通过；运行 `python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`，3 项通过；`powershell` 解析 `install.ps1` 与 Git Bash 解析 `install.sh` 均通过。
- 验证结论：I-001 的 required 信息已由可核对实现和测试关闭，状态改为 `verified`。本次没有建立 I-002 宿主/版本矩阵、跨版本 fixtures、CI 发布证据或 release tag。
- 计划：下一步收集并审视 I-002，先定义实际宿主、wrapper 与 Web 解析器的支持边界，再进入受影响实施。

### 2026-07-19 · I-001 最终复核

- 在治理记录完成后复跑 `python -m unittest skills/tests/test_skills_orchestrator.py -v`（29 项通过）和 `python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`（3 项通过）。
- PowerShell 解析 `skills/install.ps1` 通过；Git Bash `bash -n skills/install.sh` 通过；14 个 `docs/contracts/` 与 `skills/contracts/` JSON 文件均可解析；`git diff --check` 通过（仅报告既有 LF/CRLF 转换提示，无空白错误）。
- 本轮复核确认 D-002 的 schema/manifest、镜像、fixtures、安装和 standalone 契约测试仍成立；未将该结果扩大解释为 I-002 兼容矩阵或 I-003 发布证据。

### 2026-07-19 · 收集并审视 I-002 宿主兼容边界

- 收集并落盘 [I-002 宿主与契约证据](attachments/i-002-host-compatibility-evidence-2026-07-19.md)：仓库内 Claude Code、Grok Build、GitHub Copilot 的安装/wrapper 路径，Web 只读解析器及其测试，以及 Claude Code、GitHub Copilot、JSON Schema Test Suite 与 SemVer 的一手公开资料。
- 核对结果：安装器和结构测试可证明分发产物、路径和本地 Web 解析行为；它们不能证明 Claude、Grok 或 Copilot 的真实运行时加载、版本支持或跨宿主行为。GitHub Copilot prompt files 目前仅有 VS Code、Visual Studio 与 JetBrains 的公开预览支持说明；初始从通用 `docs.x.ai` 入口未取得 Grok Build 资料，后续已按用户提供的一手产品页复核并更正，见下条事实记录。
- 新发现：当前机器可读协议仅为 `0.1.0`，没有可追溯的前一协议产物；不得凭空制造“上一版本” fixture。I-002 仍为 `required / collecting`，不冻结受影响实施或兼容验收范围。
- 计划：待用户选择初始基线/上一版本策略、目标宿主与实际版本环境、以及 Web 是 manifest 消费者还是仅目标文档解析器后，再记录 D-003 并实施矩阵与 fixtures。

### 2026-07-19 · 按用户提供来源复核 Grok Build 仓库 Skills

- 用户提供 [Introducing Grok Build](https://x.ai/news/grok-build-cli) 后，直接核对 xAI 公告和 [Grok Build Skills, Plugins & Marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces) 文档。
- 官方文档明确：Grok 从 `./.grok/skills/` 发现 skills，并向上遍历至仓库根；user-invocable skills 会以 `/<skill-name>` 成为斜杠命令；Grok 也读取从 cwd 向仓库根遍历的 `AGENTS.md` 指令文件。仓库的 `.grok/skills/govern/SKILL.md` 与 `.grok/skills/audit/SKILL.md` 因而具有一手路径/发现语义依据。
- 更正此前“未取得 Grok Build 官方发现资料”的证据边界：此前仅访问通用文档入口所得的缺口，不是产品不支持的事实。已更新 I-002 证据附件和信息台账，并在 A-004 留下可追溯的审视更正。
- 该证据仍不是本包在某一固定 Grok Build release 中的端到端运行结果；contract manifest 继续保持 `adapterCompatibilityStatus: I-002-pending`，I-002 保持 `required / collecting`。

### 2026-07-19 · 记录 D-003 并冻结 I-002 初始支持边界

- 用户书面裁决：协议 `0.1.0` 为首个支持基线，上一版本明确为无；不得伪造 predecessor fixture。
- 用户将 Grok Build CLI 纳入已声明支持范围，但当前明确承诺仅为 Claude Code CLI 与 GitHub Copilot VS Code 插件；Web 继续仅解析目标文档，未来完整闭环不属于当前实现范围。
- 记录 [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)，将其与 A-003 / A-004 的证据边界和 I-002 台账对齐。
- 依据该裁决，将 canonical manifest/schema 增补首个/上一协议基线和 `declared` / `committed` adapter 层级，并同步镜像、fixtures 与契约测试；这些变更尚不构成 Claude、Grok 或 Copilot 的实际产品运行时验证。
- 更新 `docs/README.md` 与 `skills/README.md`，将核心文档可独立应用、Web 当前只读解析、以及“安装面”与“声明/承诺/验证状态”的边界显式写出。

### 2026-07-19 · 验证 D-003 契约范围实现

- 运行 `python -m unittest skills/tests/test_skills_orchestrator.py -v`：30 项通过，其中包括 D-003 的 baseline、adapter 层级、mirror、fixtures、安装输出和 hash ledger 断言。
- 运行 `python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`：3 项通过，确认核心文档层独立启用与同步台账仍成立。
- 解析 `docs/contracts/` 与 `skills/contracts/` 的全部 JSON，并核对 9 个 contract/schema/fixture 镜像文件逐字节一致；`git diff --check` 通过（仅有工作树 LF/CRLF 转换提示，无空白错误）。
- 本次没有调用 Claude Code CLI、Grok Build CLI 或 Copilot VS Code 的真实产品环境；三条 adapter 仍保持 `unverified`。

### 2026-07-19 · 执行 I-002 版本固定 Runtime Fixture

- 直接探测并固定本机环境：Claude Code CLI `2.1.215`、Grok Build CLI `0.2.103 (89c3d36fb6)`、VS Code `1.129.1` / commit `8a7abeba6e03ea3af87bfbce9a1b7e48fed567b8`。根目录 `.claude/.grok` 的 `govern/SKILL.md` 分别与 `skills/install/claude|grok/` source 的 SHA-256 一致。
- Claude 以 `-p`、`--no-session-persistence`、`--permission-mode plan`、`--max-turns 3` 执行 `0.1.0` current 与“无 previous fixture”negative prompt，均 exit `0` 并返回预期边界文本；由于输出可受 prompt 直接引导，记录为 project-context runtime probe，而不是 `verified` compatibility pass。
- Grok 用相同 current 语义加 `--no-subagents --no-memory --disable-web-search` 实际调用，Responses API 返回 `502 Bad Gateway: unknown provider for model grok-build`。即使 CLI 最终 exit `0` 并回显 prompt，也以 API 错误作为 fixture `blocked` 结果，不将其写成通过。
- 用户补充并提供 screenshot：GitHub Copilot VS Code Chat 中 `/GOVERN GOAL-008` 已实际输出 I-002 / A-006 摘要，故升级该子证据为 `slash-dispatch observed / unverified`。本机 `code --list-extensions --show-versions` 未列出该扩展，screenshot 也未显示扩展版本，因此仍不可标完整 adapter `verified`。
- Web 的首次根目录 system-Python 执行因错误 cwd 与缺少依赖失败；按 [web README](../../../web/README.md) 使用 `web/.venv`、从 `web/` 目录复跑后，20 项通过、1 项因 Windows `WinError 1314` symlink 权限跳过。该结果仅验证 Web 目标文档解析器。
- 详细命令、环境、哈希、输出和边界见 [I-002 runtime fixture 结果](attachments/i-002-runtime-fixture-2026-07-19.md)。本轮没有改动 adapter 的 `verificationStatus`。

### 2026-07-19 · 收齐三宿主的 `/govern` 运行时调度证据

- 用户补充的 [Claude Code screenshot](attachments/claude-code-govern-runtime-2026-07-19.png)（SHA-256 `5B6D05DCC5555AE888EBADA8382A9A728505C59AF44095DC782E758AA46BE791`）显示 Claude Code `2.1.215` 在本仓库工作目录实际运行 `/govern`，并开始检索 `**/03-audit.md`；这补足了先前 headless probe 缺少的可观察 slash-dispatch 信号。
- 用户补充的 [Grok Build screenshot](attachments/grok-build-govern-runtime-2026-07-19.png)（SHA-256 `A3123997316830338985233E0A94C4F160D0D0BE3234225E3A9DB39400C22531`）显示本仓库工作目录中的 `/govern` 正在响应，并输出 goal-tree、`skills/`、canonical/mirror contract 与 S2 / I-002 门禁扫描结果。该 UI 证据与 `grok --version` 的 `0.2.103 (89c3d36fb6)` 共同固定本条 fixture；先前 `grok -p` 的 provider 502 仍保留为该 headless 调用配置的失败事实，不再被扩展为“Grok 宿主不能运行”。
- 已归档的 [Copilot runtime screenshot](attachments/copilot-vscode-govern-runtime-2026-07-19.png)（SHA-256 `BE9E28996BD4BB39DA75FA226B6225BB0C6462F33CD462F1F83B82B0601BA713`）和 [extension screenshot](attachments/copilot-vscode-extension-2026-07-19.png)（SHA-256 `7AC4B47EA2E6D2C49D91CE9BB65716F9EA46984D6700BC92D3708293FD9C274F`）记录 `/GOVERN GOAL-008` 的实际输出与 built-in `github.copilot-chat` 表面；本机 VS Code `1.129.1` 的内置 package manifest 进一步确认 `GitHub / copilot-chat` `0.57.0`、build `1`、`engines.vscode: ^1.129.1`，package JSON SHA-256 为 `4304D865FF058792AE0AA5304014534FA61447C08D966429FB4AD38A0CC17AC0`。因此 `code --list-extensions` 未列出它不表示扩展缺失。
- 将 canonical manifest 与 Skills mirror 的 Claude、Grok、Copilot 三条 `verificationStatus` 更新为 `verified`，并同步契约测试与说明。该状态严格指向上述 `0.1.0` current `/govern` fixture 的实际调度，不涵盖 `/audit`、manifest 解析、CI 或 release 验收。
- I-002 仍为 `required / collecting`，progress 保持 `20%`：本次完成的是首要入口的版本固定运行时行，完整矩阵/自动化重放和 I-003 发行证据尚未完成。

### 2026-07-19 · 用户确认当前最低可用并延期发布一致性门禁

- 用户在核对现有安装、契约测试与三宿主 current `/govern` runtime fixture 后，确认当前“可安装、可使用”的最低基线已经足够，不继续投入完整兼容矩阵、自动化重放、CI 或 tag/release。
- 记录 [D-004](01-decision.md#d-004--当前最低可用基线与发布一致性延期2026-07-19)：I-002、I-003 和上游 `F-005` 保留 `required`，状态改为 `deferred`；本轮没有接受 residual risk，也没有将其写为 `verified` 或关闭。
- I-002 的复核触发为首次支持新的宿主/版本或首次对外/可复现发布；I-003 与 F-005 的复核触发为首次对外/可复现发布。目标状态和进度保持 `active / 20%`。
- 本次治理记录变更后，运行 `python -m unittest skills/tests/test_skills_orchestrator.py -v`（30 passed）、`python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`（3 passed）及在 `web/` 使用根 `.venv` 的 Web 回归（20 passed / 1 Windows symlink-permission skipped）；`git diff --check` 无空白错误。

## 当前事实与门禁

- 已完成目标设立、范围记录、信息需求登记、高层路线图，以及 I-001 的行业实践收集、设计、schema/manifest、镜像同步和契约测试。
- I-001 已关闭；D-003 已冻结 I-002 的初始协议与声明/承诺范围，且三宿主已取得固定版本的 `/govern` 可观察 dispatch 通过。当前只据此声明最低可用；CI 重放、release tag 或阶段 5 发布验收尚未取得。
- I-002、I-003 与 F-005 均为 `deferred required`：它们不阻断当前最低可用范围，却在其复核触发或受影响门禁到达时阻断完整兼容验收、阶段 5 发布验收、阶段 7 验收与根目标关门。不得把 `govern` current fixture 的局部运行时通过扩大为 `/audit`、manifest 解析或产品发布通过。

## 进度评估

**20%**：首项成功标准已由 D-002 的 canonical schema/manifest、镜像和契约测试完成；I-001 已 `verified`。D-003 已收敛 I-002 的支持边界，三宿主 `govern` current 矩阵行也已获得可观察 dispatch 证据。完整矩阵、自动化重放、CI 与 I-003 未完成但已按用户裁决 `deferred required`，故不调整百分比，也不把三条局部运行时验证误作跨宿主兼容验收。
