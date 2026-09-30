---
id: E-006
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: execution
title: 按 D-005 限定受管渲染写集
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.1
---

# E-006 · 按 D-005 限定受管渲染写集（2026-09-30）

## 事实

- 用户书面选择修正 F-001 之后，`skills/render_managed.py` 删除整树渲染。`render_managed_pairs` 只渲染 `list_managed_pairs` 给出的、已经存在的消费方目的地。`skills/update.py` 的 `managed_file_pairs` 改为调用同一份清单。
- `install.sh` 与 `install.ps1` 在解析两个目录令牌之后、复制任何安装文件之前调用分离检查。渲染步骤改为 `--render-map`，包根是安装脚本所在的技能包目录。
- 分离检查覆盖互相包含和路径相同。`docs` 与 `docs-extra` 不判为包含。
- 本机 `python -m unittest` 跑了 23 项，结果 `OK`，耗时 10.296s，退出码 0。其中：
  - `test_install_ps1_rendered_placeholders_survive_update` 与 `test_install_sh_rendered_placeholders_survive_update`：真实安装器使用 `methodology` 与 `my-skills`。安装后的原则文件等于渲染字节；事先放入的 `methodology/notes/mine.md`（含 `{governance_root}`）和 `.claude/skills/local-only/SKILL.md`（含 `{{SKILLS_DIR}}`）字节不变；dry-run 升级的 `managed_conflicts` 为空；手改一行后仍报 `managed files have local changes`。
  - `test_nested_dirs_are_rejected_by_update`、`test_install_ps1_rejects_nested_skills_before_write`、`test_install_sh_rejects_nested_skills_before_write`：skills 位于方法论目录之内时，升级抛出 `outside the methodology`；两个真实安装器非 0 退出，`methodology/my-skills/KEEP` 仍为 `keep`，且没有写出 `methodology/architecture/principles.md`。
  - `test_methodology_inside_skills_is_rejected_before_render`：方法论目录为 `skills/core/docs`、skills 目录为 `skills` 时，升级与 `render_managed_pairs` 都在写文件前停止，预先放入的 `principles.md` 字节不变。相同路径 `docs` 与 `docs` 同样停止。
  - `scripts.tests.test_agents_merge` 仍通过。这些夹具是 LF，不覆盖 F-002 的 CRLF 改写。
- 本切片没有改 `docs/architecture`、`docs/templates`、`docs/contracts` 或 `docs/vision/alignment.md`，没有重跑 stage 写入。
- 没有改 `skills/agents_merge.py`。F-002 仍开放。没有把 GOAL-009 标为 `done`，progress 仍是 75%（3/4）。没有发布，没有另开子目标。

## Checkpoint

- 行为提交：`c449915`（`c4499158775d20609ca1fce9e5bb1607a9791ced`）
- 该提交的 scope：`skills/render_managed.py`、`skills/update.py`、`skills/install.sh`、`skills/install.ps1`、`scripts/tests/test_skills_update.py`
- 响应提交：`8fc6b6f`（`8fc6b6f3220cfd604e135ab99830ca82e6cca7fc`）
- 响应 scope：D-005、E-006、A-003、三个索引、GOAL-009 `00-meta.md`、本区 `goal-tree.md`、Root `00-meta.md` 的 R3 指针
- 这两个 hash 证明 F-001 的代码、测试和闭合留痕已提交。它们不证明 F-002 已闭合，也不证明已经发布或已经关门

## 本轮未发生

- 没有跑新的 codex 复审。复审等 F-002 合法闭合之后。
- 没有把全库 CRLF 归一化写进 `.gitattributes` 或 `/commit`。
