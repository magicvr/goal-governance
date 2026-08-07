---
id: A-004
goal: GOAL-006-consumer-surface-convergence
doc: audit
title: 响应 F-003（deferred → fixed）· governance_root≠docs 消费场景 e2e（self · 编排器）
status: recorded
source: self
date: 2026-08-08
scope: 响应 GOAL-006 关门后仍开放项 F-003（independent A-002，low，deferred 至 VP-002 波次）与 A-001 R-002（并入）：补充 governance_root≠docs 消费场景 e2e 测试；不改变目标 status/progress
verdict: pass
version: 0.1.0
---

# A-004 · F-003 执行响应（2026-08-08）

## 结论

`pass`。用户 2026-08-08 指令执行 F-003——`skills/tests/test_consumer_surface_relativeization.py` 新增 **`ConsumerSurfaceE2ETests`**（3 条）：

1. **`test_pinned_agents_reads_paths_under_non_docs_root`**：模拟消费仓 `governance_root = governance`（非 docs）+ `.goal-governance.json` 配置；AGENTS.md = 模板拷贝 + `{{GOVERNANCE_ROOT}}` 安装时 pin 展开为 `governance`——断言安装产物**无裸 `docs/`**，且关键协议路径（`governance/architecture/principles.md`、`governance/workspace-<NNN>-<slug>/`、`governance/vision/`、`governance/templates/`、`governance/goals/`、`governance/README.md`）**全部读取于配置根**。
2. **`test_installed_shells_read_paths_under_governance_root`**：四入口 SKILL.md 壳安装产物无裸 `docs/` 且含 `{governance_root}/` 路径引用。
3. **`test_all_path_references_resolve_under_configured_root`**：从安装产物提取全部路径引用，断言无一泄漏 `docs/`、全部解析于配置根（`governance/` 或 `{governance_root}`）——读取路径断言。

- **F-003（independent，low）fixed**：`governance_root≠docs` 从「仅字面断言」升级为「模拟消费仓安装 + pin 展开 + 路径读取」e2e；与 A-001 R-002（同构建议）一并闭合。
- GOAL-006 已 `done`（2026-08-08），本响应为 **post-close 维护轮**（先例 A-014/A-015 模式）：不改变目标 status/progress。

## 响应对象

- **F-003**（A-002 independent · low · deferred 至 VP-002 波次）：「`governance_root≠docs` 仅有字面/占位断言，无消费场景 e2e」。
- **R-002**（A-001 self · low · 并入 F-003）：同构建议。

## 关闭证据表

| Finding | source | 级别 | 状态 | 证据 |
|---------|--------|------|------|------|
| F-003（≠docs 消费场景 e2e） | independent | low | **fixed** | `ConsumerSurfaceE2ETests` 3 条（模拟安装 + pin 展开 + 路径读取断言）；8 passed（本文件） |
| R-002（同构） | self | low | **fixed**（并入） | 同上 |

## 验证

| 动作 | 结果 |
|------|------|
| `pytest skills/tests/test_consumer_surface_relativeization.py` | **8 passed**, 90 subtests（5 防再犯 + 3 e2e） |
| 全量 `pytest docs/tests skills/tests scripts/tests` | 见 E-006（应 242 passed：239 + 3 e2e） |
| stage | 未改白名单文件（测试文件非 canonical）→ 无需 stage |

## 仍开放项

- GOAL-002 I-003（矩阵 committed；发版宣称前另决）、GOAL-003 F-003（Web writer 复审；带触发）、GOAL-006 R-001（matrix candidateRevision；release 轮）——均为登记项，触发未到。
- GOAL-006 至此 **F-001～F-004 全部响应完毕**（A-003/A-004）。

## 边界

- 本响应为编排器 self 侧记录（response 模式）；不改 status/progress/goal-tree。
- 审计模式 `self`：低风险可逆维护（纯测试新增），post-close 兜底已足够。
