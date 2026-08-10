---
id: GOAL-005-r4-mcp-docker-release
doc: execution-entry
record_id: E-003
status: recorded
parent: GOAL-001-mcp-file-dual-channel-delivery
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
---

# E-003 · I-007 关闭：v0.13.1 正式 tag/Release + GHCR 验收

## 2026-08-08 · 首次真实 GHCR 发布验收

### 已发生事实

1. **正式发布已完成**（2026-08-07，非本会话新建 tag）：annotated `v0.13.1` → commit `a10a98fe8c880191385266301f823e545b500ad3`；GitHub Release 含 9 项资产；`skills-pack-release` run `31212196389` **success**（含 Environment `release`、硬 release-evidence、GHCR login/build/push、Release create/upload）。
2. **本会话验收**（用户指令）：本机 `docker pull`  
   - `ghcr.io/magicvr/goal-governance-mcp-server:0.13.1`  
   - `ghcr.io/magicvr/goal-governance-mcp-server:latest`  
   二者 **Repo digest 相同**：`sha256:e17ff08c6434ab99c8d3f5fd390f1542f28e73f6e3acb03d18f927a807e97205`；镜像 ENV `GOAL_GOVERNANCE_MCP_VERSION=0.13.1`。
3. 自 Release 下载并核对 skills/core `.sha256` 文件与 asset 列表一致。
4. **I-007 → closed**（见 A-004）；目标 status 保持 **`done`**（不重开）。

### 证据

| 主张 | 路径 / 命令 / 引用 |
|------|-------------------|
| 完整验收证据包 | [attachments/i-007-v0.13.1-ghcr-acceptance-2026-08-08.md](../attachments/i-007-v0.13.1-ghcr-acceptance-2026-08-08.md) |
| Workflow | https://github.com/magicvr/goal-governance/actions/runs/31212196389 |
| Release | https://github.com/magicvr/goal-governance/releases/tag/v0.13.1 |
| GHCR digest | `ghcr.io/magicvr/goal-governance-mcp-server@sha256:e17ff08c6434ab99c8d3f5fd390f1542f28e73f6e3acb03d18f927a807e97205` |
