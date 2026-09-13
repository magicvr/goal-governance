---
id: E-004
goal: GOAL-008-consumer-layer-split-and-hosting
doc: execution
title: S2 双层路线图语义拆分实施
status: recorded
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# E-004 · S2 双层路线图语义拆分（2026-09-13）

## 事实

- **范围**：GOAL-008 纲领 **S2**。前置：S1 完成（[E-003](E-003-s1-inventory.md)）、I-005 provider 已指定、A-001 F-002/F-003 已闭合。
- **用户指令**：本会话目标「推进工作区 2，目标 8，直到顺利关门」；S1 关门后按路线图进入 S2。
- **方案冻结**：[D-007](../01-decision/D-007-s2-layer-semantics-freeze.md)。

## 产物（逐项）

### 1. canonical 规则

| 文件 | 改动 |
|------|------|
| `docs/architecture/principles.md` | §6.4 命名表由 4 类扩为 **6 类**（新增「子目标」「VP 内阶段结构」）并新增**落位谓词 8 条**与「判定对象是职责与权威」守卫、「总路线图」口径；§6.5 VP 最小完备新增**受限期**；P-001「记录位置」新增层级范围限定 |
| `docs/vision/alignment.md` | §0.3 命名表新增「子目标」「VP 内阶段结构」「总路线图（口语）」并补判定谓词、层级错位清单、状态/跟踪权威与派生投影规则；§1 类型与禁止新增「组合编排索引」行、VP 行补禁止项 |
| `AGENTS.md` | §6e 命名表由 4 类扩为 6 类；新增层级判定谓词、层级错位、节点数量守卫、`总路线图` 映射与派生投影口径（手维面） |
| `skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md` | 新增 **§6e.1 层级命名与判定谓词（防「路线图」混淆）**：6 类命名表 + `总路线图` 映射 + 3 条层级错位谓词 + 节点数量守卫 + VP 状态权威口径（三处同文） |

### 2. 模板

| 文件 | 改动 |
|------|------|
| `docs/templates/vision/roadmap.md` | **新增**：组合编排索引骨架；`status` 列标注为「派生投影」，禁止门禁用途；含 legacy 迁移提示 |
| `docs/templates/vision/vision-plan.md` | 新增「方向级阶段结构（可选 · 受限）」节，明列可写/禁写 |
| `docs/templates/goal-folder/00-meta.md` | 新增「纲领路线图（P-001 · 大目标适用）」槽位；派生进度说明补「只选一处 progress 来源」 |
| `docs/templates/goal-folder/01-decision.md` | 新增「纲领路线图与阶段计划（按需）」槽位 |
| `docs/templates/README.md` | 目录说明登记 roadmap 模板与新增槽位；使用边界补层级命名与判定谓词；版本 `0.9.0 → 0.10.0` |

### 3. 镜像与测试

- `python scripts/stage_skills_mirrors.py`：`checked_pairs: 37`、`copied: 5`（含新增 `skills/core/docs/templates/vision/roadmap.md`）；`--check` = `ok: skills mirrors match docs/`。
- `docs/tests/test_vision_protocol.py`：新增 `LayerNamingTests`（5 项断言）。
- `skills/tests/test_skills_orchestrator.py`：新增 `test_layer_naming_disambiguation_ships_to_rule_surfaces`；`test_core_d004_mirror_is_complete` 的 templates README 版本断言更新为 `0.10.0`，并新增 vision roadmap 模板镜像一致性断言。

## 验证结果（可复现）

| 命令 | 结果 |
|------|------|
| `python scripts/stage_skills_mirrors.py --check` | ok：37 对镜像一致（copied 0） |
| `python -m unittest skills/tests/test_skills_orchestrator.py` | **43 tests OK** |
| `python -m unittest discover -s docs/tests -p 'test_*.py'` | **56 tests OK** |
| `python -m unittest skills/tests/test_consumer_surface_relativeization.py skills/tests/test_mcp_l1.py` | **25 tests OK** |
| `git diff --check` | 洁净（0 命中） |

### probe corpus 执行情况（[验收矩阵](../attachments/s1-acceptance-matrix.md) §4）

| case | 本轮可核对证据 | 状态 |
|------|----------------|------|
| CE1 一区一 Root 一 VP 合法 | 谓词「判定对象是职责与权威，不是节点数量」+ 消费端守卫测试 | 静态可核对 |
| CE2 「更新愿景总路线图」 | 四处文档的 `总路线图` 映射；`LayerNamingTests` 断言 | 静态可核对 |
| CE3 VP 内能否写方向级阶段 | VP 模板受限期（可写方向级、禁写可执行纲领阶段） | 静态可核对 |
| CE4 VP 与 Root 同名同标签 | 规则唯一化（可执行纲领路线图只属 Root）；**实例（VP-004 / workspace-003）未改写** | 规则已定；实例留 S3 |
| CE5 VP 当子目标 | principles §6.4/§6.5 禁止项 + 模板守卫 + 消费端守卫 | 静态可核对 |
| CE6 roadmap 跟踪表进目标文件 | alignment §1「组合编排索引」行 + roadmap 模板禁止门禁用途 | 静态可核对 |
| CE7 多 VP 绑同区合法 | 谓词明列「多 VP 绑同区」合法 | 静态可核对 |
| CE8 0 区 `active` VP | 谓词明列合法；空转规则仍在 alignment §5.1 | 静态可核对 |
| CE9 实施方案写进 `01-decision` | §6.4 命名表「阶段计划」行 + 目标模板槽位 | 静态可核对 |
| CE10 VP status 当 Goal status | alignment §1 类型与禁止 + VP 模板 status 枚举 + 消费端权威口径 | 静态可核对 |

**未做**：真实宿主（claude / grok / copilot）行为探针。S2 **不宣称**「AI 已不再混淆」；宿主级行为证据并入 S6 cross 回归，并在验收矩阵 §3 S2 行注明。

## 证据时效变化（重要）

- 改动根 `AGENTS.md` 使 `docs/releases/runtime/v0.13.2/` 的 **12 份**宿主证据 `behaviorSources` 全部过期：`python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.2` 报 **12 problems**（`behavior source is stale: AGENTS.md`，记录 `95c5611a6a6a…` → 当前 `046bf79795ec…`）。
- 依 S1 冻结的 C6 与 S6 范围：**不改写历史证据快照**；重捕获在 S6（`I-006` 冻结的版本/revision 上，使锚点与发布修订一致）。因此 `scripts/tests/test_release_evidence.py` 的 4 failures / 12 errors 与 `scripts/compatibility_report.py --require-ready` 在本轮**预期为红**，S6 前必须转绿。
- 该失败**不是** S2 引入的回归：其根因是「规则面变更 → 证据锚点过期」这一既有设计要求；已在此登记为 S6 待办。

## 检查点

- owned paths = `docs/architecture/principles.md`、`docs/vision/alignment.md`、`AGENTS.md`、`docs/templates/{README.md,vision/roadmap.md,vision/vision-plan.md,goal-folder/00-meta.md,goal-folder/01-decision.md}`、`skills/AGENTS.template.md`、`skills/install/{claude/AGENTS.md,copilot/copilot-instructions.md}`、`skills/core/docs/**`（stage 产物）、`docs/tests/test_vision_protocol.py`、`skills/tests/test_skills_orchestrator.py`，以及本目标五件套。
- 未使用 `git add -A`。
