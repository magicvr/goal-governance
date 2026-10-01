---
id: E-004
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: execution
title: 安装时渲染受管占位符并让升级接受该结果
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.1
---

# E-004 · 安装时渲染受管占位符并让升级接受该结果（2026-09-30）

## 事实

- 方案冻结提交是 `a1730ba`（`a1730ba8f57ecbef726e601f6083c07eb01594cb`）。该提交只有 D-004 和索引，没有安装器改动。
- 按 D-004 新增 `skills/render_managed.py`。`install.sh`、`install.ps1` 与 `skills/update.py` 都调用它。安装把核心方法论写到方法论目录令牌下，渲染消费方目的地，并用临时副本合并根 `AGENTS.md` 的受管块。`update.py` 的 `--methodology-dir` 默认 `docs`；受管文件等于包内原文或等于这次渲染字节时不算手改。
- 新测试 `scripts/tests/test_skills_update.py`：`test_rendered_bytes_match_and_a_hand_edit_still_conflicts`、`test_install_ps1_rendered_placeholders_survive_update`、`test_install_sh_rendered_placeholders_survive_update`。后两项在临时目录执行真实安装器，目录为 `methodology` 与 `my-skills`，再对离线包做 `update_package` dry-run。安装后的 `methodology/architecture/principles.md` 字节等于渲染结果；dry-run 的 `managed_conflicts` 为空；追加一行手改后抛出 `managed files have local changes`。
- 同一轮还通过：研究门禁测试、安装脚本接线、`install.ps1 -All` 隔离安装（绝对 `-SkillsDir` 仍落在项目内 `skills`，契约字节未被渲染）、带 primitives 的 P-005 提示、既有 update dry-run 与真实安装器升级、以及 `scripts.tests.test_agents_merge`。合计 25 项，`OK`。
- 本机 `PATH` 上的 `bash` 是不能执行 `/bin/bash` 的 WSL 桩。安装脚本测试改用第一个能打印 `ok` 的 bash，此处为 Git Bash。这不是安装器失败。
- S3 标为已完成。`progress` 改为 **75%（3/4）**。S4 未开始。
- 本切片没有改 `docs/architecture`、`docs/templates`、`docs/contracts` 或 `docs/vision/alignment.md`，没有重跑 stage 写入。镜像 `--check` 仍为 37 对一致。
- 没有跑 codex，也没有把本条目写成 independent。没有发布，也没有把 GOAL-009 标为 `done`。

## Checkpoint

- commit：`ecca659`（`ecca65995fe40f7344fbb826a1d5b83e9b2c9425`）
- scope：`skills/render_managed.py`、`install.sh`、`install.ps1`、`update.py`、安装后再升级测试、E-004、执行索引、审计索引、本区 `goal-tree.md`、Root `00-meta` 里 GOAL-009 的阶段指针
- 方案冻结是前一个提交 `a1730ba`，不含这些安装器改动。此 hash 证明占位符升级行为已提交，不证明已经发布或已经关门

## 本轮未发生

- 没有打 tag，也没有宣称消费方已经拿到这次安装行为。
- 没有另开子目标。
