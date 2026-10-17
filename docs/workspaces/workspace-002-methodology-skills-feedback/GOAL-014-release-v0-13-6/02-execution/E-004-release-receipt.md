---
id: E-004
goal: GOAL-014-release-v0-13-6
doc: execution-entry
title: S3 PR、CI、main merge、tag 与 gated 发布回执
status: recorded
parent: GOAL-014-release-v0-13-6
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-004 · v0.13.6 main、tag 与正式发布回执

## PR 与 CI

- 分支 `codex/release-v0.13.6`（含 GOAL-013 的两个已关门源码检查点 `e37cad3`、`f86b406` 与两个发布检查点）推送到 origin，开 [PR #29](https://github.com/magicvr/goal-governance/pull/29)，base `main`。
- PR CI run [38999047596](https://github.com/magicvr/goal-governance/actions/runs/38999047596)：`contract-and-report` **pass**（1m14s）、`windows-install-surface` **pass**（2m40s）——双平台全绿后才合并。
- PR #29 于 2026-10-17T03:34:09Z 合并，merge commit **`97f6f1ea028006769518d9854aeaff58b8cfa453`**（merge 方式，非 squash/rebase）。
- main CI run [38999290522](https://github.com/magicvr/goal-governance/actions/runs/38999290522) 在该 merge 上 **success**。

## tag 与严格预检

- 本地同步 `origin/main` 到该 merge，工作树干净，创建 annotated tag **`v0.13.6`**（tag object `a1224918ae8b2d11fdbb915b2dd866a6c6cacf4e` → `97f6f1ea`）。
- 推 tag 前在该 merge 上重生成 compatibility report 并执行 `release_evidence.py --mode release --tag v0.13.6 --run-checks`：`release status: release-candidate`，**`checks passed: True`**，exit 0。使用与 E-002 相同的仓内 TEMP 与系统 Python 3.11.9（`.venv` 3.14 沙箱限制见 E-002 复核段；未改产品代码）。
- 推送 tag 成功（`git push origin v0.13.6`，远端 tag object `a1224918`）。

## gated 发布

- tag 工作流 run [39000107099](https://github.com/magicvr/goal-governance/actions/runs/39000107099)：`pack` **success**（版本解析、镜像 stage、M-001 证据一致性门禁、pack 单测、双 ZIP 打包与上传全过）；`Publish GitHub Release (gated)` **success**。
- publish job 先等 Environment `release` 人工门禁：pending deployment 记录 reviewer `magicvr`、`wait_timer` 5 分钟；随后 [API 回执](../attachments/release-receipt.json) 为 **magicvr 人工 `skipped` 放行**（非普通 `approved`）。编排 AI **未**代批、未改 Environment 配置，只在用户确认后回读状态。
- 日志里程碑：`Release evidence passed for v0.13.6`（03:50:05Z）→ GHCR build/push（`0.13.6` 与 `latest` 两个 tag，`containerimage.digest = sha256:0d48e35e…`）→ `Uploaded 9 asset(s) to release v0.13.6`（03:50:18Z）。
- [Release v0.13.6](https://github.com/magicvr/goal-governance/releases/tag/v0.13.6) 于 **2026-10-17T03:50:16Z** 发布，`isDraft = false`、`isPrerelease = false`，9 项资产。

## 事实边界

S3 完成，I-005 verified。远端身份与工作流回执见 [release-receipt.json](../attachments/release-receipt.json)。`releaseStatus: release-candidate` 是证据 schema 的产出值，Release 是否正式由 GitHub `isDraft` / `isPrerelease` / `publishedAt` 判断。资产逐项验收见 [E-005](E-005-published-asset-verification.md)；本地构建的预演 ZIP 未用于冒充正式资产。
