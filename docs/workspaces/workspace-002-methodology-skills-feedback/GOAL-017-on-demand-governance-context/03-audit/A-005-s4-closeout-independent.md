---
id: GOAL-017-on-demand-governance-context
doc: audit-entry
record_id: A-005
source: independent
scope: S4 published release and goal close-out readiness
verdict: pass
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-03
updated: 2026-11-03
auditor: Grok Build / Grok 4.7
version: 0.1.0
---

# A-005 · S4 发布验收与关门就绪独立复核

## 范围与区间

- auditor: Grok Build / Grok 4.7。正式命令 `/audit workspace-002 goal-017`。本会话看不到 D-002 所写的思考强度设置，因此不把该强度写成已核对事实。
- type: close-out
- 工作区: `workspace-002-methodology-skills-feedback`；目标 `GOAL-017-on-demand-governance-context`
- covered: S4 发布身份、正式 9 资产、Core 子集、隔离安装日志所依据的同一 ZIP、GHCR 摘要与版本、I-001～I-004、A-001/A-002 required 的 A-003 闭合证据是否仍在、A-004 的关门就绪主张
- excluded: 重跑 16 格宿主矩阵、重跑隔离安装、重跑 release-evidence 四项检查；其他工作区目标正文；本意见不修改 status、检查点、progress 或 goal-tree
- 保证等级: L0

## 成果与证据

