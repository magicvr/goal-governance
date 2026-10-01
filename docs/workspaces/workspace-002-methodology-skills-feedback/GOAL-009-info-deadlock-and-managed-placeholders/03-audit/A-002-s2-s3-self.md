---
id: A-002
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: audit-entry
record_id: A-002
source: self
provider: 编排器
scope: S2 规则区分与 S3 安装升级执行事实
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# A-002 · S2/S3 执行事实自审（2026-09-30）

- **source**：self
- **auditor**：编排器
- **类型** / **scope**：execution-facts；S2 与 S3。不是关门审计。
- **verdict**：conditional

## 范围与区间

对照 D-003、D-004、E-003、E-004，以及 `skills/render_managed.py`、`skills/install.sh`、`skills/install.ps1`、`skills/update.py`、`skills/agents_merge.py`。HEAD 为 `693a4e6`。本条不改 status、progress。

## 成果（有证据）

- 原则第 5 条与规则回归测试锁住两边句子。见 `docs/architecture/principles.md` 与 `skills/tests/test_skills_orchestrator.py` 的 `test_research_result_is_not_a_gate_into_its_own_work`。
- 安装后再升级测试调用仓库里的 `install.ps1` / `install.sh`，断言原则文件字节等于 `render_managed_bytes`，dry-run 冲突列表为空，手改后抛出 `managed files have local changes`。本轮回归 25 项通过。
- 双基线已写在 D-004。它保留升级原先就接受的包内原文，并加上这次渲染结果。这不是未落盘的第二次用户选择。

## 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 研究结论不是进入该项工作的门禁，先于执行的事实仍可设门禁 | 达成 | D-003 与规则测试 |
| 指定两个目录后，替换本身不让升级失败，手改仍失败 | 主路径达成 | E-004 与两条安装后再升级测试 |
| 只渲染消费方受管目的地，不改技能包源码，标记外字节不改 | 未完全达成 | F-001、F-002 |
| 开放 required 已闭合后才关门 | 未达成 | 本条与 A-001 的 required 仍 open |

## Findings

### F-001 · 整树渲染会改到消费方自有文件和嵌套的技能包

- 严重度：high
- 建议：required
- 状态：open
- 描述：`_render_tree` 递归处理方法论目录和宿主技能树里所有非隐藏文件，没有受管文件清单，也不排除落在方法论目录里面的 skills 目录。临时目录复现：`methodology/notes/mine.md` 与 `methodology/my-skills/core/docs/architecture/principles.md` 里的 `{governance_root}` 都被换成 `methodology`。
- 证据：`skills/render_managed.py` 的 `_render_tree`；`install.sh` 的 `render_installed_placeholders`；`install.ps1` 的 `Update-RenderedManagedCopies`

### F-002 · 受管块更新时，AGENTS 标记外的 CRLF 会被改成 LF

- 严重度：med
- 建议：required
- 状态：open
- 描述：`merge_agents_text` 先对整份目标做换行归一，文件层在内容有变化时再用 LF 写回。渲染会改变受管块，因此重装或升级合并时，标记外的 CRLF 前缀不再保持原字节。临时目录复现：前缀 `consumer\r\n` 合并后变成 `consumer\n`。
- 证据：`skills/agents_merge.py` 的 `_norm_newlines` 与 `merge_agents_file`；D-004 写明标记外字节不改

### F-003 · 台账里有两处过时措辞

- 严重度：low
- 建议：recommended
- 状态：open
- 描述：`00-meta.md` 的 I-001 证据仍写「原则正文尚未改」。E-003 写「已发布文本」，同条又写没有发布。
- 证据：GOAL-009 `00-meta.md` 信息表 I-001；`02-execution/E-003-rule-distinction.md`

## 必改项汇总

F-001、F-002。与 A-001 的必改项相同。F-003 不阻断。

## 与 A-001 的异同

两边都把 F-001、F-002 标为 open required，都不把双基线当成需要另一次确认的静默决策。verdict 不同：A-001 为 fail，本条为 conditional。差别在于主路径的安装与 dry-run 升级已经按测试成立，所以本条不把整个 S2/S3 判成名不副实。这个标签差异不改变必改项，也不放行关门。

## 结论 + 建议下一步

建议用户对 F-001、F-002 都选 fixed。在书面选择之前不改安装器，不把 GOAL-009 标为 done。
