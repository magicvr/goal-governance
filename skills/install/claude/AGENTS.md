---
title: AGENTS · 目标治理 AI 规则（Claude Code）
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.3.4
---

# AGENTS.md

> **适用工具**：Claude Code  
> 将本文件放在**目标项目根目录**并命名为 `AGENTS.md`。  
> 按项目实际情况修改路径与可选节；未使用的可选节可删除。

面向在本仓库工作的 AI 助手（及人类协作者）。**以下规则必须遵守。**

## 1. 文档真相来源

| 内容 | 路径 | 要求 |
|------|------|------|
| 目标与过程记录 | `docs/goals/` | 唯一长期存储 |
| 目标树与状态 | `docs/goals/goal-tree.md` | **必读、必更新** |
| 架构约定 | `docs/architecture/` | 若项目启用 |
| 治理原则 | `docs/architecture/principles.md` | 若存在；含 P-001 |
| 文档使用规范 | `docs/README.md` | 若存在 |

冲突时以 `docs/goals/` 与本文件为准。

## 2. 目标存储与编号

1. **扁平存储**：所有目标文件夹平铺在 `docs/goals/`，**禁止**用子文件夹表达父子关系。
2. **Root**：`GOAL-001` 固定为总目标，其 `parent` 必须为 `null`；禁止改号。
3. **编号**：先读 `goal-tree.md`（或扫描 `docs/goals/`），新编号 = 当前最大编号 + 1，三位数字（如 `004`）。
4. **文件夹名**：`GOAL-NNN-short-slug`（`NNN` 三位；slug 小写英文、短横线）。
5. **`id` = 文件夹名**：`00-meta.md` 的 `id` 必须与文件夹名完全一致（如 `GOAL-004-foo-bar`）。
6. **层级唯一来源**：仅通过各目标 `00-meta.md` 的 `parent` 字段维护。
   - 值为**父目标完整 id**（含 slug，例：`GOAL-001-your-root-slug`），Root 为 `null`。
   - Root 的 slug **由项目自定**，勿照搬其他仓库示例名。
   - **禁止**用目录嵌套、文件名或正文标题充当层级真相。

## 3. 目标五件套（创建时一次建齐）

```text
docs/goals/GOAL-NNN-short-slug/
├── 00-meta.md
├── 01-decision.md
├── 02-execution.md
├── 03-audit.md
└── attachments/          # 可为空，目录必须存在
```

- 不得省略任一文件或目录。
- 可从 skills 包内 `templates/goal-folder/` 复制后改写（包目录名可能不是 `skills`）。

## 4. Frontmatter 最低要求

每个 Markdown 至少包含：

| 字段 | 说明 |
|------|------|
| `status` | 见下表 |
| `created` | `YYYY-MM-DD` |
| `updated` | 修改内容时更新为当日 |
| `parent` | 目标：父目标完整 id 或 `null`；非目标文件可用 `null` |
| `version` | 文档版本号 |

`00-meta.md` **必须**另含：`id`、`title`；**建议**含 `progress`（如 `50%`）。

### status 取值

| 值 | 含义 |
|----|------|
| `draft` | 草稿，未正式启动 |
| `active` | 进行中 |
| `blocked` | 阻塞 |
| `done` | 已完成 |
| `cancelled` | 已取消 |

## 5. 内容写作要求

| 文件 | 写什么 | 禁止 |
|------|--------|------|
| `01-decision` | 决定了什么 + 为什么；重要取舍写未选方案 | 编造未发生的决策 |
| `02-execution` | 按时间线记**事实**（做了什么、产物路径、进度评估） | 虚构未完成工作 |
| `03-audit` | 阶段性：成果 / 偏差 / 改进 / 结论 | 无复盘节点时硬写「已完成」 |

不确定标注「待确认」。语言简洁真实。

## 6. 目标可执行性与路线图（P-001）

**判定**：范围大、步骤不明、或明显需要拆成多个可独立交付的子目标 → 视为「尚不可直接执行」。

**强制顺序**：

1. **禁止**在尚不可直接执行时，直接批量创建细粒度子目标并开工。
2. **必须先**写可追踪的高层路线图：主要阶段 + 先后关系（可含完成标记）。
3. 路线图写在该目标的 `00-meta.md` 或 `01-decision.md`，并随进展更新。
4. 路线图就位后，再**按阶段**创建与执行具体子目标。
5. 已可直接执行的小目标**无需**强行补路线图。

原则以本文件第 6 节为准；`docs/architecture/principles.md` 若存在可作补充，**不要求**必有 architecture。

## 7. 必须同步更新 goal-tree.md

以下任一操作后，**必须**更新 `docs/goals/goal-tree.md`：

- 新建目标
- 修改 `status` / `progress`
- 修改 `parent`（调整树）
- 完成或取消目标
- 重命名文件夹或 slug（并修正所有引用）

