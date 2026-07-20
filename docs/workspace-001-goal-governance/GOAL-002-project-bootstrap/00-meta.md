---
id: GOAL-002-project-bootstrap
title: 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向）
status: done
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.1.0
progress: 100%
---

# GOAL-002 · 完成项目初始化

## 概述

在总目标 [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md) 下，完成仓库可协作的最小基础：

1. 文档体系（目标结构、索引、规范）
2. Web 应用基础框架
3. Skills / 提示词方向约定

## 范围

### 已完成

- 技术栈选定：FastAPI + Jinja2 + Tailwind CSS + HTMX
- Web 应用基础骨架（首页 + 决策/执行/审计占位页）
- Web 应用收纳至 `web/` 子目录
- 文档结构定为「目标中心 + 决策/执行/审计」
- 层级管理定为「扁平存储 + goal-tree.md」
- 双交付形态确认：Web + Skills/提示词
- 首批目标 GOAL-001 / GOAL-002 五件套与 `goal-tree.md` 落地
- `docs/README.md`、`AGENTS.md`、根 `README.md` 与架构文档固化
- Skills 基础结构落地：`skills/`（README、AGENTS 模板、目标文件夹模板）

### 移出本目标范围（后续子目标）

- 可安装的具体 Skill 包 / 自动化提示词脚本
- Web 与 `docs/goals` 的数据联动
- 自动化校验（编号、parent、goal-tree 一致性）

## 成功标准

- [x] Web 可本地启动并访问三个模块页
- [x] 文档核心规则已书面确认
- [x] 目标目录符合规范且 GOAL-001/002 齐全
- [x] `goal-tree.md` 与 `AGENTS.md` 可指导后续协作
- [x] 架构文档记录当前技术栈与目录约定
- [x] Skills 基础结构可复用（`skills/` + 模板 + 使用说明）

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
