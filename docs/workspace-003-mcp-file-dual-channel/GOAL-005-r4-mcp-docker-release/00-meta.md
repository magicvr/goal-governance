---
id: GOAL-005-r4-mcp-docker-release
title: R4：MCP Docker 资产发布与通道资产分离
status: done
parent: GOAL-001-mcp-file-dual-channel-delivery
plan_refs: VP-004-mcp-file-dual-channel-delivery
primary_plan: VP-004-mcp-file-dual-channel-delivery
serves_summary: 服务 VP-004 R4（reopen 增补）：File 资产排除 MCP 实现源码、MCP server 以 Docker 镜像随同 tag 发布、仓库与 README 安装指南
created: 2026-08-07
updated: 2026-08-07
version: 0.3.0
progress: 100%
---

# GOAL-005 · R4：MCP Docker 资产发布与通道资产分离

## 概述

R1–R3 关门后，2026-08-07 发布面核查（用户指令）发现三项发布资产缺口，Root 据此回退关门状态并新开本目标：

1. **通道资产未分离**：File 资产 `goal-governance-skills-v*.zip` 把 `skills/mcp/` 实现源码（10 个文件）一并打包（`scripts/pack_skills_release.py` 无 mcp 排除规则，90 成员含 10 个 MCP 成员）。
2. **MCP 无可分发发布资产**：仓库无 `Dockerfile` / `.dockerignore`；`skills-pack-release.yml`（tag 触发）无任何 docker build / GHCR push 步骤；根 README 无 MCP 安装指南。
3. **文案与事实不符**：`skills/mcp/README.md` 称「`Dockerfile` 仅作便捷（可选）」——仓库不存在 Dockerfile。

修复方向（用户书面要求）：File 资产**不得**打包 MCP 代码；MCP server 以 **Docker 镜像**发布到本仓 GitHub 仓库的容器资源（GHCR），与 File 资产**同 tag 同时发布同版本**；仓库与 README 提供安装 MCP server 的命令与指南。

## 成功标准

- [x] 缺口已登记：三项缺口见上（本目标即登记事实）。
- [x] R4a：方案冻结已落盘（D-001）：生产布局 = 根目录 `mcp/`（与 skills 并列）；消费形态 = GHCR Docker 镜像固定入口（`--repo-root /workspace` 挂载卷）；`-Channel mcp` 薄装重定义（不再 materialize 代码）；workflow 同 tag 同版本发布；I-005/I-006 closed。
- [x] R4b：实施完成——`git mv skills/mcp → mcp/` + 全部引用更新；`mcp/Dockerfile` + `.dockerignore` 落盘并可本地构建；File zip 不含 mcp 且测试断言（防御复发）；`skills-pack-release.yml` 在 tag 流程内构建并推送 GHCR（同 tag 同版本 + latest、environment 门禁后、`packages: write`）；`-Channel mcp` 薄装重定义（bootstrap sh/ps1 + 测试）；根 README 与 `mcp/README.md` 含安装 MCP server 的命令与指南；`mcp/README.md`「Dockerfile 可选」空头文案修正。
- [x] R4c：验证与关门——pack/CI 测试全绿（197 passed）、docker 构建验证有证据、cross 审计（A-001 self + A-002 independent grok build）通过后关门（2026-08-07 A-003 合并响应闭合）。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **R4a** | 方案冻结 | **完成** | D-001：生产布局 = 根目录 `mcp/`；消费形态 = GHCR 镜像固定入口；薄装重定义；workflow 同 tag 发布；I-005/I-006 关闭 |
| **R4b** | 实施 | **完成** | `git mv skills/mcp → mcp/`；Dockerfile/.dockerignore；pack 结构性排除 + 防御断言；workflow docker build + GHCR push；bootstrap 薄装重定义；README 安装指南与文案修正；全量测试 197 passed |
| **R4c** | 验证与关门 | **完成** | 2026-08-07：全量测试回归（197 passed）、docker 构建证据、cross 审计（A-001 self + A-002 independent grok build）均 pass → A-003 合并响应 → C3 闭合 |

