---
id: D-007
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: decision
title: A-005 的必改项按继续修正闭合
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# D-007 · A-005 的必改项按继续修正闭合（2026-09-30）

**状态**：accepted

**触发**：用户于 2026-09-30 对 A-005 书面选择。F-001 与 F-002 都选「继续修正」。F-004 选「纳入并修正」。

## 决定

1. **F-001 继续按 fixed 闭合。** 分离检查按当前平台的目录身份判断。在 Windows 上，大小写不同的同一路径算作包含或相同，写入前停止。`docs` 与 `docs-extra` 仍然不是包含。
2. **F-002 继续按 fixed 闭合。** 已有受管标记时，标记外的换行字节原样保留，包括只有空白的前后缀。只有完全空的文件才整份换成受管块。
3. **F-004 纳入本目标并按 fixed 闭合。** MCP 安装、升级、卸载读取时不把 CR/CRLF 折成 LF，卸载时不删标记外的换行。
4. **不另开子目标。** 写集是 `skills/render_managed.py`、`skills/agents_merge.py`、`mcp/lifecycle.py` 和对应测试。
5. **不改 `.gitattributes` 或 `/commit`。** F-003 仍是 recommended，本条不处理。

## 为什么

- 用户已经为 F-001、F-002 选择过修正。A-005 指出那次修正还有缺口，用户选择把同一条修正补完。
- F-004 在 A-005 里是 recommended。用户这次书面把它纳入本目标，所以它进入写集。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 把大小写别名或空白换行接受为残余 | 用户选择的是继续修正 |
| 驳回 F-001 或 F-002 | 用户选择的是继续修正 |
| MCP 留在本目标之外 | 用户选择纳入并修正 |

## 仍待后续

- 用本地 codex CLI（`gpt-6.1-sol`，思考强度 high）复审这次修正。本条不是独立审计。
- 发布范围与 GOAL-009 关门仍待用户书面决定。本条不把目标标为 `done`。
