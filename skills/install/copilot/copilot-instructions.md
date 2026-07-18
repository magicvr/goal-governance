---
title: Copilot Instructions · 目标治理 AI 规则（GitHub Copilot）
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.3.3
---

# GitHub Copilot 项目指令 · 目标治理

> **适用工具**：GitHub Copilot（VS Code / GitHub）  
> 将本文件放在目标项目的 `.github/copilot-instructions.md`。  
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

- **目标真相源**：长期过程记录在 `docs/goals/`，不要把目标正文只写进业务代码或 UI 当唯一真相。
- **代码布局不统一**：普遍形态是代码在**仓库根**（或该语言惯例分布）；子目录仅为部分项目约定。禁止照搬示例仓库的 `web/`。
- **刚装本包、文件很少时**：不得先验判定「非代码项目」或规定代码目录——由用户决定。
- **语言**：标题/正文跟随用户；slug 建议英文短横线。
- architecture 目录**可选**；未启用则不要擅自创建。

## 8b. Skills 包路径

- 包目录常见名 `skills/`，也可改名。以含 `prompts/00-govern-orchestrator.md` 的目录为准，**禁止**写死必须为 `./skills`。

## 9. 交付形态（按项目裁剪）

默认：**文档驱动的目标治理**（可叠加任意布局的代码库）。**不**默认必须有 Web 应用。

1. **文档体系**：`docs/goals/` + `goal-tree.md`
2. **产品/代码（常见）**：仓库根或项目实际目录
3. **Skills 包（可选）**：上节定位的包目录

## 10. 变更工作流

```text
1. 读 goal-tree.md → 确认最大编号与 parent
2. 若尚不可直接执行 → 先写/更新高层路线图（00-meta 或 01-decision）
3. 创建或修改目标五件套（frontmatter + 正文）
4. 更新 goal-tree.md（树 + 表）
5. 仅当项目已有对应文件时更新 docs/README、architecture 等（不强制新建）
6. 再改代码或 Skills（路径以项目实际为准）
```

步骤 **1–4 强制**；5–6 按影响面执行。

## 11. 禁止事项

- 在 `docs/goals/` 下用子文件夹嵌套表达父子目标
- 跳过 `goal-tree.md` 只改单目标文件就结束
- 伪造已完成的执行条目或审计结论
- 擅自把 Root 从 `GOAL-001` 改成其他编号
- 对明显需拆解的大目标跳过路线图，直接批量创建并执行细粒度子目标
- 用 `parent` 以外的方式（目录、标题、正文）作为层级真相
- 新建目标时漏五件套任一文件或目录
- 把「应用代码只能在 `web/` 等子目录」当成未约定项目的通用规则
- 仅因刚装本包、仓库文件少，就先验断定「非代码项目」
- 写死 skills 包必须为 `./skills`；因缺 architecture 拒绝工作；强加示例 Root slug

## 12. 完成前检查清单

每次涉及目标的任务结束前自检：

- [ ] 编号未冲突；`id` = 文件夹名
- [ ] `parent` 为完整父 id 或 `null`（Root）
- [ ] 五件套齐全（若新建）
- [ ] 大目标已写/更新路线图（若适用 P-001）
- [ ] `goal-tree.md` 树与表已同步
- [ ] `updated` / `progress` / `status` 与事实一致
- [ ] 无虚构进度或审计结论

## 常见错误（避免）

| 错误 | 正确做法 |
|------|----------|
| 用 `docs/goals/父/子/` 建层级 | 平铺 + `parent` 字段 |
| `parent: GOAL-001`（缺 slug） | `parent: GOAL-001-<实际 slug>`（完整 id） |
| 只改 `00-meta` 进度，不改 goal-tree | 两处一起改 |
| 大目标一次创建十几个子目标 | 先路线图，再按阶段立项 |
| 把计划写成「已完成」 | 只记已发生事实；计划单独标注 |
| 复制模板后仍留示例 id（如 GOAL-042） | 改成真实 id / 标题 / parent |

## Skills 主入口（若已安装本包）

- **默认（且通常是唯一 slash）**：**`/govern`** → 定位 **SKILLS_PKG**（含 `prompts/00-govern-orchestrator.md` 的目录，名可能不是 `skills`）后执行编排器。
- **原语正文**：`<SKILLS_PKG>/prompts/01`～`04` 由编排器调用；**默认安装不会**装四个填表 slash。
- 若曾用 `--with-primitives` 安装 advanced slash，仍应优先 `/govern`。
- 生命周期：设立目标 → 推进目标 → 阶段性/关门审计。
- P-001 以本文件第 6 节为准；architecture 可选。

## GitHub Copilot 使用提示

- 本文件路径固定为 `.github/copilot-instructions.md`，供 GitHub Copilot 读取项目级指令。
- 若仓库根另有 `AGENTS.md`（例如同时给 Claude Code 用），两边规则应保持一致。
- 日常目标协作使用 **`/govern`**；需要原子写入时由编排器调用 01～04。
- 在 VS Code 中修改本文件后，新对话/Agent 会话会采用更新后的指令。

## 快速链接（按项目填写）

- 目标树：`docs/goals/goal-tree.md`
- Root Goal：`docs/goals/GOAL-001-<your-slug>/00-meta.md`
- 治理原则：本文件第 6 节；`docs/architecture/principles.md`（若存在）
