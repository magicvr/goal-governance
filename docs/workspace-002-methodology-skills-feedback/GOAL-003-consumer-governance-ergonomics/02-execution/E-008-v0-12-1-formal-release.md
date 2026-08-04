---
id: GOAL-003-consumer-governance-ergonomics
doc: execution-entry
record_id: E-008
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-008 · v0.12.1 正式 Release 与资产核验

## PR 与 main 集成

- `dev` release-candidate checkpoint 为 `a5f74e5552409efaa54669f0cbeac3a6c718a20f`，已推送到远端。
- [PR #9](https://github.com/magicvr/goal-governance/pull/9) 以普通 merge 合入 `main`；PR Actions run [`30865217702`](https://github.com/magicvr/goal-governance/actions/runs/30865217702) 的 Linux 与 Windows jobs 均为 `success`。
- merge commit 为 `1c21f246377025f295363dbfb7b149b6f7e9fd9e`。合并后 `main` Actions run [`30865380671`](https://github.com/magicvr/goal-governance/actions/runs/30865380671) 的两项 jobs 均为 `success`。

## strict tag 与发布门禁

- 在 clean、exact merged `main` commit 上创建 annotated tag `v0.12.1`；tag object 为 `7e79a5c3ec95be83f021cb2d7efb8afb8c7e627a`，远端 tag peel 到上述 merge commit。
- 本地 strict `release_evidence.py --mode release --tag v0.12.1 --run-checks --include-web` 通过：`releaseStatus: release-candidate`、`checksPassed: true`、candidate `v0.12.1`、compatibility `ready-for-release-evidence`、uncovered `0`、mirror verification passed。
- 只在上述事实成立后推送 tag。GitHub Actions run [`30865670069`](https://github.com/magicvr/goal-governance/actions/runs/30865670069) 的 pack 与 Environment `release` gated publish 均为 `success`；deployment `5735842972` 经配置的 reviewer 门禁批准，没有绕过 strict evidence。

## Release 与下载后核验

- 正式 [GitHub Release v0.12.1](https://github.com/magicvr/goal-governance/releases/tag/v0.12.1) 于 `2026-08-04T00:33:08Z` 发布，`draft: false`、`prerelease: false`。
- 9 个资产均为 `uploaded`：skills/core zip + SHA-256 sidecar、PowerShell/Bash bootstrap、bootstrap README、compatibility report 与 release evidence。
- 从 Release 重新下载全部 9 个资产后，逐项计算的 SHA-256 与 GitHub Release API digest 全部一致；两个 zip 也分别与 sidecar 一致。
- core zip SHA-256 为 `c989ccd745b34a5bad11273a3cf689924e7e034640f80fdcec644da1bc4b3974`；skills zip 为 `b2802757978791cd60911a73343d490ce90e3ef1f0b201f59471ca37235ec4ed`。
- 下载的 `release-evidence.json` 绑定 merge commit、annotated tag 与 tag object，且 `checksPassed: true`；`compatibility-report.json` 为 candidate `v0.12.1`、coverage ready、uncovered `0`、mirror passed。
- core zip 含 architecture 与 canonical templates，不含 Skills prompts；skills zip 含三个 updater、consumer contract + schema，不含 producer-only compatibility matrix、runtime-evidence schema 或 release evidence。

本记录是 tag 后的治理事实，不改变已发布资产所绑定的不可变 tag commit。
