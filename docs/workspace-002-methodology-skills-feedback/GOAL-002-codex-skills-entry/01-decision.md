---
id: GOAL-002-codex-skills-entry
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-07-31
updated: 2026-07-31
version: 0.1.0
---

# 决策记录 · GOAL-002

## 信息需求与阶段门禁

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 状态 |
|----|------|-----------------|----------|--------------|------|
| I-001 | required | Codex skills 加载机制 | 方案冻结 | B | open |
| I-002 | required | 四入口最小形态 | 方案冻结 | B | open |
| I-003 | non-blocking | 矩阵是否 committed | 发版宣称 | 验收 | open |
| I-004 | non-blocking | 跨平台路径 | 实施完整度 | C | open |

> **门禁**：在 I-001/I-002 未 `verified` 或用户书面 `accepted-residual` 前，**不得**冻结「最终目录/安装开关」方案并大批量实现；允许有界探测实验（状态保持 `collecting`）。

## D-001 · 立项：Codex Skills 入口（2026-07-31）

**决定**：

1. 新建本目标，`parent` = Root，`status: active`。
2. 范围：**安装面 + 可调用入口**，使 Codex 能消费本包治理 Skills；核心 prompts 仍以 `skills/prompts/` 为真相，不复制第二套编排正文。
3. 对标现有三宿主适配模式；具体 Codex 目录约定待 I-001 关闭后写入 D-00N 方案决策。
4. 阶段 A→D 见 meta；先信息澄清再方案再实现。

**为什么**：

- 用户明确需要「Codex 所能使用的 skills 入口」。
- 现包已有 claude / copilot / grok，缺 Codex 是明确的消费面缺口，适合作为 VP-002 / R1 首刀。

**未选方案**：

- **仅 README 说明「请手工复制 prompts」**：不能称为可用入口，也难与 install 门禁对齐。
- **改核心协议代替宿主适配**：问题在消费入口，不在 P-001～P-006 正文。
- **四入口一次全部 runtime-verified 才允许任何代码**：可作为关门高标准，但不应阻塞有界探测与骨架落地；验收标准仍要求至少主入口可核对验证。
