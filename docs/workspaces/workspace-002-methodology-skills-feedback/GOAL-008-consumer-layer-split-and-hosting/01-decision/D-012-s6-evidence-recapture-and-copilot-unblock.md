---
id: D-012
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-012
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-012 · S6 发布证据重捕获与 Copilot 阻断处置（2026-09-13）

**状态**：accepted

**触发**：按 [D-011](D-011-s6-release-scope-freeze.md) §4 执行 12 格 runtime 证据重捕获。首轮 `github-copilot-cli` 四格全部 `verdict=fail`（`400 unknown provider for model deepseek-v4-flash`），用户随后更新了本机 BYOK 环境变量并要求重试。

## 决定

1. **证据在 v0.13.3 目录重捕获，不改写历史**：`docs/releases/runtime/v0.13.3/` 12 格全部 `verdict=pass`；v0.13.2 快照保留为历史捕获点，不再作为当前验证引用。
2. **宿主版本如实记录**：claude `2.1.270`、grok `1.0.30`、copilot `1.0.75`。契约与矩阵的 `host.version` 同步为实测值，**不**沿用旧版本数字。
3. **Copilot 阻断的处置 = fix（而非 residual）**：
   - 根因：本机 BYOK 端点已不再提供 `deepseek-v4-flash`，而 Copilot CLI 仍在请求该模型（持久化 `settings.json` 的 `model` 与旧会话缓存可覆盖 `COPILOT_MODEL`）。
   - 处置：重放脚本 `copilot-cli-replay.ps1` 改为**显式传 `--model`**（优先首个位置参数，其次 `COPILOT_MODEL`），并记录实际使用的模型；捕获命令传 `--model gemini-3.8-flash-high`。
   - 验证：直接探测端点 `/v1/models` 与 `/v1/chat/completions`，确认 `gemini-3.8-flash-high` 与 `gpt-5.6-terra` 可用、`deepseek-v4-flash` 返回 400；随后四格全部 `pass`。
4. **失败证据不得被引用**：首轮失败的四份 JSON 与产物保留在 `v0.13.3` 目录中作为**过程记录**，但矩阵与契约的 `evidence` 指向**重试成功的同名文件**（已覆盖为 pass）。矩阵 `evidence` 列表中不含任何 fail 项；`compatibility_report.py` 与 `capture_runtime_evidence.py --check` 均可核对。
5. **不改必达/便利边界**：本决定不涉及 `/commit` 的契约位置（[D-010](D-010-s5-commit-entry.md) 维持）。
6. **不静默降级**：若再次出现宿主或端点失败，仍按 P-003 保持门禁未满足，不得以旧证据或其它宿主顶替。

## 为什么

- 用户已修正环境并明确要求重试；重试成功后问题性质从「环境阻断」变为「已修复」，应据实记为 `fixed` 而不是保留 blocked（保留 blocked 会让发布门禁永久无效）。
- 显式传 `--model` 是**可复现**的修法：它消除了「环境变量 vs 持久化配置 vs 会话缓存」三方覆盖的隐式依赖；否则同一脚本在不同机器上会给出不同结果。
- 宿主版本必须如实更新：v0.13.2 的证据绑定当时的 CLI 版本，本次实测版本不同，沿用旧数字会使契约与事实脱节。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 以 residual 保留 Copilot blocked 并发布 | 用户选择「不含残余」的发布路径；且阻断已可修复 |
| 只改环境变量、不重放脚本 | 持久化 `settings.json` 仍会覆盖，问题会在下次重捕获时复发 |
| 引用 v0.13.2 的 Copilot 证据充当当前验证 | 那些证据的 `behaviorSources` 已对当前规则面过期；引旧证据即失真 |
| 把失败的四份 JSON 从目录删除 | 会抹去真实发生过的失败过程；保留并在本条留痕更可审计 |
| 把 `/commit` 加入 12 格以「一并验证」 | 会把它升格为必达证据面，违反 D-002 §4 |

## 影响

- `docs/releases/runtime/v0.13.3/`：12 份 pass 证据 + 各自 `.d/` 原始 stdout/stderr。
- `docs/contracts/skills-consumer-compatibility-matrix.json`：`candidateRevision = v0.13.3`、三宿主 12 格 `runtime-verified`、宿主版本与证据路径更新。
- `docs/contracts/skills-consumer-contract.json`：copilot adapter `verificationStatus` 恢复 `verified`（与矩阵一致）。
- `docs/workspaces/workspace-001-goal-governance/GOAL-008-.../attachments/runtime/prompts/copilot-cli-replay.ps1`：显式 `--model` 支持。
- 测试：证据日期断言改为形状断言；矩阵覆盖断言改为「按矩阵自身状态推导未覆盖集合」，使合规重捕获不会误红、blocked 格不会被遗忘。
