---
id: E-005
goal: GOAL-020-goal-drift-detection
title: PR合入、v0.16.0正式发布及资产验收
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
---

# E-005 · 已发生的交付链

- dev `1f6c8eb` 的 [PR #45](https://github.com/magicvr/goal-governance/pull/45)，双平台CI `43755947518` success；合入main `e1f4a6723a8323d101a18fe00fe468ffab712972`，main双平台CI `43756364292` success。
- annotated `v0.16.0` 对象 `2fa1c53b1998017776239ab5915621f8f16f0fb3` 指向该main提交。本地严格release evidence checksPassed=true后推送；tag workflow `43756992355` pack/publish均success。[正式Release](https://github.com/magicvr/goal-governance/releases/tag/v0.16.0)九资产已上传。
- CI七项候选包下载、119个归档成员与bootstrap源字节比对及隔离安装通过；正式九资产按API名称/大小/SHA-256核验，Skills89成员/Core30成员全部匹配不可变tag blobs，Core为Skills内嵌core字节一致子集，contract/matrix摘要与tag一致，正式evidence/report commit均绑定e1f4a67。
- 正式bootstrap隔离安装保留CRLF用户AGENTS字节前缀与项目配置原字节，安装后的GD规则存在。
- GHCR `ghcr.io/magicvr/goal-governance-mcp-server:0.16.0` 的pull digest与实际build/push日志metadata一致：`sha256:8de74f3d2ebd3aec758aa13cf311a6a757eb6d54015eeb22e8746a275daa5414`。按digest运行、只读挂载consumer，serverInfo.version=0.16.0、四入口存在、govern/audit返回GD指导，退出0且consumer所有文件摘要不变。

## 收据

`attachments/s4-delivery-chain.json`、`s4-release-metadata.json`、`s4-formal-file-acceptance.json`、`s4-container-digest-source.json`、`s4-container-acceptance.json`，及CI候选、本地strict副本。

Environment原始审批API见`s4-release-approvals.json`，记录为magicvr两条`skipped`，不写成approved。本侧准备正常审批时pending已消失，在前置断言处退出，未发送审批POST；未修改Environment配置。只记录实际workflow success及原始状态，不虚构人工确认。

I-003 verified、C4产物/验收成立；S4最终cross关门意见尚未返回，仍active75%，未标done。收据与关门记录将走后续dev文档PR合main，发布tag保持原源码身份。Root/R3/VP长期active、Root67%不变。
