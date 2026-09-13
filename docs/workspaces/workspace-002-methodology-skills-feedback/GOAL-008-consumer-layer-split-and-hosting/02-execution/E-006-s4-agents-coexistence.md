---
id: E-006
goal: GOAL-008-consumer-layer-split-and-hosting
doc: execution
title: S4 消费仓 AGENTS.md 受管标记块共存实施
status: recorded
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# E-006 · S4 消费仓 `AGENTS.md` 共存（2026-09-13）

## 事实

- **范围**：GOAL-008 纲领 **S4**。前置：S1～S3 完成；用户裁决共存模型 A 与 docs 范围（[D-009](../01-decision/D-009-s4-agents-coexistence.md)）。
- **用户指令**：本会话目标「推进工作区 2，目标 8，直到顺利关门」；S4 方案冻结前用户选定 A 模型。

## 产物

| # | 文件 | 改动 |
|---|------|------|
| 1 | `skills/agents_merge.py` | **新增**：受管标记块合并实现（嵌套感知的 `_outer_frame`、`merge_agents_text`、`block_payload`、`merge_agents_file`、CLI；半写标记 fail closed） |
| 2 | `skills/install.sh` | 新增 Python 探测（`PYTHON_BIN`）、`same_content`、`merge_agents_file`；`copy_file` 复用 `same_content`；`--claude` / `--codex` 两处 `AGENTS.md` 改为合并；无 Python 且已存在不同内容时 **fail closed** |
| 3 | `skills/install.ps1` | 新增 `$script:PythonBin` 探测与 `Merge-RuleAgentsFile`；两处 `AGENTS.md` 改为合并；无 Python 时同样 fail closed |
| 4 | `skills/update.py` | `managed_file_pairs` 移除根 `AGENTS.md`；新增 `agents_managed_conflict`（仅「区间被人工改写」算冲突）与 `merge_root_agents`；换包前把 legacy 整份安装迁入标记形态 |
| 5 | `skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md` | 规则源面加**外层受管标记**（整份规则进受管区间；内部规则级标记对作为嵌套） |
| 6 | `scripts/tests/test_agents_merge.py` | **新增** 12 例：新装、消费方内容保留、幂等、区间被改刷新、legacy 迁移（两种形态）、半写标记 fail closed、CLI fail closed、dry-run 不写、`managed_file_pairs` 不含根 AGENTS.md、消费方编辑不算冲突、人工改区间算冲突、`merge_root_agents` 保留消费方字节 |

## 验证结果（可复现）

| 命令 / 场景 | 结果 |
|-------------|------|
| `python -m unittest scripts/tests/test_agents_merge.py` | **12 tests OK** |
| `python -m unittest skills/tests/test_skills_orchestrator.py` | **43 tests OK** |
| `python -m unittest scripts/tests/test_skills_update.py` | **7 tests OK** |
| `python -m unittest discover -s skills/tests -p 'test_*.py'` | **89 tests OK** |
| `python -m unittest discover -s docs/tests -p 'test_*.py'` | **62 tests OK** |
| `powershell -NoProfile -ExecutionPolicy Bypass -File skills/tests/test_install_ps1_isolated.ps1` | **PASS**（隔离 `-All -InitWorkspace`：四入口 + core + 工作区骨架；无 GOAL 五件套；无 tech-stack） |
| 端到端（隔离临时仓，消费方已有自有 `AGENTS.md`） | 输出 `Merged managed block: …\AGENTS.md`；结果 `begin=True end=True consumerKept=True`（自有 `# Consumer rules` 保留在文件开头，长度 16446） |
| `git diff --check` | 洁净（0 命中） |

## S4 通过阈值逐条对照（[验收矩阵](../attachments/s1-acceptance-matrix.md) §3 / §2.C）

| 负例 | 期望 | 本轮结果 |
|------|------|----------|
| 1 消费仓已有自有 `AGENTS.md` | 自有内容保留（共存模型下） | **满足**：`test_consumer_content_outside_block_is_preserved`、端到端 `consumerKept=True` |
| 2/3 `docs/` 下自有文件与项目树 | 额外文件不改动 | 未在本轮改动写入策略（docs 范围 = 现状 + 说明）；保持既有行为 |
| 5 改过受管文件后再 update | 默认 fail closed；`--force-managed` 后按共存模型保留自有内容 | **满足**：`managed_file_pairs` 不再含根 `AGENTS.md`；消费方编辑**不再**算冲突（`test_consumer_edited_agents_is_not_a_managed_conflict`），人工改区间才冲突（`test_hand_edited_block_is_a_managed_conflict`） |
| 9 同包重复安装幂等 | 第二次不写入 | **满足**：`merge_agents_text` 幂等断言；`merge_root_agents` 第二次返回 `unchanged` |
| 7 非 Git 消费仓 | 安装成功（防回归） | 保持（安装器不调用 git） |
| 4/6/8/10/11（可配置根、大小写、只读、bootstrap rm -rf、点文件） | — | **未实现**，仍为 open（[D-009](../01-decision/D-009-s4-agents-coexistence.md) §5） |
| 12/13（`/commit` 负例） | — | 属 S5 |

## 事实边界

- **未**做真实消费仓冷启动/升级实测（属 S6 前的 A-006 F-001）；本轮证据为本仓测试 + 隔离临时仓端到端 + PowerShell 隔离安装测试。
- **未**改动 `docs/` 归属策略，未接入 `.goal-governance.json`（候选 C 不在本轮范围）。
- 端到端验证期间曾误以**仓库根**为目标运行一次安装器，导致根 `AGENTS.md` 被写入受管形态；已用 `git checkout -- AGENTS.md` 恢复，恢复后核对 S2 的 §6e 内容仍在（`:226/:228/:230`）。此为执行事故，已留痕。

## 检查点

- owned paths = `skills/agents_merge.py`、`skills/install.sh`、`skills/install.ps1`、`skills/update.py`、`skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md`、`scripts/tests/test_agents_merge.py`，以及本目标五件套。
- 未使用 `git add -A`。
