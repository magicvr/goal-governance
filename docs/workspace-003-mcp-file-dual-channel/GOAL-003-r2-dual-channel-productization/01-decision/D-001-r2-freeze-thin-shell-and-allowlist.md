---
id: D-001
goal_id: GOAL-003-r2-dual-channel-productization
title: R2 方案冻结 · 薄壳落点与 managed paths allowlist（I-001 关闭）
status: accepted
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
parent: null
---

# D-001 · 薄壳落点与 allowlist（2026-08-07）

## 决定

1. **消费仓薄入口（薄壳）**由两部分构成：
   - `AGENTS.md` 的 **managed 段**：`<!-- goal-governance:begin managed -->` … `<!-- goal-governance:end managed -->`。内容为紧凑治理规则摘要 + 版本/指针；更新/卸载**只改标记内**，标记外用户自有内容逐字节不变。
   - `.goal-governance/` 目录：工具状态（`install.json`：channel、version、installed_at）。
2. **managed paths allowlist** = `{AGENTS.md, .goal-governance}`。MCP lifecycle 工具（install/upgrade/uninstall）**只能**写 allowlist 内路径；任何其他路径（含绝对路径、`..` 越界、`docs/`、`skills/` 等）fail closed 并报明确错误。
3. **默认确认写盘**：install/upgrade/uninstall 的 `confirm` 参数默认 `false`；未显式 `confirm: true` 时拒绝写盘并提示（P-002 消费侧确认语义）。
4. **官方 gitignore 片段**：`skills/mcp/gitignore-fragment.txt`，内容忽略 `.goal-governance/`（薄壳默认不进 git；团队可选项锁 git，文档声明）。
5. **`doctor`**：只读状态工具——governance_root 解析、managed 段存在性与版本、`.goal-governance/install.json` 一致性、薄壳是否被 gitignore、合同存在性。
6. 薄壳 managed 段内容与 `skills/mcp/lifecycle.py` 的 marker 逻辑为**同一真相**；bootstrap PS/bash 内嵌的同构逻辑（`-Channel mcp`）由测试核对两侧 marker 结构一致。

## 未选方案

- 薄壳写 `docs/`、`skills/` 或仓内其他路径：排除（allowlist 外一律 fail closed）。
- 无确认直接写盘：排除（默认确认写盘）。
- 薄壳整体锁进 git 作为默认：排除（默认 gitignore，团队可选）。

## 依据

- VP-004 R2：「AGENTS.md（及等价规则文件）治理相关段落用机器可解析标记包裹，更新/卸载只改标记内」；「默认建议 gitignore（不进仓库）；提供官方 ignore 片段 + `doctor`；允许团队可选将薄壳锁进 git」；「managed paths allowlist；默认确认写盘」。

## 证据 / 结论

- I-001 以本决定关闭（required → closed）。验证动作：`skills/tests/test_mcp_lifecycle.py`（allowlist 拒绝、标记外字节不变、确认门禁）+ bootstrap mcp 通道测试。
