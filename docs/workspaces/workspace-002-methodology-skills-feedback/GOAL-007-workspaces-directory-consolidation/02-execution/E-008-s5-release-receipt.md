---
id: E-008
goal: GOAL-007-workspaces-directory-consolidation
date: 2026-08-11
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
version: 0.1.0
---

# E-008 · S5 正式发布收据

## PR 与 main

- PR #18 在 `contract-and-report` 与 `windows-install-surface` 全绿后，以 merge commit `c63fbf3` 合入 `main`。
- 首次 tag workflow `31416348175` 在历史 L3 evidence consistency 门禁失败，未创建 Release；问题为 4 份 workspace-003 历史证据仍引用旧 flat 路径和旧行为源摘要。
- 修复通过 PR #19 的同一双平台 CI，以 merge commit `f37d67c` 合入 `main`；历史证据保留原采集时间、宿主版本和结果，只重绑定迁移后的仓内路径与 LF-normalized digest。

## Tag、workflow 与资产

- annotated tag `v0.13.2` 的 tag object 为 `7cd26134ce36b1d5823ad9d2047a507fe33b7645`，peeled commit 为 main merge `f37d67c67101df11b5a92563e30a16cfbcd1b362`。
- GitHub Actions run `31416803940` 全绿：pack、M-001 evidence consistency、strict release-evidence、GHCR build/push、Release 创建与资产上传均成功。
- Release：`https://github.com/magicvr/goal-governance/releases/tag/v0.13.2`，共 9 项资产。
- 下载验收：`goal-governance-core-v0.13.2.zip` SHA-256 为 `845da63d8129d59cdd5b17c433bbbc127eddfd948486b6689be8dc6591a433f1`；`goal-governance-skills-v0.13.2.zip` 为 `760ed2186262d01dc535b74c14ac8b169c4cd73afffa0998e61cc5c7435f5544`，均与 sidecar 一致。
- `release-evidence.json` 绑定 annotated tag `v0.13.2`、commit `f37d67c`，`checksPassed: true`。

## 结论

S5 的 PR、CI、main、annotated tag、GHCR、Release 资产、digest 与 evidence 成功边界均已满足。
