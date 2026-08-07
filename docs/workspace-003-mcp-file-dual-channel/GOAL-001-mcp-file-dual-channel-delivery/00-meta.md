---
id: GOAL-001-mcp-file-dual-channel-delivery
title: 消费交付双通道（MCP + File）与可配置治理根
status: done
parent: null
plan_refs: VP-004-mcp-file-dual-channel-delivery
primary_plan: VP-004-mcp-file-dual-channel-delivery
serves_summary: delivery Root；服务 VP-004 / vision-goal-governance@0.2.0；File+MCP 双通道、四承诺宿主、最小测试内核与可配置 governance_root
created: 2026-08-07
updated: 2026-08-07
version: 0.8.0
progress: 100%
---

# GOAL-001 · 消费交付双通道（MCP + File）与可配置治理根

## 概述

在 Charter `vision-goal-governance@0.2.0` 与 **VP-004** 下，交付 **File** 与 **MCP** 双通道一等公民消费适配：同一协议与四治理入口语义，分发形态与证据分列；并实现可配置 `governance_root`（默认 `docs`，内部布局冻结）。

本 Root 是 [workspace-003-mcp-file-dual-channel](../workspace.md) 的唯一 `parent: null` 总目标。**不**以本仓 Web / VP-003 驱动；协议内容反馈演进主波次仍在 [workspace-002](../../workspace-002-methodology-skills-feedback/) / VP-002。

## 成功标准（Root 方向级 · 对齐 VP-004 退出）

- [x] 双通道一等：File 与 MCP 均可按发布约定取得；推荐 MCP 不废除 File（bootstrap `-Channel files|mcp` + 合同 `deliveryChannels` + 推荐声明同屏，GOAL-003）
- [x] R1：MCP 无 File 大包可达四治理入口等价检查点；L2 共享 + 分通道 L1 + 抽稀 L3 可读（GOAL-002 done）
- [x] R2：薄壳 lifecycle、gitignore 默认、AGENTS managed、生产仓 File 自举有证据（GOAL-003 done）
- [x] R3：`governance_root` 可配置 + 越界 fail closed + canonical 权威修订（GOAL-004 done）
- [x] 宿主：P0（Claude / Grok / Codex）达约定级验证；P1 Copilot 至少 L1（L3 已捕获 pass，无需 residual）——见「宿主适配状态」表
- [x] **不**要求关闭 VP-002/VP-003 或 Charter 可完成（边界声明，见 VP-004 退出判据 #7）

## 纲领路线图（P-001 · 对齐 VP-004 R1–R3）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **R1** | MCP 通道并行达标 + 最小共享测试内核 | **完成（GOAL-002 done）** | 四入口等价检查点；L2 共享 + L1 分列 + 抽稀 L3；合同 `deliveryChannel` 分列 |
| **R2** | 双通道产品化 | **完成（GOAL-003 done）** | bootstrap 双入口；薄壳 lifecycle；gitignore；AGENTS managed；File-classic |
| **R3** | 可配置 `governance_root` 与消费面收敛 | **完成（GOAL-004 done）** | 配置 pin；仓外 fail closed；alignment/AGENTS/templates 权威路径补丁（V-F-013 车辆） |
| **R4** | MCP Docker 资产发布与通道资产分离（reopen 增补） | **完成（GOAL-005 done）** | 发布面核查缺口修复：File zip 结构性排除 `mcp/` 实现（80/0 成员）+ 防御断言；Dockerfile + GHCR 同 tag 发布管线（workflow + 契约测试断言）；`-Channel mcp` 薄装重定义；README 安装指南与文案修正 |

同一纲领阶段内可并行多个子目标；阶段间通常串行。R1/R2/R3 已完成并关门（GOAL-002/003/004 `done`）；**R4 因发布资产面缺口于 2026-08-07 回退关门后新开**（GOAL-005），同日完成并复关（GOAL-005 `done` → Root 复关 `done`、VP-004 `closed`、workspace.md `closed`）。

## 派生进度展示

`progress: 100%` = 纲领阶段 R1～R4 中已完成 **4 / 4**（等权；R1/R2/R3 于 2026-08-07 关门，R4 于 2026-08-07 回退后新开并当日完成复关）。progress **仅展示**，不放行关门、不关闭 finding；Root 状态由审计与 VP-004 退出判据证据链决定。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | MCP 通道最小运行时形态（进程/stdio 或 Docker 推荐路径）与薄 Skills/宿主入口如何映射四治理入口 | R1 方案冻结 | R1 方案 | 对照现有 skills 入口 + MCP 合同草案 | **closed** | — | GOAL-002 D-002 + `skills/mcp/` 实现 + L1 测试全绿 |
| I-002 | required | 共享测试内核 L2 fixture 范围与「等价」检查点落地位置（docs/tests vs skills） | R1 实施 | R1 实施 | 对照 VP-004 十条检查点设计套件 | **closed** | — | GOAL-002 D-003 + `kernel.py` + L2/L1 测试全绿 |
| I-003 | required | `governance_root` 项目配置 schema 与权威面改写清单（alignment 等） | R3 方案冻结 | R3 方案 | 按 VP-004 R3 车辆列 diff 清单 | **closed** | — | GOAL-004 D-001/D-002 + `config.py` + canonical 修订 + stage `--check` |
| I-004 | non-blocking | P0 宿主 L3 探针环境是否本机/CI 可用 | R1 宿主退出 | R1 验收 | 各宿主只读 dispatch 探针 | **closed** | — | 四宿主 L3 探针全 pass（GOAL-002 attachments/runtime/evidence/） |

