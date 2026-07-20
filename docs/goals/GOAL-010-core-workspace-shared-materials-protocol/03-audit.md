---
id: GOAL-010-core-workspace-shared-materials-protocol
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-20
version: 0.2.0
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
