---
title: /write-audit · 写阶段性复盘（Copilot wrapper）
description: 引导收集复盘参数后，按 skills/prompts/04-write-audit.md 写入 03-audit.md
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
slash: /write-audit
---

<!--
  这是 GitHub Copilot 斜杠命令 wrapper（轻量交互入口）。
  核心提示词在：skills/prompts/04-write-audit.md
  修改核心提示词即可全局生效；本文件只负责引导参数与引用核心。
  用法：复制到项目根 .github/prompts/（建议命名 write-audit.prompt.md），
  在 Copilot Chat 输入 /write-audit 调用。
-->

# /write-audit · 写阶段性复盘

你是本仓库的目标治理协作者。请严格遵守项目 AI 规则（根目录 `AGENTS.md`，或已安装的 `.github/copilot-instructions.md`）。

## 第一步：向我收集必要参数

信息缺失或不确定时，**先向我确认，不要猜测后继续**。请确认：

| 参数 | 说明 |
|------|------|
| 目标 ID / 路径 | 如 `GOAL-003-skills-practice` |
| 复盘区间 | 如 `2026-07-18 ～ 2026-07-25`，或「立项至首次 Skills 落地」 |
| 复盘类型 | 中期检查 / 阶段结束 / 目标关闭 |
| 主要成果 | 可选；也可由你从文档归纳后请我确认 |
| 已知偏差或问题 | 可选 |
| 是否调整 status/progress | 否 / 是（说明） |
| 今日日期 | `YYYY-MM-DD` |

材料不足时列出「证据缺口」，不要脑补成果。

## 第二步：按核心提示词执行

参数齐备后，**完整阅读并严格执行**核心提示词：

- 路径：[`./skills/prompts/04-write-audit.md`](../../../prompts/04-write-audit.md)
- 使用其中「提示词正文」的 `A-NNN` 结构、强制步骤、禁止项与交付检查清单
- 必须先通读该目标 `00-meta` / `01-decision` / `02-execution` 再写复盘

## 必须遵守的 AGENTS 要点（摘要）

1. 复盘锚定已有文档事实；成果须能指向文件、决策编号或 execution 条目  
2. 对照成功标准逐条：已达成 / 部分 / 未开始 / 证据不足  
3. 追加 `03-audit.md` 新章节，**不要覆盖**历史复盘  
4. 若结论导致 status / progress 变化：更新 `00-meta.md` 并**必须**同步 `docs/goals/goal-tree.md`  
5. 重大取舍应写入 `01-decision.md`，不要只留在 audit  
6. 遵守扁平存储、五件套、P-001；语气具体可验证，避免无证据形容词  

## 完成后

用核心提示词中的交付检查清单自检，并汇报：复盘编号、成功标准对照结论、是否联动 meta / goal-tree。
