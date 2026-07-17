---
id: GOAL-003-skills-practice
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.1.2
---

# 执行记录 · GOAL-003

## 时间线

### 2026-07-18 · 目标立项

- 在 GOAL-001 下创建本目标完整五件套（meta / decision / execution / audit / attachments）。
- 在决策记录中确认：优先完善 Skills 再推进 Web 数据能力（见 [01-decision.md](01-decision.md) D-001）。
- 同步更新 [goal-tree.md](../goal-tree.md) 登记 GOAL-003。
- 当时进度 **0%**：仅完成立项与范围界定。

### 2026-07-18 · 新增 skills/prompts/ 提示词模板

- 创建目录 [skills/prompts/](../../../skills/prompts/)。
- 新增文件：
  - [README.md](../../../skills/prompts/README.md) — 目录用途与使用方式
  - [01-create-new-goal.md](../../../skills/prompts/01-create-new-goal.md) — 创建新目标
  - [02-record-decision.md](../../../skills/prompts/02-record-decision.md) — 记录决策
  - [03-update-execution.md](../../../skills/prompts/03-update-execution.md) — 更新执行进度
  - [04-write-audit.md](../../../skills/prompts/04-write-audit.md) — 写阶段性复盘
- 各提示词均要求遵守 AGENTS（扁平存储、parent、五件套、goal-tree 同步、P-001 路线图优先），并引导结构化、可验证输出。
- 同步更新 [skills/README.md](../../../skills/README.md) 目录说明，去掉「提示词尚未包含」的表述。
- 成功标准「至少 4 类常用提示词模板可用」对应产物已落地；其余项未动。

### 2026-07-18 · 微调 prompts 四个提示词模板

- 四个文件（01～04）的「用户输入」统一增加：信息缺失或不确定时先确认、不猜测后继续。
- [01-create-new-goal.md](../../../skills/prompts/01-create-new-goal.md)「使用注意事项」增加：创建完成后建议立刻用 03-update-execution 追加「目标已创建」执行记录。
- 其余正文未改；进度仍约 **20%**（属模板打磨，未新开成功标准项）。

## 待办（按范围）

1. 优化 `skills/AGENTS.template.md`
2. ~~补充常用提示词模板（新目标 / 决策 / 执行 / 复盘）~~ **已完成**（见上）
3. 完善 `skills/templates/goal-folder/` 示例内容
4. 在本项目强制使用并记录反馈
5. 产出「Skills 使用反馈与修正记录」

## 进度评估

**约 20%**：4 类提示词模板已就绪；AGENTS.template 优化、goal-folder 示例、强制使用反馈与修正记录尚未开始。
