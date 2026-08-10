---
id: D-001
goal_id: GOAL-005-r4-mcp-docker-release
title: R4a 方案冻结 · 通道资产分离布局 + Docker 发布形态（I-005/I-006 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-001 · R4a 方案冻结（2026-08-07）

## 决定

1. **生产布局（决策点①）**：MCP 通道实现从 `skills/mcp/` 搬迁至仓库根 **`mcp/`**（与 `skills/` 并列）。`skills/` = File 通道资产 + 方法论；`mcp/` = MCP 通道实现（独立分发单元，含 Dockerfile）。File zip 由 pack（只打 `skills/`）**结构性**排除 mcp，无需排除规则；pack 测试加防御断言防复发。
2. **消费形态（决策点③）**：MCP 主消费路径 = GHCR Docker 镜像，**固定入口**——`ENTRYPOINT ["python", "server.py"]` + `CMD ["--repo-root", "/workspace"]`；MCP client 以 `docker run -i --rm -v <仓库根>:/workspace ghcr.io/…` 连接，客户端零参数。本地 stdio 进程形态仍合法（源码/镜像内执行均可），**不**强制 Docker-only（VP-004 非目标保持）。
3. **`-Channel mcp` 薄装重定义（决策点②）**：不再从发布资产 materialize mcp 代码；改为：安装 consumer contract（`skills/contracts/`）+ 跑 lifecycle CLI（写 `AGENTS.md` managed 段 + `.goal-governance/install.json`，`channel=mcp`）+ 输出 MCP client 配置指引（docker run 命令）。lifecycle allowlist 语义不变（仅 `AGENTS.md` + `.goal-governance/`；mcp 代码本就不在 allowlist）。
4. **发布（同 tag 同版本）**：`skills-pack-release.yml` 的 publish job（`environment: release` 门禁 + release evidence gate 通过后）构建 `mcp/` 镜像并推送 GHCR：**`ghcr.io/magicvr/goal-governance-mcp-server:<去 v 版本>`**（如 `0.13.0`，对应 GitHub Release tag `v0.13.0`）+ `latest` 便利 tag；与 File 资产同一 workflow、同一 tag 触发、同时发布。publish 增加 `packages: write` 权限。
5. **文档**：根 README 增加「MCP 通道安装（Docker）」节（pull/run 命令、MCP client 配置示例、同 tag 发布说明）；`mcp/README.md` 修正「`Dockerfile` 仅作便捷（可选）」空头文案（仓库原本无 Dockerfile）并补 Docker 用法。
6. **I-005 / I-006 关闭**（用户 2026-08-07 书面确认：镜像名 `ghcr.io/magicvr/goal-governance-mcp-server`、tag = 去 v 版本 + latest、固定入口形态）。

## 未选方案

- 保持 `skills/mcp/` + pack 排除规则：防混入依赖单条排除规则（脆弱，问题 1 复发风险），通道边界语义模糊。
- 多级 GHCR 命名空间 `ghcr.io/magicvr/goal-governance/mcp-server`：可读但更长；单段镜像名足够且与 release 资产命名习惯一致。
- 薄装继续 materialize mcp 代码到消费仓：与「File 资产不含 MCP 代码」+「Docker 主路径」冲突。
- stdio 直连 + 客户端传 `--repo-root` 参数：固定入口更简单，MCP client 配置零参数。

## 依据

- 用户 2026-08-07 讨论确认：布局方案「根目录并列 mcp/」+ I-005/I-006 选项。
- 发布面核查缺口（File zip 混入 `skills/mcp/` 源码；MCP 无 Docker 发布资产；README 无安装指南 + 空头文案）。
- VP-004 退出判据 #8（2026-08-07 reopen 增补）。
