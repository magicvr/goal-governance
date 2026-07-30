---
title: Skills templates pointer (not a second truth)
status: active
created: 2026-07-19
updated: 2026-07-30
parent: null
version: 0.3.0
---

# skills/templates · 已收敛

**GOAL-022**：包内模板分发源为 **`core/docs/templates/`**（由 monorepo `docs/templates/` stage 生成）。

本目录**不再**维护五件套或 `workspace-context.md` 副本。

| 需要 | 使用路径 |
|------|----------|
| 消费仓 install 默认落点 | `docs/templates/`（从 `core/docs/templates` 安装） |
| 包内离线模板 | `skills/core/docs/templates/goal-folder/` |
| monorepo 编辑 | **只改** `docs/templates/`，再运行 `python scripts/stage_skills_mirrors.py` |

遗留路径 `skills/templates/goal-folder` 若出现在旧文档中，请改读 `core/docs/templates/goal-folder`。
