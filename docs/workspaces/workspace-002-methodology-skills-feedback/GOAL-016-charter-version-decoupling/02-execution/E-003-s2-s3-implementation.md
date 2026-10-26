---
id: E-003
goal: GOAL-016-charter-version-decoupling
doc: execution-entry
title: S2/S3 协议修正、校验实现与回归
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

# E-003 · S2/S3 协议修正、校验实现与回归（2026-10-26）

## 已发生事实

按 [D-002](../01-decision/D-002-adjudication.md) 写集实施 A1+A3+A2，primary 采用单一权威（仅 `workspace.md`），`closed`/`abandoned` VP 仅校验 `vision_id`，发布版本冻结为 `v0.13.8`。

### S2 · protocol / canonical 文档

1. `docs/vision/charter.md`：删除 `primary_workspace` 与「现行版本」中的 Primary / active VP / 组合编排登记行；`version` 保持 `0.2.0`，只更新 `updated`。新增说明指向 `roadmap.md` / `workspaces.md` / VP frontmatter。
2. `docs/vision/revisions.md`：新增 `VR-007`（`editorial`，Charter 版本 `0.2.0`），记录注册表移除与版本语义；未改写历史 `VR-001`～`VR-006`。
3. `docs/vision/alignment.md`（0.10.0 → **0.11.0**）：§0.1 / §0.2 MUST / §2 / §2.1 / §3.1 / §6 / §8 改为按 VP status 校验、primary 单一权威、editorial 不 bump；新增 §8.1。
4. `docs/architecture/principles.md`（0.15.0 → **0.16.0**）：P-006 §6.1/§6.3/§6.5/§6.8/§6.10 同步；旧 `primary_workspace` 仅 legacy hint；新增「不承载可变注册表」与「不全量重钉历史 VP」非目标。
5. `docs/architecture/workspace-protocol.md`（1.2.0 → **1.3.0**）：§4b 的 vision_ref / fail closed / primary 三条同步。
6. `AGENTS.md`（0.16.1 → **0.17.0**）与 `.github/copilot-instructions.md`（0.13.1 → **0.14.0**）、`skills/AGENTS.template.md`（0.15.1 → **0.16.0**）：§6d 增补版本语义与 primary 单一权威；完成前检查清单增加版本/历史项。
7. `docs/templates/vision/charter.md`：删除 `primary_workspace` 与注册表；模板不再生成可变登记行。
8. `docs/vision/consumer-checklist.md`（0.5.1 → **0.6.0**）、`docs/vision/README.md`（0.7.0 → **0.8.0**）、`docs/vision/workspaces.md`（0.6.0 → **0.7.0**）、`docs/standalone-bootstrap.md`（0.9.0 → **0.10.0**）、`docs/README.md`（0.15.0 → **0.16.0**）同步操作说明。
9. `skills/prompts/00-govern-orchestrator.md`（0.14.2 → **0.15.0**）、`06-vision-orchestrator.md`（0.5.3 → **0.6.0**）、`07-independent-vision-review.md`（0.3.1 → **0.4.0**）同步校验与 V1/V4 语义。

### S3 · validator、测试与镜像

1. `docs/tests/test_vision_protocol.py`：
   - `validate_vision_plan()` 对 `planned`/`active` 保留精确匹配，对 `closed`/`abandoned` 仅校验 `vision_id`；`validate_vision_stack()` 增加可选 `workspaces_root` 并调用 primary 扫描。
   - 新增 `validate_primary_workspace_consistency()`：仅按 `workspace.md` 的 `vision_role: primary` 收集；≥2 个 primary 抛错；不读取 `workspaces.md` 或旧 Charter 字段作为门禁。
   - 新增回归：closed/abandoned 历史 ref 通过、active/planned 旧 ref 失败、closed 不同 `vision_id` 失败、workspace `plan_refs` 接受 closed 历史 VP、新建 VP/工作区不改 Charter、primary 多声明失败、旧 `primary_workspace` 被忽略、production primary 扫描与 `workspaces.md` 投影一致、revisions 的 editorial/strategic 版本语义。
2. 镜像：`python scripts/stage_skills_mirrors.py` 复制 5 对；`--check` 报告 `checked_pairs: 38` / `ok: skills mirrors match docs/`。
3. 回归结果（Python 3.11.9，系统解释器）：
   - `docs/tests`：**76 tests OK**；
   - `skills/tests`：**102 tests OK**；
   - `skills/tests/test_skills_orchestrator.py`：**45 tests OK**；
   - `docs/tests/test_standalone_bootstrap.py`：**5 tests OK**；
   - `git diff --check`：干净（exit 0）。
4. **已知红门禁（不在 S3 内修复）**：`scripts/tests` 运行 **147 tests / 4 failures / 12 errors**，全部归因 `runtime evidence behavior source is stale`；`capture_runtime_evidence --check --evidence-dir docs/releases/runtime/v0.13.7` 报 **22 份 / 109 个 stale problem**；`compatibility_report.py` 同因失败。根因是本次改动命中 behavior sources（`AGENTS.md`、`skills/AGENTS.template.md`、`docs/architecture/principles.md`、`workspace-protocol.md`、`docs/vision/alignment.md`、`skills/prompts/00/06/07`），与 GOAL-015 S5 的模式一致。按 D-002 / meta S3 退出条件，这些 producer 发布门禁移交 S5：在 `docs/releases/runtime/v0.13.8/` 重捕获 16 格并更新矩阵。
5. 本轮未提交、未打 tag、未发布；未运行 self/independent 审计。

## 证据路径

- 文档：`docs/vision/alignment.md`、`docs/architecture/principles.md`、`docs/architecture/workspace-protocol.md`、`AGENTS.md`、`docs/vision/charter.md`、`docs/vision/revisions.md`
- 校验：`docs/tests/test_vision_protocol.py`
- 镜像：`skills/core/docs/`（stage 生成）
- 门禁日志：见本轮会话 `docs-tests2.log` / `skills-tests.log` / `scripts-tests.log`（临时文件，不作为发布证据）
