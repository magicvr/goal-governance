---
id: E-008
goal: GOAL-001-mcp-file-dual-channel-delivery
doc: execution
title: 维护轮：F-004/F-005/F-007 fixed
status: recorded
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
---

# E-008 · 维护轮执行事实（2026-08-07）

## 事实

用户 `/govern` 确认维护轮「修 F-004/F-005/F-007」（承接 A-013 登记，A-014 后剩余 low 项）。

### F-004 · MCP initialize 门禁（fixed）

- `mcp/server.py` `serve()`：`initialize` 之外的方法在 `self.initialized` 为 false 时返回协议错误 **`-32002`**（Server not initialized），覆盖 `tools/list`、`tools/call`、`ping`；`notifications/initialized` 通知路径不受影响。
- 测试：`skills/tests/test_mcp_l1.py` `McpInitializeGateTests` 4 条（tools/list / tools/call / ping 握手前 `-32002`；握手后可用）。

### F-005 · lifecycle root 信任边界（fixed）

- `mcp/server.py` `_handle_lifecycle_call`：客户端 `root` 解析后必须 `root ⊆ self.repo_root`（`relative_to` 校验），越界返回 **`-32602`**「lifecycle root must stay inside the server-bound repo root」；默认（无 `root`）仍为 `--repo-root`。
- 四个 lifecycle 工具 schema 的 `root` 描述注明越界 fail closed；`mcp/README.md` 增「安全与信任模型」节。
- 测试：`McpLifecycleRootBoundaryTests` 3 条（install 越界 / doctor 越界 → `-32602`；`root=repo_root` 通过包含检查到达 confirm=false 拒写门禁）。

### F-007 · directory-layout 增补 mcp/（fixed · 含 §8c stage）

- `docs/architecture/directory-layout.md` v0.6.5：目录树增 `mcp/` 块（server/entries/kernel/lifecycle/doctor/config/README/Dockerfile）；约束节增「通道资产分离（VP-004 R4 / A-012 F-007）」条目。
- **§8c 强制**：`python scripts/stage_skills_mirrors.py`（copied 1）→ `skills/core/docs/architecture/directory-layout.md` 镜像同步；`--check` 36 对 0 漂移；镜像变更纳入同一提交。

## 验证

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests skills/tests scripts/tests -q` | **210 passed**（原 203 + 7 新增），4 skipped，4 subtests passed |
| `python scripts/stage_skills_mirrors.py --check` | ok（36 pairs，0 漂移） |

## Checkpoint

- 提交 hash 见本轮 commit 记录；owned paths = 本轮全部变更文件（`mcp/server.py`、`mcp/README.md`、`skills/tests/test_mcp_l1.py`、`docs/architecture/directory-layout.md` + stage 镜像 `skills/core/docs/architecture/directory-layout.md`、GOAL-001 03-audit A-015 + 索引 + 本执行记录）。未用 `git add -A`。

## 下一步（待用户）

1. 可选：`/audit` 独立复审 F-004/F-005/F-007 关闭证据（A-015 为 self）。
2. **F-006**：归 VP-002 消费面/协议正文收敛（A-012 建议；触发 = VP-002 推进或下一次协议面修订）。
3. **F-008 / I-007**：首次真实 `v*` GHCR 发布验收时关闭（回填 digest/URL）。
