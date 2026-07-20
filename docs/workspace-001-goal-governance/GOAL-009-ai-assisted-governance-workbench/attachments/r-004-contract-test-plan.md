---
title: R-004 · 负向契约测试计划与实现前门禁清单（收集稿）
status: active
created: 2026-07-21
updated: 2026-07-21
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.3.0
type: information-collection
review_state: govern-approved-collection-plan
specification_state: govern-accepted-with-minor-revisions
accepted_by: D-010
---

# R-004 · 负向契约测试计划与实现前门禁清单

> 本文档是 D-008 记录的测试范围收集稿。所有 CT-001～CT-018 都是待实现、待执行、待审视的计划案例，不是测试通过事实，不关闭 F-007/F-008，也不把 I-003/I-004/I-006 标为 `verified`。CT-016～CT-018 按 D-007 的已接受边界补入；其接口和错误码细节仍以待用户审视的规格包为候选，不是运行时事实。

## 1. 范围与非目标

本计划把 [R-004 受控变更契约](r-004-controlled-change-contract.md) 第 6 节及 D-007 的用户接受约束转成可执行的负向契约测试范围，服务于首个受限动作：在一个显式选定的既有工作区和既有目标中，向 `02-execution.md` 追加一条用户确认的执行事实。

本计划不实现或验证 Web 路由、AI 服务、数据库、共享资料区、跨工作区导航、生产部署、`ops/receipts/` 运行时目录或任何 canonical 写入。测试计划中的“拒绝”“冲突”“不写入”和“不可显示成功”均为预期断言，尚未发生。

## 2. 实现前门禁清单

以下条件是进入单独实现目标、开放受控写入或声明验收证据前的必要检查；本次全部保持未完成：

- [ ] `I-003` 已有单用户 CandidateRevision、Proposal、UserDecision、Receipt 的 API/UX 契约和正反测试证据，并达到 `verified`。
- [ ] `I-004` 已有 canonical 基线、写集、事务/恢复、operation id、幂等、并发和审计关联的负向测试证据，并达到 `verified`。
- [ ] `I-006` 已有 fail-closed 负向矩阵、故障升级和恢复后重核对证据，并达到 `verified`。
- [ ] `F-007` 的确认绑定、基线绑定和信任边界测试完成并由后续审视关闭。
- [ ] `F-008` 的原子性、恢复、幂等、并发和审计证据测试完成并由后续审视关闭。
- [ ] 每个测试有隔离的 workspace/goal fixture、可核对的 pre/post digest、operation id 和 receipt 结果。
- [ ] 测试运行环境、版本、命令、退出码和机器可读结果已记录；本计划不代替这些运行证据。
- [ ] 任何实现前用户确认只批准测试范围，不等于批准 Web/AI 写入、残余风险或目标关门。

## 3. 负向契约矩阵

