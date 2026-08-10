---
id: A-015
goal: GOAL-001-mcp-file-dual-channel-delivery
title: 维护轮响应 · F-004/F-005/F-007 fixed（self · 编排器）
status: recorded
source: self
date: 2026-08-07
scope: 响应 A-013 登记的维护轮：F-004（MCP initialize 门禁）、F-005（lifecycle root 信任边界）、F-007（directory-layout 补 mcp/）；不改变任何目标 status/progress
verdict: pass
version: 0.1.0
---

# A-015 · 维护轮响应：F-004/F-005/F-007 fixed（2026-08-07）

## 结论

`pass`。用户 2026-08-07 确认维护轮「修 F-004/F-005/F-007」（均 low、非必改，A-013 登记）后执行，三条全部 **fixed**：

- **F-004 fixed**：MCP server 强制 `initialize` 先于一切请求——`initialize` 之外的方法在握手完成前一律返回协议错误 `-32002`（Server not initialized）。
- **F-005 fixed**：lifecycle 工具（install/upgrade/uninstall/doctor）的 `root` 参数必须落在 server 绑定的 `--repo-root` 内，越界 **fail closed**（`-32602` 明确错误）；allowlist 只对绑定仓库生效。
- **F-007 fixed**：`docs/architecture/directory-layout.md` 增补仓库根 `mcp/`（通道资产分离布局）与对应约束；canonical → Skills 镜像按 §8c stage（1 个文件复制，`--check` 0 漂移）。

全量测试 **210 passed**（原 203 + 7 新增）；stage 镜像 `--check` 36 对 0 漂移。无 status/progress 变化；goal-tree 不变；不回退/不重开任何关门状态。

## Findings 响应表

| Finding | source | 级别 | 响应 | 证据 / 留痕 |
|---------|--------|------|------|-------------|
| **F-004**：MCP 协议未强制 `initialize` 后再 `tools/list|call`（`initialized` 为 false 时工具仍可用） | independent | low | **fixed** | `mcp/server.py` `serve()`：`initialize` 之外的方法在 `self.initialized` 前返回 `-32002`（含 `ping`；`notifications/initialized` 通知路径不受影响）。测试（`test_mcp_l1.py` `McpInitializeGateTests` 4 条）：`tools/list` / `tools/call` / `ping` 在握手前 → `-32002`；握手后工具可用。 |
| **F-005**：lifecycle `root` 可指向任意本机目录并写 AGENTS.md（allowlist 相对该 root，非绑定 server `--repo-root`） | independent | low | **fixed** | `mcp/server.py` `_handle_lifecycle_call`：`root` 解析后必须 `root ⊆ self.repo_root`，越界 `-32602`「must stay inside the server-bound repo root」；四个 lifecycle 工具 schema 的 `root` 描述注明「必须位于其内，越界 fail closed」；`mcp/README.md` 增「安全与信任模型」节（绑定根 + allowlist + confirm 双门禁，Docker 与 stdio 同语义）。测试（`McpLifecycleRootBoundaryTests` 3 条）：`install`/`doctor` 越界 → `-32602`；`root=repo_root` 时通过包含检查、到达 confirm=false 拒写门禁。 |
| **F-007**：`directory-layout.md` 未反映 R4 根目录 `mcp/`（仍停在 skills 包内布局叙事） | independent | low | **fixed** | `docs/architecture/directory-layout.md`（v0.6.5）：目录树增 `mcp/` 块（server/entries/kernel/lifecycle/doctor/config/README/Dockerfile），约束节增「通道资产分离（VP-004 R4 / A-012 F-007）」：`mcp/` 实现与 `skills/tests/test_mcp_*.py` 不进 File zip；GHCR 为 MCP 发布资产。按 §8c `python scripts/stage_skills_mirrors.py`（copied 1）+ `--check` ok，镜像 `skills/core/docs/architecture/directory-layout.md` 随本轮提交。 |

## 验证证据

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests skills/tests scripts/tests -q` | **210 passed**, 4 skipped, 4 subtests passed（~41s；原 203 + 7 新增） |
| `python scripts/stage_skills_mirrors.py --check` | **ok**（36 pairs；0 漂移；本轮 1 个 canonical → 镜像复制） |

## 仍开放项

- F-006：归 **VP-002** 消费面/协议正文收敛（A-012 建议），不 reopening workspace-003。
- F-008 / I-007：首次真实 `v*` GHCR 发布验收时关闭（non-blocking）。
- A-012 登记项至此 **F-001～F-005、F-007 全部 fixed**（A-014/A-015）；剩余 F-006、F-008 有明确归属与触发。

## 边界

- 未修改任何目标 `status` / 检查点 / 派生 `progress`；未改 VP-004 / workspace.md；goal-tree 无变化。
- 本响应为编排器 self 侧记录（response 模式），不冒充 `source: independent`。
- 审计模式 `self`：维护修复低风险、可逆、边界清楚；如需独立复审可再跑 `/audit` 核验关闭证据。
