---
id: E-003
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: execution
title: 回归、门禁与发布产出
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# E-003 · 回归、门禁与发布产出（2026-10-01）

## 1. 门禁结果（本机，Python 3.11.9）

| 命令 | 结果 |
|------|------|
| `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.4` | `evidence consistency ok (12 evidence file(s))` |
| `python scripts/compatibility_report.py --output artifacts/compatibility-report.json` | `coverage status: ready-for-release-evidence`（exit 0） |
| `python scripts/release_evidence.py --mode rehearsal --run-checks --compatibility-report … --output artifacts/release-evidence.json` | `release status: rehearsal`、`checks passed: True`（exit 0） |
| `python -m unittest skills/tests/test_skills_orchestrator.py` | `Ran 45 tests` → **OK** |
| `python -m unittest discover -s docs/tests -p test_standalone_bootstrap.py` | `Ran 3 tests` → **OK** |
| `python -m unittest discover -s scripts/tests -p test_*.py` | `Ran 145 tests` → **OK (skipped=7)** |
| `python scripts/stage_skills_mirrors.py --check` | `ok: skills mirrors match docs/`（37 对，0 漂移） |
| `git diff --check` | exit 0（仅 CRLF→LF 归一化提示，非空白错误） |

rehearsal 内部四项检查全部 `passed: True`：
`skills-contract-tests`、`standalone-bootstrap-tests`、`release-evidence-tool-tests`、`diff-whitespace`。
`annotatedTag` 与 `tagObject` 均为 `null`，`releaseStatus: rehearsal`——未把 rehearsal 写成发布。

## 2. 本机环境限制（如实记录，不构成发布门禁降级）

- 工作区 `.venv` 是 **Python 3.14**。本机受限临时目录（`…\Temp\dsh-*`）不允许
  Python 3.14 `tempfile` 清理时使用的 `chmod(follow_symlinks=False)`，导致用 `.venv`
  跑 fixture 测试时出现大量 teardown `PermissionError`（93 errors / 145），**测试本身并未失败**。
- 已单独验证：同一临时目录下 Python 3.11 的 `tempfile.TemporaryDirectory` 正常，3.14 报
  `PermissionError [WinError 5]`。GitHub CI 的两个 runner 都用 **Python 3.11**（`actions/setup-python@v5`），
  因此该现象**不影响 CI**。
- 为跑通本机 rehearsal，临时把 `scripts/release_evidence.py::_python_with_imports` 的解释器
  优先级改为「先 `sys.executable`」，跑完**已用 `git checkout --` 还原**（`git status` 无该文件改动），
  未进入任何提交。

## 3. 内容变更清单

- 新增：`docs/releases/runtime/v0.13.4/`（12 份证据 + 12 组 `.d/`）、
  `GOAL-010-release-gate-recapture-and-v0-13-4/` 五件套与三个 ledger 目录、
  `GOAL-001-*/01-decision/D-011-create-goal-010.md`。
- 修改：`CHANGELOG.md`、`docs/README.md`、`docs/releases/README.md`、
  `docs/contracts/skills-consumer-compatibility-matrix.json`（+ stage 镜像）、
  `README.md`、`skills/README.md`、`scripts/bootstrap/README.md`、`mcp/README.md`、
  `skills/tests/test_skills_orchestrator.py`、`scripts/tests/test_release_evidence.py`、
  `goal-tree.md`、`GOAL-001-*/00-meta.md`、`GOAL-001-*/01-decision.md`。
- 明确**未**改：`AGENTS.md`、`skills/prompts/00-govern-orchestrator.md`、
  `skills/install.ps1`、`skills/render_managed.py`、`scripts/capture_runtime_evidence.py`、
  `docs/architecture/**`、`docs/templates/**`、`docs/vision/alignment.md`。

## 4. independent 审计（S3 出口）

- provider：本地 **grok build CLI**，模型 `grok-4.6`（用户 2026-10-01 书面改派；原定本地 codex CLI 在本机沙箱下无法初始化）。
- 结论：**A-002 `pass`，开放 required = 0**，5 条 recommended。审计者独立复算 12 格哈希 / marker / 断言、矩阵镜像逐字节、证据目录卫生与台账一致性，并亲眼复现了 Python 3.14 的 tempfile 现象。
- 响应：[A-003](../03-audit/A-003-response-a002.md) 按 3 `fixed` / 1 `accepted-residual`（F-001 命令级重放残余，用户已确认继续发布）/ 1 `fixed` 闭合；其中 F-003、F-004、F-005 是本轮**真实台账与措辞缺陷**，已在本提交内改正。
- 无意见冲突。

## 5. 尚未发生（不得写成已完成）

- PR 创建与 `dev` → `main` 合并。
- annotated tag `v0.13.4` 的创建与推送。
- `skills-pack-release.yml` 的 pack / publish run、Environment `release` 审批、Release 资产上传与核对。

以上三步完成后须在 `02-execution` 增补条目，并把发布产出核对写进后续审计。
