---
id: GOAL-006-consumer-surface-convergence
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-08
updated: 2026-08-08
version: 0.2.0
---

# 决策记录 · GOAL-006

## 信息需求与阶段门禁

> 本文件是稳定索引。信息台账可放在这里；长决策和独立决策记录放在 `01-decision/D-NNN-<slug>.md`。`accepted-residual` 必须指向用户的书面决策或审计响应，且不等同于 `verified`。

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 决策 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | `{governance_root}` 占位符在安装展开链路中的处理方式（纯文档语义 vs 安装时按 pin 替换） | S1 方案冻结 | S1 方案 | 盘点 install/薄壳/消费仓展开 + 对照 alignment 定义句 | **closed**（2026-08-08） | — | E-002 盘点（14 文件约 240 处）+ D-001：**A+C 混合**（字面相对化 + 模板 `{{GOVERNANCE_ROOT}}` 占位；无机器展开） |
| I-002 | non-blocking | 相对化对已发布 zip / 已安装消费仓的兼容面影响 | S3 验收 | S3 | 对照已发布资产与消费方样例 | open | — | 待确认 |

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-08-08 | 消费面路径相对化方案冻结（A+C 混合） | accepted | `01-decision/D-001-relativeization-scheme.md` |
