---
id: D-003
goal: GOAL-014-release-v0-13-6
doc: decision
title: v0.13.6 发布验收与关门
status: accepted
parent: GOAL-014-release-v0-13-6
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# D-003 · v0.13.6 发布验收与关门

## 依据

1. 用户会话指令「提交 PR，确保 CI 全绿的前提下合并到 main 分支，并打 tag 发布新资产」已实际完成：PR #29 双平台 CI 全绿后合入 main，annotated `v0.13.6` 指向 merge `97f6f1ea`，tag 工作流 39000107099 的 pack 与 gated publish 均 success，Release 已发布 9 项资产。
2. S4 资产验收通过（E-005）：双 ZIP 摘要与 sidecar 一致、Core 为 Skills 的逐字节子集、发布证据 `checksPassed: true` 且身份字段与 tag/merge 一致、下载资产驱动的隔离消费安装 exit 0 且消费者自有 AGENTS 规则保留、GHCR 镜像 digest 与发布日志一致且内置版本 `0.13.6`。
3. A-001（Grok Build / independent / pass，开放 required 0）已落盘并由 A-002 闭合全部建议项；A-003 发布产出与关门审视 pass。无冲突、无 residual、无 overruled。
4. I-001～I-006 全部 `verified`；成功标准 4 项全部满足。

## 决定

1. 将 GOAL-014 标为 **`done`**，S1～S4 全部完成，派生 `progress` = 4/4 = 100%（等权检查点）。
2. 同步 `goal-tree.md`（树、状态表、编号节）与父目标 `GOAL-001` 子目标表及备注。
3. 在回执提交中把 `docs/README.md` 的「最新发布基线」更新为 `v0.13.6`（含 run 链接与资产验收事实），「快照日期」更新为 2026-10-17；v0.13.5 条目保留为其历史发布身份。
4. Root R3 / VP-002 保持长期 `active`，Root `progress` 67% 不变（R3 是持续闭环与长期演进）。
5. 上限声明照 A-003：保证等级 L0，不把本次发布验收外推为第三方鉴证或所有下游环境安装成功；不新增系统级硬拦截主张。

## 未选方案

| 方案 | 未选原因 |
|------|----------|
| 因 Gated 回执是 `skipped` 而判本次发布不合规 | Environment 的人工放行由 magicvr 实际给出（回执可回读）；把 `skipped` 反写成「未审批」或「已 approved」都不符合事实 |
| 在 receipt 提交里更新 `candidateRevision` 或移动 `v0.13.6` tag | 矩阵身份固定在被发布内容上；tag 固定发行 merge，不为追加记录移动；回执只追加文档 |
| 保持 active 不关门 | 成功标准与信息门禁均已闭合，用户指令即为发布与验收授权；继续挂 active 会让「已完成」与「进行中」歧义长期存在 |
