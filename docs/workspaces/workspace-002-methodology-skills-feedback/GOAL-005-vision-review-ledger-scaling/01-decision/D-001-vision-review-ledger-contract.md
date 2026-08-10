---
id: D-001
goal: GOAL-005-vision-review-ledger-scaling
title: 冻结 Vision Review 可扩展台账终态
status: accepted
created: 2026-08-06
updated: 2026-08-06
version: 0.1.0
---

# D-001 · 冻结 Vision Review 可扩展台账终态

## 决定

1. `docs/vision/reviews.md` 保持稳定入口与完整安装 MUST 文件，但职责收窄为 frontmatter、使用约定、当前状态投影和条目链接索引。
2. 新增单层平铺目录 `docs/vision/reviews/`；一条正式意见一个 `VRev-NNN-<slug>.md`，self 与 independent 共用 `VRev-00N` 序列。
3. `reviews.md` 索引与 `reviews/VRev-NNN-*.md` 报告共同构成唯一 Vision Review 台账。报告至少保留 source、auditor、scope、verdict、class、findings、required 状态与声明。
4. finding 响应继续由 `/vision` 负责，作为原 VRev 报告内 append-only 响应节追加；不得改写原审计结论。索引的 `open required` 是从报告 finding + 响应闭合证据派生的当前投影，不替代历史原文。
5. 兼容 reader 合并 `reviews.md` 中 legacy inline VRev 与目录报告；编号扫描两处最大值。legacy inline 继续有效，但切换后只向目录写新 VRev。
6. Vision ledger 采用与目标 ledger 相同的切换阈值：legacy 索引达到 32 KiB、800 行、12 条独立记录任一条件，下一次追加必须切换目录；新安装从第一条 VRev 起即使用目录报告。
7. 本仓现有 `VRev-001`～`VRev-006` 在 S2 全量迁移为独立报告；不得重编号、改写 verdict/finding/响应语义或丢失链接。迁移后 `reviews.md` 不再保留这些正文副本。
8. 发布范围包括 canonical、stage 镜像、Skills prompts/host surfaces、模板/bootstrap、tests/fixtures、版本身份、PR/main/tag/Release 与下载资产/消费边界验证。

## 为什么

- 当前 `reviews.md` 仅 6 条 VRev 已达到 30,473 bytes / 352 行；现有“长文可链附件”不能阻止意见正文和响应持续累积。
- Goal Audit 已证明稳定索引 + 平铺独立报告能同时支持可读性、编号稳定和历史兼容；Vision Review 应取得同等级的 ledger 可扩展性，但保持愿景与 Goal 台账边界不混写。
- 只改变未来写入、不迁移当前正文，会长期保留已接近阈值的单文件负担，也无法验证完整 end state。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 只允许把长证据放附件 | 审计正文、findings 与响应仍无限增长，且附件不是正式报告索引 |
| 每 12 条轮转一个 `reviews-archive-N.md` | 引入多索引与编号发现歧义，不符合稳定入口原则 |
| 只对未来 VRev 分片、保留本仓全部 inline 正文 | 不能解决本仓已存在的体量问题，也缺少迁移证据 |
| 为 Vision Review 建 Goal `03-audit` | 破坏 P-006 的愿景/目标台账分界 |

## 门禁

- I-002 未 verified 前不进入 S2 写入。
- S4 cross audit 未形成 self + independent 且 required = 0 前，不进入 S5 发布。
- 发布身份、merged-main ancestry、annotated tag、Environment、资产摘要与消费包边界任一缺失时，不宣称正式发布完成。

