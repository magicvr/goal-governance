---
id: GOAL-001-mcp-file-dual-channel-delivery
title: 消费交付双通道（MCP + File）与可配置治理根
status: active
parent: null
plan_refs: VP-004-mcp-file-dual-channel-delivery
primary_plan: VP-004-mcp-file-dual-channel-delivery
serves_summary: delivery Root；服务 VP-004 / vision-goal-governance@0.2.0；File+MCP 双通道、四承诺宿主、最小测试内核与可配置 governance_root
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
progress: 0%
---

# GOAL-001 · 消费交付双通道（MCP + File）与可配置治理根

## 概述

在 Charter `vision-goal-governance@0.2.0` 与 **VP-004** 下，交付 **File** 与 **MCP** 双通道一等公民消费适配：同一协议与四治理入口语义，分发形态与证据分列；并实现可配置 `governance_root`（默认 `docs`，内部布局冻结）。

本 Root 是 [workspace-003-mcp-file-dual-channel](../workspace.md) 的唯一 `parent: null` 总目标。**不**以本仓 Web / VP-003 驱动；协议内容反馈演进主波次仍在 [workspace-002](../../workspace-002-methodology-skills-feedback/) / VP-002。

## 成功标准（Root 方向级 · 暂定 · 对齐 VP-004 退出）

- [ ] 双通道一等：File 与 MCP 均可按发布约定取得；推荐 MCP 不废除 File
- [ ] R1：MCP 无 File 大包可达四治理入口等价检查点；L2 共享 + 分通道 L1 + 抽稀 L3 可读
- [ ] R2：薄壳 lifecycle、gitignore 默认、AGENTS managed、生产仓 File 自举有证据
- [ ] R3：`governance_root` 可配置 + 越界 fail closed + canonical 权威修订（或 residual）
- [ ] 宿主：P0（Claude / Grok / Codex）达约定级验证；P1 Copilot 至少 L1（缺 L3 须 residual）
- [ ] **不**要求关闭 VP-002/VP-003 或 Charter 可完成

## 纲领路线图（P-001 · 对齐 VP-004 R1–R3）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **R1** | MCP 通道并行达标 + 最小共享测试内核 | **未开始** | 四入口等价检查点；L2 共享 + L1 分列 + 抽稀 L3；合同 `deliveryChannel` 分列 |
| **R2** | 双通道产品化 | **未开始** | bootstrap 双入口；薄壳 lifecycle；gitignore；AGENTS managed；File-classic |
| **R3** | 可配置 `governance_root` 与消费面收敛 | **未开始** | 配置 pin；仓外 fail closed；alignment/AGENTS/templates 权威路径补丁（V-F-013 车辆） |

同一纲领阶段内可并行多个子目标；阶段间通常串行。子目标按阶段再立，本回合只 scaffold Root。

## 派生进度展示

`progress: 0%` = 纲领阶段 R1～R3 中已完成 **0 / 3**（等权）。progress **仅展示**，不放行阶段、不关闭 finding、不推导 Root `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | MCP 通道最小运行时形态（进程/stdio 或 Docker 推荐路径）与薄 Skills/宿主入口如何映射四治理入口 | R1 方案冻结 | R1 方案 | 对照现有 skills 入口 + MCP 合同草案 | open | — | 待 R1 首子目标澄清 |
| I-002 | required | 共享测试内核 L2 fixture 范围与「等价」检查点落地位置（docs/tests vs skills） | R1 实施 | R1 实施 | 对照 VP-004 十条检查点设计套件 | open | — | 待方案 |
| I-003 | required | `governance_root` 项目配置 schema 与权威面改写清单（alignment 等） | R3 方案冻结 | R3 方案 | 按 VP-004 R3 车辆列 diff 清单 | open | — | 不阻断 R1 启动 |
| I-004 | non-blocking | P0 宿主 L3 探针环境是否本机/CI 可用 | R1 宿主退出 | R1 验收 | 各宿主只读 dispatch 探针 | open | 不可用则 residual | — |

## 愿景对齐

| 项 | 值 |
|----|-----|
| Charter | `vision-goal-governance@0.2.0` |
| primary_plan | [VP-004-mcp-file-dual-channel-delivery](../../vision/plans/VP-004-mcp-file-dual-channel-delivery.md) |
| workspace | `workspace-003-mcp-file-dual-channel` · `vision_role: delivery` |
| lead | 本区 = VP-004 `lead_workspace` |
| 并行区 | [workspace-002](../../workspace-002-methodology-skills-feedback/) · VP-002（不混 parent） |

## 子目标

| id | title | status |
|----|-------|--------|
| — | （尚未创建；R1 首子目标下一拍 `/govern` 再立） | — |

## 备注

- 开区决策见 [01-decision/D-001-open-workspace-003.md](01-decision/D-001-open-workspace-003.md)。
- 编号自 GOAL-001 起；**不**延续其他工作区编号。
- 宿主 P0/P1、入口等价检查点、R3 协议车辆以 VP-004 v0.1.1+ 正文为准。
