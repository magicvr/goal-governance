---
id: GOAL-001-main-vision
title: 交付可复用的目标治理方法论、文档协议与消费工具
status: done
parent: null
plan_refs: VP-001-governance-platform-delivery
primary_plan: VP-001-governance-platform-delivery
serves_summary: 奠基 Root（有界 done）；服务已关 VP-001 / vision-goal-governance@0.2.0；演进见 VP-002 + workspace-002-methodology-skills-feedback
created: 2026-07-18
updated: 2026-08-04
version: 1.0.2
---

# GOAL-001 · 交付可复用的目标治理方法论、文档协议与消费工具

## 现时摘要（2026-08-04）· 单一权威入口 · **有界关门**

> **本文件现时 status 只以本节为准**。完整树见 [goal-tree.md](../goal-tree.md)。
>
> **有界关门**：[D-028](01-decision.md#d-028--root-有界关门奠基完成演进改挂-vp-002--workspace-0022026-07-31) / [A-021](03-audit.md#a-021--root-有界关门审计close-out2026-07-31) **pass**。  
> **不等于** Charter done、Web 产品终态、协议停止演进。  
> **演进容器**：**VP-002** + **[workspace-002-methodology-skills-feedback](../../workspace-002-methodology-skills-feedback/)**（禁止在本 done Root 下开 GOAL-024+）。

### Root 现时

| 项 | 值 |
|----|-----|
| **status** | **`done`**（有界奠基关） |
| **progress 宣称** | 奠基波完成；**不**宣称 Web 终态 / Charter 完成 |
| **关门** | D-028 + A-021；前置 D-027 Web 冻结、Charter 0.2.0、VP-001 closed |
| **子目标** | GOAL-002～023 均 `done / 100%` |
| **本区编号** | **封存**（不再分配 GOAL-024+） |
| **工作区** | `workspace-001-goal-governance` · `status: archived` |
| **后置决策** | [D-029](01-decision/D-029-retire-frozen-web-assets.md)：授权退役冻结 Web；实施由 workspace-002 GOAL-004 承接，Root 不重开 |

### 交付面结项

| 交付面 | 状态 | 移交 |
|--------|------|------|
| 核心方法论与模板 | 奠基 done | 修正 → **VP-002** |
| Skills | 奠基 done | F-006 等 → **VP-002** |
| Web | 历史有界；物理退役进行中 | R-009-X → **VP-003**（`planned` + 正式挂起） |

### 愿景栈（关门时）

| 项 | 值 |
|----|-----|
| Charter | [vision-goal-governance@0.2.0](../../../vision/charter.md) · 仍 `active`（不可 done） |
| 本 Root primary_plan | [VP-001](../../../vision/plans/VP-001-governance-platform-delivery.md) · **closed** |
| 组合编排 | VP-001 closed · **VP-002 active**（lead workspace-002）· VP-003 planned |
| Vision Review | [VRev-006](../../../vision/reviews.md) portfolio close-out |

### Residual（不因 Root done 而关闭）

| 项 | 状态 | 去向 |
|----|------|------|
| R-009-X | accepted | VP-003 |
| A-006 F-006 | recommended open | VP-002 |
| H-WEB-01 / H-EVOL-01 | Charter 假设 | 复核触发见 Charter |

### 下一步（本 Root 已关）

1. **禁止**在本树新建子目标或改回 active 假装未关（除非用户新 D 重开）。  
2. **演进区已开**：[workspace-002-methodology-skills-feedback](../../workspace-002-methodology-skills-feedback/) · Root + GOAL-002（Codex Skills 入口）；推进请对该区 `/govern`。  
3. 只读查阅本区历史过程；冻结 `web/` 资产的退役事实由 workspace-002 GOAL-004 记录。

---

## 2026-07-28 · 关键决策指针（非现时 status 表）

| 裁决 | 要点 | 权威版本 / 说明 |
|------|------|----------------|
| **[D-024](01-decision.md#d-024--a-015-f-008-路径-d仅维护发版协议不关-root2026-07-28)** | **路径 D**：仅维护不关 Root；关闭 A-015 F-008；018/019 归属 Skills 维护波次 | A-017；A/B/C 延期 |
| **[D-025](01-decision.md#d-025--响应-a-018p-006-后核心包--standalone--agents-回流2026-07-29)** | A-018 F-012～F-015 fixed；standalone/core/AGENTS 回流 | A-019；路径 D |
| [D-017](01-decision.md#d-017--p-006-愿景组合治理与级联对齐第一刀2026-07-28) | P-006；冷启动 Charter→VP→区；取消 sandbox opt-out；Vision Review | principles **0.7.0**；alignment **0.3.0**；AGENTS **0.10.1** |
| [D-016](01-decision.md#d-016--核心协议逻辑一致性修订finding-闭合--隐式工作区--p-004-扩表2026-07-28) | finding 三路径；P-004.3/4.4；legacy 唯一路径 | 其后 D-017 升版；Root 仍 active |
| D-018～D-023 | `/vision` 第二刀；follow-through；`/vision-audit`；runtime 重采（不发版） | 见 [02-execution](02-execution.md)；追溯为路径 D 型维护 |

## 愿景对齐

| 项 | 值 |
|----|-----|
| Charter | [vision-goal-governance@0.2.0](../../../vision/charter.md) |
| plan_refs | `VP-001-governance-platform-delivery` |
| primary_plan | [VP-001-governance-platform-delivery](../../../vision/plans/VP-001-governance-platform-delivery.md) |
| serves_summary | 本 Root 是 primary 工作区的可治理总目标：展开区内路线图与子目标，推进 VP-001（协议 + Skills；Web 历史切片其后由 D-029 授权退役），而不把仓库 Charter 标为可 `done` 的 Goal。 |

## 2026-07-22 · 阶段 6 有界结项（D-015 / A-014）

> **历史结项记录**（仍有效作为阶段 6 有界证据）。**现时三面状态与下一步**以上方「现时摘要（2026-07-28）」为准；结项之后已发生 GOAL-018/019 与 D-016～D-023。

| 项 | 值 |
|----|-----|
| **阶段 6** | **有界结项** — AI 协助人类 Web 工作台在有界交付意义上完成 |
| **裁决** | [D-015](01-decision.md#d-015--阶段-6-有界结项审视不关-rootr-009-x-仍-accepted2026-07-22) / [A-014](03-audit.md#a-014--阶段-6-有界结项审视2026-07-22) |
| **证据** | GOAL-009 有界关门 + GOAL-012～017 有界 done（α / 受控写 / X-AI / N1 / 资料 / 路径试点） |
| **Root status** | **`active`（本条不改为 done）** |
| **R-009-X** | **仍 accepted** — 约束终态宣称、I 全文 verified、人手 UX 全文、AI 读资料全文等 |
| **明确不构成** | 一期 Web 产品终态；Root 关门；R-009-X closed；阶段 7 完成 |

## 2026-07-20 · 阶段 5 关门交接（历史）

GOAL-008 已按 A-013 完成阶段 5 发布一致性关门，状态为 `done / 100%`。I-001～I-003 与 F-005 均有关闭证据：GitHub Copilot CLI `1.0.71` 提供当时 Copilot runtime replay，GitHub Actions run `29700051047` 绑定候选 commit `8a33ecd...` 完成 Ubuntu/Windows Web replay，annotated `v0.7.0` 通过 release-candidate checks。GOAL-001 仍保持 `active`；F-006 继续为非阻塞 recommended。**其后**阶段 6 有界结项与 018/019 见现时摘要。

## 2026-07-20 · 阶段 6 方向重定向（历史）

用户明确拒绝将 Web 发展成“完善的只读工具”。阶段 6 的目标改为**供人类实际治理工作时获得 AI 协助的 Web 工作台**：它应帮助发现上下文、提出可审查的下一步、生成决策/执行/审计候选、展示影响与证据，并在明确的人类确认后受控写入 canonical 工作区根。Web 不取得独立状态所有权，也不得自动裁决 P-004、关闭 required finding 或把目标标为 `done`。本方向由 D-014 和 [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md) 承接。**规划起点叙述已过时**；现时见有界结项与现时摘要。

## 2026-07-20 · 工作区与共享资料区跨层协议（历史）

用户要求将工作区与共享资料区从 Web 产品发现中提升为核心文档协议，并先由 Skills 适配。[GOAL-010-core-workspace-shared-materials-protocol](../GOAL-010-core-workspace-shared-materials-protocol/00-meta.md) 已以 `done / 100%` 完成该跨层工作。GOAL-010 不改写 GOAL-006/GOAL-008 的历史关门，也不替代 GOAL-009 对 I-009/I-010 等产品门禁的责任。

## 2026-07-20 · 显式工作区目录迁移（历史）

[GOAL-011-multi-workspace-directory-migration](../GOAL-011-multi-workspace-directory-migration/00-meta.md) 已完成当前项目从全局 `docs/goals/` 到 `docs/workspace-001-goal-governance/` 的迁移。该工作区根现在承载本 Root Goal、`goal-tree.md` 和全部目标实例；`docs/shared-materials/` 只承载候选资料库存。

## 概述

本仓库的**根目标（Root Goal）**：建立一套可复用、可审计的目标治理方法论与文档协议，把「目标 → 决策 → 执行 → 审计」固化为可追踪、可复盘、可协作的工作流，并提供两类消费适配器：面向 AI / Git 仓库协作的 Skills，以及面向人的 Web 工作台。

核心方法论与文档模板必须能够脱离 AI 宿主和 Web 独立使用；已验证工作区根保存其具体项目的目标实例与过程事实，是运行时唯一真相源。

## 三层交付

### 1. 核心方法论与文档协议

- 生命周期、P-001～P-006、目标元数据和五件套写作约定。
- canonical 文档入口：`docs/README.md`、`docs/architecture/`、`docs/templates/goal-folder/`。
- `docs/templates/goal-folder/` 是规范模板（canonical）。包内分发镜像由 **stage** 生成到 `skills/core/docs/templates/goal-folder/`（GOAL-022）；`skills/templates/README.md` 仅为指针。install `-All` 若再写 `skills/templates/`，视为**派生副本**，禁止手维、禁止在 monorepo 对 `./skills` 跑 `-All` 当同步手段。

### 2. Skills

- 面向 AI / Agent 在 Git 仓库内设立、推进、记录和审计目标。
- `/govern`、`/audit`、`/vision`、`/vision-audit`、原语、宿主 wrappers、安装脚本和契约测试均消费核心文档协议，不拥有独立状态。

### 3. Web

- 面向人完成目标治理工作，并由 AI 提供上下文发现、方案候选、门禁提示、证据追溯与受控变更协助。
- 当前工作区根继续是唯一 runtime truth source。Web 可以在经验证的阶段提出和执行受人确认的变更，但不得自建生命周期、状态库或绕过同一协议、事务保护和审计证据。

## 成功标准（历史快照 · 阶段 5 关门前）

> **不可作现时 status。** 现时三面与门禁见上方「现时摘要（2026-07-28）」。下表仅解释当时门禁语境。

| 标准 | 当时记录（过时） |
|------|------------------|
| 核心方法论、文档协议和 canonical 模板可独立复制使用 | 已完成（GOAL-006 done / 100%；A-005 close-out pass） |
| Skills 能按核心协议安装并驱动 AI 闭环 | 当时 I-002 / I-003 / F-005 仍开放（**其后** GOAL-008 A-016 / Root A-013 已关） |
| Web 能只读浏览目标并展示文档/树诊断，且不产生第二真相源 | 基线 GOAL-004；**其后**阶段 6 有界结项 |
| 三个交付面共享同一版本化协议，并有一致性/发布证据 | 当时 coverage pending（**其后** v0.7.0 / v0.8.0 等；现时候选见 goal-tree 日志） |
| 至少一个子目标走完可审计的阶段性闭环 | 已由 GOAL-003、GOAL-004、GOAL-005 留有证据 |

## 高层路线图（历史快照 · 重基线后早期表）

> **不可作现时 status。** 表内阶段 5「进行中 / 20%」、阶段 6「未开始」等为**早期快照**，与现时冲突时以「现时摘要（2026-07-28）」为准。
> 既有 GOAL-002～005 是重基线前完成的基础与验证历史；它们不被改写为「核心产品从未关门」。

| 阶段 | 主题 | 快照状态（过时） | 关联 |
|------|------|------------------|------|
| 阶段 1 | 项目初始化与文档/Web/Skills 基础结构 | 已完成 | [GOAL-002-project-bootstrap](../GOAL-002-project-bootstrap/00-meta.md) |
| 阶段 2 | Skills 编排实践与闭环审计验证 | 已完成（历史基线） | [GOAL-003-skills-practice](../GOAL-003-skills-practice/00-meta.md)、[GOAL-005-skills-closed-loop-audit](../GOAL-005-skills-closed-loop-audit/00-meta.md) |
| 阶段 3 | Goal 数据模型与 Web 只读基线 | 已完成（历史基线） | [GOAL-004-core-data-model](../GOAL-004-core-data-model/00-meta.md) |
| 阶段 4 | 核心方法论、文档协议与 canonical 模板产品化 | 已完成（GOAL-006） | [GOAL-006-core-methodology-template-productization](../GOAL-006-core-methodology-template-productization/00-meta.md) |
| 阶段 5 | Skills 消费适配器与发布一致性 | 快照曾写进行中（**现时：已关门**） | [GOAL-008-skills-consumer-adapter-release-consistency](../GOAL-008-skills-consumer-adapter-release-consistency/00-meta.md) |
| 阶段 6 | Web 人类工作台深化 | 快照曾写未开始（**现时：有界结项**） | GOAL-009 + 012～017 |
| 阶段 7 | 三面一致性、版本化与发布验收 | 快照曾写未开始（**现时：路径 D 下延期未开 · D-024**） | 改道 A 须新契约 |

### 阶段 6 路线图明细（结项后保留 · 现时承接列）

| 顺序 | 阶段 | 目标与退出条件 | 承接 / 现时 |
|------|------|----------------|------------|
| 6A | 产品形态与信息发现 | 明确人类角色、核心工作流、AI 协作边界、成功标准和 required 信息门禁。 | GOAL-009 **有界 done** |
| 6A-P | 跨层工作区与共享资料协议 | 工作区 Root Goal 绑定、串行阶段、共享资料固定引用与 Skills 首先适配。 | GOAL-010 / 011 `done` |
| 6B | 可信读模型与 AI 协作面 | 事实准入、WS/SM 有界验证；AI 运行时有界。 | F-002～004 有界 + GOAL-014 **有界 done**；全文 → R-009-X |
| 6C | 受控变更契约 | 预览/diff、确认、事务/恢复；α CT + 生产双门闩。 | GOAL-013 **有界 done**；GOAL-009 写入 F-007/008 closed；A-030 |
| 6D | 首个端到端工作流（α） | 配置化产品工作区详情 + 受限执行事实追加。 | GOAL-012 **有界 done** |
| 6E | 试点与有界关门评估 | E-α 冒烟；有界 close-out；扩展 residual。 | GOAL-009 E-α + **R-009-X accepted** |
| 6X | 扩展（未宣称终态） | N1 导航、资料 CRUD 产品、人类多会话试点、I 全文 verified、终态宣称。 | **R-009-X**；015～017 有界 done ≠ 终态 |

### 阶段 4 的可执行产品化与退出契约

阶段 4 的最小交付包、canonical 所有者、独立复制场景、版本同步策略、非目标、验收证据和进入阶段 5 的门槛，由 [D-008](01-decision.md#d-008--阶段-4-产品化与退出契约2026-07-19) 定义。GOAL-006 已以 A-005 self close-out 与 A-004 independent targeted 复审完成阶段 4。

### 跨阶段协议修订：信息就绪

[A-004](03-audit.md) 发现的信息就绪协议缺口已由 [GOAL-007-information-readiness-governance](../GOAL-007-information-readiness-governance/00-meta.md) 完成，并由 [A-005](03-audit.md#a-005--响应-a-004--f-004-信息就绪协议缺口2026-07-19) 关闭 F-004。

## 子目标索引（现时）

完整树与 status 以 [goal-tree.md](../goal-tree.md) 为准。**下一编号 GOAL-021**。

| ID | 标题 | 状态 | 作用 |
|----|------|------|------|
| GOAL-002～007 | 初始化 / Skills 实践 / 数据模型 / 闭环 / 核心产品化 / 信息就绪 | done | 阶段 1～4 基线 |
| GOAL-008-skills-consumer-adapter-release-consistency | Skills 消费适配器跨宿主/跨版本发布一致性 | done / 100% | 阶段 5 |
| GOAL-009-ai-assisted-governance-workbench | AI 协助的人类目标治理 Web 工作台 | done / 100%（有界） | 阶段 6 规划 + α/X-AI 台账；**R-009-X** |
| GOAL-010 / 011 | 工作区·共享资料协议；目录迁移 | done / 100% | 跨层协议 + 显式工作区根 |
| GOAL-012～017 | α 切片 / 写入 CT / X-AI / X-NAV / X-SM / X-PILOT | done / 100%（有界） | 阶段 6 有界交付；各 residual 仍挂本目标 |
| GOAL-018-skills-release-packaging | Skills Release 打包与对外安装路径 | done / 100% | 阶段 6 后 **Skills 维护波次**（[D-024](01-decision.md#d-024--a-015-f-008-路径-d仅维护发版协议不关-root2026-07-28)） |
| GOAL-019-skills-consumer-workspace-bootstrap | Skills 消费方工作区骨架（空仓可运行） | done / 100% | 同上 · 消费方 core+scaffold |
| GOAL-020-methodology-adversarial-audit-fix | 核心方法论对抗性审计与纠错 | done / 100% | 路径 D 单点：A～E 完成；D-005/A-005 关门；F-010 recommended follow-up |

### 子目标（历史快照 · 阶段 5 中途）

> **不可作现时。** 下表曾写 GOAL-008 `active / 20%`；现时 GOAL-008 已 `done`。

| ID | 标题 | 快照状态（过时） |
|----|------|------------------|
| GOAL-002～007 | （略） | done |
| GOAL-008-skills-consumer-adapter-release-consistency | Skills 消费适配器跨宿主/跨版本发布一致性 | active / 20%（**过时**） |

## 相关路径

- 树状总览：[../goal-tree.md](../goal-tree.md)
- 文档规范：[../../README.md](../../README.md)
- 核心模板：[../../templates/](../../templates/)
- 架构说明：[../../architecture/](../../architecture/)
- 愿景：[../../vision/charter.md](../../vision/charter.md) · [reviews.md](../../vision/reviews.md)
