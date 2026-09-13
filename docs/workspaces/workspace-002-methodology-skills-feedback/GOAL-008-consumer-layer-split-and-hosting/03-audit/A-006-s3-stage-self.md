---
id: A-006
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-006
source: self
auditor: 编排主线程 /govern
scope: S3 愿景总路线图与 VP 跟踪解耦 · 投影/legacy 兼容/骨架复制
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-006 · S3 阶段自审（2026-09-13）

## 头字段

- **source**：self
- **auditor**：编排主线程 `/govern`
- **类型 / scope**：stage · S3 投影标注、legacy 兼容规则、骨架复制修正、漂移修正
- **verdict**：conditional

## 范围与区间

- covered：D-005/D-008 的落地情况；S3 五条通过阈值逐条对照；canonical 与镜像一致性；回归结果；实例未改范围。
- excluded：真实消费仓冷启动演练（consumer 侧证据）；`AGENTS.md`/`docs/` 共存模型（S4）；`/commit`（S5）；版本与发布基线（S6）。
- 未运行：消费仓安装/复制端到端演练、宿主 probe。

## 成果与证据

| 主张 | 证据 |
|------|------|
| 投影标注落在表头与正文 | [E-005](../02-execution/E-005-s3-projection-and-compat.md) §产物 1；`test_production_roadmap_labels_status_column_as_projection` |
| 兼容规则进入规则权威 | alignment §0.4；`test_alignment_defines_projection_and_legacy_compatibility` |
| 骨架复制缺陷修正 | `docs/standalone-bootstrap.md` §2.3；`test_bootstrap_does_not_copy_composition_index_verbatim` |
| 两处漂移修正 | overview.md、workspace-001 Root `00-meta.md`；`test_no_stale_portfolio_status_list_in_overview_or_root_meta` |
| 回归绿 + 镜像一致 | docs 62 OK、skills 43 OK、37 对镜像 ok、`git diff --check` 洁净 |
| 未新增 MUST | [D-008](../01-decision/D-008-s3-projection-and-legacy-compat.md) §6 |

## Findings

### F-001 · 骨架复制修正未做端到端消费仓演练

| 字段 | 值 |
|------|-----|
| level | **required** |
| status | open |
| evidence | [E-005](../02-execution/E-005-s3-projection-and-compat.md)「事实边界」；S3 通过阈值 ⑤ 仅文档级 |
| closure | S6 前完成一次隔离仓冷启动（按 `standalone-bootstrap.md` 步骤）并核对：本地 `roadmap.md` 不含他仓 VP 行、缺列不判不完整安装、legacy 行不阻断推进 |
| 影响门禁 | **不阻断 S4/S5**；阻断 S6 发布与「消费仓兼容已实测」的宣称 |

### F-002 · legacy 兼容只有规则与静态断言，无 reader 实现

| 字段 | 值 |
|------|-----|
| 结论 | **非缺陷，登记为设计边界** |
| level | recommended |
| status | open |
| evidence | S1 盘点（`attachments/s1-inventory-evidence.md` §2.B「机读读取者 = 零」）：无脚本解析该表，故本轮不引入 reader；兼容规则由规则权威 + prompts 读序承担 |
| closure | 若将来引入机读解析（例如发布门禁校验组合编排），须同时实现 legacy 兼容读取顺序并在该目标内验收 |
| 影响门禁 | 无 |

### F-003 · VP-004 / workspace-003 实例仍示范同名同标签双层路线图

| 字段 | 值 |
|------|-----|
| level | recommended |
| status | open（沿用 A-005 F-003） |
| evidence | `docs/vision/plans/VP-004-mcp-file-dual-channel-delivery.md:75`；`workspace-003` Root `00-meta.md:32` |
| closure | 后续实例整理或在该 VP 落一条 editorial 口径说明 |
| 影响门禁 | 无（规则已在 S2 唯一化） |

## 必改项汇总

| Finding | 来源 | 闭合路径 | 状态 | 仍阻断 |
|---------|------|----------|------|--------|
| A-001/F-005 | independent | — | open | S6 发布 |
| I-003 选型（A-004 F-001） | self | 用户裁决 | open | S4 方案冻结 |
| A-005 F-001（宿主行为证据） | self | S6 cross 回归 | open | 「不再混淆」宣称、S6 |
| A-005 F-002（runtime evidence 锚点过期） | self | S6 重捕获 | open | S6 发布 |
| 本审 F-001（冷启动演练） | self | S6 前隔离仓演练 | open | S6 发布 |

**开放 required 合计 = 5**（新增本审 F-001）；无冲突；无 residual / overruled。**均不阻断 S4/S5 实施**；S6 前必须闭合。

## 与既有意见的异同

- 与 D-005（用户裁决）同向：A1 模型 + 必须兼容已按要求落地，未出现 fail closed 路径。
- 与 A-005 同向：S2 F-003（实例措辞）本轮未改，继续登记为 recommended。
- 与 A-003 F-007 同向：本轮改动未涉及节点数量判定。
- 无相反 verdict；A-001 F-002/F-003 的闭合依据（验收矩阵、owned paths）未被本轮修改。

## 结论与下一步

**verdict：`conditional`。** S3 五条通过阈值中 ①②④⑤ 已满足、③ 的**规则**已满足（实测属 S4/S6）；开放 required 5 项均不阻断 S4，但 S6 前必须闭合（冷启动演练、宿主行为证据、runtime evidence 重捕获、I-003 选型、F-005 发布基线）。S3 判定关门 → `progress` **50%（3/6）**。

**下一步**：① 待 independent 复审（grok build）对 S1/S2/S3 一并出意见；② S4 方案冻结**前**必须取得用户对 `AGENTS.md`/`docs/` 共存模型的裁决（候选 A～E）；③ S4 完成后按 D-006 串行进入 S5。
