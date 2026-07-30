---
id: GOAL-002-codex-skills-entry
title: 添加 Codex 可用的 Skills 入口
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-07-31
updated: 2026-07-31
version: 0.4.0
progress: 100%
---

# GOAL-002 · 添加 Codex 可用的 Skills 入口

## 概述

为 **OpenAI Codex**（CLI / 宿主）补齐本仓库 Skills 包的**可安装、可调用入口**，使消费方能像 Claude Code / GitHub Copilot / Grok Build 一样使用治理主路径（至少 `/govern`，并覆盖 `audit` / `vision` / `vision-audit` 四入口对齐策略）。

本目标属 Root 纲领 **R1**（消费宿主补齐）。**2026-07-31 关门**：install 面 + 脚本 + Codex CLI `0.146.0` 只读 `$govern` dispatch 探针已落盘。

## 成功标准（可验证）

- [x] 已落盘 Codex 宿主如何加载 project skills / 规则的**有据结论**（关闭 I-001，或用户书面 residual）
- [x] 包内存在 Codex 安装面（如 `skills/install/codex/` 或文档化等价路径），覆盖四入口策略（可分阶段，但范围写清）
- [x] `install.ps1` / `install.sh`（或文档主路径）可一键/可复制安装到 Codex 约定位置
- [x] 至少一次在 Codex 宿主上对主入口（优先 `/govern` 或等价）做 **runtime 探针或可核对手工验证**，证据落入本目标 `attachments/` 或发布证据链

## 派生进度展示

`progress: 100%` = 上方 4 个检查点完成 4 / 4。仅展示；**不**单独推导 `done`（`done` 见关门审计 A-001）。

## 阶段计划（目标内 · 非树节点）

| 阶段 | 内容 | 状态 |
|------|------|------|
| A | 信息澄清：Codex skills / AGENTS / 项目规则加载路径 | **完成** |
| B | 方案：目录布局、与 claude/grok 差异、install 开关、契约/矩阵是否声明 | **完成**（D-002） |
| C | 实现：install 适配 + 脚本/文档 | **完成** |
| D | 验证 + 关门审计 | **完成**（探针 + A-001） |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | Codex 如何发现 skills | 方案冻结 B | B 前 | 官方文档 | **verified** | 官方路径变更时复核 | [attachments/i-001-i-002-…](attachments/i-001-i-002-codex-skills-loading-2026-07-31.md) |
| I-002 | required | 四入口最小形态 | 方案冻结 B | B 前 | 对照 + 能力 | **verified** | — | 同上；四独立 skill |
| I-003 | non-blocking | 是否写入 consumer 兼容矩阵为 committed 宿主 | 发版宣称 | 验收/发版前 | 发布纪律 | **open** | 可 residual；不阻塞本目标关门 | 探针仅 dispatch-readonly，未升格矩阵 |
| I-004 | non-blocking | Windows / 非 Windows 安装路径差异 | 实施完整度 | C | 双平台脚本 | **verified** | — | install.ps1 + install.sh |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)

## 备注

- 关门不把 I-003 写成 verified；不把本仓 Web 或矩阵三宿主历史证据扩到 Codex。
- dogfood：仓库根 `.agents/skills/` 由 install 产生，对标 `.claude/skills` / `.grok/skills`。
