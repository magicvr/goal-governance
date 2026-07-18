---
id: GOAL-004-core-data-model
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-19
version: 0.7.0
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

## A-003 · 阶段 B 读取路径实施事实自审（2026-07-19）

- **source**：self
- **auditor**：Codex
- **类型 / scope**：execution-facts / 阶段 B 读取路径（列表、详情、诊断、树校验与测试）
- **verdict**：pass

### 范围与区间

核对阶段 A §10 检查清单与阶段 B 实际产物：`web/services/`、`web/tests/`、`web/requirements.txt`、`web/README.md`，以及 [02-execution.md](02-execution.md) 2026-07-19 的验证记录。

### 成果（有证据）

- `GoalsRepository` 已提供可注入 `GOALS_DIR` 的 List/Get，并显式返回 `GoalLoadResult` 与稳定 issue code；普通读取无写副作用。
- 路径边界、部分缺失降级、frontmatter/version 校验、结构化树诊断和数字编号稳定排序均有实现及夹具测试。
- 真实仓库扫描成功加载 5/5 个目标、无读取错误或警告；树投影差异被结构化报告，而非静默覆盖 meta。
- 项目虚拟环境运行 7 项单测通过；`compileall` 与 `pip check` 通过。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 完成 Goal 及关联实体的数据模型设计 | 已达成 | 阶段 A + A-001/A-002 |
| 实现 Goal 基础 CRUD | 部分达成 | 阶段 B 已完成 Read/List；Create/Update 属阶段 C |
| Web 首页和详情页展示真实目标数据 | 未开始 | 阶段 D |
| 详情展示决策 / 执行 / 审计基础信息 | 部分准备 | 阶段 B 已解析三类文档；页面接入属阶段 D |

### Findings

#### F-001 · 当前 goal-tree 投影存在 3 个字段差异

- **严重度**：low
- **建议**：recommended
- **描述与证据**：真实扫描报告 GOAL-001/002 的表格标题与 meta 不同，GOAL-001 的表格 progress 与 meta 缺省值不同；读取层已正确返回 `tree_drift: true` 和字段明细。
- **状态**：open；属于文档维护或投影语义澄清，不阻断阶段 B。

#### F-002 · Windows 环境未执行真实符号链接逃逸用例

- **严重度**：low
- **建议**：recommended
- **描述与证据**：containment 逻辑和测试均已存在；当前进程因 Windows `WinError 1314` 无创建符号链接权限而跳过该用例。
- **状态**：open；建议在具备符号链接权限或非 Windows CI 环境复跑。

### 必改项汇总

无开放 required finding。

### 结论与建议下一步

**pass**：阶段 B 合同与主要异常路径均有实现和测试证据，可进入阶段 C。F-001/F-002 为低风险 recommended residual，不阻断推进；下一步按 D-006/D-013 实现 Create/Update、goal-tree 同步与故障恢复测试。

## A-004 · 阶段 C 可恢复写路径实施事实自审（2026-07-19）

- **source**：self
- **auditor**：Codex
- **类型 / scope**：execution-facts / 阶段 C Create、Update、goal-tree 同步与恢复
- **verdict**：pass

### 范围与区间

核对 D-006、D-013、D-014 与阶段 C 产物：`web/services/goals_repo.py`、`web/tests/test_goals_repo.py`、[02-execution.md](02-execution.md) 2026-07-19 阶段 C 记录。

### 成果（有证据）

- Create 生成 canonical 编号、完整五件套和附件目录；Update 支持 meta 与 section 正文，拒绝非法 slug/status/parent、重复编号、环和非单 Root 树。
- Create 与影响 tree 投影的 Update 同步生成 ASCII 树、状态表和 tree 文件 `updated`；section-only Update 不做无关 tree 写入。
- 多文件提交在目标文件和 tree 替换失败时恢复原始内容；补偿失败会保留 recovery record、阻断普通写入，并由 `repair_goal_tree()` 恢复后重建 tree。
- 14 项单测通过，覆盖 Create/Update、Root 规则、五件套、未知 frontmatter 保留、tree 内容、校验失败无写入、目标文件失败、tree 失败、补偿失败和 repair。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 完成 Goal 及关联实体的数据模型设计 | 已达成 | 阶段 A + A-001/A-002 |
| 实现 Goal 基础 CRUD | 已达成 | 阶段 B Read/List + 阶段 C Create/Update |
| Web 首页和详情页展示真实目标数据 | 未开始 | 阶段 D |
| 详情展示决策 / 执行 / 审计基础信息 | 部分准备 | 服务层已读写三类 section；页面接入属阶段 D |

### Findings

#### F-003 · 进程级中断与并发写入尚无端到端验证

- **严重度**：med
- **建议**：recommended
- **描述与证据**：当前协议覆盖受控异常下的备份、补偿和 repair；未模拟进程在替换步骤间被终止，也未实现乐观锁或并发写测试。D-006 已明确本阶段无乐观锁。
- **状态**：open；不阻断阶段 D 的单进程服务接入，后续若引入多进程部署或高可靠要求，应补进程崩溃恢复和并发策略验证。

