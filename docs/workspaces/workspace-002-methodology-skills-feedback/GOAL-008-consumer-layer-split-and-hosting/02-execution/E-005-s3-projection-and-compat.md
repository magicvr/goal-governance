---
id: E-005
goal: GOAL-008-consumer-layer-split-and-hosting
doc: execution
title: S3 愿景总路线图与 VP 跟踪解耦实施
status: recorded
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# E-005 · S3 愿景总路线图与 VP 跟踪解耦（2026-09-13）

## 事实

- **范围**：GOAL-008 纲领 **S3**。前置：用户裁决 [D-005](../01-decision/D-005-s3-consumer-compat.md)（A1 索引承载投影 + 必须兼容）；S2 完成（[E-004](E-004-s2-layer-semantics.md)）。
- **方案落地**：[D-008](../01-decision/D-008-s3-projection-and-legacy-compat.md)。

## 产物

| # | 文件 | 改动 |
|---|------|------|
| 1 | `docs/vision/roadmap.md` | 列名改 `status（派生投影）`；表前新增「权威与投影」段（权威在 VP frontmatter、投影不得用于门禁、legacy 行/列只作提示）；使用说明改为「先改 VP frontmatter 再刷新投影」并补「列的去留」 |
| 2 | `docs/vision/alignment.md` | MUST 表 roadmap 行补「**不要求任何特定列**」；§0.3 补投影段；**新增 §0.4 组合编排索引的投影与兼容读取**（投影/无列要求/legacy 不得 fail closed/VP frontmatter 优先/骨架复制） |
| 3 | `docs/standalone-bootstrap.md` | §2.3 roadmap 行补「必须按本地 VP 集合重写」；复制示例**移除整文件复制 `roadmap.md`**，改为复制 `templates/vision/roadmap.md` 骨架并重写；补复制后核对要求 |
| 4 | `docs/vision/README.md` | 文件地图标注 roadmap 的投影权威与 plans/ 的权威落点 |
| 5 | `docs/architecture/overview.md` | 组合编排摘要不再复写 VP 状态清单（原漏 VP-004），改为指向 roadmap + plans 并声明投影 |
| 6 | `docs/workspaces/workspace-001-goal-governance/GOAL-001-main-vision/00-meta.md` | 同上漂移修正（原漏 VP-004） |
| 7 | `docs/tests/fixtures/vision/valid-stack/roadmap.md` | 3 列 → 带投影标注的 6 列 fixture |
| 8 | `docs/tests/test_vision_protocol.py` | 新增 `CompositionRoadmapAuthorityTests`（6 项：投影列标注与表头、写入顺序、alignment §0.4 兼容规则、bootstrap 不整文件复制、愿景入口投影权威、两处漂移不得复现） |

## 验证结果（可复现）

| 命令 | 结果 |
|------|------|
| `python -m unittest discover -s docs/tests -p 'test_*.py'` | **62 tests OK** |
| `python -m unittest skills/tests/test_skills_orchestrator.py` | **43 tests OK** |
| `python scripts/stage_skills_mirrors.py` → `--check` | `copied: 2`；`ok: skills mirrors match docs/`（37 对） |
| `git diff --check` | 洁净 |

## S3 通过阈值逐条对照（[验收矩阵](../attachments/s1-acceptance-matrix.md) §2.B）

| 阈值 | 状态 | 证据 |
|------|------|------|
| ① 本仓 `roadmap.md` 无未标注的重复权威字段 | **满足** | 列名 `status（派生投影）` + 表前权威段；`test_production_roadmap_labels_status_column_as_projection` |
| ② `docs/tests/test_vision_protocol.py` 全绿且新增断言生效 | **满足** | 62 tests OK；`CompositionRoadmapAuthorityTests` |
| ③ 消费仓兼容：缺新列/残留旧行**不**触发「不完整安装」 | **规则满足**（真实消费仓实测属 S4/S6） | alignment §0.4 legacy 条款 + MUST 行「不要求任何特定列」；`test_alignment_defines_projection_and_legacy_compatibility` |
| ④ 两处漏 VP-004 的漂移已修正 | **满足** | overview.md + Root `00-meta.md` 改为指针；`test_no_stale_portfolio_status_list_in_overview_or_root_meta` |
| ⑤ `standalone-bootstrap` 不再把生产仓 VP 行带入消费仓 | **满足**（文档级） | 复制示例改为模板骨架；`test_bootstrap_does_not_copy_composition_index_verbatim` |

## 事实边界

- 未执行真实消费仓冷启动复制演练（属 S4/S6 的 consumer 侧证据）；本轮的 ⑤ 是**文档/示例级**修正，未做端到端复现。这一点在 [A-006](../03-audit/A-006-s3-stage-self.md) 中登记为 required finding（S6 前闭合）。
- 未新增 MUST 文件或列；未改 Charter / VP `vision_ref`；未产生 VRev（editorial 级）。
- `docs/vision/plans/VP-004` 与 `workspace-003` Root 的实例措辞未改（规则已唯一）；登记为 A-005 F-003 后续项。

## 检查点

- owned paths = `docs/vision/roadmap.md`、`docs/vision/alignment.md`、`docs/vision/README.md`、`docs/standalone-bootstrap.md`、`docs/architecture/overview.md`、`docs/tests/fixtures/vision/valid-stack/roadmap.md`、`docs/tests/test_vision_protocol.py`、`skills/core/docs/{vision/alignment.md,architecture/overview.md}`（stage 产物）、`workspace-001` Root `00-meta.md`，以及本目标五件套。
- 未使用 `git add -A`。
