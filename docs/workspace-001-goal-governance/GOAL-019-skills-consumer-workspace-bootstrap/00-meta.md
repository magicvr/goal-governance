---
id: GOAL-019-skills-consumer-workspace-bootstrap
title: Skills 消费方工作区骨架落地（空仓可运行）
status: active
parent: GOAL-001-main-vision
created: 2026-07-24
updated: 2026-07-24
version: 0.4.0
progress: 45%
---

# GOAL-019 · Skills 消费方工作区骨架落地（空仓可运行）

## 概述

承接对外 Skills 资产在**其他项目**安装后的体验缺口：消费方装完 zip/`install` 后往往没有治理**存储骨架**，也没有 **`docs/architecture` 核心方法论**，只剩适配器入口——半成品。

本目标关闭两件事（见 [D-003](01-decision.md#d-003--核心方法论与-skills-同级必备内嵌-core-镜像默认安装2026-07-24)）：

1. **核心方法论与 Skills 同级必备**：skills zip **内嵌 core 镜像**，`install` **默认**安装到目标仓 `docs/architecture/`（及约定的 templates/入口）。
2. **工作区真相源 scaffold**：空仓可建立 `docs/workspace-…` + `goal-tree` + Root 引导路径。

**仍不**打包 monorepo dogfood 过程树（`docs/workspace-001-goal-governance/GOAL-*`）或本仓 Web/实现专属内容。

## 背景（已确认事实）

2026-07-24 `/govern` 诊断 + 用户裁决：

| 观察 | 判定 |
|------|------|
| 目标项目无 dogfood 目标树 | **按设计**：过程数据不进发布物 |
| 目标项目无 `docs/architecture/*` | **产品缺陷**（D-003 纠正：不得再标「可选」）；方法论与 Skills 同级必备 |
| 安装不 scaffold 工作区；S0/`01` 弱 | **真缺口** |
| `install.ps1` Next steps 仍指向 legacy `docs\goals\` | **真缺口** |

相关：GOAL-006（核心可独立启用——**不**否定与 Skills 共交付）、GOAL-010、GOAL-018（skills-only 边界由 D-003 **扩展**为 skills+core 镜像，仍排除 dogfood）。

## 成功标准

- [x] **Core 镜像（D-004）**：`skills/core/docs/` 含 principles + workspace-protocol + overview/layout + templates + 精简 README；无 tech-stack
- [x] **默认安装（D-004 落点）**：`install.sh` / `install.ps1` 任意宿主安装均调用 core → `./docs/`
- [x] **打包**：`pack_skills_release` required 校验 core 文件；拒 tech-stack；单测覆盖
- [x] `install.ps1` Next steps 与 `install.sh` 一致：`docs/workspace-…`（非 legacy `docs\goals\`）
- [x] `skills/README.md`：**最小可运行集** + core 同级必备
- [ ] 编排器 S0 与 `01-create-new-goal`：空仓先 scaffold 工作区根（**阶段 B**）
- [ ] 可选：`--init-workspace`（**阶段 C**）
- [x] 临时空目录：`install.ps1 -All` 隔离冒烟断言 core 落点（结构证据）
- [ ] 阶段/关门审计无未关闭 required finding

## 非目标（本目标不交付）

- monorepo dogfood 目标树进 zip
- Marketplace、协议大版本升级、强制刷新全部宿主 runtime 证据
- **单独**再维护一套与 zip 无关的「仅 core 迷你包」作为主路径（GOAL-006 standalone 可保留为**无 AI 时**的次路径，主消费路径以 D-003 为准）
- Web 工作台安装或生产写入放行
- 把本仓 `tech-stack` 全量当作消费方强制依赖

## 高层路线图

| 阶段 | 内容 | 状态 |
|------|------|------|
| **A** | 冻结 core 清单 + pack 内嵌镜像 + install 默认安装 architecture/templates；修 `install.ps1` 引导；README 最小可运行集（含 core 必备） | **完成**（2026-07-24） |
| **B** | 强化 S0 / 原语 01 空仓工作区 scaffold；AGENTS/prompts 引用已装 core，不再写「architecture 整体可选」 | 待开始 |
| **C** | 可选 `--init-workspace` + 隔离可复现证据；canonical↔镜像一致性测试 | 待开始 |
| **D** | 阶段审 / 有界关门 | 待开始 |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | non-blocking | 消费方常见安装形态：仅拷宿主 skill 还是完整 zip + `install` | C 是否补「无 install 手拷 core」说明 | C | 用户反馈 | open | — | 形态待细化 |
| I-002 | non-blocking | 是否必须实现 `--init-workspace` | C 范围 | C | 用户裁决 | open | — | 倾向「有则更好」 |
| I-003 | required | 空仓 scaffold 的工作区/Root slug 策略 | B 实施 | B | 用户确认后写 prompts | open | — | 不得静默假定 |
| I-004 | required | Core 镜像精确文件清单与目标路径映射 | A pack/install | A 实施 | 用户清单 → D-004 | **closed** | — | [D-004](01-decision.md#d-004--core-镜像文件清单与安装映射关闭-i-004)：principles + workspace-protocol + overview/layout（去 monorepo 段）+ templates + 精简 docs/README；不装 tech-stack |
| I-005 | non-blocking | GOAL-006 standalone-bootstrap 文案如何与 D-003 主路径并存 | A 文档 | A | skills README 已写主路径；standalone 全文改写可延后 | deferred | 责任人：维护者；复核：阶段 B 或下次 standalone 触达 | skills README 已标明 core 默认 install 为主路径 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 相关目标

- [GOAL-006](../GOAL-006-core-methodology-template-productization/00-meta.md) · 核心层独立启用
- [GOAL-010](../GOAL-010-core-workspace-shared-materials-protocol/00-meta.md) · 工作区协议
- [GOAL-018](../GOAL-018-skills-release-packaging/00-meta.md) · Skills Release 打包路径
