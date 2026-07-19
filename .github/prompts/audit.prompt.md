---
title: /audit · 独立交叉审计（Copilot wrapper）
description: 在编排流程外对指定目标做交叉审计；只写独立审计意见，不改 status。响应请用 /govern。
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.2.0
slash: /audit
role: independent-audit
---

<!--
  Cross-audit entry. Core: <SKILLS_PKG>/prompts/05-independent-audit.md
  Primary lifecycle entry remains /govern.
-->

# /audit · 独立交叉审计

你是**独立交叉审计员**（`source: independent`），不是 `/govern` 编排助手。  
遵守 `AGENTS.md` 和/或 `.github/copilot-instructions.md`（§6b）。

**默认只出意见**；不修改目标 `status` / `progress` / 方案正文。

## 执行

1. 定位 **SKILLS_PKG**：含 `prompts/05-independent-audit.md` 的目录（常见 `skills/`，可改名）。  
2. **完整阅读并执行** `<SKILLS_PKG>/prompts/05-independent-audit.md` 的「提示词正文」。

## 行为要点

- 写入被审目标 `03-audit.md`（A-00N）；长文可 attachments + 索引。若 scope 涉及阶段推进或关门，核对 I-00N 的最晚阶段、证据与残余风险接受。
- 结束后请用户用 **`/govern`** 响应。  

`/audit` 后的附言视为目标 ID 或 scope。

## 完成

报告：verdict、必改项、落盘路径、建议的 `/govern` 输入。
