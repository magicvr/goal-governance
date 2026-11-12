---
id: GOAL-018-host-wait-and-audit-config
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-12
updated: 2026-11-12
version: 0.1.0
---

# E-005 · PR/main、annotated tag 与发布环境门禁

[PR #41](https://github.com/magicvr/goal-governance/pull/41) 的Ubuntu/Windows CI run43178873978均success，按head945e518匹配合并；2026-11-12T08:00:35Z合入main `b1434524dab6df79721d58eb1a1e8d3e34175786`。合并树与已审PR head一致；main CI run43179479745双平台success。检查点945e518含cross退出与发布准备，不存在开放required。

本地main clean下严格release检查checksPassed=true、全部checks通过；annotated tag `v0.15.0` object `0e66284532cdb2dd69dd39bc9753fa368b089df3` 指向上述main，已推送。`s4-main-release-evidence.json`保存本地严格证据，不是正式Release资产。

[tag run43180014952](https://github.com/magicvr/goal-governance/actions/runs/43180014952) 的pack success，7项CI资产已下载核验：双ZIP摘要与sidecar相符，Core30成员是Skills89成员逐字节子集。证据为`s4-ci-pack-verification.json`，formalPublication=false。

Publish GitHub Release (gated) 当前waiting：GitHub release Environment仍要求维护者magicvr审核并有5分钟计时，pending_deployments可核对；approvals查询当前为空。已向用户提供实际Review deployments链接，未由AI代批或修改保护。此为外部平台发布门禁事实，不把本治理目标改成blocked，也不为询问新增目标或同步暂停投影。

正式9资产和GHCR尚未发布/验收，I-004仍collecting，S4进行中，Goal active75%。收到平台实际放行后继续当前发布run，不重打tag；完成正式资产、安装和容器验证以及S4关门复核后再结项。当前收据分支codex/goal-018-release-receipt留存后续文档，不改变tag或已发布源码身份。
