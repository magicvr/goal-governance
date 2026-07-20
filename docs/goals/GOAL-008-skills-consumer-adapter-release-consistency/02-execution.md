---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-20
version: 1.6.0
---

### 2026-07-20 - Install GitHub Copilot CLI and complete CLI replay (历史记录)

- Installed with `npm install -g @github/copilot`. Node `v22.17.0` and npm `10.9.2` were present; `Get-Command copilot` points to `%APPDATA%/npm/copilot.ps1`; `copilot version` returns `GitHub Copilot CLI 1.0.71`. Raw installation facts are recorded in `attachments/copilot-cli-install-2026-07-20.md`.
- The non-interactive `-p/--prompt` surface was used with a read-only runner. File writes were denied and no VS Code or IDE plugin was used. Authentication was supplied to the process through `gh auth token` and is not stored in evidence.
- `/govern` and `/audit` both passed through `scripts/capture_runtime_evidence.py` with exit `0` and observed markers. JSON, stdout/stderr, and SHA-256 digests are recorded at `attachments/runtime/copilot-cli-govern-2026-07-20.json` and `attachments/runtime/copilot-cli-audit-2026-07-20.json`.
- Canonical/mirror contracts, compatibility matrix, negative fixtures, tests, and `skills/README.md` now use `github-copilot-cli`. The compatibility report is still `coverage: pending` with the Web parser CI replay as the uncovered cell.
- Copilot's two I-002 cells are closed for current runtime evidence, but I-002, I-003, and upstream F-005 remain open because Web CI, ready coverage, a clean candidate, and an authorized annotated release tag are still missing.

### 2026-07-20 - CI replay, annotated candidate, and close-out

- GitHub Actions run `29700051047` replayed the workflow on commit `8a33ecd21d9183a680c9c0d63e471469f5e515a8`; Ubuntu and Windows jobs both passed the contract, standalone, release-tool, Web parser, and whitespace checks.
- The run uploaded `skills-release-evidence-ubuntu` (artifact `8446173390`, archive SHA-256 `bb21872af6e0fcf2f1bd2c039c4a5da2fd64230800d17bafd199b3bfb08c56ff`) and `skills-release-evidence-windows` (artifact `8446177156`, archive SHA-256 `0920a213097d59e3105ccdc3ca4fe4170d8ce2762b65e888401106403c23e931`). Detailed report digests are recorded in `attachments/runtime/web-parser-ci-replay-2026-07-20.json`.
- Created and pushed annotated `v0.7.0` at the same commit. `scripts/release_evidence.py --mode release --tag v0.7.0 --run-checks --include-web` passed with `releaseStatus: release-candidate`, `coverageStatus: ready-for-release-evidence`, `checksPassed: true`, and a clean working tree. Summary: `attachments/runtime/release-candidate-v0.7.0-2026-07-20.json`.
- I-002 and I-003 are verified; GOAL-001 F-005 is responded to by the root close-out entry. No VS Code plugin evidence participates in the final candidate.

# 执行记录 · GOAL-008

### 2026-07-20 · 未发布工作区协议变更的运行时证据边界

- GOAL-010 修改了 `skills/install/claude/skills/govern/SKILL.md`，加入显式工作区上下文的读取与 fail-closed 校验；当前源摘要已不同于 `v0.7.0` 时的 Claude `/govern` runtime evidence。`scripts/compatibility_report.py` 因而拒绝将旧运行时输出用于当前源，报出 `runtime evidence behavior source is stale`。
- 该拒绝是预期的 release-evidence 安全栏：不得只改 JSON 摘要或报告来伪造新行为已在真实宿主运行。下一次发布包含该源时，先同步安装的宿主 skill，再捕获真实 Claude `/govern`（以及受影响的其他宿主）运行时输出/摘要，并据此重生成兼容性和 release evidence。
- GOAL-008 的 `v0.7.0` 历史关门结论不被当前未发布工作树改写；本条只记录未来 release 的复核触发条件，不将 GOAL-010 的 core/Skills 测试通过外推成新的宿主 runtime 或 release 证据。

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

### 2026-07-19 · 用户重启完整发布一致性关门路径

- 用户明确要求完整关门 GOAL-008，并确认在核心文档与 Skills 完整完成前不推进 Web 深化；据此记录 D-005，解除 D-004 对 I-002 / I-003 / F-005 的延期。
- 现场只读探测当前机器：`claude --version` 返回 `2.1.215 (Claude Code)`；`grok --version` 返回 `0.2.103 (89c3d36fb6)`；`code --version` 返回 `1.129.1` / commit `8a7abeba6e03ea3af87bfbce9a1b7e48fed567b8`。VS Code 内置 GitHub Copilot Chat package 为 `0.57.0` build `1`，其 `package.json` SHA-256 为 `4304D865FF058792AE0AA5304014534FA61447C08D966429FB4AD38A0CC17AC0`。
- `code --list-extensions --show-versions` 未列出 Copilot 是因为该包为内置扩展；版本以 VS Code 安装目录的 package manifest 为证，不将空列表误写为扩展缺失。
- 本次仅恢复 required 门禁、固定基线并开始实现自动化；尚未重新验证候选发行物的 `/govern` / `/audit` runtime，也未创建 CI、tag 或 release。

