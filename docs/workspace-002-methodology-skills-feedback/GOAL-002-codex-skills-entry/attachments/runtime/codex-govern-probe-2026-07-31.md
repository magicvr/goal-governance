---
title: Codex CLI · $govern runtime 探针（GOAL-002 阶段 D）
status: active
created: 2026-07-31
updated: 2026-07-31
parent: GOAL-002-codex-skills-entry
version: 0.1.0
---

# Codex CLI · `$govern` runtime 探针

> 范围：只读 **dispatch** 验证（skill 可发现、包装可加载、`prompts/00` 可读）。  
> **不是**：完整 `/govern` 写盘 e2e；**不是** consumer 矩阵 `committed` / 全入口 runtime 升格。

## 环境

| 项 | 值 |
|----|-----|
| 日期 | 2026-07-31 |
| 主机 | Windows |
| Codex CLI | `codex-cli 0.146.0`（`npm` 全局 `codex.ps1`） |
| 工作目录 | `C:\Users\magicvr\Documents\Code\goal-governance` |
| 安装 | `.\skills\install.ps1 -Codex -SkillsDir .\skills -Force -NonInteractive` |
| 落点 | `.agents/skills/{govern,audit,vision,vision-audit}/SKILL.md` |
| 模型（本次会话） | `gpt-5.6-terra`（provider: custom） |
| sandbox | `read-only` |
| approval | `never`（`-c approval_policy="never"`） |
| 其它 | `--ephemeral`（不持久会话） |

## 命令（可重放）

```powershell
# 1) 安装面（仓库根）
.\skills\install.ps1 -Codex -SkillsDir .\skills -Force -NonInteractive

# 2) 只读探针
$out = 'docs\workspace-002-methodology-skills-feedback\GOAL-002-codex-skills-entry\attachments\runtime\codex-govern-last-message-2026-07-31.txt'
$prompt = @'
RUNTIME PROBE ONLY — do not modify any files, do not create goals, do not change status.
1. Explicitly use the project skill named govern ($govern). Read .agents/skills/govern/SKILL.md if needed.
2. Confirm you can locate SKILLS_PKG (directory containing prompts/00-govern-orchestrator.md).
3. Reply with EXACTLY these lines (plus optional short notes after):
CODEX-GOVERN-PROBE host=codex-cli skill=govern path=.agents/skills/govern/SKILL.md status=loaded
SKILLS_PKG=<absolute-or-repo-relative path>
ORCHESTRATOR_EXISTS=<yes|no>
WORKSPACE_FOCUS=workspace-002 GOAL-002-codex-skills-entry
OUTCOME=dispatch-readonly
'@
codex exec -C (Get-Location).Path -s read-only --ephemeral --color never `
  -c 'approval_policy="never"' -o $out $prompt
```

## 结果

| 检查 | 结果 |
|------|------|
| 进程 exit | **0** |
| 技能入口文件 | 已读 `.agents/skills/govern/SKILL.md` |
| SKILLS_PKG | `C:\Users\magicvr\Documents\Code\goal-governance\skills` |
| 编排器存在 | **yes**（`skills/prompts/00-govern-orchestrator.md`） |
| 写盘 | 探针过程 **未**修改目标五件套 / goal-tree（read-only sandbox） |

### 最后一条消息（原样）

见 [codex-govern-last-message-2026-07-31.txt](codex-govern-last-message-2026-07-31.txt)：

```text
CODEX-GOVERN-PROBE host=codex-cli skill=govern path=.agents/skills/govern/SKILL.md status=loaded
SKILLS_PKG=C:\Users\magicvr\Documents\Code\goal-governance\skills
ORCHESTRATOR_EXISTS=yes
WORKSPACE_FOCUS=workspace-002 GOAL-002-codex-skills-entry
OUTCOME=dispatch-readonly
```

### 原始日志

[codex-govern-exec-2026-07-31.log](codex-govern-exec-2026-07-31.log)（含 tool 调用与模型输出；Windows 控制台可能乱码中文正文，**判定以 marker 行与 exit 0 为准**）。

## 判定

| 主张 | 状态 |
|------|------|
| install 面在 Codex CLI 上可被 `$govern` / skill `govern` 路径消费 | **verified（dispatch-readonly）** |
| 关闭 GOAL-002 成功标准 #4 | **是** |
| 矩阵 `committed` / 三入口全覆盖 runtime | **否**（I-003 仍 non-blocking；本探针仅主入口） |

## 副作用记录

- 安装脚本默认会装 core → `./docs/` 并可能覆写 monorepo `AGENTS.md` / `docs/README.md` 等。本轮探针后已 **`git checkout` 恢复** monorepo 侧 `AGENTS.md`、`docs/README.md`、`docs/vision/README.md`。  
- dogfood 安装产物 **`.agents/skills/*`** 保留（对标已跟踪的 `.claude/skills`、`.grok/skills`）。
