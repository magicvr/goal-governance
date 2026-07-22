---
id: GOAL-014-ai-collaboration-runtime
title: 实现 AI 协作运行时与用户确认链（有界）
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.0
progress: 100%
planning_source: GOAL-009-ai-assisted-governance-workbench
expansion_code: X-AI
---

# GOAL-014 · 实现 AI 协作运行时与用户确认链（有界）

## 有界关门（2026-07-22）

本目标 `done / 100%` 关闭的是 **有界 X-AI 范围**（见成功标准与 [A-006](03-audit.md#a-006--有界关门审计-close-out2026-07-22)）。**不**构成：

1. GOAL-009 关门或 AI 成功标准自动勾选（仍须 GOAL-009 / R-E-3-X 裁决）。  
2. 网络检索/敏感工具（D-006 明确不做）。  
3. 浏览器 DOM 全矩阵或真实提供方生产联调（**R-014-E2E** accepted residual）。  
4. 默认开启 AI（仍 `AI_ENABLED=false`）。

## 概述

有界 AI 协作运行时：`.env` 配置、用户触发候选、FA 确认后生成受限提案、decide 才写 canonical。

## 成功标准

- [x] 冻结 AI 运行时边界 — R-014-A / D-002
- [x] 配置加载与 broker 骨架 — D-003 / A-002
- [x] 用户触发调用 + 候选展示 — 阶段 C UI/API
- [x] 确认/拒绝入口；未确认不进 canonical — confirm/reject + decide 分离
- [x] 与 `fact_admission` 热路径一致 — confirm 调用 FA；digest 陈旧拒绝
- [x] 不默认开放工具/网络 — 仅 completion；**本目标不做**检索/敏感工具（D-006）
- [x] 无第二真相源；密钥不进 HTML/health
- [x] 正反测试：禁用 fail closed；confirm 提案；stale digest；回归 **102 passed, 1 skipped**

## 高层路线图

| 阶段 | 主题 | 状态 |
|------|------|------|
| A | 边界冻结 | **完成** |
| B | 配置 + broker | **完成** |
| C | 候选 API/UI + 确认链 | **完成** |
| D | 工具同意与降级 | **有界退出（不做）** · R-014-D closed |
| E | 验收与阶段审 / 有界关门 | **完成** · A-004 阶段审 + A-006 有界关门 |

## 交付索引

| 模块 | 路径 |
|------|------|
| 边界 | `attachments/r-014-a-runtime-boundary.md` |
| 配置 | `web/services/ai_config.py` |
| Broker | `web/services/ai_broker.py` |
| 候选链 | `web/services/ai_candidates.py` |
| HTTP/UI | `web/main.py`、`templates/goal_detail.html` |
| 测试 | `web/tests/test_ai_*.py`、`test_main.py` AI 用例 |

## Residual（关门时）

| ID | 范围 | 状态 |
|----|------|------|
| R-014-D | 检索/敏感工具 | **closed**（不做） |
| **R-014-E2E** | 浏览器 E2E / 真实提供方联调 | **accepted residual**（A-006）；复审：宣称 UI 全矩阵验收或生产真联调前 |

## 父目标 / 规划来源

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
- [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md)
