---
id: GOAL-002-r1-mcp-equivalence-kernel
title: R1：MCP/File 等价验证内核
status: active
parent: GOAL-001-mcp-file-dual-channel-delivery
plan_refs: VP-004-mcp-file-dual-channel-delivery
primary_plan: VP-004-mcp-file-dual-channel-delivery
serves_summary: 服务 VP-004 R1；定义 MCP 最小运行形态、四治理入口映射、deliveryChannel 合同分列与 File/MCP 共享 L2 验证内核
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
progress: 0%
---

# GOAL-002 · R1：MCP/File 等价验证内核

## 概述

在 `workspace-003-mcp-file-dual-channel` 的 Root `GOAL-001-mcp-file-dual-channel-delivery` 下，推进 VP-004 的 R1 阶段。目标是先把 MCP 通道的最小运行形态与四治理入口映射讲清，再建立 `deliveryChannel: files | mcp` 的合同分列、File/MCP 分通道 L1 证据与共享 L2 fixture/断言内核。

本目标处于方案与信息澄清阶段；现有仓库尚未提供 MCP Server/tool 实现、`deliveryChannel` 合同字段或 File/MCP 共享 L2 fixture，均不得假定为已存在。

## 成功标准（R1 子目标检查点）

- [ ] C1：I-001 已有可核对结论：MCP 运行时形态、四治理入口映射、tool 名称与关键参数边界已记录。
- [ ] C2：`deliveryChannel` 合同分列及 L1/L2/L3 证据分级已冻结，并与现有 File contract/schema 不冲突。
- [ ] C3：共享 L2 fixture/核心断言与 File/MCP 分通道 L1 测试均已实现，且没有用 MCP mock 替代 File 证据。
- [ ] C4：R1 证据完成 self + independent 审视；所有 required 信息与 finding 按合法路径闭合。

`progress: 0%` = C1–C4 已完成 0 / 4。progress 仅为展示，不放行 R1，不关闭信息门禁，也不推导本目标 `done`。

## 纲领路线图与边界

1. **方案澄清**：关闭 I-001，明确 MCP 运行时与四入口映射；同步记录不确定项。
2. **合同与测试设计**：关闭 I-002 的范围决策，冻结 `deliveryChannel` 分列和共享 L2 检查点。
3. **分通道实现**：分别建立 File 与 MCP 的 L1 证据，并复用共享 L2 核心断言。
4. **验证与关门准备**：收集可核对事实，运行 self + independent 审视，响应 required findings。

本目标不包含 R2 的 bootstrap/lifecycle/gitignore/AGENTS managed，也不包含 R3 的 `governance_root` 配置实现与 canonical 规则修订。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | MCP 最小运行时形态与 Skills/宿主入口到 `vision`、`vision-audit`、`govern`、`audit` 的映射 | R1 方案冻结 | 方案澄清 | 对照现有 File 入口、MCP 合同草案与可运行边界 | open | 进入方案前复核 | 待确认 |
| I-002 | required | 共享 L2 fixture 范围、等价断言及其在 `docs/tests`/`skills` 中的落点 | R1 实施 | 合同与测试设计 | 对照 VP-004 R1 检查点并设计 File/MCP 分列测试 | open | 进入实施前复核 | 待确认 |
| I-003 | required | `cross` 审计所需 independent provider | R1 实施与验证 | 实施前 | 由用户指定可用 provider；失败不得静默降级 | open | provider 未指定前保持阻断 | 待用户指定 |
| I-004 | non-blocking | P0 宿主 L3 探针环境是否本机/CI 可用 | R1 宿主验收 | R1 验收 | 各宿主只读 dispatch 探针 | open | 不可用时按范围记录 residual | 待确认 |

## 愿景对齐

- Charter：`vision-goal-governance@0.2.0`
- primary plan：[VP-004-mcp-file-dual-channel-delivery](../../vision/plans/VP-004-mcp-file-dual-channel-delivery.md)
- parent：[GOAL-001-mcp-file-dual-channel-delivery](../GOAL-001-mcp-file-dual-channel-delivery/00-meta.md)
- workspace：`workspace-003-mcp-file-dual-channel` · `vision_role: delivery`

## 实施前治理门禁

已按用户 2026-08-07 确认采用 `cross` 审计模式：需要本目标 self 审视与至少一个指定 provider 的 independent 审视。provider 尚未指定，因此当前只完成子目标立项与边界记录，未进入实施放行。
