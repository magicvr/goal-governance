---
id: GOAL-001-methodology-skills-feedback-evolution
doc: decision
status: active
parent: null
created: 2026-07-31
updated: 2026-07-31
version: 0.1.0
---

# 决策记录 · GOAL-001

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同源；关键项：

| ID | 级别 | 状态 | 影响 |
|----|------|------|------|
| I-001 | required | open | 阻断 GOAL-002 方案冻结，直至 Codex 加载机制有据 |
| I-002 | non-blocking | open | R2 优先级 |
| I-003 | non-blocking | 已裁决（本轮） | primary 仍为 workspace-001 |

## D-001 · 开区 workspace-002 + Root 服务 VP-002（2026-07-31）

**决定**：

1. Scaffold **`docs/workspace-002-methodology-skills-feedback/`** 为 VP-002 主交付区。
2. Root = **`GOAL-001-methodology-skills-feedback-evolution`**，`parent: null`，`primary_plan` = `VP-002-methodology-skills-feedback-evolution`。
3. `vision_role` = **`delivery`**；**不**改 Charter `primary_workspace`；workspace-001 仍 monorepo **primary**（奠基封存）。
4. 纲领路线图 R1→R2→R3 写入 Root meta；首子目标 **GOAL-002-codex-skills-entry** 进入 R1。
5. 结束 VP-002「0 区空转」：本区为 `lead_workspace`。

**为什么**：

- VP-001 / workspace-001 Root 已有界 done；协议禁止在 done Root 下为 VP-002 开子目标。
- Charter 0.2.0 + H-EVOL-01：下一阶段价值来自方法论 + Skills 问题回流。
- 用户本轮书面确认 slug、Root slug、delivery 角色与首子目标范围。

**未选方案**：

- **在 workspace-001 继续 GOAL-024+**：违反封存纪律与 VRev-006。
- **002 立刻改 primary**：用户本轮明确 001 仍 primary。
- **无 Root 只建子目标**：违反工作区绑定（须有唯一 `parent: null` Root）。

## D-002 · 首子目标聚焦 Codex Skills 入口（2026-07-31）

**决定**：

R1 首交付为 **GOAL-002-codex-skills-entry**：为 Codex 增加与现有 Claude / Copilot / Grok 对等的 **Skills 入口**（安装面 + 可调用编排入口），使消费方可在 Codex 宿主中使用 `/govern` 等主路径。

**为什么**：

- 现 Skills 包已有 `install/claude`、`install/copilot`、`install/grok`；**无** Codex 专用入口。
- 用户明确本轮意图：补 Codex 可用 skills 入口，作为演进波可见的第一刀。

**未选方案**：

- **先做协议大改再补宿主**：无具体反馈前成本高；宿主缺口已明确。
- **只写文档不落 install 适配**：无法在 Codex 中实际调用。
