---
title: 提示词 · 记录决策
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.1
role: primitive
---

# 02 · 记录决策（原语 / primitive）

## 说明

**角色**：文档原语，供 [00-govern-orchestrator.md](00-govern-orchestrator.md) 调用；也可高级直调。默认用户路径请用编排器。

解决「做了取舍却没写清楚、或写了一堆空话」的问题。  
引导 AI 在目标的 `01-decision.md` 中追加结构化决策条目：决定了什么、为什么、未选方案是什么。

---

## 提示词正文

```markdown
你是本项目的目标治理协作者。遵守项目 AI 规则（根 `AGENTS.md` 和/或 `.github/copilot-instructions.md`）。P-001 以 AGENTS 为准；architecture 文档可选。

## 任务
为指定目标追加一条（或若干条）**决策记录**，写入该目标的 `01-decision.md`。只记录真实取舍，不编造。

## 用户输入
如果某项信息缺失或不确定，请先向我确认，不要猜测后继续。
- 目标 ID / 路径：【如 GOAL-003-skills-practice 或 docs/goals/GOAL-003-skills-practice/】
- 决策标题：【一句话】
- 决定了什么：【明确结论】
- 为什么（背景、约束、收益）：【填写】
- 考虑过但未选的方案（可选）：【列出 + 简短否决理由】
- 影响范围（可选）：【会影响哪些目标 / 文档 / 代码】
- 后续动作（可选）：【因此要做什么】
- 今日日期：【YYYY-MM-DD】

## 强制步骤
1. 读取目标的 `00-meta.md` 与现有 `01-decision.md`，保持风格与编号连续。
2. 决策条目建议格式：

   ### D-NNN · <决策标题>
   - **日期**：YYYY-MM-DD
   - **状态**：accepted / proposed / superseded
   - **决定**：……
   - **理由**：……
   - **未选方案**：……
   - **影响**：……
   - **后续**：……

3. 编号：在该文件已有 D-00x 基础上 +1；若无历史编号，从 D-001 起。
4. 更新 `01-decision.md` 的 frontmatter `updated` 为今日日期；必要时微调 `version`（小改可保持）。
5. 若该决策改变了目标范围、成功标准或路线图：
   - 同步修改 `00-meta.md` 中对应段落
   - 在 `02-execution.md` 时间线追加一句「记录决策 D-NNN：……」（事实，非空话）
6. 若决策导致目标 status/progress 变化，**必须**同步 `docs/goals/goal-tree.md`。
7. 语言简洁：每条决策以「可执行结论」为主，避免口号式表述。

## 写作约束
- 必须写清「决定了什么」和「为什么」。
- 重要取舍尽量注明未选方案。
- 不确定的前提标「待确认」，不要假装已验证。
- 不要把执行流水账写进 decision；过程细节放 execution。

## 禁止
- 禁止虚构未发生的共识
- 禁止用决策文件代替执行时间线
- 禁止改 parent/编号后不更新 goal-tree.md

## 交付检查清单
- [ ] 决策条目结构完整
- [ ] 编号不冲突
- [ ] updated 已刷新
- [ ] 范围/成功标准若变则 meta 已对齐
- [ ] 需要时已更新 execution 与 goal-tree
```

---

## 使用注意事项

- 一条提示词可记多条决策，但请在输入区逐条列清，避免 AI 合并成含糊一段。
- 若决策已过时，用新条目 `superseded` 旧决策，并在旧条目状态改为 `superseded`，不要静默删除历史。
