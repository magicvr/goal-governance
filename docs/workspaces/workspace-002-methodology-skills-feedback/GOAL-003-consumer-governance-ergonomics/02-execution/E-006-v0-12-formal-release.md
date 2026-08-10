---
id: GOAL-003-consumer-governance-ergonomics
doc: execution-entry
record_id: E-006
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-006 · v0.12.0 正式 Release 与真实消费更新

## 已发生事实

- release-candidate checkpoint `0748c8d8480e7f87f23578b60ec24dc809d6d8d7` 创建 annotated tag `v0.12.0`；tag object 为 `d969de55b69785fb107ff2747fc4bd401171412b`，远端 tag peel 到同一 commit。
- 本地 strict `release_evidence.py --mode release --tag v0.12.0 --run-checks --include-web` 通过：`releaseStatus: release-candidate`、`checksPassed: true`、工作树 clean、compatibility `ready-for-release-evidence`。
- 只推送 `refs/tags/v0.12.0`；未额外推送此前已领先的 `dev` 分支。GitHub Actions run [`30859281729`](https://github.com/magicvr/goal-governance/actions/runs/30859281729) 的 pack 与 gated publish 均成功；Environment `release` 的 reviewer / wait timer 正常通过，没有手工绕过 strict evidence。
- 正式 [GitHub Release v0.12.0](https://github.com/magicvr/goal-governance/releases/tag/v0.12.0) 于 `2026-08-03T22:42:05Z` 发布，非 draft / prerelease；9 个资产含 skills/core zip + sha256、PowerShell/Bash bootstrap、bootstrap README、compatibility report 与 release evidence。
- 官方 skills zip SHA-256 为 `b7407b01ba492e1e6c2d6444be2e609c7a9d5d80a4a641dbcbe9eb04a166ccb0`；core zip 为 `05236aa06b59b6b3925ac2da8bcbbc792f522ae21dad6b87084295aa097c8f7f`。两者与 sidecar 和 Release asset digest 一致。
- skills zip 含 `update.py` / `update.ps1` / `update.sh` 与升级指南；只含 consumer contract + schema，producer-only compatibility matrix、runtime/release evidence 均为 0 项。

## 真实消费更新

隔离消费项目位于临时核验目录 `goal-governance-v0.12.0-release-verification-30859281729/consumer-project`：

1. 用正式 Release 的 `install-online.ps1`、skills zip 与 sidecar 完成首次 `0.12.0 -All` bootstrap；四宿主入口、core 与 consumer-only contract 落盘。
2. 已安装 `skills/update.ps1 --version 0.12.0 --dry-run` 在线固定版本复核：当前/目标协议均 `0.1.0`，archive SHA-256 为上述正式 hash，managed conflicts 为空，result 为 `dry-run`。
3. 再执行同一在线固定版本的真实事务：result `updated`；`skills/.goal-governance-install.json` 记录 version `0.12.0`、source `magicvr/goal-governance@v0.12.0`、正式 archive hash 与 rollback path。
4. rollback 目录 `20260803T224534Z-v0.12.0` 存在；3 个 updater、Claude/Grok/Codex/Copilot 入口均存在；consumer contracts 仅 contract + schema；producer-only 文件计数 0。

这是首个包含 updater 的正式版本，因此证据是“正式 bootstrap 后的同版本真实事务”，不是 `v0.11.0 -> v0.12.0` 自升级，也不宣称跨版本更新已经验证。

## 独立复核

- 前两次 Grok 尝试没有产出 verdict，按 D-005 fail closed 排除，不进入意见台账。
- 最终 Grok Build `0.2.118` / `grok-4.5` session `019fc9d5-02ac-7ff2-b8ed-d611cf4f36df` 在 `read-only` sandbox 中独立点验，`stopReason: end_turn`；A-006 verdict `pass`，F-001 `fixed`，开放 required = 0。
- workflow 唯一 annotation 是 GitHub runner 对 Node 20 actions 的弃用提醒；运行时/本地既有 WSL Bash 与 Windows symlink skips 继续按 E-005 单列，不写成通过。

## 关门记录验证

- Docs `26`、Skills 编排 `42`、scripts `72` 项通过；scripts `3` 项按既有平台边界跳过。
- Web 从组件目录使用项目解释器运行 `143` 项通过、`1` 项跳过。此前一次从仓库根使用错误 discovery 路径与解释器的调用产生 import errors；该调用不符合正式门禁命令，已排除，未写成产品失败或通过。
- canonical -> Skills 镜像 `34` 对一致；compatibility `--require-ready` 为 `ready-for-release-evidence`；A-006 JSON 可解析；`git diff --check` 通过。
