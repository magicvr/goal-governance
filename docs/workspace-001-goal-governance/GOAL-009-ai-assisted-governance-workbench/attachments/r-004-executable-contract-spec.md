---
title: R-004 · 最小可执行契约规格包（收集稿）
status: active
created: 2026-07-21
updated: 2026-07-21
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.1.0
type: information-collection
review_state: pending-user-review
specification_of: r-004-contract-test-plan.md
---

# R-004 · 最小可执行契约规格包（收集稿）

> 本规格包响应 A-014 **F-023**：把 CT-001～CT-018 下沉为可审视的 fixture、service-level 操作入口、错误/结果码、receipt 字段与 digest 算法说明。  
> **非实现、非测试通过、非 Web/AI 写入授权**。用户审视通过 ≠ I-003/I-004/I-006 `verified` ≠ F-007/F-008 关闭。  
> 权威设计约束仍以 [R-004 §6](r-004-controlled-change-contract.md#6-用户接受的首切片设计约束d-0072026-07-21) 与 [D-007](../01-decision.md#d-007--接受-r-004a-011-的首切片设计裁决包2026-07-21) 为准。

## 1. 范围与非目标

| 在范围内 | 不在范围内 |
|----------|------------|
| 首切片动作 `append-execution-fact` | HTTP 路由、页面组件、AI 调用 |
| 单工作区 / 单目标 fixture 布局 | 多工作区导航、共享资料 CRUD |
| service-level 操作入口（函数/命令契约） | 开放生产写入或部署 |
| 错误码 / 结果码表 | 运行时已生成的 receipt 文件 |
| receipt JSON 字段示例与 digest 算法 | 将规格包当作已通过测试 |

工作区上下文：`workspace-001-goal-governance`；canonical 根为 `docs/workspace-001-goal-governance/`。首切片只允许写该工作区内目标的 `02-execution.md`。

## 2. Fixture 布局（候选约定）

实现目标立项后，测试 fixture 建议放在实现仓库约定路径（例如 `web/tests/fixtures/r004/`）；本 GOAL-009 附件不创建运行时目录。

```text
fixtures/r004/
├── README.md                      # fixture 索引与禁止项
├── workspace-ok/                  # 合法单工作区骨架
│   ├── workspace.md
│   ├── goal-tree.md
│   └── GOAL-999-fixture-target/
│       ├── 00-meta.md
│       ├── 01-decision.md
│       ├── 02-execution.md        # 仅允许被追加的目标文件
│       ├── 03-audit.md            # 可含 open required finding（CT-016）
│       └── attachments/
├── workspace-cross/               # 第二工作区（仅负向：禁止读写）
│   └── ...
└── cases/
    ├── CT-001-missing-fields.json
    ├── CT-016-open-finding-append.json
    ├── CT-017-crlf-digest.json
    └── CT-018-split-affirm-execute.json
```

### Fixture 规则

1. `workspace_id` 必须与 `workspace.md` 的 `id` 一致；`goal_id` 必须存在且 `parent` 合法。
2. 每个案例 JSON 至少含：`case_id`、`operation_id`、输入对象摘要、预期 `result` 或 `error_code`、预期 canonical 写入效果、关联 CT-ID。
3. open-finding fixture（CT-016）在 `03-audit` 保留与本次追加无关的 required finding；操作成功后 finding 仍 open，`00-meta`/`goal-tree` digest 不变。
4. 禁止 fixture 预置 `ops/receipts/` 成功记录伪装为历史运行证据。

## 3. Service-level 操作入口（候选）

首切片不定义公开 HTTP API。候选 service 边界（名称可调整，语义不得削弱）：

| 入口 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `prepare_candidate_revision` | workspace/goal、user content、source_statement | `CandidateRevision` 或错误 | 草稿可编辑；提交后固定 content digest |
| `build_proposal` | candidate_revision_id / digest | `Proposal` 或错误 | 计算 write_set、diff、baseline、gate_snapshot |
| `decide_and_execute` | proposal_digest + `UserDecision.action` + trust_context | `ExecutionReceipt` | **唯一**可写入口；`affirm` 与执行同请求重校验 |
| `get_receipt` | operation_id | receipt 或 not_found | 只读；不触发写入 |
| `get_recovery_state` | workspace_id | recovery 状态 | recovery_pending 时阻断同工作区后续写入 |

### 硬约束

1. **禁止**独立的 `execute_proposal` / `commit` 第二步写入口（CT-018）。
2. **禁止**在 F-007/F-008 或 I-003/I-004/I-006 未闭环时暴露 `decide_and_execute` 为生产能力（CT-013）。
3. 所有入口必须携带 `workspace_id` + `goal_id`；跨范围请求 fail closed 且不得泄漏另一工作区内容（CT-003）。

## 4. 结果码与错误码（候选枚举）

### 4.1 `ExecutionReceipt.result`

| 码 | 含义 | canonical 写入 |
|----|------|----------------|
| `committed` | 单文件追加成功，pre/post digest 可核对 | 仅 `02-execution.md` |
| `conflict` | 基线/must-unchanged/并发冲突 | 不写入 |
| `rejected` | 门禁、内容、信任或决策拒绝 | 不写入 |
| `failed` | 非冲突技术失败 | 不写入或需 recovery |
| `recovery_pending` | 事务中断或恢复未决 | 停止后续同 workspace 写入 |

### 4.2 `error_code`（拒绝/失败时）

| 码 | 触发（对应 CT） | 说明 |
|----|-----------------|------|
| `ERR_MISSING_FIELD` | CT-001 | 缺 source_statement / content_digest / 绑定 |
| `ERR_INVALID_SOURCE` | CT-002 | source_kind ≠ user-provided |
| `ERR_SCOPE_MISMATCH` | CT-003 | 跨 workspace/goal 或试图暴露他区 |
| `ERR_INVALID_WRITE_SET` | CT-004、CT-014 | 非 append-execution-fact 或写集扩大 |
| `ERR_BASELINE_DRIFT` | CT-005 | 确认前 baseline / meta / tree digest 变化 |
| `ERR_DECISION_INVALID` | CT-006 | 过期、撤回、拒绝、digest 不匹配 |
| `ERR_IDEM_REPLAY` | CT-007 | 同 operation_id + 同请求摘要 → 返回原 receipt（非错误也可作 `result=committed` 幂等） |
| `ERR_IDEM_CONFLICT` | CT-008 | 同 operation_id + 不同摘要 |
| `ERR_CONCURRENT_WRITE` | CT-009 | 同 baseline 竞争 |
| `ERR_RECOVERY_PENDING` | CT-010 | 恢复未决 |
| `ERR_RECEIPT_UNVERIFIABLE` | CT-011 | receipt / digest 不可复核，不得显示成功 |
| `ERR_CONTENT_CONTRACT` | CT-012、CT-017 | 内容/规范化/治理指令违规 |
| `ERR_PRODUCT_GATE_OPEN` | CT-013 | 产品实现门禁未闭环 |
| `ERR_GOVERNANCE_MUTATION` | CT-014 | 试图改 status/progress/finding/阶段 |
| `ERR_TRUST_CONTEXT` | CT-015 | 外部访问继承 loopback 假设 |
| `ERR_DIGEST_MISMATCH` | CT-017 | 调用方摘要 ≠ UTF-8/LF 规范化后摘要 |
| `ERR_SPLIT_EXECUTE` | CT-018 | 拆分 affirm 与无重校验执行 |

`ERR_IDEM_REPLAY` 在实现中可表现为“成功返回既有 receipt”而非 HTTP 4xx；契约要求是**不重复写入**。

## 5. Digest 算法说明（候选）

1. **文本规范化（必须先于摘要）**  
   - 解码为 Unicode 文本；  
   - 统一换行为 `LF`（`\n`）；去掉尾随 `CR`；  
   - 以 UTF-8 无 BOM 编码后再哈希。
2. **算法**：候选默认 `sha256` 十六进制小写；实现目标可固定为 `sha256:<hex>` 前缀形式，但同一系统内必须一致。
3. **对象摘要**  
   - `content_digest`：规范化后的候选执行事实正文。  
   - `proposal_digest`：规范化后的不可变提案有效载荷（含 write_set、baseline、diff、gate_snapshot 引用）。  
   - `decision_digest` / `confirmation_digest`：规范化后的 UserDecision 有效载荷（action + proposal_digest + trust_context 声明）。  
   - `pre_write_digest` / `post_write_digest`：目标 `02-execution.md` 全文规范化后摘要。  
   - `meta_digest` / `tree_digest`：must-unchanged 的 `00-meta.md` 与工作区 `goal-tree.md` 全文规范化摘要。
4. **CT-017**：若调用方提交的 digest 不是规范化后重算值，返回 `ERR_DIGEST_MISMATCH`，不写入。

## 6. Receipt 字段示例（候选 JSON）

```json
{
  "schema": "r004-execution-receipt/v0",
  "operation_id": "op_fixture_0001",
  "workspace_id": "workspace-001-goal-governance",
  "goal_id": "GOAL-999-fixture-target",
  "operation_kind": "append-execution-fact",
  "expected_write_set": ["02-execution.md"],
  "proposal_digest": "sha256:…",
  "decision_digest": "sha256:…",
  "request_digest": "sha256:…",
  "pre_write_digest": "sha256:…",
  "post_write_digest": "sha256:…",
  "meta_digest_unchanged": "sha256:…",
  "tree_digest_unchanged": "sha256:…",
  "result": "committed",
  "error_code": null,
  "recovery_ref": null,
  "trust_context": {
    "mode": "local-loopback-single-user",
    "external_access": false
  },
  "created_at": "2026-07-21T00:00:00Z"
}
```

未来落盘位置（**尚未创建**）：工作区根非 canonical `ops/receipts/<operation_id>.json`（D-007 / R-004 §6.4）。receipt 不可复核时不得向用户显示成功。

### 可选 Markdown 人类摘要（非权威）

```markdown
# Receipt op_fixture_0001
- result: committed
- goal: GOAL-999-fixture-target
- write_set: 02-execution.md only
- proposal_digest / pre / post: （与 JSON 一致）
```

人类摘要若与 JSON 冲突，以 JSON receipt + canonical digest 为准。

## 7. CT 与规格映射

| CT | 本规格关键点 |
|----|--------------|
| CT-001～CT-015 | 错误码表 §4.2；入口 §3 |
| CT-016 | fixture open finding；committed 且 finding/status 不变 |
| CT-017 | §5 规范化 + `ERR_DIGEST_MISMATCH` |
| CT-018 | 仅 `decide_and_execute`；`ERR_SPLIT_EXECUTE` |

完整场景表见 [r-004-contract-test-plan.md](r-004-contract-test-plan.md)。

## 8. 实现前门禁（再次声明）

- [ ] 用户审视并接受本规格包（或书面修订后接受）
- [ ] I-003/I-004/I-006 有正反测试证据并 `verified`
- [ ] F-007/F-008 由后续审视关闭
- [ ] F-005 关闭前不立项实现子目标；F-007/F-008 关闭前不开放 Web/AI 写入
- [ ] 未创建生产 `ops/receipts/` 或把本附件当作运行证据

## 9. 当前结论

本附件是 **待用户审视** 的最小可执行契约规格收集稿，用于关闭 A-014 F-023 的“形成规格包”要求。它不执行 CT、不修改 `web/`、不放行写入、不关闭 F-007/F-008。
