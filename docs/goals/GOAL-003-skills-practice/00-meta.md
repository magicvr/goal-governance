---
id: GOAL-003-skills-practice
title: 完善 Skills 并在本项目中实践验证
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.1.5
progress: 70%
---

# GOAL-003 · 完善 Skills 并在本项目中实践验证

## 概述

在总目标 [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md) 下，把 GOAL-002 已落地的 Skills **基础结构** 打磨为可执行、可复用的协作规范，并在本项目中强制使用、收集反馈、迭代修正。

## 范围

### 在范围内

1. 优化 [skills/AGENTS.template.md](../../../skills/AGENTS.template.md)，使规则更清晰、可执行
2. 补充实用的提示词模板（创建新目标、记录决策、更新执行进度、写阶段性复盘等）
3. 完善 [skills/templates/goal-folder/](../../../skills/templates/goal-folder/) 的示例内容
4. 在本项目中强制使用这套 Skills，并记录使用反馈与改进点
5. 产出一份简短的「Skills 使用反馈与修正记录」

### 不在范围内

- Web 数据模型、CRUD
- 自动化校验工具（编号、parent、goal-tree 一致性等）
- 完整可安装 Skill 包（VS Code / Copilot 等）

## 成功标准

- [x] `skills/AGENTS.template.md` 规则可直接照做，歧义点已收敛
- [x] 至少 4 类常用提示词模板可用（新目标 / 决策 / 执行 / 复盘）
- [x] `skills/templates/goal-folder/` 带有可参考的示例内容（非空白占位）
- [ ] 本仓库协作已按 Skills 规则运行，并有书面使用反馈
- [ ] 「Skills 使用反馈与修正记录」已产出（可放 `attachments/` 或本目标文档内）

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
