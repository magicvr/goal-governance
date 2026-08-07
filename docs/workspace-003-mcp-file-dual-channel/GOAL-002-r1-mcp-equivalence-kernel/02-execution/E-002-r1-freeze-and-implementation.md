---
id: E-002
goal_id: GOAL-002-r1-mcp-equivalence-kernel
title: R1 方案冻结与 MCP/File 双通道实现落盘
status: recorded
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# E-002 · R1 方案冻结与实现（2026-08-07）

## 事实

1. **方案冻结**：D-002（MCP 运行时形态 + 四入口映射）、D-003（L2 内核 + 合同分列）、D-004（independent provider 指定）已落盘并 accepted；I-001 / I-002 / I-003 关闭（required → closed）。
2. **MCP 通道实现**（`skills/mcp/`，随 skills 包分发）：
   - `entries.py`：四入口映射纯数据（名称、关键参数边界、层级、角色边界、台账目标、只读 dispatch 集合；`commit` 不入集）。
   - `server.py`：MCP stdio server（换行分隔 JSON-RPC 2.0），`initialize` / `tools/list` / `tools/call` / `ping`；零第三方运行时依赖；`tools/call` 返回结构化元数据（entrypoint/layer/role/readonly/prompt_path/guidance）。
   - `kernel.py`：L2 共享等价内核（VP-004 V-F-016 十条检查点 + 两通道描述 + 同断言校验）。
   - `README.md`：通道文档。
3. **合同分列**：`docs/contracts/skills-consumer-contract.json`（+ schema）与兼容矩阵（+ schema）新增 `deliveryChannels: files | mcp`（各含 status first-class、evidenceLevels L1/L2/L3、entrypoints、runtime）；`contractFormatVersion` 0.3.0 → **0.4.0**；valid fixtures 同步；`skills/contracts` 镜像已 stage（`--check` 通过）。
4. **测试**（新增 25 条，全绿）：

   | 文件 | 层 | 结果 |
   |------|----|------|
   | `skills/tests/test_mcp_l1.py` | L1 MCP | 通过：真启动 server 进程，四工具名 + 参数边界 + 只读 dispatch 角色边界 + 两次运行一致 |
   | `docs/tests/test_file_l1.py` | L1 File | 通过：真实 File 资产（prompts/host 安装面/脚本/合同 files 分列），无 MCP mock |
   | `docs/tests/test_dual_channel_l2.py` | L2 共享 | 通过：同一组断言驱动 File 与 MCP 两通道描述，10 条检查点全过 |
   | `scripts/tests/test_contract_delivery_channels.py` | 合同 | 通过：schema 校验、镜像一致、legacy 语义不冲突、缺字段 fail |

5. **全量回归**：`python -m pytest docs/tests scripts/tests skills/tests` = 168 passed / 3 skipped / 4 subtests（基线 143 → 168）。
6. **MCP 真启动冒烟**：`tools/list` + 只读 dispatch 连续 2 次运行退出码 0、输出逐字节一致（scratch: `mcp-launch-1.log` / `mcp-launch-2.log`）；pytest 输出捕获（scratch: `pytest-r1.log`）。

## 进度评估

- C1（I-001 关闭 + 映射记录）✅、C2（合同分列冻结）✅、C3（L2 + 分列 L1 实现）✅、C4（self + independent 审计）⏳。
- I-004（P0 宿主 L3 探针环境）待探针结果后关闭。
- 待办：L3 四宿主探针捕获；self 审视落盘；grok build（grok-4.5 / high）independent 意见落盘；required findings 闭合；R1 检查点 git commit。
