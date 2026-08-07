---
id: D-001
goal_id: GOAL-004-r3-configurable-governance-root
title: R3 方案冻结 · governance_root 配置 schema 与解析规则（I-001 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-001 · governance_root 配置与解析规则（2026-08-07）

## 决定

1. **配置载体**：项目配置 **`.goal-governance.json`**（仓库根，可提交）为机器可读 pin：
   ```json
   { "governance_root": "governance" }
   ```
   缺文件或缺字段 → 默认 **`docs`**。schema 随包分发：`skills/mcp/governance-root.schema.json`。
2. **解析规则**（`skills/mcp/config.py::resolve_governance_root`，fail closed）：
   - 值必须为非空字符串；**绝对路径**（`/`、`\`、盘符如 `C:`）→ 明确错误；
   - 含 `..` 段或解析后逃出仓库根 → 明确错误（fail closed）；
   - 合法时返回根名（如 `governance`），根目录 = `<repo>/<root>`。
3. **内部布局冻结**：`{governance_root}` 以下相对布局**不可改**：`vision/`、`workspace-*`、`goal-tree.md`、目标五件套形状、`contracts/` 等保持协议约定；配置只改变根前缀。
4. **接线**：`doctor` 与 MCP server 的 doctor 工具使用解析后的根；`lifecycle` managed 段内容保持 `{governance_root}` 相对叙述（不硬编码 docs）。AGENTS managed 段亦可声明 `governance_root`（叙述性），机器 pin 以 `.goal-governance.json` 为准。
5. **例外**：本 monorepo 生产仓固定 `governance_root = docs`（其自身即生产实例；File 自举权威），配置可缺省。

## 未选方案

- 仅环境变量 pin：排除（VP-004 R3 目标 4：可提交项目配置，避免团队漂移）。
- 支持多根 / 修改内部文件夹名：排除（VP-004 R3 非目标）。

## 依据

- VP-004 R3 目标 1–5；「R3 协议面变更车辆（V-F-013 路径 A）」。

## 证据 / 结论

- I-001 以本决定关闭（required → closed）。验证动作：`skills/tests/test_mcp_config.py`（默认/配置/绝对路径/越界/非法 JSON fail closed）。
