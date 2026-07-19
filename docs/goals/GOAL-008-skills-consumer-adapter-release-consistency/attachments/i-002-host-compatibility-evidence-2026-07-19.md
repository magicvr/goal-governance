---
id: I-002-host-compatibility-evidence-2026-07-19
title: I-002 宿主兼容与契约消费证据
status: active
parent: GOAL-008-skills-consumer-adapter-release-consistency
created: 2026-07-19
updated: 2026-07-19
version: 0.3.0
---

# I-002 · 宿主兼容与契约消费证据

## 问题与证据分层

I-002 要回答的是：哪些宿主/wrapper/Web 解析器的**实际版本**必须支持当前和上一协议版本，以及兼容矩阵与 fixtures 的边界。为避免把包装、结构测试和宿主运行时混为一谈，本附件使用三层证据：

1. **schema-valid**：实例按指定 JSON Schema dialect 应当被接受或拒绝；它不证明消费者会读取或接受实例。
2. **consumer-declared**：消费者的版本、入口和预期 fixture 被明确列入矩阵；它不等同于已执行。
3. **consumer-verified**：记录了精确宿主/消费者版本、fixture、环境、预期/实际结果与可重放的验证证据。只有这一层才能让对应矩阵单元为 `verified`。

访问日期均为 2026-07-19。外部页面只作为公开资料，不覆盖未记录的产品版本或运行时。

## 仓库可核对事实

