---
id: E-002
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: execution
title: containment 测试对齐与版本清单同步
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# E-002 · containment 测试对齐与版本清单同步（2026-10-01）

## 1. containment 测试对齐（按 [D-003](../01-decision/D-003-containment-test-realignment.md)）

改 `skills/tests/test_skills_orchestrator.py::TestSkillsOrchestratorPackage.test_init_workspace_refuses_existing_path`：

- 先把 `skills/` 包复制到临时项目内（`shutil.copytree`，忽略 `__pycache__` / `*.pyc`），
  再以 `-SkillsDir .\staged-skills`（**相对路径、项目内**）调用**复制后**的 `install.ps1`。
- 断言原意不变：第一次 `returncode == 0`、`workspace.md` 落盘、第二次非零退出且消息命中
  `already exists|refuse`。
- `skills/install.ps1` 与 `skills/render_managed.py` **未改**。

验证（单测）：`python -m unittest skills.tests.test_skills_orchestrator.TestSkillsOrchestratorPackage.test_init_workspace_refuses_existing_path` → **OK**。

## 2. 版本清单同步（`0.13.4` / `v0.13.4`）

| 文件 | 改动 |
|------|------|
| `CHANGELOG.md` | `## Unreleased` 改为「未发布；`0.13.4` 为发布候选…」；新增 `## 0.13.4 - 2026-10-01` 节 |
| `docs/contracts/skills-consumer-compatibility-matrix.json` | `candidateRevision` → `v0.13.4`；三宿主 12 格 `evidence` 改指 `docs/releases/runtime/v0.13.4/*-2026-10-01.json`；`host.version` 改为实测值（Claude `2.1.285`、Grok `1.0.44`、Copilot `1.0.75`）；三处 `evidenceScope` 改写为 GOAL-009 的变更说明 |
| `skills/contracts/skills-consumer-compatibility-matrix.json` | stage 生成的逐字节镜像（`python scripts/stage_skills_mirrors.py`） |
| `README.md` | 入口 1 示例 pin `v0.13.2` → `v0.13.4`（URL、`-Version`、`--version`、zip 名）；GHCR 镜像示例 `0.13.2` → `0.13.4` |
| `skills/README.md` | 同上（`v0.13.2` → `v0.13.4`） |
| `scripts/bootstrap/README.md` | 同上（`v0.13.2` → `v0.13.4`） |
| `mcp/README.md` | 镜像 tag 示例与 GHCR pin → `0.13.4` |
| `docs/releases/README.md` | pin 规则里的「本轮为 `v0.13.2`」→ `v0.13.4` |
| `docs/README.md` | 可复制核心包版本 `0.13.3` → `0.13.4`；最近发布基线保留 `v0.13.3` 为已发布，新增「`v0.13.4` 为发布候选，尚未打 tag」；快照日期 → 2026-10-01；工作树边界宿主版本与证据目录 → v0.13.4 |
| `scripts/tests/test_release_evidence.py` | `candidateRevision` 断言 `v0.13.3` → `v0.13.4`（2 处） |
| `skills/tests/test_skills_orchestrator.py` | `candidateRevision` 断言与证据路径断言 `v0.13.3` → `v0.13.4` |

发现（既有不一致，如实记录）：进入本轮时 v0.13.3 已正式发布，但根 `README.md`、
`skills/README.md`、`scripts/bootstrap/README.md`、`docs/releases/README.md` 的 pin
与 `mcp/README.md` 的 GHCR 示例**仍停在 `v0.13.2`**。本轮一并前移到 `v0.13.4`。

## 3. 镜像 stage

`python scripts/stage_skills_mirrors.py` → `copied: 1`（契约矩阵镜像）；
`--check` → `ok: skills mirrors match docs/`。本轮**未**改
`docs/architecture/`、`docs/templates/`、`docs/vision/alignment.md` 的 canonical 正文。

## 4. 未改文件（避免破坏证据锚点）

`AGENTS.md`、`skills/prompts/00-govern-orchestrator.md` 以及任何会渲染进
`skills/install/**` 的规则面**未改**：它们是本轮 12 格证据的 `behaviorSources`，
改动会让刚重捕获的证据再次过期。

## 5. 环境说明（影响复现）

- 本机控制台代码页 936（GBK）；Python 需 `PYTHONUTF8=1`，否则子进程 stdout 会被
  按 cp936 解码，破坏宿主 CLI 的 UTF-8 输出。
- Claude Code CLI：用户 settings 的 `ANTHROPIC_BASE_URL` 带 `/v1`，而 CLI 会再拼
  `/v1/messages`，实际请求落到 `/v1/v1/messages` 并 404。探针以 `--settings` 覆盖
  base URL 修正，并显式指定可用模型。
