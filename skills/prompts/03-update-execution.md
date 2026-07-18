---
title: 提示词 · 更新执行进度
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.1
role: primitive
---

# 03 · 更新执行进度（原语 / primitive）

## 说明

**角色**：文档原语，供 [00-govern-orchestrator.md](00-govern-orchestrator.md) 调用；也可高级直调。默认用户路径请用编排器。

解决「做了工作却不写、或写成虚假 100%」的问题。  
引导 AI 在 `02-execution.md` 按时间线追加**事实**，并在确有进展时同步 meta / goal-tree 的进度。

---

## 提示词正文

```markdown
你是本项目的目标治理协作者。遵守项目 AI 规则（根 `AGENTS.md` 和/或 `.github/copilot-instructions.md`）。

## 任务
更新指定目标的执行记录与（如适用）进度。只记录真实发生的工作。

## 用户输入
如果某项信息缺失或不确定，请先向我确认，不要猜测后继续。
- 目标 ID / 路径：【如 GOAL-003-skills-practice】
- 今日日期：【YYYY-MM-DD】
- 本次实际完成的工作（条目列表，务必具体）：
  1. 【例如：完成了某某模块的接口草稿；路径按项目实际填写】
  2. 【……】
- 阻塞 / 风险（如有）：【填写或「无」】
- 下一步计划（可选，标为计划而非已完成）：【填写】
- 进度百分比是否调整：【保持 / 调整为 N%】
  - 若调整：给出简短依据（对照 00-meta 成功标准勾选情况）
- status 是否变化：【保持 / 改为 draft|active|blocked|done|cancelled】

## 强制步骤
1. 读取该目标 `00-meta.md`、`02-execution.md`，以及 `docs/goals/goal-tree.md`。
2. 在 `02-execution.md` 的「时间线」下追加一节：

   ### YYYY-MM-DD · <短标题>
   - 事实条目（做了什么、改了哪些路径）
   - 阻塞（如有）
   - 下一步（如有，明确是计划）

3. 内容规则：
   - **只写已发生事实**；未做的事不得写成完成。
   - 尽量带路径或产物名，避免「优化了体验」这类空话。
   - 不要回填虚构的历史日期。
4. 更新 frontmatter `updated`。
5. 若用户要求调整 progress/status：
   - 改 `00-meta.md` 的 progress / status / updated
   - **必须**同步 `docs/goals/goal-tree.md` 的树与表格
6. 若本次完成了某条成功标准，可在 `00-meta.md` 将对应 `- [ ]` 改为 `- [x]`，并在 execution 中点明。
7. 待办列表（若 execution 中有）按事实勾掉或改写，勿把计划项标成已完成。

## 进度评估写法（建议）
在 execution 文末用一两句说明当前百分比依据，例如：
「约 20%：提示词模板已落地；AGENTS 优化、示例内容、使用反馈尚未开始。」

## 禁止
- 禁止编造未提交/未创建的文件与结果
- 禁止无依据地把进度写成 100%
- 禁止改 status/progress 却不更新 goal-tree.md
- 禁止把决策论证长文塞进 execution（决策去 01-decision.md）

## 交付检查清单
- [ ] 时间线新增条目为事实
- [ ] updated 已刷新
- [ ] progress/status 与 meta、goal-tree 一致（若有变更）
- [ ] 成功标准勾选与事实一致
```

---

## 使用注意事项

- 输入区尽量写「改了什么文件 / 达成什么可验证结果」，AI 才能避免空话。
- 小步提交时 progress 可保持不变，只追加时间线即可。
- 若工作实际属于另一目标，应改记到正确目标，勿堆在错误 ID 下。
