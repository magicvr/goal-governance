---
title: 领域模型与存储约定（GOAL-004 阶段 A）
status: active
created: 2026-07-18
updated: 2026-07-18
parent: GOAL-004-core-data-model
version: 0.1.0
---

# 领域模型与存储约定

> **目标**：GOAL-004 阶段 A 产出。  
> **约束**：`docs/goals` Markdown + frontmatter 为唯一 source of truth（D-002）；Web/服务层读写文件，不引入业务库。  
> **状态**：accepted（2026-07-18，见 GOAL-004 `01-decision` D-004～D-007）

---

## 1. 设计目标

1. 让 Web/服务层用稳定的**领域对象**表达目标治理实体，而不是散落的路径字符串。
2. 映射必须与 AGENTS / `docs/README` 一致：平铺文件夹、`parent` 完整 id、五件套、`goal-tree.md` 同步。
3. 阶段 B（只读）与阶段 C（写回）共用同一模型；写路径校验边界一次说清，避免实现时再扯皮。

---

## 2. 实体一览

```text
GoalTreeIndex          ← 列表/总览投影（可从 goal-tree 或扫描重建）
Goal                   ← 一个目标文件夹
  ├── GoalMeta         ← 00-meta 的结构化字段 + 正文摘要
  ├── DecisionDoc      ← 01-decision 全文 + 解析出的 DecisionEntry[]
  ├── ExecutionDoc     ← 02-execution 全文 + ExecutionEntry[]（可选解析）
  └── AuditDoc         ← 03-audit 全文 + 阶段结论摘要（可选）
AttachmentRef[]        ← attachments/ 下文件引用（路径 + 名称）
```

### 2.1 Goal（聚合根）

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `id` | string | `00-meta` frontmatter `id` | 与文件夹名完全一致，如 `GOAL-004-core-data-model` |
| `folder_name` | string | 目录名 | 必须等于 `id` |
| `path` | Path | 扫描 | `docs/goals/<id>/` |
| `title` | string | meta `title` | 展示标题 |
| `status` | enum | meta `status` | `draft \| active \| blocked \| done \| cancelled` |
| `parent_id` | string \| null | meta `parent` | Root 为 `null`；否则为**完整父 id** |
| `progress` | string \| null | meta `progress` | 如 `0%`、`50%`；允许缺失 |
| `created` | date | meta | `YYYY-MM-DD` |
| `updated` | date | meta | `YYYY-MM-DD` |
| `version` | string | meta | 文档版本 |
| `summary` | string | meta 正文「概述」等 | 解析启发式；失败时用正文前 N 字或空 |
| `success_criteria` | list[str] | meta 正文 | 可选解析；展示可回退到全文 Markdown |
| `roadmap_present` | bool | meta/decision | 是否含路线图表（启发式，非硬失败） |

**文件夹布局（硬约束）**：

```text
docs/goals/<id>/
├── 00-meta.md
├── 01-decision.md
├── 02-execution.md
├── 03-audit.md
└── attachments/          # 目录必须存在，可为空
```

### 2.2 GoalMeta

与 `00-meta.md` 一一对应：frontmatter 结构化字段 + `body_markdown`（frontmatter 之后的全文）。  
**列表/树视图**优先用 frontmatter；**详情页**默认渲染 `body_markdown`。

### 2.3 DecisionDoc / DecisionEntry

| 层级 | 字段 | 说明 |
|------|------|------|
| Doc | `body_markdown` | 全文真相 |
| Doc | `entries: DecisionEntry[]` | **尽力解析**，解析失败不阻塞展示全文 |
| Entry | `id` | 如 `D-001` |
| Entry | `title` | 标题行文本 |
| Entry | `status` | 可选：`accepted \| proposed \| superseded`（文中有则取） |
| Entry | `decided` / `rationale` / `rejected` | 从「决定 / 理由 / 未选」等标题段抽取；抽不出则整段保留在 `raw_markdown` |

**解析约定（阶段 B 最低要求）**：

- 识别 `## D-NNN` 或 `### D-NNN` 标题块为一条 entry。
- 块内子标题不强制；UI 可对 entry 仅展示标题 + 折叠全文。

### 2.4 ExecutionDoc / ExecutionEntry

| 层级 | 字段 | 说明 |
|------|------|------|
| Doc | `body_markdown` | 全文真相 |
| Entry | `date` | 时间线 `### YYYY-MM-DD · …` |
| Entry | `title` | 短标题 |
| Entry | `raw_markdown` | 该时间线段正文 |

列表页不需要 entry；详情页「执行」Tab 可按时间线分段或整页渲染。

### 2.5 AuditDoc

