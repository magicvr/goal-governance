---
id: D-003
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: decision
title: 结果尚不存在时不是进入该项工作的门禁
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# D-003 · 结果尚不存在时不是进入该项工作的门禁（2026-09-30）

**状态**：accepted

**触发**：S1 已核对死锁条文。本目标成功标准要求调查可以作为工作本身推进，同时保留真正先于执行的事实仍可设门禁。I-004 已指定 provider。占位符策略不在本条范围内。

## 决定

1. 在 `docs/architecture/principles.md` P-005「设立与阶段门禁」增加第 5 条：某个 required 信息项只有做完它要挡住的那项工作才有答案，则它不是进入该项工作的门禁。调查、研究或澄清本身就是这项工作时，做这项工作就是在收集该信息。工作开始前已经可以独立查询或核对的事实，仍然可以是进入执行、发布或验收的 required 门禁。
2. 同一对句子写入根 `AGENTS.md`、`skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md`、`.github/copilot-instructions.md` 的 P-005 摘要，以及 `skills/prompts/00-govern-orchestrator.md` 的 P-005 节和 §3.5。
3. 完成清单里「本次要推进的阶段没有开放 required 信息门禁」和编排器「未跨越到期 required 信息门禁」都加上同一例外：该项答案只有做完本阶段工作才存在。否则清单会把死锁重新写回来。
4. 原有阶段门禁、有界实验、残余风险和「不得以后再说」保持不变。先于执行已经可以核对的事实仍然挡住进入执行。
5. 镜像只通过 `scripts/stage_skills_mirrors.py` 从 canonical 生成。不手改 `skills/core/docs/architecture/principles.md`。

## 为什么

- S1 附件写明：现行实施门禁和阶段门禁不区分「做完才有的结论」和「开始前已经可以核对的事实」。编排器虽然允许把收集当作下一步，但 §3.5 仍要求实施前先有证据。
- 成功标准已经要求这两边同时成立。本条只选定落在哪些句子上，不另开产品分叉。
- provider 在 D-002 已书面指定。审计意见留到实施可核对之后，不在本条冒充 independent。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 删掉阶段门禁，只保留「可以带未知立项」 | 先于执行的事实就不再能挡住发布或实施 |
| 只改编排提示，不改原则 | 原则是权威全文；摘要和提示会在下次安装时把旧门禁带回去 |
| 用一条「禁止」子弹写进编排器 | 该文件以「- 禁止」开头的条目已有上限，增补用肯定句 |
| 本条一起改安装器 | 占位符策略仍待用户选定 |
