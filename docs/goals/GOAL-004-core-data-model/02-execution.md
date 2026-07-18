---
id: GOAL-004-core-data-model
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.3.0
---

# 执行记录 · GOAL-004

## 时间线

### 2026-07-18 · 目标立项

- 在 GOAL-001 下创建本目标完整五件套（meta / decision / execution / audit / attachments）。
- 因范围跨模型、CRUD 与 Web 接入，按 P-001 在 [00-meta.md](00-meta.md) 写高层路线图（阶段 A→D），**本回合未**批量创建细粒度子目标。
- 决策记录确认：独立立项、Markdown 为 SoT、细粒度选型延后至阶段 A（见 [01-decision.md](01-decision.md)）。
- 同步更新 [goal-tree.md](../goal-tree.md)；轻量更新 GOAL-001 路线图阶段 3 关联。
- 进度 **0%**：仅完成立项与路线图。

### 2026-07-18 · 阶段 A：领域模型与存储约定

- 产出设计说明：[attachments/domain-model-and-storage.md](attachments/domain-model-and-storage.md)（实体、五件套映射、列表数据源、写路径校验与 goal-tree 同步、服务模块建议、阶段 B 检查清单）。
- 记录决策 **D-004～D-007**（见 [01-decision.md](01-decision.md)）；关闭 D-003 中阶段 A 待确认三项。
- 勾选成功标准「完成 Goal 及关联实体的数据模型设计」；路线图阶段 A → 已完成。
- 进度调整为 **25%**（四阶段中 A 完成；B/C/D 与 CRUD/Web 未实现）。
- 同步 [goal-tree.md](../goal-tree.md)。

### 2026-07-18 · 阶段 A：设计审计整改闭环

- 在 [03-audit.md](03-audit.md) 记录 **A-001** 条件通过审计，识别无效文档结果、路径边界、写回恢复、审计结论误报、树漂移报告和 version 约束六项问题。
- 在 [01-decision.md](01-decision.md) 记录并接受 **D-008～D-013**：显式加载结果、canonical ID 与 containment、结构化树校验报告、显式审计结论状态、version 必填、可恢复多文件提交。
- 将 [attachments/domain-model-and-storage.md](attachments/domain-model-and-storage.md) 修订至 **v0.2.0**，补齐上述契约及阶段 B 测试检查项。
- 文档诊断未发现格式错误；未修改 GOAL-004 的范围、status 或 progress，因此 `goal-tree.md` 无需变更。
- 进度保持 **25%**：阶段 A 设计已评审并修正，阶段 B 读取代码尚未开始。

## 待办

1. 阶段 B：在 `web/services/` 实现只读 `list_goals` / `get_goal`（含加载诊断、路径 containment、树校验报告），加夹具单测
2. 阶段 C：Create/Update 写回 + goal-tree 强制同步
3. 阶段 D：首页/详情接真实数据

## 进度评估

**约 25%**：阶段 A 设计、审计与整改已闭环；读取路径与代码尚未开始。
