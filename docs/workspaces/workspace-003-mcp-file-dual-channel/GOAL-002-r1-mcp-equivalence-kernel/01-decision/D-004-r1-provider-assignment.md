---
id: D-004
goal_id: GOAL-002-r1-mcp-equivalence-kernel
title: R1 方案冻结 · cross 审计 independent provider 指定（I-003 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-004 · cross 审计 provider 指定（2026-08-07）

## 决定

1. 用户于 **2026-08-07** 在本目标推进指令中书面指定：本工作区 cross 审计的 independent provider = **Grok Build**，模型 **grok-4.5**，思考强度 **high**（「关节环境需要交叉审计的话，可以调用 grok build（模型 grok 4.5，思考强度 high）进行独立审计」）。
2. independent 审计意见以 `source: independent`、`provider: grok-build / grok-4.5 / thinking-high` 标注落盘到被审目标 `03-audit/A-NNN-*.md` 并更新 `03-audit.md` 索引；不直接改被审目标 `status`/`progress`。
3. 若该 provider 实际不可用，**不得**静默降级为 self 或跳过（P-003/P-004）：回到用户裁决。

## 未选方案

- 静默以 self 顶替 independent：排除（P-003 明确禁止）。
- 指定其他 provider（Claude Code / OpenAI Codex CLI）：用户未指定，不擅自更换。

## 依据

- P-003 审计模式 `cross`：self + 至少一个指定 provider 的 independent。
- 用户 2026-08-07 目标指令（本决定即书面留痕）。

## 证据 / 结论

- I-003 以本决定关闭（required → closed）。independent 意见条目见 `03-audit/A-00N-*.md`（R1 验证后写入）。
