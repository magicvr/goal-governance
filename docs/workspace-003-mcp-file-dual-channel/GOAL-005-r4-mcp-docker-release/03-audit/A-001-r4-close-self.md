---
id: A-001
goal: GOAL-005-r4-mcp-docker-release
title: R4 关门自审计（self · 编排器；R4c 前半）
status: recorded
source: self
auditor: grok build / grok-4.5（编排器自审）
date: 2026-08-07
scope: R4 关门（R4a 冻结 + R4b 实施 + R4c 自审部分）；对照成功标准、VP-004 退出判据 #8 与信息门禁
verdict: pass
version: 0.1.0
---

# A-001 · R4 关门自审计（2026-08-07）

## 结论

`pass`（self 范围）。R4a 方案冻结（D-001）与 R4b 实施全部完成且证据可复核：`git mv skills/mcp → mcp/` 后 File zip **结构性**不含 MCP 实现（80 成员 / 0 MCP 成员，此前 90 / 10）；Dockerfile 本地构建通过；`skills-pack-release.yml` 同 tag 发布 GHCR 镜像（版本 tag + latest）；薄装 `-Channel mcp` 重定义为镜像内 lifecycle 写入（e2e 真实验证）；README 安装指南齐备且空头文案已修正。I-005/I-006 closed；I-007（GHCR 权限可达性）open（non-blocking，发布验收前关闭）。

**cross 审计的 independent 部分待 `/audit`（provider = grok build / grok-4.5 / thinking-high，D-004 指定）**；本 self 审计不替代独立审，不单独放行关门。

## 范围与区间

| 项 | 内容 |
|----|------|
| 目标 | GOAL-005-r4-mcp-docker-release（R4） |
| 方案 | D-001（布局 / 镜像形态 / 薄装重定义 / 发布 / 文档） |
| 实施 | E-001（搬迁、Dockerfile、workflow、bootstrap、README、引用面） |
| 发布面 | `skills-pack-release.yml`、`mcp/Dockerfile`、`scripts/bootstrap/install-online.{sh,ps1}`、根 README、`mcp/README.md` |
| 排除 | 其他工作区；R1–R3 已 done 目标结论（不重审）；历史记录路径（CHANGELOG / GOAL-004 台账）不改写 |

## 独立核验（亲自执行）

| 动作 | 结果 |
|------|------|
| `inventoriable_files(skills)` | **80 成员 / 0 MCP 成员**（搬迁前 90 / 10）——结构性通道资产分离成立 |
| 全量回归 `pytest docs/tests scripts/tests skills/tests` | **197 passed, 4 skipped, 4 subtests**（与 A-009 基线一致） |
| `stage_skills_mirrors.py --check` | **ok**（36 对 0 漂移；workspace-protocol 引用 `skills/mcp/config.py` → `mcp/config.py` 已镜像） |
| 本地 `docker build mcp/` | **通过**（bootstrap e2e 测试内构建；固定入口 `python server.py --repo-root /workspace`） |
| 薄装 e2e（ps1 + bash × `docker run` 镜像内 lifecycle） | AGENTS.md managed 段 + `.goal-governance/install.json`（`channel=mcp`）真实写入；**消费仓无 mcp 代码**；输出 GHCR 镜像配置指引 |
| `git log` 检查点 | `f71b8b2`（38 文件 +456/−96：搬迁 + Dockerfile + workflow + 薄装 + 文档 + 台账） |
| 引用面扫描 `skills/mcp` | 剩余引用均为历史记录（CHANGELOG、GOAL-004 台账、缺口描述）——行为面 0 遗漏 |

## 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 缺口已登记 | ✅ | 00-meta 概述（三项缺口） |
| R4a 方案冻结（D-001；I-005/I-006 closed） | ✅ | D-001 + 用户 2026-08-07 书面确认 |
| R4b 实施（搬迁/Dockerfile/workflow/薄装/README/文案） | ✅ | E-001 + 本审计核验表 |
| R4c 验证与关门（测试绿 + docker 证据 + cross 审计） | 🔶 部分 | 测试绿 ✓、docker 构建证据 ✓；**independent 审计待 `/audit`** |

## 信息门禁核对

| I-ID | 级别 | 状态 | 备注 |
|------|------|------|------|
| I-005（GHCR 命名/tag 策略） | required | **closed** | 用户确认 `ghcr.io/magicvr/goal-governance-mcp-server` + 去 v tag + latest（D-001） |
| I-006（容器运行形态） | required | **closed** | 用户确认固定入口（D-001） |
| I-007（GHCR `packages: write` 可达性） | non-blocking | **open** | 验证动作：首次 tag 发布实测（或 `docker login ghcr.io` 检查）；**R4c 发布验收前关闭**，不阻断本自审 |

## VP-004 退出判据 #8 核对

| 判据 | 状态 | 证据 |
|------|------|------|
| File 发布资产不含 MCP 实现（通道资产分离） | ✅ | `inventoriable_files` 80/0；pack 防御断言（`test_pack_skills_release.py`） |
| MCP server 以 Docker 镜像发布（GHCR） | ✅（发布步骤就位） | `skills-pack-release.yml`：login-action + build-push-action（context `mcp/`，版本 tag + latest），evidence gate 后、`environment: release` |
| 与 File 资产同 tag 同版本同时发布 | ✅（结构） | 同一 workflow run（tag `v*` 触发）内 File zip 与镜像同 `needs.pack.outputs.version` |
| README 安装指南（根 + mcp/）+ 无空头文案 | ✅ | 根 README「MCP Server 安装（Docker 通道）」节；`mcp/README.md`（「Dockerfile 可选」→ Docker 主形态） |
| 镜像真实发布（GHCR push 成功） | 🔶 **待首次 tag 发布实测** | 属发布验收（I-007）；workflow 结构已就位，未真实执行过 |

## Findings

### required findings

**无。**

### recommended（非阻断）

| ID | 严重度 | 说明 | 建议 |
|----|--------|------|------|
| **R-001** | low | `skills-pack-release.yml` 的 GHCR 构建/推送步骤未真实执行过（尚无 tag 发布触发）；`docker/build-push-action` 依赖 buildx（ubuntu-latest 自带，未实测）。 | 首次 tag 发布（或 `workflow_dispatch` 试跑）时验证；成功后回填镜像 digest/URL 证据到本目标 attachments。 |
| **R-002** | low | I-007（GHCR 权限可达性）open：`packages: write` 依赖仓库权限与 `GITHUB_TOKEN` 对 GHCR 命名空间的有效性。 | 首次发布实测关闭；若权限不足（如 GHCR 需 PAT），须用户书面调整或改用 PAT secret 并留痕。 |
| **R-003** | low | 薄装 e2e 测试在无 docker 环境自动跳过（`skipTest`）；CI ubuntu 有 docker 覆盖。 | 保持现状；CI 红绿以 ubuntu 为准。 |

## 必改项汇总

- **required / 阻断：无**（self 范围）。
- recommended：R-001～R-003（均不阻断；I-007 在发布验收前关闭）。

## 结论 + 建议

1. **self 范围 pass**：R4a/R4b 完成、证据可复核；R4c 的测试与 docker 构建部分完成。
2. **下一步（R4c 后半）**：`/audit` 独立审计（provider = grok build / grok-4.5 / thinking-high）——independent 通过且 I-007 关闭（或用户书面 residual）后，Root 复关（GOAL-001 `done`、VP-004 `closed`、workspace.md `closed`）。
3. 首次 tag 发布后回填 GHCR 镜像发布证据（R-001/R-002 触发）。
