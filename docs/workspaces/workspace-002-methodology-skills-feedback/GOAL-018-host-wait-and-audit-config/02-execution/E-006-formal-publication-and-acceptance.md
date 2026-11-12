---
id: GOAL-018-host-wait-and-audit-config
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-12
updated: 2026-11-12
version: 0.1.0
---

# E-006 · 正式发布、资产与容器验收

用户确认“已经在github授权”后，继续原 [tag run 43180014952](https://github.com/magicvr/goal-governance/actions/runs/43180014952)，pack 与 gated publish 均 success，2026-11-12T08:12:46Z 正式发布 [v0.15.0](https://github.com/magicvr/goal-governance/releases/tag/v0.15.0)。未修改环境保护或重新打 tag。审批 API 原始记录为 magicvr `state=skipped`、空 comment，以及 github-actions[bot] `state=approved`、comment 为 `5 minute wait timer`；不把前者改述为普通 approved。原始收据见 [workflow](../attachments/s4-tag-workflow-completed.json)、[approvals](../attachments/s4-release-approvals.json) 和 [Release metadata](../attachments/s4-release-metadata.json)。E-005 保留当时 waiting 的历史事实。

远端 Git API 确认 annotated tag object `0e66284532cdb2dd69dd39bc9753fa368b089df3` 指向 main 发布提交 `b1434524dab6df79721d58eb1a1e8d3e34175786`，见 [remote tag](../attachments/s4-remote-tag.json)。Release 的 target_commitish=main 只作元数据，不以它单独证明源码身份。

## 正式资产

下载正式 Release 的 9 项资产：Skills/Core ZIP、两份 SHA-256 sidecar、PowerShell/bash bootstrap、bootstrap README、release-evidence 与 compatibility-report。所有文件 size/SHA-256 均匹配 GitHub digest；前 7 项与同 run 的 CI pack 逐字节一致。双 ZIP 摘要匹配 sidecar，Core 30 个文件是 Skills 89 个文件中 core/ 下的逐字节子集。证据见 [asset verification](../attachments/s4-published-asset-verification.json)。

[正式 release-evidence](../attachments/s4-formal-release-evidence.json) 的 source commit/tag/object 与远端一致，checksPassed=true、4 项 checks 全部 passed/exitCode=0、workingTree.clean=true。[正式 compatibility-report](../attachments/s4-formal-compatibility-report.json) 的 candidateRevision=v0.15.0、coverage=ready-for-release-evidence、uncovered=[]。报告内 releaseStatus=release-candidate 是发布前硬门禁报告的模式（scripts/release_evidence.py:437），不是 GitHub 当前发布状态；正式发布事实由已完成 workflow 与 Release metadata 证明，原始报告不改写。

## 安装与 GHCR

使用下载的 install-online.ps1、Skills ZIP 和 sidecar，在全新隔离消费者执行 files 通道安装，exitCode=0。预置合法项目配置 codex / gpt-6.1-sol / high 与 CRLF 格式逐字节保留，AGENTS 自有 CRLF 前缀逐字节保留，governance-guide 与 orchestrator 已安装。见 [formal install verification](../attachments/s4-formal-install-verification.json)。最初测试夹具额外含不支持的 consumer_note 字段，镜像按契约返回 -32602；另用合法夹具完成正向验收，拒绝结果也保留在 [invalid-config verification](../attachments/s4-ghcr-invalid-config-verification.json)。

拉取 ghcr.io/magicvr/goal-governance-mcp-server:0.15.0，RepoDigest `sha256:86e132f950cb758459ea3c8850399039b698cdab515afa9405ef69c3c0a01543` 与 [发布 job](https://github.com/magicvr/goal-governance/actions/runs/43180014952/job/131053513170) 的 [digest 原文](../attachments/s4-ghcr-publish-digest.txt) 一致。实际 server.py --version 返回 goal-governance-mcp 0.15.0；以只读挂载完成 stdio initialize + govern 查询，serverInfo.version=0.15.0、independentAudit=消费者配置、source=.goal-governance.json。前后 160 个文件摘要不变。见 [GHCR verification](../attachments/s4-ghcr-verification.json) 与 [MCP request/response](../attachments/s4-ghcr-mcp-response.json)。

## 下一门禁

I-004 的正式发布与一致性信息已由上述事实验证；S4 保持进行中、Goal active75%，等待发布范围的独立意见与本侧关门响应。运行保证仍为 L0，不把 headless 退出或容器只读查询推导为宿主原生 /goal pause/cancel/resume 已验证。发布收据和最终关门记录将经后续文档 PR 合入 main，不移动 v0.15.0。
