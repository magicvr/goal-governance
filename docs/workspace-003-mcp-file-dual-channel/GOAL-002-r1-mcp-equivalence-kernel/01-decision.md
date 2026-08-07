---
id: GOAL-002-r1-mcp-equivalence-kernel
doc: decision
status: active
parent: GOAL-001-mcp-file-dual-channel-delivery
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
---

# 决策记录 · GOAL-002

## 信息需求与阶段门禁

本索引与 [00-meta.md](00-meta.md) 信息表同源。I-001、I-002、I-003 已于 2026-08-07 以 D-002/D-003/D-004 关闭；I-004 于宿主探针通过后关闭。

| ID | 级别 | 状态 | 影响 |
|----|------|------|------|
| I-001 | required | closed（D-002） | R1 方案冻结 |
| I-002 | required | closed（D-003） | R1 实施 |
| I-003 | required | closed（D-004） | R1 实施与 cross 审计验证 |
| I-004 | non-blocking | closed | R1 宿主验收 |

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-08-07 | R1 范围、边界与 cross 审计模式 | accepted | `01-decision/D-001-r1-scope-and-cross-audit.md` |
| D-002 | 2026-08-07 | R1 方案冻结 · MCP 运行时形态与四治理入口映射（I-001） | accepted | `01-decision/D-002-r1-freeze-mcp-runtime-and-entry-mapping.md` |
| D-003 | 2026-08-07 | R1 方案冻结 · L2 共享内核范围与 deliveryChannel 合同分列（I-002） | accepted | `01-decision/D-003-r1-freeze-l2-kernel-and-contract-split.md` |
| D-004 | 2026-08-07 | R1 方案冻结 · cross 审计 independent provider 指定（I-003） | accepted | `01-decision/D-004-r1-provider-assignment.md` |

## 当前方案边界

- 先澄清 I-001，再冻结 I-002 相关合同与测试落点；不得先写实现后补门禁。
- File 与 MCP 的 L1 证据必须分列；共享只限 L2 核心断言/fixture。
- R2/R3 工作留在 Root 后续阶段，不通过本目标的名称或测试假装已覆盖。
