---
id: GOAL-009-info-deadlock-and-managed-placeholders
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-10-01
version: 0.9.1
---

# 决策记录 · GOAL-009

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同源。I-001、I-002、I-004 已由 D-002 记为 verified。I-003 已由 D-004 记为 verified：用户不走「不替换占位符」这一支。

| ID | 级别 | 状态 | 影响 |
|----|------|------|------|
| I-001 | required | verified | S2 方案冻结前的条文级死锁证据已有；原则正文已由 D-003 修改 |
| I-002 | required | verified | S3 方案冻结前的复现与负结果已有；策略已由 D-004 选定 |
| I-003 | required | verified | 用户拒绝「不替换占位符」分支；截断句不再需要 |
| I-004 | required | verified | provider 已书面指定为本地 codex / `gpt-6.1-sol` / high。用户于 2026-10-01 书面选择继续修正剩余的空后缀。[A-009](03-audit/A-009-a007-reaudit.md) verdict 为 pass。开放 required 为无。用户尚未书面确认关门 |

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-09-30 | 两条反馈纳入同一 R3 子目标，S1 先行 | accepted | `01-decision/D-001-scope-and-roadmap.md` |
| D-002 | 2026-09-30 | S1 证据闭合条文与复现，占位符策略不在本条冻结 | accepted | `01-decision/D-002-s1-evidence.md` |
| D-003 | 2026-09-30 | 结果尚不存在时不是进入该项工作的门禁 | accepted | `01-decision/D-003-research-result-is-not-a-gate.md` |
| D-004 | 2026-09-30 | 安装时渲染受管占位符，升级按双基线比较 | accepted | `01-decision/D-004-render-placeholders-on-install.md` |
| D-005 | 2026-09-30 | F-001 按受管映射闭合；F-002 评估不构成闭合 | accepted | `01-decision/D-005-f001-managed-map.md` |
| D-006 | 2026-09-30 | F-002 按保留标记外字节闭合 | accepted | `01-decision/D-006-f002-preserve-outside-bytes.md` |
| D-007 | 2026-09-30 | A-005 的必改项按继续修正闭合 | accepted | `01-decision/D-007-a005-continue-fix.md` |
| D-008 | 2026-10-01 | A-007 的空后缀按继续修正闭合 | accepted | `01-decision/D-008-a007-empty-suffix.md` |
