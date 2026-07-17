---
id: GOAL-001-main-vision
title: 构建一个实用的目标治理框架（Goal Governance Framework）
status: active
parent: null
created: 2026-07-18
updated: 2026-07-18
version: 0.1.0
---

# GOAL-001 · 构建一个实用的目标治理框架

## 概述

本仓库的**根目标（Root Goal）**：构建一套可落地的目标治理框架，把「目标 → 决策 → 执行 → 审计」串成可追踪、可复盘、可协作的闭环。

## 交付形态（双交付）

1. **Web 应用**：可视化查看与操作目标、决策、执行与审计信息。
2. **Skills / 提示词**：让 AI 助手按同一套规则读写文档、推进目标。

## 成功标准（高层）

- 文档体系规则清晰，AI 与人都可稳定遵守。
- 目标层级可维护（扁平存储 + `parent` + `goal-tree.md`）。
- Web 应用能覆盖决策 / 执行 / 审计的基础浏览与后续扩展。
- 至少一个完整子目标从启动走到可审计的阶段性结果。

## 高层路线图

> 后续阶段会根据实践反馈再正式拆分为具体子目标；当前仅作方向指引。

| 阶段 | 主题 | 状态 | 关联 |
|------|------|------|------|
| 阶段 1 | 项目初始化 | 已完成 | [GOAL-002-project-bootstrap](../GOAL-002-project-bootstrap/00-meta.md) |
| 阶段 2 | Skills 完善与实践验证 | 进行中 | [GOAL-003-skills-practice](../GOAL-003-skills-practice/00-meta.md) |
| 阶段 3 | 核心数据模型与 Goal 基础管理 | 未开始 | 待拆分子目标 |
| 阶段 4 | Web 与文档体系联动 | 未开始 | 待拆分子目标 |
| 阶段 5 | 高级能力与打磨（漂移检测、AI 辅助等） | 未开始 | 待拆分子目标 |

## 子目标

| ID | 标题 | 状态 |
|----|------|------|
| GOAL-002-project-bootstrap | 完成项目初始化 | done |
| GOAL-003-skills-practice | 完善 Skills 并在本项目中实践验证 | active |

## 相关路径

- 树状总览：[../goal-tree.md](../goal-tree.md)
- 文档规范：[../../README.md](../../README.md)
- 架构说明：[../../architecture/](../../architecture/)
