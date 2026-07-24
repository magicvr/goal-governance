---
id: GOAL-019-skills-consumer-workspace-bootstrap
title: Skills 消费方工作区骨架落地（空仓可运行）
status: done
parent: GOAL-001-main-vision
created: 2026-07-24
updated: 2026-07-24
version: 1.0.0
progress: 100%
---

# GOAL-019 · Skills 消费方工作区骨架落地（空仓可运行）

## 有界关门（2026-07-24）

本目标 `done / 100%` 关闭的是 **GOAL-019 成功标准全表**（A–C 实现 + A-001 响应 + 自审 A-002）：

1. skills zip **内嵌 core** 并 **install 默认**装到 `docs/architecture` + `docs/templates` + 精简 `docs/README`
2. S0/`01` 空仓 scaffold + slug 用户确认（D-005）
3. 可选 `--init-workspace`（D-006；显式 slug；不建 Root 五件套）
4. pack/README/宿主 wrappers 与隔离证据
5. A-001 findings：F-001 closed；F-002 closed（补测）；F-003/F-004/I-005 residual 已书面接受

**不**构成：Marketplace、强制 bash 跨平台 CI 冒烟（见 residual）、standalone-bootstrap 全文重写（I-005 residual）、宿主 runtime 证据全量刷新。

## Residual（关门后）

| ID | 级别 | 说明 | 复审触发 | 状态 |
|----|------|------|----------|------|
| **R-019-SH-RUNTIME** | non-blocking | install.sh 端到端隔离冒烟未在 Windows 本环境 bash 复跑；静态断言 + ps1 隔离为主证据 | 增加 bash CI job 或维护者在 Linux/macOS 跑 sh 冒烟 | open residual |
| **R-019-STANDALONE-COPY** | non-blocking | `docs/standalone-bootstrap.md` 未全文改写为「有 Skills 时主路径=core 内嵌 install」；skills README 已标主路径（I-005） | 下次触达 standalone / GOAL-006 文档 | open residual |
| **R-019-I001-INSTALL-SHAPE** | non-blocking | 消费方「仅拷宿主 skill vs 完整 zip+install」形态未做现场统计（I-001） | 外部试点反馈 | open residual |

## 概述

承接对外 Skills 资产在**其他项目**安装后的体验缺口：消费方装完 zip/`install` 后往往没有治理**存储骨架**，也没有 **`docs/architecture` 核心方法论**，只剩适配器入口——半成品。

本目标关闭两件事（D-003）：

1. **核心方法论与 Skills 同级必备**：skills zip **内嵌 core 镜像**，`install` **默认**安装到目标仓 `docs/architecture/`（及 templates/入口）。
2. **工作区真相源 scaffold**：空仓可建立 `docs/workspace-…` + `goal-tree`；Root 由 `/govern` 创建。

## 成功标准

- [x] **Core 镜像（D-004）**
- [x] **默认安装（D-004 落点）**
- [x] **打包** required + 拒 tech-stack
- [x] `install.ps1` Next steps 对齐 workspace
- [x] `skills/README.md` 最小可运行集 + core 同级必备
- [x] S0 与 `01` scaffold；slug 用户确认（D-005）
- [x] AGENTS / wrappers 必备话术（含 monorepo 根 AGENTS §11，A-001 F-001）
- [x] 可选 `--init-workspace`（D-006）
- [x] 临时空目录隔离冒烟（ps1；sh 见 R-019-SH-RUNTIME）
- [x] 阶段/关门审计：无未关闭 **required** finding（A-001 响应 + A-002 self）

## 高层路线图

| 阶段 | 内容 | 状态 |
|------|------|------|
| **A** | core 镜像 + pack + install 默认 + README | **完成** |
| **B** | S0/01 + AGENTS 必备话术 | **完成** |
| **C** | `--init-workspace` + 隔离证据 | **完成** |
| **D** | A-001 响应 + self + 有界关门 | **完成**（2026-07-24） |

## 信息就绪与未知项

| ID | 级别 | 状态 | 证据 / 结论 |
|----|------|------|-------------|
| I-001 | non-blocking | **accepted-residual** | → R-019-I001-INSTALL-SHAPE |
| I-002 | non-blocking | **closed** | D-006 |
| I-003 | required | **closed** | D-005 |
| I-004 | required | **closed** | D-004 |
| I-005 | non-blocking | **accepted-residual** | → R-019-STANDALONE-COPY；skills README 主路径已标 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 相关目标

- [GOAL-006](../GOAL-006-core-methodology-template-productization/00-meta.md)
- [GOAL-010](../GOAL-010-core-workspace-shared-materials-protocol/00-meta.md)
- [GOAL-018](../GOAL-018-skills-release-packaging/00-meta.md)
