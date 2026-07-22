---
title: A-011 · R-004 受控变更契约设计合理性独立审计（全文）
status: active
created: 2026-07-21
updated: 2026-07-21
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.1.0
source: independent
verdict: conditional
---

# A-011 · R-004 受控变更契约设计合理性独立审计（全文）

- **source**：independent
- **auditor**：GitHub Copilot · Grok 4.5
- **日期**：2026-07-21
- **类型**：design-plan
- **scope**：审视 [R-004 受控变更与可核对操作身份契约（收集稿）](r-004-controlled-change-contract.md) 是否合理、是否足以支撑 I-003/I-004/I-006 与 F-007/F-008 的后续收集，以及是否存在更好的方案与建议。不审计实现、试点或关门。
- **verdict**：conditional

## 1. 范围与证据

只读材料（当前工作区 `workspace-001-goal-governance`，未跨工作区比较）：

| 证据 | 用途 |
|------|------|
| [workspace.md](../../workspace.md) | Root Goal / canonical 范围 |
| [00-meta.md](../00-meta.md) I-003/I-004/I-006、路线图 C、R-004 入口 | 信息门禁与收集定位 |
| [D-006](../01-decision.md#d-006--收敛首个垂直切片与设计契约2026-07-20) | 首切片与四类对象边界 |
| [R-001](r-001-single-user-workflow-ia-vertical-journey.md) §2–§5 | 用户旅程与对象最小边界 |
| [R-004](r-004-controlled-change-contract.md) | 本审计主对象 |
| [A-002 F-007/F-008](../03-audit.md#a-002--web-工作台产品设想合理性审计2026-07-20)、[A-004 R-004 响应组](../03-audit.md#a-004--对-a-001a-002-的合并响应与开放项管理2026-07-20)、[A-010](../03-audit.md#a-010--r-001-首切片收敛的用户裁决响应2026-07-20) | 既有必改门禁与收敛响应 |
| [web/services/goals_repo.py](../../../../web/services/goals_repo.py) | 现有文件事务/recovery 能力与缺口 |
| [principles.md](../../../architecture/principles.md) P-002～P-005 | 事实、确认、门禁原则 |

本意见**不**把 R-004 候选字段当作用户已接受事实，**不**关闭 F-007/F-008，**不**将 I-003/I-004/I-006 标为 verified。

## 2. 成果（有证据）

1. **方向正确**：四类对象 `Candidate → Proposal → Confirmation → ExecutionReceipt` 与 D-006 §3 及 R-001 表格一致；先契约、后实现，符合 P-001/P-005 与 A-010 的下一步建议。
2. **范围纪律良好**：R-004 明确仅覆盖“用户提供的候选 → 向既有目标 `02-execution.md` 追加”；排除 AI/工具、跨工作区、共享资料、任意 Markdown、自动关闭 finding；并声明不选数据库、HTTP 形态或并发原语——与 D-005/D-006 一致。
3. **fail-closed 原则正确**：确认摘要绑定、基线重校验、跨工作区拒绝、写集越界无效、恢复待处理时停写、失败不伪装成功——直接响应 F-007/F-008 的核心风险。
4. **负向矩阵有价值**：第 4 节把缺字段、跨范围、基线漂移、过期确认、幂等冲突、并发覆盖、recovery 待处理列为“不写入/不重复写入”，适合后续契约测试清单。
5. **事实准入意识正确**：`source_kind=user-provided`、`source_statement` 缺失不能成提案；与 I-008/F-002 方向兼容（首切片不接入 AI 时也可先落地用户来源绑定）。
6. **收集稿元状态诚实**：`review_state: pending-user-review`、禁止把候选当关闭证据；未误报进度或实现。

## 3. 总体判断

R-004 **作为 I-003/I-004/I-006 的首份可审视输入是合理且有用的**，比“直接暴露 `GoalsRepository` 写方法”或“仅有页面按钮无操作身份”更符合本仓库治理协议。

它尚**不足以**作为路线图 C 退出或 F-007/F-008 关闭的充分设计：状态机过细且自洽性不足；门禁语义可能过度阻断“记事实”；持久化与审计侧信道未决；与现有 repository 的整文件事务模型衔接未写清；§5 五项取舍仍待用户裁决。

故 **verdict = conditional**。

## 4. Findings

### F-013 · 四对象状态机过细，且内部迁移描述不完全自洽

- **级别**：recommended；**严重度**：medium
- **关联信息项**：I-003、I-011
- **证据**：
  - Candidate：`draft → submitted → under_review → rejected|withdrawn|proposal_requested`
  - Proposal：`drafting → ready → awaiting_confirmation`，又写“只有当前 `ready` 且重校验通过才能请求确认”
  - Confirmation：`pending → affirmed|…` 后再“请求执行”
  - R-001 旅程只需：形成候选 → 受限提案 → 明确确认 → 结果
- **问题**：
  1. `under_review` 与 Proposal 的“确认前审视”职责重叠，首切片单用户场景缺少独立“审核者”。
  2. Proposal 既要求处于 `ready` 才能确认，又存在 `awaiting_confirmation`，两态边界不清。
  3. Candidate 的 `proposal_requested` 与 Proposal 生命周期的耦合未定义（提案失效后候选是否回退）。
  4. 确认与执行拆成两次用户动作会增加过期/基线漂移窗口，对首切片未必必要。
- **风险**：实现与 UX 成本上升；状态组合爆炸导致契约测试不可完成；用户在详情页无法对应“当前该点哪一步”。
- **建议（更好方案）**：首切片采用**线性管线 + 终态失败码**，而不是四套完整状态机：
  1. `CandidateRevision`（可编辑草稿；提交后产生不可变 `content_digest`）
  2. `Proposal`（由某一候选修订生成；不可变 `proposal_digest`；仅 `open|invalidated|expired|cancelled`）
  3. `UserDecision`（对 `proposal_digest` 的 `affirm|reject|cancel` 一次动作）
  4. 若 `affirm`：同一请求内**重校验后执行**，产出 `ExecutionReceipt`
  - 中间“审核中/等待确认中”可仅作 UI 计算态，不必成为可持久化权威状态。
- **关闭要求（若采纳）**：用户裁决后写入决策/修订 R-004；状态表与 R-001 旅程步骤一一对应；删除或降级与首切片无关的态。

### F-014 · `gate_snapshot` 未区分“产品实现门禁”与“运行时治理门禁”，存在过度阻断记事实的风险

- **级别**：required；**严重度**：high
- **关联信息项**：I-003、I-006、I-004
- **证据**：R-004 §2.2/`gate_snapshot` 与 §4“门禁快照过期或 required 仍阻断 → 拒绝执行”；F-007/F-008、I-003/I-004 本身正是“首个 Web 写入”的阻断项；P-002/P-005 阻断的是阶段放行/关门/关闭 finding，而非禁止记录用户确认的执行事实。
- **问题**：若把“目标上存在任何 open required finding / collecting I-00N”一律解释为禁止 `append-execution-fact`，则：
  - 与“执行记录只写事实”冲突；
  - 与首切片“不关闭 finding、不改 status”的价值相矛盾——用户最需要的正是在门禁仍开放时**如实追加执行事实**；
  - 会把设计期门禁（F-007 未关闭前不得实现写入 API）与运行时门禁混为一谈。
- **更好方案**：把门禁拆成三层，并在 `gate_snapshot` 中显式字段化：
  1. **实现前产品门禁**（设计/立项层）：I-003/I-004/I-006、F-007/F-008 未关闭前不得部署写入 API——不进入每次 Proposal 运行时快照。
  2. **操作策略门禁**（运行时必查）：workspace/goal 匹配、write set 仅 `02-execution.md`、基线、确认摘要、有效期、recovery 未决、内容格式合法。
  3. **治理推进门禁**（本操作不适用则不得误用）：状态改为 `done`、关闭 finding、放行阶段等；`append-execution-fact` 的默认策略应是**允许记事实，禁止借写入推进或关门**。
- **关闭要求**：R-004（或后续 D-00N）写明 `append-execution-fact` 的 gate 允许/拒绝表；至少一条负向案例：“目标存在 open required finding 时，追加用户确认执行事实仍应允许（若操作策略门禁通过），且不得关闭该 finding”。

### F-015 · 与现有整文件事务模型及 `goal-tree` 不变性的衔接仍不充分

- **级别**：required；**严重度**：high
- **关联信息项**：I-004、I-006
- **证据**：
  - R-004 要求 `expected_write_set` 只能含 `02-execution.md`，`unified_diff` 呈现精确变更；
  - `GoalsRepository.update_goal` / `_transactional_write` 以**整文件替换**多路径集合，并在 meta/status/parent 变化时同步 `goal-tree.md`；
  - §5.2 仍把“是否绑定 goal-tree 不变性声明”列为未决。
- **问题**：
  1. “语义追加”与“物理整文件写”未声明；实现者可能误做真正 OS 级 append 或误改 frontmatter `status/updated` 策略。
  2. 若不 pin `goal-tree.md`（及 `00-meta` 的 status/progress）的只读摘要，用户确认的 diff 可能与“顺带同步树”的实现分叉，破坏 F-008 的“确认的 diff = 最终写入”。
  3. 缺少“追加位置/格式”契约：时间线条目形态、是否禁止改 frontmatter 业务字段、`updated` 日期是否允许随写更新。
- **更好方案**（首切片建议默认，待用户裁决）：
  1. **语义**：仅向 `02-execution.md` 正文时间线追加一节用户确认事实；frontmatter 仅允许实现定义的机械字段（如 `updated`），**禁止**改 `status/progress/parent/id`。
  2. **物理**：仍用现有 transactional replace 写单文件；`expected_write_set = {02-execution.md}`。
  3. **不变性 pin**：`base_snapshot` 至少含 `02-execution` 全文 digest；另含 `goal-tree.md` 与目标 `00-meta` 的 digest 作为 **must-unchanged** 声明——执行前后必须相等，否则 `conflict`。
  4. **diff**：对用户展示“将追加的文本块 + 上下文”，对机器校验使用全文前后 digest；避免只存无法重建的模糊 diff。
- **关闭要求**：用户确认上述默认或替代方案后写入 R-004/决策；负向矩阵增加“误含 goal-tree 或改 status 的提案无效”“meta/tree 在确认后被外部修改 → conflict/不写入”。

### F-016 · 无数据库前提下，操作对象与 receipt 的权威存放未形成最小选项

- **级别**：required；**严重度**：high
- **关联信息项**：I-004、I-005、I-006
- **证据**：D-005 暂缓数据库；R-004 声明不选持久化实现，但 F-007/F-008 要求 operation id 幂等、过期、重放、恢复后可核对；`ExecutionReceipt.audit_reference` / `recovery_reference` 未说明落点。
- **问题**：若 Candidate/Proposal/Confirmation/Receipt 仅存活在浏览器内存，则：
  - 无法在恢复后证明“确认过的 digest”；
  - 幂等重放无权威 store；
  - 易把 receipt 误写入 canonical 五件套，形成第二状态源。
- **更好方案**：先让用户在**有界选项**中选一，而不是无限延后：
  | 选项 | 含义 | 适用 |
  |------|------|------|
  | A. 进程内 + 显式导出 | 单次本地会话；receipt 可下载/展示；重启即失 | 极早期 UX 演练，**不能**关闭 F-008 |
  | B. 工作区旁路 ops 日志（推荐首切片） | 如工作区根下非 canonical 目录（名称待定）仅存 ops/receipt；**禁止**当 goal 状态；写入仍只动 `02-execution.md` | 本地单用户、无 DB |
  | C. 延后 DB/外部 store | 明确非当前 | D-005 复核触发后再议 |
- **硬约束**：无论 A/B/C，canonical 真相仍只有五件套 + `goal-tree.md`；ops 日志缺失时 fail-closed（不显示“已成功写入” unless pre/post digest 可从 canonical 复核）。
- **关闭要求**：用户选定存放策略与保留期限；R-004 写清“权威结果如何被用户与恢复路径再次核对”。

### F-017 · 并发模型只否定 last-write-wins，未给出首切片可测默认

- **级别**：recommended；**严重度**：medium
- **关联信息项**：I-004、I-006
- **证据**：§3/§4 要求后到冲突失败；§5.4 在串行化 / 乐观基线 / 组合之间未决；现有 repo 无 workspace lock。
- **建议默认（待裁决）**：**乐观基线检查为必须**（已有 base_snapshot）；同工作区再加**合作式单写者锁或写入队列**为 should——单用户本地也可防双标签页。首切片验收至少：同基线双提交 → 一成功一 `conflict`；不要求分布式锁。
- **关闭要求**：选定默认并写入负向案例的通过标准。

### F-018 · `trust_context` 与本地单用户信任假设仍是空壳，F-007 未实质推进

- **级别**：recommended；**严重度**：medium
- **关联信息项**：I-003、I-005
- **证据**：Confirmation 仅“留出字段”；I-005 仍 collecting；A-002 F-007 要求本地/受控外部分别写清信任假设。
- **建议最小本地假设（候选，非接受）**：
  - 运行于本机 loopback 开发服务；无多租户；
  - 确认动作 = 本机 UI 显式按钮 + 服务端持有的 `proposal_digest` 匹配；
  - 不防本机恶意进程；外部暴露前必须重审 I-005。
- **关闭要求**：用户接受或修改最小 `trust_context` 枚举；外部访问不得静默继承。

### F-019 · 执行事实“内容契约”缺失，diff 无法单独保证语义正确

- **级别**：recommended；**严重度**：medium
- **关联信息项**：I-003、I-008
- **证据**：R-004 有 `content`/`content_digest`，无长度、结构、禁止路径穿越、禁止夹带 frontmatter、禁止 HTML/脚本、时间戳格式等；I-008 仍 collecting。
- **风险**：用户确认了 digests，但仍可能追加破坏文档结构的内容，或把未结构化散文写成无法审计的“事实”。
- **建议**：首切片规定最小内容模板，例如：
  - 必含：日期、1–N 条可核对事实句、可选产物路径；
  - 禁止：修改既有时间线条目、闭合 finding 用语、改 status 指令；
  - 服务端规范化后再算 digest（统一换行），避免跨平台 diff 噪声。
- **关闭要求**：内容模板与规范化规则写入 R-004 或 I-008 交叉引用。

## 5. 必改项汇总

| Finding | 级别 | 与 F-007/F-008 关系 | 阻断 |
|---------|------|---------------------|------|
| F-014 | required | 直接影响运行时确认/拒绝语义是否正确 | 路线图 C 退出前须澄清；否则写入 API 验收标准错误 |
| F-015 | required | 直接影响“确认的 diff = 最终写入” | 路线图 C 退出、首个 Web 写入契约 |
| F-016 | required | 直接影响幂等、恢复后可核对 | 路线图 C 退出、F-008 关闭证据 |
| F-013 | recommended | 影响可实现性与 UX | 不单独阻断，但强烈建议在用户审视 R-004 时一并裁决 |
| F-017 | recommended | 并发可测默认 | 建议与 F-015 同批裁决 |
| F-018 | recommended | F-007 信任边界 | 可与 I-005 并行，但 C 退出前至少要有本地最小假设 |
| F-019 | recommended | 内容可审计性 | 建议首切片最小模板 |

既有 **F-007、F-008 保持 open**：R-004 是收集稿，不是关闭证据。

## 6. 对照成功标准 / 信息项

| 项 | 判断 |
|----|------|
| I-003 确认状态机 | 有候选，未自洽、未用户接受、无契约测试 |
| I-004 变更包/事务/幂等 | 有对象与负向场景骨架；缺持久化、tree pin、与 repo 衔接 |
| I-006 fail-closed | 原则正确；门禁分层与恢复权威 store 不足 |
| F-007 | 部分覆盖（digest 绑定）；trust 与确认-执行窗口仍弱 |
| F-008 | 部分覆盖（operation_id、conflict、recovery_pending）；权威 receipt 与 tree 不变性不足 |
| D-006 范围 | 遵守，未拖宽 |
| 放行写入 | **不得**；本稿与本审计均不授权 |

## 7. 与既有意见的异同

- 与 A-002 **同向**：受控写入必要且高风险；文件 recovery ≠ 操作原子性。
- 与 A-004 R-004 组 **同向**：正是该响应组要求的字段/状态机/负向验证收集。
- 与 A-010 **同向**：四类对象已命名，本意见审计其首份设计质量。
- **新增**：不重复编号 F-007/F-008；新增 F-013～F-019 专门针对 R-004 设计缺口与可选简化方案。
- **无冲突**：不要求否决四对象模型，只要求收敛状态机、门禁分层与落盘策略。

## 8. 建议的更优默认方案（供用户 /govern 裁决，非已接受）

```text
用户编辑 CandidateRevision
    → 生成不可变 Proposal{write_set={02-execution.md}, base digests, append payload, proposal_digest}
    → 用户一次动作：拒绝 | 取消 | 确认并执行(proposal_digest)
    → 服务端重读：workspace/goal/base/must-unchanged(tree+meta)/recovery/expiry
    → 通过则 transactional replace 单文件 + 旁路 ops Receipt(operation_id 幂等)
    → 失败则 conflict|rejected|failed|recovery_pending，canonical 无部分成功表象
```

门禁：操作策略门禁必查；治理推进门禁不适用于纯追加事实；产品实现门禁留在立项/发布前。

## 9. 结论与给编排器的下一步

R-004 是**合格的收集起点**，方向合理，但作为“可冻结契约”尚不充分 → **conditional**。

建议 `/govern`：

1. 按 P-004 询问是否需要同范围 self 审视（已有 independent，尚无专门针对 R-004 的 self）。
2. 请用户逐项裁决：状态机简化（F-013）、门禁三层（F-014）、tree/meta pin 与追加语义（F-015）、ops 存放选项 A/B/C（F-016）、并发默认（F-017）、本地 trust 最小集（F-018）、内容模板（F-019）。
3. 将接受项写入 D-007（或修订 R-004 + 决策），再评估 I-003/I-004/I-006 是否仍为 collecting。
4. **在契约测试与用户接受前**，不得关闭 F-007/F-008，不得立项无边界的 Web 写入实现。

## 10. 声明

本意见只追加审计台账与本附件；不修改 GOAL-009 的 `status`、`progress`、方案正文或 `goal-tree.md`。finding 响应与阶段推进归 `/govern` 与用户。
