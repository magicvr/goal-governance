---
id: E-002
goal: GOAL-005-vision-review-ledger-scaling
title: canonical 迁移、Skills 同步与候选验证
status: recorded
created: 2026-08-06
updated: 2026-08-06
version: 0.1.0
---

# E-002 · canonical 迁移、Skills 同步与候选验证

## 事实

- `docs/vision/reviews.md` 已收窄为稳定索引；`VRev-001`～`VRev-006` 已迁移到 `docs/vision/reviews/VRev-*.md`，`preserved_blocks=6`，无重编号或历史结论改写。
- `principles.md`、`alignment.md`、workspace protocol、overview、AGENTS、README、bootstrap、Vision prompts、四宿主 wrappers、模板与 consumer checklist 已同步新契约。
- `python scripts/stage_skills_mirrors.py --check` 通过，canonical / Skills mirror 无漂移。
- 自动化回归通过：docs `32` 项、Skills `42` 项、scripts `72` 项（scripts 环境跳过项保持原有边界）。
- 旧 `v0.12.1` runtime evidence 在行为源变化后被 freshness guard 正确拒绝；随后真实重采 Claude/Grok/Copilot 四入口，共 `12` 项 2026-08-06 `runtime-verified`，归档于 `docs/releases/runtime/v0.13.0/`。
- `python scripts/compatibility_report.py --require-ready` 通过，coverage 为 `ready-for-release-evidence`；当前候选为 `v0.13.0`。
- 旧 workspace-001 中指向 `reviews.md#VRev-*` 的陈旧链接已改为独立报告路径；当前扫描无残留旧锚点。

## 边界

上述事实证明 S2/S3 与候选证据已完成，不证明 PR、merged-main、annotated tag、GitHub Release 或消费安装完成；这些属于 S5。
