---
id: D-008
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: decision
title: A-007 的空后缀按继续修正闭合
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# D-008 · A-007 的空后缀按继续修正闭合（2026-10-01）

**状态**：accepted

**触发**：用户于 2026-10-01 对 A-007 剩余的 F-002 书面选择「继续修正」。

## 决定

1. **F-002 继续按 fixed 闭合。** 已有受管块被替换时，结束标记后面的空后缀保持为空，不再补一个 LF。同内容的 CRLF 受管块即使没有末尾换行，也不算手改。
2. **完全空的新文件不变。** 文件里一个字节都没有时，仍写成受管块再加一个 LF。
3. **不另开子目标。** 写集是 `skills/agents_merge.py` 与 `scripts/tests/test_agents_merge.py`。
4. **不改 `.gitattributes`、`/commit` 或 `mcp/lifecycle.py`。** F-003 仍是 recommended，本条不处理。F-001 与 F-004 维持 A-007 已经认可的关闭证据。

## 为什么

- A-007 确认先前的标记外换行修正仍有一个边界：结束标记后没有字节时，合并会补上 LF，升级因此把同内容的 CRLF 块报成手改。
- 用户选择把这条修正补完，而不是接受这个 LF，也不是驳回意见。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 接受「空后缀会被补一个 LF」为残余 | 用户选择的是继续修正 |
| 驳回这条意见并维持补 LF | 用户选择的是继续修正 |
| 把全库 CRLF 归一化为 LF | 用户此前已经拒绝把这条评估当成闭合路径 |

## 仍待后续

- 用本地 codex CLI（`gpt-6.1-sol`，思考强度 high）复审这次修正。本条不是独立审计。
- 发布范围与 GOAL-009 关门仍待用户书面决定。本条不把目标标为 `done`。
