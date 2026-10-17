---
id: D-002
goal: GOAL-014-release-v0-13-6
doc: decision
title: 用户指定 independent 审计 provider 为 Grok Build
status: accepted
parent: GOAL-014-release-v0-13-6
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# D-002 · independent provider 指定

## 真实用户答复

2026-10-17，通过阻塞询问卡片收到：

| 问题 ID | 实际提交值 |
|---------|------------|
| independent_provider_goal014 | `Grok Build CLI（Recommended）` |

卡片给出三个互斥选项（Grok Build CLI / Codex CLI 独立子代理 / Claude Code CLI）并允许自由输入；用户选择了明确推荐项，不是空返回、取消或预选推定。

## 决定

1. 本目标 independent 审计 provider = **Grok Build**（本机 1.0.60 / `01a8e1c591c0`，仓内 `.grok/skills/audit` 指向正式 prompts）。
2. 派发输入只允许正式命令 **`/audit 002 014`**：不附加 scope、文件清单、阶段、结论预期或编排历史；不 resume 既有会话；stdin 为 DEVNULL。`--model` / `--reasoning-effort` 等调用 flag 是执行配置，不是审计输入。
3. provider 失败时门禁保持未满足：不静默降级为 self、不换用其他 provider、不由编排器代写 independent 意见。
4. 审计员只写被审目标 `03-audit/A-NNN-*.md` 与索引，不改 `status` / `progress` / 方案正文；响应与整改由编排器在后续条目留痕。
