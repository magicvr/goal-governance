---
id: GOAL-003-skills-practice
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.1.11
---

# 执行记录 · GOAL-003

## 时间线

### 2026-07-18 · 产出 Skills 使用反馈与修正记录并结项

- 基于本目标交付物与实际使用 wrapper 创建 GOAL-004 的体验，产出书面反馈：
  - [attachments/skills-feedback.md](attachments/skills-feedback.md)
- 反馈覆盖：核心交付清单、GOAL-004 创建体验、优点、待改进（wrapper 智能程度）、后续建议；语气客观中性。
- 成功标准后 2 项已勾选（强制使用 + 书面反馈；修正记录已产出）；成功标准 **5/5**。
- 进度调整为 **100%**；`status` 调整为 **done**。
- 同步 [00-meta.md](00-meta.md)、[goal-tree.md](../goal-tree.md)、[GOAL-001 路线图阶段 2](../GOAL-001-main-vision/00-meta.md)。
- 阻塞 / 风险：无。遗留改进见反馈文档（不阻塞本目标结项）。

### 2026-07-18 · 补充 Copilot wrapper 自动复制逻辑

- 更新安装脚本：使用 `--copilot` / `-Copilot` 或 `--all` / `-All` 时，自动：
  1. 创建目标项目根目录 `.github/prompts/`（若不存在）
  2. 将 [skills/install/copilot/prompts/](../../../skills/install/copilot/prompts/) 下 4 个 wrapper 复制为 `.github/prompts/*.prompt.md`（`new-goal` / `log-decision` / `update-execution` / `write-audit`）
- 涉及文件：
  - [skills/install.sh](../../../skills/install.sh) — Bash：Copilot 分支内循环 `copy_file`，目标固定 `.github/prompts/`
  - [skills/install.ps1](../../../skills/install.ps1) — PowerShell：同上逻辑
- 行为约定：wrapper 安装**不受** `--skills-dir` / `-SkillsDir` 影响，始终落在项目根 `.github/prompts/`；覆盖前仍询问。
- 更新帮助文案与 Next steps，说明会自动安装 Copilot slash wrappers。
- 更新 [skills/README.md](../../../skills/README.md)（version **0.2.3**）：Copilot 安装小节与脚本参数表，写明 wrapper 自动复制。
- 成功标准仍 **3/5**；属安装体验补全，不替代「强制使用 + 书面反馈」。
- 进度维持 **约 70%**。
- 阻塞 / 风险：无。

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

### 2026-07-18 · 完善 skills/ 安装体验

- 目标工具限定为 **Claude Code** 与 **GitHub Copilot**。
- 新增安装用规则（基于 `AGENTS.template.md` v0.2.0，做工具适配）：
  - [skills/install/claude/AGENTS.md](../../../skills/install/claude/AGENTS.md) → 复制到目标项目根 `AGENTS.md`
  - [skills/install/copilot/copilot-instructions.md](../../../skills/install/copilot/copilot-instructions.md) → 复制到 `.github/copilot-instructions.md`
- 新增可选安装脚本（离线、在当前工作目录安装、存在则询问覆盖）：
  - [skills/install.sh](../../../skills/install.sh) — Bash：`--claude` / `--copilot` / `--all` / `--help`
  - [skills/install.ps1](../../../skills/install.ps1) — PowerShell：`-Claude` / `-Copilot` / `-All` / `-Help`（兼容 `--*`）
  - `--all` 额外复制 `prompts/` 与 `templates/` 到目标项目 `skills/`
- 更新 [skills/README.md](../../../skills/README.md)（version **0.2.0**）：新增「安装」章节（手动推荐 + 脚本可选），更新目录结构与交付定位说明。
- 成功标准未新增勾选（仍 3/5）；属可复用交付物的安装路径完善，不改变「强制使用 + 反馈」待办。
- 进度维持 **约 60%**（可复用产物更完整；实践验证闭环未启动）。
- 阻塞 / 风险：无。本仓库根 `AGENTS.md` 仍为生效规则，未用 install 产物覆盖。

### 2026-07-18 · 中期复盘 A-001 后的跟进计划

- 完成中期复盘 [03-audit.md](03-audit.md) **A-001**（区间：立项至今日；类型：中期检查）。
- 结论摘要：可复用产物与 Claude/Copilot 安装支持基本完成（成功标准 3/5）；强制使用、书面反馈与修正记录未闭环；**不结项**。
- 进度由 **60%** 调整为 **70%**；`status` 保持 `active`。已同步 [00-meta.md](00-meta.md)、[goal-tree.md](../goal-tree.md)。
- 跟进计划（来自 A-001 改进措施，尚未执行）：
  1. 后续目标操作强制优先使用 `skills/prompts/`（01～04 至少各走通一轮），execution 记使用提示词与卡点。
  2. 产出「Skills 使用反馈与修正记录」（建议 `attachments/skills-feedback.md` 或本目标专节）。
  3. 任选 1 个外部/空项目实测 install 手动路径或脚本，结果写入反馈记录。
  4. 若改规则：先改 template，再按 D-003 评估同步根 AGENTS.md。
  5. 反馈可审计后再评估后 2 项成功标准与是否 `done`。

