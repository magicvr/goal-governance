---
id: GOAL-004-core-data-model
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-19
version: 0.5.0
---

# 决策记录 · GOAL-004

## D-001 · 承接 GOAL-001 阶段 3，独立立项

**决定**：

将「核心数据模型与 Goal 基础管理」作为 GOAL-001 下独立子目标 GOAL-004 推进，而不是继续塞进 GOAL-002（已 done）或 GOAL-003（Skills 实践）。

**为什么**：

- GOAL-001 高层路线图已将阶段 3 单独列出；独立目标便于进度、决策与审计边界清晰。
- GOAL-003 明确不在范围内包含 Web 数据模型 / CRUD，避免 Skills 与数据层交付混写。
- 本目标跨模型设计与 Web 接入，需按 P-001 先写路线图再按阶段拆解，不宜挂在其他目标下零散开工。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 继续写在 GOAL-003 | 与 Skills 成功标准冲突，范围膨胀 |
| 直接批量创建「模型 / CRUD / 页面」多个子目标后开工 | 违反 P-001；设计未定时拆碎易返工 |
| 跳过本目标、直接改 `web/` | 缺少可追踪的决策与成功标准，易与文档体系约定漂移 |

## D-002 · 短期仍以 `docs/goals` Markdown 为 source of truth

**决定**：

本目标实现期间，**不**引入独立业务数据库作为真相源；Goal 及关联内容的权威存储仍是 `docs/goals/` 下的 Markdown + frontmatter（与 [tech-stack.md](../../architecture/tech-stack.md) 一致）。Web / 服务层从文档读取（并在写路径上按约定写回文件）。

**为什么**：

- 与现有 AGENTS / 文档体系一致，避免「库里一份、文件一份」双源。
- 人与 AI 已按 Markdown 五件套协作；先接通读写比先迁库更能验证模型是否贴合真实结构。
- 后续若需库表或索引，应在模型跑通后再单独立项评估。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 本阶段直接上 Postgres 等 | tech-stack 明确当前未采用；过早迁库增加同步与迁移成本 |
| 仅内存 mock、不接 `docs/goals` | 无法验证成功标准中的「真实目标数据」 |

## D-003 · 细粒度技术选型延后到阶段 A

**决定**：

解析库、目录扫描策略、API 形状、写回是否经服务层校验等**具体实现选型**，在路线图**阶段 A（领域模型与存储约定）**产出设计后再正式记录；立项时不预先锁定。

**为什么**：

- 先定实体与映射，再选库与接口，减少「实现先行、模型后补」。
- 避免在信息不足时编造决策。

**待确认（阶段 A）**：

- ~~实体边界：Goal / Decision / Execution / Audit 如何映射到五件套文件~~ → 见 **D-004**
- ~~列表是否必须读 `goal-tree.md` 或可扫描目录 + meta~~ → 见 **D-005**
- ~~写路径是否同步更新 `goal-tree.md`~~ → 见 **D-006**

## D-004 · 领域实体与五件套映射

**日期**：2026-07-18  
**状态**：accepted

**决定**：

采用「Goal 为聚合根 + 五件套文档为组成部分」的领域模型：

| 实体 | 磁盘映射 |
|------|----------|
| Goal / GoalMeta | `docs/goals/<id>/` + `00-meta.md` |
| DecisionDoc（含可选 DecisionEntry[]） | `01-decision.md` |
| ExecutionDoc（含可选时间线条目） | `02-execution.md` |
| AuditDoc | `03-audit.md` |
| AttachmentRef[] | `attachments/*` |
| GoalTreeIndex | 运行时由扫描（主）+ `goal-tree.md`（辅）构建 |

正文 Markdown 始终是真相；结构化 entry 为**尽力解析**，失败时 UI 回退全文渲染。完整说明见 [attachments/domain-model-and-storage.md](attachments/domain-model-and-storage.md)。

**为什么**：

- 与现有协作习惯一致，避免引入第二套数据形状。
- 列表与校验需要结构化字段（id/status/parent），详情需要全文，分层清晰。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 仅强类型 entry、丢弃非结构化正文 | 破坏人手写文档自由度 |
| 把 decision/execution/audit 拆成多文件多实体表 | 超出阶段范围，与五件套约定冲突 |

**影响**：阶段 B 服务层模型与本映射对齐；阶段 C 写回以文件为单位。

## D-005 · 列表运行时权威为目录扫描，goal-tree 为投影

**日期**：2026-07-18  
**状态**：accepted

**决定**：

- **List / 树构建 / CRUD 读**：以扫描 `docs/goals/GOAL-*/00-meta.md` 为运行时权威。
- **`goal-tree.md`**：辅助总览与漂移检测；与扫描不一致时 UI 以 meta 为准并标记 `tree_drift`。
- **写后**：Create/Update 凡触及 id/title/status/progress/parent 时，**必须**同步更新 goal-tree 的树与表（见 D-006）。

