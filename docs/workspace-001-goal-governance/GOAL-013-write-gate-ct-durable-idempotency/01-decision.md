---
id: GOAL-013-write-gate-ct-durable-idempotency
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.5.0
---

# 决策记录 · GOAL-013

## D-001 · 按 A-020 立项 CT 缺口与跨进程幂等目标（2026-07-21）

**状态**：accepted

**确认来源**：用户 `/govern 按 A-020 立项 GOAL-013（补 CT 缺口与跨进程幂等；生产门禁默认仍关）`。

**决定**：

1. 新建本目标，承接 GOAL-009 A-020 的 **F-007/F-008 关闭前缺口** 与 GOAL-012 **F-003 residual**（跨进程幂等）。
2. 范围 = 实现与可运行测试：  
   - 跨进程 / 跨 service 实例幂等（CT-007 完整语义）  
   - CT 缺口：003、008、009、015  
   - A-020「部分」补全：001、006、012、014 及 010、011  
3. **非范围**：开放生产写入；关闭 GOAL-009 F-007/F-008 或将 I-003/I-004/I-006 标 `verified`（仅回写证据，关闭归 GOAL-009 审视）；AI/N1/共享资料；扩大 `append-execution-fact` 以外的写操作。
4. **生产门禁默认仍关**：`PRODUCT_GATES_OPEN` 默认 true；成功路径测试仅用 `test_authorized` / `TEST_WRITE_MODE`。
5. 权威对照：R-004 测试计划 CT-001～018 + A-020 矩阵；实现优先 `web/services/controlled_change.py` 与 `web/tests/`。

**为什么**：

- GOAL-012 有界关门后，关键路径已有证据，但不足以关闭写入门禁；缺口已冻结，宜独立实现目标承载证据，避免与 GOAL-009 规划台账混淆。
- 跨进程幂等是生产放行前的硬 residual；应在门禁仍关时先补齐。

**未选方案**：

- 在 GOAL-009 内直接编码：混淆规划台账与实现证据。
- 先开放生产写入再补 CT：违反 A-020 硬边界与 CT-013。
- 本目标直接改 GOAL-009 finding 为 closed：关闭须有审视与台账响应，非实现目标静默完成。

**影响**：创建五件套；goal-tree 同步；GOAL-009 记录立项回写；开始编码前完成阶段 A 顺序确认（默认：B 幂等 → C F-007 CT → D F-008 CT → E 回归）。

## D-002 · 阶段 B · 持久化 receipt 与跨实例幂等语义（2026-07-21）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-013 阶段 B`；对照 A-020 F-008 缺口与 CT-007。

**决定**：

1. 成功路径 `decide_and_execute` 将 `ExecutionReceipt` **原子写入**工作区旁路 `ops/receipts/{operation_id}.json`（非五件套）。
2. `decide_and_execute` 在任何 canonical 写入前调用 `_lookup_prior_receipt`：先内存，再磁盘。
3. 同一 `operation_id` 且 `proposal_digest` 与既有 receipt 相同 → 返回既有 receipt，**不**再写 `02-execution.md`（CT-007 跨实例）。
4. 同一 `operation_id` 但 `proposal_digest` 不同 → `ERR_OPERATION_ID_CONFLICT` / `rejected`，不写入（CT-008 部分；完整 request 摘要冲突矩阵可在阶段 D 补）。
5. 生产门禁默认仍关；本阶段测试仅 `test_authorized=True`。

**为什么**：GOAL-012 residual 的根因是幂等表仅在进程内存；磁盘已有 receipt 文件却未加载。加载 + 原子写即可关闭该 residual 的实现缺口。

**未选方案**：把 receipt 写入五件套；用 SQLite 存 operation 表；本阶段开放生产写入。

**影响**：实现见 `web/services/controlled_change.py`；测试见 `test_durable_idempotent_replay_new_service_instance` / `test_operation_id_conflict_different_proposal`。GOAL-009 F-008 **不**因本阶段自动关闭。

## D-004 · 阶段 D · F-008 向 CT 补全（2026-07-21）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-013 阶段 D（F-008：009/010/011 + CT-008 补全）`。

**决定**：

