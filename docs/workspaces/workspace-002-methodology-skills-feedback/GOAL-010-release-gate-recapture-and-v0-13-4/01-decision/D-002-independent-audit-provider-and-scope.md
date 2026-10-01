---
id: D-002
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: decision
title: independent 审计 provider 与 scope
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# D-002 · independent 审计 provider 与 scope

**状态**：accepted（2026-10-01）

## 触发

本目标 scope 是**正式发布 + 消费兼容矩阵变更**，按 P-004.1 属
`release` / `compatibility` 高影响门禁，最低要求为**至少一个会话指定 provider 的
independent**。AGENTS §6b 规定：仅当 independent/cross 已确定但会话无 provider 时才询问。

## 决定

| 项 | 值 |
|----|-----|
| 模式 | `independent` |
| provider | **本地 grok build CLI**，模型 `grok-4.6`（2026-10-01 用户书面改派，见下「provider 变更」） |
| scope | **发布候选完整审计**：12 格证据是否真实、新鲜且被矩阵引用；版本清单（CHANGELOG / 矩阵 `candidateRevision` / 三处安装 pin）是否一致；回归与发布门禁是否真的转绿 |
| 落盘 | `03-audit/A-002-independent-release-candidate.md`，`source: independent` |

用户于 2026-10-01 书面指定，最初为本地 codex CLI（模型 `gpt-6.1-sol`，思考强度 `high`），
沿用 GOAL-009（A-009 用同一 provider）的已验证可用配置。

### provider 变更（2026-10-01，用户书面裁决）

实测本地 codex CLI 在**本机沙箱下无法初始化**：

```text
Error: failed to initialize in-process app-server client: 拒绝访问。 (os error 5)
```

`--sandbox read-only`、`--skip-git-repo-check`、把 `CODEX_HOME` 重定位到工作区内均不能绕过；
该 CLI 需要命名管道与工作区外临时目录写入，二者在本机受限模式下都不可用。

按本决定 §约束 1 与 P-004.1，provider 失败**不静默降级**、也不由编排器冒充 `independent`。
已就此向用户提问，用户于 2026-10-01 书面**同意改用本地 grok build CLI（模型 `grok-4.6`）**。
变更后的 provider 已在同一台机器上跑通纯文本输出（本轮 4 格 Grok 宿主探针与本次审计均使用它）。

A-002 的 provider 因此记为 `grok-4.6`；本节的变更留痕即为该改派的书面依据。

## 约束

1. **provider 失败不降级。** CLI 不能给出可核对意见（超时、不可用、无可核对输出）时，
   该门禁回到未满足，不得静默降级，也不得由编排器冒充 `independent`。
2. **独立审计只出意见。** 默认不改 `status` / `progress` / 方案正文；响应与状态变更
   归编排器，并走用户确认。
3. **开放 required 未合法闭合前不放行。** finding 只能按 `fixed` /
   `accepted-residual` / `user-overruled` 三路径闭合，口头不算。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 坚持本地 codex CLI，在沙箱外由用户手工跑 | 用户选择改派到 grok，避免让发布等待外部手工步骤 |
| 本地 Claude Code CLI | 当前代理配置需 `--settings` 修正 base URL 才可用，审计链路风险更高；且它同时是本轮被审宿主之一 |
| 不做 independent、只自审 | 违反高影响门禁最低要求 |
| 编排器自行充当 `independent` | P-003 / D-002 §约束 1 明文禁止 |

## 仍待后续

- A-002 的 finding 响应与闭合记录落在 `03-audit/A-003-response-a002.md`。
