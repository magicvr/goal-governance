---
id: GOAL-003-skills-practice
doc: audit
status: active
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.1.1
---

# 审计 · GOAL-003

## A-001 · 中期检查：Skills 可复用产物与安装支持（2026-07-18）

### 范围与区间

- **区间**：2026-07-18（立项）～ 2026-07-18（今日）
- **类型**：中期检查
- **覆盖**：GOAL-003 范围内可复用产物（AGENTS 模板、提示词、goal-folder 示例）及当日补齐的 Claude Code / Copilot 安装路径；不含 Web 与自动化校验

### 成果（有证据）

1. **AGENTS 模板可执行化**  
   - 证据：[skills/AGENTS.template.md](../../../skills/AGENTS.template.md) 升至 v0.2.0；[02-execution.md](02-execution.md)「优化 skills/AGENTS.template.md」；[00-meta.md](00-meta.md) 成功标准第 1 项已勾选。  
   - 要点：表格化真相来源 / frontmatter / 常见错误；明确编号、`parent` 完整 id、status 枚举、P-001、goal-tree 同步与完成前检查清单。

2. **4 类实用提示词模板**  
   - 证据：[skills/prompts/](../../../skills/prompts/)（01 新目标 / 02 决策 / 03 执行 / 04 复盘 + README）；execution「新增 skills/prompts/」与「微调 prompts」。  
   - 要点：均要求遵守 AGENTS；用户输入缺失时先确认；创建目标后建议立刻记执行记录。

3. **goal-folder 示例内容**  
   - 证据：[skills/templates/goal-folder/](../../../skills/templates/goal-folder/) 以虚构 GOAL-042-optimize-readme 填充四文件；meta 成功标准第 3 项已勾选。  
   - 要点：决策含未选方案；执行按日事实；审计含完整阶段性结构。

4. **Claude Code / Copilot 安装支持（手动 + 脚本）**  
   - 证据：execution「完善 skills/ 安装体验」；[skills/install/claude/AGENTS.md](../../../skills/install/claude/AGENTS.md)、[skills/install/copilot/copilot-instructions.md](../../../skills/install/copilot/copilot-instructions.md)、[skills/install.sh](../../../skills/install.sh)、[skills/install.ps1](../../../skills/install.ps1)；[skills/README.md](../../../skills/README.md) v0.2.0「安装」章节。  
   - 说明：属可复用交付路径完善；**未**新增成功标准勾选（仍 3/5）。

5. **过程治理本身按 Skills 运转**  
   - 证据：本目标五件套齐全；decision D-001～D-003；execution 时间线与进度复核；goal-tree 已登记 GOAL-003。  
   - 说明：证明「写文档」路径可用，但尚不等于「强制使用 + 书面反馈」已完成。

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| `skills/AGENTS.template.md` 规则可直接照做，歧义点已收敛 | 已达成 | template v0.2.0；meta 已勾选；execution 优化条目 |
| 至少 4 类常用提示词模板可用（新目标 / 决策 / 执行 / 复盘） | 已达成 | `skills/prompts/01`～`04` + README；meta 已勾选 |
| `skills/templates/goal-folder/` 带有可参考的示例内容 | 已达成 | GOAL-042 虚构示例四文件；meta 已勾选 |
| 本仓库协作已按 Skills 规则运行，并有书面使用反馈 | 部分 | 本目标协作已按规则运行（meta/decision/execution/本复盘）；**书面使用反馈尚未产出**；提示词尚未在多轮真实协作中大量强制使用 |
| 「Skills 使用反馈与修正记录」已产出 | 未开始 | execution 待办第 5 项仍开放；`attachments/` 与文档内均无该记录 |

### 偏差与问题

1. **实践验证闭环未启动**：成功标准后 2 项依赖「强制使用 + 书面反馈」，execution 明确「实践验证闭环未启动」。
2. **提示词使用深度不足**：4 类模板已落盘，但尚未在真实协作中大量强制调用并沉淀问题清单。
3. **安装物未做外项目验证**：`install.sh` / `install.ps1` 与 install 规则仅在本仓库交付，未见其他项目实测记录。
4. **根规则与模板的字面同步未做**：execution 注明根 [AGENTS.md](../../../AGENTS.md) 未在本回合改写；生效仍以根文件为准，模板侧已对齐核心约束（见 D-003）。
5. **范围轻扩展（可接受）**：meta「不在范围内」写了「完整可安装 Skill 包」；实际交付了 Claude/Copilot 的手动复制 + 可选脚本，属于安装体验而非完整 Skill 包，未改成功标准，需在后续反馈中确认是否正式纳入范围描述。

### 根因（简要）

- 当日工作优先完成「可复制产物」与安装路径，有意把「强制使用与反馈」留到产物齐备之后（execution 进度复核与安装条目均如此表述）。
- 反馈与修正记录依赖真实使用次数；立项当日完成物多、跨项目试用少，证据不足。
- 安装脚本属于便利层，验证成本在「复制到其他仓库跑一遍」，尚未排入执行。

### 改进措施（可执行）

- [ ] 在本仓库后续目标操作中**强制**优先使用 `skills/prompts/`（至少各走通 01～04 一轮），每轮在 execution 记「使用了哪条提示词 / 卡点」。
- [ ] 产出「Skills 使用反馈与修正记录」（建议 `attachments/skills-feedback.md` 或本目标 execution 专节），覆盖：歧义点、漏步骤、与根 AGENTS 不一致处。
- [ ] 任选 1 个外部/空项目目录，用手动或 `install.ps1`/`install.sh` 实测 Claude 与 Copilot 安装路径，把结果写入反馈记录。
- [ ] 若反馈要求改规则：先改 `skills/AGENTS.template.md`，再按 D-003 评估是否同步根 `AGENTS.md`，并记 execution。
- [ ] 反馈闭环达到可审计后，再评估是否将 success 后 2 项勾选并考虑 `done`（不在本次中期检查关闭目标）。

### 结论

可复用侧（AGENTS 模板、4 类提示词、goal-folder 示例）与 Claude/Copilot 安装支持在立项当日已基本落地，成功标准 **3/5 已达成**；目标价值的后半段——**强制使用、书面反馈与修正记录**——证据仍不足，**不宜结项**。  
**建议**：`status` 保持 `active`；`progress` 由 **60%** 调整为 **70%**（产物与安装路径完成度提高，实践验证权重仍大）；下一步按改进措施推进强制使用与反馈文档，不以安装脚本「看起来完整」代替闭环。

### 进度与状态调整（本复盘）

| 字段 | 调整前 | 调整后 | 说明 |
|------|--------|--------|------|
| status | active | active | 中期检查，不关闭 |
| progress | 60% | 70% | 可复用产物 + 安装支持；成功标准仍 3/5 |

同步：`00-meta.md`、`docs/goals/goal-tree.md`。
