---
id: GOAL-003-r2-dual-channel-productization
title: R2：双通道产品化（bootstrap 双入口 + MCP 薄壳 lifecycle + AGENTS managed）
status: done
parent: GOAL-001-mcp-file-dual-channel-delivery
plan_refs: VP-004-mcp-file-dual-channel-delivery
primary_plan: VP-004-mcp-file-dual-channel-delivery
serves_summary: 服务 VP-004 R2；bootstrap 双入口、MCP 薄壳 lifecycle（allowlist + 确认写盘）、gitignore + doctor、AGENTS managed 标记、File-classic 保留与生产仓 File 自举证据
created: 2026-08-07
updated: 2026-08-07
version: 0.3.0
progress: 100%
---

# GOAL-003 · R2：双通道产品化

## 概述

在 `workspace-003-mcp-file-dual-channel` 的 Root `GOAL-001-mcp-file-dual-channel-delivery` 下推进 VP-004 的 **R2 阶段**：File 与 MCP **均为一等发布通道**。交付 bootstrap 双入口（MCP 通道与 file zip 均为一等发布路径，File 不被废除）、MCP 薄壳 lifecycle（install/upgrade/uninstall 由 MCP 工具管理，managed paths allowlist，默认确认写盘）、消费仓薄入口默认 gitignore + 官方 ignore 片段 + `doctor`、AGENTS.md managed 标记（更新/卸载只改标记内、不触碰用户自有配置）、File-classic（无 Docker/无 MCP）路径完整可用、生产仓 File 自举证据。

R1 已由 [GOAL-002-r1-mcp-equivalence-kernel](../GOAL-002-r1-mcp-equivalence-kernel/00-meta.md) 关门交付（四入口等价内核 + 合同分列）。

## 成功标准（R2 子目标检查点）

- [x] C1：bootstrap/在线安装为双入口（MCP 通道与 file zip 均为一等发布路径）；「推荐 MCP」叙述同屏声明 File 仍一等、非日落。
- [x] C2：MCP 薄壳 lifecycle（install/upgrade/uninstall 由 MCP 工具管理，managed paths allowlist，默认确认写盘）已实现并有测试。
- [x] C3：消费仓薄入口默认 gitignore + 官方 ignore 片段 + `doctor`（对样例消费目录给出正确状态）。
- [x] C4：AGENTS.md（及等价规则文件）managed 标记：更新/卸载只改 `<!-- goal-governance:begin managed -->` 与 `end managed` 之间内容；标记外用户自有配置逐字节不变（有测试）。
- [x] C5：File-classic（无 Docker、无 MCP 标志）路径完整可用（有测试）；生产仓 File 自举有证据。
- [x] C6：R2 证据完成 self + independent 审视（A-001/A-002/A-003；F-001 修复后全 pass）；所有 required finding 按合法路径闭合。

`progress: 100%` = C1–C6 已完成 6 / 6（等权）。R2 子目标 `done`（关门审计见 03-audit A-003）。

## 纲领路线图与边界

1. **方案澄清**：关闭 I-001（薄壳落点 + allowlist 集合）、I-002（bootstrap 双入口形态）。
2. **薄壳 lifecycle 实现**：managed 标记纯函数 + install/upgrade/uninstall + doctor + gitignore 片段。
3. **bootstrap 双入口**：install-online `-Channel files|mcp`；「推荐 MCP」+ File 一等同屏声明（文档与脚本注释）。
4. **验证与关门准备**：消费目录全路径测试（安装/升级/卸载/managed 边界/doctor/File-classic）、生产仓 File 自举证据、self + independent 审计。

本目标不包含 R3 的 `governance_root` 配置实现与 canonical 规则修订（Root 后续阶段）。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 薄壳落点与 managed paths allowlist 集合（`.goal-governance/` + `AGENTS.md` managed 段） | C2 方案冻结 | 方案澄清 | 对照 VP-004 R2 与现有 install 面设计 | **closed** | — | D-001；`lifecycle.py` + `test_mcp_lifecycle.py` 全绿 |
| I-002 | required | bootstrap 双入口的脚本/文档形态（`-Channel files\|mcp`；默认行为与既有 install 测试兼容） | C1 实施 | 方案澄清 | 对照 install-online.* 现状与既有测试 | **closed** | — | D-002；`-Channel` 实现 + 10 条 bootstrap 测试全绿 |
| I-003 | required | 生产仓 File 自举证据形态（只读 dispatch + 安装面核验） | C5 验收 | 验证 | 本仓 File 通道只读核验 + 临时消费目录安装 | **closed** | — | `{SCRATCH}/file-bootstrap.log`；R1 L3 探针（生产仓 File skill 面） |
| I-004 | non-blocking | 消费仓薄壳 gitignore 默认策略（默认忽略、团队可选锁 git）是否需要用户确认 | C3 验收 | C3 | 文档声明默认策略 | **closed** | — | 默认策略落盘（`gitignore-fragment.txt` + doctor 报告）；无需裁决 |

## 愿景对齐

- Charter：`vision-goal-governance@0.2.0`
- primary plan：[VP-004-mcp-file-dual-channel-delivery](../../vision/plans/VP-004-mcp-file-dual-channel-delivery.md)
- parent：[GOAL-001-mcp-file-dual-channel-delivery](../GOAL-001-mcp-file-dual-channel-delivery/00-meta.md)
- workspace：`workspace-003-mcp-file-dual-channel` · `vision_role: delivery`

## 实施前治理门禁

本工作区采用 `cross` 审计模式（GOAL-002 D-001/D-004）：self + independent（provider = grok build / grok-4.5 / thinking-high）。R2 实施与验证沿用该模式；进入实施前先关闭 I-001/I-002。
