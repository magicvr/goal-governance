---
title: 核心目标文档模板
status: active
created: 2026-07-19
updated: 2026-07-19
parent: null
version: 0.1.0
---

# 核心目标文档模板

这里是 Goal Governance 的 **canonical 模板层**。它属于核心方法论与文档协议，不属于 Web，也不依赖任何 AI 宿主。

## 目录

`goal-folder/` 包含一个目标的完整五件套：

- `00-meta.md`：目标元信息、成功标准与父子关系
- `01-decision.md`：决定、理由与未选方案
- `02-execution.md`：按时间线记录可核对事实
- `03-audit.md`：阶段复盘与 `self` / `independent` 审计意见
- `attachments/`：可选证据附件目录

## 使用边界

- 新目标实例仍创建在 `docs/goals/`，并遵守根目录 `AGENTS.md` 与 `goal-tree.md`。
- 本目录只定义可复用的文档结构与写作起点，不是运行中的目标记录。
- `skills/templates/goal-folder/` 是面向离线复制与安装脚本的分发镜像；修改模板时先改本目录，再同步镜像。
- Web 读取生成的目标实例，不读取本目录来推断目标状态。

## 版本与同步

模板变更应同时更新本文件的 `updated` / `version`，并用仓库测试核对 `docs/templates/goal-folder/` 与 `skills/templates/goal-folder/` 的四个 Markdown 文件一致。
