---
title: 提示词 · 创建新目标
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
---

# 01 · 创建新目标

## 说明

解决「要新增一个目标，但容易漏五件套、编号冲突、忘更新 goal-tree、大目标直接拆碎」的问题。  
把本提示词交给 AI 后，应得到：正确编号的目标文件夹 + 完整五件套 + 已同步的 `goal-tree.md`。

---

## 提示词正文

```markdown
你是本仓库的目标治理协作者。请严格遵守根目录 AGENTS.md 与 docs/architecture/principles.md（尤其 P-001）。

## 任务
按下列信息创建一个新目标。不要省略任何必备文件。

## 用户输入（请先向我确认空白项，或使用我填写的内容）
如果某项信息缺失或不确定，请先向我确认，不要猜测后继续。
- 目标标题：【填写】
- 英文短 slug（小写、短横线）：【填写，如 skills-practice】
- 父目标 ID：【填写，如 GOAL-001-main-vision；Root 则写 null】
- 一句话概述：【填写】
- 成功标准（可验证的勾选项）：【列出 2～5 条】
- 是否明显需要拆解（尚不能直接执行）？【是 / 否】
- 若「是」：请先在 00-meta 或 01-decision 写高层路线图（阶段 + 先后关系），本回合**不要**批量创建细粒度子目标
- 初始状态：draft 或 active（默认 draft）
- 今日日期：【YYYY-MM-DD】

## 强制步骤（按顺序）
1. 读取 `docs/goals/goal-tree.md`，确认当前最大编号；新编号 = 最大编号 + 1（三位，如 GOAL-004）。GOAL-001 永久为 Root，禁止改号。
2. 文件夹名：`docs/goals/GOAL-NNN-<slug>/`（平铺在 docs/goals/ 下，禁止用子文件夹表达父子关系）。
3. 一次创建完整五件套：
   - 00-meta.md
   - 01-decision.md
   - 02-execution.md
   - 03-audit.md
   - attachments/（可空，目录必须存在）
4. 可参考 `skills/templates/goal-folder/` 的结构与字段。
5. 每个 Markdown 文件 frontmatter 至少包含：status, created, updated, parent, version。
   - 00-meta.md 还必须有：id, title；建议有 progress。
   - parent 填父目标完整 ID，或 Root 时为 null。
6. 内容要求：
   - 00-meta：概述、范围（可选）、成功标准、父目标链接
   - 01-decision：若已有明确取舍则写「决定了什么 + 为什么」；暂无则写「待立项后补充」，不要编造决策
   - 02-execution：时间线只记真实事实（如「今日创建目标」）；不写未发生的工作
   - 03-audit：可写「尚未到达复盘节点」
7. **必须**同步更新 `docs/goals/goal-tree.md`：ASCII 树 + 状态表格都要有新目标。
8. 若父目标进度/说明需要轻量提及「已挂新子目标」，可更新父目标相关文档；不要伪造父目标完成度。

## 禁止
- 禁止在 docs/goals/ 下嵌套目标文件夹表示层级
- 禁止跳过 goal-tree.md
- 禁止对大目标跳过路线图、直接创建大量子目标
- 禁止虚构已完成工作或审计结论

## 交付检查清单
完成后逐条自检并简短汇报：
- [ ] 编号正确且未与现有冲突
- [ ] 五件套齐全
- [ ] parent 正确
- [ ] goal-tree.md 已更新
- [ ] 大目标已写路线图（若适用）
- [ ] 无编造进度
```

---

## 使用注意事项

- 创建前先在对话里填好标题、父目标与是否需拆解；AI 缺信息时应先问再写。
- 目标创建完成后，建议立刻使用「03-update-execution」提示词，追加一条「目标已创建」的执行记录。
- Root Goal 只能是 GOAL-001 且 `parent: null`；一般不要用本提示词「重建 Root」。
- 若只是草稿试探，状态用 `draft`，并在 goal-tree 中如实标注。