### 必改项汇总

无开放 required finding。A-003 的 F-001/F-002 和本条 F-003 均为 recommended residual。

### 结论与建议下一步

**pass**：阶段 C 的约定主路径、同步边界和受控失败恢复均有实现与测试证据，可进入阶段 D。下一步接入首页和目标详情页，展示 Goal 与 decision/execution/audit 基础信息；写接口路由仅在页面交互需要时接入。

## A-005 · 阶段 D 真实数据 Web 接入实施事实自审（2026-07-19）

- **source**：self
- **auditor**：Codex
- **类型 / scope**：execution-facts / 阶段 D 首页、目标详情、诊断、兼容路由与验证
- **verdict**：pass

### 范围与区间

核对 D-015 与阶段 D 产物：`web/main.py`、`web/templates/base.html`、`web/templates/index.html`、`web/templates/goal_detail.html`、`web/tests/test_main.py`、`web/README.md`，以及 [02-execution.md](02-execution.md) 的阶段 D 验证记录。

### 成果（有证据）

- 首页经 `GoalsRepository` 读取 `docs/goals/`，展示有效目标、未关门计数、无效文档与 goal-tree 漂移诊断；树诊断覆盖字段差异、缺项、孤儿、环、重复编号和解析问题。
- `/goals/{goal_id}` 对有效 Goal 渲染元数据、成功标准、附件、结构化 Decision / Execution、Audit 原文与结论状态；非法或不存在的 Goal 返回 404。
- 旧模块地址兼容跳转到统一的目标工作台，不再呈现过时的占位页；页面不暴露写入路由或 JSON API。
- 自动化验证运行 20 项通过（1 项 Windows 符号链接权限环境跳过）；`compileall`、`pip check`、`git diff --check` 通过。本地页面两个目标 URL 均返回 200，浏览器在桌面与移动视口下验证布局和三个详情标签切换。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 完成 Goal 及关联实体的数据模型设计 | 已达成 | 阶段 A、D-004～D-013、A-001/A-002 |
| 实现 Goal 的基础 CRUD（创建、读取、更新、列表） | 已达成 | 阶段 B/C、D-006、D-013、D-014、A-003/A-004 |
| Web 应用首页和详情页能展示真实目标数据 | 已达成 | `web/main.py`、`web/templates/index.html`、`web/templates/goal_detail.html`、`web/tests/test_main.py` |
| 实现目标详情页，能看到决策 / 执行 / 审计的基础信息 | 已达成 | `web/templates/goal_detail.html`、阶段 D 浏览器标签切换验证 |

### Findings

本轮未发现新的 required 或 recommended finding。

### 既有 residual

| Finding | 状态 | 说明 |
|---------|------|------|
| F-001 | open / recommended | 当前 `goal-tree.md` 仍有 3 个既有投影字段差异；阶段 D 已将其明确展示，不静默覆盖。 |
| F-002 | open / recommended | 当前 Windows 进程没有创建符号链接权限，真实逃逸用例仍需在具备权限的环境复跑。 |
| F-003 | open / recommended | 受控异常补偿已测试；进程中断与并发写入仍未端到端验证。 |

### 必改项汇总

无开放 required finding。

### 结论与建议下一步

**pass**：阶段 D 的实现与验证证据满足本目标全部成功标准，可进入 GOAL-004 关门审计。此条仅确认实施阶段完成；目标保持 `active / 100%`，等待用户确认关门后才可改为 `done`。

## A-006 · GOAL-004 关门独立交叉审计（2026-07-19）

- **source**：independent
- **auditor**：Codex audit skill
- **类型 / scope**：close-out / GOAL-004 整体完成情况；四项成功标准、阶段 A～D 实施事实、既有 residual 与关门条件
- **verdict**：pass

### 范围与区间

独立核对 `00-meta.md` 的范围、成功标准和路线图，`01-decision.md` 的 D-004～D-015，`02-execution.md` 的阶段 A～D 时间线，既有 A-001～A-005 审计意见，以及当前实现与测试：

- `web/services/models.py`、`web/services/parse_md.py`、`web/services/goals_repo.py`
- `web/main.py`、`web/templates/index.html`、`web/templates/goal_detail.html`
- `web/tests/test_goals_repo.py`、`web/tests/test_main.py`
- 当前仓库 `docs/goals/` 扫描与 `goal-tree.md` 投影校验

### 成果（有证据）

