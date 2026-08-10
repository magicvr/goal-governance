---
id: GOAL-003-consumer-governance-ergonomics
doc: execution-entry
record_id: E-005
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-005 · A-004 F-001 fixed 候选冻结与预检

## 2026-08-04 · v0.12.0 release candidate preflight

### 已发生事实

- `/govern` 校验 Charter `vision-goal-governance@0.2.0` → VP-002 → workspace-002 → Root 对齐链；Vision Review 无开放 required。A-004 F-001 是当前唯一阻断 GOAL-003 close-out 的 required finding。
- 用户选择 `fixed`；D-010 冻结 `0.12.0` / `v0.12.0` 受控发布切片。GOAL-003 恢复 `active / 6/7`，I-007 恢复 collecting；Root R2 与派生 progress 同步回退。
- 在不修改正式矩阵前，先用 canonical `scripts/capture_runtime_evidence.py` 真实执行三宿主四入口：Claude Code `2.1.220`、Grok Build `0.2.118` / `grok-4.5`、GitHub Copilot CLI `1.0.75` / BYOK，共 **12/12 pass**。每格均满足 exit 0、入口 marker、非平凡 stdout 与当前 behaviorSources SHA-256。
- 12 份 JSON 与 stdout/stderr 摘要固化在 `docs/releases/runtime/v0.12.0/`；敏感模式扫描未发现 token、API key、Authorization、私网 URL 或未脱敏 Request URL。
- canonical compatibility matrix 冻结 `candidateRevision: v0.12.0`，指向上述版本化证据；Grok host 元数据同步到 `0.2.118` / `1e1687c1cf`。`python scripts/stage_skills_mirrors.py --check` 为 **34 pairs matched**。
- `python scripts/compatibility_report.py --require-ready` 通过：coverage `ready-for-release-evidence`，无 uncovered required 单元。
- `release_evidence.py --mode rehearsal --run-checks --include-web` 通过并保持 `releaseStatus: rehearsal`：Skills contract **42 passed**；standalone bootstrap **3 passed**；release/tool **72 passed, 3 skipped**；Web **143 passed, 1 skipped**；diff whitespace pass。skip 仅为本机无可用 WSL Bash与 Windows symlink 权限，不写成通过。
- 根 / Skills / bootstrap 安装 pin、CHANGELOG、发行说明与 candidate 测试断言已同步到 `v0.12.0`；首次全量回归捕获两个旧 Grok 版本/证据日期断言，修正后定向复跑通过。

### 当前门禁

- 尚未创建 annotated `v0.12.0` tag；rehearsal 不等于 strict release-candidate evidence。
- 尚未推送 tag、等待 Environment `release`、创建 GitHub Release 或核对正式资产。
- 尚未从正式 Release 完成真实消费仓更新；因此 A-004 F-001 仍为 required/open，S7 仍为整改中。

### 下一步（计划）

1. 复核完整 diff，完成 release-candidate checkpoint，使工作树干净。
2. 创建 annotated `v0.12.0` tag，在 tag/clean tree 上运行 strict release evidence，再推送 tag。
3. 等待受控 workflow，核对 Release 资产并执行真实消费更新；随后做 independent finding-closure 复核。
