---
title: 提示词 · 写阶段性复盘
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.2.0
role: primitive
---

# 04 · 写阶段性复盘（原语 / primitive）

## 说明

**角色**：文档原语，供 [00-govern-orchestrator.md](00-govern-orchestrator.md) 调用；也可高级直调。默认用户路径请用编排器。

解决「阶段结束了却没有结论，或复盘写成表扬稿」的问题。  
引导 AI 基于 `00-meta` / `01-decision` / `02-execution` 的**已有事实**，在 `03-audit.md` 写出成果、偏差、改进与结论。

---

## 提示词正文

```markdown
# 角色
你是本项目的目标治理协作者。遵守 `AGENTS.md` 和/或 `.github/copilot-instructions.md`。

# 任务
基于已有 meta / decision / execution，在 `03-audit.md` **追加**阶段性复盘（保留历史章节）。成果须能指回文档证据。

# 用户输入（缺项先确认）
- 目标 ID / 路径：
- 复盘区间：
- 类型：中期检查 / 阶段结束 / 目标关闭
- 你认为的成果（可选，可先由文档归纳再确认）：
- 已知偏差（可选）：
- 是否调整 status/progress：【否 / 是，说明】
- 今日日期：

# 步骤
1. 通读 `00-meta`、`01-decision`、`02-execution`、现有 `03-audit`。
2. 对照成功标准：已达成 / 部分 / 未开始 / 证据不足。
3. 追加一节（A-001 起递增）：

   ## A-NNN · <标题>（YYYY-MM-DD）
   ### 范围与区间
   ### 成果（有证据）— 指向文件、决策号或 execution 条目
   ### 对照成功标准（表：标准 | 状态 | 证据）
   ### 偏差与问题 / 根因 / 改进措施（可勾选）
   ### 结论 + 建议下一步

4. 刷新 `updated`。
5. 立刻要做的跟进可记入 execution（标为计划）；正式取舍写入 decision。
6. status/progress 变更时同步 meta 与 goal-tree。
7. 语气具体、可验证；证据不足时写明缺口，状态用「部分/未开始/证据不足」。

# 完成标准
- [ ] 有编号与日期；历史复盘仍在  
- [ ] 成果均可指回证据  
- [ ] 成功标准对照完整  
- [ ] 改进措施可执行  
- [ ] status/progress 变更已同步 meta 与 goal-tree  
```

---

## 使用注意事项

- 中期复盘不必强行关闭目标；结论可以是「继续，但收窄范围」。
- 若材料不足，应让 AI 列出「证据缺口」而不是脑补成果。
- 目标正式 `done` 前，建议至少有一次阶段复盘（A-00x）沉淀结论。
