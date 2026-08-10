---
title: R-004 · 受控变更与可核对操作身份契约（收集稿）
status: active
created: 2026-07-21
updated: 2026-07-21
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.2.0
type: information-collection
review_state: user-reviewed-design-constraints-accepted
---

# R-004 · 受控变更与可核对操作身份契约（收集稿）

> **审视状态**：用户于 2026-07-21 授权起草本收集稿，并在同日按 P-004 明确选择跳过 A-011 的同范围 self 审视、接受 D-007 所列的裁决包。第 2～4 节保留原始收集基线；与第 6 节冲突时，以第 6 节的用户接受设计约束为准。用户接受设计不等于实现、契约测试、运行时事实、I-003/I-004/I-006 已验证、F-007/F-008 关闭或 Web/AI 写入授权。

## 1. 目标与已确认边界

本稿为 I-003、I-004、I-006 收集首个受控变更切片所需的可审视输入。它只覆盖 D-006 已收敛的动作：在一个显式选定的既有工作区内，对一个既有目标形成一项向 `02-execution.md` 追加用户确认执行事实的受限提案。

以下是已有决定的约束，而非本稿新增决定：

- 首个切片只接受用户提供的候选输入，不调用 AI、网络或本地工具。
- 写入前必须有结构化提案、可读 diff、明确确认、门禁检查和可核对结果。
- 首个切片不创建目标、不关闭 finding、不改变状态、不跨工作区导航、不管理共享资料区，也不允许任意 Markdown 编辑。
- 现有 required findings 和信息门禁仍然开放；本稿只收集设计，绝不放行 Web 或 AI 写入。

本稿不选择数据库、实际 HTTP/API 形态或部署方案。D-007 已选择首切片的非 canonical receipt 存放类别、并发约束和本地 trust_context 最小假设；这些仍是待实现和契约测试的设计约束，不是既有运行时能力。

## 2. 候选对象契约

下表中的字段均为待用户审视的候选。字段名服务于后续契约讨论，不代表已经存在的应用状态或存储结构。

### 2.1 `Candidate`

| 候选字段 | 候选用途 |
|----------|----------|
| `candidate_id` | 标识一个候选及其不可变修订。 |
| `workspace_id`、`goal_id` | 绑定唯一工作区和既有目标；不匹配即拒绝。 |
| `source_kind` | 首个切片固定为 `user-provided`，不能伪装为 AI、网络或资料区来源。 |
| `source_statement` | 用户提供的来源说明；缺失时不能形成提案。 |
| `content`、`content_digest` | 待追加执行事实及其摘要，供后续提案和确认核对。 |
| `created_at`、`revision` | 区分候选被编辑前后的版本。 |

候选状态的待审视方案：`draft` -> `submitted` -> `under_review`，其后只能进入 `rejected`、`withdrawn` 或 `proposal_requested`。编辑已提交候选必须产生新修订；旧修订不可继续形成提案。

### 2.2 `Proposal`

| 候选字段 | 候选用途 |
|----------|----------|
| `proposal_id`、`candidate_id`、`candidate_digest` | 把提案绑定到一个精确候选修订。 |
| `workspace_id`、`goal_id` | 重复绑定作用域，防止跨工作区或跨目标使用。 |
| `operation_kind` | 首个切片只能是 `append-execution-fact`。 |
| `target_document`、`expected_write_set` | 只能指向该目标的 `02-execution.md`；出现其他 canonical 文件即无效。 |
| `base_snapshot` | 记录目标文档的 canonical 基线摘要、读取时间及适用工作区/目标。 |
| `unified_diff`、`diff_digest` | 呈现精确变更并提供可核对摘要。 |
| `gate_snapshot` | 记录生成时涉及的 finding、I-00N 与允许/阻断结果。 |
| `expires_at`、`proposal_digest` | 限定有效期，并让确认只能绑定不可变提案摘要。 |

提案状态的待审视方案：`drafting` -> `ready` -> `awaiting_confirmation`。它可因候选变化、基线变化、门禁变化或时间届满进入 `invalidated` 或 `expired`，也可被用户 `cancelled`。只有当前 `ready` 且所有重校验通过的提案可以请求确认。

### 2.3 `Confirmation`

| 候选字段 | 候选用途 |
|----------|----------|
| `confirmation_id`、`proposal_id`、`proposal_digest` | 只确认一个不可变提案摘要，不能以“看过页面”替代。 |
| `workspace_id`、`goal_id`、`base_snapshot_digest` | 再次绑定范围和基线，执行前必须逐项匹配。 |
| `action`、`confirmed_at`、`expires_at` | 明确区分确认、拒绝、取消和到期。 |
| `trust_context` | 留出记录本地单用户运行假设的字段；具体信任模型仍待 I-005 审视。 |
| `confirmation_digest` | 使执行时可核对确认内容未被替换。 |

确认状态的待审视方案：`pending` -> `affirmed`、`rejected`、`revoked`、`expired` 或 `invalidated`。只有 `affirmed` 且提案、基线、门禁和工作区/目标都仍匹配时，才可能请求执行；其余状态必须保持不写入。

