---
id: D-003
goal_id: GOAL-002-r1-mcp-equivalence-kernel
title: R1 方案冻结 · L2 共享内核范围与 deliveryChannel 合同分列（I-002 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-003 · L2 共享内核与合同分列（2026-08-07）

## 决定

1. **L2 共享内核落点**：`skills/mcp/kernel.py`（随包分发、零依赖纯模块）。
   - `EQUIVALENCE_CHECKPOINTS`：VP-004「R1 四治理入口等价检查点」10 条（V-F-016）作为纯数据。
   - `describe_file_channel(repo_root, governance_root)`：从**真实 File 资产**（`skills/prompts/*.md`、安装脚本、合同）构建通道描述。
   - `describe_mcp_channel(tools)`：从**真实 MCP server** `tools/list` 输出构建同构通道描述。
   - `check_equivalence(file_desc, mcp_desc)`：同一组 L2 断言参数化驱动两通道，返回逐检查点结果。
2. **L2 fixture**：`docs/tests/fixtures/dual-channel/` 最小工作区 fixture（`goal-tree.md` + Root 五件套，按 canonical 模板生成），供 L2 断言核对实例真相、台账边界与五件套形状。
3. **测试落点**（`python -m pytest docs/tests scripts/tests skills/tests` 全量可见）：

   | 文件 | 层 | 内容 |
   |------|----|------|
   | `skills/tests/test_mcp_l1.py` | L1 MCP | 真启动 `skills/mcp/server.py` 进程：`initialize`→`tools/list`→四工具名与参数边界→只读 `tools/call` 角色边界（audit/vision-audit 不改 status） |
   | `docs/tests/test_file_l1.py` | L1 File | 直接驱动真实 File 资产：四入口 prompt 文件 + 安装脚本 + AGENTS 模板 + 合同 files 分列；**不使用 MCP mock** |
   | `docs/tests/test_dual_channel_l2.py` | L2 共享 | 同一组共享断言分别对 file_desc 与 mcp_desc 运行，10 条检查点两通道全部通过 |
   | `scripts/tests/test_contract_delivery_channels.py` | 合同 L1/L2 | contract/schema 校验：`deliveryChannel: files \| mcp` 分列、L1/L2/L3 标注、与既有 File contract 不冲突 |

4. **合同分列**：`docs/contracts/skills-consumer-contract.json`（+ schema）与 `skills-consumer-compatibility-matrix.json`（+ schema）新增 `deliveryChannels` 数组：`files` 与 `mcp` 各一条，含 `status: first-class`、`evidenceLevels`（L1/L2/L3）、`entrypoints`、运行形态说明。既有 `adapters`/`protocol` 语义不变；schema 同步放宽（同一提交内）。
5. **证据分级语义**：L1 = 通道直接证据（分列，mock 不得顶替）；L2 = 共享断言（两通道共用）；L3 = 承诺宿主真探针（抽稀）。分级标注写入合同 `deliveryChannels[].evidenceLevels` 与各测试文件头。

## 未选方案

- L2 fixture 放 `skills/tests/fixtures`：排除——L2 是协议/合同级共享面，放 `docs/tests/fixtures` 便于 File 通道与合同测试共用，且不随消费安装分发。
- 共享内核用第三方断言库：排除——零依赖纯函数，unittest 直接驱动。
- 每个宿主 × 每入口独立 L3 探针矩阵（4×3=12 条）：R1 阶段不要求——VP-004 只要求**每条抽稀 L3 真探针覆盖四入口 dispatch/角色边界**，逐宿主一条即可（见 I-004/D-005）。

## 依据

- VP-004 R1「伴生必达 · 最小统一测试内核」表（L2 共享 / L1 MCP / L1 File / L3 / 合同可读）。
- VP-004「R1 四治理入口等价检查点（V-F-016 · L2 可引用）」10 条。

## 证据 / 结论

- I-002 以本决定关闭（required → closed）。验证动作：`docs/tests/test_dual_channel_l2.py` 与 `scripts/tests/test_contract_delivery_channels.py` 全绿（见 02-execution E-003）。
