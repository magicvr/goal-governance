---
id: D-002
goal_id: GOAL-001-mcp-file-dual-channel-delivery
title: 建立 R1 MCP/File 等价验证内核子目标
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-002 · 建立 R1 MCP/File 等价验证内核子目标（2026-08-07）

## 决定

1. 在当前工作区建立 `GOAL-002-r1-mcp-equivalence-kernel`，父目标为 `GOAL-001-mcp-file-dual-channel-delivery`。
2. 子目标只覆盖 VP-004 的 R1：MCP 最小运行形态与四治理入口映射、`deliveryChannel` 合同分列、File/MCP 分通道 L1 证据，以及共享 L2 fixture/断言内核。
3. R2 产品化与 R3 `governance_root` 不纳入本子目标；Root 继续保留 R1→R2→R3 的纲领路线图。
4. 本子目标采用 `cross` 审计模式。实施前必须指定 independent provider；在 provider 指定前不得将 R1 实施或验证写成已开始/已通过，也不得静默降级为 `self`。

## 理由与取舍

- R1 同时跨越协议合同、File/MCP 交付通道与测试证据边界，单一连续实施计划不足以表达其门禁关系，因此先建立独立子目标。
- 将 R2/R3 排除可保持 Root 纲领阶段串行，避免把尚未澄清的 `governance_root` 方案带入 R1。
- 保留 File 侧独立证据，避免用 MCP mock 替代 File 交付证明。

## 未决门禁

- I-001：MCP 运行时形态与四入口映射，R1 方案冻结前关闭。
- I-002：共享 L2 fixture 与等价检查点落点，R1 实施前关闭。
- I-003：`cross` 审计的 independent provider，R1 实施前指定。
