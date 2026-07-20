---
title: Goal Tree · 目标树与进展总览
status: active
created: 2026-07-18
updated: 2026-07-20
parent: null
version: 0.19.0
---

# Goal Tree

## 2026-07-20 · 阶段 6 Web 工作台规划

GOAL-009 启动 AI 协助的人类目标治理工作台的产品定义与信息发现。它不把只读浏览器定义为产品终态，也尚未授权 Web 写入、AI 服务或部署；`docs/goals/` 继续是 canonical 真相源。本目标将先定义人类确认、AI 提案、可审计变更、安全与证据如何成立，再进入实现。

## 2026-07-20 · 工作区与共享资料区核心协议

GOAL-010 已完成跨层的核心协议与 Skills 首先适配：它把一个工作区绑定一个 Root Goal 与 canonical 范围，并定义共享资料固定引用的文档边界。它只为 GOAL-009 的 R-003 提供输入，不关闭其 F-003/F-004、I-009/I-010 或放行 Web 阶段；Web 的物理存储、用户 CRUD、AI 执行和跨工作区产品验证仍由 GOAL-009 及后续实现目标负责。

> 所有目标平铺存放在本目录；层级仅通过各目标 `00-meta.md` 的 `parent` 字段维护。  
> **新建、修改状态或调整 parent 后，必须同步更新本文件。**

## 树状结构

> 根目标当前采用“三层交付、一个真相源”：核心方法论与模板、Skills 消费适配器、Web 人类工作台。核心 canonical 模板位于 `docs/templates/goal-folder/`；`skills/templates/goal-folder/` 为分发镜像。阶段 5 已按 D-010 由 GOAL-008 承接。

```text
GOAL-001-main-vision · 交付可复用的目标治理方法论、文档协议与消费工具 [active]
├── GOAL-002-project-bootstrap · 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） [done 100%]
├── GOAL-003-skills-practice · 完善 Skills 并在本项目中实践验证 [done 100%]
├── GOAL-004-core-data-model · 实现核心数据模型与 Goal 基础管理 [done 100%]
├── GOAL-005-skills-closed-loop-audit · Skills 治理闭环与交叉审计 [done 100%]
├── GOAL-006-core-methodology-template-productization · 核心方法论、文档协议与 canonical 模板产品化 [done 100%]
├── GOAL-007-information-readiness-governance · 信息就绪与未知项治理 [done 100%]
├── GOAL-008-skills-consumer-adapter-release-consistency · Skills 消费适配器跨宿主/跨版本发布一致性 [done 100%]
├── GOAL-009-ai-assisted-governance-workbench · 规划 AI 协助的人类目标治理 Web 工作台 [active 0%]
└── GOAL-010-core-workspace-shared-materials-protocol · 建立工作区与共享资料区核心协议，并完成 Skills 首先适配 [done 100%]
```

## 状态总览

| ID | 标题 | Parent | Status | Progress | 路径 |
|----|------|--------|--------|----------|------|
| GOAL-001-main-vision | 交付可复用的目标治理方法论、文档协议与消费工具 | — | active | — | [GOAL-001-main-vision/](GOAL-001-main-vision/) |
| GOAL-002-project-bootstrap | 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） | GOAL-001-main-vision | done | 100% | [GOAL-002-project-bootstrap/](GOAL-002-project-bootstrap/) |
| GOAL-003-skills-practice | 完善 Skills 并在本项目中实践验证 | GOAL-001-main-vision | done | 100% | [GOAL-003-skills-practice/](GOAL-003-skills-practice/) |
| GOAL-004-core-data-model | 实现核心数据模型与 Goal 基础管理 | GOAL-001-main-vision | done | 100% | [GOAL-004-core-data-model/](GOAL-004-core-data-model/) |
| GOAL-005-skills-closed-loop-audit | Skills 治理闭环与交叉审计 | GOAL-001-main-vision | done | 100% | [GOAL-005-skills-closed-loop-audit/](GOAL-005-skills-closed-loop-audit/) |
| GOAL-006-core-methodology-template-productization | 核心方法论、文档协议与 canonical 模板产品化 | GOAL-001-main-vision | done | 100% | [GOAL-006-core-methodology-template-productization/](GOAL-006-core-methodology-template-productization/) |
| GOAL-007-information-readiness-governance | 信息就绪与未知项治理 | GOAL-001-main-vision | done | 100% | [GOAL-007-information-readiness-governance/](GOAL-007-information-readiness-governance/) |
| GOAL-008-skills-consumer-adapter-release-consistency | Skills 消费适配器跨宿主/跨版本发布一致性 | GOAL-001-main-vision | done | 100% | [GOAL-008-skills-consumer-adapter-release-consistency/](GOAL-008-skills-consumer-adapter-release-consistency/) |
| GOAL-009-ai-assisted-governance-workbench | 规划 AI 协助的人类目标治理 Web 工作台 | GOAL-001-main-vision | active | 0% | [GOAL-009-ai-assisted-governance-workbench/](GOAL-009-ai-assisted-governance-workbench/) |
| GOAL-010-core-workspace-shared-materials-protocol | 建立工作区与共享资料区核心协议，并完成 Skills 首先适配 | GOAL-001-main-vision | done | 100% | [GOAL-010-core-workspace-shared-materials-protocol/](GOAL-010-core-workspace-shared-materials-protocol/) |

当前根目标已完成阶段 5「Skills 消费适配器与发布一致性」：GOAL-008 为 `done / 100%`，I-001～I-003 与上游 `F-005` 均有关闭证据。候选 commit `8a33ecd21d9183a680c9c0d63e471469f5e515a8` 由 GitHub Actions run `29700051047` 在 Ubuntu/Windows 重放，annotated `v0.7.0` 与 release-candidate summary 相互绑定；Copilot 证据只来自 GitHub Copilot CLI，不使用 VS Code 插件。GOAL-010 已以 `done / 100%` 交付工作区/共享资料固定引用协议和 Skills 首先适配；其新行为将在下次发布前触发 GOAL-008 runtime evidence 刷新。阶段 6 现由 GOAL-009 规划 AI 协助的人类工作台，而非完善纯只读页面；GOAL-001 仍为 `active`，`F-006` 保持非阻塞 `recommended / open`，`GOAL-006` 的 F-003 保持非阻塞 recommended/open residual。

## 状态图例

| Status | 含义 |
|--------|------|
| `draft` | 草稿，尚未正式启动 |
| `active` | 进行中 |
| `blocked` | 阻塞 |
| `done` | 已完成 |
| `cancelled` | 已取消 |

## 编号规则速查

1. `GOAL-001` 固定为 Root Goal（`parent: null`）。
2. 新目标从现有最大编号 +1 顺序分配（当前下一个：`GOAL-011`）。
3. 文件夹命名：`GOAL-NNN-short-slug`（英文短横线 slug）。
4. 每个目标必须包含：`00-meta.md`、`01-decision.md`、`02-execution.md`、`03-audit.md`、`attachments/`。
