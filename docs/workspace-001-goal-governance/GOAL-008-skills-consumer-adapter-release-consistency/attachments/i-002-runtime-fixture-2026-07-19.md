---
id: I-002-runtime-fixture-2026-07-19
title: I-002 · 0.1.0 版本固定 Runtime Fixture 结果
status: active
parent: GOAL-008-skills-consumer-adapter-release-consistency
created: 2026-07-19
updated: 2026-07-19
version: 0.4.0
---

# I-002 · 0.1.0 版本固定 Runtime Fixture 结果

## 范围与判定规则

- **协议基线**：`0.1.0`；`previousSupportedProtocol: null`，所以没有 previous fixture，也不得伪造 `0.0.x`。
- **当前 fixture**：在项目根目录、已安装的 project skill 与 canonical contract 都存在时，以受限 headless 方式调用 `/govern GOAL-008`。
- **negative fixture**：验证治理入口不把 `previousSupportedProtocol: null` 改写为虚构 predecessor；这不表示外部宿主会解析 manifest。
- **证据尺度**：CLI 返回不等于 host runtime compatibility pass。只有精确宿主版本、安装路径或 built-in package 身份、fixture、环境、预期/实际输出均齐全，且能证明相应入口被实际消费时，才可把该 fixture 的 adapter 行标为 `verified`；这不自动覆盖其他入口、manifest 解析、CI 或 release。

## Fixture 身份与环境

| 项 | 值 |
|----|----|
| 执行时间（UTC） | `2026-07-19T10:49:22.4715108Z` |
| OS | Microsoft Windows 11 专业版 `10.0.26200` / AMD64 |
| canonical manifest SHA-256 | `519DCB7456065D4E475B6D3D3478D5F68215F701C7F7D932AAE4EC047ED7F51C` |
| schema SHA-256 | `AA18EFE1AE85D3A37678DA435B82E1E572E06AD1EA5FFCA84287195C7840D309` |
| Claude project `govern` SHA-256 | `4132FDC6DB73B5992EAC0B42CDA92452191A6444490758E9DBC1EA396D017D34`；与 `skills/install/claude/` source 相同 |
| Grok project `govern` SHA-256 | `E4703839674911D005FC9CFF9BA976473F32356CBBFB8DC8C3B2B08F4C48B33E`；与 `skills/install/grok/` source 相同 |
| Claude Code CLI | `2.1.215` |
| Grok Build CLI | `0.2.103 (89c3d36fb6)` |
| VS Code | `1.129.1` / commit `8a7abeba6e03ea3af87bfbce9a1b7e48fed567b8` / x64 |
| Copilot VS Code 插件 | [VS Code Chat screenshot](copilot-vscode-govern-runtime-2026-07-19.png)（SHA-256 `BE9E28996BD4BB39DA75FA226B6225BB0C6462F33CD462F1F83B82B0601BA713`）显示 `/GOVERN GOAL-008` 已实际进入 Chat 并生成 I-002 / A-006 摘要；[extension screenshot](copilot-vscode-extension-2026-07-19.png) 识别 `github.copilot-chat`；VS Code 内置 package manifest 的 `GitHub / copilot-chat` 为 `0.57.0`、build `1`、`engines.vscode: ^1.129.1`，SHA-256 `4304D865FF058792AE0AA5304014534FA61447C08D966429FB4AD38A0CC17AC0`。`code --list-extensions --show-versions` 未列出它是因为它为 built-in package，而非缺失。 |

## 执行矩阵

