---
id: GOAL-NNN-short-slug
doc: audit
status: active
parent: GOAL-001-root-slug
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.2.0
---

# 审计 · GOAL-NNN

> 本文件是稳定索引和信息核对入口。每条正式意见完整写在 `03-audit/A-NNN-<slug>.md`；reader 同时兼容本文件内 legacy `A-NNN` 正文。
> 未关闭的 required 信息项应作为 finding，不得被写成“已知”或“已完成”。

## 信息就绪核对（按 scope）

| 核对项 | 状态 | 备注 |
|--------|------|------|
| 影响本 scope 的 I-00N | 待填 | 编号与最晚阶段 |
| 到期 required 是否已 verified / residual | 待填 | 未关闭项阻断对应门禁 |
| 资料引用（若有）是否固定且用户确认 | 待填 / 无 | 缺字段 fail closed |

## 目标漂移核对（GD-01～GD-08）

每条 self/independent A 意见必须自主读取直接父目标相关正文/决策（Root 对 VP），并保留本 scope 的「父级条目/版本→原始承诺及有效授权变更→当前范围/阶段→实际证据→对齐/漂移/证据不足及影响门禁」对照，小 scope 可一段。不可只审当前本地清单/测试；显著漂移或无授权验收替代形成 required finding，缺关键证据登记 required 缺口，闭合前不放行。合法贡献子集/调查阶段/已批准演进不自动算漂移，剩余承诺须保留。权威：`{governance_root}/architecture/principles.md#goal-drift`。

## 意见台账索引

| A-ID | 日期 | source | scope | verdict | 开放 required | 文件 |
|------|------|--------|-------|---------|---------------|------|
| A-001 | YYYY-MM-DD | self / independent | `<scope>` | pass / conditional / fail | N | `03-audit/A-001-<slug>.md` |

## 结论状态

尚未到达审计节点。独立意见不直接改 `status` / `progress`；响应和状态变更走 `/govern` 与用户裁决。
