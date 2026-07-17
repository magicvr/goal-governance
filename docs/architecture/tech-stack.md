---
title: 技术栈
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
---

# 技术栈

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

## 双交付中的 Skills

- 形态：提示词 / Agent 规则 / 后续可打包的 Skill 文件
- 入口规则：根目录 [AGENTS.md](../../AGENTS.md)
- 实现状态：**方向已定，具体 Skill 未落地**
