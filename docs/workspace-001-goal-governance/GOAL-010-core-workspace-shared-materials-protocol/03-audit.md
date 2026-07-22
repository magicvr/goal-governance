---
id: GOAL-010-core-workspace-shared-materials-protocol
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-20
version: 0.3.0
---

# 审计 · GOAL-010

## 初始审视状态（历史）

本目标刚完成立项。D-001 已记录范围、路线图和 I-001～I-005；尚未产生实现或验证事实，也尚未到达阶段或关门审计节点。后续自审必须核对 canonical 协议、Skills 镜像、legacy 单工作区兼容、共享资料引用的拒绝路径，以及与 GOAL-009 未关闭门禁的边界。

## A-001 · core/Skills 工作区协议关门自审（2026-07-20）

- **source**：self
- **auditor**：`/govern`（Codex）
- **类型**：close-out
- **scope**：D-001/D-002 的 core 文档协议、可复制模板、Skills 消费适配、镜像/standalone/安装验证，以及 GOAL-009 R-003 的协议交接边界。
- **verdict**：pass

### 证据与对照

| 关门项 | 可核对证据 | 结论 |
|--------|------------|------|
| 工作区/Root Goal/串行阶段/legacy | [workspace-protocol.md](../../architecture/workspace-protocol.md) 第 2～4 节、[workspace-context.md](../../templates/workspace-context.md)、`docs/tests/test_workspace_protocol.py` | I-001 已验证；显式绑定和隐式单工作区均有可读规则与测试。 |
| 固定资料引用与拒绝路径 | 协议第 5 节、模板引用表、有效引用与 workspace 不匹配/无效摘要负例测试 | I-002 已验证；引用不会成为跨工作区状态或未经确认的事实捷径。 |
| Skills first 消费 | `skills/prompts/00`～`05`、Claude/Grok/Copilot 规则镜像、`skills/tests/test_skills_orchestrator.py` | I-003 已验证；有 context 时先校验、无 context 时保持 legacy，失配 fail closed。 |
| 分发与独立启用 | `docs/tests/test_standalone_bootstrap.py`、canonical/Skills 镜像断言、F-018 isolated install smoke | I-004 已验证；core 可以独立启用，分发包包含一致的模板和规则。 |
| 下游交接 | [GOAL-009 02-execution](../GOAL-009-ai-assisted-governance-workbench/02-execution.md) 与 A-008 | I-005 保持 `non-blocking / open`；未将 I-009/I-010、F-003/F-004 或 Web 门禁写成关闭。 |

### 验证结果

- 在原生 CPython 3.14.6 `.venv` 中，`python -m unittest discover -s docs\\tests -v`：8 passed。
- `python -m unittest skills\\tests\\test_skills_orchestrator.py -v`：32 passed。
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\\skills\\tests\\test_install_ps1_isolated.ps1`：F-018 isolated install passed。
- `web/` 中的 `python -m unittest discover -s tests -v`：20 passed、1 个 Windows symlink 权限跳过。

这些测试覆盖本目标的文档、模板、适配和安装表面；本审计不声称共享资料物理存储、用户 CRUD、AI 执行、跨工作区访问模型或部署已经验证。`scripts` 的 release-evidence 组正确拒绝了已被本次行为变更弄旧的 GOAL-008 runtime evidence；它要求下一次发布前重新取得真实宿主证据，不是本目标 required 信息门禁的失败。

### Findings 与结论

本目标没有 open required finding，也没有 residual risk 接受。I-001～I-004 已有对应产物和可重复验证；I-005 是明确排除的非阻塞下游范围。下一次包含新 `govern` 行为的发布应按 GOAL-008 的运行时证据流程重新验证。GOAL-010 因此满足 D-002、P-002 与 P-005 的关门条件，状态可以为 `done / 100%`。

## A-002 · 工作区协议与 GOAL-011 目录迁移的回归影响独立审计（2026-07-20）

- **source**：independent
- **auditor**：Codex `/audit`
- **类型**：ad-hoc
- **scope**：D-001/D-002 的工作区协议在 GOAL-011 将本仓库迁移到显式工作区根后，对已关门 GOAL-002～GOAL-008 的实际产物、当前消费者与历史记录的影响。
- **verdict**：pass

### 范围与证据

- 当前工作区的 `workspace.md` 已将 `GOAL-001-main-vision` 绑定到 `docs/workspace-001-goal-governance/`；[workspace-protocol.md](../../architecture/workspace-protocol.md) 第 1～2、4 节明确该根是当前 canonical scope，`docs/goals/` 只适用于没有显式工作区根的外部 legacy 仓库。
- 当前消费者没有继续以旧根运行：`web/services/goals_repo.py:45-51` 的默认 scope 为 `workspace-001-goal-governance`，并保留旧参数名仅作 scope 注入；`web/tests/test_goals_repo.py:23-26` 覆盖该默认值。
- 本轮在项目 `.venv` 中复跑：`docs/tests` 10 项、`skills/tests/test_skills_orchestrator.py` 32 项、`web/tests` 21 项、`scripts/tests` 36 项均通过。两个 Windows 符号链接负向用例因缺少创建权限而跳过，未计为通过。
- 因此没有发现 GOAL-002～GOAL-008 的五件套、附件、现行 Web/Skills 读取路径或回归测试因目录迁移而失效；GOAL-011 的迁移事实亦记录在其 [02-execution.md](../GOAL-011-multi-workspace-directory-migration/02-execution.md#2026-07-20--显式工作区迁移资料索引与验证完成)。

### Findings

#### F-001 · recommended / medium · open — 为仍以现时语气出现的旧 canonical 路径补充迁移语境

- `02-execution.md:24` 仍把协议描述为绑定到 `docs/goals/` canonical 范围，但当前协议已在 `workspace-protocol.md:12,30,51` 明确否定该表述在本仓库的现时适用性。
- 相同风险也存在于当前工作区的 [goal-tree.md](../goal-tree.md#2026-07-20--阶段-6-web-工作台规划) 对 `docs/goals/` 的现时描述；已关门 GOAL-004 的 D-002 等条目则是迁移前的历史模型/证据，不应机械改写或据此推定运行时仍依赖旧根。
- 建议由 `/govern` 做最小、可追溯的文档一致性修正：修正现时语气的入口说明，并为仍会被当作现行规范阅读的历史记录加上“GOAL-011 迁移前布局”的语境。保留时间线、附件和历史运行证据中的原始路径，不重开 GOAL-002～GOAL-008，也不把该建议升级为 release 或产品能力结论。

### 必改项与信息门禁

本审计没有发现 open required finding。I-001～I-004 已验证；I-005 仍是已登记的 `non-blocking / open` 下游产品问题，未被目录迁移伪装为已关闭。

### 结论与建议

GOAL-010 的协议交付没有造成其他已关门目标的功能性回归，无需为这些目标进行代码、产物或关门状态的回归修正。只建议处理 F-001 的文档语义一致性；是否及如何写入该响应应由 `/govern` 决定。

### 声明

本独立审计仅追加意见；未修改任何目标的 `status`、`progress`、决策正文或 `goal-tree.md` 状态。
