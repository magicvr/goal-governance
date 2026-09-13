---
id: GOAL-008-consumer-layer-split-and-hosting
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.2.0
---

# 决策记录 · GOAL-008

## 信息需求与阶段门禁

> 本文件是稳定索引。信息台账与 [00-meta.md](00-meta.md) 同源；长决策写在 `01-decision/D-NNN-<slug>.md`。`accepted-residual` 必须指向用户书面决策或审计响应，且不等同于 `verified`。

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 决策 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 双层路线图命名与判定缺口 | S1 / S2 方案冻结 | S2 前 | 盘点 P-006 / alignment / prompts / 模板 + 最小反例 | open | — | 待确认 |
| I-002 | required | 愿景总路线图与 VP 跟踪的权威落点 | S1 / S3 方案冻结 | S3 前 | 对照 roadmap.md、VP 正文、alignment 工件表 | open | — | 待确认 |
| I-003 | required | 消费仓 `AGENTS.md` / `docs/` 共存模型 | S1 / S4 方案冻结 | S4 前 | 盘点 install / updater / 完整安装 MUST | open | — | 待确认 |
| I-004 | required | `/commit` 命令形状、宿主覆盖与 fail-closed 负例（治理边界已由 D-002 冻结） | S1 / S5 方案冻结 | S5 前 | 对照 checkpoint 契约、VP-004 入口面与现有 prompt | open | — | D-002：便利可选；形状仍待确认 |
| I-005 | required | cross 审计 independent provider | S2 实施 | S2 实施前 | 用户书面指定；失败不降级 | open | provider 失效时回到门禁 | D-002：S1 可不含此项 |
| I-006 | required | 发布版本、tag/revision、资产清单、回归矩阵、cross 覆盖、consumer/producer 证据归属 | S6 发布 | S6 前 | 对齐当前版本源与远端基线 | open | 基线前移时重算 | F-005 绑定；待冻结 |

I-001～I-006 不阻断目标设立；未经验证不得把候选机制写成已选方案。

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-09-13 | 将四项消费仓痛点纳入同一 R3 大目标，并采用 S1 先行路线图 | accepted | `01-decision/D-001-scope-and-roadmap.md` |
| D-002 | 2026-09-13 | 响应 A-001：唯一化闸门、并行写集与 `/commit` 边界 | accepted | `01-decision/D-002-a001-response.md` |
