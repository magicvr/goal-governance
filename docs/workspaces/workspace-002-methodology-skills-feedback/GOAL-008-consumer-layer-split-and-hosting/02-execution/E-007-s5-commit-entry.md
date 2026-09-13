---
id: E-007
goal: GOAL-008-consumer-layer-split-and-hosting
doc: execution
title: S5 默认 /commit 便利入口实施
status: recorded
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# E-007 · S5 默认 `/commit` 便利入口（2026-09-13）

## 事实

- **范围**：GOAL-008 纲领 **S5**（S4→S5 串行，[D-006](../01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md)）。治理边界由 [D-002 §4](../01-decision/D-002-a001-response.md) 冻结，安装面与契约位置见 [D-010](../01-decision/D-010-s5-commit-entry.md)。
- **用户指令**：本会话目标「推进工作区 2，目标 8，直到顺利关门」。

## 产物

| # | 文件 | 改动 |
|---|------|------|
| 1 | `skills/install/claude/skills/commit/SKILL.md` | **新增**：`/commit` 壳（`user-invocable`，含 fail-closed 负例表与硬约束） |
| 2 | `skills/install/grok/skills/commit/SKILL.md` | **新增**：同文（Grok 面 `/commit`） |
| 3 | `skills/install/codex/skills/commit/SKILL.md` | **新增**：同文（Codex 面 `$commit`） |
| 4 | `skills/install/copilot/prompts/commit.md` | **新增**：Copilot wrapper（`role: convenience`） |
| 5 | `skills/install.sh` | 新增 `CLAUDE_COMMIT_SRC` / `GROK_COMMIT_SRC` / `CODEX_COMMIT_SRC`；3 处 `copy_file` 接入；新增 `CONVENIENCE_WRAPPER_NAMES=(commit)` 并并入 Copilot 安装循环；输出分离 `governance-must` 与便利入口两行 |
| 6 | `skills/install.ps1` | 新增三个 `*CommitSrc` 变量与 3 处 `Copy-RuleFile`；新增 `$convenienceWrapperNames = @('commit')` 并并入循环；输出两行 |
| 7 | `skills/README.md` | 新增「便利入口（非必达）」行与 `/commit` 契约位置说明（仍只在四个治理入口的必达字段内） |
| 8 | `docs/tests/test_file_l1.py` | 新增 3 个守卫：必达集不变（`ENTRYPOINT_NAMES` 仍四入口、契约 `hostEntrypoints` 无 `commit`）、四宿主面均产出壳、壳文本含 `git add -A` 禁止/owned path/fail closed/非必达边界/不 push |

## 验证结果（可复现）

| 命令 / 场景 | 结果 |
|-------------|------|
| `python -m unittest discover -s docs/tests -p 'test_file_l1.py'` | **10 tests OK** |
| `python -m unittest discover -s docs/tests -p 'test_*.py'` | **65 tests OK** |
| `python -m unittest discover -s skills/tests -p 'test_*.py'` | **89 tests OK** |
| `powershell -NoProfile -ExecutionPolicy Bypass -File skills/tests/test_install_ps1_isolated.ps1` | **PASS** |
| 端到端隔离仓 `install.ps1 -All -NonInteractive` | 四个治理入口 + `commit` 壳全部落盘（`.claude/.grok/.agents/skills/commit/SKILL.md`、`.github/prompts/commit.prompt.md` 均 `True`）；输出含 `Convenience entry: /commit (default-installed; NOT a governance-must entrypoint)` |
| `python scripts/stage_skills_mirrors.py --check` | `ok: skills mirrors match docs/`（37 对） |
| `git diff --check` | 洁净 |
| `python -m unittest discover -s scripts/tests` | 128 tests，**4 failures / 12 errors 全部为既有 `test_release_evidence.py` runtime 证据锚点过期项**（A-005 F-002，S6 重捕获），无 S5 相关新增失败 |

## S5 通过阈值逐条对照（[验收矩阵](../attachments/s1-acceptance-matrix.md) §2.D / §3）

| 阈值 / 负例 | 结果 |
|-------------|------|
| ① 已支持宿主可调用（四个宿主面均有壳） | **满足**：三个 SKILL.md + 一个 Copilot prompt；`test_convenience_commit_surface_ships_for_every_host`；端到端实测四路径均为 `True` |
| ② `docs/tests/test_file_l1.py` 必达等式仍成立 | **满足**：`test_convenience_commit_entry_never_joins_the_must_set`（`ENTRYPOINT_NAMES` 仍四入口；契约 `hostEntrypoints` / `files.entrypoints` 均无 `commit`）；docs 65 OK |
| ③ 契约中 `commit` 不进入必达字段 | **满足**：未改契约 JSON/schema；断言守卫 |
| ④ 非完整安装 MUST / 非治理必达 / 非 checkpoint 替代 | **满足**：壳文本与 README 明示；`test_convenience_commit_contract_forbids_unsafe_staging` |
| ⑤ 负例 fail closed（无改动、非 Git、验证失败、hook 拒绝、detached HEAD、用户禁用、越界、既有用户改动、push 禁止） | **满足（契约文本层）**：四个壳均含负例表与硬约束；行为实测属 S6 |
| ⑥ 缺 `commit` 时安装仍判完整 | 结构上成立（未进入 MUST/必达字段）；实测登记 S6 |
| ⑦ 相对化守卫覆盖新壳 | **满足**：新壳不含 `docs/` 绝对硬编码（守卫测试 `test_consumer_surface_relativeization.py` 89 tests 全绿范围内通过） |

## 事实边界

- 未做**真实宿主调用** `/commit` 的行为验证（属 S6 cross 回归 / A-005 F-001）。
- 未改 `docs/contracts/**`（保持四入口必达）；未改 MCP 工具集。
- `skills/update.py` 未额外改动：S4 之后新壳由目录枚举自动纳入托管面。

## 检查点

- owned paths = 4 个新增壳、`skills/install.sh`、`skills/install.ps1`、`skills/README.md`、`docs/tests/test_file_l1.py`，以及本目标五件套。
- 未使用 `git add -A`。
