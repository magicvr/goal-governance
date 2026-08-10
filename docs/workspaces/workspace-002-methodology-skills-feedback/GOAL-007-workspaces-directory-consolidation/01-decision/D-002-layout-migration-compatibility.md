---
id: D-002
goal: GOAL-007-workspaces-directory-consolidation
status: accepted
created: 2026-08-10
updated: 2026-08-10
version: 0.1.0
---

# D-002 · 工作区布局迁移与兼容策略

## 决定

1. 新的唯一 canonical 显式工作区布局为 `{governance_root}/workspaces/workspace-<NNN>-<slug>/`；`workspaces/` 只容纳显式工作区，不成为第二套状态或目标层级。
2. 旧的 `{governance_root}/workspace-<NNN>-<slug>/` 仅作为待迁移布局检测，不再允许新建、推进、放行或关门。
3. 若只发现旧布局，工具与 AI 必须 fail closed 并给出迁移指引；不得将其当成新 canonical 继续写入。
4. 若新旧布局同时存在，视为混合布局冲突并 fail closed；禁止双读、合并推断或任选一侧。
5. installer/updater/lifecycle 不静默移动消费仓用户目录。新建工作区只写新路径；升级只更新受管包并报告旧布局门禁。
6. 本 monorepo 的三个工作区在同一受控变更内显式迁移，使用 Git rename 语义保留历史；迁移后根 `docs/` 不保留活动 `workspace-*` 目录。
7. Q2 canonical 引用改为 `{governance_root}/workspaces/workspace-<NNN>-<slug>/GOAL-NNN-slug/`；Q1/Q3 与 workspace id 不变。

## 理由

自动移动消费仓目录会改变用户数据边界，且 updater 现有 rollback 只覆盖受管文件，不能可靠回滚任意工作区内容。长期双布局则会制造两套活动真相。显式 fail-closed 迁移门禁能保持单一 canonical，又避免升级器越权。

## 验收断言

- new-only：可正常发现、创建与推进。
- old-only：只报告迁移阻断，不写入。
- mixed：明确冲突并 fail closed。
- 本仓迁移后：`docs/workspaces/workspace-001|002|003-*/workspace.md` 均与 canonical scope 一致，旧直属 `docs/workspace-*` 活动目录为 0。
