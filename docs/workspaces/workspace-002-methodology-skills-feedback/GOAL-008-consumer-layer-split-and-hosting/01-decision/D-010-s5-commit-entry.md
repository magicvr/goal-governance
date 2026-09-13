---
id: D-010
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-010
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-010 · S5 落地：`/commit` 便利入口的安装面与契约位置（2026-09-13）

**状态**：accepted

**触发**：治理边界已由 [D-002 §4](D-002-a001-response.md) 冻结（便利可选、非 MUST、非必达、非 checkpoint 替代），VP-004 入口面同向；S1 盘点（I-004）确认 `/commit` **只在 monorepo 自用 prompt 中存在**、四个安装源目录均无壳，且「默认安装但不入必达集」在契约层缺表达位。

## 决定

1. **四个宿主面默认安装**：新增
   - `skills/install/claude/skills/commit/SKILL.md`
   - `skills/install/grok/skills/commit/SKILL.md`
   - `skills/install/codex/skills/commit/SKILL.md`
   - `skills/install/copilot/prompts/commit.md`
   安装器在 `--claude` / `--grok` / `--codex` / `--copilot`（及 `--all`）时**默认**写入对应宿主面；`/commit` 与 `$commit` 可直接调用。
2. **契约位置 = 不进入必达字段**：`docs/contracts/skills-consumer-contract.json` 的 `hostEntrypoints` 与 `deliveryChannels[files].entrypoints` **保持四入口不变**；`/commit` 的「默认安装但不入必达集」表达位落在
   - `skills/README.md` 的便利入口行 + 契约位置说明，
   - `docs/tests/test_file_l1.py` 的**机读守卫**（`test_convenience_commit_entry_never_joins_the_must_set`）。
   **不**改契约 schema——schema 变更是消费面数据结构变更，成本高且非本阶段必要；用断言把边界钉死，等价且可核对。
3. **命令契约**（写入四个壳）：先看 `git diff --cached --name-status` → 归属不清即停止报告 → 仅按显式 owned paths `git add --` → `git diff --cached --check` → 中文 Conventional Commits（`feat, fix, docs, style, refactor, test, chore`，≤50 字）→ `git commit -m` → 回显提交 ID 与暂存范围。
4. **fail closed 负例**（全部写入壳文本）：既有用户改动或不可分离、owned path 越界、`--check` 失败、无改动、非 Git 仓库、hook 拒绝/锁/签名失败、detached HEAD / rebase / 冲突、用户禁用 → 停止报告，不覆盖、不回退、不夹带；**禁止** `git add -A` / `git add .`；**不得** `git push`；**不得**以 commit 作为治理放行依据。
5. **默认面与必达面在安装输出中分离表达**：安装器打印 `governance-must` 与 `Convenience entry: /commit (default-installed; NOT a governance-must entrypoint)` 两行，避免读者把便利入口误读为必达。
6. **不再新增契约字段、不改 MCP 工具集**：`/commit` 不进 MCP（`mcp/entries.py` 保持四工具）。

## 为什么

- 「默认提供」必须真的默认产出，否则 FB-009 未解决；因此四个宿主面都要有壳，且安装器默认清单要带上它。
- 但**不得**顺手把它写进必达字段：那会把便利入口升格为治理 MUST，与 D-002 §4 和 VP-004 入口面直接冲突，也会让 `test_file_l1.py` 的必达等式失效。
- 用机读断言而非 schema 变更来固定边界，是因为断言能在 CI 里**主动阻止**未来的越界改动，而 schema 变更只表达现状、且提高消费面升级成本。
- 负例写进壳文本（而不只写在目标记录里）才能让「AI 在消费仓调用 `/commit`」时真正看到 fail-closed 要求。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 把 `commit` 加进 `hostEntrypoints` / `ENTRYPOINT_NAMES` | 直接违反 D-002 §4 与 VP-004 入口面；并会破坏四入口机读等式与必达语义 |
| 默认清单与 `--with-primitives` 共用一条列表 | 会把便利入口与「进阶填表原语」混为一谈；两者语义不同（一个是便利提交，一个是治理原语包装） |
| 改契约 schema 新增 `convenienceEntrypoints` | 消费面 schema 变更成本高、需兼容处理；本轮以 README + 断言达到同等可核对性 |
| 只装 Copilot 面（沿用 monorepo 先例） | FB-009 期望「已支持宿主默认可调用」；只装一面会让 `/commit` 在 Claude/Grok/Codex 上缺失 |
| 让 `/commit` 复用 `/govern` 的 checkpoint 实现 | 会使便利入口耦合编排状态；D-002 §4 明确禁止替代 checkpoint |

## 影响

- 新增 4 个安装源壳；`skills/install.sh`（3 处 copy + COPILOT 便利清单 + 输出两行）与 `skills/install.ps1`（3 处 copy + `$convenienceWrapperNames` + 输出两行）接入。
- `skills/README.md` 新增便利入口行与契约位置说明。
- `docs/tests/test_file_l1.py` 新增 3 个守卫（必达集不变、四宿主面均产出、壳文本含 fail-closed 契约）。
- `skills/update.py` 的托管枚举按目录自动纳入新壳（S4 后托管语义已按区间/枚举处理），无需额外改动。
- 未改契约 JSON/schema；未改 MCP 工具集；未新增 MUST。
