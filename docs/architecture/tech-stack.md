---
title: 技术栈
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.3.0
---

# 技术栈

## 核心方法论与文档协议（canonical）

| 层 | 路径 | 说明 |
|----|------|------|
| 方法论 | `docs/architecture/` | P-001～P-005、架构与长期约定 |
| 文档规范 | `docs/README.md` | 目标实例、五件套和同步规则 |
| 模板 | `docs/templates/goal-folder/` | canonical 五件套模板；不保存运行状态 |
| 实例真相源 | `docs/goals/` | 目标、决策、执行、审计和附件 |

`skills/templates/goal-folder/` 是上述 canonical 模板的分发镜像，用于离线安装和复制到其他仓库；它不构成第二套规范。

## Web 应用（已确定）

| 层 | 技术 | 说明 |
|----|------|------|
| 后端 | Python 3.10+ / FastAPI | 路由、模板渲染、后续 API |
| 模板 | Jinja2 | 服务端 HTML |
| 样式 | Tailwind CSS（CDN） | 快速布局，暂无构建管线 |
| 交互 | HTMX（CDN） | 渐进增强，减少自写 JS |
| 服务器 | Uvicorn | ASGI |

依赖清单：[web/requirements.txt](../../web/requirements.txt)

## 文档

| 项 | 约定 |
|----|------|
| 格式 | Markdown + YAML Frontmatter |
| 目标模型 | 扁平目录 + `parent` + `goal-tree.md` |
| 每目标文件 | meta / decision / execution / audit + attachments |

## 运行位置

- 应用代码：`web/`
- 建议虚拟环境：仓库根 `.venv`
- 启动方式见 [web/README.md](../../web/README.md)

## 明确未采用（当前阶段）

- 前端 SPA 框架（React / Vue 等）
- 数据库（Postgres 等）— 目标仍以 Markdown 文件为主
- 认证 / 多租户
- Tailwind 本地构建管线（后续可按需引入）

## 三层交付中的 Skills

- 形态：提示词、Agent 规则、宿主 wrappers、安装脚本和可复制模板镜像
- 入口规则：根目录 [AGENTS.md](../../AGENTS.md) 与 `skills/prompts/00-govern-orchestrator.md`
- 消费关系：读取核心方法论与文档协议，驱动 AI 在 `docs/goals/` 中执行闭环
- 实现状态：**当前基线已交付**；核心协议对齐、镜像漂移检查和跨宿主发布验收属于后续阶段
