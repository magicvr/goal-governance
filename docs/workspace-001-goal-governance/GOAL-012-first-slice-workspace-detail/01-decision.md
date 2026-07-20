---
id: GOAL-012-first-slice-workspace-detail
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.1.0
---

# 决策记录 · GOAL-012

## D-001 · 立项首垂直切片实现并冻结 α 范围（2026-07-21）

**状态**：accepted

**确认来源**：用户接受建议选项并要求开始推进；GOAL-009 [D-012](../GOAL-009-ai-assisted-governance-workbench/01-decision.md) 关闭 F-005（路径 α）并授权本目标。

**决定**：

1. 本目标实现范围严格等于 α：单一配置选中的**产品工作区**详情（目标树核心）+ 用户提供执行事实 + 门禁内受限 `append-execution-fact`。
2. 不实现：总览/列表 N1 产品化、共享资料 CRUD、AI/工具、SQLite、多用户。
3. 配置 fail closed：无显式数据根/工作区则不加载；禁止默认本仓 dogfood（开发开关可选）。
4. 契约测试使用合成 fixture；生产写入启用绑定 GOAL-009 F-007/F-008 与 I-003/I-004/I-006。
5. 权威设计：R-004 §6 + 已接受规格包；中间对象非 canonical。

**未选方案**：

- 把 GOAL-009 规划目标直接改成实现目标：混淆发现与交付证据。
- 首目标同时做 N1+资料+AI+写入：违背 α 与 F-009 教训。
- 首切片引入 SQLite：D-011 已排除。

**影响**：创建本五件套并开始编码准备；不自动开放生产写入。
