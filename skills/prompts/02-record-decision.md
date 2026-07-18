---
title: 提示词 · 记录决策
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.2.0
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
# 角色
你是本项目的目标治理协作者。遵守 `AGENTS.md` 和/或 `.github/copilot-instructions.md`。P-001 以 AGENTS 为准。

# 任务
为指定目标在 `01-decision.md` 追加真实决策：写清「决定了什么」与「为什么」。

# 用户输入（缺项先确认）
- 目标 ID / 路径：
- 决策标题：
- 决定了什么：
- 为什么（背景、约束、收益）：
- 未选方案（建议有）：【方案 + 简短理由】
- 影响范围（可选）：
- 后续动作（可选）：
- 今日日期：【YYYY-MM-DD】

# 步骤
1. 读 `00-meta.md` 与现有 `01-decision.md`，延续编号风格。
2. 追加条目（D-001 起递增）：

   ### D-NNN · <决策标题>
   - **日期** / **状态**（accepted | proposed | superseded）
   - **决定** / **理由** / **未选方案** / **影响** / **后续**

3. 刷新 `updated`；小改可保持 version。
4. 若决策改变范围、成功标准或路线图：同步 `00-meta`，并在 `02-execution` 记一句「记录决策 D-NNN：…」。
5. 若 status/progress 变化：同步 `goal-tree.md`。
6. 过程流水账写在 execution；decision 保持可执行结论。

# 完成标准
- [ ] 条目含决定 + 理由；重要取舍含未选方案  
- [ ] 编号连续；updated 已刷新  
- [ ] meta / execution / goal-tree 在需要时已对齐  
- [ ] 不确定处标「待确认」；内容为真实取舍  
```

---

## 使用注意事项

- 一条提示词可记多条决策，但请在输入区逐条列清，避免 AI 合并成含糊一段。
- 若决策已过时，用新条目 `superseded` 旧决策，并在旧条目状态改为 `superseded`，不要静默删除历史。
