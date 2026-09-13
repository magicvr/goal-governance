---
id: GOAL-NNN-short-slug
doc: decision
status: active
parent: GOAL-001-root-slug
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
---

# 决策记录 · GOAL-NNN

## 纲领路线图与阶段计划（按需）

> **纲领路线图**（P-001）写在 `00-meta.md` 或本文件的**阶段计划索引**节，二选一，不重复。层级边界：本表只属于**本目标**；愿景层没有可执行纲领路线图。
> **阶段计划**是本目标某阶段的方案与实施安排（**非树节点**、不建第二套状态源），通常落在 `01-decision/D-NNN-<slug>.md`。判定谓词见 `{governance_root}/architecture/principles.md` §6.4。

| 阶段 | 计划文件 / 落点 | 说明 |
|------|-----------------|------|
| S1 | `01-decision/D-001-<slug>.md` | `<该阶段方案要点>` |

## 信息需求与阶段门禁

> 本文件是稳定索引。信息台账可放在这里；长决策和独立决策记录放在 `01-decision/D-NNN-<slug>.md`，每条记录必须保持可独立阅读。`accepted-residual` 必须指向用户的书面决策或审计响应，且不等同于 `verified`。

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 决策 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required / non-blocking | `<问题或假设>` | `<方案 / 实施 / 关门>` | `<阶段>` | `<动作>` | open | `<deferred 时填理由、责任人、复核触发>` | 待确认 |

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | YYYY-MM-DD | `<标题>` | proposed / accepted / superseded | `01-decision/D-001-<slug>.md` |

> legacy inline 的 `## D-NNN` 记录仍可保留并被读取；新记录从目录写入。编号在本目标内单调不复用。