1. CT-008 以完整 `request_digest` 绑定 `operation_id`；同一 operation_id 的不同 action/request 必须返回 `ERR_IDEM_CONFLICT` / `conflict`，且不得覆盖已提交 receipt 或重复追加 canonical。
2. CT-009 采用当前服务进程内、按 workspace 共享的非阻塞锁；锁竞争返回 `ERR_CONCURRENT_WRITE` / `conflict`。本阶段不宣称跨进程、跨主机或分布式锁能力。
3. CT-010 在写入前检查 `.goal-write-recovery.json`；recovery pending 返回 `ERR_RECOVERY_PENDING` / `recovery_pending`，不修改 canonical。
4. CT-011 对加载的 committed receipt 执行最小可验证性检查；缺少 request/pre/post digest 时降级为 `ERR_RECEIPT_UNVERIFIABLE` / `failed`，不得作为成功重放。
5. 生产门禁保持关闭；测试使用显式授权，GOAL-009 F-008、I-003/I-004/I-006 不因本阶段自动关闭或 verified。

**为什么**：这些行为直接对应 A-020/F-008 的请求冲突、并发、恢复未决和 receipt 可核对性缺口；在不开放生产写入的前提下先形成可重复运行证据。

**限制**：CT-009 当前是 process-local lock。真正跨进程/跨部署实例的协调仍是未解决的生产边界，须在 GOAL-009 关闭审视或后续目标中明确。

**影响**：代码与测试见 `web/services/controlled_change.py`、`web/tests/test_controlled_change.py`；阶段 D 退出后进入阶段 E 全量回归与台账回写。

## D-005 · 阶段 E · 最终回归、门禁审视与本目标有界关门（2026-07-21）

**状态**：accepted

**确认来源**：用户 `/govern GOAL-013 阶段 E 的最终回归与门禁审视`。

**决定**：

1. **最终回归**：在 `web/` 运行 `python -m unittest discover -s tests -v`；通过标准 = 全绿（允许既有 symlink skip）。
2. **本目标成功标准**：以 A-020 承接的实现/测试证据为准；证据索引写在 `02-execution` / `03-audit` A-004；**不**在本目标静默关闭 GOAL-009 F-007/F-008，**不**将 GOAL-009 I-003/I-004/I-006 标 `verified`。
3. **门禁审视结论（回写 GOAL-009）**：
   - F-007：A-022 所列关闭条件 1–4 已有运行证据；**正式关闭仍须 GOAL-009 用户/台账动作**。
   - F-008：CT-007/008/010 有完整运行证据；CT-009 仅 process-local；CT-011 为最小 receipt 可核对性（非完整 audit linkage）。**整体仍 open**。
   - 生产写入：**继续阻断**（`PRODUCT_GATES_OPEN` 默认 true）。
4. **本目标有界关门**：GOAL-013 标 `done / 100%`，表示 CT 缺口与跨实例幂等实现目标已交付；残余产品门禁归 GOAL-009。
5. 本目标 I-003/I-004 以 D-004 实现与阶段 E 回归标 `verified`。

**为什么**：实现证据已齐；继续把 GOAL-013 开着只会与规划台账混淆。关闭本目标不等于生产放行。

**未选方案**：在阶段 E 同步关闭 F-007/F-008；开放生产写入；将 process-local lock 伪称为跨进程互斥。

**影响**：更新五件套与 goal-tree；GOAL-009 追加 A-024 门禁审视回写。

## D-003 · 阶段 C · F-007 向 CT 补全语义（2026-07-21）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-013 阶段 C（F-007 向 CT：001/003/006/012/014/015）`。

**决定**：

1. **CT-001**：缺 `goal_id` / `workspace_id` / `source_statement` / content → `ERR_MISSING_FIELD`；candidate content 与 digest 不一致 → `ERR_DIGEST_MISMATCH`。
2. **CT-003**：`workspace_id` 必须等于 service 绑定；`goal_id` 禁止 `..`/`/` 逃逸；跨区绑定不泄漏他区内容。
3. **CT-006**：`expires_at` 到期 → `ERR_DECISION_EXPIRED`；`reject`/`cancel`/`withdraw` 不写 canonical；未知 `proposal_digest` → `ERR_DECISION_INVALID`。
4. **CT-012 / CT-014**：扩展内容契约，拒绝 status/progress/parent/id 治理字段、script、路径穿越、五件套文件名引用。
5. **CT-015**：`external_access=true` 或非 `local-loopback-single-user` mode → `ERR_TRUST_CONTEXT`。
6. 生产门禁默认仍关；本阶段**不**关闭 GOAL-009 F-007（关闭须台账审视 + 仍待 F-008 相关 CT）。

**影响**：`controlled_change.py` + `test_controlled_change.py` 新增 `test_ct00*` 用例。
