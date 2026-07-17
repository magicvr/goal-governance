---
id: GOAL-003-skills-practice
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.1.5
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
- 其余正文未改；当时进度仍约 **20%**（属模板打磨，未新开成功标准项）。

### 2026-07-18 · 完善 skills/templates/goal-folder/ 示例内容

- 将四份 Markdown 从极简占位改为虚构示例目标 **GOAL-042-optimize-readme**（优化项目 README 文档结构；`parent: GOAL-040-docs-quality`），避免使用本仓库真实 GOAL-00x。
- [00-meta.md](../../../skills/templates/goal-folder/00-meta.md)：概述、可勾选成功标准、parent 链接示例、复制后需改写的备注。
- [01-decision.md](../../../skills/templates/goal-folder/01-decision.md)：两条完整决策（决定 + 为什么 + 未选方案）。
- [02-execution.md](../../../skills/templates/goal-folder/02-execution.md)：按日时间线条目，只记事实与待办、进度评估。
- [03-audit.md](../../../skills/templates/goal-folder/03-audit.md)：一次阶段性复盘（成果 / 偏差 / 改进 / 结论）。
- `attachments/` 保持为空目录。
- 同步更新 [skills/README.md](../../../skills/README.md)、[skills/prompts/README.md](../../../skills/prompts/README.md) 对 goal-folder 的表述（由「空模板」改为「含示例的可复制模板」）。
- 成功标准「goal-folder 带有可参考的示例内容」已满足。

### 2026-07-18 · 进度复核至 50%

- 复核本日已完成产物：
  1. [skills/prompts/](../../../skills/prompts/) 及 4 个提示词模板 + README
  2. 提示词小优化（「信息缺失先确认」；创建后立刻记执行记录）
  3. [skills/templates/goal-folder/](../../../skills/templates/goal-folder/) 四文件示例（虚构 GOAL-042）
- 成功标准已勾选 2/5（提示词模板、goal-folder 示例）；AGENTS.template 优化与「强制使用 + 书面反馈」尚未开始。
- 进度由 **40%** 调整为 **50%**：前半段可复用产物已齐；实践验证与反馈闭环未启动。
- 阻塞 / 风险：无。
- 下一步（计划）：在本项目中强制使用这套 Skills，开始收集使用反馈；之后产出「Skills 使用反馈与修正记录」。

### 2026-07-18 · 优化 skills/AGENTS.template.md

- 重写 [skills/AGENTS.template.md](../../../skills/AGENTS.template.md)（version **0.2.0**），目标：规则更清晰可执行、减少歧义，并与根 [AGENTS.md](../../../AGENTS.md) 核心规则对齐。
- 主要改进：
  1. 用表格收敛「真相来源 / frontmatter / 写作要求 / 常见错误」，减少散文式歧义。
  2. 明确编号流程（先读 goal-tree）、`id` = 文件夹名、`parent` 必须为**完整 id（含 slug）**。
  3. 补齐 `status` 枚举与 `progress` 建议字段。
  4. P-001：补充「尚不可直接执行」判定标准；工作流标明 1–4 强制 / 5–6 按影响面。
  5. goal-tree 同步：显式含 `progress` 变更；写明「不更新视为任务未完成」。
  6. 新增完成前检查清单 + 常见错误对照表（适度，不冗长）。
  7. 保留并扩展 `{{占位符}}`（`APP_DIR`、`SKILLS_DIR`、`GOAL_FOLDER_TEMPLATE` 等）以保持可移植。
- 成功标准「AGENTS.template.md 规则可直接照做，歧义点已收敛」已勾选。
- 进度由 **50%** 调整为 **60%**（成功标准 3/5）；剩余「强制使用 + 书面反馈」与「修正记录」。
- 同步更新 [goal-tree.md](../goal-tree.md)。
- 阻塞 / 风险：无。根 `AGENTS.md` 未在本回合改写（本仓库生效规则仍以根文件为准；模板侧已对齐核心约束，后续若需字面同步可单开一轮）。

## 待办（按范围）

1. ~~优化 `skills/AGENTS.template.md`~~ **已完成**（见上，v0.2.0）
2. ~~补充常用提示词模板（新目标 / 决策 / 执行 / 复盘）~~ **已完成**
3. ~~完善 `skills/templates/goal-folder/` 示例内容~~ **已完成**
4. 在本项目强制使用并记录反馈
5. 产出「Skills 使用反馈与修正记录」

## 进度评估

**约 60%**：可复用产物三项（AGENTS.template / 提示词 / goal-folder 示例）已完成（成功标准 3/5 已勾选）；「强制使用 + 书面反馈」与修正记录尚未开始。
