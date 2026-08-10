---
id: GOAL-012-first-slice-workspace-detail
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.5.0
---

# 执行记录 · GOAL-012

## 时间线

### 2026-07-21 · 立项

- 用户接受 GOAL-009 建议选项并要求推进；GOAL-009 D-012 关闭 F-005（α）并授权本实现目标。
- 创建五件套；尚未编码。

### 2026-07-21 · 实现配置 fail-closed、工作区详情、R-004 受控变更与测试

- 新增 `web/services/workspace_config.py`：`GOAL_GOVERNANCE_WORKSPACE_DIR` / `DATA_ROOT` / `DEV_DOGFOOD`；无配置不加载 dogfood。
- `GoalsRepository.from_config()`；默认不再静默绑定 monorepo 过程树。
- 新增 `web/services/controlled_change.py`：candidate → proposal → decide_and_execute（同请求）→ `ops/receipts`；生产门禁默认拒绝。
- Web：`main.py` 工作区详情 + 目标树导航 + 候选提案表单；`/api/health`。
- 合成 fixture：`web/tests/fixtures/r004/workspace-ok/`（根目标 `GOAL-001-fixture-target`，因协议仅 GOAL-001 可为 null parent）。
- 测试：`test_workspace_config.py`、`test_controlled_change.py`、扩展 `test_main.py`；依赖 `python-multipart`。
- 文档：`web/README.md`、`.env.example` 配置与生产写入检查清单。
- 验证：`python -m unittest discover -s tests -v` → OK（1 skipped symlink）；uvicorn 对 fixture 返回 200 且含目标树。

### 2026-07-21 · 响应 A-001（台账/self 审、F-002～F-004）

- 用户 `/govern` 指令：优先 F-001 台账与 self 审；F-002～F-004 整改或 residual；生产写入仍绑 GOAL-009 门禁。
- F-001：更新 `03-audit` 审视状态；A-002 self 阶段审；progress → **95%**（未 `done`）。
- F-002：收窄 00-meta 成功标准与 `web/README.md` 为 R-004 **关键路径**（非 CT-001～018 全矩阵）。
- F-003：README 标明幂等=进程内；I-005 `accepted-residual`（复审=生产写入前 / GOAL-009 F-008）；**不**开放生产写入。
- F-004：新增 `test_decide_http_rejects_when_product_gates_open`（临时 fixture + HTTP decide → `rejected` / `ERR_PRODUCT_GATE_OPEN`，canonical 未写）。
- 验证：`web/` unittest **44 passed, 1 skipped**（含新增 HTTP decide 门禁用例）。

### 2026-07-21 · 有界关门

- 用户确认：`OK 按有界条件关门 GOAL-012`（生产写入仍关；F-003 residual 不随关门消失）。
- [D-002](01-decision.md#d-002--有界关门α-实现完成生产写入与-f-003-residual-不随关门解除2026-07-21) / [A-003](03-audit.md#a-003--有界关门审计-close-out2026-07-21)：`status: done` / `progress: 100%`；goal-tree 同步。
- **未**设置 `PRODUCT_GATES_OPEN=false`；**未**关闭 GOAL-009 F-007/F-008；**未**将 I-003 标 `verified`；I-005 residual 当时保留。

### 2026-07-21 · 回写关闭 F-003 residual（GOAL-013 CT-007）

- 用户 `/govern` 回写：F-003 residual + GOAL-009 A-020（CT-007 持久化证据）。
- [A-004](03-audit.md#a-004--回写关闭-f-003-residualct-007-持久化2026-07-21)：F-003 **closed**；I-005 **verified**。
- 证据归属 GOAL-013 阶段 B（实现与测试在 `web/`，非本目标重开门编码）。
- **未**开放生产写入；**未**关闭 GOAL-009 F-007/F-008。

## 进度评估

**100%（有界）**：α 实现目标关门。F-003 residual 已后置关闭；生产写入仍阻断。
