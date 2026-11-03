---
id: GOAL-017-on-demand-governance-context
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-03
updated: 2026-11-03
version: 0.1.0
---

# E-008 · 正式资产与 GHCR 验收

[v0.14.0](https://github.com/magicvr/goal-governance/releases/tag/v0.14.0) 于2026-11-03T10:54:46Z发布，[run41622193036](https://github.com/magicvr/goal-governance/actions/runs/41622193036) completed/success。annotated tag object dd387ceea63d7d97aba0b09b575634dbdcd373d0 → main合并提交10bba8600b4d8575b6d6230bac2529795ae7129c；不改tag。

## 正式9资产

使用 `gh release download v0.14.0` 新目录下载，与GitHub资产元数据逐项比较、ZIP与sidecar摘要比较，均通过。7项pack文件与先前CI候选文件逐字节一致；其余两项为CI生成的release-evidence与compatibility-report。

- Skills ZIP 88成员，Core ZIP 29成员；Core在Skills的core/下逐字节一致，missing0/mismatch0。
- 最小入口17行/1374 UTF-8 bytes；完整指南和入口模板都在Core资产。
- release-evidence：release-candidate、checksPassed=true、全部checks=true、clean=true、commit/tag/tagObject均与实际一致。
- compatibility-report：candidateRevision=v0.14.0，ready-for-release-evidence，uncovered0，同一提交。
- [逐文件摘要与比对](../attachments/s4-published-asset-verification.json)、[Release元数据](../attachments/s4-release-metadata.json)、[发布证据](../attachments/s4-published-release-evidence.json)、[兼容报告](../attachments/s4-published-compatibility.json)。

## 真实消费安装与镜像

下载的install-online.ps1、Skills ZIP和sidecar在全新隔离目录运行：`-Version 0.14.0 -Channel files -Force -ZipPath <downloaded zip> -Sha256Path <downloaded sidecar> -TargetDir <isolated consumer>`，exit0。安装前AGENTS中消费方自有CRLF前缀逐字节保留；最小入口指向安装后的完整指南，指南存在。见[安装日志](../attachments/s4-published-install.txt)。

`docker pull ghcr.io/magicvr/goal-governance-mcp-server:0.14.0` 成功；RepoDigest=sha256:0579508b6412de67955f8d748ea4796dda28e18020d25ae00e6c9ec775a284dd，与CI构建日志一致；实际容器 `server.py --version` 输出 `goal-governance-mcp 0.14.0`。见[结构化核验](../attachments/s4-install-and-ghcr-verification.json)、[拉取日志](../attachments/s4-ghcr-pull.txt)、[版本](../attachments/s4-ghcr-version.txt)。

## 人工放行事实与当前状态

用户本会话确认已在GitHub授权；[最终审批原始记录](../attachments/s4-approvals-final.json)保留magicvr skipped、github-actions[bot] approved/comment5 minute wait timer。[最终workflow记录](../attachments/s4-published-workflow.json)为成功；不声称magicvr普通approved，AI未代批/修改Environment。

I-004 verified，所有信息门禁证据齐备；A-004 self/pass。为覆盖A-002排除的S4发布范围，继续用用户指定Grok4.7/xhigh执行正式独立复核；在返回前仍active / 75%，S4关门检查点未完成，Root active / 67%。
