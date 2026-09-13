---
id: GOAL-008-consumer-layer-split-and-hosting
doc: attachment
title: /commit 便利入口宿主实测 + legacy 兼容核对（S6）
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# 附件 · `/commit` 宿主实测与 legacy 兼容核对（2026-09-13）

> 目的：闭合 [A-009](../03-audit/A-009-s5-stage-self.md) **F-001**（`/commit` 单列宿主调用 + fail-closed 负例）与 [A-006](../03-audit/A-006-s3-stage-self.md)/[A-008](../03-audit/A-008-s4-stage-self.md) **F-001** 的剩余子项（隔离仓「缺列/legacy 不判不完整安装」）。
> 环境：Windows + Windows PowerShell 5.1；隔离消费仓 `%TEMP%\s6-commit-68aba7`（`git init`，非本仓）；安装包 = 本工作树 `skills/`。

## 1. `/commit` 真实宿主调用（Claude Code `2.1.270`）

被测对象 = 安装到消费仓的 `.claude/skills/commit/SKILL.md`（安装器默认产出）。
命令形态：`claude -p --no-session-persistence --allowedTools Bash --permission-mode acceptEdits --output-format text --effort low --max-turns 12~14`（prompt 走 stdin，指向 `SKILL.md` 并给出 owned path）。

### 1.1 正例（给出 owned path = `a.txt`）

| 项 | 观察 |
|----|------|
| 输出 | `COMMIT_ID: 6d357ac` / `STAGED: a.txt` / `TOUCHED_B: no` |
| 提交内容 | `git show --stat` = **仅 `a.txt`**（1 file changed）；提交信息为中文 Conventional Commit（`chore: 更新 a.txt 内容`） |
| 未声明路径 | `b.txt` 保持 ` M`（工作区已改、**未**被暂存或提交） |
| 结论 | **通过**：只暂存显式 owned path，未吞入未声明路径，未使用 `git add -A` |

原始输出：`attachments/probes/commit-positive-claude.txt`。

### 1.2 负例（无 owned path、暂存区为空）

| 项 | 观察 |
|----|------|
| 输出 | `COMMIT_ID: none` / `STAGED: none` / `REFUSED_REASON: 没有可安全提交的已暂存改动，且本轮未指定 owned paths。` |
| 仓库状态 | HEAD 未变化（`6d357ac` 前后一致）；`git diff --cached --name-only` 为空；`b.txt` 仍为 ` M` |
| 结论 | **通过（fail closed）**：未提交、未擅自选择路径、未改动仓库状态；拒绝理由与 SKILL.md 文本一致 |

原始输出：`attachments/probes/commit-failclosed-claude.txt`。

### 1.3 附带观察（权限层 fail closed）

首次尝试在**未授予 Bash 权限**的会话中运行：skill **拒绝执行**并报告「`git add -- a.txt` 需要运行权限批准，当前未获批准，因此按 SKILL.md fail closed，未执行提交」，随后经核对确认**未纳入 `b.txt` 之外的任何路径、未提交**（当时仓库仍无 commit）。
→ 该行为与 SKILL.md 的失败路径要求一致，作为**额外负例**记录（权限不足时不静默绕过）。

### 1.4 必达/便利边界（本轮同时核对）

`/commit` **不在** 12 格 runtime 矩阵中；其证据单列于本附件与 `layer-semantics-host-probe.md`，不进入必达集合；契约 `hostEntrypoints` / `files.entrypoints` / `mcp.entrypoints` 均无 `commit`（守卫见 `docs/tests/test_file_l1.py`）。

## 2. legacy 组合编排兼容核对（隔离仓）

在已安装的隔离仓中把 `docs/vision/roadmap.md` 替换为**legacy 形态**：无 `status` 列、无投影标注、含**他仓遗留 VP 行**（`VP-999-foreign-from-other-repo`），然后重跑安装器。

| 检查项 | 结果 |
|--------|------|
| 安装器是否因 legacy 列/遗留行而失败 | **否**：安装继续进行（`Already present` / `Installing core methodology` 正常输出）；它在 `docs/architecture` 处因**非交互模式拒绝覆盖既有目录**而停止，与 roadmap 无关（该停止点已在 `s6-isolated-consumer-evidence.md` §2.1 登记） |
| `docs/vision/roadmap.md` 是否被改写或阻断 | **否**：内容长度差 **0**，他仓遗留行仍在 —— 符合 alignment §0.4「legacy 行/列只作提示，不改写、不阻断」 |
| 「不完整安装」判定是否由 legacy 列驱动 | **否**：该仓的 `docs/vision/charter.md` 与 `revisions.md` 本就不存在（缺 **MUST** 文件），这才是「不完整安装」的依据；legacy 列/行不参与该判定 |
| MUST 表是否要求特定列 | alignment §0.2 已明确「**不要求任何特定列**」，与实测一致 |

**结论**：S3 的兼容条款在真实隔离仓成立——**缺列/残留他仓行既不改写文件、也不阻断安装，更不构成「不完整安装」**；不完整安装信号只由缺失 MUST 文件驱动。

## 3. 尚未覆盖（诚实登记）

- `/commit` 仅在 **Claude Code** 一个宿主实测；Grok / Codex / Copilot 的 `/commit` 仅落盘层面验证（安装器产出）。
- 负例覆盖「无 owned path / 无改动」「权限不足」两类；「路径含任务开始前的用户改动」「非 Git 仓库」「hook 拒绝」「detached HEAD」仍为契约文本层要求，未逐项实测。
- legacy 核对在**单个**隔离仓形态上进行，未覆盖「治理根改为 `governance/`」与「大小写变体 `agents.md`」（后者仍属 [D-009](../01-decision/D-009-s4-agents-coexistence.md) §5 的未实现清单）。

## 4. 复现命令

```powershell
$t = Join-Path $env:TEMP ("s6-commit-" + [guid]::NewGuid().ToString("N").Substring(0,6))
New-Item -ItemType Directory -Path $t | Out-Null
Copy-Item -Recurse '<repo>\skills' (Join-Path $t 'skills')
Push-Location $t; git init -q; git config user.email probe@local; git config user.name Probe
& (Join-Path $t 'skills/install.ps1') -Claude -NonInteractive -SkillsDir (Join-Path $t 'skills')
git add -A; git commit -q -m "chore: baseline"; Set-Content a.txt "owned`n"; Set-Content b.txt "other`n"
# 正例
"按 .claude/skills/commit/SKILL.md 执行 /commit，owned path 只有 a.txt" |
  cmd.exe /d /s /c "claude -p --no-session-persistence --allowedTools Bash --permission-mode acceptEdits --output-format text --effort low --max-turns 14"
git show --stat HEAD      # 期望：仅 a.txt
# 负例
"执行 /commit；没有 owned path，暂存区为空" |
  cmd.exe /d /s /c "claude -p --no-session-persistence --allowedTools Bash --permission-mode acceptEdits --output-format text --effort low --max-turns 12"
git log --oneline -1      # 期望：HEAD 未变化
```
