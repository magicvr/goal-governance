---
title: Skills · 提示词模板
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.2.0
---

# prompts/ · 目标治理提示词

## 默认用户路径（主入口）

| 文件 | 角色 | 用途 |
|------|------|------|
| [00-govern-orchestrator.md](00-govern-orchestrator.md) | **primary** | 扫描项目与 goal-tree → 分类情境 → 引导设立总目的 **或** 提议下一步并确认 → 调用下方原语 |

Copilot 对应主 wrapper：`/govern`（`install/copilot/prompts/govern.md`）。

**请优先使用主入口。** 生命周期：设立目标 → 推进目标 → 阶段性/关门审计。

## 原语（primitives / advanced）

编排器在用户确认后调用；熟练用户也可直调。**不是**四个并列的默认产品入口。

| 文件 | 角色 | 用途 |
|------|------|------|
| [01-create-new-goal.md](01-create-new-goal.md) | primitive | 创建新目标（五件套 + goal-tree） |
| [02-record-decision.md](02-record-decision.md) | primitive | 记录决策（决定了什么 / 为什么） |
| [03-update-execution.md](03-update-execution.md) | primitive | 更新执行时间线与进度 |
| [04-write-audit.md](04-write-audit.md) | primitive | 阶段性 / 关门复盘 |

## 使用方式

### 主路径

1. 打开 [00-govern-orchestrator.md](00-govern-orchestrator.md)，复制「提示词正文」，或在 Copilot 使用 `/govern`。
2. 让 AI 先扫描再提议；确认后再写入。
3. 确保仓库已有 AGENTS / copilot-instructions。

### 原语直调（高级）

1. 打开对应 `01`～`04`，复制「提示词正文」。
2. 填占位符；信息缺失时先确认。
3. 核对五件套与 `goal-tree.md`。

## 设计原则

| 原则 | 说明 |
|------|------|
| 目的优先 | 辅助达到目的，而非辅助填表 |
| 单入口 | 默认只暴露编排器 |
| 原语可组合 | 01～04 保证文档结构一致 |
| 遵守 AGENTS | 扁平存储、parent、goal-tree、P-001 |
| 真实 | 禁止编造进度与空话 |

## 与其他交付物

| 路径 | 角色 |
|------|------|
| [../AGENTS.template.md](../AGENTS.template.md) | 规则正文 |
| [../templates/goal-folder/](../templates/goal-folder/) | 目标文件夹示例 |
| [../install/copilot/prompts/](../install/copilot/prompts/) | Copilot：默认只装 `govern`；四原子 slash 仅 `--with-primitives` |