阶段间串行（R4a 冻结后才实施）。检查点 C1/C2/C3 = R4a/R4b/R4c 完成。

## 派生进度展示

`progress: 100%` = 纲领阶段 R4a～R4c 已完成 **3 / 3**（等权；R4a/R4b 于 2026-08-07 完成，R4c 于 2026-08-07 经 A-003 合并响应闭合）。progress 仅展示，不放行阶段、不关闭 finding、不推导 `done`；关门依据 = 03-audit 台账 + 成功标准证据。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-005 | required | GHCR 镜像命名与 tag 策略：镜像名（如 `ghcr.io/magicvr/goal-governance-mcp-server`）、tag 与 File 资产同版本的具体形态（去 `v` 前缀？） | R4a 方案冻结 | R4a | 用户确认 + 对照 GitHub Release tag 惯例（`v*`）与 Docker tag 惯例 | **closed** | — | 用户 2026-08-07 确认：`ghcr.io/magicvr/goal-governance-mcp-server`，tag = 去 v SemVer（如 `0.13.0`）+ `latest`，与 Release tag `v0.13.0` 同源同发布（D-001） |
| I-006 | required | MCP server 容器运行形态：stdio 容器入口、`--repo-root` 挂载卷 vs 内置默认；MCP client 连接方式（`docker run -i`） | R4a 方案冻结 | R4a | 对照 `mcp/server.py` CLI 与 MCP stdio 传输 | **closed** | — | 用户 2026-08-07 确认固定入口：`ENTRYPOINT python server.py` + `CMD --repo-root /workspace`；挂载卷映射仓库根（D-001） |
| I-007 | non-blocking | 仓库/环境对 GHCR `packages: write` 的可用性与镜像命名空间可达性 | R4c 发布验收 | R4c | workflow 实测（或本地 `docker login ghcr.io` 检查） | open | 首次真实 tag 发布验收时关闭（A-001 R-002 / A-002 F-001；A-003 响应） | 不阻断 R4c 关门；发布后回填 digest/URL 证据至 attachments |

## 审计模式

发布/生产面高影响门禁 → **cross**（self + 至少一个指定 provider 的 independent）。independent provider 沿用 D-004 用户指定：**Grok Build（grok-4.5 / thinking-high）**；provider 不可用时不静默降级（P-003/P-004）。已执行：A-001（self，pass）+ A-002（independent，pass）+ A-003（self 合并响应，pass）。

## 父目标

- [GOAL-001-mcp-file-dual-channel-delivery](../GOAL-001-mcp-file-dual-channel-delivery/00-meta.md)（Root，本目标为其 R4 纲领阶段子目标）

## 台账布局

三个 ledger 目录 `01-decision/`、`02-execution/`、`03-audit/` 与 `attachments/` 已建；索引文件见各 `01/02/03-decision/execution/audit.md`。

## 备注

- 立项背景：2026-08-07 用户指令核查发布资产面 → 三缺口确认 → 用户书面确认「全套方案」：新开本目标 + 回退 Root / VP-004 / workspace.md 关门状态（留痕见 Root 03-audit 与 goal-tree）。
- 与 VP-004 的关系：本目标为 VP-004 reopen 后的 R4 增补交付；VP-004 退出判据 #8（发布资产面）随本目标验收（**F-003**：复关时把 #8 路径字面 `skills/mcp/` → `mcp/`，不改语义）。
- 关门：2026-08-07 用户 `/govern`「合并响应」→ A-003 落盘（响应 A-001/A-002 全部 recommended；F-002 fixed、R-003/F-004/F-005 accepted、R-001/R-002/F-001/F-003 deferred）→ C3 闭合 → `done`（100%）。I-007 首次真实 GHCR 发布验收时关闭。
