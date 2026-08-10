---
id: GOAL-016-shared-materials-product
title: 实现共享资料区产品（CRUD / 固定引用 / 隔离）
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.1
progress: 100%
planning_source: GOAL-009-ai-assisted-governance-workbench
expansion_code: X-SM
residual_source: R-009-X
---

# GOAL-016 · 实现共享资料区产品（CRUD / 固定引用 / 隔离）

## 有界关门（2026-07-22）

本目标 `done / 100%` 关闭的是 **有界 X-SM 范围**（A-007；独立复审 [A-008](03-audit.md#a-008--独立交叉审计-close-out2026-07-22)；推荐项 [A-009](03-audit.md#a-009--响应-a-008关闭-f-001f-0032026-07-22)）。**不**构成：

1. GOAL-009 I-010 **整项** `verified` 或取消 **R-009-X**。  
2. 阶段 6 终态 / Root 关门。  
3. AI 读资料运行时（**R-016-AI-READ**）。  
4. 浏览器 DOM 全矩阵（**R-016-E2E**）。  
5. 高级列表 UX、**Web 对已有 material 追加版本**（**R-016-UX**；service 支持 `material_id=` 追加）。  
6. 将 ref 写入各区 `workspace.md` 协议表 / 强制 protocol `source` 字段（产品权威 = `shared-materials/refs/`；见 R-016-A §3.1）。  
7. 物理粉碎法证级删除、多用户 ACL、跨实例共享。

## Residual（关门时）

| ID | 残余 | 复审触发 | 状态 |
|----|------|----------|------|
| **R-016-AI-READ** | AI 读资料运行时 | 宣称 AI 读资料产品前 | **accepted** |
| **R-016-E2E** | 浏览器 DOM 全矩阵 / 人类多会话资料 UX | 宣称 UI 全矩阵或试点放行前 | **accepted** |
| **R-016-UX** | 分页/搜索/预览；**Web 对已有 material 追加版本**（上传表单传 material_id） | 扩大体验验收前 | **accepted** |

## 成功标准

- [x] 有界范围交付 + residual 书面 · D-006 / A-007  
- [x] 回归 **142 passed, 1 skipped**  

## 高层路线图

| 阶段 | 状态 |
|------|------|
| A–E | **完成**（有界关门） |

## 交付索引

| 模块 | 路径 |
|------|------|
| 边界 | `attachments/r-016-a-shared-materials-boundary.md`（v1.0.1 勘误） |
| Store | `web/services/materials_store.py` · refs=`shared-materials/refs/{workspace_id}.json` |
| Web | `main.py`、`templates/materials.html` |
| 测试 | `test_materials_*.py` |

## 信息就绪（完整字段 · A-009 / F-002）

| ID | 级别 | 问题 | 影响门禁 | 最晚阶段 | 验证 | 状态 | 证据 |
|----|------|------|----------|----------|------|------|------|
| I-001 | required | 字节存储位置 | 方案冻结 | A | R-016-A §3 | **verified** | `{DATA_ROOT}/shared-materials/` · D-002 |
| I-002 | required | 版本/sha256 | 实现 B | B | put_bytes | **verified** | `materials_store` · D-003 · `test_materials_store` |
| I-003 | required | 删除前引用检查 | 删除 | B/D | SM-005 | **verified** | delete_material · stage_d |
| I-004 | required | AI 读范围 | AI 读 | A/D | 裁决 residual | **residual** | **R-016-AI-READ** · D-005 |
| I-005 | non-blocking | 列表 UX / Web 追加版本 | 体验 | 试点 | residual | **residual** | **R-016-UX** |
| I-006 | non-blocking | N1 焦点衔接 | 引用 | C | attach 焦点 | **verified（有界）** | `/materials/attach` · refs 按 workspace_id 隔离 |

## 父目标

GOAL-001 · GOAL-009（R-009-X / X-SM）