| 字段 | 说明 |
|------|------|
| `body_markdown` | 全文真相 |
| `has_conclusion` | 启发式：是否含「结论」「已完成」等（仅 UI 提示，不作业务关单） |

**关单权威**仍是 Goal.`status`，不是 audit 正文措辞。

### 2.6 AttachmentRef

| 字段 | 说明 |
|------|------|
| `name` | 文件名 |
| `relative_path` | 相对目标文件夹，如 `attachments/domain-model-and-storage.md` |
| `media_type` | 可选，按扩展名猜测 |

阶段 A/B：**只列文件，不强制解析附件内容**。

### 2.7 GoalTreeIndex（列表投影）

| 字段 | 说明 |
|------|------|
| `nodes: GoalTreeNode[]` | 扁平列表 + 可选 `children` 树 |
| `generated_at` | 构建时间（运行时） |
| `source` | `goal_tree_md` \| `directory_scan` \| `merged`（见 §3） |

**GoalTreeNode**：

| 字段 | 说明 |
|------|------|
| `id`, `title`, `parent_id`, `status`, `progress` | 与 meta / 表列对齐 |
| `depth` | 由 parent 链计算；Root=0 |
| `path` | 文件夹相对 `docs/goals/` |

---

## 3. 列表数据源策略

**决策（D-005）**：

| 路径 | 用途 | 权威性 |
|------|------|--------|
| **主**：扫描 `docs/goals/GOAL-*/00-meta.md` | 列表、详情、CRUD 读写 | **运行时权威**（与磁盘一致） |
| **辅**：解析 `goal-tree.md` 状态表 | 快速总览、检测漂移 | **投影**；不得单独作为写后唯一真相 |
| **校验**：对比扫描结果 vs goal-tree 表 | 管理/诊断 | 不一致时：以 **meta 扫描为准** 展示，并暴露 `tree_drift: true` |

**理由**：

- AGENTS 要求变更后同步 goal-tree，但文件可能暂时不同步；UI 不能因 tree 过期而读不到真实 meta。
- `goal-tree.md` 的 ASCII 树与表格可能手工编辑；解析脆弱，适合辅助而非唯一源。

**实现提示（阶段 B）**：

1. `list_goals()` → 扫描目录 + 读各 `00-meta` frontmatter。  
2. `build_tree(goals)` → 按 `parent_id` 组树；检测环与孤儿。  
3. `load_goal_tree_file()` → 可选加载表格行；与扫描 diff。  
4. 首页默认展示 **扫描树**；若有 drift，页面提示「goal-tree 与磁盘不一致」。

---

## 4. 路径与仓库根约定

| 常量 | 默认 | 说明 |
|------|------|------|
| `REPO_ROOT` | `web/` 的父目录 | `Path(__file__).resolve().parent.parent` |
| `GOALS_DIR` | `{REPO_ROOT}/docs/goals` | 可配置覆盖（env / settings） |
| `GOAL_TREE_FILE` | `{GOALS_DIR}/goal-tree.md` | |

服务层**禁止**写死本机绝对路径；测试可用临时目录注入 `GOALS_DIR`。

---

## 5. Frontmatter 读写约定

### 5.1 解析

- 使用常见 Markdown frontmatter 解析（如 `python-frontmatter` 或等价实现）。
- 缺失 `---` 块：该文件视为 **invalid**；详情可展示 raw 文本，列表可标红并跳过结构化字段。
- 未知 frontmatter 键：**保留**在 `extra: dict`，读写往返不丢键。

### 5.2 必填（Goal meta）

| 键 | 必填 | 备注 |
|----|------|------|
| `id` | 是 | = 文件夹名 |
| `title` | 是 | |
| `status` | 是 | 枚举见上 |
| `parent` | 是 | YAML `null` 或完整 id 字符串 |
| `created` / `updated` | 是 | 日期 |
| `version` | 建议 | 缺省时写回补 `0.1.0`（待实现时定） |
| `progress` | 否 | |

### 5.3 非 meta 文件

`01`/`02`/`03` 建议含 `doc: decision|execution|audit` 与 `id`（目标 id）；缺省不阻断读取。

### 5.4 正文往返

- **读**：`body_markdown` 保留原文换行与标题。  
- **写**：只改约定字段时，应 **保留** 用户手写的 frontmatter 未知键与正文结构；禁止「整文件模板覆盖」除非 API 明确为 replace。

---

## 6. 写路径约定（阶段 C 预置，阶段 B 只读可不实现）

### 6.1 操作集合（Goal 基础 CRUD）

