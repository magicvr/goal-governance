---
id: D-006
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: decision
title: F-002 按保留标记外字节闭合
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# D-006 · F-002 按保留标记外字节闭合（2026-09-30）

**状态**：accepted

**触发**：用户于 2026-09-30 对 F-002 书面选择「修正：保留标记外字节」。在此之前，用户要求评估「把所有 CRLF 归一化为 LF，并用 git 规则强制，且在 commit 技能里于提交时执行归一化」。该评估已写入 D-005，结论是那条路线不闭合 F-002。

## 决定

1. **F-002 按 fixed 闭合。** 刷新根 `AGENTS.md` 的受管块时，标记外的原始字节保持不变，包括 CR、LF 与 CRLF。写回的受管块使用 LF。
2. **换行拼写相同的受管块不是手改。** 整份文件只是把同一块写成 CRLF 时，升级不把它当成 `managed files have local changes`。块内措辞被改过时，仍然 fail closed。
3. **不把全库 CRLF→LF 或 `/commit` 扫描写进本条。** `.gitattributes` 与四个宿主的 `/commit` 技能保持原样。
4. **不另开子目标。** 写集是 `skills/agents_merge.py`、`skills/update.py` 和对应测试。
5. **本条不改 `mcp/lifecycle.py`。** F-002 的证据路径是安装与升级共用的 `agents_merge.py`。MCP 另有自己的区段替换。

## 为什么

- 用户选定的修正与 A-001 的建议一致：只替换受管区间，标记外字节不改。
- D-004 已经写明标记外字节不改。整份归一化会在受管块更新时改写消费方自己的段落。
- 本仓库的 `eol=lf` 只约束本仓库提交。它不保住消费方工作区里、标记外的 CRLF。
- 受管块是框架文本，本仓库以 LF 存放，所以新写入的块用 LF。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 接受安装时把整份 `AGENTS.md` 写成 LF | 用户选择的是修正，不是残余 |
| 驳回 F-002 | 用户选择的是修正 |
| 在 `/commit` 里扫描整棵树做归一化 | D-005 已记录：该技能只提交点名路径，整树扫描会越过这个边界，也不闭合安装时的改写 |
| 本条一并修改 MCP 区段替换 | 证据路径不在那里。若复审把它列为 required，再由用户决定 |

## 仍待后续

- F-003 仍是 recommended，本条不处理。
- 用本地 codex CLI（`gpt-6.1-sol`，思考强度 high）复审 F-001 与 F-002 的修正。本条不是独立审计。
- 发布范围与 GOAL-009 关门仍待用户书面决定。本条不把目标标为 `done`。
