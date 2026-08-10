---
id: A-014
goal: GOAL-001-mcp-file-dual-channel-delivery
title: 维护轮响应 · F-001 选项 A 重捕获 + F-002/F-003 fixed（self · 编排器）
status: recorded
source: self
date: 2026-08-07
scope: 响应 A-013 登记的维护轮：F-001（选项 A：重捕获 L3）、F-002（server 版本发布钉）、F-003（File 包测试隔离）；不改变任何目标 status/progress
verdict: pass
version: 0.1.0
---

# A-014 · 维护轮响应：F-001 选项 A + F-002/F-003 fixed（2026-08-07）

## 结论

`pass`。用户 2026-08-07 确认维护轮「F-001 选 A，修 F-002/F-003」后执行：

- **F-001 fixed（选项 A · 重捕获 L3）**：四宿主（claude / grok / codex / copilot）以**同一探针 prompt**（哈希未变）与**同一宿主 CLI 版本**重跑，`behaviorSources` 更新为当前树 `mcp/{entries,kernel,server}.py` 当前哈希；四条证据 verdict 全 `pass`（capturedAt 2026-08-07T15:34–15:37Z）。R1 时点 verdict 不因重捕获作废。
- **F-002 fixed**：`mcp/__init__.py` 有效版本改由 `GOAL_GOVERNANCE_MCP_VERSION` 环境钉定（发布流水线经 Docker build arg 传入 pack/tag 版本），内部布局版本独立为 `MCP_LAYOUT_VERSION`；doctor 分列报告 `server.version` / `server.layoutVersion`。
- **F-003 fixed**：`pack_skills_release.py` 排除 `skills/tests/test_mcp_*.py`（MCP 集成测试依赖仓库根 `mcp/` 包，纯 File 解包必失败）；真实打包验证 77 成员、0 `test_mcp_*`、0 MCP 实现路径。

全量测试 **203 passed**（原 198 + 5 新增）、stage 镜像 `--check` **36 对 0 漂移**。无 status/progress 变化；goal-tree 不变；不回退/不重开任何关门状态。

## Findings 响应表

| Finding | source | 级别 | 响应 | 证据 / 留痕 |
|---------|--------|------|------|-------------|
| **F-001**：L3 `behaviorSources` 与当前树字面不一致（R4 迁路径后证据账本过期；`server.py` 哈希合法演进；Root 00-meta 宿主表备注字面不成立） | independent | med | **fixed（选项 A · 重捕获）** | 四宿主重捕获全 `pass`；`behaviorSources` = `mcp/{entries,kernel,server}.py` 当前哈希（entries `ab183e…`、kernel `b0168b…` 与 R1 一致，server `c0af461e…` = 当前树）；prompt 哈希未变；`GOAL-002/attachments/runtime/README.md` 增「捕获点与重捕获」节（R1 绑定历史路径 → R4 remap → 同日重捕获）；Root 00-meta 宿主表备注「behaviorSources 哈希与当前树一致」恢复字面成立。附带修正 R1 证据 `stdoutPath` 目录名不一致（`grok-build-cli-…d` → 实际 `grok-l3-four-entry-…d`）。 |
| **F-002**：`mcp/__version__ = "0.1.0"` 与发布 tag 脱节；经 MCP tools 安装写入 0.1.0，镜像 tag 与进程自报版本可长期漂移 | independent | med | **fixed** | `mcp/__init__.py`：`__version__ = effective_version()`（`GOAL_GOVERNANCE_MCP_VERSION` 钉定，未设时回退 `MCP_LAYOUT_VERSION = "0.1.0"`）；`mcp/Dockerfile` ARG/ENV 接线；`skills-pack-release.yml` docker 步骤增 `build-args: GOAL_GOVERNANCE_MCP_VERSION=${{ needs.pack.outputs.version }}`（镜像内版本与 GHCR tag 同源）；`mcp/doctor.py` 分列 `server.version`（有效）与 `server.layoutVersion`（布局）；`mcp/README.md` 增「版本语义」节；测试：`test_mcp_l1.py` 版本钉 3 条（env 覆盖 / 回退 / serverInfo 端到端）、`test_mcp_config.py` doctor 分列 1 条、`test_pack_skills_release.py` workflow build-arg 契约断言。 |
| **F-003**：File zip 内 `tests/test_mcp_*.py` 在纯 skills 解包环境失败（本审隔离解包 6 failed） | independent | low | **fixed** | `scripts/pack_skills_release.py` `should_exclude` 增 `tests/test_mcp_*`（注释注明 F-003 依据）；`test_pack_skills_release.py` 增单元断言（test_mcp_* 排除、其他 skills 测试保留）+ 真实打包 `/tests/test_mcp_` 片段防御断言；实测 `--version 0.0.0-f003check` 打包 **77 成员、0 `test_mcp_*`、0 `mcp/` 实现路径**。 |

## 验证证据

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests skills/tests scripts/tests -q` | **203 passed**, 4 skipped, 4 subtests passed（~43s；原 198 + 5 新增） |
| `python scripts/stage_skills_mirrors.py --check` | **ok**（36 pairs；无漂移，本轮未改 canonical 白名单） |
| 真实打包 `0.0.0-f003check` | 77 成员；`test_mcp_*` 0 条；`mcp/` 实现 0 条（channel 资产分离保持） |
| L3 重捕获（四宿主，同 prompt/同版本） | claude / grok / codex / copilot 全 `pass`（marker observed、exit 0） |

## 仍开放项（A-013 登记，未在本轮处置）

- F-004（MCP 协议 initialize 顺序）、F-005（lifecycle root 信任模型）、F-007（directory-layout.md 补 `mcp/` 行）：**open**，归后续维护轮（均 low、非必改）。
- F-006：归 **VP-002** 消费面/协议正文收敛（A-012 建议），不 reopening workspace-003。
- F-008 / I-007：首次真实 `v*` GHCR 发布验收时关闭（non-blocking）。

## 边界

- 未修改任何目标 `status` / 检查点 / 派生 `progress`；未改 VP-004 / workspace.md；goal-tree 无变化。
- 本响应为编排器 self 侧记录（response 模式），不冒充 `source: independent`。
- 审计模式 `self`：维护修复低风险、可逆、边界清楚；如需独立复审可再跑 `/audit` 核验 F-001～F-003 关闭证据。
