---
id: E-004
goal: GOAL-012-release-v0-13-5
doc: execution
title: v0.13.5 main、tag 与正式发布回执
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
---

# E-004 · 正式发布

- [PR #27](https://github.com/magicvr/goal-governance/pull/27) CI [38690508297](https://github.com/magicvr/goal-governance/actions/runs/38690508297) 的 Ubuntu/Windows job 均成功；2026-10-15T06:10:59Z 合入 main，merge `1a6668e6b791b63af1caded0924335db7bd00aac`。main CI [38690908662](https://github.com/magicvr/goal-governance/actions/runs/38690908662) 同样 success。
- 本地 fast-forward 至该 merge，clean tree 上创建 annotated tag `v0.13.5`，tag object `14afdb080c37561cf0a5e3a7f6b0cba6c52caf50`。重新生成 compatibility ready，执行 `release_evidence.py --mode release --tag v0.13.5 --run-checks`，checksPassed true，再推 tag。使用 S2 已验证的仓内 TEMP/TMP/TMPDIR，仅调整命令环境。
- [正式工作流 38691121485](https://github.com/magicvr/goal-governance/actions/runs/38691121485) 的 pack 与 Publish GitHub Release (gated) 全部 success，hard release-evidence gate 成功。release Environment 仍为 reviewer magicvr + wait_timer 5；`/actions/runs/38691121485/approvals` 返回 magicvr 的两条 `state: skipped`，并非普通 approved。AI 未调用审批/绕过接口或修改环境设置。
- [正式 Release](https://github.com/magicvr/goal-governance/releases/tag/v0.13.5) 于 2026-10-15T06:14:48Z 发布，isDraft/isPrerelease 均 false，9 项资产。
- GHCR 同一 job 的 build/push 成功，日志列出 `ghcr.io/magicvr/goal-governance-mcp-server:0.13.5` 和 `:latest`，containerimage.digest 为 `sha256:d315fe4296d95ee386e8a572b66a5aff66516f1e9e9cf24bf7de9d19c88a0a03`。

I-004 verified，S3 完成。远端身份与步骤回执见 [release-receipt.json](../attachments/release-receipt.json)。原始本地输出在仓库忽略目录 `artifacts/release-0.13.5-{strict.json,workflow.json,workflow.log,approvals.json}`；正式 release-evidence 本身作为 Release 资产保留，不以本地报告替代远端发布证据。