## 愿景对齐

| 项 | 值 |
|----|-----|
| Charter | `vision-goal-governance@0.2.0` |
| primary_plan | [VP-004-mcp-file-dual-channel-delivery](../../vision/plans/VP-004-mcp-file-dual-channel-delivery.md) |
| workspace | `workspace-003-mcp-file-dual-channel` · `vision_role: delivery` |
| lead | 本区 = VP-004 `lead_workspace` |
| 并行区 | [workspace-002](../../workspace-002-methodology-skills-feedback/) · VP-002（不混 parent） |

## 子目标

| id | title | status |
|----|-------|--------|
| [GOAL-002-r1-mcp-equivalence-kernel](../GOAL-002-r1-mcp-equivalence-kernel/00-meta.md) | R1：MCP/File 等价验证内核 | done |
| [GOAL-003-r2-dual-channel-productization](../GOAL-003-r2-dual-channel-productization/00-meta.md) | R2：双通道产品化 | done |
| [GOAL-004-r3-configurable-governance-root](../GOAL-004-r3-configurable-governance-root/00-meta.md) | R3：可配置 governance_root 与消费面收敛 | done |
| [GOAL-005-r4-mcp-docker-release](../GOAL-005-r4-mcp-docker-release/00-meta.md) | R4：MCP Docker 资产发布与通道资产分离 | done |

## 宿主适配状态（VP-004 承诺面）

| 宿主 | 波次 | L1（通道分列） | L3 抽稀探针 | 状态 | 证据 |
|------|------|----------------|-------------|------|------|
| Claude Code CLI 2.1.223 | **P0** | ✅（File 通道 L1 测试 + 合同 files 分列） | ✅ `pass`（四入口 dispatch/角色边界） | 达标 | GOAL-002 `attachments/runtime/evidence/claude-l3-four-entry-2026-08-07.json` |
| Grok Build CLI（grok-4.5） | **P0** | ✅ | ✅ `pass` | 达标 | `…/grok-l3-four-entry-2026-08-07.json` |
| OpenAI Codex CLI 0.146.1 | **P0** | ✅ | ✅ `pass`（npm shim 经 cmd.exe 包装） | 达标 | `…/codex-l3-four-entry-2026-08-07.json` |
| GitHub Copilot CLI 1.0.75 | **P1** | ✅ | ✅ `pass`（优于最低 L1 地板；无需 residual） | 达标 | `…/copilot-l3-four-entry-2026-08-07.json` |

- 探针面边界（宿主入口面 vs MCP 进程面）见 GOAL-002 `attachments/runtime/README.md`。
- L3 证据经 `runtime-evidence.schema.json` 校验（capture 脚本内建），behaviorSources 哈希与当前树一致。
- 非目标宿主（Antigravity / Open Code）不入矩阵（VP-004 明确）。

## 备注

- 开区决策见 [01-decision/D-001-open-workspace-003.md](01-decision/D-001-open-workspace-003.md)。
- 编号自 GOAL-001 起；**不**延续其他工作区编号。
- 宿主 P0/P1、入口等价检查点、R3 协议车辆以 VP-004 v0.1.1+ 正文为准。
- R1 实施已按 D-002/D-003/D-004 冻结完成；cross 审计 provider = grok build（grok-4.5 / thinking-high）已指定并落盘（GOAL-002 D-004）。
- **R4 reopen（2026-08-07）**：A-009 关门复审通过后，发布面核查（用户指令）发现三项缺口——File zip 混入 `skills/mcp/` 源码、MCP 无可分发 Docker 发布资产、`skills/mcp/README.md`「Dockerfile 可选」文案与事实不符。用户书面确认「全套方案」：Root 回退 `done → active`（progress 100% → 75%，纲领 3/4），新开 **GOAL-005-r4-mcp-docker-release**（R4）；VP-004 与 workspace.md 同步回退 active（留痕见各自文件与 goal-tree）。
- **R4 复关（2026-08-07）**：GOAL-005 `done`（cross 审计 A-001/A-002 pass + A-003 合并响应）→ **Root 复关 `done`**（progress 75% → 100%，纲领 4/4；A-011）；VP-004 `closed`（退出判据 1–8 证据链完整；F-003 #8 路径字面修正）；workspace.md `closed`。I-007（non-blocking）于首次真实 GHCR 发布验收时关闭。
