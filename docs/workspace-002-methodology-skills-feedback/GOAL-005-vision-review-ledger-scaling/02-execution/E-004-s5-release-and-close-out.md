---
id: E-004
goal: GOAL-005-vision-review-ledger-scaling
title: S5 正式发布与闭门
status: recorded
created: 2026-08-06
updated: 2026-08-06
version: 0.1.0
---

# E-004 · S5 正式发布与闭门

## 事实

- PR #11（`codex/vision-review-ledger-scaling` → `main`）CI 双 job 全绿后以 merge commit `33934efc83e24e78435e469832dd38266474e8ad` 合入；分支 5 个提交（e4ccb35 → bb1f745）全部可达于 `origin/main`。
- S5 前置缺陷在仓内修复并补测试：`release_evidence.py` 失败路径打印失败 check 明细（含输出 tail）；`test_release_evidence.py` 临时 git fixture 禁用 auto-gc（`gc.auto=0`）消除 Linux runner 上 `Errno 39 Directory not empty: 'objects'` 的清理竞态（runner 上连续 3 次失败 → 修复后连续 2 次通过）。
- annotated `v0.13.0` tag（tag object `29d5b28c`）指向 merged-main `33934efc`，已推送远端。
- `skills-pack-release` workflow run [`31073547050`](https://github.com/magicvr/goal-governance/actions/runs/31073547050)（push tag 触发）：pack job 成功；publish job 经 Environment `release` 门（wait timer 5 分钟 + repo owner 批准，`current_user_can_approve=true`）后 release-mode evidence 全部 check 通过，`gh release create` 并上传 9 项资产。
- GitHub Release [`v0.13.0`](https://github.com/magicvr/goal-governance/releases/tag/v0.13.0) 资产：`goal-governance-skills-v0.13.0.zip` + `.sha256`、`goal-governance-core-v0.13.0.zip` + `.sha256`、`install-online.ps1`、`install-online.sh`、`bootstrap-README.md`、`release-evidence.json`、`compatibility-report.json`。
- 本地重新下载后：skills zip sha256 `e48e1c3a…`、core zip sha256 `24d5db6f…` 与发布 sidecar 逐项一致；`release-evidence.json` release 模式（tag `v0.13.0`、commit `33934efc`、`checksPassed=true`，4 项 check 全过）。
- 隔离消费方（`%TEMP%\gg-consumer-v013`，无 monorepo 访问）：包边界检查通过（`docs/workspace-*`/`web/`/`__pycache__`/`tech-stack.md`/`artifacts/`/`.git` 均为 0，仅模板 `.gitkeep` 占位）；bootstrap 离线安装（SHA-256 校验 → `install.ps1 -All` 四入口 + core docs）成功；`update.ps1 --version 0.13.0 --dry-run`（`result=dry-run`）与 real update（`result=updated`，`rollback_path` 落盘）成功；`.goal-governance-install.json` 版本 `0.13.0`、protocol `0.1.0`、`archiveSha256` 与发布摘要一致。
- 闭门记录：D-003 闭门决策、A-005 闭门审计；GOAL-005 `done / 100%`；Root GOAL-001（`done`）与 VP-002（`active`）状态未变。

## 边界

以上事实覆盖 S5 全链路与闭门；不涉及 Root R3 自动关闭或新目标创建。
