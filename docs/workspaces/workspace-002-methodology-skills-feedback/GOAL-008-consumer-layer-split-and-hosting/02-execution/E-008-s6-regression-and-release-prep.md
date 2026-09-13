---
id: E-008
goal: GOAL-008-consumer-layer-split-and-hosting
doc: execution
title: S6 回归、证据重捕获与发布准备（首轮）
status: recorded
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# E-008 · S6 首轮：回归、证据重捕获与发布准备（2026-09-13）

## 事实

- **范围**：GOAL-008 纲领 **S6**（回归、审计与发布）。前置：S1～S5 完成；用户裁决 S6 **含正式发布**、**分轮推进不开残余**。
- **发布范围冻结**：[D-011](../01-decision/D-011-s6-release-scope-freeze.md)（I-006）。
- **证据与 Copilot 处置**：[D-012](../01-decision/D-012-s6-evidence-recapture-and-copilot-unblock.md)。

## 本轮完成

### 1. 全量回归（全部通过）

| 套件 | 结果 |
|------|------|
| `python -m unittest discover -s docs/tests -p 'test_*.py'` | **65 OK** |
| `python -m unittest discover -s skills/tests -p 'test_*.py'` | **89 OK** |
| `python -m unittest discover -s scripts/tests -p 'test_*.py'` | **128 OK**（skipped=4，环境相关） |
| `python scripts/stage_skills_mirrors.py --check` | `ok: skills mirrors match docs/`（37 对，0 漂移） |
| `git diff --check` | 洁净（0 命中） |
| `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.3` | `evidence consistency ok (12 evidence file(s))` |
| `python scripts/compatibility_report.py --require-ready` | **通过**，`coverage status: ready-for-release-evidence` |
| `python scripts/release_evidence.py --mode rehearsal --run-checks …` | **通过**（`release status: rehearsal`、`checks passed: True`） |

> 对照：S6 开始前 `scripts/tests` 有 4 failures / 12 errors（全部为 `test_release_evidence.py` 的 runtime 证据锚点过期），`--require-ready` 亦为红；本轮重捕获后**全部转绿**。

### 2. 12 格 runtime 证据在 `docs/releases/runtime/v0.13.3/` 重捕获

| consumer | 版本 | govern | audit | vision | vision-audit |
|----------|------|--------|-------|--------|--------------|
| claude-code-cli | `2.1.270` | pass | pass | pass | pass |
| grok-build-cli | `1.0.30` | pass | pass | pass | pass |
| github-copilot-cli | `1.0.75` | pass | pass | pass | pass |

- 每格含 `result.verdict=pass`、marker 观测成立、条目 token、非平凡 stdout；原始 stdout/stderr 落各自 `.d/` 目录。
- v0.13.2 快照**未改写**（保留为历史捕获点）。
- 契约与矩阵同步：`candidateRevision = v0.13.3`、宿主版本实测值、证据路径指向新目录；copilot adapter `verificationStatus` 恢复 `verified`。

### 3. Copilot 阻断与解除（过程留痕）

- 首次重捕获四格 `fail`：`400 unknown provider for model deepseek-v4-flash`（本机 BYOK 端点已停用该模型；CLI 仍请求它，因持久化 `settings.json` 的 `model` 与旧会话缓存可覆盖 `COPILOT_MODEL`）。
- 端点探测：`gemini-3.8-flash-high`、`gpt-5.6-terra` 可用；`deepseek-v4-flash` 返回 400。
- 修法：`copilot-cli-replay.ps1` 显式传 `--model`（优先位置参数，其次 `COPILOT_MODEL`）并打印实际模型；捕获命令传 `--model gemini-3.8-flash-high`。重试后四格 **pass**。
- 失败的 JSON 保留在目录内作为过程记录，但**未被矩阵引用**。

### 4. 版本落地

- `CHANGELOG.md`：新增 `## 0.13.3 - 2026-09-13`（S2～S5 变更 + 验证 + 证据重捕获），`Unreleased` 复位为「空；2026-09-13 发布 v0.13.3」。
- `docs/README.md`：可复制核心包版本 → `0.13.3`；最近发布基线追加 `v0.13.3`；快照日期/身份/工作树边界（含三宿主实测版本与证据目录）更新。

### 5. 隔离消费仓实测（S6 前段，附件）

见 [attachments/s6-isolated-consumer-evidence.md](../attachments/s6-isolated-consumer-evidence.md)：冷启动骨架复制不再泄漏生产仓 VP 行；消费方自有 `AGENTS.md` 规则保留 + 唯一受管区间；升级重放幂等（`Already present (managed block unchanged)`）。

## 本轮未完成（保持 open，不得以残余关门）

| 项 | 说明 | 关联 finding |
|----|------|--------------|
| S6 independent 关门审计 | provider = grok build（grok-4.6 / high），已启动、结论待落盘 | A-001 F-005 之后的关门判据 |
| PR / merge 到 `main` | 发布 tag 必须指向 main merge commit（[D-011](../01-decision/D-011-s6-release-scope-freeze.md) §1） | — |
| annotated tag `v0.13.3` + tag workflow | 需在 merge 后执行；资产与 evidence 以 workflow 实际上传为准 | — |
| Release 资产逐项核对 | 重下载比对 sha256（9 项形态） | — |
| `/commit` 真实宿主调用证据 | 四治理入口已 probe；便利入口属非必达，需单列证据 | A-009 F-001 |

## 检查点

- owned paths = `docs/releases/runtime/v0.13.3/**`、`docs/contracts/{skills-consumer-compatibility-matrix.json,skills-consumer-contract.json}`、`skills/contracts/**`（stage 产物）、`skills/tests/test_skills_orchestrator.py`、`scripts/tests/test_release_evidence.py`、`CHANGELOG.md`、`docs/README.md`、`workspace-001` 的 copilot 重放脚本、`artifacts/compatibility-report.json`，以及本目标五件套。
- 未使用 `git add -A`。
