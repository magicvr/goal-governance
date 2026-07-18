---
id: GOAL-004-core-data-model
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.2.0
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
