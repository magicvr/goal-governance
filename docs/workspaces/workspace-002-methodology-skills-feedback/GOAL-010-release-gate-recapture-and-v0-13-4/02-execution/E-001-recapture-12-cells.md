---
id: E-001
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: execution
title: 12 格 L3 宿主证据在 v0.13.4 目录重捕获
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# E-001 · 12 格 L3 宿主证据重捕获（2026-10-01）

## 范围与方法

- **落点**：`docs/releases/runtime/v0.13.4/<consumer>-<entrypoint>-2026-10-01.json` 与各自 `.d/`（原始 stdout/stderr）。
- **矩阵**：3 宿主 × 4 治理入口 = **12 格**（`govern` / `audit` / `vision` / `vision-audit`）。
- **探针 corpus 未改**：沿用 GOAL-008 冻结的 prompt 文件（`claude-*` / `grok-*` / `copilot-cli-*`），
  hash 与 v0.13.3 记录值一致。
- **behaviorSources**：每格两项 —— `AGENTS.md` 与 `skills/prompts/00-govern-orchestrator.md`
  （与 v0.13.3 相同口径，可对照过期的旧锚点）。
- **驱动**：`scripts/capture_runtime_evidence.py`（未改动）。断言策略 = 默认
  `marker+entrypoint+nontrivial-stdout@1`。

## 结果

| 宿主 | 实测版本 | 模型 | 格数 | verdict |
|------|----------|------|------|---------|
| claude-code-cli | `2.1.285` | `gpt-6.1-sol`（本机代理） | 4 | 全部 `pass` |
| grok-build-cli | `1.0.44` | `grok-4.6` | 4 | 全部 `pass` |
| github-copilot-cli | `1.0.75` | `gemini-3.8-flash-high`（BYOK） | 4 | 全部 `pass` |

每格满足：`exitCode = 0`、marker 实际出现在 stdout、非平凡 stdout、`behaviorSources` 与
当前树哈希一致。

## 过程偏差（如实记录）

重捕获不是一次跑通。以下是实际发生过的失败与处置；**失败证据未留在最终目录内**，因为
最终目录只允许放被矩阵引用的 `pass` 捕获（与 [D-012]（v0.13.3 先例）一致的做法：
失败件保留为过程记录，但不得被矩阵引用）。失败原因逐条如下。

| # | 现象 | 根因 | 处置 |
|---|------|------|------|
| 1 | Claude 4 格 `marker=False`，stderr 报 `unrecognized_model` | 用户 settings 的 `ANTHROPIC_BASE_URL` 带 `/v1`，CLI 再拼 `/v1/messages` → 实际打到 `/v1/v1/messages` 并 404；且默认模型别名在本机已不可用 | 以 `--settings` 覆盖 base URL（去掉末尾 `/v1`），并显式 `--model` |
| 2 | marker 出现在落盘 stdout 里，却被判为未观测 | 运行器把 marker 前缀写成小写（`claude_…` / `grok_…`），断言要求全大写 | 修正运行器 marker 生成（**运行器缺陷，不是证据或产品问题**） |
| 3 | Grok 4 格 exit 1，`Couldn't create session: Permission denied (os error 5)` | 沙箱拒绝对工作区外写盘，而 Grok 在 `~/.grok` 下建 session | 以 `GROK_HOME` 把 home 重定位到工作区内，并复用真实 `auth.json`；重跑 4/4 `pass` |
| 4 | Copilot 4 格未启动 | 运行器用了 `copilot-<entrypoint>.txt`，实际文件名为 `copilot-cli-<entrypoint>.txt` | 修正运行器文件名解析 |
| 5 | Copilot 4 格 exit 1，`Failed to append to JSONL … .copilot\session-state\…` | 同 #3，Copilot 在 `~/.copilot` 下持久化 session | 以 `COPILOT_HOME` 重定位 home，并带过本地 `settings.json` / `config.json` |
| 6 | Copilot 4 格 `marker=False`，但落盘 stdout 里含 marker | 运行器把 Copilot 的 marker 写成 `COPILOT_<EP>_DISPATCH_OK`；冻结 corpus 的写法是 **`COPILOT_CLI_<EP>_DISPATCH_OK`**（含 `CLI` 段） | 修正运行器 marker（**运行器缺陷**） |
| 7 | 同上，落盘 stdout 出现乱码、marker 找不到 | 控制台代码页 936；node 系宿主把非 ASCII 输出按 cp936 写入管道，Python 再按 UTF-8 解码 → 双重编码 | 运行器显式把控制台与宿主输出编码设为 UTF-8（`[Console]::OutputEncoding` + `chcp 65001`），并对 Python 设 `PYTHONUTF8=1` |
| 8 | Copilot 的 `-File` 调用被拒 | 本机执行策略不允许未签名脚本 | 运行器的 `powershell.exe -File` 调用补 `-ExecutionPolicy Bypass` |

失败件（#1～#7 产生的 JSON）已在最终一轮前删除；最终目录内的 12 份 JSON 全部为 `pass`。
与 v0.13.3 的做法对照见同目录 [D-012]（v0.13.3 把失败件保留为过程记录但矩阵不引用）；
本轮的失败件在重跑覆盖时即被删除，因此目录内不含 fail 件。逐条失败事实以本节表格为准。

## 被矩阵引用

`docs/contracts/skills-consumer-compatibility-matrix.json` 的 12 格 `evidence` 全部指向本目录，
`candidateRevision = v0.13.4`，三宿主 `host.version` 改为上表实测值（见 [E-002](E-002-test-realignment-and-manifest.md)）。

## 验证命令

```bash
python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.4
python scripts/compatibility_report.py --output artifacts/compatibility-report.json
python scripts/release_evidence.py --mode rehearsal --run-checks \
  --compatibility-report artifacts/compatibility-report.json \
  --output artifacts/release-evidence.json
```

结果见 [E-003](E-003-regression-gates-and-release.md)。

## 复现 Claude 格所需的临时覆盖文件（A-002 F-001）

Claude 4 格的 `invocation.command` 引用了工作区根的 `.gg-probe-settings.json`，该文件是
**一次性探针配置**，用完即删、不入库。要在干净检出上重放这 4 格，需先在工作区根重建它：

```json
{ "env": { "ANTHROPIC_BASE_URL": "http://<你的代理主机>:<端口>" } }
```

要点：`ANTHROPIC_BASE_URL` **不要**带结尾的 `/v1`（Claude Code CLI 会自行拼 `/v1/messages`；
带了就会打到 `/v1/v1/messages` 并 404）。独立审计（A-002）已判定这不构成「证据不可复现」
required——L3 门禁核的是落盘 stdout/stderr 与 `behaviorSources`，A-002 已 12/12 独立复算通过；
残余范围仅限「命令级原样重放」，按 `accepted-residual` 闭合（见 [A-003](../03-audit/A-003-response-a002.md)）。
