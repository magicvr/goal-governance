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

本索引与 [00-meta.md](00-meta.md) 信息表同源。I-001、I-002、I-003 为 required/open；I-004 为 non-blocking/open。未关闭前不得把对应门禁写成已验证。

| ID | 级别 | 状态 | 影响 |
|----|------|------|------|
| I-001 | required | open | R1 方案冻结 |
| I-002 | required | open | R1 实施 |
| I-003 | required | open | R1 实施与 cross 审计验证 |
| I-004 | non-blocking | open | R1 宿主验收 |

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-08-07 | R1 范围、边界与 cross 审计模式 | accepted | `01-decision/D-001-r1-scope-and-cross-audit.md` |

## 当前方案边界

- 先澄清 I-001，再冻结 I-002 相关合同与测试落点；不得先写实现后补门禁。
- File 与 MCP 的 L1 证据必须分列；共享只限 L2 核心断言/fixture。
- R2/R3 工作留在 Root 后续阶段，不通过本目标的名称或测试假装已覆盖。
