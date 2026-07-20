---
id: GOAL-002-project-bootstrap
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.1.0
---

# 决策记录 · GOAL-002

## D-001 · Web 技术栈：FastAPI + Jinja2 + Tailwind CSS + HTMX

**决定**：采用上述组合作为 v0 技术栈。

**为什么**：

- **FastAPI**：Python 生态友好，路由清晰，后续易接 API / 数据层。
- **Jinja2**：服务端模板足够支撑早期页面，无需过早引入 SPA 复杂度。
- **Tailwind CSS**：快速搭界面，当前用 CDN 降低构建成本。
- **HTMX**：以少量 JS 实现局部刷新，适合文档驱动型应用的渐进增强。

**未选方案**：

- 纯静态站点：后续动态与表单成本高。
- 完整前端框架（React/Vue 等）：对当前阶段过重。

## D-002 · Web 应用放在 `web/` 子目录

**决定**：应用代码、模板、静态资源统一放在 `web/`，与 `docs/` 解耦。

**为什么**：

- 文档与代码独立演进，职责边界清楚。
- 根目录保持干净，便于同时维护文档规范与工程配置。
- 虚拟环境仍建议放在仓库根（`.venv`），依赖清单放在 `web/requirements.txt`。

## D-003 · 文档结构：目标中心 + 决策 / 执行 / 审计

**决定**：每个目标固定四类文件：`00-meta`、`01-decision`、`02-execution`、`03-audit`，外加 `attachments/`。

**为什么**：

- 强制闭环：先决策、再执行、后审计，减少「只写计划不复盘」。
- 文件名编号保证阅读顺序稳定。
- 与 Web 三个模块（Decision / Execution / Audit）一一对应，便于后续打通。

## D-004 · 扁平存储 + `goal-tree.md`

**决定**：目标全部平铺在 `docs/goals/`；层级用 `parent` 字段表达，总览写在 `goal-tree.md`。

**为什么**：

- 避免深层嵌套导致路径漂移与重命名困难。
- AI 与脚本更容易枚举、校验、生成树。
- 人读一份 `goal-tree.md` 即可掌握全局进展。

## D-005 · 双交付形态

**决定**：项目同时产出 Web 应用与 Skills/提示词协作能力。

**为什么**：

- Web 服务「看与操作」；Skills 服务「写与推进」。
- 同一套目标文档是双方共享的真相来源（source of truth）。