更新内容至少包括：**ASCII/文本树** + **状态表格**。  
只改单目标文件、不更新 goal-tree → **视为任务未完成**。

## 8. 代码与文档边界

- **目标真相源**：长期过程记录在 `docs/goals/`（本包约定）。业务代码与 UI 可以引用目标，长期存储以 `docs/goals/` 为准。
- **代码布局（默认策略）**：
  - 默认：应用/库代码可在**仓库根**，或按该语言/生态惯例分布。
  - 若项目已约定子目录（如 `web/`、`app/`、`services/`）：按该约定；`{{APP_DIR}}` 仅在有约定时填写。
  - 刚装本包、文件很少时：项目性质与代码路径标为待确认，**问用户**或读已有 README/架构；目录观察只作参考。
- **语言与日期**：标题/正文跟随用户语言；slug 建议小写英文短横线；日期用会话/系统 `YYYY-MM-DD`。
- **architecture**：已有则改架构先更新文档；没有则按用户要求再考虑是否建立。

## 8b. Skills 包路径

- 常见目录名 `skills/`，也可改名。
- **定位 SKILLS_PKG**：含 `prompts/00-govern-orchestrator.md`（或 `prompts/01-create-new-goal.md`）的目录。原语与模板相对该根。
- `{{SKILLS_DIR}}` = 包根相对仓库根的路径。

## 9. 交付形态（按项目裁剪）

默认：**文档驱动的目标治理**；代码与可视化应用按项目实际叠加。

1. **文档体系（本包约定）**：`docs/goals/` + `goal-tree.md`
2. **产品/代码（常见）**：仓库根或项目实际目录
3. **独立可视化应用（可选）**：有则按项目路径
4. **Skills 包（可选）**：`{{SKILLS_DIR}}`

## 9b. Skills 主入口（若已安装本包）

- **默认路径**：`{{SKILLS_DIR}}/prompts/00-govern-orchestrator.md`（Copilot 若已装：`/govern`）。
- 编排器：扫描 → 分类 → 提议 → 确认 → 调用原语 `01`～`04`。
- advanced slash 可选（`--with-primitives`）。
- **P-001** 以本文件第 6 节为准；有 architecture 原则文档时一并参考即可。

## 10. 变更工作流

```text
1. 读 goal-tree.md → 编号、parent、未关门目标
2. 未指定原子操作时 → 优先编排器
3. 尚不可直接执行 → 先高层路线图
4. 创建或修改五件套
5. 更新 goal-tree.md（树 + 表）
6. 项目已有 docs/README、architecture 等时再按需更新
7. 再改代码或 Skills（路径以项目实际为准）
```

步骤 **1、3–5 强制**；编排优先；6–7 按影响面。

## 11. 正确做法与硬约束

**正确做法**

- 层级：平铺文件夹 + `parent` 完整 id。
- 改 status/progress/parent/新建：同步 goal-tree 树与表。
- 大目标：先路线图，再按阶段建子目标。
- 执行/审计：只写有证据的事实；计划单独标注。
- 代码布局与 Root slug：默认见第 8 节；以用户/项目约定为准（`web/` 等为可选约定示例）。
- Skills 包：按内容定位 SKILLS_PKG。
- P-001：本文件第 6 节足够；architecture 可选。

**硬约束**

- Root 编号保持 `GOAL-001`；`parent: null`。
- 新建一次建齐五件套。
- 决策、执行、审计只记录真实内容。

## 12. 完成前检查清单

- [ ] 编号未冲突；`id` = 文件夹名
- [ ] `parent` 为完整父 id 或 `null`
- [ ] 五件套齐全（若新建）
- [ ] 大目标路线图已写/更新（若适用）
- [ ] `goal-tree.md` 已同步
- [ ] `updated` / `progress` / `status` 与事实一致

## 写法对照（简表）

| 推荐 | 说明 |
|------|------|
| 平铺 + `parent: GOAL-001-<slug>` | 完整 id |
| 改 progress 同时改 goal-tree | 两处一致 |
| 大目标先路线图 | 再按阶段立项 |
| 计划与已完成分开写 | 时间线只记事实 |
| 复制模板后改真实 id | 例如勿留 GOAL-042 |
| 按 prompts 文件定位包目录 | 包名可以是 `skills` 或其他 |


## Claude Code 使用提示

- 本文件为 Claude Code 的项目级规则入口；保持在仓库根目录、文件名 `AGENTS.md`。
- 日常目标协作优先编排器（§9b）；原子写入再走 01～04。
- 改规则后无需额外注册；下次会话即按本文件执行。

## 快速链接（按项目填写）

- 目标树：`docs/goals/goal-tree.md`
- Root Goal：`docs/goals/GOAL-001-<your-slug>/00-meta.md`
- 治理原则：AGENTS 第 6 节；`docs/architecture/principles.md`（若存在）
