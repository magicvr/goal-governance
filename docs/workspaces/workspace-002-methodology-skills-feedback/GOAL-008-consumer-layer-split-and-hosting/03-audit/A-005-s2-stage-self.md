---
id: A-005
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-005
source: self
auditor: 编排主线程 /govern
scope: S2 双层路线图语义拆分 · 谓词/命名表/模板/守卫与证据时效
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-005 · S2 阶段自审（2026-09-13）

## 头字段

- **source**：self
- **auditor**：编排主线程 `/govern`
- **类型 / scope**：stage · S2 双层路线图语义拆分；覆盖 D-007 方案冻结、命名表补全、落位谓词、模板槽位、镜像与测试守卫、证据时效变化
- **verdict**：conditional

## 范围与区间

- covered：S2 退出条件逐项（判定谓词落点、固定 corpus、正反例、通过阈值、覆盖的提示词/规则面）；canonical 与镜像一致性；消费端规则面同步；负例与守卫测试；证据时效影响的范围与归属。
- excluded：真实宿主 AI 行为（未跑 probe）；`/commit` 安装面（S5）；消费仓安装行为（S4）；发布与版本基线（S6）。
- 未运行：安装器、宿主 CLI、发布流程。

## 成果与证据

| 主张 | 证据 |
|------|------|
| 命名表 6 类在四处命名面同表 | [D-007](../01-decision/D-007-s2-layer-semantics-freeze.md) §1；`LayerNamingTests` + 消费端守卫测试 |
| 落位谓词 8 条 + 节点数量守卫 | principles §6.4；`test_principles_define_layer_placement_predicate` |
| `总路线图` 术语映射 | principles §6.4 / alignment §0.3 / AGENTS §6e / 消费端 §6e.1；`test_alignment_maps_colloquial_term_and_projection_authority` |
| VP 内阶段结构受理期 | VP 模板「方向级阶段结构（可选 · 受限）」；`test_vision_plan_template_has_no_executable_roadmap_section` |
| 模板槽位与 roadmap 模板 | `docs/templates/vision/roadmap.md` 等 4 处；`test_goal_folder_templates_provide_roadmap_and_phase_plan_slots`、`test_composition_roadmap_template_exists_and_avoids_duplicate_authority` |
| 镜像一致 | `stage_skills_mirrors.py --check` = ok（37 对） |
| 测试绿 | skills 43 OK；docs 56 OK；consumer-surface+mcp 25 OK；`git diff --check` 0 |
| corpus 10 例静态可核对 | [E-004](../02-execution/E-004-s2-layer-semantics.md)「probe corpus 执行情况」 |
| 证据时效变化已登记 | [E-004](../02-execution/E-004-s2-layer-semantics.md)「证据时效变化」；`capture_runtime_evidence.py --check` 报 12 stale |

## Findings

### F-001 · 宿主级 AI 行为证据缺失，S2 通过仅基于静态谓词

| 字段 | 值 |
|------|-----|
| level | **required** |
| status | open |
| evidence | [E-004](../02-execution/E-004-s2-layer-semantics.md)「未做」；[验收矩阵](../attachments/s1-acceptance-matrix.md) §3 S2 行 |
| closure | S6 cross 回归内完成至少一个真实宿主 probe，或由用户书面接受该残余（含范围与复审触发） |
| 影响门禁 | **不阻断 S3**（S3 处理工件落点与迁移）；阻断「AI 已不再混淆」的任何宣称，且 S6 发布前必须闭合 |

### F-002 · 12 份 runtime evidence 锚点过期，producer 门禁当前为红

| 字段 | 值 |
|------|-----|
| level | **required** |
| status | open |
| evidence | `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.2` → 12 problems（`AGENTS.md` 记录 `95c5611a6a6a…` → 当前 `046bf79795ec…`）；`scripts/tests/test_release_evidence.py` 4 failures / 12 errors |
| closure | S6 在 I-006 冻结的 revision 上重捕获（或 per 用户裁决的其它路径）；历史快照不改写 |
| 影响门禁 | **不阻断 S3/S4/S5 的实施**；阻断 S6 发布与任何 `--require-ready` 声明 |

### F-003 · VP-004 / workspace-003 实例仍示范同名同标签双层路线图

| 字段 | 值 |
|------|-----|
| level | recommended |
| status | open |
| evidence | `docs/vision/plans/VP-004-mcp-file-dual-channel-delivery.md:75`；`docs/workspaces/workspace-003-mcp-file-dual-channel/GOAL-001-mcp-file-dual-channel-delivery/00-meta.md:32`（S1 盘点 §2.A 缺口 2/3） |
| closure | S3 实例整理或在 VP-004 落一条口径说明（该 VP 已 `closed`，仅 editorial 措辞，不触发 strategic） |
| 影响门禁 | 无（规则已唯一）；影响先例可读性 |

### F-004 · roadmap 迁移兼容规则尚未落地（S3 范围）

| 字段 | 值 |
|------|-----|
| level | recommended |
| status | open |
| evidence | [D-005](../01-decision/D-005-s3-consumer-compat.md)；S1 盘点 §2.B「消费侧风险」 |
| closure | S3 内落盘兼容读取顺序与 `standalone-bootstrap` 整文件复制修法 |
| 影响门禁 | S3 通过阈值 |

## 必改项汇总

| Finding | 来源 | 闭合路径 | 状态 | 仍阻断 |
|---------|------|----------|------|--------|
| A-001/F-005 | independent | — | open | S6 发布 |
| I-003 选型（A-004 F-001） | self | 用户裁决 | open | S4 方案冻结 |
| 本审 F-001（宿主行为证据） | self | S6 cross 回归 | open | 「不再混淆」宣称、S6 发布 |
| 本审 F-002（证据锚点过期） | self | S6 重捕获 | open | S6 发布 |

**开放 required 合计 = 4**；无冲突；无 residual / overruled。

## 与既有意见的异同

- 与 A-004（self，S1）同向：S1 的 F-003（`总路线图` 无落点）本轮**已由 D-007 §3 闭合**。
- 与 A-003（independent）F-007 同向：成对正反例已写入验收矩阵 §4，并在 S2 谓词中显式守卫「节点数量」。
- 无相反 verdict；A-001 F-002/F-003 的闭合不因本轮改动被推翻（验收矩阵与 owned paths 未被修改）。

## 结论与下一步

**verdict：`conditional`。** S2 退出条件已满足：判定谓词与 prompts/模板落地、corpus 固定、正反例与通过阈值可核对、覆盖的规则/提示词面已列；canonical 与镜像一致、四套回归绿。开放 required 4 项均**不阻断 S3**（三项属 S6/发布范围，一项属 S4 前置裁决）。

**下一步**：① 待 independent 复审（grok build，A-006）对本阶段与 S1 一并出意见；② 进入 S3（D-005 已定 A1 模型与消费仓兼容口径），按 S3 通过阈值落盘兼容读取规则与 bootstrap 修法；③ S4 前取得 I-003 共存模型裁决。
