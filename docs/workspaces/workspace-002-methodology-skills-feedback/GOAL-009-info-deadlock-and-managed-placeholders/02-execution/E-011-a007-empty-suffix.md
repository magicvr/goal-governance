---
id: E-011
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: execution
title: 按 D-008 保留受管块的空后缀
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.1
---

# E-011 · 按 D-008 保留受管块的空后缀（2026-10-01）

## 事实

- `skills/agents_merge.py` 在替换已有受管块时不再因为后缀为空而追加 LF。完全空的文件仍走原来的分支，结果是受管块加一个 LF。
- 新测试 `test_crlf_block_without_a_trailing_newline_is_not_a_hand_edit` 读取真实的 `skills/install/claude/AGENTS.md`，把受管块换成 CRLF 并且不在结束标记后留字节。它同时要求替换旧块时后缀仍为空，并调用 `agents_managed_conflict`。
- 修正前，这项测试失败。失败点是合并结果以 `end managed -->\n` 结尾。1 项测试，失败 1 处，耗时 0.002s，退出码 1。解释器是 Python 3.11.9。
- 修正后，`scripts.tests.test_agents_merge` 共 21 项 `OK`，耗时 0.219s，退出码 0。同一解释器。
- 同一轮还跑了 `scripts.tests.test_agents_merge` 加 `scripts.tests.test_skills_update`，共 36 项，耗时 13.347s，退出码 1。新测试通过。失败的一项是 `test_new_managed_path_conflicts_and_rolls_back_when_install_fails`：测试桩 `fail_after_new_write` 不接受 `methodology_dir`。这次 diff 没有改 `skills/update.py`，也没有改该测试。
- 没有改 `.gitattributes`、`/commit` 或 `mcp/lifecycle.py`。没有把 GOAL-009 标为 `done`，progress 仍是 75%（3/4）。没有发布，没有另开子目标。

## Checkpoint

- 行为提交：`bd4a863`（`bd4a8632e2287fcd493a2b151e7aa9fa0f59d54e`）
- 该提交的 scope：`skills/agents_merge.py`、`scripts/tests/test_agents_merge.py`
- 响应提交：`6f710f8`（`6f710f8843cc27529792324c5506e3e75445eded`）
- 响应 scope：D-008、E-011、A-008、三个索引、GOAL-009 `00-meta.md`、本区 `goal-tree.md`、Root `00-meta.md` 的 R3 指针
- 这两个 hash 证明这次修正的代码、测试和闭合留痕已提交。它们不证明已经发布或已经关门，也不代替尚未落盘的复审

## 本轮未发生

- 这次修正的复审尚未跑。
- 用户尚未书面确认关门，也没有决定发布范围。
