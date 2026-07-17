---
title: AGENTS · AI 助手强制规则
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
---

# AGENTS.md

面向在本仓库工作的 AI 助手（及人类协作者）。**以下规则必须遵守。**

## 1. 文档真相来源

- 目标与过程记录以 `docs/goals/` 为准。
- 架构约定以 `docs/architecture/` 为准。
- 文档使用规范见 `docs/README.md`。
- 全局树与状态见 `docs/goals/goal-tree.md`（**必读、必更新**）。

## 2. 目标存储与编号

1. 所有目标**平铺**存放在 `docs/goals/`，**禁止**嵌套目标文件夹。
2. `GOAL-001` 固定为总目标（Root Goal），`parent` 必须为 `null`。
3. 新目标从当前最大编号 +1 分配（现有：001、002 → 下一个为 **003**）。
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

不得省略其中任一文件。

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

## 7. Web 与文档边界

- 应用代码只在 `web/`。
- 不要把目标正文写进模板里当长期存储；长期记录回写 `docs/goals/`。
- 当前 Web 为骨架（FastAPI + Jinja2 + Tailwind + HTMX），扩展时先更新 `docs/architecture/` 再改代码。

## 8. 双交付意识

本项目交付两类能力：

1. **Web 应用**（`web/`）
2. **Skills / 提示词**（协作规范、后续 Skill 包）

改规则或目标模型时，评估是否两边都需要同步说明。

## 9. 变更工作流（建议）

```text
读 goal-tree.md → 确认编号与 parent
→ 创建/修改目标五件套
→ 更新 goal-tree.md
→ 必要时更新 docs/README.md、architecture/、根 README.md
→ 再改 web/ 或 Skills
```

## 10. 禁止事项

- 禁止在 `docs/goals/` 下用子文件夹嵌套表达父子目标。
- 禁止跳过 `goal-tree.md` 只改单目标文件就结束任务。
- 禁止伪造已完成的执行条目或审计结论。
- 禁止擅自把 Root Goal 从 GOAL-001 改成其他编号。

## 快速链接

- [docs/README.md](docs/README.md)
- [docs/goals/goal-tree.md](docs/goals/goal-tree.md)
- [GOAL-001-main-vision](docs/goals/GOAL-001-main-vision/00-meta.md)
- [docs/architecture/overview.md](docs/architecture/overview.md)