**为什么**：

- tree 可能短暂过期；以磁盘 meta 为准避免「文件有目标但列表空白」。
- 仍落实 AGENTS「变更必更 tree」：写路径强制同步，而不是读路径盲信 tree。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 只读 goal-tree.md 做列表 | 解析脆弱且可能与 meta 漂移 |
| 双源对等合并写回 | 复杂度高，阶段不需要 |

## D-006 · 写路径校验与 goal-tree 同步边界

**日期**：2026-07-18  
**状态**：accepted

**决定**：

1. Goal CRUD：List/Get（B）、Create/Update meta 与 section（C）；**不做**物理删除（取消用 `cancelled`）。
2. 写失败规则：id≠文件夹名、非法 status、parent 不存在或成环 → error。
3. Create 一次建齐五件套 + `attachments/`；编号 = 当前最大 GOAL 号 + 1。
4. 改 status/progress/parent/title 或 Create 后必须更新 `goal-tree.md`（树 + 表 + updated）；同步失败不得静默忽略。
5. 本阶段无乐观锁；文档注明并发覆盖风险。

细节表见设计说明 §6。

**为什么**：把 AGENTS 规则变成服务层可执行契约，避免 Web 写出非法树。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 写业务文件不同步 tree，交给人补 | 与 AGENTS 强制项冲突 |
| 本阶段上物理删除 | 不可逆风险高，cancelled 足够 |

## D-007 · 阶段 B 模块落点与解析依赖方向

**日期**：2026-07-18  
**状态**：accepted

**决定**：

- 服务代码落在 `web/services/`（`models` / `parse_md` / `goals_repo`），由 `main.py` 逐步接入。
- Frontmatter 解析优先采用轻量库（如 `python-frontmatter`）或等价自研；**实现阶段 B 时再写入 requirements**，阶段 A 不锁死包版本。
- 阶段 B 可仅内部 service + SSR，不强制先暴露 JSON API。

**为什么**：贴合现有 `web/` FastAPI 布局；避免阶段 A 过早钉死依赖版本。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 新建独立 Python 包于仓库根 | 当前规模不必要 |
| 阶段 A 即改 requirements 并装库 | 无运行代码时无处 |

## D-008 · 读取结果显式承载无效文档与诊断

**日期**：2026-07-18
**状态**：accepted

**决定**：

- `Goal` 仅表示通过最低结构校验的目标。
- 仓库读取接口使用 `GoalLoadResult` 承载 `goal | null`、来源路径、raw Markdown 与 `ValidationIssue[]`。
- `ValidationIssue` 至少包含稳定错误码、严重度、路径和消息。
- `list_goals` 不静默丢弃无效目录；`get_goal` 明确区分不存在、无效 frontmatter 与五件套部分缺失。

**为什么**：阶段 B 需要既能展示有效目标，又能向用户暴露可修复的文档问题；用半初始化 `Goal` 无法维持类型契约。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 无效目录直接跳过 | UI 会把磁盘中真实存在的问题隐藏掉 |
| 给 `Goal` 所有字段加 `None` | 有效领域对象失去约束，调用方处处判空 |

## D-009 · Goal ID 与文件读取必须受路径边界约束

**日期**：2026-07-18
**状态**：accepted

**决定**：

- 外部输入的 Goal ID 必须匹配 canonical 格式：`^GOAL-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$`。
- 目标与附件路径 `resolve()` 后必须仍位于注入的 `GOALS_DIR` 内。
- 拒绝逃逸 `GOALS_DIR` 的符号链接；调用方不得传入任意相对路径代替 Goal ID。

**为什么**：阶段 D/API 接入后，路径拼接会接触外部输入；在仓库层统一限制比依赖每个路由自行过滤更可靠。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 只依赖 FastAPI 路由参数不含斜杠 | 不能覆盖编码字符、Windows 分隔符、符号链接与内部调用 |
| 只校验目录存在 | 无法证明解析后的路径仍在目标根目录内 |

## D-010 · 树索引必须返回结构化校验报告并稳定排序

**日期**：2026-07-18
**状态**：accepted

**决定**：

- `GoalTreeIndex` 增加 `tree_drift` 与 `TreeValidationReport`。
- 报告至少覆盖：tree 缺项、磁盘缺项、字段不一致、孤儿、环、重复数字编号和通用 issues。
- 列表、树根和同级 children 均按 GOAL 数字编号升序稳定排序；同号异常项再按完整 id 排序。

