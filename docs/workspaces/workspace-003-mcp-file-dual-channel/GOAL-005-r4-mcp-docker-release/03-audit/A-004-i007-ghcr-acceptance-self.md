---
id: A-004
doc: audit-entry
source: self
status: recorded
parent: GOAL-005-r4-mcp-docker-release
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
scope: I-007 首次真实 GHCR 发布验收（v0.13.1）
verdict: pass
---

# A-004 · I-007 关闭 · v0.13.1 GHCR 验收（self · 编排器）

## 条目头

| 字段 | 值 |
|------|-----|
| source | `self` |
| 日期 | 2026-08-08 |
| scope | GOAL-005 I-007（non-blocking）关闭；关联 Root A-012 F-008 |
| verdict | **pass** |
| 开放 required | **0** |

## 结论

**pass**。v0.13.1 正式 annotated tag + GitHub Release（9 资产）+ `skills-pack-release` publish 全绿（含 GHCR push）已可核对；本机成功 pull `0.13.1` 与 `latest`，**同 digest** `sha256:e17ff08c6434ab99c8d3f5fd390f1542f28e73f6e3acb03d18f927a807e97205`，镜像内 `GOAL_GOVERNANCE_MCP_VERSION=0.13.1`。

### I-007 闭合

| 项 | 原状态 | 新状态 | 路径 |
|----|--------|--------|------|
| I-007（GHCR packages:write / 命名空间可达） | open（non-blocking） | **closed / verified** | fixed（证据链） |

### 关联 finding（Root 台账）

| 项 | 处置 |
|----|------|
| A-012 **F-008** | 由 Root **A-021** 登记 **fixed**（与本条同源证据） |
| A-001 R-002 / A-002 F-001（历史 recommended） | 由 I-007 关闭满足其「首次真实 tag 后回填」触发 |

**不**改变 GOAL-005 / Root / VP-004 / workspace 的 `done`/`closed` 状态。

## 证据

- [i-007-v0.13.1-ghcr-acceptance-2026-08-08.md](../attachments/i-007-v0.13.1-ghcr-acceptance-2026-08-08.md)
- E-003：`02-execution/E-003-i007-v0131-ghcr-acceptance.md`
