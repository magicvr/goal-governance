---
id: GOAL-021-skills-release-chain-hardening
title: 加固 Skills「规则→分发→证据→发布」执行链
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.3.0
progress: 100%
---

# GOAL-021 · 加固 Skills「规则→分发→证据→发布」执行链

## 有界关门（2026-07-30）

本目标 `done / 100%` 关闭的是 **执行链 P1/P2 机制修复与负例覆盖**（A-001 findings F-001～F-005 fixed；A-003 self close-out `pass`；用户确认 D-003）。

**不**构成：新 Skills annotated tag / GitHub Release、12 宿主 runtime 全量重采、Root 终态、阶段 7。

### Residual / follow-up（非阻断）

| ID | 级别 | 说明 | 状态 |
|----|------|------|------|
| **R-021-RUNTIME-RECAPTURE** | non-blocking | 若以 **新断言策略** 作为正式发版证明，须按 GOAL-008 惯例全量重采 runtime 后再 tag | open · Root 路径 D / 发版候选时 |
| **R-021-SYMLINK-CI** | non-blocking | Windows 本机无 symlink 特权时动态负例 skip；逻辑已落地，Linux CI 可执行 | open · 发布机 Ubuntu 已覆盖风险面 |

## 概述

闭合一条独立对抗审对 **Skills 执行链** 的发现：核心原则本身总体自洽，但「规则 → 分发 → 证据 → 发布」曾存在 **4 项 P1** 与 **1 项 P2** 风险。本目标完成机制修复与回归。

## 成功标准

- [x] 对抗审正式意见已落本目标 `03-audit.md`（`A-00N` + `source`）
- [x] **F-001～F-004**（required）均已 `fixed` 并留痕
- [x] **F-005** 已 `fixed`
- [x] 负例测试覆盖（含 marker-only；symlink 在有权限环境）
- [x] docs / skills / scripts 回归通过
- [x] 自审 A-003 `pass` + 用户确认关门（D-003）

## 纲领路线图（P-001）

| 阶段 | 内容 | 完成标记 |
|------|------|----------|
| **A · 审计落盘** | A-001 independent | [x] |
| **B · core mirror** | F-001 | [x] |
| **C · 运行证据** | F-002 | [x] |
| **D · 打包围堵** | F-003 | [x] |
| **E · P-006 验证** | F-004 | [x] |
| **F · 安装/工作区** | F-005 | [x] |
| **G · 回归与关门** | A-003 + D-003 | [x] |

**派生 progress**：7/7 = **100%**。progress 仅为展示，不构成放行或发版证明。

## 信息就绪与未知项（P-005）

| ID | 级别 | 状态 | 证据 / 结论 |
|----|------|------|-------------|
| I-001 | non-blocking | closed | D-002 断言策略 |
| I-002 | non-blocking | closed | F-005 in-scope fixed |
| I-003 | non-blocking | closed (out of scope) | 本目标不授权 tag/Release；见 R-021-RUNTIME-RECAPTURE |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
