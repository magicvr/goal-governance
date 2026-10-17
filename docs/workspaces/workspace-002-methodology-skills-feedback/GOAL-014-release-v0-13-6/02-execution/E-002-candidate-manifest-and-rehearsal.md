---
id: E-002
goal: GOAL-014-release-v0-13-6
doc: execution-entry
title: S2 候选清单、预演与严格门禁本地校验
status: recorded
parent: GOAL-014-release-v0-13-6
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-002 · S2 候选清单与预演

## 清单变更（检查点 `5de854d`，分支 `codex/release-v0.13.6`，父 `f86b406`）

- `CHANGELOG.md` 新增 `0.13.6` 节并把 `Unreleased` 复位为空；条目说明自动审计派发白名单与缺答阻塞规则、镜像同步、审计结论与证据复用边界，并明确发布身份仍需 main merge + annotated tag + strict evidence + 人工审批 + 资产核对建立。
- canonical 矩阵 `docs/contracts/skills-consumer-compatibility-matrix.json` 的 `candidateRevision` 改为 `v0.13.6`，三个 `evidenceScope` 改写为「由 GOAL-014 原样复用为 v0.13.6 候选基线，不建立新宿主运行」；`python scripts/stage_skills_mirrors.py` 同步 `skills/contracts/`，`--check` 38 对 0 漂移。
- 版本 pin 对齐 `v0.13.6`：根 `README.md`（bootstrap 与 GHCR 示例）、`skills/README.md`、`scripts/bootstrap/README.md`、`mcp/README.md`；`docs/releases/README.md` 的「本轮发版 pin」同步。`docs/README.md` 记为 **v0.13.6 发布候选**，最近正式基线仍写 `v0.13.5`，不提前声称已发布。
- 受影响断言同步：`skills/tests/test_skills_orchestrator.py` 与 `scripts/tests/test_release_evidence.py` 的 `candidateRevision` 期望值改为 `v0.13.6`。
- 运行证据 JSON、原始 stdout/stderr 与 fixtures **未**修改、未改名、未改捕获日期。

## 本地门禁结果（Python 3.11.9，与 CI 同主版本）

| 检查 | 命令 | 结果 |
|------|------|------|
| 镜像漂移 | `stage_skills_mirrors.py` + `--check` | 复制 1 对后 38 对一致，0 漂移 |
| Skills 回归 | `unittest skills/tests/test_skills_orchestrator.py` | 45 tests OK |
| bootstrap 回归 | `unittest discover -s docs/tests -p 'test_standalone_bootstrap.py'` | 5 tests OK |
| scripts 回归 | `unittest discover -s scripts/tests -p 'test_*.py'` | 147 tests OK（7 skipped） |
| 兼容性 | `compatibility_report.py` | `ready-for-release-evidence` |
| 运行证据 | `capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/goal-013-s3-2026-10-17-current` | 16 份一致 |
| rehearsal | `release_evidence.py --mode rehearsal --run-checks` | `checks passed: True` |
| strict release 预检 | 临时本地 annotated tag `v0.13.6`（不推送）+ `release_evidence.py --mode release --tag v0.13.6 --run-checks` | `release status: release-candidate`，`checks passed: True`，exit 0；随后删除本地临时 tag |

严格预检确认了 release 模式的全部硬条件：CHANGELOG 含 `0.13.6` 节、工作树干净、canonical/mirror 一致、coverage 无 uncovered、矩阵 `candidateRevision == v0.13.6`、四项内部检查全过。该临时 tag **未**推送、**未**发布，正式 tag 仍待 PR 合入 main 后在 merge commit 上创建。

## 边界与环境说明

- 本机 `.venv` 为 Python 3.14.6，`release_evidence.py` 会优先选它作为子进程解释器；在该解释器下 `tempfile` 清理会 `chmod` 临时目录并被本机 DSH 文件沙箱以 `WinError 5` 拒绝，导致与代码无关的 cleanup error。因此上述含子进程的检查在**临时将 `.venv` 移出**、回落到系统 Python 3.11.9 的条件下执行，执行后立即恢复；未修改仓库代码或测试来掩盖该差异。CI 在干净 runner 上用 3.11 判定，不受此限制。
- 复核（A-001 F-003）：指定 provider Grok Build 的独立会话**独立复现了同一限制**——它自己的 `release_evidence.py --mode rehearsal --run-checks` 也因 `.venv` 3.14.6 与同一沙箱拒绝而 `checksPassed` false（`install` 渲染写 `%TEMP%` 得 `Errno 13`、PowerShell `Write-Progress` 得 Win32 `0x5`、3.14 `tempfile` 清理得 `WinError 5`），而同一机器上系统 Python 3.11.9 直接跑三套 unittest 均 exit 0。两个独立会话都只在该解释器 + 沙箱组合下失败，进一步支持「环境限制，不是仓库缺陷」。结论：不为本机沙箱去改产品代码；本地严格预检与 S3 绑定预演以系统 3.11.9 / CI 干净 runner 为准。
- 未 push、未开 PR、未创建正式 tag、未发布；候选是否可放行取决于 provider independent 意见与 required 闭合情况（见 A 系列）。
