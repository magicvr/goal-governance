---
name: commit
description: 根据已暂存变动或用户明确给出的 owned paths 生成中文提交描述并安全提交（便利入口，非治理必达）
user-invocable: true
argument-hint: "[owned paths…]"
---

# /commit · 安全提交便利入口

> **定位（GOAL-008 D-002 §4 / VP-004 入口面）**：这是**便利可选**入口——在支持的宿主上默认安装、可直接调用，
> 但它**不是**完整治理安装的 MUST，**不在**四治理入口（`vision` / `vision-audit` / `govern` / `audit`）必达集内，
> 也**不替代** `/govern` 的长流程 Git checkpoint。缺少本入口不会让安装变为「不完整安装」，也不会阻断 `/govern`。

按以下步骤操作；**任一步失败即 fail closed**（停止、说明原因、不执行 `git commit`）。

## 1. 检查暂存区

1. 运行 `git diff --cached --name-status`。
2. 非空（已有暂存改动）：确认暂存路径均属于当前动作；发现**无关路径或归属不明**时停止并报告，**不替用户撤销或覆盖**。
3. 为空：**仅当**用户或当前治理流程已经明确给出 owned paths 时，运行 `git add -- <owned paths>`；**不得**扩大到其他路径。
4. 既无暂存改动也无明确 owned paths：说明「没有可安全提交的已暂存改动；请指定 owned paths」并终止。
5. 暂存后再次运行 `git diff --cached --name-status` 与 `git diff --cached --check`；**无改动、校验失败或路径越界时不得提交**。

## 2. 生成描述

- 依据 `git diff --cached` 生成中文 Conventional Commits 描述；格式 `类型(范围): 简短描述`，范围可选。
- 类型必须取自：`feat, fix, docs, style, refactor, test, chore`；描述具体、精炼，中文，不超过 50 字。

## 3. 提交

- 运行 `git commit -m "<描述>"`。
- 提交成功后回显：提交 ID、已暂存的路径范围。

## 负例与 fail closed（必须遵守）

| 情形 | 期望行为 |
|------|----------|
| 路径含任务开始前的用户改动，或与无关改动不可分离 | 停止并报告；**不**覆盖、**不**回退、**不**夹带 |
| owned path 越界（不在用户/流程声明范围内） | 不暂存、不提交 |
| `git diff --cached --check` 失败（空白错误等） | 不提交 |
| 无改动可提交 | 不执行 `git commit`，简短提示 |
| 非 Git 仓库 | 报告并非零终止，不宣称成功 |
| 提交失败（hook 拒绝、锁、签名失败） | 报告原始错误，不重试绕过；**禁止** `--no-verify` 除非用户明确要求 |
| detached HEAD / rebase 中 / 合并冲突未解 | 停止并报告，不自动修复 |
| 用户已禁用该入口 | 不提交，直接说明 |

## 硬约束

- **禁止** `git add -A`、`git add .` 或任何会吞入未声明路径的命令。
- **不得** `git push` 或产生远端副作用（除非用户在同一轮明确要求）。
- **不得**把本入口当作治理放行依据：commit 是恢复点，不是审计、实现或发布通过证据。
- 只输出必要的执行结果与关键信息。

## 输出示例

- `已检测到暂存改动，生成提交信息：feat(auth): 新增令牌校验` / `执行 git commit 成功：提交 ID abcdef1`
- `未检测到暂存改动，已按 owned paths 暂存：src/auth、tests/auth；生成提交信息：fix(auth): 修复令牌校验`
- `没有可安全提交的已暂存改动；请指定 owned paths`
- `无改动可提交`