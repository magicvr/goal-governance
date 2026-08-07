---
id: D-002
goal_id: GOAL-003-r2-dual-channel-productization
title: R2 方案冻结 · bootstrap 双入口形态（I-002 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-002 · bootstrap 双入口形态（2026-08-07）

## 决定

1. `scripts/bootstrap/install-online.ps1`（及 `.sh`）新增 **`-Channel files|mcp`** 参数：
   - **`files`（默认）**：现有完整安装行为不变（zip 校验 → 整包 materialize → 包内 install -All → docs/architecture + skills + 宿主面）。既有测试与既有消费路径不受影响。
   - **`mcp`**：薄通道安装——仅 materialize `skills/mcp/**` 与 consumer contract（`skills/contracts/skills-consumer-contract.json` + `.schema.json`），写 `.goal-governance/install.json`（`channel: mcp`），并在消费仓 `AGENTS.md` 写 managed 段（无文件则创建）；**不**安装 File 大包（docs/architecture、prompts 全量等）。运行时为 stdio 进程，**不要求 Docker**。
2. **「推荐 MCP」叙述**：bootstrap README / 脚本 Usage / 对外文档在推荐 MCP 通道的**同屏/同节**声明：File 通道仍为一等发布路径、未被废除、非日落；`-Channel files` 完整安装始终可用（VP-004 Charter 叙事选择 V-F-015）。
3. 生产仓继续 File 自举；File-classic（无 Docker、无 MCP）路径完整可用且测试覆盖。
4. mcp 通道 bootstrap 的 marker/install.json 结构与 `skills/mcp/lifecycle.py` 同构；测试对两侧产物结构做一致性断言。

## 未选方案

- 默认通道改为 mcp：排除——破坏既有消费路径与既有测试；「推荐」留在文档叙述层。
- 在线安装拆成两个独立脚本：排除——单脚本 `-Channel` 参数即双入口，减少维护面。

## 依据

- VP-004 R2：「Bootstrap / 在线安装：双入口文档与脚本路径；可推荐 MCP（遵守叙事选择），保留 file zip 安装」。
- VP-004 Charter 叙事选择（V-F-015）：「推荐 MCP」= 安装/bootstrap 便利推荐，不是废除 File。

## 证据 / 结论

- I-002 以本决定关闭（required → closed）。验证动作：`scripts/tests/test_bootstrap_install_online.py` 扩展 mcp 通道用例 + 既有 files 用例保持全绿。
