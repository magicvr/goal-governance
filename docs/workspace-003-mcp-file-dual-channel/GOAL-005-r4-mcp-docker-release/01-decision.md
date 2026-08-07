---
id: GOAL-005-r4-mcp-docker-release
doc: decision
status: active
parent: GOAL-001-mcp-file-dual-channel-delivery
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
---

# 决策 · GOAL-005

> 本文件是稳定索引。每条正式决策完整写在 `01-decision/D-NNN-<slug>.md`；信息项与残余风险以 `00-meta` 信息表为同源核对入口。

## 审计模式（R4 · cross）

发布/生产面高影响门禁 → `cross`：self（04）+ 至少一个指定 provider 的 independent（05）。independent provider 沿用 [GOAL-002 D-004](../GOAL-002-r1-mcp-equivalence-kernel/01-decision/D-004-r1-provider-assignment.md) 的用户指定：**Grok Build（grok-4.5 / thinking-high）**。provider 不可用/失败时门禁保持未满足，不静默降级。

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-08-07 | R4a 方案冻结：通道资产分离布局（根目录 `mcp/`）+ Docker 发布形态（I-005/I-006 关闭） | accepted | `01-decision/D-001-r4a-freeze-layout-and-docker-release.md` |

## 信息需求登记

见 `00-meta.md` 信息表：I-005（GHCR 命名/tag 策略，required，R4a）→ **closed**（用户确认，D-001）；I-006（容器运行形态，required，R4a）→ **closed**（用户确认固定入口，D-001）；I-007（GHCR 权限可达性，non-blocking，R4c）open。
