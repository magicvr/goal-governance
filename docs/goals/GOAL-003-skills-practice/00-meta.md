---
id: GOAL-003-skills-practice
title: 完善 Skills 并在本项目中实践验证
status: done
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.2.1
progress: 100%
---

# GOAL-003 · 完善 Skills 并在本项目中实践验证

## 概述

在总目标 [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md) 下，把 Skills 打磨为**可执行、可复用**的协作能力：默认以**单一编排入口**辅助用户完成「设立目标 → 推进目标 → 阶段性/关门审计」，规则与文档原语支撑该流程；并在本项目中实践、反馈、修正。

## 范围

### 在范围内

1. 优化 `skills/AGENTS.template.md`（及安装用规则）使规则可执行
2. **主交付**：单一编排提示词 + 安装/wrapper 主入口，覆盖情境分类与生命周期引导
3. **原语**：创建目标 / 记录决策 / 更新执行 / 写审计（供编排器调用；高级用户可直调）
4. 完善 `skills/templates/goal-folder/` 示例
5. 本项目强制使用、书面反馈；并按偏差审计完成产品面纠正
6. Claude Code / GitHub Copilot 安装路径安装**主入口**（及原语作为 advanced）

### 不在范围内

- Web 数据模型、CRUD
- 自动化校验工具（编号、parent、goal-tree 一致性等）
- 独立运行时 Agent 二进制 / 新 IDE 平台
- 删除历史审计 A-001 / A-002

## 成功标准

### 修订标准（结项以此为准 · A-003 之后）

- [x] **单一主入口**：默认用户路径为编排器（`00-govern-orchestrator` + 对应 install/wrapper），非四个并列填表入口
- [x] **情境分类**：编排器要求扫描项目 / `goal-tree`，区分「无未关门总目的」与「存在未关门目标」
- [x] **设立引导**：无未关门总目的时，引导用户说清第一个/下一个总目的后再创建目标
- [x] **推进引导**：有未关门目标时，分析树并提议下一步（拆解 / 决策 / 执行 / 审计），用户确认后再经原语协助
- [x] **原语降级**：01～04（及旧四 slash）标明为 primitives / advanced，文档与 README 不以四入口为默认产品面
- [x] **规则与安装**：AGENTS 模板或安装规则指向主入口；Copilot 安装至少装上主 wrapper
- [x] **历史地基保留**：AGENTS 可执行、goal-folder 示例、书面反馈记录仍在（见历史标准）

### 历史标准（A-002 时曾作为结项条；alone 不足以对齐核心预期，地基已达成）

- [x] `skills/AGENTS.template.md` 规则可直接照做
- [x] 至少 4 类文档原语提示词可用（新目标 / 决策 / 执行 / 复盘）
- [x] `skills/templates/goal-folder/` 带有可参考示例
- [x] 本仓库曾按 Skills 规则运行并有书面反馈
- [x] 「Skills 使用反馈与修正记录」已产出

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
