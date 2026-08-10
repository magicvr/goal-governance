---
id: GOAL-015-n1-workspace-navigation
title: 实现 N1 多工作区导航（列表 / 选择 / 归档）
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.1
progress: 100%
planning_source: GOAL-009-ai-assisted-governance-workbench
expansion_code: X-NAV
residual_source: R-009-X
---

# GOAL-015 · 实现 N1 多工作区导航（列表 / 选择 / 归档）

## 有界关门（2026-07-22）

本目标 `done / 100%` 关闭的是 **有界 X-NAV / N1 导航范围**（见成功标准与 [A-007](03-audit.md#a-007--有界关门审计-close-out2026-07-22)；独立复审 [A-008](03-audit.md#a-008--独立交叉审计-close-out2026-07-22)；推荐项响应 [A-009](03-audit.md#a-009--响应-a-008关闭-f-001f-0032026-07-22)）。**不**构成：

1. GOAL-009 I-009 **整项** `verified` 或取消 **R-009-X**。  
2. 阶段 6 Web 产品终态 / Root 关门。  
3. 浏览器 DOM 全矩阵 E2E（**R-015-E2E** residual）。  
4. Web 表单「新建工作区」完整 UX（**service** `create_workspace` 已交付；**Web 表单** = **R-015-CREATE-UI** residual；R-015-A §1.1 已勘误）。  
5. 物理删除工作区、共享资料入口（X-SM）、多用户权限。

## 概述

承接 GOAL-009 **R-009-X** / **X-NAV**：平台级最小导航（列表 / 选择 / 归档索引 / service 有界创建），无第二真相源、跨区 fail closed。

| 阶段 | 产物 |
|------|------|
| A | [R-015-A](attachments/r-015-a-n1-navigation-boundary.md) |
| B | `web/services/workspace_registry.py` |
| C | `workspace_binding.py` + `/workspaces` 选择 + focus cookie |
| D | 归档 UX + 跨区负向矩阵 |
| E | 阶段审 + 有界关门 |

## 成功标准

- [x] 冻结 N1 范围与白名单 — R-015-A / D-002  
- [x] 注册/发现 service — D-003  
- [x] Web 列表 / 选择；详情与写路径跟焦点 — D-004  
- [x] 归档 HTTP/UX（不删 canonical；归档清焦点 cookie）— D-005  
- [x] 跨区拒绝可测 — D-005  
- [x] 无第二真相源 — 列表仅 N1  
- [x] unittest 回归 — **126 passed, 1 skipped**（E 关门复跑）  
- [x] 有界关门 — D-006 / A-007；**≠** GOAL-009 I-009 全文 verified  

## 高层路线图

| 阶段 | 主题 | 状态 |
|------|------|------|
| A | 范围与白名单冻结 | **完成** |
| B | 注册/发现 + 隔离 service | **完成** |
| C | Web 列表/选择 + 焦点绑定 | **完成** |
| D | 归档 UX + 负向矩阵 | **完成** |
| E | 阶段审 / 有界关门 | **完成** · A-006 + A-007 |

## 交付索引

| 模块 | 路径 |
|------|------|
| 边界 | `attachments/r-015-a-n1-navigation-boundary.md` |
| Registry | `web/services/workspace_registry.py` |
| 绑定 | `web/services/workspace_binding.py` |
| HTTP/UI | `web/main.py`、`templates/workspaces.html` |
| 测试 | `test_workspace_registry.py`、`test_workspace_binding.py`、`test_workspace_stage_d.py` |

## Residual（关门时）

| ID | 残余范围 | 复审触发 | 状态 |
|----|----------|----------|------|
| **R-015-E2E** | 浏览器 DOM 全矩阵 / 真实多会话人类导航试点 | 宣称 UI 全矩阵验收或人类多会话试点放行前 | **accepted** |
| **R-015-CREATE-UI** | Web 表单新建工作区（**service 已交付**；HTTP/表单未交付） | 产品要求浏览器内一键建区前 | **accepted** |

## 信息就绪（完整字段 · A-009 / F-002）

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚阶段 | 验证 / 收集 | 状态 | 证据 / 结论 |
|----|------|-----------------|----------|----------|-------------|------|-------------|
| I-001 | required | N1 白名单与禁止字段 | 方案冻结 | A | R-015-A §3 + 用户推进 A | **verified（边界）** | R-015-A；D-002；`to_n1_dict` / `validate_n1_list_row` |
| I-002 | required | 注册/发现/创建/归档拓扑 | 实现 B | B | service + tests | **verified（service）** | `workspace_registry.py`；D-003；`test_workspace_registry.py` |
| I-003 | required | 当前工作区 Web 绑定 | 实现 C | C | cookie/query + fail closed | **verified（Web 绑定）** | `workspace_binding.py`；D-004；`test_workspace_binding.py` |
| I-004 | required | 跨区拒绝 CT 集合 | 验收 D | D | HTTP + service 矩阵 | **verified（负向）** | `test_workspace_stage_d.py`；D-005 |
| I-005 | non-blocking | 创建是否纳入本目标 | 范围 A | A | 裁决 | **closed** | **service 有界创建纳入**；Web 表单 → **R-015-CREATE-UI**（非 I 开放） |
| I-006 | non-blocking | 与共享资料入口关系 | 与 X-SM | A | 书面非目标 | **closed** | R-015-A §1；→ X-SM / R-009-X |

## 父目标 / 规划来源

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)  
- [GOAL-009](../GOAL-009-ai-assisted-governance-workbench/00-meta.md)（R-009-X / X-NAV）  
