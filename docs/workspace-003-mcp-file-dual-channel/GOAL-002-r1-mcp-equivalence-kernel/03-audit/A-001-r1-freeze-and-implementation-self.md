---
id: A-001
goal: GOAL-002-r1-mcp-equivalence-kernel
title: R1 方案冻结与双通道实现自审
status: recorded
source: self
date: 2026-08-07
scope: R1 方案冻结（D-002/D-003/D-004）、skills/mcp 双通道实现、deliveryChannel 合同分列、L2/L1 测试与四宿主 L3 探针证据
verdict: pass
version: 0.1.0
---

# A-001 · R1 方案冻结与双通道实现自审

## 结论

`pass`。本审覆盖 R1 方案冻结、实现与验证事实；不替代 independent cross audit（A-002 待写），也不宣称 R2/R3 或目标关门。

## 证据（可指回）

| 主张 | 证据 |
|------|------|
| I-001/I-002/I-003 关闭 | `01-decision/D-002/D-003/D-004` accepted；`00-meta` 信息表 closed |
| MCP 通道实现 | `skills/mcp/{entries,server,kernel}.py` + README；MCP stdio 真启动冒烟 2 次逐字节一致（scratch `mcp-launch-1/2.log`） |
| 合同分列 | `docs/contracts/*` `deliveryChannels: files\|mcp` + contractFormatVersion 0.4.0；`skills/contracts` 镜像 `--check` 通过；`scripts/tests/test_contract_delivery_channels.py` 全绿 |
| L2 共享内核 | `kernel.py` 十条检查点 + 同断言驱动两通道；`docs/tests/test_dual_channel_l2.py` 通过 |
| L1 分列测试 | `skills/tests/test_mcp_l1.py`（真进程）+ `docs/tests/test_file_l1.py`（真 File 资产，无 MCP mock）通过 |
| 全量回归 | `python -m pytest docs/tests scripts/tests skills/tests` = 168 passed / 3 skipped / 4 subtests（基线 143）；输出捕获 scratch `pytest-r1.log` |
| 四宿主 L3 探针 | `attachments/runtime/evidence/*-l3-four-entry-2026-08-07.json`：claude / grok / codex / copilot 全部 `pass` + marker observed（schema 校验通过，capture 脚本内建） |

## Findings

- **required findings：无。**
- **recommended（非阻断）：**
  - R-001：`describe_mcp_channel` 的角色文本与 File 描述同源（`entries.py` ROLE_BOUNDARIES），L2 角色一致性断言为同源比较；已由 L1 测试对真实 server `tools/call` 输出做独立核对，接受该分层。
  - R-002：codex CLI 为 npm shim（`codex.cmd`），子进程捕获需 `cmd.exe /d /s /c` 包装；已体现在证据 `invocation.command`，后续复用探针时注意。
  - R-003：I-004 关闭依据为本机 2026-08-07 四宿主探针；CI 或他机环境可用性不在本证据范围（VP-004 只要求一条抽稀 L3/宿主）。

## 边界与后续

- 未覆盖：R2/R3 实施、正式 Release 身份、CI 远端重放。
- 后续：independent cross audit（A-002，provider=grok build / grok-4.5 / thinking-high）→ 响应 findings → R1 检查点 git commit。
