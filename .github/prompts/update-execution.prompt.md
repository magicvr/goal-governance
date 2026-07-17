---
title: /update-execution · 更新执行进度（Copilot wrapper）
description: 引导收集今日事实后，按 skills/prompts/03-update-execution.md 更新 02-execution 与进度
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
slash: /update-execution
---

<!--
  这是 GitHub Copilot 斜杠命令 wrapper（轻量交互入口）。
  核心提示词在：skills/prompts/03-update-execution.md
  修改核心提示词即可全局生效；本文件只负责引导参数与引用核心。
  用法：复制到项目根 .github/prompts/（建议命名 update-execution.prompt.md），
  在 Copilot Chat 输入 /update-execution 调用。
-->

# /update-execution · 更新执行进度

你是本仓库的目标治理协作者。请严格遵守项目 AI 规则（根目录 `AGENTS.md`，或已安装的 `.github/copilot-instructions.md`）。

## 第一步：向我收集必要参数

信息缺失或不确定时，**先向我确认，不要猜测后继续**。请确认：

| 参数 | 说明 |
|------|------|
| 目标 ID / 路径 | 如 `GOAL-003-skills-practice` |
| 今日日期 | `YYYY-MM-DD` |
| 本次实际完成的工作 | 条目列表，尽量带路径/产物名（必须是事实） |
| 阻塞 / 风险 | 有则写，无则「无」 |
| 下一步计划 | 可选；须标明为计划而非已完成 |
| 进度百分比 | 保持 / 调整为 N%（若调整须给依据） |
| status | 保持 / 改为 `draft` \| `active` \| `blocked` \| `done` \| `cancelled` |

用户若已在命令后写下「今天做了什么」，从中提取事实后再补问缺失项。

## 第二步：按核心提示词执行

参数齐备后，**完整阅读并严格执行**核心提示词：

- 路径：[`./skills/prompts/03-update-execution.md`](../../../prompts/03-update-execution.md)
- 使用其中「提示词正文」的时间线格式、强制步骤、禁止项与交付检查清单

## 必须遵守的 AGENTS 要点（摘要）

1. 只在 `02-execution.md` 追加**已发生事实**；禁止编造未完成工作  
2. 尽量写清改了哪些路径/产物，避免空话  
3. 调整 progress / status 时：改 `00-meta.md`，并**必须**同步 `docs/goals/goal-tree.md`  
4. 完成成功标准时，可在 meta 勾选并与事实一致  
5. 决策论证不写进 execution（去 `01-decision.md`）  
6. 遵守扁平存储、五件套与 parent 约定  

## 完成后

用核心提示词中的交付检查清单自检，并汇报：新增时间线条目、progress/status 是否与 meta、goal-tree 一致。