**为什么**：布尔 drift 只能提示“有问题”，不能支持诊断或测试；文件系统遍历顺序也不应决定 UI 和测试输出。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 只返回 `tree_drift: true` | 无法定位差异和提供修复入口 |
| 保留扫描自然顺序 | 跨平台结果不稳定，测试容易抖动 |

## D-011 · 审计结论采用显式状态而非关键词命中

**日期**：2026-07-18
**状态**：accepted

**决定**：

- `AuditDoc` 使用 `conclusion_state: none | provisional | final | unknown`。
- 仅从明确的结论章节或后续约定的结构化字段推导；自然语言关键词仅可辅助定位，不得直接决定状态。
- 无结论章节返回 `none`；存在章节但无法解析时返回 `unknown`。

**为什么**：诸如“不写『已完成』结论”的否定句会使关键词启发式产生确定误报。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 搜索“结论”或“已完成”并返回布尔值 | 无法理解否定语义，也无法区分阶段结论和最终结论 |

## D-012 · version 是必填字段且读取不得隐式修复

**日期**：2026-07-18
**状态**：accepted

**决定**：

- 按 AGENTS，所有治理 Markdown 的 `version` 均为必填字段。
- 缺失时读取层返回 validation issue；普通 List/Get 不修改磁盘。
- 补齐或升级版本只能由显式维护/写入操作完成。

**为什么**：读取操作应可重复且无副作用，并与项目级 frontmatter 最低要求保持一致。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 读取时自动补 `0.1.0` | GET 产生写副作用，且可能覆盖用户预期版本 |
| 继续把 version 视为建议 | 与 AGENTS 硬约束直接冲突 |

## D-013 · 多文件写回采用可恢复提交而非伪原子承诺

**日期**：2026-07-18
**状态**：accepted

**决定**：

- 阶段 C 写回前先在内存生成并校验所有目标内容与新的 `goal-tree.md`。
- 写入采用同目录临时文件、原文件备份、受控替换和失败补偿；成功后再清理备份。
- 补偿失败时保留 recovery record，并阻止继续普通写入，直到显式恢复或运行 `repair_goal_tree()`。
- `repair_goal_tree()` 以 meta 扫描为权威重建树和表；跨文件系统写入明确为“可恢复提交”，不宣称真正原子事务。

**为什么**：仅在 tree 写失败后返回错误仍会留下不一致状态；普通文件系统无法直接提供跨多个 Markdown 文件的原子事务。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 业务文件先写、tree 失败只记日志 | 违反变更后必须同步 goal-tree 的硬约束 |
| 引入数据库事务 | 当前 Markdown SoT 不变，代价超出本目标范围 |

**影响**：本决策补充 D-006 的写失败规则；D-006 其余 CRUD、校验与不物理删除约定继续有效。

## D-014 · 阶段 C 以仓库服务命令承载写入与恢复

**日期**：2026-07-19
**状态**：accepted

**决定**：

- `GoalsRepository` 在阶段 C 提供 `create_goal`、`update_goal` 和 `repair_goal_tree()`；Web 路由仍留待阶段 D 接入。
- Create 接收标题、slug、parent、状态、进度和各文档正文，生成完整五件套；Update 以字段和各 section 的**整段正文替换**为最小写入粒度，保留未改 section 与未知 frontmatter 键。
- Create 或变更 title/status/progress/parent 的 Update 在内存中重建并校验 `goal-tree.md`；普通 section-only Update 不重写 tree。
- 变更 Goal 的 `status` 或 `parent` 时，同一事务同步三个 section 文件的对应 frontmatter 和 `updated`，避免五件套保留过期的目标元数据。
- 多文件提交失败且补偿也失败时，服务在 `docs/goals/.goal-write-recovery.json` 保留恢复记录并拒绝后续普通写入；`repair_goal_tree()` 先恢复已知备份，再以 meta 扫描重建 tree。

**为什么**：

- 服务命令让阶段 D 可以复用同一套校验、同步和恢复边界，而不会把文件系统细节散落到路由中。
- Markdown 正文没有稳定的细粒度语法树；整段替换的语义明确，能够保护未修改的文档和未知 frontmatter 字段。
- 恢复记录把“无法确认补偿是否完成”的状态显式化，避免后续写入在半提交状态上继续扩大偏差。

**未选方案**：

| 方案 | 未选原因 |
|------|----------|
| 阶段 C 直接暴露 POST/PATCH 路由 | 页面和 API 形状属于阶段 D，当前会扩大调试面 |
| 用字符串局部替换 YAML/Markdown 行 | 难以可靠保留未知字段和任意正文结构 |
| tree 写失败后仅报错或写日志 | 不能恢复跨文件一致性，违反 D-013 |

**影响**：阶段 C 的测试必须覆盖 Create、Update、tree 同步、树替换失败后的补偿、补偿失败后的阻断，以及 `repair_goal_tree()`。