| ID | 触发条件 | 预期行为 | canonical 写入 | 关联门禁 |
|----|----------|----------|----------------|----------|
| CT-001 | Candidate 缺少 `source_statement`、`content_digest` 或 workspace/goal 绑定 | 拒绝 Candidate/Proposal，指出缺失字段 | 不写入 | I-003/I-004/I-006、F-007 |
| CT-002 | `source_kind` 不是 `user-provided`，或将 AI、网络、资料区内容伪装为用户来源 | 拒绝并保留候选为非 canonical 输入 | 不写入 | I-003/I-006、F-007 |
| CT-003 | Candidate、Proposal 或 UserDecision 跨 workspace/goal，或请求试图暴露另一工作区内容 | 拒绝且不返回另一工作区内容 | 不写入 | I-003/I-006、F-007/F-008 |
| CT-004 | `operation_kind` 不是 `append-execution-fact`，或 `expected_write_set` 含 `02-execution.md` 之外的文件 | Proposal 无效并拒绝执行 | 不写入 | I-004/I-006、F-007/F-008 |
| CT-005 | CandidateRevision、canonical baseline 或 meta/tree must-unchanged digest 在确认前变化 | Proposal/UserDecision 失效，要求重新审视 diff | 不写入 | I-004/I-006、F-007/F-008 |
| CT-006 | UserDecision 已过期、撤回、拒绝、取消，或 proposal/confirmation digest 不匹配 | 拒绝执行 | 不写入 | I-003/I-004/I-006、F-007/F-008 |
| CT-007 | 相同 `operation_id` 与完全相同的请求摘要被重放 | 返回同一不可变 receipt，禁止重复执行 | 不重复写入 | I-004/I-006、F-008 |
| CT-008 | 相同 `operation_id` 绑定不同 proposal/decision/request 摘要 | 拒绝 ID 复用冲突 | 不写入 | I-004/I-006、F-008 |
| CT-009 | 两个请求竞争同一 baseline/workspace | 后到请求为 conflict，禁止 last-write-wins 覆盖 | 冲突请求不写入 | I-004/I-006、F-008 |
| CT-010 | transactional replace 中断，或 recovery 状态未决 | 标为 `recovery_pending`，阻止同 workspace 后续受控写入 | 停止写入，恢复后重核对 | I-004/I-006、F-008 |
| CT-011 | result、recovery 或 audit linkage 缺失，或 receipt/pre/post digest 无法复核 | 不显示成功，保留 failed/pending 状态 | 不把结果写成成功 | I-004/I-006、F-008 |
| CT-012 | 内容违反执行事实契约：frontmatter、既有条目修改、路径穿越、HTML/script、非法治理指令等 | Proposal 无效或拒绝 | 不写入 | I-004/I-006、F-007/F-008 |
| CT-013 | 产品实现门禁仍开放：F-007/F-008 或 I-003/I-004/I-006 尚未闭环 | 不暴露可调用的受控写入能力；运行时不得被误当作已放行 | 不写入 | I-003/I-004/I-006、F-007/F-008 |
| CT-014 | 追加 payload 试图修改 status/progress/parent/id、meta/tree、finding、阶段或 `done` | 拒绝或 conflict，写集不得扩大 | 不写入 | I-004/I-006、F-007/F-008 |
| CT-015 | 外部访问试图继承本机 loopback 单用户 `trust_context` | 拒绝并回流 I-005 复核 | 不写入 | I-006、F-007 |
| CT-016 | 在已实现且单独授权的测试环境中，fixture 保留一个与该操作无关的 open required finding；操作策略门禁全部通过 | 允许受限追加；finding、status/progress/parent 与 meta/tree 保持不变 | 仅 `02-execution.md` 变化 | I-003/I-004/I-006、F-007/F-008 |
| CT-017 | 输入执行事实使用 CRLF 或混合换行；调用方提供的摘要不是 UTF-8/LF 规范化后的摘要 | 先按规范化内容重算摘要；不匹配时返回内容摘要冲突并拒绝，匹配时才能继续后续门禁 | 摘要不匹配时不写入 | I-004/I-006、F-007/F-008 |
| CT-018 | 调用方试图把 UserDecision.affirm 与执行拆为无重校验的两步，或直接调用第二个执行入口 | 拒绝独立第二步执行；affirm 必须在同一受控请求内重校验并产生终态 receipt | 不写入 | I-003/I-004/I-006、F-007/F-008 |

## 4. 证据记录格式

每个后续实现测试至少记录：

1. 测试 ID、目标 fixture、workspace/goal 范围和运行时版本。
2. 输入中的 candidate/proposal/decision/operation 摘要及预期写集。
3. 触发的门禁、拒绝/冲突/fail-closed 结果和机器可读错误码。
4. canonical 目标文件、meta、goal-tree 的 pre/post digest；若没有写入，应证明摘要不变。
5. receipt、recovery、audit linkage 的可核对路径和命令退出码。
6. 所用 fixture ID、契约规格包版本和预期 result/error code；候选接口或错误码尚未获用户审视时，结果只能记为规格待确认。

缺少上述任一项只能记为证据缺口，不得将该案例标为通过或据此关闭 finding。

## 5. 当前结论与后续

- 本计划是 R-004 的可审视收集输入，覆盖 I-003/I-004/I-006 的负向验证范围；未执行任何测试。
- F-007/F-008 仍为 `open / required`；I-003/I-004/I-006 仍为 `required / collecting`。
- 已新增 CT-016～CT-018，以覆盖 open finding 下的受限事实追加、UTF-8/LF 规范化摘要，以及 affirm 与执行同请求三个 D-007 边界。它们仍未执行。D-009/A-016 将本增补记为 A-014 F-020 的计划覆盖关闭证据（非测试通过）。
- 配套规格见 [r-004-executable-contract-spec.md](r-004-executable-contract-spec.md)（F-023；D-010 **接受含小修订**）。
- **2026-07-21 审视**：CT-016～CT-018 与规格包一并接受为实现前测试范围基线；幂等 CT-007 的规范断言为“返回既有 receipt + 不重复写入”，不以错误码表示成功重放。
- 下一步：并行推进 R-001/R-002/R-003 证据；**F-005 关闭前**不另立实现目标；**F-007/F-008 关闭且 I-003/I-004/I-006 `verified` 前**不得开放 Web/AI 写入。
