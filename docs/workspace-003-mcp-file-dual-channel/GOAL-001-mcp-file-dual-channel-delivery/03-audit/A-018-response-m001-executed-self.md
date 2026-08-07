---
id: A-018
goal: GOAL-001-mcp-file-dual-channel-delivery
title: 响应 M-001 · capture --check 一致性校验落地（self · 编排器）
status: recorded
source: self
date: 2026-08-08
scope: 执行维护项 M-001（A-016 防再犯建议：capture 证据哈希一致性检查）；实现 --check 校验与测试；不改变任何目标 status/progress
verdict: pass
version: 0.1.0
---

# A-018 · M-001 执行响应（2026-08-08）

## 结论

`pass`。M-001（registered，E-010 登记）按用户 2026-08-08 指令执行完毕：

- `scripts/capture_runtime_evidence.py` 新增 **`--check`** 一致性校验（`check_evidence_file` / `run_evidence_check`）：枚举证据 `behaviorSources` 与当前树逐一比对（复用 `_repo_file` 防穿越、`_sha256_repo_text` 同捕获哈希语义、`_validate` schema 校验）；非证据 JSON 跳过；`--evidence-dir` 可重复且 check 模式必填（**历史时点证据绑定捕获时点树，不隐式全仓扫描**——A-016 建议落地时的重要语义修正）。
- 新增 10 条测试（`EvidenceConsistencyCheckTests`）：一致绿 / stale 红 / 缺失红 / 穿越拒绝 / 非证据跳过 / 计数 / CLI exit 0/1 / 缺目录 1 / 缺 `--evidence-dir` exit 2 / 多目录累加。
- 端到端：workspace-003 L3 证据目录 **ok（4 文件）**；历史发布证据目录（`docs/releases/runtime/v0.12.1`）显式检查正确红（exit 1）。全量 **234 passed**（+10 新增，无回归）。
- 维护钩子文档入 `GOAL-002/attachments/runtime/README.md`「一致性检查（M-001 · A-016）」节。

**M-001：registered → done**。A-016 防再犯建议（建议 3）闭环；F-001/F-001r 的「证据账本过期复发」根因（改 `mcp/` 实现后无检查暴露）自此有测试层兜底。

## 响应对象

- **M-001**（维护项，E-010 登记，来源 A-016 建议 3）：capture 证据哈希一致性检查——验收标准 ①～⑤ 全部满足（详见 `02-execution/E-011-execute-m001-check.md` 验收对照表）。
- **A-016**（independent，conditional）：三条建议中 建议 1/2（F-001r 关闭证据）已由 A-017 处置；**建议 3（防再犯）由本轮闭环**。

## 关闭证据表

| 项 | 状态 | 证据路径 |
|----|------|----------|
| M-001（capture `--check` + 测试） | **done** | `scripts/capture_runtime_evidence.py`（`check_evidence_file` / `run_evidence_check` / `--check` CLI）；`scripts/tests/test_runtime_evidence.py` `EvidenceConsistencyCheckTests`（10 条）；端到端 `--check` workspace-003 evidence ok（4 文件）/ v0.12.1 显式检查红；全量 234 passed；GOAL-002 runtime README「一致性检查」节；`02-execution/E-011` |

## 仍开放项

- **F-006**：归 VP-002 消费面/协议正文收敛（A-012/A-013）。
- **F-008 / I-007**（non-blocking）：首次真实 `v*` GHCR 发布验收时关闭。
- 可选（非必改）：CI 挂接 `--check`（发布 workflow 对 L3 证据目录定期校验），随下次发布轮决定。

## 验证证据

| 动作 | 结果 |
|------|------|
| `python -m pytest scripts/tests/test_runtime_evidence.py -q` | **38 passed**, 8 subtests passed（含 10 条新增） |
| `python -m pytest docs/tests skills/tests scripts/tests -q` | **234 passed**, 4 skipped, 8 subtests passed（~42s；无回归） |
| `--check` workspace-003 L3 evidence 目录 | `evidence consistency ok (4 evidence file(s))`（exit 0） |
| `--check` docs/releases/runtime/v0.12.1（历史时点证据） | 正确检出 stale（exit 1）——验证检查有效性；历史证据语义绑定捕获时点树 |
| stage | 未改 canonical 白名单；无需 stage |

## 边界

- 未修改任何目标 `status` / 检查点 / 派生 `progress`；未改 VP-004 / workspace.md；goal-tree 无变化。
- 本响应为编排器 self 侧记录（response 模式），不冒充 `source: independent`。
- 审计模式 `self`：工具链维护低风险、可逆、有全量测试兜底；如需独立复审可再跑 `/audit`。