| consumer / fixture | 受限调用与实际结果 | 结论 |
|--------------------|--------------------|------|
| Claude Code CLI `2.1.215` / current | `claude -p`、`--no-session-persistence`、`--permission-mode plan`、`--max-turns 3` 返回 `RUNTIME-FIXTURE-CURRENT protocol=0.1.0 previous=null adapters=claude-code-cli,grok-build-cli,github-copilot-vscode outcome=discovery-not-acceptance`，exit `0`；随后用户提供的 [interactive screenshot](claude-code-govern-runtime-2026-07-19.png) 显示仓库 `/govern` 已实际开始检索 `**/03-audit.md`。 | 固定版本 current `/govern` dispatch `verified`；headless 输出仍不单独证明 manifest 被 Claude 解析，也不覆盖 `/audit`。 |
| Claude Code CLI `2.1.215` / negative | 同样受限调用，要求不虚构 predecessor；返回 `RUNTIME-FIXTURE-NEGATIVE previousFixture=not-applicable outcome=reject-fabricated-predecessor`，exit `0`。 | 与 D-003 的无上一版本边界一致；不是 previous runtime compatibility pass。 |
| Grok Build CLI `0.2.103` / current | `grok -p`、`--permission-mode plan`、`--max-turns 3`、`--no-subagents`、`--no-memory`、`--disable-web-search` 发起调用时，Responses API 返回 `502 Bad Gateway: unknown provider for model grok-build`。进程随后回显 prompt 并以 exit `0` 退出，不能按 exit code 判成功；随后用户提供的 [interactive screenshot](grok-build-govern-runtime-2026-07-19.png) 显示本仓库 `/govern` 正在输出真实的 goal-tree / SKILLS_PKG / S2 扫描。 | headless provider 配置仍为 `blocked` 子结果；固定版本交互式 current `/govern` dispatch `verified`，不得把前者扩大为 Grok 宿主不能运行。 |
| GitHub Copilot VS Code / current | 用户提供的 screenshot 显示 VS Code Chat 标题 `/GOVERN GOAL-008`，并输出 I-002 三类缺口与 A-006 摘要；工作区 VS Code 为 `1.129.1`。内置 `GitHub / copilot-chat` package manifest 已确认版本 `0.57.0`、build `1` 和 SHA-256。 | 固定版本 current `/govern` dispatch `verified`；不扩展到其他 Copilot 表面、`/audit` 或完整协议兼容验收。 |
| Web 目标文档解析器 / web-repository | 从 `web/` 使用仓库 `.venv` 执行 `python -m unittest discover -s tests -v`：20 项通过、1 项因 Windows `WinError 1314` 无法建 symlink 而跳过。 | Web 的只读 goal-document parser 行通过本地验证；它不是 adapter，也未读取 manifest。 |

## 可重放命令

```powershell
# Claude current / negative：用子 PowerShell 隔离 claude.ps1 的 exit 行为。
powershell -NoProfile -NonInteractive -Command '& claude -p $env:FIXTURE_PROMPT --no-session-persistence --output-format text --permission-mode plan --max-turns 3'

# Grok current：`grok-build-cli` 是适配器 ID，不是 API model；当前 endpoint 的可识别 model 显式固定为 `grok-4.5`。
# 实际调用失败时以 Responses API 错误为准，而非回显 prompt 或 exit code。
grok -p $prompt --model grok-4.5 --output-format plain --permission-mode plan --max-turns 3 --no-subagents --no-memory --disable-web-search --cwd <repo-root>

# Web：必须在 web/ 目录并使用项目 venv。
Push-Location web
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
Pop-Location
```

两条 Claude prompt 分别固定为 `i002-current-0.1.0` 的协议/adapter 边界和 `previousFixture=not-applicable` 的 negative 语义；执行时均明确禁止修改文件、shell 与网络访问。Grok 使用相同 current 语义，且额外禁用 web search、memory 与 subagents。

### Grok provider/model 防误用约定

- `grok-build-cli` 只表示兼容矩阵中的宿主适配器 ID；不得把它或 `grok-build` 作为 API model 传给 Grok Build。
- 本机当前 `GROK_MODELS_BASE_URL` endpoint 的测试主 model 为 `grok-4.5`，所以本目标的候选 headless 重放显式包含 `--model grok-4.5`。该参数只控制主采样；Grok 仍可能使用内置 `grok-build` 别名生成会话标题或辅助请求。本机用户配置虽存在以下路由覆盖，但 2026-07-19 的 streaming probe 中标题辅助请求仍返回 provider 502，不能把配置存在写成辅助链路已验证：

  ```toml
  [model.grok-build]
  model = "grok-4.5"
  base_url = "${GROK_MODELS_BASE_URL}"
  env_key = "XAI_API_KEY"
  api_backend = "responses"
  ```

  若 endpoint 或可识别 model 改变，必须先同步此覆盖、本约定、测试断言和实际环境证据。
- 主请求出现 `unknown provider`、模型相关 5xx 或无法确认实际 model 时，结果记为 `blocked`；CLI 的 exit `0` 或 prompt 回显不能覆盖主请求失败。若仅非必要辅助请求失败，而主请求 exit `0`、加载实际 skill、读取仓库来源并输出预期标记，可将对应入口记为通过，但必须在证据中保留辅助故障警告。

### 2026-07-19 · 自定义 endpoint 路由修正验证

- 显式传入 `--model grok-4.5` 的简单主请求进程 exit `0` 并返回 `GROK_MODEL_ROUTE_OK`，证明当前 endpoint 的主采样可用。
- 后续 `/govern` streaming probe 同样由主 model 成功完成 skill 加载、仓库读取和治理扫描，exit `0`；与此同时，stderr 仍记录会话标题辅助请求对 `grok-build` 的 `502 unknown provider`。因此主入口 dispatch 与辅助标题链路必须分开判定。
- 该验证不替代其余候选入口；每个 `/govern`、`/audit` 单元仍须各自形成可机读证据。

