---
title: /new-goal · 创建新目标（Copilot wrapper）
description: 引导收集参数后，按 skills/prompts/01-create-new-goal.md 创建目标五件套并同步 goal-tree
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
slash: /new-goal
---

<!--
  这是 GitHub Copilot 斜杠命令 wrapper（轻量交互入口）。
  核心提示词在：skills/prompts/01-create-new-goal.md
  修改核心提示词即可全局生效；本文件只负责引导参数与引用核心。
  用法：复制到项目根 .github/prompts/（建议命名 new-goal.prompt.md），
  在 Copilot Chat 输入 /new-goal 调用。
-->

# /new-goal · 创建新目标

你是本仓库的目标治理协作者。请严格遵守项目 AI 规则（根目录 `AGENTS.md`，或已安装的 `.github/copilot-instructions.md`），以及 `docs/architecture/principles.md`（尤其 **P-001**：大目标先写高层路线图，禁止直接批量拆细粒度子目标）。

## 第一步：向我收集必要参数

信息缺失或不确定时，**先逐项向我确认，不要猜测后继续**。请确认：

| 参数 | 说明 |
|------|------|
| 目标标题 | 中文一句话标题 |
| 英文短 slug | 小写、短横线，如 `skills-practice` |
| 父目标 ID | 完整 id（含 slug），如 `GOAL-001-main-vision`；Root 写 `null` |
| 一句话概述 | 这个目标要解决什么 |
| 成功标准 | 2～5 条可验证勾选项 |
| 是否需拆解 | 是 / 否；若「是」本回合只写路线图，不批量建子目标 |
| 初始状态 | `draft` 或 `active`（默认 `draft`） |
| 今日日期 | `YYYY-MM-DD` |

用户若在斜杠命令后已附带部分信息，只追问空白项。

## 第二步：按核心提示词执行

参数齐备后，**完整阅读并严格执行**核心提示词：

- 路径：[`./skills/prompts/01-create-new-goal.md`](../../../prompts/01-create-new-goal.md)
- 使用其中「提示词正文」的强制步骤、禁止项与交付检查清单
- 可参考 `./skills/templates/goal-folder/` 的字段与结构

## 必须遵守的 AGENTS 要点（摘要）

1. 目标平铺在 `docs/goals/`，**禁止**用子文件夹表达父子关系  
2. 一次建齐五件套：`00-meta` / `01-decision` / `02-execution` / `03-audit` / `attachments/`  
3. `parent` 填父目标**完整 id**（或 Root 的 `null`）；`id` = 文件夹名  
4. **必须**同步更新 `docs/goals/goal-tree.md`（ASCII 树 + 状态表）  
5. 只记真实事实，不编造进度或审计结论  
6. 编号：先读 goal-tree，新编号 = 最大编号 + 1；`GOAL-001` 永久为 Root  

## 完成后

用核心提示词中的交付检查清单自检，并简短汇报：编号、路径、parent、goal-tree 是否已更新。
