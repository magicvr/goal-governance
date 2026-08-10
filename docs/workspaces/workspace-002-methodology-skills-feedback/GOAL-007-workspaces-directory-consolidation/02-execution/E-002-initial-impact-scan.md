---
id: E-002
goal: GOAL-007-workspaces-directory-consolidation
status: recorded
created: 2026-08-10
updated: 2026-08-10
version: 0.1.0
---

# E-002 · 初始影响面扫描

## 已核对事实

- 本仓当时存在三个旧直属显式工作区：`docs/workspace-001-goal-governance/`、`docs/workspace-002-methodology-skills-feedback/`、`docs/workspace-003-mcp-file-dual-channel/`。
- 核心协议、alignment、directory layout、README、workspace 模板将内部布局冻结为治理根直属 `workspace-*`。
- Skills prompts/AGENTS、MCP entry/config/schema、安装器、release packaging 与多组测试包含旧路径发现或断言。
- 修改 architecture/templates/alignment 属于 canonical → Skills stage 白名单，必须刷新镜像并通过 `scripts/stage_skills_mirrors.py --check`。
- 任务开始时 Git 分支为 `dev`，相对 `origin/dev` ahead 1；本轮尚未创建发布分支、PR、tag 或 Release。

## 尚未发生

兼容策略、版本号与 provider 尚未冻结；S2～S5 均未开始。
