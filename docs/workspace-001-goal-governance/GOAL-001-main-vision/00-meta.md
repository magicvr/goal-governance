---
id: GOAL-001-main-vision
title: 交付可复用的目标治理方法论、文档协议与消费工具
status: active
parent: null
created: 2026-07-18
updated: 2026-07-22
version: 0.6.0
---

# GOAL-001 · 交付可复用的目标治理方法论、文档协议与消费工具

## 2026-07-22 · 阶段 6 有界交付现时（A-057 F-029 响应）

> 现时以 [goal-tree.md](../goal-tree.md) 与下表为准。下文「2026-07-20」各节及「历史快照」表保留原貌，**不要**当作现时 status。

阶段 6 **有界规划/α/X-AI 闭环已完成**（GOAL-009～014 均为 `done / 100%`，各目标有界范围见各自 meta）。**未**宣称一期 Web 产品终态；扩展与终态复审挂 [GOAL-009 **R-009-X**](../GOAL-009-ai-assisted-governance-workbench/00-meta.md#residual-台账e--accepted)。Root 保持 `active`。

| 交付面 | 现时状态 | 结论 |
|--------|----------|------|
| 核心方法论与模板 | GOAL-006 / 007 / 010 `done / 100%` | 协议与模板可复用；工作区/共享资料固定引用协议已就位。 |
| Skills 消费适配器 | GOAL-008 `done / 100%` | 阶段 5 已关门；含新行为的发布仍须按 GOAL-008 惯例刷新 runtime evidence。 |
| Web 工作台 | GOAL-009 `done / 100%`（有界）；GOAL-012/013/014 `done / 100%` | 规划台账 + α 切片 + 受控写 CT + X-AI 有界运行时已交付。生产受控写须双门闩 env；**N1 / 资料 CRUD 产品 / 人类多会话试点 / I 全文 verified / 阶段 6 终态宣称** → **R-009-X**。 |

## 2026-07-20 · 阶段 5 关门交接

GOAL-008 已按 A-013 完成阶段 5 发布一致性关门，状态为 `done / 100%`。I-001～I-003 与 F-005 均有关闭证据：GitHub Copilot CLI `1.0.71` 提供当前 Copilot runtime replay，GitHub Actions run `29700051047` 绑定候选 commit `8a33ecd...` 完成 Ubuntu/Windows Web replay，annotated `v0.7.0` 通过 release-candidate checks。GOAL-001 仍保持 `active`；阶段 6 Web 深化可按路线图另行立项，F-006 继续为非阻塞 recommended。

## 2026-07-20 · 阶段 6 方向重定向

用户明确拒绝将 Web 发展成“完善的只读工具”。阶段 6 的目标改为**供人类实际治理工作时获得 AI 协助的 Web 工作台**：它应帮助发现上下文、提出可审查的下一步、生成决策/执行/审计候选、展示影响与证据，并在明确的人类确认后受控写入 canonical `docs/goals/`。Web 不取得独立状态所有权，也不得自动裁决 P-004、关闭 required finding 或把目标标为 `done`。本方向由 D-014 和 [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md) 承接；当前仅进入产品规划与信息发现，不把写入、鉴权、AI 提案或部署写成已实现事实。

## 2026-07-20 · 工作区与共享资料区跨层协议

用户要求将工作区与共享资料区从 Web 产品发现中提升为核心文档协议，并先由 Skills 适配。[GOAL-010-core-workspace-shared-materials-protocol](../GOAL-010-core-workspace-shared-materials-protocol/00-meta.md) 已以 `done / 100%` 完成该跨层工作：它定义工作区到独立 Root Goal/canonical 范围的绑定、串行阶段子目标与共享资料固定引用规则。GOAL-010 不改写 GOAL-006/GOAL-008 的历史关门，也不替代 GOAL-009 对 I-009/I-010、F-003/F-004、Web 访问或产品验证的责任。

## 2026-07-20 · 显式工作区目录迁移

[GOAL-011-multi-workspace-directory-migration](../GOAL-011-multi-workspace-directory-migration/00-meta.md) 已完成当前项目从全局 `docs/goals/` 到 `docs/workspace-001-goal-governance/` 的迁移。该工作区根现在承载本 Root Goal、`goal-tree.md` 和全部目标实例；`docs/shared-materials/` 只承载候选资料库存，不形成目标状态或关闭 GOAL-009 的产品门禁。

## 概述

本仓库的**根目标（Root Goal）**：建立一套可复用、可审计的目标治理方法论与文档协议，把「目标 → 决策 → 执行 → 审计」固化为可追踪、可复盘、可协作的工作流，并提供两类消费适配器：面向 AI / Git 仓库协作的 Skills，以及面向人的 Web 工作台。

核心方法论与文档模板必须能够脱离 AI 宿主和 Web 独立使用；已验证工作区根保存其具体项目的目标实例与过程事实，是运行时唯一真相源。

## 三层交付

### 1. 核心方法论与文档协议

- 生命周期、P-001～P-005、目标元数据和五件套写作约定。
- canonical 文档入口：`docs/README.md`、`docs/architecture/`、`docs/templates/goal-folder/`。
- `docs/templates/goal-folder/` 是规范模板；`skills/templates/goal-folder/` 是供离线安装与复制的同步分发镜像。

### 2. Skills

- 面向 AI / Agent 在 Git 仓库内设立、推进、记录和审计目标。
- `/govern`、`/audit`、原语、宿主 wrappers、安装脚本和契约测试均消费核心文档协议，不拥有独立状态。

### 3. Web

- 面向人完成目标治理工作，并由 AI 提供上下文发现、方案候选、门禁提示、证据追溯与受控变更协助。
- 当前工作区根继续是唯一 runtime truth source。Web 可以在后续经验证的阶段提出和执行受人确认的变更，但不得自建生命周期、状态库或绕过同一协议、事务保护和审计证据。

## 当前阶段状态（2026-07-22）

| 交付面 | 当前状态 | 结论 |
|--------|----------|------|
| 核心方法论与模板 | GOAL-006 `done / 100%`；GOAL-007 `done / 100%`；GOAL-010 `done / 100%` | 核心协议、信息就绪与工作区/共享资料固定引用已就位。 |
| Skills 消费适配器 | GOAL-008 `done / 100%`；GOAL-010 `done / 100%` | 阶段 5 已关门；新行为发布前刷新 runtime evidence。 |
| Web 工作台 | GOAL-009 `done / 100%`（有界）；GOAL-012/013/014 `done / 100%` | α + 受控写 + X-AI 有界已交付；扩展/终态见 **R-009-X**（≠ 产品终态）。 |

> **历史注记**：2026-07-20 曾将 Web 记为 `GOAL-009 active / 0%`（规划起点）。该行已失效；勿再引用为现时。

## 成功标准（历史快照）

> 下表保留阶段 5 关门前的判断，用于解释当时的门禁；当前状态以本文件“当前阶段状态”、D-014、GOAL-008 A-016 与 goal-tree 为准。

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

### 阶段 6 当前路线图：AI 协助的人类目标治理工作台

| 顺序 | 阶段 | 目标与退出条件 | 承接 / 现时 |
|------|------|----------------|------------|
| 6A | 产品形态与信息发现 | 明确人类角色、核心工作流、AI 协作边界、成功标准和 required 信息门禁。 | GOAL-009 **有界 done** |
| 6A-P | 跨层工作区与共享资料协议 | 工作区 Root Goal 绑定、串行阶段、共享资料固定引用与 Skills 首先适配。 | GOAL-010 / 011 `done` |
| 6B | 可信读模型与 AI 协作面 | 事实准入、WS/SM 有界验证；AI 运行时有界。 | F-002～004 有界 + GOAL-014 **有界 done**；全文 → R-009-X |
| 6C | 受控变更契约 | 预览/diff、确认、事务/恢复；α CT + 生产双门闩。 | GOAL-013 **有界 done**；F-007/008 closed；A-030 |
| 6D | 首个端到端工作流（α） | 配置化产品工作区详情 + 受限执行事实追加。 | GOAL-012 **有界 done** |
| 6E | 试点与有界关门评估 | E-α 冒烟；有界 close-out；扩展 residual。 | GOAL-009 E-α + **R-009-X accepted** |
| 6X | 扩展（未宣称终态） | N1 导航、资料 CRUD 产品、人类多会话试点、I 全文 verified、终态宣称。 | **R-009-X**；可选 X-NAV / X-SM / 试点等另立目标 |

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

## 当前子目标指向（2026-07-22）

| ID | 标题 | 状态 | 作用 |
|----|------|------|------|
| GOAL-009-ai-assisted-governance-workbench | 规划 AI 协助的人类目标治理 Web 工作台 | **done / 100%**（有界） | 阶段 6 规划台账 + α/X-AI 有界闭环已关；扩展/终态 → **R-009-X**。 |
| GOAL-010-core-workspace-shared-materials-protocol | 建立工作区与共享资料区核心协议，并完成 Skills 首先适配 | done / 100% | 跨层协议与 Skills 适配。 |
| GOAL-011-multi-workspace-directory-migration | 完成多工作区目录迁移与共享资料索引骨架 | done / 100% | 显式工作区根 + 共享资料候选库存。 |
| GOAL-012-first-slice-workspace-detail | 首个垂直切片：配置化工作区详情与受控执行事实追加 | done / 100%（有界） | α 实现。 |
| GOAL-013-write-gate-ct-durable-idempotency | 受控写入 CT 与跨进程幂等 | done / 100%（有界） | 写入门禁证据。 |
| GOAL-014-ai-collaboration-runtime | AI 协作运行时与用户确认链 | done / 100%（有界） | X-AI；R-014-E2E residual。 |

完整树与 status 以 [goal-tree.md](../goal-tree.md) 为准。下一编号 **GOAL-015**（扩展另立时）。

## 相关路径

- 树状总览：[../goal-tree.md](../goal-tree.md)
- 文档规范：[../../README.md](../../README.md)
- 核心模板：[../../templates/](../../templates/)
- 架构说明：[../../architecture/](../../architecture/)
