---
id: A-001
goal: GOAL-016-charter-version-decoupling
doc: audit-entry
record_id: A-001
source: self
auditor: 编排器（DeepSeek Harness）
scope: S1～S3 协议修正、校验实现与回归（不含 S4 独立审计与 S5 发布）
verdict: pass
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

# A-001 · S1～S3 自审（2026-10-26）

- **source**：self
- **auditor**：编排器（DeepSeek Harness）
- **类型 / scope**：stage / `S1～S3 协议修正、校验实现与回归`；不含 S4 独立意见与 S5 发布
- **verdict**：pass
- **完整意见**：本文件

## 范围与区间

审阅 [GOAL-016 五件套](../00-meta.md)、[D-001](../01-decision/D-001-scope-and-roadmap.md)、[D-002](../01-decision/D-002-adjudication.md)、[E-003](../02-execution/E-003-s2-s3-implementation.md)、[E-004](../02-execution/E-004-checkpoint.md)，以及 commit `2b601c4` 覆盖的 35 个 owned paths。未审 S5 发布产出（尚未发生）。

## 成果（有证据）

1. **A1 去注册表**：`docs/vision/charter.md` 删除 `primary_workspace` 与现行版本中的 Primary / active VP / 组合编排登记行，`version` 保持 `0.2.0`、仅更新 `updated`；`docs/templates/vision/charter.md` 同步；旧字段在 alignment §3.1/§8.1 明确为 legacy hint。
2. **A3 生命周期分层**：`docs/tests/test_vision_protocol.py` 的 `validate_vision_plan()` 对 `planned`/`active` 精确匹配，对 `closed`/`abandoned` 仅校验 `vision_id`；workspace `plan_refs` 复用同一校验；`validate_vision_stack()` 可选扫描 `workspaces_root` 的 primary。
3. **A2 版本语义**：`docs/vision/alignment.md`、`principles.md` P-006、`workspace-protocol.md`、`AGENTS.md`、`consumer-checklist.md`、`/vision` V1/V4 与 `/govern` 均改为「Charter version = 战略对齐版本；editorial 不 bump；strategic 至少 minor」；`revisions.md` 新增 `VR-007`（editorial / 0.2.0）并以测试约束 editorial 不 bump、strategic bump。
4. **primary 单一权威**：`validate_primary_workspace_consistency()` 只读 `workspace.md` 的 `vision_role: primary`，≥2 个 primary 抛错；不读取 `workspaces.md` 或旧 Charter 字段作为门禁。production 测试断言仅 workspace-001 primary，且 `workspaces.md` 投影一致。
5. **回归**：docs 76 / skills 102 / orchestrator 45 / standalone 5 全绿；`stage_skills_mirrors.py --check` 38 对一致；`git diff --check` 干净。检查点 `2b601c4`。
6. **旧仓兼容**：新增测试在临时 Charter 写入 `primary_workspace: workspace-does-not-exist` 后 `validate_vision_stack` 仍通过；closed VP 的旧 `vision_ref` 在 Charter 0.3.0 下仍通过，active/planned 旧 ref 失败。

## 对照成功标准（scope 内适用）

| 标准 | 状态 | 证据 |
|------|------|------|
| 新增 VP/工作区不改 Charter 内容或 version | 达成（合成测试） | `test_new_vp_and_workspace_do_not_mutate_charter` |
| editorial 不改 version、active/planned 不重钉 | 达成（规则 + revisions 测试） | `VR-007`；`test_revisions_version_semantics` |
| strategic bump 后 active/planned 旧 ref 失败、closed 旧 ref 通过 | 达成 | `test_closed_vp_keeps_historical_ref_and_checks_vision_id`、`test_workspace_plan_refs_accept_closed_historical_vp` |
| primary 仅 `workspace.md` 权威；多声明 fail closed；旧 Charter 字段不参与门禁 | 达成 | `validate_primary_workspace_consistency`、`test_primary_workspace_single_authority_fails_on_multiple`、`test_legacy_charter_primary_workspace_is_ignored` |
| 文档/模板/Skills 同步；镜像一致 | 达成 | `stage --check` 38 对；commit `2b601c4` |
| 消费兼容旧 `primary_workspace` / 旧 `vision_ref` | 达成（合成测试） | 同上两条兼容测试 |

## Findings

- **F-001 · 发布门禁仍红（S5 前置）**
  - 严重度：medium
  - 建议：recommended
  - 描述：`scripts/tests` 147（4 failures / 12 errors）与 `capture_runtime_evidence --check` 22 份 / 109 stale 全部归因本次 behavior source 变更；`compatibility_report` 同因失败。这不是 S1～S3 的逻辑缺陷，而是发布链路已知前置：S5 必须在 `docs/releases/runtime/v0.13.8/` 重捕获 16 格并更新矩阵，否则不可 tag/发布。
  - 状态：open（触发 = S5；计划已写入 meta S5 与 E-003）

- **F-002 · 保证等级边界**
  - 严重度：low
  - 建议：recommended
  - 描述：primary/version 规则由 canonical 文档、提示词与仓库测试约束，不新增系统级硬拦截；消费仓仍依赖 checklist / 编排器自觉执行。该边界与 GOAL-013/015 的 L0 保证等级一致，但不得宣称「系统级强制拦截」。
  - 状态：open（触发 = 对外宣称/发布说明；S5 措辞须保留 L0 边界）

## 必改项汇总

无 required findings。

## 结论 + 建议下一步

S1～S3 在声明的 scope 内可核对，self 判 `pass`；无开放 required。F-001/F-002 为 recommended，不阻断 S4。下一步按 D-001 以正式入口派发 `/audit workspace-002 goal-016` 给本地 codex CLI（`gpt-6.1-sol` / high），由独立审计员自主定 scope；编排器在 A-002 落盘后统一响应全部 findings。
