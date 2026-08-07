---
id: A-002
goal: GOAL-005-r4-mcp-docker-release
title: R4 关门独立交叉审计（independent · close-out）
status: recorded
source: independent
auditor: grok build / grok-4.5（thinking-high；/audit 独立会话）
date: 2026-08-07
scope: R4 关门（R4a 冻结 + R4b 实施 + R4c 验证就绪）；对照成功标准、D-001、VP-004 退出判据 #8、信息门禁与 A-001 self
verdict: pass
version: 0.1.0
parent: null
---

# A-002 · R4 关门独立交叉审计（2026-08-07）

## 声明

- **source**：`independent`（`/audit`，非编排推进）
- 本意见**不**修改 `status` / 检查点 / 派生 `progress` / goal-tree / 方案正文
- 响应、finding 闭合与是否 `done` 由用户经 **`/govern`** 处理

## 范围与区间

| 项 | 内容 |
|----|------|
| 工作区 | `workspace-003-mcp-file-dual-channel`（`root_goal` = GOAL-001；`primary_plan` = VP-004；canonical = 本目录） |
| 目标 | GOAL-005-r4-mcp-docker-release（R4） |
| audit_type | close-out |
| 方案 | D-001（布局 / 固定入口 / 薄装 / 同 tag GHCR / 文档） |
| 实施 | E-001（搬迁、Dockerfile、workflow、bootstrap、README、引用面） |
| 既有意见 | A-001（self，pass；R-001～R-003 recommended） |
| 排除 | 不读不比其他工作区；不重审 R1–R3 子目标关门结论；不写 Vision Review 台账 |

## 独立核验（本会话亲自执行）

| 动作 | 结果 |
|------|------|
| 工作区绑定 | `workspace.md`：id / root / plan_refs / primary_plan 一致；共享资料表空（无固定引用义务） |
| 布局 | `skills/mcp` **不存在**；实现在仓库根 `mcp/`（含 `Dockerfile`、`.dockerignore`、server/lifecycle 等） |
| File zip 成员 | `pack_skills(version=0.0.0-audit, …)` → **80 成员**；含 `mcp` 字样仅 3 条 **`tests/test_mcp_*.py`**（测试名，非 MCP 实现路径）；**无** `mcp/server` / `skills/mcp` / 根级 `mcp/` 实现 |
| 全量回归 | `pytest docs/tests scripts/tests skills/tests` → **197 passed, 4 skipped, 4 subtests**（venv 现装 pytest 后复跑） |
| stage 镜像 | `python scripts/stage_skills_mirrors.py --check` → **ok**（36 对 0 漂移） |
| Docker 构建 | `docker build -t goal-governance-mcp-server:audit-local mcp/` 成功；`docker inspect` → `Entrypoint=["python"]` `Cmd=["server.py","--repo-root","/workspace"]`；`docker run … server.py --help` 输出合法 usage |
| workflow | `skills-pack-release.yml` publish：`packages: write`；`docker/login-action@v3`（ghcr.io）+ `docker/build-push-action@v6`（context `mcp/`）；tags = `ghcr.io/magicvr/goal-governance-mcp-server:${{ needs.pack.outputs.version }}` + `:latest`；位于 evidence gate **之后**；pack 输出 `version` 已去 `v` 前缀 |
| 薄装 | `install-online.{sh,ps1}`：`-Channel mcp` 写 contracts + `docker run … lifecycle.py install`（不 materialize mcp 代码）；e2e 在 suite 内（有 docker 则跑，无则 skip） |
| 文档 | 根 README「在其他项目中安装 MCP Server（Docker 通道）」；`mcp/README.md` Docker 主形态 + 本地 stdio 合法；**无**「Dockerfile 可选」空头文案 |
| 历史路径 `skills/mcp` | 残留于 CHANGELOG / 已关门台账 / 缺口叙述 / VP 历史句 —— **非**运行时 import 面 |

## 成果（有证据）

1. **通道资产分离成立**：File 发布只打 `skills/`；MCP 实现物理上在 `mcp/`，zip 结构性不可能混入实现源码；pack 测试含 `mcp/` 防御断言（`scripts/tests/test_pack_skills_release.py`）。
2. **Docker 发布形态就位**：Dockerfile 固定入口与 D-001/I-006 一致（默认 `python server.py --repo-root /workspace`；CMD 可覆盖以跑 lifecycle，与薄装路径一致）。
3. **同 tag 同版本发布结构**：同一 publish job、同一 pack `version` 输出驱动 File 资产与 GHCR 镜像 tag。
4. **薄装重定义**：MCP 通道不再把实现装进消费仓；contract + lifecycle 状态 + client 配置指引。
5. **文档与实现一致**：安装命令可核对；空头 Dockerfile 文案已消除。
6. **信息门禁**：I-005/I-006 required 已 closed（用户确认 + D-001）；无到期未关 required。

## 对照成功标准

| 标准 | 判定 | 证据 |
|------|------|------|
| 缺口已登记 | ✅ | 00-meta 概述三项缺口 |
| R4a 冻结（D-001；I-005/I-006 closed） | ✅ | D-001 + 信息表 |
| R4b 实施（搬迁/Dockerfile/workflow/薄装/README） | ✅ | E-001 + 本表核验 |
| R4c 验证与关门（测试绿 + docker 证据 + cross） | 🔶 **验证部分 ✅**；**正式 `done` 须 `/govern` 响应本意见后执行** | 197 绿；本地镜像构建；self A-001 + 本 independent |

