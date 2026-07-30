---
id: GOAL-002-codex-skills-entry
title: 添加 Codex 可用的 Skills 入口
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-07-31
updated: 2026-07-31
version: 0.1.0
progress: 0%
---

# GOAL-002 · 添加 Codex 可用的 Skills 入口

## 概述

为 **OpenAI Codex**（CLI / 宿主）补齐本仓库 Skills 包的**可安装、可调用入口**，使消费方能像 Claude Code / GitHub Copilot / Grok Build 一样使用治理主路径（至少 `/govern`，并覆盖 `audit` / `vision` / `vision-audit` 四入口对齐策略）。

**现状观察（开题时）**：

- 已有：`skills/install/claude/`、`skills/install/copilot/`、`skills/install/grok/`
- `install.ps1` / `install.sh` 支持 `--claude` / `--copilot` / `--grok`
- **尚无** `install/codex/` 或等价宿主适配与安装开关

本目标属 Root 纲领 **R1**（消费宿主补齐）。

## 成功标准（可验证 · 暂定）

- [ ] 已落盘 Codex 宿主如何加载 project skills / 规则的**有据结论**（关闭 I-001，或用户书面 residual）
- [ ] 包内存在 Codex 安装面（如 `skills/install/codex/` 或文档化等价路径），覆盖四入口策略（可分阶段，但范围写清）
- [ ] `install.ps1` / `install.sh`（或文档主路径）可一键/可复制安装到 Codex 约定位置
- [ ] 至少一次在 Codex 宿主上对主入口（优先 `/govern` 或等价）做 **runtime 探针或可核对手工验证**，证据落入本目标 `attachments/` 或发布证据链

## 派生进度展示

`progress: 0%` = 上方 4 个检查点完成 0 / 4。仅展示。

## 阶段计划（目标内 · 非树节点）

| 阶段 | 内容 | 状态 |
|------|------|------|
| A | 信息澄清：Codex skills / AGENTS / 项目规则加载路径 | 未开始 |
| B | 方案：目录布局、与 claude/grok 差异、install 开关、契约/矩阵是否声明 | 未开始 |
| C | 实现：install 适配 + 脚本/文档 | 未开始 |
| D | 验证 + 关门审计 | 未开始 |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | Codex 如何发现 skills（目录名、SKILL.md 约定、与 AGENTS.md / 项目指令关系） | 方案冻结 B | B 前 | 官方文档 + 本地宿主探测 | open | — | 待收集 |
| I-002 | required | 四入口在 Codex 上的最小可行形态（独立 skill vs 单入口 dispatch） | 方案冻结 B | B 前 | 对照 claude/grok 包装 + Codex 能力 | open | — | 待收集 |
| I-003 | non-blocking | 是否写入 consumer 兼容矩阵为 committed 宿主 | 发版宣称 | 验收/发版前 | 与 GOAL 发布纪律对齐 | open | 可 residual | 未决 |
| I-004 | non-blocking | Windows / 非 Windows 安装路径差异 | 实施完整度 | C | 文档与脚本双平台 | open | — | 可分阶段 |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)

## 备注

- 不在本目标内改 Charter；不把矩阵升格为「已 verified」除非有 runtime 证据。
- 实现时优先复用 `skills/prompts/` 真相，宿主层只做薄包装（与现有三宿主一致）。
