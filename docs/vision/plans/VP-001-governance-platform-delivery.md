---
doc_type: vision-plan
id: VP-001-governance-platform-delivery
title: 治理协议与 Skills 可复用交付（奠基 · 有界关）
status: closed
vision_ref: vision-goal-governance@0.2.0
lead_workspace: workspace-001-goal-governance
created: 2026-07-28
updated: 2026-07-31
version: 0.3.0
---

# VP-001 · 治理协议与 Skills 可复用交付（奠基 · 有界关）

## 意图

在 Charter（`vision-goal-governance@0.2.0`）下，完成 **可复用治理协议与 Skills 消费适配器** 的**奠基交付**，并使本仓人类 Web 达到 **有界冻结参考** 状态——**不**包含「随真实项目无限演进」（该波次见 **VP-002**），**不**包含人类 UI 产品终态（见 **VP-003** / R-009-X）。

## 方向级退出判据（关门所用 · 奠基波）

1. 核心协议（含愿景/工作区/资料边界）可独立复制使用，且 dogfood 工作区对齐链完整。
2. Skills 主路径按既有发布门禁可验证：`/govern` `/audit` `/vision` `/vision-audit` 与安装/发布约定（默认四入口面）。
3. 本仓 Web：阶段 6 有界交付已记录，定位 **frozen reference**；扩展 residual 显式点名；不以 Web 产品终态为退出条件。
4. 无阻断本规划退出的 required 协议缺口（或用户书面 residual）。

## 工作区绑定

| workspace_id | root_goal | role | joined | notes |
|--------------|-----------|------|--------|-------|
| workspace-001-goal-governance | GOAL-001-main-vision | lead | 2026-07-28 | 奠基 dogfood；Root **有界 done**（2026-07-31）；过程树封存 |

## 关门记录

| date | outcome | summary | evidence_links | residuals |
|------|---------|---------|----------------|-----------|
| 2026-07-31 | **closed · bounded** | 意图 1 奠基有界完成：协议 + Skills 可用；Web 冻结参考；workspace-001 Root 有界 done。演进 → VP-002；人类 UI 产品波 → VP-003。 | [GOAL-001 D-028 / A-021](../../workspace-001-goal-governance/GOAL-001-main-vision/01-decision.md)；goal-tree 全子目标 done；Charter 0.2.0；D-027 Web 冻结；VRev-005/006 | **R-009-X** → VP-003；**F-006** recommended → VP-002；H-WEB-01 / H-EVOL-01 仍为 Charter 假设；可选 V-F-009/010 |

## 规划修订短史

| date | change |
|------|--------|
| 2026-07-31 | **有界关门**：退出判据收敛为奠基波；`status: closed`；residual 移交 VP-002/VP-003。 |
| 2026-07-31 | strategic 对齐 Charter 0.2.0（Web 冻结；当时仍含演进叙述）。 |
| 2026-07-30 | editorial：Skills 退出判据补 `/vision`、`/vision-audit`。 |
| 2026-07-28 | 初创。 |
