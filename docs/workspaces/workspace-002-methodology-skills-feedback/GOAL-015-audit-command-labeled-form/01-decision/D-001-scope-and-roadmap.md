---
id: GOAL-015-audit-command-labeled-form
doc: decision-entry
record_id: D-001
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

## D-001 · 立项范围、路线图与用户裁决（2026-10-17）

### 触发

1. 用户 2026-10-17 指令原文：「在工作区2添加一个子目标，我们上一次修正搞错了一点小问题，形式审计命令应该是 `/audit workspace-<工作区编号> goal-<目标编号>` 和 `/vision-audit vp-<vp编号>`。现在误成了类似 `/audit 3 2` 的命令（显然就不对了）。做一个小的修正。」
2. 偏差来源可核对：用户 2026-10-16 的原始要求为「只允许向审计员输入形式审计命令 `/audit <工作区编号> <目标编号>` 或 `/vision-audit <vp编号>`」（[GOAL-013 D-001](../../GOAL-013-audit-dispatch-and-user-input-gates/01-decision/D-001-scope-and-roadmap.md)），而 [GOAL-013 D-002](../../GOAL-013-audit-dispatch-and-user-input-gates/01-decision/D-002-s1-contract-proposal.md) 把选择器写成裸数字 `/audit NNN NNN`，并写入 `principles.md` AD-01 与全部消费面。因此本轮是**恢复用户原始形式**，不是新增需求。
3. 编排前只读核对：全仓带旧形式的文件约 35 个（canonical 3、根 AGENTS 1、Skills prompts 5、四宿主安装源 19、MCP 2、契约测试 1，另有 stage 镜像与 dogfood 副本由脚本/拷贝同步）。
4. 已知后果：根 `AGENTS.md` 与 `skills/prompts/00-govern-orchestrator.md` 是运行证据的 `behaviorSources`，改后 16 份「当前来源一致」记录会过期（同 GOAL-010 曾遇到的情形）。

### 决定

1. 在本区创建 **GOAL-015-audit-command-labeled-form**（`active`，parent = 本区 Root），承载该修正；不重开已 `done` 的 GOAL-013。
2. 纲领路线图 S1～S4 见 [00-meta.md](../00-meta.md#纲领路线图p-001)：契约冻结 → 规范与消费面同步 → 验证与证据影响核对 → cross 审计与关门。本目标为可直接执行的小目标，阶段内不拆子目标。
3. 语法与拒绝面冻结见 [D-002](D-002-labeled-command-contract.md)。
4. 范围含本次实施；**不含**运行证据重捕获、版本发布/tag/Release。
5. 审计模式 `cross`（改 P-003 元规则）；independent provider = **Grok Build**。

### 用户裁决留痕（同步阻塞卡片，2026-10-17）

| 问题 ID | 原题 / 选项 | 影响门禁 | 真实答复 |
|---------|-------------|----------|----------|
| Q-001 | GOAL-015 本次做到哪一步？A：立项 + 立即实施修正（推荐）；B：只立项 + 冻结契约；C：立项 + 实施 + 本次重捕获 16 份运行证据 | 实施范围与验收边界 | **A** |
| Q-002 | cross 审计的 independent provider：A：Grok Build（沿用 GOAL-013/014，推荐）；B：Claude Code CLI；C：稍后指定 | S4 审计与关门 | **A（Grok Build）** |

卡片展示与提交均在本会话实际发生；未选的 B/C 不作默认推定，不记 residual。

### 为什么

- 用户原始要求本就是带标签形式；裸数字 `3 2` 对人和审计员都不可自解释，恢复带标签形式同时消除「形式命令」与「自由提示」之间的辨识成本。
- GOAL-013 已 `done`，按治理规则不自动 reopen；形式偏差以新子目标承接，保留原目标的关门事实与历史记录。
- 一次改完规范与全部消费面，避免只改 canonical 造成发货面与镜像漂移（§8c 与「源/安装/dogfood 一致」测试会立刻抓到）。

### 未选方案

- **B 只立项 + 冻结契约**：把实施推到下一轮；本轮用户已授权立即实施，故不选。
- **C 立项 + 实施 + 本次重捕获 16 份运行证据**：需真实调用 4 个宿主 CLI，耗时长且可能失败；用户选择把重捕获留在本目标之外（不选）。
- **保留裸数字兼容窗口**：会让入口同时存在两种形式，违背「仅正式命令」的收敛目的；D-002 明确拒绝。
- **把形式偏差直接回写进 GOAL-013 台账**：会改写已关门的审计与执行事实；改为在 GOAL-013 D-002 加「现时注」指针，不改其结论。
