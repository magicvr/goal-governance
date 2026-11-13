---
id: GOAL-019-independent-audit-lifecycle
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-13
updated: 2026-11-13
version: 0.1.0
---

# E-009 · 正式发布、九资产与GHCR验收

[Tag workflow 43447166061](https://github.com/magicvr/goal-governance/actions/runs/43447166061) 的pack与publish均success。[Release v0.15.1](https://github.com/magicvr/goal-governance/releases/tag/v0.15.1) 于2026-11-13T15:01:25Z正式发布，draft=false、prerelease=false、9资产。Environment放行历史原始记录为magicvr/skipped及“5 minute wait timer”的github-actions[bot]/approved；本任务通过既有workflow的实际发布门禁，相关API原文保存在 `attachments/s4-formal/`。

远端annotated tag object仍为 `e32e1bdbb8bea127b32f7c004f4f97736d03de24`，指向main merge `fbc2d2fbaa0fd8a15a4e30a3f3d92d4bec1eaf33`。正式下载的release-evidence与compatibility-report均绑定该提交；release硬门禁内部检查通过、覆盖ready。矩阵/contract摘要与tag对应Git blob一致；Skills包89个文件逐字节对应tag的 `skills/` 源，三份bootstrap资产也逐字节对应tag源，见 `attachments/s4-release-source-binding.json`。比较使用tag blob，不把本地文本checkout换行差异当作发行漂移。

9份正式资产全部下载并逐项匹配GitHub API名称、大小、SHA-256；双zip sidecar正确，Core30成员为Skills89成员中core的逐字节子集。正式下载的bootstrap驱动全新隔离消费安装exit0，消费AGENTS原CRLF及项目配置原字节保留，新生命周期规则与完整指南已安装。实际收据及stdout/stderr见 `attachments/s4-formal-file-assets*`。

GHCR镜像 `ghcr.io/magicvr/goal-governance-mcp-server:0.15.1` 已拉取，RepoDigest与workflow build/push日志均为 `sha256:0b837930b43db78f661126c325b0bf3ea7029bb758b14862b9bbcdb6045c90d6`。按此digest、只读挂载正式消费仓启动容器，实际stdio initialize返回serverInfo.version=0.15.1，tools/list含四治理入口及四管理入口，exit0。见 `attachments/s4-ghcr-image-verification.json` 及stdout/stderr；此为镜像接受检查，未执行独立审计。

I-004按上述实际证据verified。A-005为S4事实自审，目标仍active75%，S4尚须最后指定provider的独立关门意见与响应，不能因资产已存在提前done。发布后收据与关门通过后续dev文档PR合入main；保持既有发布tag不变。