### 2026-07-19 · 实现兼容矩阵、CI 与发行证据 rehearsal

- 新增 canonical compatibility matrix 与 JSON Schema：`docs/contracts/skills-consumer-compatibility-matrix.json`、`skills-consumer-compatibility-matrix.schema.json`，并逐字节同步 `skills/contracts/` 镜像。矩阵固定 Claude Code `2.1.215`、Grok Build `0.2.103 (89c3d36fb6)`、VS Code `1.129.1` / Copilot Chat `0.57.0` 和 Web parser 行；三宿主 `/govern` / `/audit` 均保持 `pending-runtime-validation`，Web 保持 `pending-ci-replay`。
- 新增 `unsupported-protocol-0.2.0.json` 与 `fabricated-predecessor-0.0.0.json` 两类 negative fixtures，并在 canonical 与 Skills 镜像中同步；报告验证它们分别确实超出 `0.1.x` 支持区间和真实伪造 `previousSupportedProtocol`，不以文件名或存在性代替语义。
- 新增 `scripts/compatibility_report.py`：验证 contract/matrix schema、SemVer 区间、required entrypoints、负例语义、仓库内 evidence 路径、canonical/Skills 全文件镜像、当前 Git commit，并生成显式 uncovered 列表。
- 新增 `scripts/release_evidence.py`、`docs/releases/release-evidence.schema.json` 与 `docs/releases/README.md`：区分 `rehearsal` 与 `release-candidate`；正式候选要求 annotated `vX.Y.Z` tag 指向 HEAD、矩阵 `candidateRevision` 等于 tag、工作树干净、CHANGELOG 同版本节、coverage ready、镜像一致且内部固定检查全过。工具不推送 tag、不创建 GitHub Release。
- 新增 `.github/workflows/ci.yml`，Ubuntu 与 Windows job 都安装 `jsonschema`、运行 Skills、standalone、发行工具和 Web 回归，并生成 compatibility / rehearsal artifacts；新增 `scripts/requirements.txt`、`CHANGELOG.md` 与 `.gitignore` 的 `artifacts/` / `.claude/worktrees/` 忽略项。
- 首轮完整本地验证曾因 A-010 段落的 Markdown 行尾空格使 `diff-whitespace` 失败；已机械清除，随后 `git diff --check` 通过。

### 2026-07-19 · 收紧 rehearsal 可信度并核对 runtime 自动化边界

- 独立实现核验发现两类 rehearsal 假阳性风险：调用方可注入任意“通过” checks，以及 rehearsal 对传入 compatibility report 只比对 commit/contract/matrix digest。已修改 `generate_evidence()` 只执行内部 checks，并要求所有模式下传入报告与当前 HEAD 重新生成的 source、contract、matrix、mirror 和 coverage 全部一致。
- 将 compatibility matrix schema 的 `candidateRevision` 限定为 `unreleased`、40 位 Git commit 或 `v` 前缀 SemVer tag；`release-candidate` 要求其与 annotated tag 精确相等，并在 release evidence 的 `protocol.candidateRevision` 中显式记录。相关回归增至 19 项并全部通过。
- 以 D-006 固化历史 contract `verified` 与候选 readiness 分层；同步更新 matrix `evidenceScope`、Skills README、发行说明和 canonical hash 台账。当前 `docs/contracts/` 与 `skills/contracts/` 的 matrix/schema 字节一致。
- 只读 runtime 探测确认：Claude Code `-p /govern` 能识别入口但未产生足以证明真实 dispatch 的 headless 输出；Grok headless 调用仍因本机后端 `502 unknown provider for model grok-build` 失败；VS Code CLI 没有可替代 Copilot Chat 的 agent/skill dispatch 路径。因此 6 个宿主入口不能由本轮自动化关闭。
- 当前 compatibility report 仍为 `coverage.status = pending`，uncovered 为 Claude/Grok/Copilot 的 `/govern`、`/audit` 六个单元及 Web parser `pending-ci-replay` 一个单元；release evidence 仍只能是 `rehearsal`，无 annotated tag，工作树也尚未成为可发布的干净提交状态。
- 最终重放命令 `python scripts/compatibility_report.py --output artifacts/compatibility-report.json` 与 `python scripts/release_evidence.py --mode rehearsal --run-checks --include-web --compatibility-report artifacts/compatibility-report.json --output artifacts/release-evidence.json` 均 exit `0`。报告记录 commit `b7653c378d55f3f12d961fb636dd3774c627c696`、mirror `true`、coverage `pending` / 7 uncovered；rehearsal 记录 5/5 固定 checks 通过、`checksPassed: true`、`candidateRevision: unreleased`、`workingTree.clean: false`。
- 当前事实关闭 A-010 F-001（执行台账漂移）、F-004（verified 语义风险）与 F-005（过时摘要）；A-010 F-002、F-003 及 I-002、I-003、GOAL-001 F-005 保持开放 required。

