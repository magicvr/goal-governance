---
id: GOAL-013-write-gate-ct-durable-idempotency
title: 补齐受控写入 CT 缺口与跨进程幂等（生产门禁默认仍关）
status: done
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.5.0
progress: 100%
planning_source: GOAL-009-ai-assisted-governance-workbench
---

# GOAL-013 · 补齐受控写入 CT 缺口与跨进程幂等（生产门禁默认仍关）

## 概述

承接 [GOAL-009 A-020](../GOAL-009-ai-assisted-governance-workbench/03-audit.md#a-020--goal-012-证据吸收与-f-007f-008-缺口清单2026-07-21) 与 [GOAL-012](../GOAL-012-first-slice-workspace-detail/00-meta.md) 有界关门后的 **F-007/F-008 关闭前缺口**：在 **生产门禁默认仍开放（写入仍拒绝）** 的前提下，补齐 CT-001～018 缺口用例、跨进程幂等/receipt 恢复，以及 A-020 列出的部分覆盖项，使 GOAL-009 具备将 I-003/I-004/I-006 标 `verified` 并关闭 F-007/F-008 的**可核对运行证据**（关闭本身仍由 GOAL-009 台账与用户审视完成）。

本目标**不是**开放生产写入、**不是** AI 接入、**不是** N1/共享资料 CRUD、**不是**关闭 F-002～F-004。

## 成功标准

- [x] **跨进程幂等（GOAL-012 F-003 residual）**：`decide_and_execute` 成功后 receipt 落盘；新进程/新 service 实例可用同一 `operation_id` + 相同 `proposal_digest` 重放并返回同一结果，**不**重复写入 canonical
- [x] **CT 缺口用例可运行**（F-007 向）：CT-001/003/006/012/014/015 + CT-008 完整 + CT-009/010/011（阶段 D）
- [x] **F-008 恢复/联动证据子集**：CT-010（recovery_pending 与受控路径集成）与 CT-011（不可复核禁止显示成功）有专用负向测试；CT-009 仅覆盖 process-local 并发锁，跨进程/跨部署协调仍待 GOAL-009 审视
- [x] **生产门禁默认仍关**：默认 `PRODUCT_GATES_OPEN=true` 时生产路径仍拒绝写入；CT-013 保持通过；测试仅用 `test_authorized` / `TEST_WRITE_MODE`
- [x] 证据可复现：`web/` unittest 命令、fixture 路径、失败码记录在本目标 `02-execution`；**不**在本目标擅自关闭 GOAL-009 F-007/F-008 或将 GOAL-009 I-003/I-004/I-006 标 `verified`（关闭回写 GOAL-009）— 阶段 E 索引完成

## 高层路线图

| 阶段 | 主题 | 状态 | 退出条件 |
|------|------|------|----------|
| A | 缺口冻结与实现顺序 | **已完成** | D-001 确认范围=A-020 清单；生产门禁硬边界 |
| B | 跨进程幂等 / receipt 恢复 | **已完成** | CT-007 跨实例通过；磁盘 receipt 原子落盘；GOAL-012 residual 已回写关闭 |
| C | F-007 向 CT 补全 | **已完成** | CT-001/003/006/012/014/015 有可运行用例 |
| D | F-008 向 CT 补全 | **已完成** | CT-008 完整 + 009/010/011 有可运行用例；CT-009 限定为 process-local lock |
| E | 回归与回写证据 | **已完成** | 全套相关测试绿；执行记录完整；GOAL-009 A-024 门禁审视回写 |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | A-020 缺口清单是否为关闭前完整必做集？ | 阶段 A 范围冻结 | 编码前 | 对照 A-020 + 用户确认 | verified | 无 | 用户 `/govern 按 A-020 立项`；清单见 A-020 |
| I-002 | required | 跨进程幂等：receipt 存储布局与加载语义 | 阶段 B | B 编码前 | 读 controlled_change + 规格包；实现并测 | verified | 无 | `ops/receipts/{operation_id}.json` 原子写；`_lookup_prior_receipt`；`test_durable_idempotent_replay_new_service_instance` |
| I-003 | required | CT-009 并发模型（线程/进程/顺序模拟） | 阶段 D | D 开始前 | 选定可稳定重现的测试策略 | verified | 无 | D-004：process-local 非阻塞 workspace 锁 + `test_ct009_concurrent_write_conflict`；跨进程协调仍属 GOAL-009 F-008 边界 |
| I-004 | non-blocking | CT-010 与 GoalsRepository recovery 如何衔接 | 阶段 D | D 结束前 | 读 goals_repo recovery | verified | 无 | 读 `.goal-write-recovery.json`；pending → `ERR_RECOVERY_PENDING`；`test_ct010_*` |
| I-005 | required | 生产门禁默认仍关的检查清单 | 全程 / 关门 | 全程 | README + 测试默认 env | verified | 无 | 阶段 E：默认 true + CT-013 测试仍绿；本目标不改默认放行 |

## 依赖与门禁

- **规划台账**：GOAL-009 F-007/F-008、I-003/I-004/I-006；关闭权在 GOAL-009 `/govern` 审视，不在本目标静默改 finding。
- **α 基础**：GOAL-012 已交付关键路径与默认 prod-gate 拒绝。
- **硬禁令**：本目标实现与测试期间，**默认生产路径不得变为可写**；任何「门禁关闭后可写」仅允许在测试显式授权下验证。

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 规划来源

- [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md) · A-020
- [GOAL-012-first-slice-workspace-detail](../GOAL-012-first-slice-workspace-detail/00-meta.md) · F-003 residual
