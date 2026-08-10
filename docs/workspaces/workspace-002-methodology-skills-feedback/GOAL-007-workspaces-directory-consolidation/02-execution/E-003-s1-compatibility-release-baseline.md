---
id: E-003
goal: GOAL-007-workspaces-directory-consolidation
status: recorded
created: 2026-08-10
updated: 2026-08-10
version: 0.1.0
---

# E-003 · S1 兼容与发布基线核验

## 安装/升级面

- `skills/install.sh` 与 `skills/install.ps1` 当前将新工作区写到 `docs/workspaces/workspace-*`。
- `skills/update.py` 只更新受管包并调用 installer，没有工作区迁移或发现逻辑。
- MCP config/entries 将旧 `workspace-*` 内部布局视为冻结，ledger allowlist 仍使用旧 glob。
- 现有测试覆盖旧 scaffold 路径，但没有 old-only/new-only/mixed 三态门禁。

因此 D-002 选择不在 updater/lifecycle 中静默搬迁用户目录；旧布局只检测并阻断写入，本仓由受控 Git 迁移完成。

## 发布面

- 本地最新 tag `v0.13.1` 是 annotated tag，peeled commit `a10a98f`；当前 `dev` HEAD 位于其后。
- `docs/contracts/skills-consumer-compatibility-matrix.json` 的 candidateRevision 仍是 `v0.13.1`。
- Release workflow 在 tag/ref、clean tree、matrix、CHANGELOG、CI/evidence、Environment `release` 和资产集合上 fail closed。

据此 D-003 冻结本目标候选为 `v0.13.2`。S1 仍未完成，因为 I-002 provider 尚未关闭。
