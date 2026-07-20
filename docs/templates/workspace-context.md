---
id: example-workspace
title: 示例工作区
status: active
root_goal: GOAL-001-example-root
canonical_scope: docs/goals/
shared_materials_catalog: https://example.invalid/shared-materials/
created: 2026-07-20
updated: 2026-07-20
version: 0.1.0
---

# 工作区上下文 · 示例工作区

> 从本模板复制为 `docs/workspace.md`，再替换示例字段。工作区绑定一个 Root Goal 与一个 canonical 范围；它不替代 `docs/goals/`、`goal-tree.md` 或目标五件套的状态真相。

## 绑定

| 字段 | 当前值 | 说明 |
|------|--------|------|
| 工作区 ID | `example-workspace` | 与所有共享资料引用的 `workspace_id` 一致。 |
| Root Goal | `GOAL-001-example-root` | 必须存在，且其 `parent: null`。 |
| canonical 范围 | `docs/goals/` | 当前工作区唯一的目标状态范围。 |
| 共享资料目录 | `https://example.invalid/shared-materials/` | 固定路径/URI，或 `none`；不在此文档保存资料内容。 |

## 固定共享资料引用

> 当 `shared_materials_catalog: none` 时，此表必须为空。缺 `material_id`、`source`、`version`、64 位十六进制 `sha256` 或匹配 `workspace_id` 的行无效，不能作为事实、证据或跨工作区上下文来源。

| reference_id | workspace_id | material_id | source | version | sha256 | purpose | local_record | status |
|--------------|--------------|-------------|--------|---------|--------|---------|--------------|--------|
| `<REF-001>` | `example-workspace` | `<MATERIAL-001>` | `<path-or-uri>` | `<version>` | `<64-hex-sha256>` | `<why this workspace uses it>` | `none` | active |

## 串行阶段说明（按需）

本工作区的 MVP、后续阶段和扩展目标应写在 Root Goal 路线图中，并以串行子目标承接。只有长期目的、成功边界或战略方向实际变化时，才在决策留痕后修改 Root Goal 定义。

## 备注

> 本模板只定义工作区上下文和共享资料固定引用。资料物理存储、用户 CRUD、AI 读取执行、跨工作区导航和 Web 写入仍须在相应消费适配器的门禁内定义与验证。
