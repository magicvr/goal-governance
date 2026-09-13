---
title: /commit · 安全提交便利入口（Copilot wrapper）
description: 依据已暂存变动或明确 owned paths 生成中文提交描述并安全提交；便利可选，非治理必达、非 checkpoint 替代。
status: active
created: 2026-09-13
updated: 2026-09-13
parent: null
version: 0.1.0
slash: /commit
role: convenience
---

<!--
  CONVENIENCE entry (not part of the four governance-must entrypoints).
  Source of truth: <SKILLS_PKG>/install/copilot/prompts/commit.md
  Governance boundary: GOAL-008 D-002 §4 / VP-004 入口面 — 便利可选，不入必达集，不替代 /govern checkpoint。
-->

# /commit · 安全提交便利入口

1. 运行 `git diff --cached --name-status`；非空则确认路径归属，可疑即停止报告。
2. 为空且用户/流程已明确 owned paths → `git add -- <owned paths>`；**禁止** `git add -A` / `git add .`。
3. 暂存后运行 `git diff --cached --check`；无改动、校验失败或路径越界 → 不提交。
4. 生成中文 Conventional Commits 描述（`feat, fix, docs, style, refactor, test, chore`，≤50 字）。
5. `git commit -m "<描述>"`；回显提交 ID 与暂存范围。

fail closed：路径含既有用户改动或不可分离、非 Git 仓库、hook 拒绝、detached HEAD/rebase、用户禁用 → 停止报告，不覆盖不回退；**不 push**；**不**把 commit 当治理放行依据。