### 2026-07-18 · 优化安装流程与自定义 skills 目录支持

- 更新 [skills/README.md](../../../skills/README.md)（version **0.2.1**）「安装」章节：
  1. 明确先把整个 `skills/` 复制到目标项目根（可改名，如 `my-governance-skills`）。
  2. 说明 `--skills-dir` / `-SkillsDir`（默认 `./skills`）。
  3. 分步写清手动安装（Claude → 根 `AGENTS.md`；Copilot → 根 `.github/copilot-instructions.md`）与脚本安装。
  4. 强调提示词统一在 skills 目录下的 `prompts/`。
- 增强 [skills/install.sh](../../../skills/install.sh)、[skills/install.ps1](../../../skills/install.ps1)：
  - 新增 `--skills-dir` / `-SkillsDir`（默认 `./skills`）；相对路径相对当前工作目录（项目根）。
  - 规则文件始终安装到 **CWD**：`AGENTS.md`、`.github/copilot-instructions.md`（自动建 `.github/`）。
  - `--all` 时 `prompts/`、`templates/` 写入 `--skills-dir` 下。
  - 源文件读自**脚本所在包**；同源同目标时提示 Already present；保留覆盖确认与缺失源报错。
  - 更新帮助与示例。
- 核对安装规则源仍在位：
  - [skills/install/claude/AGENTS.md](../../../skills/install/claude/AGENTS.md)
  - [skills/install/copilot/copilot-instructions.md](../../../skills/install/copilot/copilot-instructions.md)
- 成功标准未新增勾选（仍 3/5）；属安装体验迭代，不改变「强制使用 + 反馈」待办。
- 进度维持 **约 70%**。
- 阻塞 / 风险：无。

### 2026-07-18 · 新增 Copilot 斜杠命令 wrapper

- 在 [skills/install/copilot/prompts/](../../../skills/install/copilot/prompts/) 新增 4 个轻量 wrapper：
  - [new-goal.md](../../../skills/install/copilot/prompts/new-goal.md) → `/new-goal` → 核心 [01-create-new-goal.md](../../../skills/prompts/01-create-new-goal.md)
  - [log-decision.md](../../../skills/install/copilot/prompts/log-decision.md) → `/log-decision` → 核心 [02-record-decision.md](../../../skills/prompts/02-record-decision.md)
  - [update-execution.md](../../../skills/install/copilot/prompts/update-execution.md) → `/update-execution` → 核心 [03-update-execution.md](../../../skills/prompts/03-update-execution.md)
  - [write-audit.md](../../../skills/install/copilot/prompts/write-audit.md) → `/write-audit` → 核心 [04-write-audit.md](../../../skills/prompts/04-write-audit.md)
- 各 wrapper：先收集必要参数 → 明确引用 `./skills/prompts/` 核心提示词 → 强调 AGENTS（五件套、goal-tree、P-001 等）→ 注释说明「改核心即可全局生效」。
- 更新 [skills/README.md](../../../skills/README.md)（version **0.2.2**）：目录结构、Copilot 安装小节（wrapper 位置、复制到 `.github/prompts/*.prompt.md` 的用法）。
- 成功标准仍 **3/5**；属 Copilot 入口体验，不替代「强制使用 + 书面反馈」。
- 进度维持 **约 70%**。
- 阻塞 / 风险：无。

## 待办（按范围）

1. ~~优化 `skills/AGENTS.template.md`~~ **已完成**（见上，v0.2.0）
2. ~~补充常用提示词模板（新目标 / 决策 / 执行 / 复盘）~~ **已完成**
3. ~~完善 `skills/templates/goal-folder/` 示例内容~~ **已完成**
4. ~~在本项目强制使用并记录反馈~~ **已完成**（见 [attachments/skills-feedback.md](attachments/skills-feedback.md)；含 wrapper 创建 GOAL-004）
5. ~~产出「Skills 使用反馈与修正记录」~~ **已完成**（同上）
6. （可选，结项后遗留）外项目实测 install 路径，结果并入反馈记录修订版

## 进度评估

**100%**：成功标准 **5/5** 已达成。可复用产物（AGENTS.template / 提示词 / goal-folder）、Claude Code / Copilot 安装与 wrapper、本仓库强制使用与书面反馈均已落地；结项后可继续按反馈改进 wrapper 智能程度，不阻塞本目标 `done`。