| 操作 | 行为 | goal-tree |
|------|------|-----------|
| **List** | 扫描 meta | 不写 |
| **Get** | 读五件套 + attachments 列表 | 不写 |
| **Create** | 新建 `GOAL-NNN-slug/` 五件套（编号=最大+1） | **必须**更新树+表 |
| **Update meta** | 改 status/progress/title/parent/正文 | status/progress/parent/title 变则 **必须**同步 tree |
| **Update section** | 改 01/02/03 正文或追加块 | 一般不同步 tree；若同时改 progress/status 则同步 |
| **Delete** | **本阶段不做**物理删除 | —；取消用 `status: cancelled` |

### 6.2 编号规则

- Root 固定 `GOAL-001`，禁止改号。  
- 新 id = 现有 `GOAL-(\d+)` 最大数字 + 1，三位补零 + `-` + slug。  
- slug：小写英文、数字、短横线；服务端校验。

### 6.3 校验边界（写失败应明确错误）

| 规则 | 级别 |
|------|------|
| `id` ≠ 文件夹名 | error |
| `parent` 指向不存在的 id | error（Root 除外） |
| `parent` 形成环 | error |
| status 非法枚举 | error |
| 缺五件套文件/attachments 目录 | create 时自动建齐；update 读时 warning |
| 并发写同一文件 | 本阶段不乐观锁；后写覆盖；文档注明风险 |
| 写 goal-tree 失败 | **error**：事务语义上「业务写成功但 tree 失败」应回滚或重试策略见实现；最低要求：返回错误且日志记录，避免静默不同步 |

### 6.4 goal-tree.md 同步内容

更新至少包括：

1. ASCII/文本树（缩进反映 parent）  
2. 状态表格（ID / 标题 / Parent / Status / Progress / 路径）  
3. frontmatter `updated` 日期  

**不**要求重写文件中与树无关的说明段落以外的自定义注释时保持最佳努力（解析-改表-写回）；若解析失败，阶段 C 可降级为「仅更新表格区域」或返回需人工修复。

### 6.5 与 AGENTS 对齐

服务端写路径是 AGENTS「变更后必须更新 goal-tree」的**机械化落实**；AI 与人手写仍须遵守同一规则。Web 不得绕过校验写入非法 parent/status。

---

## 7. 服务层模块建议（阶段 B 起）

建议在 `web/` 下（路径可微调，阶段 B 实现时落盘）：

```text
web/
├── main.py                 # 路由（逐步替换占位）
├── services/
│   ├── goals_repo.py       # 扫描、读写文件、tree 同步
│   ├── models.py           # dataclass / Pydantic 模型
│   └── parse_md.py         # frontmatter + 轻量分段
└── ...
```

**依赖建议（实现时再写入 requirements）**：

- 已有：FastAPI / Jinja2 / Uvicorn  
- 新增候选：`python-frontmatter`（或自研极简 frontmatter 解析，避免过重）

**API 形状（预览，非本阶段交付）**：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/goals` | 列表（扫描） |
| GET | `/api/goals/{id}` | 详情（含 sections） |
| POST | `/api/goals` | 创建（阶段 C） |
| PATCH | `/api/goals/{id}` | 更新 meta/正文（阶段 C） |
| GET | `/` | 服务端渲染列表（阶段 D 可先 SSR 不暴露 API） |

阶段 B 可仅内部 service + SSR，不强制先做 JSON API。

---

## 8. 与成功标准映射

| 成功标准 | 本设计如何支撑 | 阶段 |
|----------|----------------|------|
| 数据模型设计 | 本文实体 + 映射 + 校验 | **A（本文件）** |
| Goal CRUD | §6 操作集 + 校验 | C（Create/Update）；B 覆盖 Read/List |
| 首页/详情真实数据 | 扫描 meta + 读五件套 | B 读 + D 接 Web |
| 详情见决策/执行/审计 | Decision/Execution/Audit Doc | B/D |

---

## 9. 明确不做（本目标内）

- 独立数据库 / ORM 迁移  
- 认证、多租户  
- 完整双向「文档编辑器级」冲突合并  
- 物理删除目标文件夹  
- 强制解析所有 decision/execution 子字段到强类型（尽力即可）  
- 阶段 4「高级写回/同步策略」产品化（属 GOAL-001 后续）

---

## 10. 阶段 B 开工检查清单

- [ ] `GOALS_DIR` 可注入；默认指向仓库 `docs/goals`  
- [ ] `list_goals` / `get_goal` 单测：用夹具目录含 1～2 个 GOAL  
- [ ] 非法 frontmatter / 缺文件时的错误与降级行为有测试  
- [ ] （可选）goal-tree 与扫描 diff 返回 drift 标志  
- [ ] 不在 B 实现写回亦可先合入只读服务

---

## 11. 修订记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-07-18 | 0.1.0 | 阶段 A 初版；关闭 D-004～D-007 待确认项 |
