---
id: GOAL-012-first-slice-workspace-detail
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.2.0
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

## D-002 · 有界关门：α 实现完成，生产写入与 F-003 residual 不随关门解除（2026-07-21）

**状态**：accepted

**确认来源**：用户在 `/govern` 关门审视后明确「OK 按有界条件关门 GOAL-012」；条件为「生产写入仍关 + F-003 residual 不随关门消失」。

**决定**：

1. 将 GOAL-012 标为 `done / 100%`：α 成功标准已有可核对实现与测试证据（A-001/A-002/A-003）。
2. **关门范围仅限 α**：配置化产品工作区详情 + 门禁内 `append-execution-fact` + R-004 关键路径测试；不宣称生产写入、全矩阵 CT 或 GOAL-009 规划门禁关闭。
3. **生产 Web/AI 写入保持关闭**：继续绑定 GOAL-009 F-007/F-008 与 I-003/I-004/I-006；本目标 I-003 保持 `collecting`。
4. **F-003 / I-005 residual 在关门后仍有效**：幂等为进程内；`ops/receipts` 落盘但不保证跨重启重放；复审触发 = 开放生产写入前或 GOAL-009 F-008 关闭路径。
5. 关闭后不得把本目标 `done` 误读为「Web 工作台已可生产写入」。

**未选方案**：

- 因 F-003 residual 暂缓关门：非 α 成功标准必达项，会拖住已可交付切片。
- 关门时顺带宣称生产写入或关闭 GOAL-009 F-007/F-008：越权且证据不足。

**影响**：status/progress 与 goal-tree 同步；A-003 close-out 落盘；规划台账回 GOAL-009。
