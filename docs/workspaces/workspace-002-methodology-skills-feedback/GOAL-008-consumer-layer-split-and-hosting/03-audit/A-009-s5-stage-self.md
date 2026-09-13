---
id: A-009
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-009
source: self
auditor: 编排主线程 /govern
scope: S5 默认 /commit 便利入口 · 宿主面/契约边界/负例
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-009 · S5 阶段自审（2026-09-13）

## 头字段

- **source**：self
- **auditor**：编排主线程 `/govern`
- **类型 / scope**：stage · S5 便利入口的安装面、契约位置与 fail-closed 负例
- **verdict**：conditional

## 范围与区间

- covered：D-010 的实现面逐项；必达集未被污染；四宿主面产出；壳文本契约；回归结果；未实现/未实测项登记。
- excluded：真实宿主调用 `/commit` 的行为验证（S6）；发布与版本基线（S6）；消费仓升级实测（S6）。
- 未运行：宿主 CLI 调用 `/commit`；真实提交场景的负例实测。

## 成果与证据

| 主张 | 证据 |
|------|------|
| 四宿主面默认安装 | [E-007](../02-execution/E-007-s5-commit-entry.md)；`test_convenience_commit_surface_ships_for_every_host`；端到端四路径 `True` |
| 必达集未被污染 | `test_convenience_commit_entry_never_joins_the_must_set`（`ENTRYPOINT_NAMES` 仍四入口；契约 `hostEntrypoints`/`files.entrypoints` 无 `commit`）；未改契约 JSON/schema |
| 壳文本含 fail-closed 契约 | `test_convenience_commit_contract_forbids_unsafe_staging`（禁 `git add -A`、owned path、fail closed、非必达边界、不 push） |
| 输出分离必达与便利 | `skills/install.sh` / `install.ps1` 两行输出；端到端日志含 `NOT a governance-must entrypoint` |
| 回归 | docs 65 OK、skills 89 OK、PowerShell 隔离安装 PASS、镜像 37 对一致、`git diff --check` 洁净；scripts 仅剩既有 runtime 证据过期项 |

## Findings

### F-001 · `/commit` 未做真实宿主行为验证

| 字段 | 值 |
|------|-----|
| level | **required** |
| status | open |
| evidence | [E-007](../02-execution/E-007-s5-commit-entry.md)「事实边界」；[验收矩阵](../attachments/s1-acceptance-matrix.md) §3 负例 12/13 |
| closure | S6 cross 回归内至少一个宿主实际调用 `/commit`（含一个 fail-closed 负例，如无改动或越界），并把该便利入口单列为**非必达**证据，避免污染必达矩阵 |
| 影响门禁 | **不阻断 S6 的回归与发布准备**；阻断「`/commit` 已实测可用」的宣称与 S6 关门 |

### F-002 · 契约层未新增机器可读的便利入口登记位

| 字段 | 值 |
|------|-----|
| level | recommended |
| status | open（设计取舍，见 [D-010](../01-decision/D-010-s5-commit-entry.md) §2） |
| evidence | 未改 `docs/contracts/skills-consumer-contract.json`；边界由 README + 断言表达 |
| closure | 若将来消费面需要机读列举便利入口，另行立项并处理 schema 兼容 |
| 影响门禁 | 无 |

### F-003 · `scripts/tests/test_release_evidence.py` 仍红（延续 A-005 F-002）

| 字段 | 值 |
|------|-----|
| level | **required**（延续） |
| status | open |
| evidence | `python -m unittest discover -s scripts/tests`：4 failures / 12 errors，全部为 runtime 证据锚点过期 |
| closure | S6 在 I-006 冻结的 revision 上重捕获 |
| 影响门禁 | 阻断 S6 发布 |

## 必改项汇总

| Finding | 来源 | 闭合路径 | 状态 | 仍阻断 |
|---------|------|----------|------|--------|
| A-001/F-005 | independent | — | open | S6 发布 |
| A-005 F-001 / 本审 F-001（宿主行为证据） | self | S6 cross 回归 | open | 「不再混淆」「/commit 可用」宣称、S6 |
| A-005 F-002 / 本审 F-003（runtime 证据） | self | S6 重捕获 | open | S6 发布 |
| A-006 / A-008 F-001（隔离仓冷启动与升级实测） | self | S6 前实测 | open | S6 发布 |

**开放 required 合计 = 4**（与 S4 后持平：S5 新增 1 项、原 A-004 F-001 已在 S4 闭合）；无冲突；无 residual / overruled。

## 与既有意见的异同

- 与 **A-007（independent，pass）** 同向：其「S6 前须闭合」四项中，I-003 选型已闭合，其余三项与本审 F-001/F-003 及 A-006/A-008 F-001 一致。
- 与 **D-002 §4 / VP-004 入口面**一致：`/commit` 仍为便利可选，未被升格为 MUST 或必达。
- 无相反 verdict。

## 结论与下一步

**verdict：`conditional`。** S5 退出条件已满足：四个已支持宿主默认产出便利入口、非完整安装 MUST、非治理入口必达、非 checkpoint 替代、fail-closed 负例写入壳文本；必达集未被污染且有机读守卫。开放 required 4 项**均属 S6 范围**。

**下一步**：进入 **S6**（回归、审计与发布）。S6 必须按序处理：
1. **I-006 冻结**（版本、tag/revision、资产清单、回归矩阵、cross 覆盖、consumer vs producer 证据归属）——闭合 A-001 F-005；
2. 在冻结 revision 上**重捕获 runtime evidence**（12 份矩阵证据）——闭合 A-005 F-002；
3. 隔离仓**冷启动与升级实测**——闭合 A-006/A-008 F-001；
4. 至少一个宿主 **probe/行为证据**（含 `/commit` 便利入口单列）——闭合 A-005 F-001/A-009 F-001；
5. cross 关门审计（self + grok build）后判定发布与 `done`。
