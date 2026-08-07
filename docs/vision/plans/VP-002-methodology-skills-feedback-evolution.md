---
doc_type: vision-plan
id: VP-002-methodology-skills-feedback-evolution
title: 真实项目反馈驱动的协议与 Skills 演进
status: active
vision_ref: vision-goal-governance@0.2.0
lead_workspace: workspace-002-methodology-skills-feedback
created: 2026-07-31
updated: 2026-08-08
version: 0.3.0
---

# VP-002 · 真实项目反馈驱动的协议与 Skills 演进

## 意图

在 Charter `vision-goal-governance@0.2.0` 与 **VP-001 奠基有界关** 之后，以**真实项目 / 消费方使用中发现的问题**为触发，持续修正核心方法论与 Skills，使协议在实战中保持可复制、可审计、可安装。

**不**以本仓 Web 产品功能清单驱动（人类 UI 见 **VP-003**）。  
**不**把 Charter 标为可完成。

### 交付容器

- **主交付工作区（已开）**：`workspace-002-methodology-skills-feedback` + Root `GOAL-001-methodology-skills-feedback-evolution`，挂本 VP 为 `primary_plan`；`vision_role: delivery`。
- **不**在 `workspace-001-goal-governance` 的已 done Root 下继续开演进子目标（奠基树封存）。

### 空转声明（alignment §5.1）

| 项 | 值 |
|----|-----|
| 空转状态 | **已结束**（2026-07-31 挂区） |
| 历史空转接受 | 是（创建时 0 区；复核原定 2026-08-14） |
| 空转起算 | 2026-07-31 |
| 挂区日 | **2026-07-31** · `workspace-002-methodology-skills-feedback` |
| 说明 | 挂区后不再适用「0 区空转 fail closed」；交付证据在工作区目标内 |

## 方向级退出判据

在同时满足下列方向时，本 VP **可以**有界或完整关门（证据在挂接工作区目标内）：

1. 至少完成 **一轮** 有界「反馈 → 协议/Skills 修正 → 可核对验证」闭环（子目标证据链完整）。
2. 修正后的协议/Skills 仍满足完整安装与发布门禁（或 residual 用户书面接受）。
3. 无阻断本波次退出的 required 协议缺口；未关闭项显式 residual。
4. **不**要求「永远修到完美」或关闭 Web 终态（R-009-X / VP-003）。

## 工作区绑定

| workspace_id | root_goal | role | joined | notes |
|--------------|-----------|------|--------|-------|
| workspace-002-methodology-skills-feedback | GOAL-001-methodology-skills-feedback-evolution | delivery / **lead** | 2026-07-31 | 用户 `/govern` 确认 slug；首子目标 GOAL-002-codex-skills-entry |

## 消费面承接路线图（2026-08-08 起）

跨区移交与本波次范围内登记的消费面协议缺口，随 R3 收束或下一次协议面修订执行；均为 recommended（非 required），不阻断波次退出，但须在 VP 关门记录中显式 residual。

| 项 | 来源 | 内容 | 触发 | 状态 |
|----|------|------|------|------|
| **F-006 消费面路径收敛** | [workspace-003 Root A-012 F-006](../../workspace-003-mcp-file-dual-channel/GOAL-001-mcp-file-dual-channel-delivery/03-audit/A-012-independent-post-close-methodology-mcp.md)（A-013 登记；2026-08-08 跨区移交） | `skills/AGENTS.template.md` 与四治理 prompts（00/05/06/07）仍硬编码 `docs/…`；`governance_root≠docs` 的 File 消费仓依赖 AI 自觉读 alignment 定义句，易误读。拟处置：模板与 prompts 改为 `{governance_root}` 或安装时按 pin 展开 | VP-002 推进或下一次协议面修订（workspace-002 Root 02-execution 待办 4） | **已并入**（registered，未执行） |
| **R-001 裸路径扫尾** | [workspace-003 Root A-009 R-001](../../workspace-003-mcp-file-dual-channel/GOAL-001-mcp-file-dual-channel-delivery/03-audit/A-009-independent-close-and-vp004-intent.md)（A-010 留痕归本波次） | `overview/directory-layout/docs-README` 的裸 `docs/…` 路径扫尾（与 F-006 同类相对化） | 同上 | **已并入**（registered，未执行） |

## 关门记录

（当前 `active`，无关门记录。）

| date | outcome | summary | evidence_links | residuals |
|------|---------|---------|----------------|-----------|
| — | — | — | — | — |

## 规划修订短史

| date | change |
|------|--------|
| 2026-07-31 | 初创 `active`；承接 VP-001 residual 中的演进焦点（H-EVOL-01）；用户接受零区空转至 2026-08-14 或首开 workspace-002。 |
| 2026-07-31 | **挂区**：`workspace-002-methodology-skills-feedback` 为 lead；空转结束；Root + GOAL-002（Codex Skills 入口）立项。 |
| 2026-08-08 | **承接跨区移交 F-006**（workspace-003 消费面路径收敛）并入「消费面承接路线图」，与 R-001 裸路径扫尾合并跟踪；recommended 级，不阻断波次退出，关门时显式 residual。 |
