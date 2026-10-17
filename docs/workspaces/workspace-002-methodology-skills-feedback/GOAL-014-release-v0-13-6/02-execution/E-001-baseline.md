---
id: E-001
goal: GOAL-014-release-v0-13-6
doc: execution-entry
title: S1 基线与证据校验
status: recorded
parent: GOAL-014-release-v0-13-6
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-001 · S1 基线与证据校验

## 基线

- 起始 HEAD：`f86b406`（`dev`），即 GOAL-013 S4 检查点；`origin/dev` 与之同步。
- `origin/main` 顶点仍为 `bbc8b99`（v0.13.5 回执 merge）；`dev` 领先 main 两个提交：`e37cad3`（GOAL-013 S2~S3 规则与消费面实现 + 12+4 运行证据）与 `f86b406`（S4 复核、归档可移植性修正与台账）。
- 远端最新正式 tag / Release：`v0.13.5`；`v0.13.6` 未被占用（`gh api repos/magicvr/goal-governance/tags` 回读）。本目标创建 GOAL-014，父目标 Root 子目标表与 `goal-tree.md` 同步。

## 证据校验（实际执行）

| 检查 | 命令 | 结果 |
|------|------|------|
| 运行证据一致性 | `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/goal-013-s3-2026-10-17-current` | `evidence consistency ok (16 evidence file(s))`，exit 0 |
| 兼容性报告 | `python scripts/compatibility_report.py --output artifacts/compatibility-report.json` | `coverage status: ready-for-release-evidence` |
| 镜像漂移 | `python scripts/stage_skills_mirrors.py --check` | 38 对一致，0 漂移 |
| Skills 回归 | `python -m unittest skills/tests/test_skills_orchestrator.py` | 45 tests OK |
| bootstrap 回归 | `python -m unittest discover -s docs/tests -p 'test_standalone_bootstrap.py'` | 5 tests OK |
| scripts 回归 | `python -m unittest discover -s scripts/tests -p 'test_*.py'` | 147 tests OK（7 skipped） |
| release rehearsal | `python scripts/release_evidence.py --mode rehearsal --run-checks --compatibility-report artifacts/compatibility-report.json --output artifacts/release-evidence.json` | `checks passed: True`，exit 0 |
| 空白检查 | `git diff --check` | 干净 |

本机环境说明（事实，不是放行依据）：上述测试与 rehearsal 以系统 Python **3.11.9**（与 CI 同主版本）执行。仓库 `.venv` 当前为 Python **3.14.6**，`release_evidence.py` 会优先选它作为子进程解释器；在该解释器下 `tempfile` 清理会对临时目录做 `chmod`，被本机 DSH 文件沙箱以 `WinError 5` 拒绝，导致 scripts 套件出现与代码无关的 95 个 cleanup error。该差异是本地沙箱限制，不是仓库缺陷；**不**修改仓库代码去掩盖它，也**不**把它当成 CI 结论——CI 在干净 runner 上用 3.11 判定。

## 边界

- 本轮未修改 `docs/` canonical 规则、`skills/` 入口或运行时代码，只新增/改写工作区目标台账与发布清单（清单在 S2）。
- 未创建 tag、未推送分支、未发布资产、未产生远端 CI 结果。S1 完成，`progress` 1/4 = 25%；S2 未开始。provider（I-003）尚未指定，按 D-001 §4 走 P-004 询问。
