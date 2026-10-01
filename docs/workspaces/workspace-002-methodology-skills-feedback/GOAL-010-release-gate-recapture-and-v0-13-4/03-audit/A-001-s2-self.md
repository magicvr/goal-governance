---
id: A-001
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: audit
title: S2 实施自查（证据重捕获与清单修正）
source: self
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# A-001 · S2 实施自查（self · 2026-10-01）

| 项 | 值 |
|----|-----|
| source | `self` |
| scope | S2：12 格证据重捕获、矩阵与清单修正、containment 测试对齐 |
| verdict | **conditional** |

## 成果（可核对）

| 主张 | 证据 |
|------|------|
| 12 格证据在 v0.13.4 目录重捕获且全部 `pass` | `docs/releases/runtime/v0.13.4/`；`capture_runtime_evidence --check` → `ok (12 evidence file(s))` |
| 矩阵改指新目录且 `candidateRevision = v0.13.4` | `docs/contracts/skills-consumer-compatibility-matrix.json`；`compatibility_report` → `ready-for-release-evidence` |
| 三处安装 pin 与 GHCR 示例指向 `v0.13.4` | `README.md`、`skills/README.md`、`scripts/bootstrap/README.md`、`mcp/README.md`、`docs/releases/README.md` |
| containment 测试在项目内相对安装下成立，且保留「拒绝二次 init」原意 | `test_init_workspace_refuses_existing_path` 单测 OK；断言仍为「首次 0 / workspace.md 落盘 / 第二次非 0 且命中 `already exists\|refuse`」 |
| 镜像 0 漂移 | `stage_skills_mirrors.py --check` → `ok: skills mirrors match docs/`（37 对） |
| 门禁转绿 | [E-003](../02-execution/E-003-regression-gates-and-release.md)：rehearsal `checks passed: True`；三套测试 45 / 3 / 145 全绿 |

## 偏差与风险（未闭合）

| ID | 级别 | 主张 | 证据 | 影响门禁 |
|----|------|------|------|----------|
| F-001 | recommended | 探针运行器是本轮新写的临时脚本，**未入库**；重捕获的逐条过程（含 7 次失败与处置）只落在 [E-001](../02-execution/E-001-recapture-12-cells.md)，别人无法用同一脚本一键复现 | E-001 §过程偏差；仓库无该脚本 | 不阻断发布；影响「下次重捕获」的效率与可复现性 |
| F-002 | recommended | 本机 rehearsal 需临时调整 `release_evidence.py` 的解释器优先级（`.venv` Python 3.14 在受限临时目录下 `tempfile` 清理失败）。脚本已还原，但该环境差异只在本条与 E-003 记录，未固化为防再犯检查 | E-003 §2 | 不阻断发布（CI 用 Python 3.11） |

## 未发现问题的项

- 证据 `behaviorSources` 与当前树一致（`--check` 12/12）。
- 未把 rehearsal 写成已发布（`releaseStatus: rehearsal`、`annotatedTag: null`）。
- `AGENTS.md`、编排提示、安装器与捕获器脚本未被改动，因此不会让新证据当场过期。

## 我不确定 / 无法核对的项

- 发布产出（PR、merge、tag、workflow、资产核对）本轮尚未发生，不在本意见范围。
- 消费方实际安装体验未在本轮重放。
