---
id: GOAL-004-r3-configurable-governance-root
title: R3：可配置 governance_root 与消费面收敛
status: done
parent: GOAL-001-mcp-file-dual-channel-delivery
plan_refs: VP-004-mcp-file-dual-channel-delivery
primary_plan: VP-004-mcp-file-dual-channel-delivery
serves_summary: 服务 VP-004 R3；governance_root 解析（默认 docs、仅仓内相对路径、仓外 fail closed、内部布局冻结）、项目配置 pin、canonical 权威面路径修订（V-F-013 车辆）与镜像 stage
created: 2026-08-07
updated: 2026-08-07
version: 0.3.0
progress: 100%
---

# GOAL-004 · R3：可配置 governance_root 与消费面收敛

## 概述

在 `workspace-003-mcp-file-dual-channel` 的 Root `GOAL-001-mcp-file-dual-channel-delivery` 下推进 VP-004 的 **R3 阶段**：治理根路径 **`governance_root`** 可配置（默认 `docs`，仅仓库内相对路径，指向仓外 **fail closed**，根下内部相对布局**不可改**）；pin 落在可提交的项目配置（`.goal-governance.json`）和/或 AGENTS managed 段；并按「R3 协议面变更车辆（V-F-013 路径 A）」完成 canonical 权威面修订（`docs/vision/alignment.md` 必改，按影响面含 `workspace-protocol.md`、根 `AGENTS.md`、相关 templates），同一任务 stage Skills 镜像并 `--check`。

R1/R2 已由 [GOAL-002](../GOAL-002-r1-mcp-equivalence-kernel/00-meta.md) / [GOAL-003](../GOAL-003-r2-dual-channel-productization/00-meta.md) 关门交付。

## 成功标准（R3 子目标检查点）

- [x] C1：`governance_root` 解析函数/入口已实现：默认 `docs`；项目配置（`.goal-governance.json`）设为其他相对根后路径解析到该根且根下内部布局（`vision/`、`workspace-*`、`goal-tree`、五件套形状）不变；绝对路径与指向仓外的相对路径（`..` 越界）返回 fail closed 明确错误（有测试）。
- [x] C2：pin 落在可提交的项目配置（`.goal-governance.json`）和/或 AGENTS managed 段（文档 + 实现）。
- [x] C3：canonical 权威面修订：`docs/vision/alignment.md` 至少（按影响面含 `docs/architecture/workspace-protocol.md`、根 `AGENTS.md`、相关 `docs/templates/**`）的路径叙述改为相对 `governance_root`（默认 `docs`）并有例外说明；`python scripts/stage_skills_mirrors.py --check` 通过（镜像与 canonical 一致）。
- [x] C4：禁止「仅运行时识别 root 而 canonical 仍硬编码 `docs/`」——测试断言 canonical 关键路径叙述无裸硬编码（或例外说明存在）。
- [x] C5：R3 证据完成 self + independent 审视（A-001/A-002/A-003 全 pass，无 required findings）；所有 required finding 按合法路径闭合。

`progress: 100%` = C1–C5 已完成 5 / 5（等权）。R3 子目标 `done`（关门审计见 03-audit A-003）。

## 纲领路线图与边界

1. **方案澄清**：关闭 I-001（配置 schema + 解析规则）、I-002（canonical 改写清单）。
2. **解析实现**：`skills/mcp/config.py`（`resolve_governance_root`）+ `.goal-governance.json` schema + fail closed 测试。
3. **canonical 修订**：alignment / workspace-protocol / 根 AGENTS / templates 路径叙述相对化 + 例外说明；stage 镜像 + `--check`。
4. **验证与关门准备**：C1–C4 测试全绿、self + independent 审计闭合。

本目标不包含 VP-002/VP-003 内容演进；Charter 边界不变（不改 strategic）。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | `governance_root` 项目配置 schema 与解析规则（默认值、相对路径、fail closed 边界、与 doctor/lifecycle 接线） | C1 方案冻结 | 方案澄清 | 对照 VP-004 R3 目标 1–5 设计 | **closed** | — | D-001；`config.py` + `test_mcp_config.py` 全绿 |
| I-002 | required | canonical 权威面改写清单与例外说明形态（alignment 哪些节、protocol/AGENTS/templates 按影响面） | C3 方案冻结 | 方案澄清 | 按 V-F-013 车辆列 diff 清单 | **closed** | — | D-002；alignment/protocol/AGENTS/templates 已修订 + stage `--check` 通过 |

## 愿景对齐

- Charter：`vision-goal-governance@0.2.0`（本阶段不改 Charter；默认 root 仍为 `docs`）
- primary plan：[VP-004-mcp-file-dual-channel-delivery](../../vision/plans/VP-004-mcp-file-dual-channel-delivery.md)
- parent：[GOAL-001-mcp-file-dual-channel-delivery](../GOAL-001-mcp-file-dual-channel-delivery/00-meta.md)
- workspace：`workspace-003-mcp-file-dual-channel` · `vision_role: delivery`

## 实施前治理门禁

本工作区采用 `cross` 审计模式（GOAL-002 D-001/D-004）：self + independent（provider = grok build / grok-4.5 / thinking-high）。R3 canonical 修订属 §8c 白名单路径：同一任务内必须 stage 镜像并 `--check`。
