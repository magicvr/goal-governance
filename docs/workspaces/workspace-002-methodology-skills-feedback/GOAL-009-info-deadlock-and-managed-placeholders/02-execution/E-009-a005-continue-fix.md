---
id: E-009
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: execution
title: 按 D-007 补上路径身份与标记外换行
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.1
---

# E-009 · 按 D-007 补上路径身份与标记外换行（2026-09-30）

## 事实

- `skills/render_managed.py` 的目录比较在 Windows 上按 `casefold` 后的路径段判断。`SKILLS/core/docs` 与 `skills` 视为包含。`docs` 与 `docs-extra` 不视为包含。安装器仍调用这个 Python 检查。
- `skills/agents_merge.py` 先按原文切已有标记。标记外只有 CRLF 时，合并结果与原文相同。完全空的文件仍换成受管块；只有换行的文件保留这些字节再追加受管块。
- `mcp/lifecycle.py` 用 `open(..., newline="")` 读取，按 UTF-8 字节写回。卸载不再压缩标记外末尾的换行。
- 修正前，新断言 4 项测试失败 6 处，退出码 1。修正后 `scripts.tests.test_agents_merge`、相关升级测试与 `skills.tests.test_mcp_lifecycle` 共 34 项 `OK`，耗时 7.598s，退出码 0。其中真实 `install.ps1` / `install.sh` 安装后再升级仍通过。
- 没有改 `.gitattributes` 或 `/commit`。没有把 GOAL-009 标为 `done`，progress 仍是 75%（3/4）。没有发布，没有另开子目标。

## Checkpoint

- 行为提交：`599d2d8`（`599d2d860d5aecd3b3dc2a8631ef004afc9a26fc`）
- 该提交的 scope：`skills/render_managed.py`、`skills/agents_merge.py`、`mcp/lifecycle.py`、`scripts/tests/test_agents_merge.py`、`scripts/tests/test_skills_update.py`、`skills/tests/test_mcp_lifecycle.py`
- 响应提交：`7d63cc6`（`7d63cc6df3b59e7b33c9e231342432927172d32f`）
- 响应 scope：D-007、E-009、A-006、三个索引、GOAL-009 `00-meta.md`、本区 `goal-tree.md`、Root `00-meta.md` 的 R3 指针
- 这两个 hash 证明这次修正的代码、测试和闭合留痕已提交。它们不证明已经发布或已经关门，也不代替尚未落盘的复审

## 本轮未发生

- 这次修正的复审尚未跑。