| 主张 | 本审计核对 |
|------|------------|
| annotated tag `v0.14.0` 指向 main 合并提交 | `git rev-parse v0.14.0` = `dd387ceea63d7d97aba0b09b575634dbdcd373d0`；`v0.14.0^{commit}` = `10bba8600b4d8575b6d6230bac2529795ae7129c` |
| tag workflow 成功 | run [41622193036](https://github.com/magicvr/goal-governance/actions/runs/41622193036)，workflow `Skills pack (tag)`，`headBranch=v0.14.0`，`conclusion=success`，`headSha` 同上 |
| 正式 9 资产摘要与 E-008 一致 | 2026-11-03 现场 `gh release view v0.14.0` 的 9 个 digest、字节数与 [s4-published-asset-verification.json](../attachments/s4-published-asset-verification.json) 逐项相同。本地 `artifacts/goal-017-release-assets/` 的 Skills/Core ZIP SHA-256 与 GitHub 相同：`fbb89a38…`、`5123ea4d…` |
| Core 29 为 Skills 内 `core/` 的字节子集 | 对上述同一 ZIP 重算：Skills 88 成员、Core 29 成员，missing 0、mismatch 0。Core 内 `governance-entry.md` 为 17 行、1374 UTF-8 bytes；`governance-guide.md` 在 Core 包内 |
| 发布证据与覆盖 | [s4-published-release-evidence.json](../attachments/s4-published-release-evidence.json)：`releaseStatus=release-candidate`（该 schema 的 tag 模式取值）、`checksPassed=true`、commit/tag/tagObject 与现场 tag 一致。兼容报告 `candidateRevision=v0.14.0`，`coverage.status=ready-for-release-evidence`，`uncovered` 长度 0 |
| 隔离安装日志使用的是这份正式 ZIP | [s4-published-install.txt](../attachments/s4-published-install.txt) 以 `artifacts/goal-017-release-assets/goal-governance-skills-v0.14.0.zip` 离线安装并写到 `Bootstrap complete.`。本审计未重跑安装；ZIP 哈希已与 GitHub 资产对齐 |
| GHCR `0.14.0` | 现场 `docker buildx imagetools inspect` digest = `sha256:0579508b6412de67955f8d748ea4796dda28e18020d25ae00e6c9ec775a284dd`，与 [s4-ghcr-pull.txt](../attachments/s4-ghcr-pull.txt) 及 E-008 一致。现场 `docker run --rm --entrypoint python … server.py --version` 输出 `goal-governance-mcp 0.14.0` |
| 常驻入口预算 | tag 上 `docs/templates/governance-entry.md` 为 17 行、1374 UTF-8 bytes，低于 D-003 的 40 行 / 4096 bytes |
| S3 required 闭合证据仍在 | [selected-runtime-evidence.json](../attachments/selected-runtime-evidence.json) 的 16 个信封文件都存在，`result.verdict=pass`。A-001/A-002 原文 verdict 仍为 conditional；闭合记录在 A-003，本意见不回写原文 |
| Environment 审批原始状态 | 现场 approvals：`magicvr=skipped`（空 comment），`github-actions[bot]=approved`，comment `5 minute wait timer`。environment `release` 仍有 required reviewer `magicvr`（`prevent_self_review=false`）与 `wait_timer=5`。这与 E-007/E-008/A-004 保留的原始状态一致。deployment `7516633425` 于 10:47:47Z `waiting`，10:53:47Z `queued`，10:54:54Z `success` |
| 信息项 | I-001～I-004 在 `00-meta.md` 均为 verified。I-004 的版本、tag、run、资产与 GHCR 已由上表复验。本目标未登记共享资料引用 |
| 对齐 | `parent` 为本区 Root；Root `parent: null` 且 `primary_plan` 为 VP-002；VP-002 `vision_ref` 为 `vision-goal-governance@0.2.0`，与现行 Charter `0.2.0` 一致。progress 75% 仍是 3/4，第五条成功标准未勾选 |

## 对照成功标准

| 标准 | 本意见 |
|------|--------|
| 常驻块预算，非治理任务不读全文 | 预算在 tag 与 Core ZIP 上复核。非治理不读全文的代表证据沿用 A-003 已闭合的 S3 记录，本意见未重跑宿主 |
| 治理命令先加载完整规则；非法根停止 | S2/S3 已有 A-003 闭合；本 scope 确认指南进入已发布 Core 包 |
| 新装、升级、自定义根、用户字节保留 | 正式 ZIP 的安装日志以同一哈希资产跑到 `Bootstrap complete.`。升级矩阵未在本意见中重跑 |
| canonical、入口、打包一致，且无开放 required | 9 资产与 Core 子集已复核。A-003 之后无新的开放 required |
| dev → main → annotated tag → CI 发布与资产/GHCR 验收 | 现场复核通过。目标仍为 active / 75%，关门记录尚未写入，本意见不把目标标成 done |

## Findings

### F-001 · 路线图括号仍停在资产验收进行中

| 字段 | 值 |
|------|-----|
| level | recommended |
| 严重度 | low |
| status | open |
| 影响门禁 | 不阻断 S4 关门。只影响路线图读者对「验收是否已经做完」的第一眼判断 |
| 关联 | 无 I-00N。不重开 A-001/A-002 |

`00-meta.md` 路线图表把 S4 写成「进行中（E-007：发布成功，正式资产验收中）」。E-008 与 A-004 已经记录正式 9 资产和 GHCR 验收通过，第五条成功标准仍未勾选，检查点仍是 3/4。阶段保持「进行中」与「关门结论尚未落盘」一致；括号里的「验收中」和「E-007」落后于 E-008。

修正：`/govern` 响应本意见时，把该括号改为指向 E-008 的已完成验收，并在用户确认关门时再把 S4 标完成、重算 progress。在关门记录写入前保持 active。

## 必改项汇总

无开放 required。

| ID | 级别 | 状态 | 要做什么 |
|----|------|------|----------|
| F-001 | recommended | open | 路线图括号改为 E-008 验收已完成；S4 完成标记留到关门记录 |

## 与既有意见的异同

A-004（self，pass）认为发布资产、GHCR、信息项和审批原始状态足以支持关门就绪，并写明 `magicvr` 不是普通 `approved`。本意见用现场 tag、Release digest、ZIP 字节比较、GHCR manifest 与容器版本复核后同意该结论。补充的低级别项是路线图括号仍引用 E-007 的「验收中」。

A-002（independent，conditional）的 F-001/F-002 已由 A-003 按 fixed 闭合。当时排除的 S4 范围由本意见覆盖。16 个选定信封仍为 pass，不回写 A-002 的历史 verdict。两边对当前关门焦点没有必改互否：A-002 的 conditional 针对当时的 S3 证据门禁，A-003 之后该 required 已闭合。

## 结论与下一步

verdict 为 **pass**。S4 的发布身份、正式资产、Core 子集和 GHCR 版本与台账一致，开放 required 为 0。目标仍是 active / 75%，本意见不改 status，也不勾选第五条成功标准。

建议 `/govern`：响应 A-005；F-001 可在同一轮关门记录里改正。无开放 required 时，再请用户确认后写 S4 关门并把目标标为 done。保持 L0。审批叙述继续使用 `magicvr skipped` 与 bot `5 minute wait timer`，Environment 规则未在本意见中被改写。

## 声明

本意见不修改 status、检查点、派生 progress 或 goal-tree。响应与 finding 闭合由 /govern 处理。
