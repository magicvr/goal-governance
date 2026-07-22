---
id: GOAL-006-core-methodology-template-productization
title: 核心方法论、文档协议与 canonical 模板产品化
status: done
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.6.0
progress: 100%
---

# GOAL-006 · 核心方法论、文档协议与 canonical 模板产品化

## 概述

承接 [GOAL-001 D-008](../GOAL-001-main-vision/01-decision.md#d-008--阶段-4-产品化与退出契约2026-07-19) 的阶段 4 最小交付包：将既有核心方法论、文档协议与 canonical 模板整理为可独立复制、可验证、可版本化演进的核心交付包。

本目标只交付核心文档层的事实证据，不把 Skills 多宿主发布、Web 写入或三面联合发布提前并入阶段 4。

## 范围

### 在范围内

1. 核对并完善 `docs/README.md`、`docs/architecture/` 与根 `AGENTS.md` 的核心入口，使目标存储、五件套、路线图和审计闭环可被找到。
2. 确认 `docs/templates/goal-folder/` 作为唯一 canonical 模板上游，且五件套与 `attachments/` 起点可脱离 Skills/Web 理解和使用。
3. 补齐由核心文档层持有的独立启用说明，并在不安装 `skills/`、不启动 `web/` 的空 Git 仓库中复现 Root Goal 初始化。
4. 记录可复制包版本/变更范围，并在 canonical 模板变更时同步 `skills/templates/goal-folder/`，运行镜像一致性验证。
5. 在阶段审计中核对上述证据；没有开放 required finding 后，才具备阶段 4 → 5 的放行条件。

### 不在范围内

- Skills 多宿主安装、发布或兼容性验收。
- Web 写入、创建/更新界面、独立数据库或写入同步。
- 三层联合发布、跨面漂移检测或阶段 7 发布验收。
- 对 P-001～P-004 语义的修改。

## 成功标准

- [x] 核心文档入口可定位目标存储、五件套、路线图和审计闭环，且入口路径可核对。
- [x] `docs/templates/goal-folder/` 保持完整五件套和 `attachments/` 起点，并可脱离 Skills/Web 作为模板使用。
- [x] 核心文档层包含独立启用说明；空 Git 仓复制场景可生成 `docs/goals/goal-tree.md` 与合规 Root Goal，并留有来源、生成路径和核对结果。
- [x] 可复制包版本/变更范围、canonical → Skills 模板镜像同步及其验证结果均有可核对记录。
- [x] 阶段审计确认无开放 required finding；未在阶段 4 完成前放行阶段 5。

## 工作顺序

1. [x] 核对核心入口与 canonical 模板的现状，明确需要补充的内容。
2. [x] 编写或修正独立启用说明，并执行空 Git 仓复制验证。
3. [x] 记录版本与镜像同步事实，运行相关验证。
4. [x] 对成功标准和证据做阶段审计（A-001 pass）；A-002 的 F-002 已响应并经 A-004 targeted 独立复审通过，A-005 完成正式 close-out；阶段 5 尚未启动。

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 相关决策

- [GOAL-001 D-008](../GOAL-001-main-vision/01-decision.md#d-008--阶段-4-产品化与退出契约2026-07-19) · 阶段 4 产品化与退出契约
