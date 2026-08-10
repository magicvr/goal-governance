---
id: D-003
goal: GOAL-007-workspaces-directory-consolidation
status: accepted
created: 2026-08-10
updated: 2026-08-10
version: 0.1.0
---

# D-003 · v0.13.2 发布基线与门禁

## 已核对基线

- 最新 annotated tag 为 `v0.13.1`，指向已合并 `main` 的 commit `a10a98f`。
- 当前工作分支为 `dev`；任务开始时 HEAD `95ade46`，`origin/dev` 为 `77dcc33`。
- 兼容矩阵 `candidateRevision`、根/Skills/bootstrap README pins 与 CHANGELOG 最新节均为 `v0.13.1`。
- Release workflow 要求 annotated tag、tag peeled commit 等于检出 HEAD、Environment `release` 审批，以及 compatibility/release evidence hard gate。

## 决定

1. 本目标发布版本为下一补丁版 `0.13.2` / tag `v0.13.2`；若进入 S5 前远端已有同名 tag 或更高正式基线，则回到本决策重算。
2. S3 必须同步 `CHANGELOG.md`、兼容矩阵 `candidateRevision` 与 evidenceScope、根/Skills/bootstrap/MCP 示例 pin 及锁定版本的测试。
3. S5 只在 PR CI 全绿并合入 `main` 后创建 annotated tag；tag 必须指向 merged main，不以分支 checkpoint 代替。
4. 发布完成须核验 workflow、Release/GHCR、所有预期资产、sha256 与 release evidence；仅 tag 存在不算完成。