### 2.4 `ExecutionReceipt`

| 候选字段 | 候选用途 |
|----------|----------|
| `operation_id`、`proposal_digest`、`confirmation_digest` | 将一次执行、提案和确认关联为同一可核对操作。 |
| `workspace_id`、`goal_id`、`expected_write_set` | 保留执行范围，证明没有扩大写入。 |
| `pre_write_digest`、`post_write_digest` | 记录写入前后文档摘要，供结果核对。 |
| `result`、`failure_code` | 区分成功、冲突、拒绝、失败或恢复中，避免把失败伪装为成功。 |
| `recovery_status`、`recovery_reference` | 关联恢复记录或说明尚无恢复结果。 |
| `audit_reference`、`completed_at` | 关联可审计证据和完成时间；不要求本切片自动关闭任何 finding。 |

结果状态的待审视方案：`started` -> `committed`、`conflict`、`rejected`、`failed` 或 `recovery_pending`；`recovery_pending` 只能进入 `recovered` 或 `failed`。相同 `operation_id` 与完全相同的请求摘要应返回同一不可变结果；同一 ID 绑定不同摘要必须拒绝。

## 3. 候选状态机与 fail-closed 条件

下列顺序是待审视的操作流程，不是实现流程：

1. 用户提交来源明确的 `Candidate`。
2. 系统仅为同一工作区和目标生成范围受限的 `Proposal`，并记录基线、diff 和门禁快照。
3. 用户只对该 `proposal_digest` 作出明确确认、拒绝或取消。
4. 执行前重新读取并核对工作区、目标、候选摘要、提案摘要、基线、门禁和有效期。
5. 所有核对通过后才可创建 `ExecutionReceipt` 并尝试一次受限写入；任何不匹配都结束为不写入的拒绝、失效或冲突结果。
6. 失败或恢复待处理时，后续同工作区受控写入必须停止，直到有可核对的恢复结果。

本稿的候选 fail-closed 规则是：不能证明“确认的提案”与“将要执行的写入”完全一致时，一律不写入；不能确定工作区归属时，一律不显示其他工作区的候选、提案、确认或结果内容。

## 4. 候选负向验证矩阵

| 场景 | 候选预期结果 | canonical 写入 |
|------|--------------|----------------|
| 缺少来源说明、内容摘要或工作区/目标绑定 | 拒绝创建提案并指出缺失字段。 | 不写入 |
| 候选或提案跨工作区、跨目标 | 拒绝且不返回另一工作区内容。 | 不写入 |
| 变更集包含 `02-execution.md` 之外的文件 | 使提案无效。 | 不写入 |
| canonical 基线或候选修订在确认前变化 | 使提案/确认失效，要求重新审视 diff。 | 不写入 |
| 门禁快照过期，或重校验发现受影响 required 门禁仍阻断 | 拒绝执行并展示受影响门禁。 | 不写入 |
| 确认已到期、被撤回、被拒绝或摘要不匹配 | 拒绝执行。 | 不写入 |
| 重放完全相同的 `operation_id` 和请求摘要 | 返回既有不可变 receipt，不重复写入。 | 不重复写入 |
| 用相同 `operation_id` 提交不同摘要 | 拒绝 ID 复用冲突。 | 不写入 |
| 两个请求竞争同一基线或同一工作区写入 | 候选方案是后到请求失败为冲突，不采用最后写入者覆盖。 | 不写入冲突请求 |
| 文件替换中断或恢复记录待处理 | 标为 `recovery_pending`，阻止同工作区后续写入。 | 停止或恢复后再核对 |
| 结果、恢复或审计关联缺失 | 不显示成功；保留失败/待处理状态供人审视。 | 不把结果写成成功 |

这些是后续 API/UX 和恢复测试的候选验收案例，尚未执行，不能作为 F-007、F-008 或 I-003/I-004/I-006 的关闭证据。

## 5. 原始收集稿的待审视取舍

第 2～4 节与本节保留为 2026-07-21 起草时的候选基线。D-007 已对状态机、门禁、写入语义、receipt、并发、trust_context 与内容契约作出裁决；未在第 6 节枚举的低层实现细节仍须在后续实现目标中收集和测试，不得被当作既有能力。

## 6. 用户接受的首切片设计约束（D-007，2026-07-21）

本节是用户确认的设计约束，而非运行时说明。它只覆盖 D-006 已收敛的单一动作：在一个显式选定的既有工作区、既有目标中，向 `02-execution.md` 追加一条用户提供且明确确认的执行事实。

### 6.1 线性对象流与 R-001 对照

1. `CandidateRevision` 是可编辑草稿；提交后固定 `content_digest`，旧修订不得继续形成提案。
2. `Proposal` 绑定一个不可变候选修订及 `proposal_digest`，其持久化状态只可为 `open`、`invalidated`、`expired` 或 `cancelled`。
3. `UserDecision` 是 D-006/R-001 所称 `Confirmation` 的用户决策对象，只能对一个 `proposal_digest` 作出 `affirm`、`reject` 或 `cancel`。`affirm` 在同一受控请求中触发重校验和执行，不另设第二次用户执行动作。
4. `ExecutionReceipt` 记录一次执行的终态；`committed`、`conflict`、`rejected`、`failed` 与 `recovery_pending` 是结果码，不扩展为四套互相重叠的权威状态机。
5. 审视中和等待确认中只可作为界面计算态。R-001 的形成候选、形成受限提案、明确确认与结果分别对应上述 CandidateRevision、Proposal、UserDecision 与 ExecutionReceipt。

