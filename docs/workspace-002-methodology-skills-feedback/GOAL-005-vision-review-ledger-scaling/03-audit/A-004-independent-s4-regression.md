---
id: A-004
goal: GOAL-005-vision-review-ledger-scaling
title: independent S4 full validation and candidate evidence cross audit
status: recorded
source: independent
date: 2026-08-06
scope: S4 full validation and candidate evidence (close-out review)
verdict: pass
version: 0.1.0
---

# A-004 · Independent S4 全量验证与候选证据交叉审计

## 范围与区间

- 目标：GOAL-005-vision-review-ledger-scaling（workspace-002-methodology-skills-feedback；Root `GOAL-001-methodology-skills-feedback-evolution`；`plan_refs`/`primary_plan` = VP-002；vision_role delivery）。
- scope：S4 全量验证与候选证据 close-out review——三套 unittest（docs/tests、skills/tests、scripts/tests）、`scripts/stage_skills_mirrors.py --check`、`scripts/compatibility_report.py --require-ready`、`scripts/release_evidence.py --mode rehearsal --run-checks`；复核对 E-003 与 A-003 的 S4 close-out 主张及候选身份 `v0.13.0`。
- 区间：checkpoint `df6a42e029e9cd90170fcca20f211d32bda5c592`（HEAD，分支 `codex/vision-review-ledger-scaling`）上的 S2/S3 产物与 S4 验证证据。
- auditor：Codex（independent sub-session）；执行环境：`.venv\Scripts\python.exe`（Python 3.14.6）；日期 2026-08-06。

## 成果（有证据）

本次审计从仓库根独立重跑全部六条命令，输出为真实运行结果：

- `python -m unittest discover -s docs/tests`：`Ran 32 tests ... OK`（0.253s）。
- `python -m unittest discover -s skills/tests`：`Ran 42 tests ... OK`（2.226s）。
- `python -m unittest discover -s scripts/tests`：`Ran 72 tests ... OK (skipped=3)`（29.378s）；stderr 中 `release evidence failed ...` 与 `runtime evidence capture failed: ... missing-prompt.txt` 来自套件内负向路径用例，非回归失败（与 A-003 记录一致）。
- `python scripts/stage_skills_mirrors.py --check`：`checked_pairs=36`、`copied=0`、`removed_legacy_template_files=0`、`ok: skills mirrors match docs/`，exit 0。
- `python scripts/compatibility_report.py --require-ready`：coverage `ready-for-release-evidence`、`mirrorVerification.passed=true`，exit 0；报告落盘 `artifacts/compatibility-report.json`（gitignored）。
- `python scripts/release_evidence.py --mode rehearsal --run-checks --output <temp>/s4-independent-rehearsal.json`：`release status: rehearsal`、`checks passed: True`、exit 0；`source.commit=df6a42e029e9cd90170fcca20f211d32bda5c592`、`source.branch=codex/vision-review-ledger-scaling`、`protocol.candidateRevision=v0.13.0`、`compatibilityReport.coverageStatus=ready-for-release-evidence`、`mirrorPassed=true`；四项 check（skills-contract-tests / standalone-bootstrap-tests / release-evidence-tool-tests / diff-whitespace `git diff --check`）全部 passed。
- 候选身份：`docs/contracts/skills-consumer-compatibility-matrix.json` 的 `candidateRevision=v0.13.0`；`docs/releases/runtime/v0.13.0/` 下 12 个 2026-08-06 host captures（Claude/Grok/Copilot × govern/audit/vision/vision-audit）文件齐全。
- 台账迁移：`docs/vision/reviews.md` 为稳定索引，VRev-001～006 条目链接至 `docs/vision/reviews/VRev-*.md`（6 个文件存在）；契约规定见 `docs/vision/alignment.md` §9 与 `docs/architecture/principles.md` P-006（索引 + 平铺报告、legacy 合并、不重编号、append-only 响应、open-required 投影）。
- E-003 / A-003 主张复核：测试计数（32/42/72）、镜像 36 对、compatibility ready 与 rehearsal checksPassed 均与本次独立重跑一致。A-003 所述 `workingTree.clean=true` 是 checkpoint `df6a42e` 捕获时刻的状态；本次重跑时工作树含 2 条 checkpoint 之后写入、尚未提交的审计台账记录（`M 03-audit.md`、`?? A-003-*.md`），rehearsal 模式不要求干净树（仅 release 模式强制），不构成对 S4 主张的否定。

## 对照成功标准

S4 判据「全量验证通过，self + independent cross audit 无开放 required finding」：全量验证独立重跑全部通过，本意见无 required finding。S5（PR→main、merged-main ancestry、annotated `v0.13.0` tag、Environment 审批、资产 digest、消费包边界）尚未发生，本意见不提前放行。

## Findings（F-00N）

- 无 required findings。
- 无 recommended findings 影响 S4 关门。

## 必改项汇总

无。

## 与既有意见的异同

- 与 A-001（self，S2/S3）、A-002（independent，S2/S3）、A-003（self，S4 full regression）结论一致：均 `pass`，开放 required = 0。
- 本意见独立重跑全部六条 S4 命令并核对原始输出；A-003 的测试数、镜像对、compatibility 与 rehearsal 结果均可重复。
- 新增观察：本次重跑 rehearsal evidence 的 `workingTree.clean=false` 仅因 checkpoint 后写入审计台账记录所致，与 A-003 在 checkpoint 捕获时的 `clean=true` 不冲突，属验证时点差异而非回归。

## 结论 + 建议

结论：`pass`。S4 全量验证与候选证据（`v0.13.0`）主张成立，E-003 / A-003 的 close-out 记录可复核。建议编排器（`/govern`）汇总 A-003（self）与本意见（independent）后推进 S4 收口；S5 仍受 D-002 门禁约束（merged-main、annotated tag、Environment、资产 digest、消费边界），不得以本意见替代正式发布证据。

## 声明

本意见为独立交叉审计（source: independent），不修改 GOAL-005 的 status/progress/检查点/方案正文，也不修改 goal-tree 状态列；响应与状态推进由 `/govern` 处理。