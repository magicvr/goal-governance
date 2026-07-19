---
id: GOAL-001-main-vision
title: 交付可复用的目标治理方法论、文档协议与消费工具
status: active
parent: null
created: 2026-07-18
updated: 2026-07-20
version: 0.2.9
---

# GOAL-001 · 交付可复用的目标治理方法论、文档协议与消费工具

## 2026-07-20 · 阶段 5 关门交接

GOAL-008 已按 A-013 完成阶段 5 发布一致性关门，状态为 `done / 100%`。I-001～I-003 与 F-005 均有关闭证据：GitHub Copilot CLI `1.0.71` 提供当前 Copilot runtime replay，GitHub Actions run `29700051047` 绑定候选 commit `8a33ecd...` 完成 Ubuntu/Windows Web replay，annotated `v0.7.0` 通过 release-candidate checks。GOAL-001 仍保持 `active`；阶段 6 Web 深化可按路线图另行立项，F-006 继续为非阻塞 recommended。

## 概述

本仓库的**根目标（Root Goal）**：建立一套可复用、可审计的目标治理方法论与文档协议，把「目标 → 决策 → 执行 → 审计」固化为可追踪、可复盘、可协作的工作流，并提供两类消费适配器：面向 AI / Git 仓库协作的 Skills，以及面向人的 Web 工作台。

核心方法论与文档模板必须能够脱离 AI 宿主和 Web 独立使用；`docs/goals/` 保存具体项目的目标实例与过程事实，是运行时唯一真相源。

## 三层交付

### 1. 核心方法论与文档协议

- 生命周期、P-001～P-005、目标元数据和五件套写作约定。
- canonical 文档入口：`docs/README.md`、`docs/architecture/`、`docs/templates/goal-folder/`。
- `docs/templates/goal-folder/` 是规范模板；`skills/templates/goal-folder/` 是供离线安装与复制的同步分发镜像。

### 2. Skills

- 面向 AI / Agent 在 Git 仓库内设立、推进、记录和审计目标。
- `/govern`、`/audit`、原语、宿主 wrappers、安装脚本和契约测试均消费核心文档协议，不拥有独立状态。

### 3. Web

- 面向人浏览目标、查看决策/执行/审计并诊断文档树。
- 当前阶段保持只读，从 `docs/goals/` 加载数据；任何未来写入都必须遵守同一协议并另立可审计子目标。

## 成功标准（高层，历史快照）

| 标准 | 当前状态 |
|------|----------|
| 核心方法论、文档协议和 canonical 模板可独立复制使用 | 已完成（GOAL-006 done / 100%；A-005 close-out pass） |
| Skills 能按核心协议安装并驱动 AI 闭环 | GOAL-008 已取得 Claude/Grok 候选 `/govern`、`/audit` 机读证据；Copilot 双入口与 Web CI replay 仍开放，I-002 / I-003 / F-005 必须关闭后才完成阶段 5 |
| Web 能只读浏览目标并展示文档/树诊断，且不产生第二真相源 | 当前基线已完成（GOAL-004） |
| 三个交付面共享同一版本化协议，并有一致性/发布证据 | 进行中（矩阵、报告与 rehearsal 已形成；coverage pending / 3 uncovered，尚无 annotated tag） |
| 至少一个子目标走完可审计的阶段性闭环 | 已由既有 GOAL-003、GOAL-004、GOAL-005 留有证据 |

## 高层路线图（历史快照）

> 既有 GOAL-002～005 是本次重基线前完成的基础与验证历史；它们不被改写为核心产品已经关门。后续按阶段立项，先路线图、后创建细粒度子目标。

