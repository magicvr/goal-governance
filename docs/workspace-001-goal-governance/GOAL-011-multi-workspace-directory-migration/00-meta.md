---
id: GOAL-011-multi-workspace-directory-migration
title: 完成多工作区目录迁移与共享资料索引骨架
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-20
version: 0.2.0
progress: 100%
---

# GOAL-011 · 完成多工作区目录迁移与共享资料索引骨架

## 概述

将当前仓库从单一 `docs/goals/` 根迁移到显式工作区根 `docs/workspace-001-goal-governance/`。每个工作区在其根内直接保存 `workspace.md`、`goal-tree.md` 和平铺的 `GOAL-*` 五件套；`docs/shared-materials/` 与工作区并列，保存用户手动复制资料后的候选索引，不保存目标状态。

## 成功标准

- [x] 当前所有目标和 `goal-tree.md` 已迁移到 `workspace-001-goal-governance/`，没有并行的 `docs/goals/` 真相源。
- [x] 工作区上下文、核心协议、模板、Skills 和 Web 默认读取根都使用工作区 canonical scope，并保留外部旧仓库的明确 legacy 识别边界。
- [x] `docs/shared-materials/` 骨架存在；用户手工复制文件后可用脚本重建稳定的路径、大小和 SHA-256 候选索引。
- [x] 索引不会把资料自动升级为事实、证据、固定引用或跨工作区上下文。
- [x] 迁移后的核心、Skills、脚本和 Web 回归测试通过；历史证据路径可重新解析。

## 高层路线图

| 阶段 | 主题 | 状态 | 退出条件 |
|------|------|------|----------|
| A | 拓扑与迁移契约 | 已完成 | D-001 明确 workspace 根、共享资料根、legacy 边界和非目标。 |
| B | canonical 记录迁移 | 已完成 | 现有目标树、五件套和工作区上下文位于 `workspace-001-goal-governance/`，不存在全局 `docs/goals/` 镜像。 |
| C | 消费者与索引工具适配 | 已完成 | core/Skills/Web 默认路径、资料索引脚本与测试对新拓扑一致。 |
| D | 验证与关门审视 | 已完成 | 迁移、索引、路径安全和回归测试可复现；A-001 无开放 required finding。 |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 现有 `docs/goals/` 如何迁为单一 `workspace-001-goal-governance/` canonical scope，同时保持目标平铺、Root Goal 和历史路径可核对？ | 阶段 B 迁移 | 阶段 B 结束前 | 迁移目录，检查五件套、goal-tree、相对链接和消费适配器路径。 | verified | 无延期；GOAL-011 负责。 | 当前工作区根、`workspace.md`、10 个既有目标和 GOAL-011 均已存在；`docs/tests/test_workspace_protocol.py` 的实际迁移断言通过。 |
| I-002 | required | 手动复制到共享资料根的文件如何被稳定索引，而不伪造 `material_id`、版本、用途、固定引用或 canonical 事实？ | 阶段 C 索引工具 | 阶段 C 结束前 | 定义候选清单格式、路径 containment、排除项、SHA-256 和确定性测试。 | verified | 无延期；GOAL-011 负责。 | `scripts/rebuild_shared_materials_index.py` 与 6 项索引测试通过；当前 `index.json` 为 0 条候选库存。 |
| I-003 | required | core、Skills、Web、安装/standalone、测试与历史证据如何从固定 `docs/goals/` 迁移到工作区根而不产生双真相或静默越界？ | 阶段 C 验证 | 阶段 C 结束前 | 更新所有受影响表面；运行核心、Skills、脚本和 Web 测试。 | verified | 无延期；GOAL-011 负责。 | docs 10 项、Skills 32 项、scripts 36 项和 Web 21 项回归测试通过；`git diff --check` 通过。 |
| I-004 | non-blocking | 多工作区动态发现、工作区创建/归档、平台级导航和 Web 选择器应如何实现？ | GOAL-009 路线图 B/D | 后续产品目标立项前 | 由 GOAL-009 I-009/I-010/I-004 收集产品模型和跨工作区验证。 | open | 不阻断本目录迁移；进入 Web 多工作区实现前复核。 | 本目标只建立目录/协议与单一现有工作区的读取根。 |

## 边界

- 不为 `docs/goals/` 保留永久兼容镜像；旧外部仓库只能作为明确的 legacy 单工作区格式识别。
- 不实现工作区列表 UI、动态选择器、资料上传/删除 API、AI 读取执行、受控 Web 写入或跨工作区导航。
- 不把共享资料索引当成资料版本、用户确认、固定引用或目标证据；这些仍由 GOAL-009 的开放门禁治理。

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
