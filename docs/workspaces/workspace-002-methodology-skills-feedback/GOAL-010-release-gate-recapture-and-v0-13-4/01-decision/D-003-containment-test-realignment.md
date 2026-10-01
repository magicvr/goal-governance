---
id: D-003
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: decision
title: 让 Windows containment 测试在新规则下成立
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# D-003 · 让 Windows containment 测试在新规则下成立

**状态**：accepted（2026-10-01）

## 触发

本机跑 `python -m unittest skills/tests/test_skills_orchestrator.py` 时，
`test_init_workspace_refuses_existing_path`（GOAL-019 A-001 F-002）失败：

```text
AssertionError: 1 != 0 : first init failed:
Error: install path must stay inside the project: C:\Users\...\goal-governance\skills
```

## 缺口性质（事实）

该测试在 `tempfile.TemporaryDirectory()` 里以 `cwd=<tmp>` 调用 `install.ps1`，但用
**绝对路径** `-SkillsDir <仓库>/skills` 指向项目外的目录。

GOAL-009 引入的 containment 规则（`skills/render_managed.py::install_token`，
被 `install.ps1::Get-InstallToken` 调用，`skills/install.ps1:277-287`）要求安装路径
留在项目内；项目外路径在写入前被拒绝。因此**第一次** init 就失败了，测试里
「第二次 init 被拒绝」的原意根本没被执行到。

这是**测试与已关门规则不一致**，不是产品回归：该规则是 GOAL-009 的既定交付
（A-009 independent pass），不接受为残余。同一测试在 GitHub CI 的
`windows-install-surface` job 里没有执行（已核对 run `34749712448` 的 Windows 日志）。

## 决定

1. **修测试，不改 containment 规则。** 让测试在新的 containment 语义下成立：把
   skills 包复制到**项目内**（目标临时目录下）再以**相对路径** `-SkillsDir .\skills` 调用
   `install.ps1`，使第一次 init 成功、第二次 init 仍按原判定被拒绝。
2. **保留断言原意**：`first.returncode == 0`、`workspace.md` 落盘、第二次非零退出且
   消息命中 `already exists|refuse`。
3. **不改 `skills/install.ps1`、不改 `skills/render_managed.py`。** 本轮不调整
   containment 的边界语义。
4. 该修复与发布同批入库，因此本机与 GitHub CI 的判定重新一致。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 放宽 containment 规则，允许项目外的 `-SkillsDir` | 会撤销 GOAL-009 已审计通过的 fail-closed 边界；把测试的不适应转嫁成产品退让 |
| 给测试加 `skip`，把缺口记为已知环境差异 | 缺口仍在，只是不再暴露；且用户已选择修正 |
| 保留测试原样，只在文档里记录 | 本机 `skills/tests` 持续红，与「CI 全绿」的目标冲突 |

## 仍待后续

- 修好后须复跑 `skills/tests` 全套，确认无其他测试同样依赖项目外的绝对安装路径。
