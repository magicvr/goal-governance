---
id: D-005
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: decision
title: F-001 按受管映射闭合；F-002 评估不构成闭合
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# D-005 · F-001 按受管映射闭合；F-002 评估不构成闭合（2026-09-30）

**状态**：accepted（只接受下面第 1 点。第 2 点没有闭合 F-002）

**触发**：用户于 2026-09-30 对 A-001 / A-002 的 F-001 书面选择「修正」。同一轮对 F-002 的书面原话是：「我们是否应该把所有的 crlf 归一化为 lf?（并用git仓库管理规则做强制验证，并且在commit技能里面明确要在提交时候执行归一化操作)——评估一下这个合理性和可行性。」

## 决定

1. **F-001 按 fixed 闭合。** 安装与升级只渲染受管文件映射里的消费方目的地。映射与 `update.py` 的比较清单是同一份：核心方法论的 README、architecture、templates、vision，以及 `.claude/skills`、`.grok/skills`、`.agents/skills`、`.github/prompts`、`.github/copilot-instructions.md`。根 `AGENTS.md` 仍用临时渲染副本合并，不整文件渲染。消费方放在这些目录里、但不在映射上的笔记和自定义 skill 保持原字节。
2. **方法论目录与 skills 目录互相包含，或两条路径相同，在任何复制和渲染之前停止。** 停止语是 `skills directory must stay outside the methodology directory`。相反方向一并停止：方法论目录落在技能包里面时，受管目的地 `{methodology}/architecture/principles.md` 会盖住包内 `core/docs/architecture/principles.md`。这是 A-001 建议修正里的「无法保证隔离则写入前 fail closed」，用来守住 D-004「不改技能包源码」。
3. **F-002 仍开放。** 用户要求的是评估，没有选择 fixed、accepted-residual 或 user-overruled。本条不改 `skills/agents_merge.py`、`.gitattributes` 或 `/commit` 技能。
4. **不另开子目标。** F-001 的写集仍在本目标 S3 的安装与升级路径内。

## 为什么

- 用户对 F-001 的书面选择与 A-001、A-002 的建议一致：限定渲染写集，并在路径无法隔离时于写入前停止。
- 整树替换会改写方法论目录里的自有笔记，以及嵌套在该目录下的技能包文件。只渲染映射内的目的地后，这些文件不再进入写集。
- 只挡住「skills 位于方法论目录之内」仍会留下包源码被受管目的地盖住的路径。两条路径的包含关系用同一谓词判断。

## F-002 评估（待用户选择闭合路径）

本段是评估，不是闭合。

- 本仓库 `.gitattributes` 已经把 `*.md`、`*.json`、`*.txt`、`*.ps1`、`*.py`、`*.sh`、`*.yml`、`*.yaml` 和 `AGENTS.md` 标为 `text eol=lf`。这些类型在本仓库提交时已经归一为 LF。再写一条同样的仓库规则，不改变消费方安装时的合并行为。
- F-002 的改写发生在消费方安装或升级合并根 `AGENTS.md` 时。`skills/agents_merge.py` 的 `_norm_newlines` 对整份目标文本做 CRLF/CR→LF，`merge_agents_file` 在内容有变化时以 `newline="\n"` 写回。标记外的消费方段落会一起变成 LF。D-004 写明标记外字节不改。
- 四个宿主的 `/commit` 技能只提交调用方点名的路径，并禁止 `git add -A` 与 `git add .`。技能正文没有换行步骤。提交时扫描整棵树做归一化，会改写未被点名的文件，也会把本仓库的换行政策套到需要 CRLF 的消费仓库上。
- Git 的 `eol=lf` 在匹配该属性的仓库里于纳入索引时转换。它不取消安装器已经写进工作区 `AGENTS.md` 的替换。没有这些属性的消费仓库，提交也不会保住标记外的 CRLF。

因此：全库 CRLF→LF 作为本仓库已有的文本卫生是成立的，可行性也已经由 `.gitattributes` 覆盖。把它再加进 `/commit`，不可行于该技能自己的路径边界。这条路线不闭合 F-002。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 继续整树渲染，只维护一份排除名单 | 消费方以后新增的笔记和自定义 skill 仍会漏进写集 |
| 只拒绝 skills 位于方法论目录之内 | 方法论目录位于技能包之内时，受管目的地会改写包源码 |
| 把全库 CRLF→LF 或 `/commit` 归一化当成 F-002 的闭合 | 用户要求先评估。评估结论是它不闭合标记外字节被安装器改写的问题。闭合路径仍待书面选择 |

## 仍待后续

- F-002 由用户书面选择 fixed（保留标记外原始字节）、accepted-residual（接受安装时整份换行被改写，并写明范围与复审触发）或 user-overruled。
- F-003 仍是 recommended，本条不处理。
- 开放 required 全部合法闭合后，再用本地 codex CLI（`gpt-6.1-sol`，思考强度 high）复审。本条不是独立审计。
- 发布范围与 GOAL-009 关门仍待用户书面决定。本条不把目标标为 `done`。
