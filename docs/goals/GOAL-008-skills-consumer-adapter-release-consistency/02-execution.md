---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.7.0
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

## 当前事实与门禁

- 已完成目标设立、范围记录、信息需求登记、高层路线图，以及 I-001 的行业实践收集、设计、schema/manifest、镜像同步和契约测试。
- I-001 已关闭；D-003 已冻结 I-002 的初始协议与声明/承诺范围，但尚未完成精确宿主版本的跨宿主/跨版本运行时测试、CI 重放、release tag 或阶段 5 发布验收。
- I-002 未关闭前，不通过受影响的兼容验收，也不把声明或承诺改写为产品运行时通过；I-003 与 F-005 未关闭前，不通过阶段 5 发布验收。

## 进度评估

**20%**：首项成功标准已由 D-002 的 canonical schema/manifest、镜像和契约测试完成；I-001 已 `verified`。D-003 已收敛 I-002 的支持边界，但兼容矩阵单元、宿主运行时证据与 I-003 仍未完成；下一步应执行已冻结范围内的 fixtures/运行时验证，不得把现有声明误作跨宿主兼容验收。
