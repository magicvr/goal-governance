---
title: 技术栈
status: active
created: 2026-07-18
updated: 2026-08-04
parent: null
version: 0.6.0
---

# 技术栈

## 核心方法论与文档协议（canonical）

| 层 | 路径 | 说明 |
|----|------|------|
| 方法论 | `docs/architecture/` | P-001～**P-006**、架构与长期约定 |
| 愿景规则 | `docs/vision/alignment.md` | 单愿景对齐门禁（非 goal-tree） |
| 文档规范 | `docs/README.md` | 目标实例、五件套和同步规则 |
| 模板 | `docs/templates/goal-folder/` | canonical 五件套模板；不保存运行状态 |
| 工作区上下文 | `docs/workspace-<NNN>-<slug>/workspace.md` | 绑定 Root Goal、工作区根范围、plan 字段和共享资料固定引用；不保存目标状态 |
| 实例真相源 | `docs/workspace-<NNN>-<slug>/` | 目标、决策、执行、审计和附件 |

`skills/core/docs/templates/` 是上述 canonical 模板的分发镜像（由 `scripts/stage_skills_mirrors.py` 生成），用于离线安装；不构成第二套规范。工作区和共享资料细节见 [workspace-protocol.md](workspace-protocol.md)。

## 人类 UI（远期，未绑定实现）

本仓冻结的 FastAPI Web 资产已由 workspace-002 GOAL-004 物理退役。未来人类 UI 仍属于 VP-003 远期适配器类；在通用基架和新的书面决策落盘前，不指定后端、模板、样式、交互或服务器栈。

## 文档

| 项 | 约定 |
|----|------|
| 格式 | Markdown + YAML Frontmatter |
| 目标模型 | 扁平目录 + `parent` + `goal-tree.md` |
| 每目标文件 | meta / decision / execution / audit + attachments |

## 运行位置

- 建议虚拟环境：仓库根 `.venv`
- 当前没有本仓应用启动入口；未来 UI 另按新目标登记。

## 明确未采用（当前阶段）

- 前端 SPA 框架（React / Vue 等）
- 数据库（Postgres 等）— 目标仍以 Markdown 文件为主
- 认证 / 多租户
- 任何具体 UI 栈（待 VP-003 重新激活后选型）

## 三层交付中的 Skills

- 形态：提示词、Agent 规则、宿主 wrappers、安装脚本和可复制模板镜像
- 入口规则：根目录 [AGENTS.md](../../AGENTS.md) 与 `skills/prompts/00-govern-orchestrator.md`
- 消费关系：读取核心方法论与文档协议，驱动 AI 在已验证的工作区根中执行闭环
- 实现状态：**当前基线已交付**；核心协议对齐、镜像漂移检查和跨宿主发布验收属于后续阶段
