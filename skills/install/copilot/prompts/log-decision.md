---
title: /log-decision · 记录决策（Copilot wrapper）
description: 引导收集决策参数后，按 skills/prompts/02-record-decision.md 写入 01-decision.md
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
slash: /log-decision
---

<!--
  这是 GitHub Copilot 斜杠命令 wrapper（轻量交互入口）。
  核心提示词在：skills/prompts/02-record-decision.md
  修改核心提示词即可全局生效；本文件只负责引导参数与引用核心。
  用法：复制到项目根 .github/prompts/（建议命名 log-decision.prompt.md），
  在 Copilot Chat 输入 /log-decision 调用。
-->

# /log-decision · 记录决策

你是本仓库的目标治理协作者。请严格遵守项目 AI 规则（根目录 `AGENTS.md`，或已安装的 `.github/copilot-instructions.md`）。

## 第一步：向我收集必要参数

信息缺失或不确定时，**先向我确认，不要猜测后继续**。请确认：

| 参数 | 说明 |
|------|------|
| 目标 ID / 路径 | 如 `GOAL-003-skills-practice` 或 `docs/goals/GOAL-003-skills-practice/` |
| 决策标题 | 一句话 |
| 决定了什么 | 明确结论（必须） |
| 为什么 | 背景、约束、收益（必须） |
| 未选方案 | 可选：列方案 + 简短否决理由 |
| 影响范围 | 可选：影响哪些目标 / 文档 / 代码 |
| 后续动作 | 可选：因此要做什么 |
| 今日日期 | `YYYY-MM-DD` |

用户若已在命令后附带内容，只追问空白项。一条命令可记多条决策，但请分条列清。

## 第二步：按核心提示词执行

参数齐备后，**完整阅读并严格执行**核心提示词：

- 路径：[`./skills/prompts/02-record-decision.md`](../../../prompts/02-record-decision.md)
- 使用其中「提示词正文」的条目格式（`D-NNN`）、强制步骤、禁止项与交付检查清单

## 必须遵守的 AGENTS 要点（摘要）

1. 决策写在目标的 `01-decision.md`：必须写清「决定了什么」和「为什么」  
2. 重要取舍注明未选方案；不确定标「待确认」，不编造共识  
3. 若决策改变范围 / 成功标准 / 路线图：同步 `00-meta.md`，并在 `02-execution.md` 记一句事实  
4. 若 status / progress 变化：**必须**同步 `docs/goals/goal-tree.md`  
5. 不要把执行流水账写进 decision；过程细节放 execution  
6. 遵守扁平存储与五件套约定；不擅自改 Root 编号  

## 完成后

用核心提示词中的交付检查清单自检，并汇报：决策编号、写入路径、是否联动 meta / execution / goal-tree。
