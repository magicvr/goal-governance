---
id: E-007
goal: GOAL-001-mcp-file-dual-channel-delivery
doc: execution
title: 维护轮：F-001 选项 A 重捕获 L3 + F-002/F-003 fixed
status: recorded
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
---

# E-007 · 维护轮执行事实（2026-08-07）

## 事实

用户 `/govern` 确认维护轮「F-001 选 A，修 F-002/F-003」（承接 A-013 登记）。

### F-001 选项 A · L3 重捕获（fixed）

- 以 `scripts/capture_runtime_evidence.py` 的 `capture()` 驱动四宿主重跑，**同一探针 prompt**（`attachments/runtime/prompts/*-l3-four-entry.txt`，哈希未变）与**同一宿主 CLI 版本**（claude 2.1.223 / grok 1.0.0 / codex 0.146.1 / copilot 1.0.75）；`behaviorSources` 更新为 `mcp/entries.py`、`mcp/kernel.py`、`mcp/server.py` 当前路径与当前哈希。
- 结果：claude / grok / codex / copilot 全 `pass`（marker observed、exit 0）；capturedAt 2026-08-07T15:34–15:37Z；`runtime-evidence.schema.json` 校验通过（capture 内建）。
- 哈希对照：entries `ab183e15…`、kernel `b0168b2e…` 与 R1 一致（A-012 remap 判断成立）；server `c0af461e…` = 当前树（R2/R4 合法演进）。
- 附带：R1 证据 `stdoutPath` 目录名不一致（`grok-build-cli-…d` vs 实际 `grok-l3-four-entry-…d`）随重捕获修正。
- `GOAL-002/attachments/runtime/README.md` 增「捕获点与重捕获」节；Root 00-meta 宿主表备注「behaviorSources 哈希与当前树一致」恢复字面成立（未改动 meta 正文）。

### F-002 · server 版本发布钉（fixed）

- `mcp/__init__.py`：`MCP_LAYOUT_VERSION = "0.1.0"`（内部布局版本）独立；`effective_version()` 读 `GOAL_GOVERNANCE_MCP_VERSION` 环境钉，未设回退布局版本；`__version__ = effective_version()`。
- `mcp/Dockerfile`：`ARG GOAL_GOVERNANCE_MCP_VERSION=` + `ENV` 接线。
- `.github/workflows/skills-pack-release.yml`：docker 步骤增 `build-args: GOAL_GOVERNANCE_MCP_VERSION=${{ needs.pack.outputs.version }}`（镜像内版本与 GHCR tag 同源）。
- `mcp/doctor.py`：报告增 `server.version`（有效）/ `server.layoutVersion`（布局）分列。
- `mcp/README.md`：增「版本语义」节。
- 测试：`skills/tests/test_mcp_l1.py` 增 `McpVersionPinTests` 3 条（env 覆盖 / 回退 / serverInfo 端到端）；`skills/tests/test_mcp_config.py` 增 doctor 分列断言；`scripts/tests/test_pack_skills_release.py` 增 workflow build-arg 契约断言。

### F-003 · File 包测试隔离（fixed）

- `scripts/pack_skills_release.py` `should_exclude` 增 `tests/test_mcp_*`（MCP 集成测试依赖仓库根 `mcp/` 包）。
- `scripts/tests/test_pack_skills_release.py`：单元断言（test_mcp_* 排除、其他 skills 测试保留）+ 真实打包 `/tests/test_mcp_` 片段防御断言。
- 实测：`pack_skills_release.py --version 0.0.0-f003check` → **77 成员**（原 80 − 3 个 test_mcp_*）、`test_mcp_*` 0 条、`mcp/` 实现 0 条。

## 验证

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests skills/tests scripts/tests -q` | **203 passed**（原 198 + 5 新增），4 skipped，4 subtests passed |
| `python scripts/stage_skills_mirrors.py --check` | ok（36 pairs，0 漂移；未改 canonical 白名单路径，无需 stage） |
| L3 重捕获四宿主 | 全 pass（见上） |

## Checkpoint

- 提交 hash 见本轮 commit 记录；owned paths = 本维护轮全部变更文件（mcp/、scripts/pack_skills_release.py、scripts/tests/test_pack_skills_release.py、.github/workflows/skills-pack-release.yml、skills/tests/test_mcp_l1.py、test_mcp_config.py、GOAL-002 runtime README + L3 证据 JSON/stdout/stderr、GOAL-001 03-audit A-014 + 索引 + 本执行记录）。未用 `git add -A`。

## 下一步（待用户）

1. 可选：`/audit` 独立复审 F-001～F-003 关闭证据（A-014 为 self）。
2. F-004/F-005/F-007 仍 open（登记于 A-013），归后续维护轮。
3. F-006 归 VP-002 消费面；F-008/I-007 于首次真实 `v*` GHCR 发布验收时关闭。
