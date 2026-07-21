---
id: GOAL-013-write-gate-ct-durable-idempotency
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.7.0
---

# 执行记录 · GOAL-013

## 时间线

### 2026-07-21 · 立项

- 用户确认按 GOAL-009 A-020 立项本目标；生产门禁默认仍关。
- 创建五件套于 `docs/workspace-001-goal-governance/GOAL-013-write-gate-ct-durable-idempotency/`；D-001 冻结范围。
- **尚未**改 `web/` 代码；**尚未**新增 CT 用例。

### 2026-07-21 · 阶段 B · 跨进程幂等 / receipt 恢复

- 用户 `/govern 推进 GOAL-013 阶段 B`。
- [D-002](01-decision.md#d-002--阶段-b--持久化-receipt-与跨实例幂等语义2026-07-21)：持久化布局与幂等语义。
- 实现（`web/services/controlled_change.py`）：
  - `_lookup_prior_receipt`：内存 → `ops/receipts/{operation_id}.json`
  - `decide_and_execute` 写前查找 prior；同 `proposal_digest` 直接返回；不同 → `ERR_OPERATION_ID_CONFLICT`
  - `_persist_receipt` 改为原子写（与 canonical 追加同一 `_atomic_write_text`）
  - `get_receipt` 走磁盘回填
- 测试（`web/tests/test_controlled_change.py`）：
  - `test_durable_idempotent_replay_new_service_instance`（CT-007 跨实例）
  - `test_operation_id_conflict_different_proposal`（CT-008 部分）
- 文档：`web/README.md` 更新幂等语义（去掉「仅进程内 residual」表述）。
- 验证：`python -m unittest tests.test_controlled_change -v` → **14 OK**；`discover -s tests` → **46 passed, 1 skipped**。
- **未**开放生产写入；**未**关闭 GOAL-009 F-007/F-008。

### 2026-07-21 · 台账回写（GOAL-012 residual / GOAL-009 A-020）

- 用户 `/govern` 回写：GOAL-012 A-004 关闭 F-003 residual；GOAL-009 A-021 更新 CT-007 为覆盖。
- 本目标不改 status；实现证据被规划台账吸收。

### 2026-07-21 · 阶段 C · F-007 向 CT（001/003/006/012/014/015）

- 用户 `/govern 推进 GOAL-013 阶段 C`。
- [D-003](01-decision.md#d-003--阶段-c--f-007-向-ct-补全语义2026-07-21)。
- 实现：`workspace` 绑定校验、proposal 过期、trust 上下文、扩展内容契约。
- 测试：`test_ct001_*`、`test_ct003_*`、`test_ct006_*`、`test_ct012_*`、`test_ct014_*`、`test_ct015_*`。
- 验证：`tests.test_controlled_change` **25 OK**；全量 web unittest **57 passed, 1 skipped**。
- **未**开放生产写入；**未**关闭 GOAL-009 F-007/F-008。

### 2026-07-21 · 台账回写（GOAL-009 A-022 阶段 C）

- 用户 `/govern` 将 CT-001/003/006/012/014/015 覆盖回写 GOAL-009 A-022。
- 本目标不改 status；F-007 正式关闭仍归 GOAL-009 审视。

### 2026-07-21 · 阶段 D · F-008 向 CT 补全

- 用户 `/govern 推进 GOAL-013 阶段 D（F-008：009/010/011 + CT-008 补全）`；依据 [D-004](01-decision.md#d-004--阶段-d--f-008-向-ct-补全2026-07-21) 执行。
- 实现 `web/services/controlled_change.py`：
  - CT-008：在 durable receipt 检查前计算完整 `request_digest`；同 operation_id 的不同 action/request 返回 `ERR_IDEM_CONFLICT` / `conflict`，已提交 receipt 不被后续拒绝结果覆盖。
  - CT-009：增加按 workspace 复用的进程内非阻塞锁；竞争写入返回 `ERR_CONCURRENT_WRITE` / `conflict`。
  - CT-010：recovery record 为 pending 时返回 `ERR_RECOVERY_PENDING` / `recovery_pending`，不写 `02-execution.md`。
  - CT-011：加载 committed receipt 时检查 request/pre/post digest；不可复核 receipt 降级为 `ERR_RECEIPT_UNVERIFIABLE` / `failed`。
- 新增/更新 `web/tests/test_controlled_change.py`：
  - `test_ct008_same_op_id_different_action_conflicts`
  - `test_ct009_concurrent_write_conflict`
  - `test_ct010_recovery_pending_blocks_write`
  - `test_ct011_unverifiable_receipt_not_success`
  - baseline drift 断言同步为 `result == conflict`。
- 验证：`web` 全量 unittest **61 passed, 1 skipped**；阶段 D 相关测试均通过。
- 证据范围限制：CT-009 仅证明同一进程内线程竞争的 deterministic conflict；不证明跨进程/跨主机锁或分布式协调。
- **未**开放生产写入；**未**关闭 GOAL-009 F-007/F-008；I-003/I-004/I-006 仍未 `verified`。

### 2026-07-21 · 阶段 E · 最终回归与门禁审视

- 用户 `/govern GOAL-013 阶段 E 的最终回归与门禁审视`；依据 [D-005](01-decision.md#d-005--阶段-e--最终回归门禁审视与本目标有界关门2026-07-21)。
- **最终回归命令**（`web/`）：
  ```text
  ..\.venv\Scripts\python.exe -m unittest discover -s tests -v
  ```
- **结果**：`Ran 61 tests in 0.968s` → **OK (skipped=1)**。  
  skip 原因：Windows 无 symlink 特权（`test_escaping_symlink_is_rejected_when_supported`），与受控写入 CT 无关。
- **生产门禁复核**：
  - `test_production_gate_blocks_without_authorization` · ok
  - `test_production_write_gated_when_product_gates_open` · ok
  - `test_decide_http_rejects_when_product_gates_open` · ok
  - `workspace_config.production_product_gates_open` 默认 `True`（空 env）→ 生产写入仍拒绝
- **证据索引（可复现）**：

| 类别 | 测试 / 路径 | 结果码（负向） |
|------|-------------|----------------|
| CT-001 | `test_ct001_*`、`test_missing_fields` | `ERR_MISSING_FIELD` / `ERR_DIGEST_MISMATCH` |
| CT-003 | `test_ct003_*` | `ERR_SCOPE_MISMATCH` |
| CT-006 | `test_ct006_*` | `ERR_DECISION_EXPIRED` / reject·cancel 不写 |
| CT-007 | `test_durable_idempotent_replay_new_service_instance` | 跨实例重放成功不重复写 |
| CT-008 | `test_ct008_*`、`test_operation_id_conflict_*` | `ERR_IDEM_CONFLICT` |
| CT-009 | `test_ct009_concurrent_write_conflict` | `ERR_CONCURRENT_WRITE`（process-local） |
| CT-010 | `test_ct010_recovery_pending_blocks_write` | `ERR_RECOVERY_PENDING` |
| CT-011 | `test_ct011_unverifiable_receipt_not_success` | `ERR_RECEIPT_UNVERIFIABLE` |
| CT-012/014 | `test_ct012_*`、`test_ct014_*` | `ERR_CONTENT_CONTRACT` |
| CT-013 | `test_production_gate_*`、HTTP decide 拒绝 | `ERR_PRODUCT_GATE_OPEN` |
| CT-015 | `test_ct015_*` | `ERR_TRUST_CONTEXT` |
| 实现 | `web/services/controlled_change.py` | — |
| 文档 | `web/README.md`（阶段 B/C/D 错误码） | — |
| fixture | `web/tests/fixtures/r004/workspace-ok/` | 合成，非 dogfood |

- **门禁审视**（对 GOAL-009 回写，见 A-004 / GOAL-009 A-024）：F-007/F-008 **仍 open**；GOAL-009 I-003/I-004/I-006 **不** `verified`；生产写入 **仍阻断**。
- 本目标有界关门：`status: done` / `progress: 100%`（实现证据交付完成；产品写入门禁不随本目标关闭）。

## 进度评估

**100%**：阶段 A～E 完成；证据索引与最终回归已落盘；GOAL-009 F-007/F-008 与生产写入门禁仍开放/阻断。