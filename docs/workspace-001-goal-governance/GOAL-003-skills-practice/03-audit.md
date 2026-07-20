---
id: GOAL-003-skills-practice
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-18
updated: 2026-07-18
version: 0.2.1
---

# 审计 · GOAL-003

## A-004 · 关门审计：编排主路径对齐核心预期（2026-07-18）

### 范围与区间

- **区间**：A-003 重开 → 编排重做完成（同日）
- **类型**：关门审计
- **验收条**：`00-meta` **修订成功标准**（非 A-002 旧 5 项 alone）

### 对照修订成功标准

| 修订标准 | 状态 | 证据 |
|----------|------|------|
| 单一主入口 | **达成** | [skills/prompts/00-govern-orchestrator.md](../../../skills/prompts/00-govern-orchestrator.md)；[govern.md](../../../skills/install/copilot/prompts/govern.md) `/govern`；[skills/README.md](../../../skills/README.md) v0.3.0 |
| 情境分类 | **达成** | 编排器正文：扫描 goal-tree；S0–S3；未关门 vs 无总目的 |
| 设立引导 | **达成** | 编排器 S0/S1：先说清总目的再调 01 原语 |
| 推进引导 | **达成** | 编排器 S2：提议拆解/决策/执行/审计 → 确认 → 原语 |
| 原语降级 | **达成** | 01～04 `role: primitive`；四 slash `advanced`；prompts/README 分层 |
| 规则与安装 | **达成** | AGENTS.template 9b；根 AGENTS 9b；install.sh/ps1 安装 `govern`；claude/copilot 安装规则 |
| 历史地基 | **达成** | goal-folder 示例；skills-feedback；01～04 仍在 |

### 过程证据

- 决策：[01-decision.md](01-decision.md) **D-004**
- 执行：[02-execution.md](02-execution.md)「A-003 偏差审计后重开…」条目
- 偏差：[A-003](#a-003--偏差审计文档填表-vs-目的推进2026-07-18)（A-002 过早结项已记录，未删除）
- 测试：`python skills/tests/test_skills_orchestrator.py` → **7 tests OK**

### 偏差与遗留

- 外项目 install 实测仍可选，不阻塞本目标。
- 编排器为提示词契约（无独立 Agent 二进制）；实际对话质量依赖宿主模型，属预期范围。
- A-002 历史「5/5 done」叙事保留；**终态以本条 + 修订标准为准**。

### 结论

修订标准 **7/7**；`status` → **done**；`progress` → **100%**。  
GOAL-003 现符合「Skills 辅助设立/推进/审计目的」的核心预期（单入口编排 + 原语），而非仅四类填表模板。  
同步：`00-meta.md`、`goal-tree.md`、GOAL-001 阶段 2。

---

## A-003 · 偏差审计：文档填表 vs 目的推进（2026-07-18）

### 范围与区间

- **区间**：A-002 结项之后至本条（同日复盘）
- **类型**：结项后偏差审计（**不删除** A-001 / A-002）
- **触发**：对照 GOAL-001「Skills 辅助推进目标」与产品面实装，发现主路径漂移

### 偏差陈述

先前交付（以 A-002 验收为终点）把 Skills **产品主面**做成了「怎样辅助用户**填写四类治理文档**」，而非「怎样辅助用户**设立目标 → 推进目标 → 阶段性/关门审计**」。

| 维度 | 核心预期（GOAL-001） | A-002 时的实际形态 |
|------|----------------------|-------------------|
| 第一公民 | Goal / 目的闭环 | 文档操作类型（新建 / 决策 / 执行 / 复盘） |
| 用户入口 | 助手帮用户推进目标 | 四个并列 slash / 提示词，用户先选「填哪张表」 |
| 智能方向 | 情境分类 + 下一步建议 | 参数推断（编号、slug、parent）以减少表单项提问 |
| 成功标准 | 推进目标的可执行协作 | AGENTS + 4 模板 + folder 示例 + 一次反馈文档 |

### 证据（既有产物，未删改历史）

1. **四类并列主入口**：`skills/prompts/01-create-new-goal.md` … `04-write-audit.md`；Copilot wrapper `new-goal` / `log-decision` / `update-execution` / `write-audit`（见 `skills/install/copilot/prompts/`、`skills/README.md` v0.2.3）。
2. **提示词 README 定位**：「覆盖目标治理日常四类**操作**」——文档类型中心，非流程编排中心。
3. **安装 Next steps** 引导用户使用 01～04 与四个 slash，**无**「单一编排入口 / 先分类情境再行动」。
4. **A-002 成功标准 5/5** 全部可在「模板正确 + 写过反馈」下勾满，**不含**「无未关门总目的时引导表述总目的」「有未关门目标时提出可确认的下一步」。

### 对 A-002 的处理

- A-002 **保留**为历史记录：在其**当时窄成功标准**下结论成立。
- 相对 GOAL-001 Skills 意图，A-002 的 `done` / `100%` **过早**：将文书规范与原子操作误当作 Skills 阶段完成。
- **本条起**：GOAL-003 **重开**（`status: active`），进度回退；以「单一主入口编排 + 生命周期辅助」为修订成功标准后再结项。

### 进度与状态调整（本条）

| 字段 | 调整前（A-002 后） | 调整后 | 说明 |
|------|-------------------|--------|------|
| status | done | **active** | 重开，不以旧 5 项为终态 |
| progress | 100% | **40%** | 保留规则/原语/安装地基；编排主路径未交付 |

同步：`00-meta.md`、`goal-tree.md`、GOAL-001 路线图阶段 2。

### 结论

**偏差成立。** 下一步：决策层固定「单入口编排 + 01～04 降为原语」；重做 Skills 主路径；再以修订标准做关门审计。

---

## A-002 · 结项检查：强制使用反馈闭环（2026-07-18）

### 范围与区间

- **区间**：A-001 之后至结项（同日）
- **类型**：结项检查
- **覆盖**：成功标准后 2 项（强制使用 + 书面反馈；修正记录）及 GOAL-004 创建实践

### 成果（有证据）

1. **书面反馈已产出**  
   - 证据：[attachments/skills-feedback.md](attachments/skills-feedback.md)  
   - 要点：核心交付、wrapper 创建 GOAL-004 体验、优点、待改进、后续建议。

2. **本仓库已按 Skills 规则运行并有使用样本**  
   - 证据：GOAL-004 五件套 + goal-tree 同步 + P-001 路线图；本目标 execution 时间线与 A-001/A-002。  
   - 说明：wrapper「先分析上下文再补问」主路径在创建 GOAL-004 时可用。

### 对照成功标准

| 标准 | 状态 |
|------|------|
| AGENTS.template 可执行 | 已达成（A-001） |
| 4 类提示词可用 | 已达成（A-001） |
| goal-folder 示例 | 已达成（A-001） |
| 按规则运行并有书面反馈 | **已达成**（本条 + skills-feedback） |
| 修正记录已产出 | **已达成**（skills-feedback） |

### 偏差与遗留

- 外项目 install 实测仍为可选遗留（不阻塞结项）。
- wrapper 智能程度、01～04 多轮压测列为持续改进，见反馈文档第 4～5 节。

### 结论

成功标准 **5/5**；`status` → **done**；`progress` → **100%**。  
同步：`00-meta.md`、`02-execution.md`、`goal-tree.md`、GOAL-001 阶段 2。

---

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
