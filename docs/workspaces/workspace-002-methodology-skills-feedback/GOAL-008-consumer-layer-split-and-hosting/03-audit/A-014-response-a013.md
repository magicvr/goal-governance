---
id: A-014
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-014
source: self
auditor: 编排主线程 /govern
scope: 响应 A-013（S6 独立关门复审）全部 findings
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-014 · 响应 A-013 独立关门复审（2026-09-13）

## 头字段

- **source**：self
- **auditor**：编排主线程 `/govern`
- **类型 / scope**：response · A-013（S6 独立关门复审，`conditional`，F-001～F-004）
- **verdict**：conditional
- **无冲突**：A-013 与既有 self 意见（A-004～A-009）**无相反 verdict**，不触发 P-004.2；用户已裁决「本轮不开残余」，故 required 只能走 `fixed`。

## 范围与区间

响应 A-013 全部 findings。不宣称 S6 关门、不打 tag、不把 GOAL-008 标 `done`。本轮只做能当场核对闭合的修正。

## Findings 响应

### F-001 · 12 格 dispatch 重捕获不能闭合 A-005 F-001（required / high）

| 字段 | 值 |
|------|-----|
| 处置 | **open（接受指正，撤回「已收窄」的表述）** |
| 证据 | A-013 §3；`A-005-s2-stage-self.md` S2 通过阈值要求「静态谓词 **加上** 至少一个真实宿主对 CE1–CE10 复核」；12 格 JSON 的 `inputSummary` 为 dispatch marker 探针 |
| 修正动作 | `00-meta.md` S6 行的「待完成」列表**恢复并显式列出**「层语义 CE1–CE10 的真实宿主 probe」，并注明 12 格 dispatch 证据**不**满足该项；本条与 A-013 一并作为 S6 关门阻断项 |
| 剩余工作 | 以真实宿主按验收矩阵 §4 corpus 复核（或用户书面 residual 含范围与复审触发——用户当前选择为「不开残余」） |

**不标 `fixed`**：独立会话的判断成立——把「宿主入口能 dispatch」当成「AI 不再混淆层级」是证据越权。

### F-002 · 公开版本台账把未打 tag 的 `v0.13.3` 写成已发布（required / high）

| 字段 | 值 |
|------|-----|
| 处置 | **fixed** |
| 证据 | 修正后：`CHANGELOG.md` 的 `Unreleased` 改为「（未发布；`0.13.3` 为发布候选，须经 merge 进 `main`、annotated tag 指向 merge commit 与 tag workflow 上传后才构成发布声明。）」；`docs/README.md` 「最近发布基线」恢复为 **`v0.13.2`** 为最近**已发布**基线，`v0.13.3` 明确标注**尚未发布**，`快照身份` 改为「**发布候选**（尚未打 tag）」 |
| 说明 | 版本号留在 `CHANGELOG`（D-011 允许）但不再声称已发布；发布身份只在 tag/workflow 之后声明 |

### F-003 · S6 决策/执行台账未入库；HEAD 不能当发布 revision（required / medium）

| 字段 | 值 |
|------|-----|
| 处置 | **fixed（本轮）／部分待办** |
| 已做 | D-012、E-008 落盘；`01-decision.md` 补 D-011/D-012、`02-execution.md` 补 E-008；A-013 落盘为独立条目并登记索引；本轮提交后 HEAD 含全部 S6 事实 |
| 仍待办 | **PR/merge 到 `main` 与 annotated tag**：D-011 §1 要求 tag 指向 main merge commit，属需要远端与用户授权的动作；未完成前不得打 tag |
| 剩余工作 | S6 self 关门意见（本目标 `03-audit/A-015` 待写，需在上述 probe 完成后出具） |

### F-004 · 便利入口守卫未覆盖 MCP 通道 entrypoints（recommended / low）

| 字段 | 值 |
|------|-----|
| 处置 | **fixed** |
| 证据 | `docs/tests/test_file_l1.py::test_convenience_commit_entry_never_joins_the_must_set` 现**遍历全部 deliveryChannels** 断言 `commit` 不在任何通道的 `entrypoints` 中（含 mcp），并保留四入口等式与 files 通道断言 |

## 必改项汇总（响应后）

| Finding | 来源 | 闭合路径 | 状态 | 仍阻断 |
|---------|------|----------|------|--------|
| A-001/F-005（I-006） | independent | D-011 冻结字段；**I-006 状态改为 `frozen`**（见下） | **部分闭合**：字段冻结完成；revision/tag/Release 未产生 → **不标 fixed** | S6 发布 |
| A-005/F-001（宿主层语义） | self | 真实宿主 CE corpus probe | **open**（A-013 F-001 确认） | S6 关门 |
| A-005/F-002（runtime 锚点过期） | self | **本轮完成**：12 份 v0.13.3 证据 + 矩阵/契约改指 + `--check` 12/12 一致 + `--require-ready` 通过 | **fixed** | — |
| A-006/F-001、A-008/F-001（冷启动/升级） | self | 主路径已完成（附件）；**子项（缺列/legacy 不判不完整安装）仍缺** | **open（部分）** | S6 关门 |
| A-009/F-001（`/commit` 宿主调用） | self | 单列宿主调用 + fail-closed 负例 | **open** | S6 关门 |
| A-013 F-001 | independent | 同 A-005 F-001 | **open** | S6 关门 |
| A-013 F-002 | independent | 台账修正 | **fixed** | — |
| A-013 F-003 | independent | 台账入库（tag/merge 另列） | **fixed** | — |
| A-013 F-004 | independent | 守卫补全 | **fixed** | — |

**开放 required 合计 = 4**（A-001 F-005 待发布产出、A-005 F-001/A-013 F-001、A-006+A-008 F-001 子项、A-009 F-001）。**均阻断 S6 关门与发布**；无 residual、无 overruled、无冲突。

## I-006 状态更新

`I-006` 由 `open` → **`frozen`**：版本、tag 语义、资产集合、回归矩阵、cross 覆盖面与证据归属已在 [D-011](../01-decision/D-011-s6-release-scope-freeze.md) 冻结，12 格证据已按该范围重捕获。**`frozen` 不等于 `verified`**：发布产出（merge/tag/workflow/资产核对）尚未发生，因此 A-001 F-005 仍为 open，直到产出可核对。

## 结论与下一步

**verdict：`conditional`。** A-013 的 3 条 required 中 2 条当场 `fixed`（台账身份、台账入库），1 条（层语义宿主 probe）**接受指正并保持 open**，同时恢复其在 S6 待完成列表中的位置；1 条 recommended 已 `fixed`。

**下一步（S6 关门前必须完成）**：
1. 真实宿主按 CE1–CE10 corpus 做 probe（或用户书面 residual）；
2. `/commit` 单列宿主调用 + 一个 fail-closed 负例；
3. 隔离仓「缺列/legacy 不判不完整安装」子项核对；
4. S6 self 关门意见（A-015）；
5. PR → merge 进 `main` → annotated tag 指向 **merge commit** → tag workflow → 逐项核对 Release 资产 sha256。
