---
id: GOAL-005-skills-closed-loop-audit
title: Skills 治理闭环与交叉审计
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.2.2
progress: 75%
---

# GOAL-005 · Skills 治理闭环与交叉审计

## 概述

在 [GOAL-003-skills-practice](../GOAL-003-skills-practice/00-meta.md) 已交付的**单一编排主入口**地基上，把 Skills 从「文档推进助手」升级为带**阶段质量意识**与**交叉审计**的治理能力：编排器推进生命周期并**响应全部审计意见**；独立审计入口专责交叉审查以防自证幻觉；冲突与「是否自审」等裁决交由用户，编排器提供建议。

承接 [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md) 双交付中的 Skills 线；与 [GOAL-004-core-data-model](../GOAL-004-core-data-model/00-meta.md)（数据/Web）并行，互不阻塞。

## 范围

### 在范围内

1. **原则定稿**：交叉审计、意见响应、用户裁决（自审可选 / 冲突必问）等写入 principles / AGENTS（表述可迭代）
2. **编排器（`00` / `/govern`）**：汇总 self + independent 意见；有独立无自审时**询问**是否自审；意见冲突时**提示用户决策并给建议**；按用户确认响应修正 / 复审 / 推进
3. **审计原语（`04`）增强**：最小意见结构（如 source、verdict、findings、必改项）；区分自审与独立审
4. **可选独立入口 `/audit`**：交叉审计、默认只出意见不改状态；可交回编排器闭环
5. **安装与文档**：主入口仍为 `/govern`；`/audit` 安装策略明确（默认或可选）
6. **实践验证**：至少一轮真实会话压测（门禁意识 + 交叉审计 + 冲突/自审问询）

### 不在范围内

- 自动判定「可否跳过自审」的复杂机制（revision 指纹、覆盖度算法等）— **延后**
- Web UI 审计工作流 / 数据模型改造（属 GOAL-004 及后续）
- 重开或改写 GOAL-003 历史结项标准与已关门审计正文
- 法律意义上的第三方独立证明；单 AI 场景仅保证意图/入口分离级的交叉审查
- Marketplace 完整包、独立 Agent 运行时

## 成功标准

- [x] 原则（或 AGENTS 等价节）写明：交叉审计、编排器响应全部开放意见、冲突用户裁决、有独立无自审时询问是否自审
- [x] `00-govern-orchestrator`（及 `/govern` 入口）实现上述用户裁决点与意见汇总/响应路径
- [x] `04-write-audit` 支持最小审计意见结构，并能标注 `self` / `independent`
- [x] 独立交叉审计路径可用（独立 skill/slash 或明确 advanced 流程），默认不直接改目标 status
- [x] 安装与 README/prompts 说明与产品面一致（单主入口 + 可选/独立审计）
- [x] 至少一次书面实践记录：覆盖「独立审计 → 编排器响应」或「冲突提示用户」之一（A-002 → D-008 / A-003）

## 高层路线图

> P-001：范围偏大，先按阶段推进；细子目标仅在阶段需要时再拆。

| 阶段 | 主题 | 状态 | 说明 |
|------|------|------|------|
| A | 原则与产品语义定稿 | **已完成** | P-002～P-004 + 落盘 + 开放必改门禁；A-002～A-005 |
| B | 提示词与入口 | **已完成** | A-007 conditional 已响应；F-017 **独立复审确认**（A-009/A-010） |
| C | 安装与文档同步 | **基本完成**（并入 B） | README v0.5.1 与默认分发一致 |
| D | 实践验证与关门审计 | **进行中** | **含 F-018**；正式压测 → 关门审计；见 A-010 |

## 与 GOAL-003 的关系

| 项 | 说明 |
|----|------|
| 继承 | 单一主入口 `/govern`、01–04 原语分层、安装与 AGENTS 地基 |
| 升级 | 门禁意识与闭环响应、交叉审计 `/audit`、多意见冲突裁决 |
| 历史 | GOAL-003 保持 `done`；不回写其成功标准 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 相关路径

- 编排器：`skills/prompts/00-govern-orchestrator.md`
- 审计原语：`skills/prompts/04-write-audit.md`
- 交叉审计：`skills/prompts/05-independent-audit.md`
- 原则：`docs/architecture/principles.md`（P-001～P-004）
- 规则：`AGENTS.md` / `skills/AGENTS.template.md`（§6 / §6b / §9b）