### 6.2 三层门禁

| 门禁层 | 规则 | 对本收集稿的含义 |
|--------|------|------------------|
| 产品实现门禁 | F-007、F-008 及 I-003/I-004/I-006 的验证要求未闭环前，不得部署或开放受控写入能力。 | 不进入单次 Proposal 的运行时快照；当前没有运行时能力。 |
| 操作策略门禁 | 必查工作区/目标匹配、来源为 user-provided、写集只含 `02-execution.md`、基线与 must-unchanged 摘要、`proposal_digest`、有效期、recovery 状态和内容契约。 | 任一失败即拒绝、失效或 conflict，且不写入。 |
| 治理推进门禁 | `append-execution-fact` 不得改变 status/progress/parent、关闭 finding、放行阶段或标记 done。 | 目标存在 open required finding 时，未来操作策略门禁通过后仍可如实追加用户确认事实，但 finding 保持 open。 |

### 6.3 追加语义、事务与不变性

- 语义上只在 `02-execution.md` 的时间线追加一节用户确认事实；物理上仍以单文件 transactional replace 落盘，`expected_write_set` 只能是该文件。
- `base_snapshot` 必须 pin `02-execution.md` 的全文摘要；目标 `00-meta.md` 与工作区 `goal-tree.md` 的摘要为 must-unchanged，执行前后任何不等均为 conflict 且不写入。
- 仅可按实现约定机械更新执行记录的 `updated` 字段；禁止修改 `id`、`status`、`progress`、`parent`，禁止把 `goal-tree.md` 放入写集。
- 用户可见 diff 必须呈现可重建的新增文本块和上下文；机器核对使用规范化全文的前后摘要。

### 6.4 Receipt 存放、幂等与恢复

- 选择 B：未来首切片在工作区根的非 canonical `ops/receipts/` 旁路日志保存 Proposal、UserDecision 与 ExecutionReceipt 的可核对关联。该目录本轮未创建，且不得承载目标状态、finding 状态或第二套生命周期。
- receipt 必须绑定 `operation_id`、proposal/decision 摘要、写集、规范化 pre/post digest、结果码和 recovery 引用。相同 `operation_id` 加相同请求摘要返回同一不可变 receipt；同 ID 不同摘要拒绝。
- 首切片不自动清理 receipt。任何未来手工清理或保留策略调整都须由用户另行决定并留痕。
- 缺少权威 receipt，或无法以 canonical pre/post digest 复核结果时，界面不得显示成功，必须 fail closed。

### 6.5 并发、信任与内容契约

- 乐观基线检查与每工作区单写者串行化均为必须：同一基线的双提交必须一成功、一 conflict，禁止 last-write-wins。锁或队列的实现形式留给后续实现目标。
- `trust_context` 的首切片最小假设仅限本机 loopback、单一用户、无多租户；确认来自本机 UI 的显式动作，服务端必须匹配 `proposal_digest`。它不防御本机恶意进程，任何外部暴露前必须重审 I-005，不得静默继承此假设。
- 内容在摘要前统一为 UTF-8、LF 换行，并且只能表达一节含日期、1 至 N 条可核对事实句及可选工作区相对产物路径的时间线条目。拒绝 frontmatter、既有条目修改、路径穿越、HTML/script、status/progress/parent/id 指令、关闭 finding 用语或其他治理推进指令。

### 6.6 负向契约案例

| 场景 | 预期结果 | canonical 写入 |
|------|----------|----------------|
| 产品实现门禁仍开放 | 当前不存在可调用的写入能力。 | 不写入 |
| 目标有 open required finding，但操作策略门禁通过 | 未来仅可追加用户确认事实；不得借此关闭 finding 或推进阶段。 | 仅允许受限追加 |
| 写集包含其他文件、meta/tree 摘要变化或内容不合格 | 提案无效或 conflict。 | 不写入 |
| 确认过期、摘要不匹配、recovery 未决或 receipt 不可核对 | 拒绝、failed 或 recovery_pending。 | 不写入 |
| 同一基线双提交或同 ID 不同摘要重放 | 一成功一 conflict，或拒绝 ID 复用。 | 不重复写入 |
| 外部访问尝试继承本地 trust_context | 拒绝并回流 I-005 审视。 | 不写入 |

## 7. 后续实施与证据要求

D-007 与第 6 节关闭的是 A-011 对 R-004 设计完整性的 F-013～F-019；它们不是实现、试点或契约测试证据。I-003/I-004/I-006 仍为 required / collecting，F-007/F-008 仍为 open / required。只有后续单独立项、完成契约与负向验证、并经审视后，才可能评估受控写入能力；本次不开放 Web 或 AI 写入。
