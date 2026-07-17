---
title: AGENTS 模板 · 目标治理 AI 规则
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
---

# AGENTS.md

> **使用说明**：将本文件复制到目标仓库根目录并命名为 `AGENTS.md`。  
> 将下方 `{{...}}` 占位符改成项目真实信息后生效。

面向在本仓库工作的 AI 助手（及人类协作者）。**以下规则必须遵守。**

## 1. 文档真相来源

- 目标与过程记录以 `docs/goals/` 为准。
- 架构约定以 `docs/architecture/` 为准（若项目启用）。
- 文档使用规范见 `docs/README.md`（若存在）。
- 全局树与状态见 `docs/goals/goal-tree.md`（**必读、必更新**）。

## 2. 目标存储与编号

1. 所有目标**平铺**存放在 `docs/goals/`，**禁止**嵌套目标文件夹。
2. `GOAL-001` 固定为总目标（Root Goal），`parent` 必须为 `null`。
3. 新目标从当前最大编号 +1 分配。
4. 文件夹命名：`GOAL-NNN-short-slug`（数字三位、英文 slug）。
5. 层级**仅**通过各目标 `00-meta.md` 的 `parent` 字段维护（值为父目标完整 ID，或 `null`）。

## 3. 每个目标的必备文件

创建目标时必须一次建齐：

```text
docs/goals/GOAL-NNN-short-slug/
├── 00-meta.md
├── 01-decision.md
├── 02-execution.md
├── 03-audit.md
└── attachments/          # 可为空，但目录必须存在
```

不得省略其中任一文件。可从 Skills 包中的 `templates/goal-folder/` 复制。

## 4. Frontmatter 最低要求

每个 Markdown 文档至少包含：

- `status`
- `created`
- `updated`
- `parent`（非目标文件可用 `null`）
- `version`

目标 `00-meta.md` 必须包含 `id` 与 `title`。修改内容时更新 `updated`。

## 5. 内容写作要求

- **决策（01-decision）**：写清「决定了什么」和「为什么」；重要取舍注明未选方案。
- **执行（02-execution）**：按时间线记录事实；**不虚构**未完成工作。
- **审计（03-audit）**：阶段性复盘：成果、偏差、改进、结论。
- 语言简洁真实；不确定则标注「待确认」，不要编造进度。

## 6. 必须同步更新 goal-tree.md

以下任一操作后，**必须**更新 `docs/goals/goal-tree.md`：

- 新建目标
- 修改目标 `status` / 进度
- 修改 `parent`（调整树）
- 完成或取消目标
- 重命名目标文件夹或 slug（同时修正所有引用）

更新内容至少包括：ASCII/文本树、状态表格。

## 7. 应用代码与文档边界（可选）

> 若项目没有 Web/应用代码，可删除本节或改为实际布局说明。

- 应用代码放在 `{{APP_DIR}}`（示例：`web/`）。
- 不要把目标正文写进 UI 模板当长期存储；长期记录回写 `docs/goals/`。
- 扩展架构时先更新 `docs/architecture/`，再改代码。

## 8. 交付形态（按项目裁剪）

本模板默认支持「文档驱动的目标治理」。可选交付：

1. **文档体系**（必选）：`docs/goals` + `goal-tree.md`
2. **应用**（可选）：可视化浏览/操作
3. **Skills / 提示词**（可选）：AI 按同一规则读写目标

改规则或目标模型时，评估是否需要同步更新文档、应用与 Skills。

## 9. 变更工作流（建议）

```text
读 goal-tree.md → 确认编号与 parent
→ 创建/修改目标五件套
→ 更新 goal-tree.md
→ 必要时更新 docs/README.md、architecture/、根 README.md
→ 再改应用代码或 Skills
```

## 10. 禁止事项

- 禁止在 `docs/goals/` 下用子文件夹嵌套表达父子目标。
- 禁止跳过 `goal-tree.md` 只改单目标文件就结束任务。
- 禁止伪造已完成的执行条目或审计结论。
- 禁止擅自把 Root Goal 从 GOAL-001 改成其他编号。

## 快速链接（按项目填写）

- docs/README.md：`{{DOCS_README_PATH}}`
- goal-tree.md：`docs/goals/goal-tree.md`
- Root Goal：`docs/goals/{{ROOT_GOAL_FOLDER}}/00-meta.md`
- 架构说明：`{{ARCHITECTURE_PATH}}`
