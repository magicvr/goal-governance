---
id: D-002
goal_id: GOAL-002-r1-mcp-equivalence-kernel
title: R1 方案冻结 · MCP 运行时形态与四治理入口映射（I-001 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-002 · MCP 运行时形态与四治理入口映射（2026-08-07）

## 决定

1. **运行时形态**：MCP 通道以 **Python 3 stdio 进程**为最小运行形态，实现 MCP stdio transport（**换行分隔 JSON-RPC 2.0**，每行一个 JSON 消息），零第三方运行时依赖（仅标准库 + 可选 `jsonschema`）。**不强制 Docker**；提供 `Dockerfile` 仅作便捷可选。落点：`skills/mcp/`（随 skills 包分发，pack 已覆盖）。
2. **四治理入口映射**：MCP server 暴露恰好四个治理工具，名称与 File 通道入口一致：

   | 工具名 | 关键参数边界 | 层级 | 角色边界 |
   |--------|--------------|------|----------|
   | `vision` | `task`(必填,string)、`workspace`(可选,string) | 决策层 | 建修 Charter、VP、组合编排、Vision Review、re-align；冷启动优先 |
   | `vision-audit` | `task`(必填,string)、`scope`(可选,string) | 决策层 | 独立 Vision Review：**只出意见**到 `{governance_root}/vision/reviews*`，不改 Charter/VP/Goal 状态 |
   | `govern` | `task`(必填,string)、`workspace`(可选,string)、`goal_id`(可选,string) | 实现层 | 实现编排：扫描→意见台账→P-004 裁决→提议→确认→原语写入 |
   | `audit` | `task`(必填,string)、`goal_id`(必填,string)、`scope`(可选,string) | 实现层 | Goal 交叉审计：**只出意见**到被审目标 `03-audit`，不改 `status` |

   `commit` **不**进入 MCP 工具集（与 VP-004 入口面一致：便利可选、不绑架治理安装）。
3. **薄宿主入口**：MCP 工具即薄入口；`tools/call` 返回结构化元数据（entrypoint、layer、role、readonly、prompt_path、guidance），可核对角色边界。若消费仓存在 `skills/prompts/<入口>.md`，同时返回其 sha256 供可追溯性核对；不存在时以内置 guidance 摘要兜底（不要求 File 大包）。
4. **实例真相**：两通道一致——实例状态仍在仓库内治理记录树（`{governance_root}`，默认 `docs`）；MCP **不得**成为权威状态库。
5. **证据分级**：L1 = 通道各自直接驱动本通道产物的测试；L2 = 共享内核断言（`skills/mcp/kernel.py`）；L3 = 承诺宿主 × 通道的抽稀真探针。合同按 `deliveryChannel: files | mcp` 分列并标注 L1/L2/L3。

## 未选方案

- **Docker-only MCP**：排除（VP-004 明确 stdio 等进程形态合法）。
- **DB/SQLite 后端状态库**：排除（VP-004 非目标；MCP 不得替代仓内实例真相）。
- **MCP mock 顶替 File 证据**：排除；L1 File 与 L1 MCP 分列。
- **把 `commit` 纳入 MCP 工具集**：排除（正交便利项，不进治理必达集）。

## 依据

- VP-004「入口面」表：四治理必达入口 + `commit` 便利可选。
- VP-004 R1：MCP 通道「不必安装 File 大包」即达四入口等价检查点；运行时推荐 Docker、允许本地 stdio。
- 现有 File 入口：`skills/prompts/00-govern-orchestrator.md`、`05-independent-audit.md`、`06-vision-orchestrator.md`、`07-independent-vision-review.md`。

## 证据 / 结论

- I-001 以本决定关闭（required → closed）。验证动作：`skills/tests/test_mcp_l1.py` 真启动 server 进程断言四工具名与关键参数边界；`docs/tests/test_dual_channel_l2.py` 用共享内核核对两通道等价检查点。
