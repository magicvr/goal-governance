---
id: GOAL-004-core-data-model
title: 实现核心数据模型与 Goal 基础管理
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.2.0
progress: 25%
---

# GOAL-004 · 实现核心数据模型与 Goal 基础管理

## 概述

设计并实现 Goal 及关联实体的数据模型，实现 Goal 基础 CRUD，让 Web 应用能操作真实目标数据。承接 [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md) 高层路线图**阶段 3**。

## 范围

### 在范围内

1. Goal 及关联实体（决策 / 执行 / 审计等）的数据模型设计
2. Goal 基础 CRUD：创建、读取、更新、列表
3. Web 首页与目标详情页展示真实目标数据
4. 目标详情页展示决策 / 执行 / 审计的基础信息

### 不在范围内

- 完整「Web 与文档体系双向联动」的高级写回/同步策略（属 GOAL-001 阶段 4）
- 认证 / 多租户 / 独立数据库迁移（除非阶段设计中明确需要且已决策）
- 漂移检测、AI 辅助等高级能力（属 GOAL-001 阶段 5）
- Skills / 提示词包继续深化（属 [GOAL-003-skills-practice](../GOAL-003-skills-practice/00-meta.md)）

## 成功标准

- [x] 完成 Goal 及关联实体的数据模型设计
- [ ] 实现 Goal 的基础 CRUD（创建、读取、更新、列表）
- [ ] Web 应用首页和详情页能展示真实目标数据
- [ ] 实现目标详情页，能看到决策 / 执行 / 审计的基础信息

## 高层路线图（P-001）

> 本目标范围跨模型、读写与 Web 接入，**尚不能直接一次性执行完毕**。先按下列阶段推进；各阶段再按需拆具体子目标，**本回合不批量创建细粒度子目标**。

| 阶段 | 主题 | 状态 | 说明 |
|------|------|------|------|
| 阶段 A | 领域模型与存储约定 | **已完成** | 设计说明：[attachments/domain-model-and-storage.md](attachments/domain-model-and-storage.md)；决策 D-004～D-007 |
| 阶段 B | 读取路径（列表 / 详情） | 未开始 | 从文档体系解析并加载 Goal 及关联信息；服务层可单测或脚本验证 |
| 阶段 C | 写路径（创建 / 更新） | 未开始 | Goal 基础创建与更新；写回约定与校验边界见设计 §6 |
| 阶段 D | Web 接入真实数据 | 未开始 | 首页列表 + 目标详情页展示决策 / 执行 / 审计基础信息；替换骨架占位 |

**先后关系**：A → B → C → D。A 已完成；B 可开工；C 依赖 A 的写约定；D 至少依赖 B（只读展示可先于完整写路径）。

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 相关路径

- 树状总览：[../goal-tree.md](../goal-tree.md)
- 架构概览：[../../architecture/overview.md](../../architecture/overview.md)
- 技术栈：[../../architecture/tech-stack.md](../../architecture/tech-stack.md)
- Web 应用：[../../../web/](../../../web/)
