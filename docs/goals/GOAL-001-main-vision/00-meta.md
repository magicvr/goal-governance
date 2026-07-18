---
id: GOAL-001-main-vision
title: 交付可复用的目标治理方法论、文档协议与消费工具
status: active
parent: null
created: 2026-07-18
updated: 2026-07-19
version: 0.2.0
---

# GOAL-001 · 交付可复用的目标治理方法论、文档协议与消费工具

## 概述

本仓库的**根目标（Root Goal）**：建立一套可复用、可审计的目标治理方法论与文档协议，把「目标 → 决策 → 执行 → 审计」固化为可追踪、可复盘、可协作的工作流，并提供两类消费适配器：面向 AI / Git 仓库协作的 Skills，以及面向人的 Web 工作台。

核心方法论与文档模板必须能够脱离 AI 宿主和 Web 独立使用；`docs/goals/` 保存具体项目的目标实例与过程事实，是运行时唯一真相源。

## 三层交付

### 1. 核心方法论与文档协议

- 生命周期、P-001～P-004、目标元数据和五件套写作约定。
- canonical 文档入口：`docs/README.md`、`docs/architecture/`、`docs/templates/goal-folder/`。
- `docs/templates/goal-folder/` 是规范模板；`skills/templates/goal-folder/` 是供离线安装与复制的同步分发镜像。

### 2. Skills

- 面向 AI / Agent 在 Git 仓库内设立、推进、记录和审计目标。
- `/govern`、`/audit`、原语、宿主 wrappers、安装脚本和契约测试均消费核心文档协议，不拥有独立状态。

### 3. Web

- 面向人浏览目标、查看决策/执行/审计并诊断文档树。
- 当前阶段保持只读，从 `docs/goals/` 加载数据；任何未来写入都必须遵守同一协议并另立可审计子目标。

## 成功标准（高层）

| 标准 | 当前状态 |
|------|----------|
| 核心方法论、文档协议和 canonical 模板可独立复制使用 | 基础已建立；独立产品化验收进行中 |
| Skills 能按核心协议安装并驱动 AI 闭环 | 当前 `/govern` + `/audit` 基线已交付；待完成核心契约对齐验收 |
| Web 能只读浏览目标并展示文档/树诊断，且不产生第二真相源 | 当前基线已完成（GOAL-004） |
| 三个交付面共享同一版本化协议，并有一致性/发布证据 | 尚未开始 |
| 至少一个子目标走完可审计的阶段性闭环 | 已由既有 GOAL-003、GOAL-004、GOAL-005 留有证据 |

## 高层路线图

> 既有 GOAL-002～005 是本次重基线前完成的基础与验证历史；它们不被改写为核心产品已经关门。后续按阶段立项，先路线图、后创建细粒度子目标。

| 阶段 | 主题 | 状态 | 关联 |
|------|------|------|------|
| 阶段 1 | 项目初始化与文档/Web/Skills 基础结构 | 已完成 | [GOAL-002-project-bootstrap](../GOAL-002-project-bootstrap/00-meta.md) |
| 阶段 2 | Skills 编排实践与闭环审计验证 | 已完成（历史基线） | [GOAL-003-skills-practice](../GOAL-003-skills-practice/00-meta.md)、[GOAL-005-skills-closed-loop-audit](../GOAL-005-skills-closed-loop-audit/00-meta.md) |
| 阶段 3 | Goal 数据模型与 Web 只读基线 | 已完成（历史基线） | [GOAL-004-core-data-model](../GOAL-004-core-data-model/00-meta.md) |
| 阶段 4 | 核心方法论、文档协议与 canonical 模板产品化 | 进行中（本次重基线；待拆分） | 待以 `GOAL-006` 起立项 |
| 阶段 5 | Skills 消费适配器与发布一致性 | 未开始 | 待拆分子目标 |
| 阶段 6 | Web 人类工作台深化 | 未开始（第一步保持只读） | 待拆分子目标 |
| 阶段 7 | 三面一致性、版本化与发布验收 | 未开始 | 待拆分子目标 |

## 子目标

| ID | 标题 | 状态 |
|----|------|------|
| GOAL-002-project-bootstrap | 完成项目初始化 | done |
| GOAL-003-skills-practice | 完善 Skills 并在本项目中实践验证 | done |
| GOAL-004-core-data-model | 实现核心数据模型与 Goal 基础管理 | done |
| GOAL-005-skills-closed-loop-audit | Skills 治理闭环与交叉审计 | done |

下一阶段子目标将在本路线图确认后，以 `GOAL-006` 起按阶段创建；本轮不提前批量创建细粒度目标。

## 相关路径

- 树状总览：[../goal-tree.md](../goal-tree.md)
- 文档规范：[../../README.md](../../README.md)
- 核心模板：[../../templates/](../../templates/)
- 架构说明：[../../architecture/](../../architecture/)