### 2026-07-19 · 候选机读 runtime evidence

- Claude Code `2.1.215`：`attachments/runtime/claude-code-cli-govern-2026-07-19.json` 与 `claude-code-cli-audit-2026-07-19.json` 均为 `pass`。两次调用仅开放 `Read,Glob,Grep`、使用 `permission-mode plan` 和 `--no-session-persistence`；stdout 为脱敏 transcript，不保留 thinking/signature 或完整工具结果正文。
- Grok Build `0.2.103 (89c3d36fb6)`：`attachments/runtime/grok-build-cli-govern-2026-07-19.json` 与 `grok-build-cli-audit-2026-07-19.json` 均为 `pass`。主 `grok-4.5` 调用完成实际 skill/仓库读取并输出 marker；可选 session-title 请求的 `grok-build` alias 502 保留为 warning，本机 `Request URL` 已脱敏。
- runtime evidence 由 canonical `docs/contracts/runtime-evidence.schema.json` 验证，并绑定行为源与 stdout/stderr SHA-256；matrix 当前只剩 Copilot 两个入口和 Web CI replay 共 3 个 uncovered。
- 具体 endpoint/model 配置仅属于本附件的本机候选证据，不进入根 `AGENTS.md` 的可复制通用规则。

## 补充：三宿主可观察 Slash Dispatch（2026-07-19）

| adapter / current fixture | 版本与环境锚点 | 预期 / 实际 | 归档证据与结论 |
|---------------------------|--------------|-------------|----------------|
| Claude Code CLI | Claude Code `2.1.215`；仓库 `C:\\Users\\magicvr\\Documents\\Code\\goal-governance` | 预期 `/govern` 发现并开始编排；实际显示 `/govern`、治理约束读取说明与 `**/03-audit.md` 搜索。 | [claude-code-govern-runtime-2026-07-19.png](claude-code-govern-runtime-2026-07-19.png)，SHA-256 `5B6D05DCC5555AE888EBADA8382A9A728505C59AF44095DC782E758AA46BE791`；`verified`（仅 current `/govern`）。 |
| Grok Build CLI | CLI `0.2.103 (89c3d36fb6)`；同一仓库；UI 同时显示模型标签 `Grok 4.5 Custom` | 预期 `/govern` 读取仓库并扫描门禁；实际显示已同步 goal-tree、`skills/` SKILLS_PKG、canonical/mirror contract 及 S2。 | [grok-build-govern-runtime-2026-07-19.png](grok-build-govern-runtime-2026-07-19.png)，SHA-256 `A3123997316830338985233E0A94C4F160D0D0BE3234225E3A9DB39400C22531`；`verified`（仅 current `/govern`）。 |
| GitHub Copilot VS Code | VS Code `1.129.1` / commit `8a7abeba6e03ea3af87bfbce9a1b7e48fed567b8`；built-in `GitHub / copilot-chat 0.57.0` build `1` | 预期 `/govern` 打开项目 wrapper 并产出编排扫描；实际 `/GOVERN GOAL-008` 输出 I-002 / A-006 摘要。 | [copilot-vscode-govern-runtime-2026-07-19.png](copilot-vscode-govern-runtime-2026-07-19.png)、[copilot-vscode-extension-2026-07-19.png](copilot-vscode-extension-2026-07-19.png)；`verified`（仅 current `/govern`）。 |

三条 `verificationStatus` 因上述补充证据更新为 `verified`，但 top-level `adapterCompatibilityStatus` 继续是 `declared`：这轮没有覆盖 `/audit`、自动化跨宿主重放、manifest 解析或发布证明。

证据落盘后的 canonical manifest 与 Skills mirror SHA-256 均为 `F49FE4A3C5BDBAC5E9DA6EDF180619E0F5CA175638E7B68CDF775E5A7D9019DA`；相对本附件第 26 行的初始 digest，该变化只写入三条 `verificationStatus`，不改变协议 `0.1.0`、`supportBaseline` 或任何 adapter 的声明/承诺范围。

## 结论与开放项

本次先记录 headless 与 Web 结果，后补齐三宿主可观察的 current `/govern` dispatch、Copilot built-in package 指纹和截图归档。因此三个 adapter 已在该**狭义 fixture**中为 `verified`。I-002 没有因此关闭：`/audit`、自动化跨宿主重放、manifest 解析和完整兼容矩阵仍未覆盖；I-003 的 CI / release 证据也仍开放。Grok 的 `502` 继续作为先前 headless provider 配置的失败记录，而非宿主能力结论。
