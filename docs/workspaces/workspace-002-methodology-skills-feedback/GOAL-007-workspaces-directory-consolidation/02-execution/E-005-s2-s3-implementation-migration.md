---
id: E-005
goal: GOAL-007-workspaces-directory-consolidation
status: recorded
created: 2026-08-10
updated: 2026-08-10
version: 0.1.0
---

# E-005 · S2/S3 方法论修订与本仓迁移

## 实施事实

- canonical 布局改为 `{governance_root}/workspaces/workspace-<NNN>-<slug>/`；旧直属布局仅触发迁移阻断，新旧并存 fail closed。
- 同步修改 canonical architecture、alignment、directory layout、template、README、AGENTS、治理 prompts、MCP config/doctor/entries/schema、File installer、release packaging 与测试。
- 将本仓三个 workspace 目录整体 `git mv` 到 `docs/workspaces/`，保留所有 workspace/goal id 与历史台账；更新三份 `canonical_scope`。
- 对迁移后的 Markdown 相对链接执行存在性检查，仅在原目标断裂且补一层 `../` 后目标存在时修正；不改历史 runtime JSON 原文。

## 兼容边界

- installer/updater/lifecycle 不静默移动消费仓目录。
- MCP doctor 对 canonical、legacy、mixed、empty 四态只读报告；legacy/mixed 进入 issues。
- 新 scaffold 只创建 `docs/workspaces/workspace-*`；旧直属上下文存在时拒绝写入。

## 待完成

最终 stage/check、全量回归、self + Grok Build independent 审计、PR/CI/main/tag/Release 仍由后续阶段记录。
