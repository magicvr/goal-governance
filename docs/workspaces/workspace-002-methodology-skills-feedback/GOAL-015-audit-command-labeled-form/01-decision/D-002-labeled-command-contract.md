---
id: GOAL-015-audit-command-labeled-form
doc: decision-entry
record_id: D-002
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

## D-002 · 带标签审计命令契约冻结与写集（2026-10-17）

### 触发

[D-001](D-001-scope-and-roadmap.md) 立项后，实施前必须冻结「形式命令」的精确语法与拒绝面，否则 35 个消费面会各自解释。旧契约（GOAL-013 D-002 / `principles.md` AD-01）为裸数字 `/audit NNN NNN`、`/vision-audit NNN`，与用户原始要求的形式命令不一致。

### 决定

1. **正式命令**：自动派发向审计员输入的语义正文只能是单行
   - `/audit workspace-<W> goal-<G>`
   - `/vision-audit vp-<V>`
2. **选择器语法**：前缀 `workspace-`、`goal-`、`vp-` 必须为**小写 ASCII 且拼写固定**，与命令名同级、由单个空格分隔；`<W>` / `<G>` / `<V>` 为 1～3 位 ASCII 十进制正整数（1～999），入口按数值补零为三位。规范输出形式为 `/audit workspace-002 goal-015`、`/vision-audit vp-002`。
3. **拒绝面**（入口 fail closed，不得截断附言后发送）：
   - 裸数字：`/audit 002 015`、`/vision-audit 002`；
   - 缺失、错误或大小写不符的前缀：`VP-002`、`Ws-002`、`ws-002`、`workspace002`；
   - 顺序或组合错误：`/audit goal-015 workspace-002`、只给一个选择器、多给选择器；
   - 完整 id / slug 冒充选择器：`workspace-002-methodology-skills-feedback`、`goal-015-audit-command-labeled-form`、`VP-002-methodology-skills-feedback-evolution`；
   - 编号非法：0、非数字、负数、小数、科学计数、超过三位、未替换占位；
   - 形态非法：多余参数、换行、注释、代码块包装、引号包裹。
4. **语义不变**：选择器仍只是入口选择器；AD-02 唯一绑定、AD-03 不限制视角、AD-04 干净上下文、AD-05 失败不替代、AD-06 通道与保证均不变。解析仍按 `workspace-protocol.md` §2.7：先唯一匹配 `workspaces/workspace-<NNN>-<slug>/workspace.md`，再在该区唯一匹配 `GOAL-<NNN>-<slug>/00-meta.md`；`/vision-audit` 在 `vision/plans/VP-<NNN>-<slug>.md` 唯一匹配。解析成功后仍以完整 `workspace_id` + `goal_id`（Q1）或 VP id 为身份，Q2/Q3 与区内短 `parent` 不变。
5. **不设兼容窗口**：裸数字形式不再合法；历史台账、审计记录与运行证据中的旧形式**保留原样**（历史事实），只加「现时注」指针，不回写。
6. **写集**（改一处即须同改其余，顺序 canonical → Skills → 安装源 → dogfood → 镜像 → MCP → 测试）：

   | 面 | 路径 |
   |----|------|
   | canonical | `docs/architecture/principles.md`（AD-01、AD-02、示例）、`docs/architecture/workspace-protocol.md`（§2.7）、`docs/vision/alignment.md`（§9.3） |
   | 仓库规则 | 根 `AGENTS.md` §6b |
   | Skills prompts | `skills/prompts/00-govern-orchestrator.md`、`04-write-audit.md`、`05-independent-audit.md`、`06-vision-orchestrator.md`、`07-independent-vision-review.md` |
   | 规则模板 | `skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md`、`.github/copilot-instructions.md` |
   | 四宿主安装源 | `skills/install/{claude,grok,codex}/skills/{govern,audit,vision,vision-audit}/SKILL.md`（含 `argument-hint`）、`skills/install/copilot/prompts/{govern,audit,vision,vision-audit}.md` |
   | MCP guidance | `mcp/entries.py`、`mcp/README.md` |
   | 契约测试 | `skills/tests/test_governance_interaction_contract.py`（含防再犯守卫） |
   | 生成/拷贝面 | `skills/core/docs/**`（stage 脚本）、`.claude|.grok|.agents/skills/**`、`.github/prompts/*.prompt.md`（dogfood 副本） |
   | 边界记录 | `docs/README.md`（当前工作树边界补记：16 份运行记录过期事实；否则该文件叙述失真） |
   | 历史指针 | GOAL-013 `01-decision/D-002-s1-contract-proposal.md` 的「现时注」（只加指针，不改其结论、状态与 verdict） |

### 为什么

- 前缀 + 编号把「工作区编号 / 目标编号 / VP 编号」写进命令本身，人、审计员与入口都能自解释，避免 `3 2` 这类无标签数字被误读为阶段、条数或版本。
- 固定小写单一拼写使入口能无歧义判定「是否正式命令」，不需要前缀匹配、别名或大小写宽容，也就没有「先删附言再派发」的灰色地带。
- 明确拒绝完整 id / slug：选择器保持纯数字语义，身份解析仍由 §2.7 唯一绑定负责，不引入第二套寻址写法。

### 未选方案

- **保留裸数字兼容**：两种形式并存会让「仅正式命令」失去收敛意义，且旧形式正是本次要修的偏差。
- **接受 `workspace-002-methodology-skills-feedback` 等完整 id**：等价形式会让选择器与身份混淆，并使 §2.7 的「纯编号唯一匹配」失效。
- **前缀大小写不敏感（接受 `VP-002`）**：扩大接受面需要额外测试与解释，且自动派发侧不需要该宽容度；人类直调本就可另附关注点。
- **同时支持 `goal-<NNN>-<slug>`**：slug 会引入拼写容错问题，无收益。