| 阶段 | 主题 | 状态 | 关联 |
|------|------|------|------|
| 阶段 1 | 项目初始化与文档/Web/Skills 基础结构 | 已完成 | [GOAL-002-project-bootstrap](../GOAL-002-project-bootstrap/00-meta.md) |
| 阶段 2 | Skills 编排实践与闭环审计验证 | 已完成（历史基线） | [GOAL-003-skills-practice](../GOAL-003-skills-practice/00-meta.md)、[GOAL-005-skills-closed-loop-audit](../GOAL-005-skills-closed-loop-audit/00-meta.md) |
| 阶段 3 | Goal 数据模型与 Web 只读基线 | 已完成（历史基线） | [GOAL-004-core-data-model](../GOAL-004-core-data-model/00-meta.md) |
| 阶段 4 | 核心方法论、文档协议与 canonical 模板产品化 | 已完成（GOAL-006 done / 100%；A-005 close-out pass） | [GOAL-006-core-methodology-template-productization](../GOAL-006-core-methodology-template-productization/00-meta.md) |
| 阶段 5 | Skills 消费适配器与发布一致性 | 进行中（GOAL-008 active / 20%；完整关门已重启） | [GOAL-008-skills-consumer-adapter-release-consistency](../GOAL-008-skills-consumer-adapter-release-consistency/00-meta.md) |
| 阶段 6 | Web 人类工作台深化 | 未开始（GOAL-008 完整关门后再启动；第一步保持只读） | 待拆分子目标 |
| 阶段 7 | 三面一致性、版本化与发布验收 | 未开始 | 待拆分子目标 |

### 阶段 4 的可执行产品化与退出契约

阶段 4 的最小交付包、canonical 所有者、独立复制场景、版本同步策略、非目标、验收证据和进入阶段 5 的门槛，由 [D-008](01-decision.md#d-008--阶段-4-产品化与退出契约2026-07-19) 定义。本契约已满足以 `GOAL-006` 承接阶段 4 的 P-001 前置条件；GOAL-006 后续以 A-005 self close-out 与 A-004 independent targeted 复审完成阶段 4，阶段 5 仍待另行立项。

### 跨阶段协议修订：信息就绪

[A-004](03-audit.md) 发现当前闭环只处理范围和实施质量，未把“尚未掌握哪些必需信息、何时必须掌握”写成协议。该 required 缺口已由 [GOAL-007-information-readiness-governance](../GOAL-007-information-readiness-governance/00-meta.md) 完成，并由 [A-005](03-audit.md#a-005--响应-a-004--f-004-信息就绪协议缺口2026-07-19) 关闭 F-004；它是阶段 5 前的核心协议修订，不把历史阶段 4 交付重写为未完成。

## 子目标（历史快照）

| ID | 标题 | 状态 |
|----|------|------|
| GOAL-002-project-bootstrap | 完成项目初始化 | done |
| GOAL-003-skills-practice | 完善 Skills 并在本项目中实践验证 | done |
| GOAL-004-core-data-model | 实现核心数据模型与 Goal 基础管理 | done |
| GOAL-005-skills-closed-loop-audit | Skills 治理闭环与交叉审计 | done |
| GOAL-006-core-methodology-template-productization | 核心方法论、文档协议与 canonical 模板产品化 | done |
| GOAL-007-information-readiness-governance | 信息就绪与未知项治理 | done |
| GOAL-008-skills-consumer-adapter-release-consistency | Skills 消费适配器跨宿主/跨版本发布一致性 | active / 20% |

`GOAL-006` 已在 D-008 的阶段 4 契约下完成最小交付包、独立复制验证、镜像核验与关门审计（A-001～A-005）。`GOAL-007` 已完成单一跨阶段协议修订，并以 A-001 / 根目标 A-005 关闭 A-004 的 required finding。`GOAL-008` 已将 Claude/Grok 四个候选 runtime 单元验证为 `runtime-verified`，当前仍缺 Copilot 双入口、Web CI replay 与 release-candidate/tag；I-002、I-003 与 F-005 为 `collecting / required`，不把阶段 5 写成完成，也不在其完成前启动阶段 6 深化。

## 相关路径

- 树状总览：[../goal-tree.md](../goal-tree.md)
- 文档规范：[../../README.md](../../README.md)
- 核心模板：[../../templates/](../../templates/)
- 架构说明：[../../architecture/](../../architecture/)