- 领域模型与五件套映射已形成设计、决策和阶段 A 整改闭环；读取层提供 `GoalLoadResult`、校验诊断、路径 containment、树校验报告和显式审计结论状态。
- `GoalsRepository` 已覆盖 List/Get/Create/Update；Create/影响树投影的 Update 同步五件套与 `goal-tree.md`，受控写入失败可补偿，补偿失败会阻断后续写入并由 `repair_goal_tree()` 恢复。
- 首页和 `/goals/{goal_id}` 详情路由复用仓库真实读取结果；详情包含 meta、成功标准、附件及 Decision / Execution / Audit 三类基础信息，非法或不存在目标返回 404。
- 独立复跑 `..\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v`：20 项通过，1 项因 Windows 无符号链接创建权限跳过；`compileall`、`pip check`、`git diff --check` 通过。
- 当前仓库扫描加载 5/5 个目标且无读取 issue；树校验复现 3 个既有字段差异，无缺项、孤儿、环或重复编号。该结果与 F-001 的 residual 记录一致。

### 对照成功标准

| 标准 | 独立核验 | 证据 |
|------|----------|------|
| 完成 Goal 及关联实体的数据模型设计 | 已达成 | 阶段 A 设计说明、D-004～D-013、A-001/A-002 |
| 实现 Goal 的基础 CRUD（创建、读取、更新、列表） | 已达成 | `GoalsRepository.list_goals/get_goal/create_goal/update_goal` 与 `test_goals_repo.py` |
| Web 首页和详情页展示真实目标数据 | 已达成 | `web/main.py` 首页/详情路由、`test_main.py` 首页与 404 回归测试 |
| 详情页展示决策 / 执行 / 审计基础信息 | 已达成 | `goal_detail.html` 三个详情面板、`test_goal_detail_renders_decision_execution_and_audit` |

### Findings

本轮未新增 finding，亦未发现开放的 `required` / 必改项。以下既有 residual 经复核仍保持开放，不应在本意见中静默关闭：

| Finding | 状态 | 独立复核 |
|---------|------|----------|
| F-001 | open / recommended | 当前 `goal-tree.md` 与两个目标的标题/进度仍有 3 个字段差异；服务层能报告且 Web 会展示，不影响读取真实性。 |
| F-002 | open / recommended | containment 实现与测试存在，但本 Windows 进程仍无法创建真实符号链接；需在具备权限的 Windows 或非 Windows CI 复跑。 |
| F-003 | open / recommended | 受控替换失败、补偿失败与 repair 有测试；进程中断和并发写入仍无端到端验证，且 D-006 明确本阶段不提供乐观锁。 |

### 必改项汇总

无开放 required finding；P-003 的 required 门禁未被触发。F-001～F-003 均为 recommended residual，可由后续治理或部署可靠性目标继续处理。

### 与既有意见的异同

本意见与 A-003～A-005 的阶段自审结论一致（均为 `pass`），但独立复跑了完整测试和当前仓库树诊断；未发现需要推翻既有完成主张的新证据，也未将既有 recommended residual 误记为已关闭。

### 结论与建议给编排器/用户的下一步

**pass**：GOAL-004 的实施范围和四项成功标准均有可复核证据，当前没有阻断关门的 required finding。建议通过 `/govern` 汇总 A-001～A-006、确认是否接受 F-001～F-003 residual，并由用户决定是否将 `00-meta.md` 与 `goal-tree.md` 的目标状态从 `active` 变更为 `done`；在该用户裁决前，本意见不放行状态变更。

### 声明

本意见为 `source: independent` 的交叉审计，只追加审计台账，不修改目标 `status` / `progress` 或 `goal-tree`；后续响应由 `/govern` 处理。

## A-007 · A-006 关门意见的编排响应（2026-07-19）

- **source**：self
- **auditor**：Codex
- **类型 / scope**：response / A-006 independent close-out、P-004 用户裁决与 F-001～F-003 residual 接受
- **verdict**：pass

### 范围与区间

响应 A-006 的关门建议，并记录用户针对 P-004 的明确裁决。此条是编排响应，**不是**补做的 self close-out 审计。

### 用户裁决与关闭证据

| 项目 | 状态 | 证据 |
|------|------|------|
| A-006 independent close-out | 已采纳 | A-006 `pass`；四项成功标准均有可复核证据，无开放 required finding |
| P-004 self close-out 选择 | 已裁决 | 用户明确选择「跳过 self 关门审计」；取舍记录为 D-016 |
| F-001 | 已接受为 residual，仍 open | 3 个既有 tree 投影字段差异持续在服务层和 Web 诊断中可见 |
| F-002 | 已接受为 residual，仍 open | 当前环境无符号链接创建权限；保留后续具备权限环境复跑要求 |
| F-003 | 已接受为 residual，仍 open | 受控失败恢复已测试；进程中断与并发写入验证留给后续可靠性范围 |
| 目标状态 | 已执行 | `00-meta.md`、三个 section frontmatter 与 `goal-tree.md` 同步为 `done / 100%` |

### Findings

未新增 finding。F-001～F-003 不因本响应而关闭，继续是 `open / recommended` residual。

### 必改项汇总

无开放 required finding。

### 结论与建议下一步

**pass**：用户已完成 P-004 裁决并接受 residual；GOAL-004 依据 A-006 和本响应关门为 `done / 100%`。后续处理 F-001～F-003 时应单独立项或纳入对应的文档维护、CI/环境或可靠性工作，不回溯否定本目标的关门结论。