| 候选消费者 | 仓库产物 / 入口 | 可核对证据 | 不能据此声称 |
|------------|----------------|------------|--------------|
| Claude Code | `.claude/skills/govern/SKILL.md`、`audit/SKILL.md`，`/govern`、`/audit` | [Skills README](../../../../skills/README.md) 的宿主表；[PowerShell 安装器](../../../../skills/install.ps1) 和 [Shell 安装器](../../../../skills/install.sh) 的复制路径；结构/隔离安装测试 | 某个 Claude Code 版本已运行并正确消费本协议，或 `AGENTS.md` 具有与 `CLAUDE.md` 相同的官方语义 |
| Grok Build | `.grok/skills/govern/SKILL.md`、`audit/SKILL.md`，`/govern`、`/audit` | [xAI Grok Build Skills 文档](https://docs.x.ai/build/features/skills-plugins-marketplaces) 明确从 `./.grok/skills/` 向上遍历到仓库根，并将 user-invocable skills 作为斜杠命令；本仓库安装路径与之匹配 | 本包已经在某个固定 Grok Build release 中端到端执行，或其协议消费结果已验证 |
| GitHub Copilot 默认 wrapper | `.github/copilot-instructions.md`、`.github/prompts/govern.prompt.md`、`audit.prompt.md` | 安装器默认复制 `/govern` 与 `/audit`；官方资料支持 custom instructions 与 prompt files | 所有 Copilot 表面、CLI 或 GitHub.com 都支持 prompt files，或任意版本均已验证 |
| GitHub Copilot advanced wrapper | `new-goal`、`log-decision`、`update-execution`、`write-audit` | 仅在 `--with-primitives` / `-WithPrimitives` 时复制 | 它们属于默认支持面或已与默认 wrapper 一起验证 |
| Web 只读解析器 | FastAPI GET `/`、`/goals/{id}` 与 legacy redirects | [Web README](../../../../web/README.md) 定义只读消费；[web/main.py](../../../../web/main.py) 版本为 `0.2.0`；[Web tests](../../../../web/tests/test_main.py) 覆盖有效/错误目标文档渲染 | Web 已直接消费 `skills-consumer-contract.json`，或具备跨宿主协议适配能力 |

`skills/tests/test_skills_orchestrator.py` 与 `docs/tests/test_standalone_bootstrap.py` 已证明 canonical/mirror、安装输出和本地结构语义；它们不是 Claude、Grok 或 Copilot 的产品运行时集成测试。

## 一手公开资料

| 来源 | 已核对事实 | 对 I-002 的作用与限制 |
|------|------------|----------------------|
| [Claude Code Skills](https://code.claude.com/docs/en/skills) | 官方文档把 project skill 位置列为 `.claude/skills/<skill-name>/SKILL.md`，并说明每个 skill 都需要 `SKILL.md` 入口。 | 支持 Claude wrapper 的路径/形状；页面没有给出本项目所需完整产品版本支持矩阵，也不能证明 `AGENTS.md` 语义。 |
| [Claude Code memory](https://code.claude.com/docs/en/memory.md) | `CLAUDE.md` 在会话开始时读取；页面对某些 project-rule 行为给出 `min-version` 注记，例如 `2.1.211`。 | 说明宿主行为可能有版本门槛，测试必须记录 `claude --version`；它不能替代本项目 skill 或协议的运行时验证。 |
| [GitHub Copilot repository custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) | `.github/copilot-instructions.md` 是仓库级指令位置；可有多个 `AGENTS.md`，最近者优先；Chat 的 References 可作为指令被使用的可观察证据。 | 支持 instructions 路径与某种可观察证据；没有给出本仓库 wrapper 的客户端版本承诺。 |
| [GitHub Copilot prompt files](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/your-first-prompt-file) | `.github/prompts/<name>.prompt.md` 可通过 `/name` 调用；prompt files 为 public preview，官方列出的可用宿主只有 VS Code、Visual Studio 与 JetBrains IDE。 | Copilot 行必须记录具体 IDE/Copilot 环境；不可把此资料扩展到未列出的 Copilot 表面。 |
| [JSON Schema Test Suite](https://github.com/json-schema-org/JSON-Schema-Test-Suite) | 测试套件供验证器实现者测试；test case 是 schema 与 tests，test 包含 instance 和 valid 布尔值。 | 适合作为 schema-valid fixture 结构；不是消费适配器运行时通过的证据。 |
| [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) | MAJOR 表示不兼容 API 变更，MINOR 表示向后兼容功能，PATCH 表示向后兼容修复。 | `protocol_version`、`host_release`、`parser_capability` 和 `wrapper_package_version` 必须分列，不可互相代替。 |
| [xAI Grok Build Skills, Plugins & Marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces) | Grok 从 `./.grok/skills/` 向上发现至仓库根；user-invocable skills 会作为 `/<skill-name>` 斜杠命令出现；Grok 也读取从 cwd 到仓库根的 `AGENTS.md` 文件。 | 为 `.grok/skills/govern|audit/SKILL.md` 与 `/govern|audit` 提供一手发现/命令语义；仍需固定 release 的实际运行时验证。 |
| [Introducing Grok Build](https://x.ai/news/grok-build-cli) | xAI 公告说明 `AGENTS.md`、plugins、hooks、skills 和 MCP servers “work out of the box”，并说明在 repo 中启动会拾取约定。 | 与细节文档相互印证；公告本身不替代版本化测试矩阵。 |

## D-003 冻结的声明/承诺范围

| 消费者 / 角色 | D-003 范围 | 协议范围 | 运行时状态 | 不代表 |
|---------------|------------|----------|------------|--------|
| Claude Code CLI | `committed` | `>=0.1.0 <0.2.0` | `unverified` | 尚未记录精确 `claude --version`、安装和 fixture 调用输出 |
| Grok Build CLI | `declared` | `>=0.1.0 <0.2.0` | `unverified` | 已确认 `.grok/skills/` 发现/斜杠命令语义，但尚不是固定 release 的端到端通过 |
| GitHub Copilot VS Code 插件 | `committed` | `>=0.1.0 <0.2.0` | `unverified` | 不扩展到 Copilot CLI、GitHub.com、Visual Studio 或 JetBrains；尚未记录精确扩展/VS Code 版本和调用输出 |
| Web 目标文档解析器 | 不作为 adapter | 不适用 | 本地解析/渲染测试另计 | 不读取 `skills-consumer-contract.json`，不因此宣称完整闭环或宿主兼容 |

`declared` 是纳入 canonical manifest 的已声明范围，`committed` 是当前支持承诺；两者均独立于 `verificationStatus`。因此 D-003 没有把 Grok Build 的官方 source-level 资料、Claude/Copilot 的安装产物或 Web 本地测试夸大为产品运行时验证。

核心文档/模板是可独立应用的基础方法论；Skills 与 Web 是互相独立、都建立在核心文档上的辅助闭环工具体系。Web 将来可扩展完整闭环，但当前范围仍限目标文档解析。

## 兼容矩阵实施字段

矩阵每行至少记录：

| 字段 | 含义 |
|------|------|
| `consumer_id` / `wrapper_id` | 例如 `claude-code-govern`、`copilot-audit`、`web-readonly-parser` |
| `host_release` | 实际 Claude Code、Copilot IDE/扩展或 Grok Build 版本；不得从 wrapper frontmatter 推导 |
| `parser_capability` | 实际可读取的文件路径、frontmatter、JSON Schema dialect 或协议特性 |
| `protocol_version` / `protocol_range` | canonical contract 所声明的协议版本与范围 |
| `fixture_id` / `fixture_class` | `current`、`previous`、`negative`、`installer` 或 `web-repository` |
| `schema_valid` | 仅 schema 层期望结果与验证器/测试证据 |
| `consumer_declared` | 该消费者是否正式列入支持范围，以及相关契约/决策链接 |
| `consumer_verified` | 精确版本、环境、运行 ID、预期/实际结果与证据链接 |
| `status` | `unknown`、`declared`、`verified` 或 `failed`；缺少运行证据不得写为 `verified` |

已冻结的 adapter 行是 Claude Code CLI `govern/audit`、Grok Build CLI `govern/audit` 与 Copilot VS Code `govern/audit`。Copilot opt-in advanced wrappers 和 Web 只读解析器仍可保留为测试/观察对象，但不属于 D-003 的 adapter 承诺行。

## 当前/上一版本与 fixture 边界

- 当前唯一可追溯协议实例是 canonical manifest 的 `0.1.0`。D-003 将其冻结为首个支持基线；它应有 current 正例、negative schema/semantic 例、canonical/mirror 例和安装输出例。
- D-003 明确 `previousSupportedProtocol: null`：没有可追溯的前一协议版本，不得伪造 `0.0.x` 或把文档 frontmatter 的旧 `version` 充作 predecessor，也不创建上一版本 fixture。
- Web fixture 应覆盖完整有效 goal tree/五件套、子目标、缺失 frontmatter/无效目标与路由结果；它只测试 Web 的目标文档解析职责，除非 D-003 明确要求 Web 读取 manifest。
- 外部宿主 fixture 必须包含宿主版本、安装路径、调用入口、fixture digest、期望行为与实际输出。仅检查文件被复制或 Markdown 包含关键字，不是 host runtime fixture。

## 审视结论与开放信息

D-003 已关闭 I-002 的首个/上一协议策略、已声明/当前承诺范围和 Web 是否为 adapter 的裁决问题，并已将这些结论写入 canonical manifest。I-002 仍为 `required / collecting`：

1. 每个 adapter 的精确 Claude Code CLI、Grok Build CLI、Copilot VS Code / 扩展 release 与运行环境仍未记录。
2. 需要逐行执行 `current` / `negative` host runtime fixture，并保存安装路径、调用入口、fixture digest、预期/实际输出和可重放证据。
3. `previous` fixture 明确不适用；这是 `null` 基线事实，不是缺失后可由任意历史版本填补的空位。
4. Web 继续以目标文档解析测试单独验证；除非未来有新决定，不要求或测试其读取 manifest。

因此 D-003 只放行范围内的矩阵/fixture 实施，不放行兼容验收；缺少运行证据的单元必须继续标为 `unverified` / `unknown`。

## Grok Build 证据更正（2026-07-19）

初始研究只从通用 `https://docs.x.ai/` 入口寻找资料，未取得 Grok Build feature 页面。用户提供 `https://x.ai/news/grok-build-cli` 后，公告及其官方文档链路证明了仓库内 `.grok/skills/` 的发现规则和 user-invocable slash-command 行为。本附件据此更正 Grok 行：它现在具有**一手 source-level discovery evidence**，但仍没有本项目在固定 Grok Build release 中的 `consumer-verified` 运行记录。
