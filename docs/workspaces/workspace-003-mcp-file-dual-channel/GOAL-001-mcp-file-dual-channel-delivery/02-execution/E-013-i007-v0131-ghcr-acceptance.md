---
id: GOAL-001-mcp-file-dual-channel-delivery
doc: execution-entry
record_id: E-013
status: recorded
parent: null
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
---

# E-013 · I-007 / F-008 关闭：v0.13.1 正式 Release + GHCR 验收

## 2026-08-08 · 首次真实 GHCR 发布验收（不重开 Root）

### 已发生事实

1. 正式 **`v0.13.1`** annotated tag（`a10a98fe…`）与 GitHub Release（9 资产）及 `skills-pack-release` run `31212196389` success 已存在（2026-08-07）；publish 含 GHCR login + build/push + Release upload。
2. 本会话本机验收 pull 成功：  
   `ghcr.io/magicvr/goal-governance-mcp-server:0.13.1` 与 `:latest`  
   digest **`sha256:e17ff08c6434ab99c8d3f5fd390f1542f28e73f6e3acb03d18f927a807e97205`**；ENV `GOAL_GOVERNANCE_MCP_VERSION=0.13.1`。
3. 子目标 GOAL-005 登记 E-003 + A-004；Root 登记 A-021 关闭 **F-008** / 同步 I-007 关闭。
4. Root / 子目标 / VP-004 / workspace **status 无变化**（均 done/closed）。

### 证据

| 主张 | 路径 / 引用 |
|------|-------------|
| 验收证据包 | [GOAL-005 attachments/i-007-…](../../GOAL-005-r4-mcp-docker-release/attachments/i-007-v0.13.1-ghcr-acceptance-2026-08-08.md) |
| GOAL-005 执行 | `GOAL-005-…/02-execution/E-003-i007-v0131-ghcr-acceptance.md` |
| GOAL-005 审计 | `GOAL-005-…/03-audit/A-004-i007-ghcr-acceptance-self.md` |
| Root 审计响应 | `03-audit/A-021-close-i007-f008-ghcr-acceptance-self.md` |
