---
id: A-021
doc: audit-entry
source: self
status: recorded
parent: GOAL-001-mcp-file-dual-channel-delivery
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
scope: 关闭 A-012 F-008 与 GOAL-005 I-007（v0.13.1 GHCR 验收）
verdict: pass
---

# A-021 · 关闭 F-008 / I-007 · v0.13.1 GHCR 验收（self · 编排器）

## 条目头

| 字段 | 值 |
|------|-----|
| source | `self` |
| 日期 | 2026-08-08 |
| scope | Root A-012 F-008 + GOAL-005 I-007（首次真实 `v*` GHCR 发布验收） |
| verdict | **pass** |
| 开放 required | **0** |

## 结论

**pass**。用户指令执行 v0.13.1 正式 tag/Release + GHCR 验收以关 I-007：

1. **Release 面**：annotated `v0.13.1` @ `a10a98fe…`；Release 9 资产齐全；workflow [31212196389](https://github.com/magicvr/goal-governance/actions/runs/31212196389) publish **success**（Environment `release` + hard evidence + **GHCR push** + asset upload）。
2. **GHCR 面（本机实测）**：pull `ghcr.io/magicvr/goal-governance-mcp-server:0.13.1` 与 `:latest` 成功；**同一 Repo digest** `sha256:e17ff08c6434ab99c8d3f5fd390f1542f28e73f6e3acb03d18f927a807e97205`；镜像 ENV `GOAL_GOVERNANCE_MCP_VERSION=0.13.1`。

### Finding / 信息项闭合

| ID | 来源 | 原状态 | 闭合路径 | 新状态 |
|----|------|--------|----------|--------|
| **F-008** | A-012 independent · recommended · info | open（登记于 A-013） | **fixed**（真实 GHCR 可 pull + digest 回填） | **closed** |
| **I-007** | GOAL-005 · non-blocking | open | **verified/closed**（GOAL-005 A-004 + 本条） | **closed** |

无 required、无冲突；**不**回退 Root / 子目标 / VP-004 / workspace 关门状态。

## 证据

- [GOAL-005 attachments/i-007-v0.13.1-ghcr-acceptance-2026-08-08.md](../../GOAL-005-r4-mcp-docker-release/attachments/i-007-v0.13.1-ghcr-acceptance-2026-08-08.md)
- GOAL-005 A-004：`../GOAL-005-r4-mcp-docker-release/03-audit/A-004-i007-ghcr-acceptance-self.md`
- E-013：`../02-execution/E-013-i007-v0131-ghcr-acceptance.md`
