---
id: GOAL-004-core-data-model
doc: audit
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.3.0
---

# 审计 · GOAL-004

## A-001 · 阶段 A 数据模型设计审计（2026-07-18）

### 范围与区间

审计 GOAL-004 阶段 A 产出的领域模型与存储约定，重点核对领域边界、Markdown 真相源、读取降级、路径安全、树一致性和后续写回边界。证据包括：

- [attachments/domain-model-and-storage.md](attachments/domain-model-and-storage.md)
- [01-decision.md](01-decision.md) D-004～D-007
- [02-execution.md](02-execution.md)「阶段 A：领域模型与存储约定」
- 项目规则 [../../../AGENTS.md](../../../AGENTS.md) 与架构约定

### 成果（有证据）

- Goal 聚合五件套、Markdown + frontmatter 真相源、目录扫描为运行时权威的主方向与现有治理规则一致。
- 阶段 B 只读、阶段 C 写回、阶段 D Web 接入的先后边界清晰，没有提前引入数据库或复杂同步系统。
- 已明确 Goal、DecisionDoc、ExecutionDoc、AuditDoc、AttachmentRef 和 GoalTreeIndex 的基本职责。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 完成 Goal 及关联实体的数据模型设计 | 部分通过 | 设计主体已完成，但以下六项契约需修正后才能无条件通过 |
| 实现 Goal 基础 CRUD | 未开始 | 阶段 B/C 尚未实现 |
| Web 首页和详情页展示真实目标数据 | 未开始 | 阶段 D 尚未实现 |
| 详情展示决策 / 执行 / 审计基础信息 | 未开始 | 已有模型映射，尚无实现证据 |

### 偏差与问题

1. **无效文档结果不可表达**：`Goal` 必填字段与“列表标红并跳过结构化字段”互相冲突，需要显式加载结果和问题模型。
2. **路径边界缺失**：`get_goal(id)` 与附件读取尚未约定 canonical ID、目录 containment 和符号链接处理。
3. **写回恢复语义不足**：业务文件成功、goal-tree 失败时，仅返回错误和日志不能恢复一致性。
4. **审计结论启发式误报**：按“结论 / 已完成”关键词判断会把否定句误判为已有结论。
5. **树漂移结果不完整**：`GoalTreeIndex` 未承载 drift、环、孤儿、重复编号和字段冲突详情，也未规定稳定排序。
6. **version 约束冲突**：设计将 `version` 标为建议，但 AGENTS 要求每个 Markdown 必须包含该字段。

### 改进措施

- [ ] 定义 `GoalLoadResult` / `ValidationIssue`，明确有效、无效、不存在和缺文件的读取结果。
- [ ] 增加 ID 格式、路径 containment、符号链接与附件读取边界。
- [ ] 为阶段 C 规定预生成、临时文件、备份补偿、恢复记录和重建 tree 的失败恢复方案。
- [ ] 将审计结论改为显式 `conclusion_state`，仅解析明确结论区段或字段。
- [ ] 增加 `TreeValidationReport`、`tree_drift` 和数字编号稳定排序。
- [ ] 将 `version` 改为必填，缺失时只报告问题，不在普通读取中隐式写回。

### 结论与下一步

**条件通过**：领域方向合理，无需推翻模型或引入数据库；阶段 B 开工前应关闭第 1、2、4、5、6 项。第 3 项可在阶段 B 期间继续设计，但必须在阶段 C 写回代码开始前形成正式决策。

## A-002 · A-001 整改验证与闭环（2026-07-18）

### 范围与区间

验证 A-001 六项审计意见是否形成正式决策并落实到阶段 A 设计文档。验证依据：

- [01-decision.md](01-decision.md) D-008～D-013
- [attachments/domain-model-and-storage.md](attachments/domain-model-and-storage.md) v0.2.0
- [02-execution.md](02-execution.md)「阶段 A：设计审计整改闭环」

### 整改验证

| A-001 问题 | 决策 | 修正证据 | 状态 |
|-------------|------|----------|------|
| 无效文档结果不可表达 | D-008 | 增加 `GoalLoadResult`、`ValidationIssue` 及 List/Get 结果约定 | 已关闭 |
| 路径边界缺失 | D-009 | 增加 canonical ID、resolve containment、符号链接和附件边界 | 已关闭 |
| 写回恢复语义不足 | D-013 | 增加预生成、临时文件、备份补偿、recovery record 与 `repair_goal_tree()` | 设计项已关闭，待阶段 C 实现验证 |
| 审计结论启发式误报 | D-011 | `has_conclusion` 改为显式 `conclusion_state` 与明确章节解析 | 已关闭 |
| 树漂移结果不完整 | D-010 | 增加 `TreeValidationReport`、`tree_drift` 与稳定排序 | 已关闭 |
| version 约束冲突 | D-012 | version 改为必填；读取仅报告 issue，不隐式写回 | 已关闭 |

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 完成 Goal 及关联实体的数据模型设计 | 已达成 | 设计 v0.2.0 + D-004～D-013 + A-001/A-002 审计闭环 |
| 实现 Goal 基础 CRUD | 未开始 | 阶段 B/C 尚未实现 |
| Web 首页和详情页展示真实目标数据 | 未开始 | 阶段 D 尚未实现 |
| 详情展示决策 / 执行 / 审计基础信息 | 未开始 | 模型已定义，尚无代码与页面证据 |

### 偏差、风险与后续验证

- 本轮关闭的是**设计契约缺口**，不是代码实现验证；阶段 B 必须按设计 §10 的夹具测试证明读取降级、路径拒绝、树诊断与稳定排序。
- D-013 已关闭“缺少恢复设计”的审计意见，但可恢复提交仍须在阶段 C 通过故障注入测试验证。
- GOAL-004 status 保持 `active`、progress 保持 `25%`，与当前仅完成阶段 A 的事实一致。

### 结论

**阶段 A 数据模型设计审计通过，A-001 意见已闭环。** 本次设计审计结论状态为 `final`，仅表示阶段 A 设计可作为实现依据，不代表 GOAL-004 已关单。下一步进入阶段 B 读取路径实现。
