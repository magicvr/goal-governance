---
title: Goal Tree · 目标树与进展总览
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.6.0
---

# Goal Tree

> 所有目标平铺存放在本目录；层级仅通过各目标 `00-meta.md` 的 `parent` 字段维护。  
> **新建、修改状态或调整 parent 后，必须同步更新本文件。**

## 树状结构

> 根目标当前采用“三层交付、一个真相源”：核心方法论与模板、Skills 消费适配器、Web 人类工作台。核心 canonical 模板位于 `docs/templates/goal-folder/`；`skills/templates/goal-folder/` 为分发镜像。

```text
GOAL-001-main-vision · 交付可复用的目标治理方法论、文档协议与消费工具 [active]
├── GOAL-002-project-bootstrap · 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） [done 100%]
├── GOAL-003-skills-practice · 完善 Skills 并在本项目中实践验证 [done 100%]
├── GOAL-004-core-data-model · 实现核心数据模型与 Goal 基础管理 [done 100%]
└── GOAL-005-skills-closed-loop-audit · Skills 治理闭环与交叉审计 [done 100%]
```

## 状态总览

| ID | 标题 | Parent | Status | Progress | 路径 |
|----|------|--------|--------|----------|------|
| GOAL-001-main-vision | 交付可复用的目标治理方法论、文档协议与消费工具 | — | active | — | [GOAL-001-main-vision/](GOAL-001-main-vision/) |
| GOAL-002-project-bootstrap | 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） | GOAL-001-main-vision | done | 100% | [GOAL-002-project-bootstrap/](GOAL-002-project-bootstrap/) |
| GOAL-003-skills-practice | 完善 Skills 并在本项目中实践验证 | GOAL-001-main-vision | done | 100% | [GOAL-003-skills-practice/](GOAL-003-skills-practice/) |
| GOAL-004-core-data-model | 实现核心数据模型与 Goal 基础管理 | GOAL-001-main-vision | done | 100% | [GOAL-004-core-data-model/](GOAL-004-core-data-model/) |
| GOAL-005-skills-closed-loop-audit | Skills 治理闭环与交叉审计 | GOAL-001-main-vision | done | 100% | [GOAL-005-skills-closed-loop-audit/](GOAL-005-skills-closed-loop-audit/) |

当前根目标焦点：阶段 4「核心方法论、文档协议与 canonical 模板产品化」；路线图确认后再以 `GOAL-006` 起创建子目标。

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
2. 新目标从现有最大编号 +1 顺序分配（当前下一个：`GOAL-006`）。
3. 文件夹命名：`GOAL-NNN-short-slug`（英文短横线 slug）。
4. 每个目标必须包含：`00-meta.md`、`01-decision.md`、`02-execution.md`、`03-audit.md`、`attachments/`。
