---
title: Goal Tree · 消费交付双通道（MCP + File）
status: active
created: 2026-08-07
updated: 2026-08-07
parent: null
version: 0.9.0
---

# Goal Tree

> 工作区：`workspace-003-mcp-file-dual-channel` · `primary_plan` = VP-004 · `vision_role` = delivery
> 目标状态真相仅本目录五件套 + 本文件；不汇总 progress 到愿景目录。

## 2026-08-07 · 开区 + Root

`/govern`：用户确认开 **workspace-003-mcp-file-dual-channel**（delivery，挂 VP-004）；VP-004 → `active`；Root **GOAL-001-mcp-file-dual-channel-delivery** `active`；纲领 R1→R2→R3 写入 Root；尚未建子目标。

## 2026-08-07 · R1 子目标立项

`/govern`：用户确认建立 R1 子目标 **GOAL-002-r1-mcp-equivalence-kernel**；目标状态 `active`、进度 0%；I-001/I-002/I-003（cross 审计 provider）仍为 open；尚未进入 R1 实施。

## 2026-08-07 · R1 方案冻结 + 实施 + 宿主探针

`/govern`（本推进轮）：GOAL-002 方案冻结（D-002/D-003/D-004 关闭 I-001/I-002/I-003）；`skills/mcp/` 双通道实现落盘；合同 `deliveryChannel` 分列（contractFormatVersion 0.4.0）；L2 共享内核 + File/MCP 分列 L1 测试（25 条新增）全绿；四宿主 L3 抽稀探针全 pass。GOAL-002 进度 0% → 75%（C1–C3 完成，C4 审计待闭合）。

## 2026-08-07 · 最终关门

`/govern`（本推进轮）：A-007（independent，conditional）F-001～F-004 全部 fixed（Root 成功标准/信息表修正、台账索引补登、L3 探针重捕获绑定当前树、goal-tree 收口）；A-008 登记关门。**Root `done`**；VP-004 `status: closed`（关门记录已填）。

## 2026-08-07 · 发布面核查 → R4 reopen + 立项

用户指令核查发布资产面（A-009 关门复审后）发现三项缺口：① File zip 混入 `skills/mcp/` 实现源码（通道资产未分离）；② MCP server 无可分发 Docker 发布资产（无 Dockerfile / 无 GHCR 发布步骤 / README 无安装指南）；③ `skills/mcp/README.md`「Dockerfile 可选」文案与事实不符。用户书面确认「全套方案」：**Root 回退 `done → active`**（progress 100% → 75%，纲领 3/4）；VP-004 与 workspace.md 回退 active；新开 **GOAL-005-r4-mcp-docker-release**（R4：MCP Docker 资产发布与通道资产分离，progress 0%）。

## 2026-08-07 · R4c 合并响应与关门

`/govern`（用户指令「合并响应 GOAL-005 的 A-001 和 A-002」）：A-001（self pass）+ A-002（independent pass）无 required、无冲突；**A-003** 合并响应登记（F-002 fixed——workflow 契约测试增补 R4 Docker 步骤断言并验证 7 passed；R-003/F-004/F-005 accepted；R-001/R-002/F-001/F-003 deferred 含触发）。**C3 闭合 → GOAL-005 `done`（100%）**；I-007 open（non-blocking）于首次真实 GHCR 发布验收时关闭。Root/VP-004 复关待下一轮（连带 F-003：VP-004 #8 路径字面 `skills/mcp/` → `mcp/`）。

## 2026-08-07 · Root/VP-004 复关（R4 完成）

`/govern`（用户确认）：GOAL-005 `done` 后复关——**A-011**（Root 03-audit，self）核验 VP-004 退出判据 #8（通道资产分离 80/0、Docker 同 tag 发布管线 + 契约断言、README 一致）并响应 **F-003 fixed**（#8 路径字面 `skills/mcp/` → `mcp/`）；**Root `done`**（progress 75% → 100%，纲领 R1–R4 4/4）；**VP-004 `closed`**（退出判据 1–8 证据链完整）；**workspace.md `closed`**。I-007 open（non-blocking）于首次真实 GHCR 发布验收时关闭。

## 树

```text
GOAL-001-mcp-file-dual-channel-delivery  [done]  progress 100%
├─ GOAL-002-r1-mcp-equivalence-kernel  [done]  progress 100%
├─ GOAL-003-r2-dual-channel-productization  [done]  progress 100%
├─ GOAL-004-r3-configurable-governance-root  [done]  progress 100%
└─ GOAL-005-r4-mcp-docker-release  [done]  progress 100%
```

## 状态表

| id | title | parent | status | progress | notes |
|----|-------|--------|--------|----------|-------|
| GOAL-001-mcp-file-dual-channel-delivery | 消费交付双通道（MCP + File）与可配置治理根 | null | done | 100% | Root；primary_plan=VP-004；R1–R4 全部完成（GOAL-002/003/004/005 done）；VP-004 closed；工作区 closed（A-011 复关） |
| GOAL-002-r1-mcp-equivalence-kernel | R1：MCP/File 等价验证内核 | GOAL-001-mcp-file-dual-channel-delivery | done | 100% | C1–C4 闭合；A-001/A-002/A-003 全 pass |
| GOAL-003-r2-dual-channel-productization | R2：双通道产品化 | GOAL-001-mcp-file-dual-channel-delivery | done | 100% | C1–C6 闭合；F-001 fixed 后全 pass |
| GOAL-004-r3-configurable-governance-root | R3：可配置 governance_root 与消费面收敛 | GOAL-001-mcp-file-dual-channel-delivery | done | 100% | C1–C5 闭合；A-001/A-002/A-003 全 pass |
| GOAL-005-r4-mcp-docker-release | R4：MCP Docker 资产发布与通道资产分离 | GOAL-001-mcp-file-dual-channel-delivery | done | 100% | R4a/R4b/R4c 全部完成；A-001/A-002 pass + A-003 合并响应（F-002 fixed）；I-007 发布验收时关闭 |

下一编号：**GOAL-006**。