## 对照 VP-004 退出判据 #8（发布资产面）

| 子项 | 判定 | 说明 |
|------|------|------|
| File 资产不含 MCP 实现 | ✅ | 80 成员；无实现路径 |
| MCP 以 Docker 镜像发布到 GHCR | ✅（**管线就位**） | workflow push 步骤存在；**尚无**真实 tag 发布 digest（见 F-001 / I-007） |
| 与 File 同 tag 同版本同时发布 | ✅（结构） | 同 job / 同 `needs.pack.outputs.version` |
| README 指南 + 无空头文案 | ✅ | 根 + `mcp/README.md`（实现路径已迁；VP 正文仍有历史 `skills/mcp/README.md` 字面，见 F-003） |

## 信息门禁核对

| I-ID | 级别 | 状态 | 对关门影响 |
|------|------|------|------------|
| I-005 | required · R4a | **closed** | 不阻断 |
| I-006 | required · R4a | **closed** | 不阻断 |
| I-007 | non-blocking · R4c | **open** | 不构成 required 开放门禁；首次真实 GHCR 发布验收前关闭为宜 |

## Findings

### required（必改 / 阻断）

**无。**

scope 内无 high required；无到期未关 required 信息项；成功标准与 VP-004 #8 在「实现 + 发布管线 + 本地可构建证据」层面可重复核对成立。真实 GHCR push 按目标信息表定为 non-blocking（I-007），**不得**用 progress% 替代上述证据。

### recommended（非阻断）

| ID | 严重度 | 说明 | 建议 |
|----|--------|------|------|
| **F-001** | med | **GHCR 镜像从未在真实 tag 发布流中推送过**（本环境仅本地 `docker build`）。A-001 R-001 同类。workflow 结构可审，**不能**声称「已在 GHCR 上可 pull 的正式发布物」。 | 下一次 annotated `v*` tag + `environment: release` 发布后，回填镜像 digest / `ghcr.io/...` URL 到本目标 `attachments/`；并关闭 I-007（或用户书面 residual，写清范围与复审触发）。 |
| **F-002** | low | **workflow 契约测试未钉死 R4 Docker 步骤**：`SkillsPackWorkflowContractTests` 校验 evidence gate / environment，**未**断言 `packages: write`、`docker/build-push-action`、`goal-governance-mcp-server` tag。回归时可能静默删掉发布步骤仍绿。 | 在 `test_pack_skills_release.py` 增补字符串/结构断言（与现有 publish 契约同风格）。 |
| **F-003** | low | **VP-004 退出判据 #8 正文仍写 `skills/mcp/` / `skills/mcp/README.md`**（reopen 时路径）。GOAL-005 实现已迁至根 `mcp/`；判据**意图**满足，字面路径过期。 | Root/VP 复关时用 `/vision` 或 `/govern` 连带把 #8 路径改为 `mcp/`（不改判据语义）。 |
| **F-004** | low | **D-001 字面 `ENTRYPOINT ["python","server.py"]` 与 Dockerfile 实际 `ENTRYPOINT ["python"]` + `CMD ["server.py",…]` 不完全同形**。默认行为等价，且 CMD 可覆盖更利于 lifecycle 薄装；属决策文本精度，非功能缺口。 | 可选：D-001 勘误一句，或接受为等价实现。 |
| **F-005** | low | 与 A-001 R-003 同构：薄装 e2e 在无 docker 环境 skip；本会话 docker 可用且全量 197 绿（含相关路径）。 | 保持；CI ubuntu 有 docker 为准。 |

## 必改项汇总

- **required / 阻断：无**
- recommended：F-001～F-005（F-001 最重要，属发布验收证据，不阻断本目标按 R4c 定义关门）

## 与既有意见（A-001 self）的异同

| 点 | A-001 self | 本 independent |
|----|------------|----------------|
| 总体 verdict | pass（self 范围） | **pass**（close-out 范围；确认可建议关门） |
| required | 无 | **无**（交叉确认） |
| GHCR 未实测 | R-001 recommended | **F-001** med recommended（加重表述：不可宣称已可 pull 正式物） |
| I-007 open | 同意 non-blocking | **同意** |
| 新增 | — | **F-002** workflow 契约未钉 Docker 步骤；**F-003** VP #8 路径字面；**F-004** ENTRYPOINT 文本精度 |
| 核验增量 | inventoriable 80/0 MCP 实现 | 复跑 pack zip 80 成员 + 全量 197 + 镜像 inspect 固定入口 |

**无冲突 verdict**；无「一要一否」的 required 冲突。不触发 P-004 冲突裁决。

## 结论 + 建议给编排器 / 用户

1. **verdict: pass** — R4 成功标准在实现与可重复本地证据层面满足；cross 的 independent 腿已落盘；无开放 required finding。
2. **可建议** `/govern`：将 GOAL-005 标为 `done`（R4c 检查点闭合 → progress 100%），并推进 Root / VP-004 / workspace 复关流程；同时登记 F-001～F-005 响应（fixed / deferred / residual）。
3. **不要**在未响应本意见前静默改 status；**不要**把 progress 67%→100% 当作放行依据——放行依据是本台账 + 成功标准证据。
4. Root 复关时建议顺手处理 F-003（VP #8 路径字面）与 F-001（发布后证据）。

### 建议的 `/govern` 下一句

```text
/govern 响应 GOAL-005 A-002（independent pass）：无 required；登记 F-001～F-005；确认 R4c 闭合并将 GOAL-005 → done，再评估 Root/VP-004 复关
```
