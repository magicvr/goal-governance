---
id: E-001
goal: GOAL-016-charter-version-decoupling
doc: execution-entry
title: 立项、issue #34 复核与基线记录
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

# E-001 · 立项、issue #34 复核与基线记录（2026-10-26）

## 已发生事实

1. 用户 2026-10-26 通过 `/govern` 指令：在工作区 2 开设新子目标，解决 issue #34，发布新版本；交叉审计调用本地 codex CLI（`gpt-6.1-sol` / high）。
2. 读取 GitHub issue #34（`gh issue view 34`）：状态 `OPEN`，标题「新建 VP/工作区导致 Charter 版本连锁：全部历史 VP 被迫重写 vision_ref」，创建于 2026-10-26T02:15:24Z，无评论。issue 正文含现象、复现、根因、影响、建议方案 A～D、验收标准与四个开放问题。
3. 代码/文档现状核对（只读）：
   - `docs/vision/charter.md` 含 `primary_workspace: workspace-001-goal-governance` 与「现行版本」表中的 Primary 工作区 / 现行 active VP / 组合编排状态；
   - `docs/tests/test_vision_protocol.py` 的 `validate_vision_stack()` 对 `plans/VP-*.md` 全量调用 `validate_vision_plan()`，不按 status 过滤；`validate_workspace_vision_alignment()` 对每个 `plan_refs` 全量精确匹配；
   - `docs/vision/alignment.md` §3.1 把 primary 放在 `workspace.md`、`workspaces.md`、Charter 三处；§8 允许 editorial 补丁级 version；§2.1 要求 VP `vision_ref` 精确匹配；
   - `docs/architecture/principles.md` P-006 §6.3/§6.8 同样要求精确匹配与 Charter 修订分 class；
   - `skills/prompts/06-vision-orchestrator.md` V1 写「更新 charter；`updated`/version（strategic 至少 minor）」，未区分注册表更新；
   - 模板 `docs/templates/vision/charter.md` 仍含空 `primary_workspace` 字段；`docs/vision/consumer-checklist.md` 仍按三处声明检查。
4. 基线：`git rev-parse HEAD` = `ec088c996a07a31972a10f00bc0875650cfe7af1`（`dev`）；`git status --porcelain=v1` 为空；最新 tag `v0.13.7`；`git remote -v` origin = `git@github.com:magicvr/goal-governance.git`；`gh auth status` 已登录 `magicvr`，token 含 `repo`/`workflow`。
5. 已创建 `GOAL-016-charter-version-decoupling/` 五件套 + `01-decision/`、`02-execution/`、`03-audit/`、`attachments/`；同步更新本区 `goal-tree.md` 与 Root `00-meta.md` 子目标表/备注。创建时 `status: active`、`progress: 0%`（S1～S5 0/5）。
6. 审计模式记为 `cross`，independent provider 为本地 codex CLI（`gpt-6.1-sol` / `model_reasoning_effort="high"`），尚无审计意见落盘。
7. 本地 codex CLI 可得：`codex-cli 0.164.0`（`codex.ps1`，npm 全局）。用户级配置为 `gpt-6-luna` / low；本目标派发将按用户指定覆盖模型与思考强度，不改用户配置。

## 本轮未发生

- 未修改任何协议/canonical 文档、模板、测试或 Skills 镜像；未提交；未打 tag；未发布。
- 未收到 Q-001～Q-004 的真实答复；D-001 中的方案推荐不构成用户裁决。
- 未运行独立审计；未产生 A-00N。
