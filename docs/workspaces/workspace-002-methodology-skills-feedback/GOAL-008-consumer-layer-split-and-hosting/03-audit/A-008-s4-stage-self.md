---
id: A-008
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-008
source: self
auditor: 编排主线程 /govern
scope: S4 消费仓 AGENTS.md 受管标记块共存 · 安装器/updater/负例
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-008 · S4 阶段自审（2026-09-13）

## 头字段

- **source**：self
- **auditor**：编排主线程 `/govern`
- **类型 / scope**：stage · S4 共存模型 A 的落地（安装器 bash/PS、updater、共享合并实现、负例）
- **verdict**：conditional

## 范围与区间

- covered：D-009 的实现面逐项；fail-closed 边界；迁移兼容；回归结果；未实现项的登记。
- excluded：真实消费仓升级实测（S6 前）；`docs/` 归属可配置化；`/commit`（S5）；发布与版本基线（S6）。
- 未运行：真实消费仓冷启动/升级端到端（仅有隔离临时仓端到端与 PowerShell 隔离安装测试）。

## 成果与证据

| 主张 | 证据 |
|------|------|
| 合并实现唯一化（安装器 + updater 共用） | `skills/agents_merge.py`；`skills/update.py` 导入 `merge_agents_text`；`skills/install.sh`/`install.ps1` 调用同一 CLI |
| 区间外字节永不被改写 | `test_consumer_content_outside_block_is_preserved`；端到端 `consumerKept=True` |
| 半写标记 fail closed | `test_half_written_markers_fail_closed`、`test_cli_reports_fail_closed_on_malformed_target` |
| 无 Python 时不覆盖消费方规则 | `merge_agents_file`（bash）/`Merge-RuleAgentsFile`（PS）分支：已存在且内容不同 → 报错退出 |
| 根 `AGENTS.md` 不再是「完全托管文件」 | `test_managed_pairs_exclude_root_agents`；`scripts/tests/test_skills_update.py` 7 OK |
| 幂等 | 合并幂等断言；`merge_root_agents` 第二次 `unchanged`；PowerShell 隔离安装 PASS |
| 回归全绿 | skills 89 OK、docs 62 OK、scripts 除既有 release_evidence 证据过期项外全绿（见 F-002） |

## Findings

### F-001 · 真实消费仓升级/冷启动未实测

| 字段 | 值 |
|------|-----|
| level | **required** |
| status | open |
| evidence | [E-006](../02-execution/E-006-s4-agents-coexistence.md)「事实边界」；[A-006](A-006-s3-stage-self.md) F-001 同源 |
| closure | S6 前在隔离仓按 `standalone-bootstrap.md` 与真实升级路径各跑一次，核对：消费方规则保留、区间刷新、缺列/残留不判不完整安装、无半写状态 |
| 影响门禁 | **不阻断 S5**；阻断 S6 发布与「消费仓共存已实测」的宣称 |

### F-002 · `scripts/tests/test_release_evidence.py` 期望仍为红（证据锚点过期）

| 字段 | 值 |
|------|-----|
| level | **required**（延续 A-005 F-002） |
| status | open |
| evidence | `docs/releases/runtime/v0.13.2/` 12 份证据在 S2 改根 `AGENTS.md` 后过期；S4 亦改动了三个规则源面，故重捕获必须与 S6 冻结的 revision 一致 |
| closure | S6 在 I-006 冻结的 revision 上重捕获 |
| 影响门禁 | 阻断 S6 发布；不阻断 S5 |

### F-003 · 无 Python 环境下 shell 安装器不做标记块拆分

| 字段 | 值 |
|------|-----|
| level | recommended |
| status | open（设计边界，已 fail closed） |
| evidence | `skills/install.sh` 的 `merge_agents_file` 分支；[D-009](../01-decision/D-009-s4-agents-coexistence.md) §4 |
| closure | 若需纯 shell 合并，另行立项；当前以「拒绝覆盖 + 明确提示」兜底 |
| 影响门禁 | 无 |

### F-004 · 端到端验证期间误以仓库根为目标运行安装器

| 字段 | 值 |
|------|-----|
| level | recommended |
| status | **fixed** |
| evidence | [E-006](../02-execution/E-006-s4-agents-coexistence.md)「事实边界」；根 `AGENTS.md` 已 `git checkout --` 恢复，S2 内容经抽查仍在 |
| closure | 已恢复并在本条与 E-006 留痕；后续同类验证一律先 `Push-Location` 到临时目标 |
| 影响门禁 | 无（未进入提交） |

## 必改项汇总

| Finding | 来源 | 闭合路径 | 状态 | 仍阻断 |
|---------|------|----------|------|--------|
| A-001/F-005 | independent | — | open | S6 发布 |
| A-005 F-001（宿主行为证据） | self | S6 cross 回归 | open | 「不再混淆」宣称、S6 |
| A-005 F-002 / 本审 F-002（runtime 证据） | self | S6 重捕获 | open | S6 发布 |
| A-006 F-001 / 本审 F-001（冷启动与升级实测） | self | S6 前隔离仓实测 | open | S6 发布 |
| A-004 F-001（I-003 选型） | self | **已由用户裁决 D-009 闭合** | **fixed** | — |

**开放 required 合计 = 4**；无冲突；无 residual / overruled。均**不阻断 S5**。

## 与既有意见的异同

- 与 **A-007（independent，pass）** 同向：其 4 条 S6 前须闭合项中，I-003 选型已由 D-009 闭合，其余 3 项与本审 F-001/F-002 一致。
- A-007 明确要求「不要因本审 pass 放行 S4」——本阶段是在用户裁决 D-009 之后才实施，未以 A-007 作为 S4 放行依据。
- 无相反 verdict。

## 结论与下一步

**verdict：`conditional`。** S4 退出条件已满足：共存模型已由用户选定（A）、实现落地、保护消费方既有规则的负例通过、完整安装 MUST 未新增、fail-closed 边界明确。开放 required 4 项**均不阻断 S5**，但 S6 前必须闭合。

**下一步**：按 [D-006](../01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md) 判定，S4 关闭后串行进入 **S5**（默认 `/commit` 便利入口），其 owned paths 与「默认安装但不入必达集」表达位已冻结。
