---
title: Goal Tree · 消费交付双通道（MCP + File）
status: active
created: 2026-08-07
updated: 2026-08-07
parent: null
version: 0.7.0
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

## 树

```text
GOAL-001-mcp-file-dual-channel-delivery  [active]  progress 75%
├─ GOAL-002-r1-mcp-equivalence-kernel  [done]  progress 100%
├─ GOAL-003-r2-dual-channel-productization  [done]  progress 100%
├─ GOAL-004-r3-configurable-governance-root  [done]  progress 100%
└─ GOAL-005-r4-mcp-docker-release  [active]  progress 67%
```

## 状态表

| id | title | parent | status | progress | notes |
|----|-------|--------|--------|----------|-------|
| GOAL-001-mcp-file-dual-channel-delivery | 消费交付双通道（MCP + File）与可配置治理根 | null | active | 75% | Root；primary_plan=VP-004；R1–R3 完成关门，**R4 发布缺口 reopen**（GOAL-005 进行中，VP-004 回退 active） |
| GOAL-002-r1-mcp-equivalence-kernel | R1：MCP/File 等价验证内核 | GOAL-001-mcp-file-dual-channel-delivery | done | 100% | C1–C4 闭合；A-001/A-002/A-003 全 pass |
| GOAL-003-r2-dual-channel-productization | R2：双通道产品化 | GOAL-001-mcp-file-dual-channel-delivery | done | 100% | C1–C6 闭合；F-001 fixed 后全 pass |
| GOAL-004-r3-configurable-governance-root | R3：可配置 governance_root 与消费面收敛 | GOAL-001-mcp-file-dual-channel-delivery | done | 100% | C1–C5 闭合；A-001/A-002/A-003 全 pass |
| GOAL-005-r4-mcp-docker-release | R4：MCP Docker 资产发布与通道资产分离 | GOAL-001-mcp-file-dual-channel-delivery | active | 67% | R4a 冻结（D-001）+ R4b 实施完成（搬迁 mcp/、Dockerfile、workflow GHCR、薄装重定义）；R4c cross 审计待跑 |

下一编号：**GOAL-006**。
