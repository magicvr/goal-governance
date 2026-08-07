---
id: A-001
goal: GOAL-004-r3-configurable-governance-root
title: R3 方案冻结与 governance_root 实现自审
status: recorded
source: self
date: 2026-08-07
scope: R3 方案冻结（D-001/D-002）、config 解析实现、canonical 权威面修订与镜像、C1–C4 测试证据
verdict: pass
version: 0.1.0
---

# A-001 · R3 方案冻结与 governance_root 实现自审

## 结论

`pass`。本审覆盖 R3 方案冻结、实现与验证事实；不替代 independent cross audit（A-002 待写），也不宣称目标关门。

## 证据（可指回）

| 主张 | 证据 |
|------|------|
| I-001/I-002 关闭 | `01-decision/D-001/D-002` accepted；`00-meta` 信息表 closed |
| 解析实现 | `skills/mcp/config.py`（默认 docs / 配置覆盖 / 绝对路径 fail / `..` 越界 fail / 非法 JSON fail / 布局冻结）；`skills/tests/test_mcp_config.py` 9 条全绿 |
| pin 载体 | `.goal-governance.json`（可提交）+ schema `skills/mcp/governance-root.schema.json` 随包分发；doctor 接线（`governanceRootError`） |
| canonical 修订 | `alignment.md`（治理根定义 + MCI 表相对化 + 例外）、`workspace-protocol.md`、根 `AGENTS.md` 0.13.0、templates（workspace-context/goal-folder/charter/vision-plan）、consumer-checklist、standalone-bootstrap |
| 镜像 | `stage_skills_mirrors.py`（6 文件复制）→ `--check` 通过 |
| C4 无裸硬编码 | `docs/tests/test_governance_root_canonical.py` 6 条全绿 |
| 行为源连锁 | v0.13.0 runtime evidence 12 条整批刷新（AGENTS.md 哈希变更；`{SCRATCH}/runtime-refresh-v0130.log`；11/12 首轮 pass + copilot-audit 重试中） |

## Findings

- **required findings：无。**
- **recommended（非阻断）：**
  - R-001：AGENTS.md 0.12.0 → 0.13.0 版本号与仓库当前发布版本（v0.13.0）同名，可能造成「AGENTS 版本 == 发布版本」的混淆；本仓 AGENTS 版本独立演进，CHANGELOG 已注明，接受。
  - R-002：canonical 修订未触及 `consumer-checklist.md` / `standalone-bootstrap.md`（alignment §0.2 的「必须同表」要求）；这两文件仍写 `docs/…`——**已在本审后补改相对化**（见 A-003 响应），本条目撤回。

## 边界与后续

- 未覆盖：Charter 变更（本阶段不改）、VP-002/VP-003 内容演进。
- 后续：independent cross audit（A-002，provider=grok build / grok-4.5 / thinking-high）→ 响应 findings → C5 闭合 → R3 检查点 git commit。