## 当前事实与门禁

- 已完成目标设立、范围记录、信息需求登记、高层路线图，以及 I-001 的行业实践收集、设计、schema/manifest、镜像同步和契约测试。
- I-001 已关闭；D-003 已冻结 I-002 的初始协议与声明/承诺范围，且三宿主已取得固定版本的 `/govern` 可观察 dispatch 通过。当前只据此声明最低可用；CI 重放、release tag 或阶段 5 发布验收尚未取得。
- I-002、I-003 与 F-005 均为 `collecting / required`：D-005 已恢复完整关门路径。矩阵/negative fixtures/自动化/CI/rehearsal 已实施，Claude/Grok 四个候选 runtime 单元已验证；Copilot 两个入口与 Web CI replay 共 3 个 candidate 单元仍未覆盖，且无可追溯 release tag。它们阻断完整兼容验收、阶段 5 发布验收、GOAL-008 关门、阶段 6 Web 深化、阶段 7 验收与根目标关门。

## 进度评估

**20%**：首项成功标准已由 D-002 的 canonical schema/manifest、镜像和契约测试完成；I-001 已 `verified`。D-005 后的矩阵、negative fixtures、自动化、CI 与 rehearsal 是成功标准 2～4 的部分实施证据，但相应标准仍包含未关闭的真实宿主 runtime、ready coverage、CI 归档/干净候选和发行身份门禁；成功标准 5 尚无 tag/release。因此保持 20%，不以“工具已存在”替代验收完成。

### 2026-07-19 · 增加 Grok provider/model 防漂移保护

- 更新根目录 `AGENTS.md` 的运行时测试硬约束：明确 `grok-build-cli` 是适配器 ID，不是 API model；Grok headless 测试当前必须显式使用 `--model grok-4.5`。
- 更新 [I-002 runtime fixture](attachments/i-002-runtime-fixture-2026-07-19.md) 的 Grok 可重放命令，加入 `--model grok-4.5`，并记录 endpoint/model 变化时须先同步规则、断言和环境证据。
- 新增 `scripts/tests/test_grok_runtime_fixture.py`：断言重放命令使用 `grok-4.5`、不把 `grok-build` / `grok-build-cli` 作为 model，并保留历史 `unknown provider` blocked 事实。
- 本次只增加防误用约束与静态验证，没有重新声称 Grok runtime 兼容通过；GOAL-008 仍为 `active / 20%`，I-002/F-002 继续开放。

### 2026-07-19 · 建立机读 runtime evidence 并验证 Claude/Grok 双入口

- 新增 canonical/Skills 镜像 `runtime-evidence.schema.json`、`scripts/capture_runtime_evidence.py` 与 8 项专用回归：捕获器拒绝路径逃逸，以行为源和 stdout/stderr SHA-256 检测陈旧/篡改，`runtime-verified` 必须引用匹配单元和协议的有效 pass JSON；探针超时写为 `blocked`，本机请求 URL 可脱敏。
- Claude Code `2.1.215` 的 `/govern`、`/audit` 均在 `plan` 权限下只开放 `Read,Glob,Grep`，实际加载 `.claude/skills/.../SKILL.md`、读取对应核心 prompt/目标记录并输出 `CLAUDE_*_DISPATCH_OK`。归档 transcript 只保留 session init、工具调用、工具结果哈希/计数、可见文本与 process result，不保留 thinking/signature 或完整文件正文。
- Grok Build `0.2.103 (89c3d36fb6)` 的 `/govern`、`/audit` 均由主 model `grok-4.5` exit `0` 并输出 `GROK_*_DISPATCH_OK`；两份 JSON 继续保留可选 session-title 请求使用 `grok-build` alias 时的 502 warning，同时脱敏本机 `Request URL`，不将辅助失败扩大为主 dispatch 失败。
- 兼容矩阵 canonical/Skills 镜像已将 Claude/Grok 四个单元改为 `runtime-verified`；当前 compatibility report 为 `coverage: pending`，仅余 Copilot `/govern`、Copilot `/audit` 与 Web parser `pending-ci-replay` 共 3 个 uncovered。
- product-specific Grok endpoint/model 规则保留在 [runtime fixture 附件](attachments/i-002-runtime-fixture-2026-07-19.md)，不写入根 `AGENTS.md`；静态测试同时验证该范围边界。
- 最终验证：Skills 31 项、standalone 3 项、scripts 30 项、Web 20 项通过（1 项 Windows symlink 权限跳过）；完整 rehearsal 的 5 个内部 checks 全部通过，仍记录 `candidateRevision: unreleased`、coverage pending、工作树不干净和无 annotated tag。
- 本轮没有提交、push、tag 或 release，也没有修改目标 `status` / `progress`。I-002/F-002 因 3 个未覆盖单元继续开放；I-003/F-003 与 GOAL-001 F-005 同样保持 required/open。
