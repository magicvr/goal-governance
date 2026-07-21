---
id: GOAL-012-first-slice-workspace-detail
title: 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内）
status: done
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.5.0
progress: 100%
planning_source: GOAL-009-ai-assisted-governance-workbench
---

# GOAL-012 · 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内）

## 概述

承接 [GOAL-009](../GOAL-009-ai-assisted-governance-workbench/00-meta.md) 路线图 D / D-006 / D-011 路径 α：在 **Web** 中实现「配置选中的**产品工作区**详情（目标树核心）+ 用户提供候选执行事实 + 门禁内的受限 `append-execution-fact`」。

本目标**不是**完善只读浏览器终态；也**不是**多工作区总览、共享资料 CRUD、AI 接入或 SQLite 必选。发布物与 dogfood 分栏遵守 D-011。

## 成功标准

- [x] Web 通过**显式配置**绑定数据根 / 工作区路径；默认**不**静默加载本仓 dogfood；开发可用显式开关
- [x] 工作区详情以目标树为核心，只读展示所选产品工作区内目标的 canonical 上下文（与计算视图区分）
- [x] 用户可提交 `user-provided` 候选执行事实，形成受限提案 diff（写集仅目标 `02-execution.md` 追加）
- [x] Service 级契约覆盖 R-004 **关键路径**（非 CT-001～018 全矩阵）：隔离合成 fixture 上可运行正反测试（成功追加 + missing/source/write-set/drift/open-finding/split/prod-gate/幂等/digest mismatch 等）
- [x] **生产路径**上的 `decide_and_execute` 在产品门禁默认开放时拒绝写入（含 HTTP decide 负向）；测试可单独授权
- [x] 无 AI 调用、无共享资料 CRUD、无跨工作区 N1 列表产品化、无 SQLite 依赖；receipt 在 `ops/receipts/` 非五件套
- [x] 发布/安装说明写明：不含本仓过程树；合成 fixture 不使用真实 GOAL-001～011 过程数据当客户样例；幂等语义见 README（**CT-007 持久化已由 GOAL-013 补齐**，见 A-004）

## 交付要点

| 模块 | 路径 |
|------|------|
| 配置 fail-closed | `web/services/workspace_config.py` |
| 受控变更 | `web/services/controlled_change.py` |
| Web 入口 | `web/main.py`、模板 `index.html` / `goal_detail.html` |
| 合成 fixture | `web/tests/fixtures/r004/workspace-ok/`（`GOAL-001-fixture-target`） |
| 测试 | `test_workspace_config.py`、`test_controlled_change.py`、扩展 `test_main.py` |
| 文档 | `web/README.md`、`web/.env.example` |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 配置键名、默认 fail-closed、DEV_DOGFOOD | 实现启动 | 编码前 | README / .env.example | verified | 无 | 见 README 配置表 |
| I-002 | required | CT fixture 与运行命令 | 契约测试验收 | 首次 CT 合并前 | unittest | verified | 无 | `python -m unittest discover -s tests -v` |
| I-003 | required | 生产写入启用检查清单 | 开放生产写入 | 启用前 | README 清单 + 环境门禁 | collecting | 待 GOAL-009 F-007/F-008 | 默认仍阻断；清单见 web/README |
| I-004 | non-blocking | 详情页 UX | 试点 | 试点前 | 模板迭代 | open | 试点 | 基础表单已有 |
| I-005 | non-blocking | 跨进程幂等/receipt 恢复（A-001 F-003） | 生产写入放行 | 启用生产写入前 | 持久化 operation 索引 + 跨重启 CT | verified | 无 | GOAL-013 阶段 B + [A-004](03-audit.md#a-004--回写关闭-f-003-residualct-007-持久化2026-07-21)；`test_durable_idempotent_replay_new_service_instance` |

## 依赖与门禁

- 生产 Web 写入仍受 GOAL-009 F-007/F-008 与 I-003/I-004/I-006 阻断（`PRODUCT_GATES_OPEN` 默认 true）。
- 打包：实现与文档遵守 D-011。

## 有界关门（2026-07-21）

本目标已 `done / 100%`，关闭的是 **α 实现范围**（见成功标准与 [A-003](03-audit.md#a-003--有界关门审计-close-out2026-07-21)）。**不**构成：

1. 生产 Web/AI 写入放行（I-003 仍 `collecting`；GOAL-009 F-007/F-008 仍 open）。
2. CT-001～018 全矩阵 `verified` 或 GOAL-009 I-003/I-004/I-006 `verified`。

**后置回写（2026-07-21 A-004）**：关门时登记的 F-003 / I-005 **accepted-residual（进程内幂等）** 已由 GOAL-013 阶段 B 证据关闭；**不**因此开放生产写入或关闭 GOAL-009 F-008。

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 规划来源

- [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md)
