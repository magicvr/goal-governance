---
id: A-004
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: audit
title: 发布产出核对（S4）
source: self
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# A-004 · 发布产出核对（self · 2026-10-01）

| 项 | 值 |
|----|-----|
| source | `self` |
| scope | S4：PR / 合并 `main` / annotated tag `v0.13.4` / tag workflow / Release 资产 |
| verdict | **pass** |

## 成果（逐项可核对，详见 [E-004](../02-execution/E-004-release-receipt.md)）

| 主张 | 证据 |
|------|------|
| PR 开了、CI 双 job 绿后才合并 | PR #23；run `36807895977` 的 `contract-and-report` 与 `windows-install-surface` 均 pass |
| merge commit 存在且 `main` CI 绿 | merge `43479838…`（`2026-10-01T02:56:24Z`）；run `36808178721` success |
| tag 是 annotated 且指向 merge commit | `git cat-file -t v0.13.4` = `tag`；tag 对象 `acb0a389…` → `43479838…` = `origin/main`；`ls-remote` 可见 `^{}` 剥离项 |
| 发布前已预检 strict 门禁 | 在 main worktree 的临时 tag 上跑 `release_evidence --mode release` → `release-candidate`、`checks passed: True`（临时 tag 与 worktree 已清理） |
| tag workflow 两个 job 全绿，含硬门禁与 GHCR 推送 | run `36808519534`：`pack` success（含 M-001 evidence gate）、`Publish GitHub Release (gated)` success（含 Hard release-evidence gate、Build and push MCP image、Create Release、Upload assets） |
| Environment `release` 人工审批由用户完成，编排器未代签 | 审批记录在 run `36808519534` 的 deployment；编排器在等待态时向用户提问，用户回复已自行点击 |
| Release 存在、非 draft / 非 prerelease、9 项资产齐全 | `releases/tag/v0.13.4`，published `2026-10-01T03:09:11Z`；资产缺失 0 / 多余 0 |
| 两个 zip 的摘要与 sidecar 逐项一致 | 重下载后重算：skills `2cc277dc…`、core `2f5ad1cf…`，均与 sidecar 相同 |

## findings

| ID | 级别 | 主张 | 证据 | 影响 |
|----|------|------|------|------|
| F-001 | recommended | GHCR 镜像 `ghcr.io/magicvr/goal-governance-mcp-server:0.13.4` / `:latest` 只有 workflow 步骤成功这一证据，**未**做产物级独立核对 | 本会话 token 无 `read:packages`；`gh api user/packages/.../versions` → 403 `You need at least read:packages scope` | 不阻断 zip 资产发布。复审触发 = 需要声称镜像可用时，或下次发布前 |
| F-002 | recommended | 本轮未做隔离消费仓的安装 / 升级重放 | [E-004](../02-execution/E-004-release-receipt.md) §未做 | 不阻断；v0.13.3 已有同类证据（GOAL-008） |

## 我已核对但发现需要更正的项

- 审计发现（A-002 F-005）本轮早前把宿主数写成「4 宿主」，已在同一提交内改为「3 宿主 × 4 治理入口 = 12 格」。
- 审计发现（A-002 F-004）本轮早前把 `v0.13.4` 直接写成「当前正式发布」，已在 pin 段加「发布候选」状态说明、并把 CHANGELOG 的措辞改为「为正式发布做准备」。

## 放行 / 关门判定

- 相关意见：A-001（self，conditional，0 required）、A-002（independent，pass，0 required）、A-003（响应）、A-004（本条）。
- 冲突：**无**。开放 required：**0**（三条 recommended：A-001 F-001、A-002 F-001、A-004 F-001 / F-002，均不阻断且已有残余范围与复审触发）。
- 成功标准：`00-meta.md` 六项**全部满足**。
- 信息门禁：I-001～I-005 全部 `verified`。
- 结论：**GOAL-010 可标 `done` / 100%（S1～S4 4/4）**。Root R3 与 VP-002 为长期持续治理，不随之关门——沿用 D-008。
