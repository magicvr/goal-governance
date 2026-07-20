---
id: GOAL-012-first-slice-workspace-detail
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.2.0
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

## 进度评估

**90%**：α 范围代码与门禁内契约测试已落地；未宣称生产写入已启用；未跑完整 CT-001～018 每一项（关键负向与成功路径已覆盖）。关门前可再做一次 self 审计。
