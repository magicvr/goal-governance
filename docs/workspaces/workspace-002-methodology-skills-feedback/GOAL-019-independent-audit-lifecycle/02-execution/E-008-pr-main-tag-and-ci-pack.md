---
id: GOAL-019-independent-audit-lifecycle
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-13
updated: 2026-11-13
version: 0.1.0
---

# E-008 · PR、main CI、annotated tag与CI包验收

dev检查点 `69cbeba6b637bcc0c1a08ac687b746d9ea0a6fcb` 后推送dev，创建 [PR #43](https://github.com/magicvr/goal-governance/pull/43)。[PR CI 43445778907](https://github.com/magicvr/goal-governance/actions/runs/43445778907) 的Ubuntu与Windows均success；2026-11-13T14:50:05Z经merge提交 `fbc2d2fbaa0fd8a15a4e30a3f3d92d4bec1eaf33` 合入main。[main CI 43446528299](https://github.com/magicvr/goal-governance/actions/runs/43446528299) 两平台也均success。

本地main在该merge提交的clean tree创建annotated `v0.15.1`，tag object `e32e1bdbb8bea127b32f7c004f4f97736d03de24`，peel为上述main提交。严格release模式本地预检实际执行内部checks，`release-candidate`、`checksPassed: true`、覆盖ready；随后在main CI全绿后推送tag。未移动tag。

[Tag workflow 43447166061](https://github.com/magicvr/goal-governance/actions/runs/43447166061) 的pack job success，包含44对镜像、23份现行信封一致性及pack单测。下载 `skills-pack-0.15.1` artifact（ID14048332004，artifact digest `sha256:abd8a9a6c440ed38545a0665ea670166327afca5f7d76a9f092255aebba43544`），得到7份预发布pack文件。双zip sidecar、Core逐字节子集、实际隔离bootstrap安装exit0、消费者AGENTS原CRLF/项目配置原字节保留、新规则安装均通过：Skills89/Core30成员。包摘要及逐文件清单见附件。

`publish` job当前waiting于仓库既有 `release` Environment：reviewer为magicvr，wait timer为5分钟，自2026-11-13T14:54:22Z开始。发布规则见 `docs/releases/README.md` 正式发布路径第7步。尚未取得人工审批，正式GitHub Release九资产及GHCR尚未发布/验收；I-004为collecting，S4未退出，目标仍active75%。

上述原始API响应、CI包验收、7文件摘要及本地严格预检保存在 `attachments/s4-preparation/`。这是发布准备收据，正式发行证据仍由受保护publish job生成。当前dev已fast-forward到main的merge提交，后续收据与关门将以新的dev文档PR合入main，保持发布tag不变。
