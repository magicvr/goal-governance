---
title: Skills · 提示词模板
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
---

# prompts/ · 目标治理提示词模板

本目录提供**可直接复制**给 AI 助手（Claude Code、Copilot、Cursor 等）使用的提示词，覆盖目标治理日常四类操作。

## 目录

```text
skills/prompts/
├── README.md                 # 本文件
├── 01-create-new-goal.md     # 创建新目标
├── 02-record-decision.md     # 记录决策
├── 03-update-execution.md    # 更新执行进度
└── 04-write-audit.md         # 写阶段性复盘
```

## 使用方式

1. 打开对应 `.md` 文件，复制 **「提示词正文」** 代码块中的全文。
2. 按提示替换占位符（如目标 ID、今天完成了什么、父目标等）。
3. 粘贴给 AI 助手，并确保仓库中已有 [AGENTS.md](../../AGENTS.md)（或从 [AGENTS.template.md](../AGENTS.template.md) 复制）。
4. 执行完成后，人工核对：五件套是否齐全、`goal-tree.md` 是否已同步、内容是否真实。

## 设计原则

| 原则 | 说明 |
|------|------|
| 遵守 AGENTS | 扁平存储、parent 字段、goal-tree 同步、五件套一次建齐 |
| 可直接丢给 AI | 提示词自包含上下文要求，少依赖口头补充 |
| 结构化、真实 | 引导写事实与取舍，禁止编造进度与空话 |
| 路线图优先 | 大目标须先高层路线图，再拆子目标（P-001） |

## 与其他交付物的关系

| 路径 | 角色 |
|------|------|
| [../AGENTS.template.md](../AGENTS.template.md) | 规则正文（AI 必须遵守） |
| [../templates/goal-folder/](../templates/goal-folder/) | 目标文件夹模板（含虚构示例，复制后改写） |
| 本目录 | **怎么做**的可复制提示词 |

## 使用建议

- 在已启用 AGENTS 规则的仓库中使用效果最好。
- 提示词要求 AI 先读 `docs/goals/goal-tree.md`，再动手；若 AI 跳过，请要求其补做。
- 不确定的信息应标「待确认」，不要让 AI 猜进度百分比或虚构完成项。
