---
id: D-004
goal: GOAL-007-workspaces-directory-consolidation
status: accepted
created: 2026-08-10
updated: 2026-08-10
version: 0.1.0
---

# D-004 · cross audit provider 与职责边界

## 决定

1. independent provider 为用户书面指定的 **Grok Build**，严格按 `skills/prompts/05-independent-audit.md` 的独立审计边界执行。
2. S4 先由主线程写 self 意见，再由 Grok Build 独立会话只读审计实现、迁移、验证与发布候选证据。
3. 子会话返回的 verdict、findings 与关键原文由主线程原样代贴到本目标 `03-audit/A-NNN-*.md`，保留 `source: independent` 与 auditor；主线程不得改写为更有利的结论。
4. 独立会话失败、超时或证据不可核对时，S4 门禁保持未满足；不得降级为第二条 self。
5. findings 的修正、残余风险或驳回仍由 `/govern` 响应，独立意见不直接修改 status/progress。

## 依据

用户于 2026-08-10 书面回复“使用 grok build 做独立审计即可”。P-003 允许交叉工具直接追加或由编排器代贴并保留 independent source。
