---
id: A-017
goal: GOAL-001-mcp-file-dual-channel-delivery
title: 响应 A-016（independent conditional）· F-001 关闭证据重捕获 fixed（self · 编排器）
status: recorded
source: self
date: 2026-08-07
scope: 响应 A-016（independent，conditional）F-001r：L3 证据 behaviorSources 与当前树不一致（A-015 改 server.py 后过期）；按用户指令执行选项 A 重新捕获；不改变任何目标 status/progress
verdict: pass
version: 0.1.0
---

# A-017 · 响应 A-016 并关闭 F-001r（2026-08-07）

## 结论

`pass`。用户 2026-08-07 指令「F-001 关闭证据过期（server.py 哈希演进），重新捕获检查」→ 执行 **F-001 选项 A（重捕获）**：四宿主（claude 2.1.223 / grok 1.0.0 / codex 0.146.1 / copilot 1.0.75）以**同一探针 prompt**（四条 prompt 输入哈希未变：`a423385d…`/`5d98a018…`/`107ebc4b…`/`fe57e7b7…`）与同一宿主 CLI 版本并行重跑，`behaviorSources` 重新绑定当前树（`entries ab183e15…`、`kernel b0168b2e…` 未变；**`server cd31cbde…` = 当前树**）；四条证据 `capturedAt` 2026-08-07T15:59–16:01Z，verdict 全 `pass`（exit 0、marker observed），capture 内建 schema 校验通过。

- **F-001r（A-016，med）fixed**：`behaviorSources` 与当前树**逐字一致**；Root `00-meta` 宿主表备注「behaviorSources 哈希与当前树一致」恢复字面成立（未改 meta 正文）；GOAL-002 runtime README「捕获点与重捕获」节补记第三次捕获点与「改 `mcp/` 须同步刷新证据」维护钩子。
- **F-002 / F-003 / F-004 / F-005 / F-007**：A-016 已核验关闭证据充分，**维持 fixed**（本轮无相关代码变更）。
- A-016 无 required、无冲突 → 不触发 P-004；**不回退** Root `done` / 子目标 done / VP-004 `closed` / workspace `closed` 状态。

## 响应对象

- **A-016**（independent · 独立复审 F-001～F-005、F-007 关闭证据）verdict `conditional`；required 0；F-001r（recommended · med）——「F-001 关闭证据在 A-015 修改 `mcp/server.py` 后再次过期（JSON `c0af461e…` vs 当前树 `cd31cbde…`）」。
- A-016 亦确认 F-002/F-003/F-004/F-005/F-007 关闭证据充分（210 测试绿 / stage 0 漂移 / 实包 77 成员 0 混入 / 门禁与边界代码就位）。

## 关闭证据表

| Finding | source | 级别 | 状态 | 证据路径 |
|---------|--------|------|------|----------|
| F-001r：L3 `behaviorSources[server.py]` 与当前树不一致（A-015 后过期） | independent（A-016） | med | **fixed（选项 A 重捕获）** | 四条 `GOAL-002/attachments/runtime/evidence/*-l3-four-entry-2026-08-07.json`（capturedAt 15:59–16:01Z；`server.py = cd31cbde…` = 当前树；prompt 输入哈希未变；verdict 全 pass）；`mcp/server.py` 当前哈希 `cd31cbdebe10e15cc6d6b2f47e6ba365874cd1c9ffb87cf847f75b3d1bdedb82`；`GOAL-002/attachments/runtime/README.md`「捕获点与重捕获」节；Root 00-meta 宿主表备注恢复字面成立 |
| F-001（A-012 原始） | independent（A-012） | med | **fixed**（维持，A-014 重捕获 + 本轮复验） | 同上；entries/kernel 哈希与 R1 一致（`ab183e15…`/`b0168b2e…`） |
| F-002（版本发布钉） | independent（A-012） | med | **fixed**（维持；A-016 认可） | `mcp/__init__.py` / Dockerfile / `skills-pack-release.yml` build-args / doctor 分列 / README 版本语义节 / 测试 |
| F-003（File 包测试隔离） | independent（A-012） | low | **fixed**（维持；A-016 实包复核 77 成员 0 混入） | `pack_skills_release.py` `should_exclude` / `test_pack_skills_release.py` 断言 |
| F-004（initialize 门禁） | independent（A-012） | low | **fixed**（维持；A-016 认可） | `mcp/server.py` `-32002` / `McpInitializeGateTests` |
| F-005（lifecycle root 边界） | independent（A-012） | low | **fixed**（维持；A-016 认可） | `mcp/server.py` `-32602` / schema 描述 / README 信任模型节 / `McpLifecycleRootBoundaryTests` |
| F-007（directory-layout mcp/） | independent（A-012） | low | **fixed**（维持；A-016 认可） | `docs/architecture/directory-layout.md` v0.6.5 / stage 镜像 0 漂移 |

## 仍开放项

- **F-006**：归 VP-002 消费面/协议正文收敛（A-012/A-013 建议；触发 = VP-002 推进或下一次协议面修订）。
- **F-008 / I-007**（non-blocking）：首次真实 `v*` GHCR 发布验收时关闭（回填 digest/URL）。
- **A-016 建议（防再犯，recommended，待用户决定）**：为 `scripts/capture_runtime_evidence.py` 或 CI 增加「L3 证据 `behaviorSources` 与当前树哈希」一致性检查，使改 `mcp/` 实现后证据过期在测试层暴露。未立项前，runtime README 维护钩子已写明。

## 验证证据

| 动作 | 结果 |
|------|------|
| 四宿主 L3 重捕获（同 prompt/同版本） | claude / grok / codex / copilot 全 `pass`（exit 0、marker observed；capturedAt 15:59–16:01Z） |
| 重捕获后 `behaviorSources` vs 当前树 | 3/3 一致（entries/kernel/server）；4 prompt 输入哈希不变 |
| 全量测试 | 210 passed（A-016 复核；本轮无代码变更） |
| stage 镜像 | 本轮未改 canonical 白名单（无需 stage）；A-016 复核 36 对 0 漂移 |

## 边界

- 未修改任何目标 `status` / 检查点 / 派生 `progress`；未改 VP-004 / workspace.md；goal-tree 无变化。
- 本响应为编排器 self 侧记录（response 模式），不冒充 `source: independent`。
- 审计模式 `self`：证据重捕获低风险、可逆、边界清楚（A-016 已 independent 定位缺口，本轮执行修正）；如需再次独立复审可再跑 `/audit`。
