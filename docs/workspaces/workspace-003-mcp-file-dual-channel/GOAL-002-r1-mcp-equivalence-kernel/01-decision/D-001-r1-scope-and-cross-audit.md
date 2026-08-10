---
id: D-001
goal_id: GOAL-002-r1-mcp-equivalence-kernel
title: R1 范围、边界与 cross 审计模式
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-001 · R1 范围、边界与 cross 审计模式（2026-08-07）

## 决定

1. 本目标覆盖 R1 的方案澄清、合同/测试设计、File/MCP 分通道实现与验证准备。
2. `vision`、`vision-audit`、`govern`、`audit` 是 R1 的四个必达治理入口；`commit` 不纳入本目标的等价集合。
3. `deliveryChannel: files | mcp` 作为分通道证据的合同边界；共享测试内核只能承载 L2 共享断言，不能替代任一通道的 L1 证据。
4. 本目标采用 `cross` 审计模式。用户已确认继续按该模式立项；independent provider 尚未指定，实施开始前必须补齐。

## 未选方案

- 不把 MCP mock 当作 File 通道证据。
- 不把 R2/R3 内容提前并入 R1。
- 不因 provider 尚未指定而静默降级为 `self` 或 `none`。

## 依据

- VP-004 R1 交付约定：`docs/vision/plans/VP-004-mcp-file-dual-channel-delivery.md`。
- 当前 Root 信息门禁：`GOAL-001-mcp-file-dual-channel-delivery/00-meta.md` 的 I-001/I-002/I-004。
