---
id: A-019
goal: GOAL-001-mcp-file-dual-channel-delivery
doc: audit
title: 独立审计 v0.13.1 发布准备物（grok build / grok-4.5 / thinking high）
status: recorded
source: independent
provider: grok build / grok-4.5 / thinking high（独立会话，经编排器代贴落盘）
date: 2026-08-08
scope: v0.13.1 资产发布准备物（workspace-003 / VP-004 发布轮）：CHANGELOG、compatibility matrix、pack/publish workflow、契约测试、Root 状态与本地门禁
audit_type: ad-hoc（release prep）
verdict: conditional
version: 0.1.0
---

# A-019 · 独立审计 v0.13.1 发布准备（2026-08-08）

> 本条目由独立会话（grok build / grok-4.5 / thinking high）出具意见，编排器代贴落盘并保留 `source: independent`；意见正文未经编排器改写。

## 结论

**verdict: `conditional`**。技术门禁与发布工件可核对且本地全绿（243 passed / stage 36 对 0 漂移 / `--require-ready` ready-for-release-evidence / rehearsal `checksPassed: true` / M-001 `--check` 绿 / workflow 契约测试真实钉死顺序与 9 资产 + GHCR）。**唯一 required 缺口：F-001（D-003 安装入口 pin 未同步 v0.13.1）**——闭合前不得无条件放行打 tag 发版。

## 独立验证结果（审计员亲自执行）

| 动作 | 结果 |
|------|------|
| `pytest docs/tests skills/tests scripts/tests` | 243 passed, 4 skipped, 98 subtests（exit 0） |
| `stage_skills_mirrors.py --check` | ok（36 pairs；0 漂移） |
| `compatibility_report.py --require-ready` | exit 0；ready-for-release-evidence；candidateRevision v0.13.1；uncovered 0 |
| `release_evidence.py --mode rehearsal --tag v0.13.1 --run-checks` | exit 0；checksPassed true（4/4：skills-contract / standalone-bootstrap / release-evidence-tool / diff-whitespace）；annotatedTag null（rehearsal 预期） |
| `capture_runtime_evidence.py --check`（L3 目录） | evidence consistency ok（4 evidence files） |
| `test_pack_job_pins_evidence_consistency_gate` | 3/3 workflow 契约测试 OK（含新 M-001 断言，非空壳） |
| 本地 pack（skills/core，--version 0.13.1） | skills 78 成员 + core 25 成员，zip+sha256 可生成 |

## Findings

| ID | 级别 | 严重度 | 说明 |
|----|------|--------|------|
| **F-001** | required | med | **D-003 安装 pin 未同步 v0.13.1**：根 `README.md` / `skills/README.md` / `scripts/bootstrap/README.md` 仍写「最新正式 tag v0.13.0」及全套 download URL / `-Version 0.13.0` / zip 名；`skills/README.md` 会打进 skills zip——v0.13.1 包内仍引导装 0.13.0。CHANGELOG 0.13.1 节与入口 pin 字面冲突。闭合建议：同一提交同步三入口 pin（+ mcp/docs README 基线）。 |
| **F-002** | recommended | low | matrix `evidenceScope` 文案仍写 `Candidate v0.13.0`（顶层 candidateRevision 已 v0.13.1）。 |
| **F-003** | recommended | low | runtime 证据目录仍 `docs/releases/runtime/v0.13.0/`（v0.13.1/ 不存在）；功能可发布，建议复制或书面说明复用策略。 |

## 必改项汇总

required：**F-001**（闭合前不宣称发布准备无条件完成）。recommended：F-002、F-003。

## 结论 + 给编排器的建议

1. 先闭合 F-001（同一提交同步三入口 pin）；可选处理 F-002/F-003。
2. 修完重跑 stage `--check` + `--require-ready` + rehearsal。
3. 推 tag 后按清单走 Actions pack → Environment `release` 审批 → 核验 9 项资产 + GHCR `:0.13.1`/`:latest` → 关闭 I-007 / F-008。
4. 远端动作（push/merge/tag/workflow/GHCR）为后续编排步骤，不记 finding；历史 08-06 证据 stale 为预期，不记 finding。

## 声明

本意见不修改 status/progress；响应由 `/govern` 合并处理。
