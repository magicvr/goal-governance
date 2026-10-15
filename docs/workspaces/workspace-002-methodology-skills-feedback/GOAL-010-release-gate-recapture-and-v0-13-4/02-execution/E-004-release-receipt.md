---
id: E-004
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: execution
title: v0.13.4 正式发布产出与资产核对
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# E-004 · v0.13.4 正式发布产出与资产核对（2026-10-01）

## 产出链

| 环节 | 事实 |
|------|------|
| PR | **#23**「GOAL-010: recapture L3 release evidence and prepare v0.13.4」，`dev` → `main`，https://github.com/magicvr/goal-governance/pull/23 |
| PR CI | run `36807895977`（event `pull_request`，head `dev`）：`contract-and-report` **pass**（57s）、`windows-install-surface` **pass**（2m37s） |
| merge | PR #23 **MERGED**（merge commit），merge commit = **`43479838d65d97f4a8b70d37d8c8226cb96c81ef`**，merged at `2026-10-01T02:56:24Z` |
| main CI | run `36808178721`（event `push`，branch `main`）**success**（3m12s） |
| annotated tag | **`v0.13.4`**，对象类型 `tag`，tag 对象 `acb0a38925f48a258f27fb6965c838cb718fa74a` → commit `43479838…`（= `origin/main`）。`git ls-remote` 同时可见 `refs/tags/v0.13.4` 与 `refs/tags/v0.13.4^{}` |
| tag workflow | run **`36808519534`**（event `push`，ref `v0.13.4`）——见下 |

## 发布前对 strict 门禁的预检（本地）

在 `main` 的临时 worktree（`.gg-maincheck`，detached at `43479838`）上打**临时** annotated tag 后运行：

```text
python scripts/release_evidence.py --mode release --tag v0.13.4 --run-checks \
  --compatibility-report artifacts/compatibility-report.json --output artifacts/gg-releasecheck.json
→ wrote release evidence; release status: release-candidate; checks passed: True   (exit 0)
```

预检后已删除临时 tag 与 worktree；预检产出写在 `artifacts/`（gitignore）内，未入库。

## tag workflow 结果

| job | 结论 | 关键步骤 |
|-----|------|----------|
| `pack` | **success**（11s） | Stage skills mirrors / Evidence consistency gate (M-001) / pack unit tests / Pack skills + core zips / Upload pack artifacts 全部 success |
| `Publish GitHub Release (gated)` | **success** | Ensure annotated tag is visible / **Hard release-evidence gate (fail closed)** / Download pack artifact / Log in to GHCR / **Build and push MCP server Docker image (GHCR)** / Create GitHub Release if missing / Upload release assets 全部 success |

Environment **`release`** 的人工审批由用户于 2026-10-01 完成（wait timer 5 分钟已过）。编排器未代为审批。

## Release 资产（9 项，全部 `uploaded`）

Release：https://github.com/magicvr/goal-governance/releases/tag/v0.13.4 ，`draft: false`、`prerelease: false`、published at `2026-10-01T03:09:11Z`。

| # | 资产 | 大小 (B) |
|---|------|----------|
| 1 | `goal-governance-skills-v0.13.4.zip` | 259 793 |
| 2 | `goal-governance-skills-v0.13.4.zip.sha256` | 101 |
| 3 | `goal-governance-core-v0.13.4.zip` | 62 792 |
| 4 | `goal-governance-core-v0.13.4.zip.sha256` | 99 |
| 5 | `install-online.ps1` | 12 737 |
| 6 | `install-online.sh` | 10 400 |
| 7 | `bootstrap-README.md` | 6 008 |
| 8 | `release-evidence.json` | 118 459 |
| 9 | `compatibility-report.json` | 10 684 |

必需资产集合核对：**缺失 0 项、多余 0 项**。

## 摘要复核（重下载）

重下载两个 zip 并各自重算 SHA-256，与 sidecar 逐项比对：

| zip | sidecar 记录 = 实测 | 结果 |
|-----|---------------------|------|
| `goal-governance-skills-v0.13.4.zip` | `2cc277dcddd63f650788081e4feea1c46e58affc20582239894401d6b68fb869` | **一致** |
| `goal-governance-core-v0.13.4.zip` | `2f5ad1cf47c1eaf57c28944dd276282843cffb699764421477bbae8acb94412d` | **一致** |

sidecar 内的文件名与 zip 名一致。

## 容器镜像

publish job 的「Build and push MCP server Docker image (GHCR)」步骤 success，按工作流定义以 `GOAL_GOVERNANCE_MCP_VERSION=0.13.4` 推送
`ghcr.io/magicvr/goal-governance-mcp-server:0.13.4` 与 `:latest`。

**未独立核对**：本次会话的 token 无 `read:packages` scope，`gh api user/packages/.../versions` 返回
403（`You need at least read:packages scope`），因此镜像 tag 与摘要**只有 workflow 步骤成功这一证据**，
没有像 zip 那样的重下载比对。此项登记为待复核，不写成已核对。

## 未做

- 未做隔离消费仓的安装 / 升级重放（沿用 v0.13.3 的既有证据，本轮不重放）。
