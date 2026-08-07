---
id: E-010
goal: GOAL-001-mcp-file-dual-channel-delivery
doc: execution
title: 立项登记维护项 M-001（A-016 防再犯建议：capture 证据哈希一致性检查）
status: recorded
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
---

# E-010 · 维护项 M-001 立项登记（2026-08-08）

## 事实

用户 `/govern` 指令：「将 A-016 防再犯建议（capture 证据哈希一致性检查）立项为维护项」。

- 背景：A-016（independent，conditional）建议 3——「为 `scripts/capture_runtime_evidence.py` 或 CI 增加『L3 证据 `behaviorSources` 与当前树哈希』一致性检查，使修改 `mcp/` 实现后证据过期在测试层即暴露」。F-001 已在 A-012→A-014→A-016（复发一次）→A-017 三轮处置中暴露两次同类过期（R4 迁路径、A-015 改 server.py），属**可复发的证据账本维护缺口**，值得正式跟踪。
- 本轮**仅立项登记**（不改变任何 status/progress；不新建子目标；不回退 workspace-003 关门状态）。实现归后续维护轮执行。
- 登记位置：本执行记录（事实）+ `03-audit.md` 结论段（响应留痕）。goal-tree 无变化（无状态/检查点变更）。

## 维护项登记表（本登记引入 M-NNN 编号；用于 workspace-003 工具链 post-close 维护项跟踪）

| 字段 | 值 |
|------|-----|
| **ID** | M-001 |
| **标题** | capture 证据哈希一致性检查（A-016 防再犯建议） |
| **来源** | A-016（independent）建议 3；关联 F-001 / F-001r（证据账本过期两轮复发） |
| **范围** | `scripts/capture_runtime_evidence.py`（新增 `--check` 或等价校验入口）+ `scripts/tests/test_runtime_evidence.py`（一致性断言测试）；可选 CI 步骤（对已提交 L3 证据 JSON 校验） |
| **验收标准** | ① 测试/检查能枚举已捕获证据的 `behaviorSources` 并比对当前树文件哈希；② `mcp/`（或 `skills/`）实现变更后该检查**红**（提示重捕获或注解）；③ 重捕获后**绿**；④ 全量测试仍绿（当前基线 210 passed）；⑤ stage `--check` 不受影响 |
| **触发条件** | 下一维护轮 / 用户安排执行；或下次修改 `mcp/` 实现前优先完成 |
| **归属** | workspace-003 Root 工具链维护（与 F-002/F-003 同域：mcp/、scripts/）；不 reopening 工作区 |
| **状态** | **registered**（未开始执行；open） |
| **非目标** | 不自动重捕获宿主证据（宿主 CLI 不可在 CI 假定可用）；不改 `runtime-evidence.schema.json` 语义；不把检查作为关门/放行依据 |

## Checkpoint

- 提交 hash 见本轮 commit 记录；owned paths = 本执行记录（`02-execution.md` 索引）+ `03-audit.md` 结论段。未用 `git add -A`。

## 下一步（待用户）

1. 执行 M-001（实现 capture 一致性检查 + 测试）——可单独一轮维护轮，也可与 F-006 移交 VP-002 等事项分批。
2. 其余仍开放项不变：F-006（VP-002）、F-008 / I-007（首次真实 GHCR 发布验收）。
