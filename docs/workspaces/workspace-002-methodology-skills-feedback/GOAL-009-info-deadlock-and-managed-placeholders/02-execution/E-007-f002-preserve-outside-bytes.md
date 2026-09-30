---
id: E-007
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: execution
title: 按 D-006 保留 AGENTS 标记外字节
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# E-007 · 按 D-006 保留 AGENTS 标记外字节（2026-09-30）

## 事实

- `skills/agents_merge.py` 的 `merge_agents_text` 仍用 LF 文本判断标记，但标记两侧的切片来自读入的原文。新写入的受管块是 LF。已有后缀保持原样，包括没有结尾换行的后缀。整份文件就是框架规则、没有标记外消费方字节时，迁移结果仍是 LF 块。
- 读文件改为 `open(..., newline="")`。本机 Python 3.11 的 `Path.read_text` 没有 `newline` 参数，沿用它会把 CRLF 先折成 LF。写文件改为按 UTF-8 字节原样写回。
- `skills/update.py` 的冲突判断、`merge_root_agents` 和 legacy 整文件迁移都改用这两个读写函数。同一逻辑块只是 CRLF 拼写时，`managed_block_equivalent` 不把它当手改。
- 安装器仍调用 `agents_merge.py` 这个 CLI。修正前，新断言失败：`consumer\r\n` 变成 `consumer\n`，退出码 1，6 项失败。修正后 `scripts.tests.test_agents_merge` 与四条安装/升级测试共 23 项 `OK`，耗时 10.440s，退出码 0。覆盖 CRLF 前后缀、混合换行、单独 CR、无结尾换行、CLI 写回字节、`merge_root_agents` 写回字节、CRLF 拼写不算冲突、标记外为 CRLF 时块内手改仍然冲突。既有 LF 夹具仍通过。真实 `install.ps1` / `install.sh` 安装后再升级仍通过。
- 没有改 `.gitattributes`、`/commit` 技能或 `mcp/lifecycle.py`。
- 没有把 GOAL-009 标为 `done`，progress 仍是 75%（3/4）。没有发布，没有另开子目标。

## Checkpoint

- 行为提交：`8861832`（`8861832092acbb67007f8de0961f095ba8dbf009`）
- 该提交的 scope：`skills/agents_merge.py`、`skills/update.py`、`scripts/tests/test_agents_merge.py`
- 此 hash 证明 F-002 的代码与测试已提交。它不证明已经发布或已经关门

## 本轮未发生

- 复审尚未跑。F-001 与 F-002 的闭合留痕写完后，再用同一 codex 模型与强度复审。
