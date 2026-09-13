---
id: D-007
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-007
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-007 · S2 层级语义冻结：命名表补全与落位谓词（2026-09-13）

**状态**：accepted

**触发**：S1 盘点（[I-001 结论](../01-decision/D-004-s1-inventory-acceptance.md)）确认三类混淆的根因：三处命名表缺**子目标**与 **VP 内阶段结构**两行、`总路线图` 在 canonical 无指称、消费端安装的规则面完全没有命名消歧表、目标/愿景模板无对应槽位、机器层只判 `roadmap.md` 存在。S2 需给出可执行判定谓词并落地。

## 决定

### 1. 命名表补全为六类（三处命名面同表）

**组合编排 / 纲领路线图 / 阶段计划 / 意图（VP）/ 子目标 / VP 内阶段结构**。落点：

| 命名面 | 位置 | 性质 |
|--------|------|------|
| canonical 全文 | `docs/architecture/principles.md` §6.4 | 权威（stage 白名单 → 镜像） |
| 规则权威 | `docs/vision/alignment.md` §0.3 | 权威（stage 白名单 → 镜像） |
| 生产仓规则入口 | `AGENTS.md` §6e | 手维 |
| 消费端规则面 ×3 | `skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md` §6e.1 | 手维，非 stage 镜像 |

### 2. 落位谓词（8 条最小充分条件）

内容**授权或改变决策** → 愿景层（Charter / 组合编排）；内容是**已落盘 VP** 的意图、方向级退出判据、绑定或关门记录 → 愿景层（该 VP 正文）；内容划分**某 Root/大目标**的纲领阶段 → 实现层（该目标 `00-meta`/`01-decision`）；内容是**某阶段内方案** → 阶段计划（非树节点）；内容是**可独立验收、需要 `parent` 与五件套**的交付节点 → 子目标。层级错位（fail closed）：①把 VP/Charter/愿景文件当目标节点、`parent` 或 Goal 状态源；②在愿景层写可执行纲领阶段、子目标编号、Goal status 或 progress%；③在目标层复写第二套愿景边界。

**判定对象是职责与权威，不是节点数量**（响应 A-003 F-007）：一区一 Root 一 VP、多 VP 绑同区、0 区 `active` VP、把实施方案写进 `01-decision` 均**合法**。

### 3. 术语映射

外部口语「**总路线图**」= 愿景层组合编排索引 `{governance_root}/vision/roadmap.md`；**不是**目标层纲领路线图。已在四类文件写明，并在 principles §6.4、alignment §0.3、AGENTS §6e、消费端 §6e.1 建立映射。

### 4. VP 内阶段结构受限期

VP **可以**写波次内**方向级**阶段（先后与退出方向），**不得**写：可执行纲领阶段、细任务、子目标编号、Goal status、progress%。这解决了 S1 发现的 in-repo 先例冲突（`docs/vision/plans/VP-004` 的「方向级路线图」与 `workspace-003` Root 的同名同标签纲领路线图并存）——**规则**现在唯一：可执行纲领路线图只属于某个 Root/大目标。**实例改写**不在 S2 范围（`docs/vision/plans/VP-004` 与 `workspace-003` Root 的措辞属 S3/后续实例整理，且不阻断本目标验收）。

### 5. 模板槽位

新增 `docs/templates/vision/roadmap.md`（组合编排骨架，`status` 列显式标注为派生投影、禁止门禁用途）；`docs/templates/goal-folder/00-meta.md` 新增「纲领路线图」槽位（含 P-001 谓词提示与层级边界）；`docs/templates/goal-folder/01-decision.md` 新增「纲领路线图与阶段计划」槽位；`docs/templates/vision/vision-plan.md` 新增「方向级阶段结构（可选 · 受限）」；`docs/templates/README.md` 同步目录与层级说明。全部属 `docs/templates/**` → 同轮 stage（C6）。

### 6. 机器层防再犯

- `docs/tests/test_vision_protocol.py` 新增 `LayerNamingTests`（5 项）：命名面必须含六类概念、principles 必须含落位谓词与「总路线图」映射、alignment 必须含口语映射与派生投影权威、VP 模板不得开可执行纲领路线图节且必须保留受限期、roadmap 模板必须存在且索引行不得携带 progress、目标模板必须提供纲领路线图与阶段计划槽位。
- `skills/tests/test_skills_orchestrator.py` 新增 `test_layer_naming_disambiguation_ships_to_rule_surfaces`：三个消费端规则面必须含 §6e.1 与六类概念、`总路线图` 映射、节点数量守卫、以及「VP 不是目标节点」守卫。

### 7. 不做什么

- **不**改安装器、updater、契约（S4/S5）。
- **不**动 `docs/vision/roadmap.md` 的列结构（S3）。
- **不**改写 `docs/vision/plans/VP-004`、`workspace-003` Root、`docs/vision/charter.md` 的实例措辞（S3 / 后续实例整理）。
- **不**把新术语写入 `docs/contracts/**`（消费契约的入口语义在 S5 才处理；S2 不引入契约面变更）。
- **不**宣称「AI 已不再混淆」：本轮只提供静态可核对的谓词与 corpus；宿主级 AI 行为证据在 S6 cross 回归。

## 为什么

- 命名表三处不同步是「同一规则多落点」的典型漂移源；把六类一次对齐、并用测试守卫消费端规则面，比只改 canonical 更能阻止复发（消费端才是 AI 第一入口）。
- 落位谓词用「职责/权威」而非「节点数量」，直接消除 A-003 F-007 指出的误判风险（把合法的一对一结构判为失败）。
- 受限期写进 VP 模板而非只在原则里说一句，才能让「VP 里能写到什么程度」在写文件时就被拦住。
- 不宣称行为已变，是为了避免把静态谓词当作行为证据（S1 盘点的残余不确定性之一）。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 只改 `principles.md`，不动消费端规则面 | 消费端规则面才是 AI 现场入口；S1 已证实那里一个概念都没定义 |
| 新增第九个概念「总路线图」作为正式术语 | 它是消费方口语，不是新工件；正式化会制造第二套命名 |
| 把「子目标」也写进 §6.4 命名表之外的独立章节 | 命名表是唯一消歧入口；分散会再次产生多落点漂移 |
| 直接改写 VP-004 / workspace-003 实例措辞 | 属 vision 实例与另一工作区目标记录；S2 改规则即可，实例整理留 S3 或后续目标，越区改写风险更高 |
| 用真实宿主 probe 作为 S2 的通过证据 | 需要三宿主真实调用与网络；S2 先冻结谓词与静态 corpus，宿主行为证据并入 S6 cross 回归（并在验收矩阵 §3 S2 行注明） |

## 影响

- canonical：`principles.md` §6.4/§6.5/P-001、`alignment.md` §0.3/§1；模板 5 个文件；`AGENTS.md` §6e。
- 镜像：`skills/core/docs/architecture/principles.md`、`skills/core/docs/vision/alignment.md`、`skills/core/docs/templates/**`（含新增 `vision/roadmap.md`）。
- 测试：`docs/tests/test_vision_protocol.py`、`skills/tests/test_skills_orchestrator.py`；`skills/tests/test_skills_orchestrator.py` 的 templates README 版本断言同步为 `0.10.0`。
- **证据时效**：改动根 `AGENTS.md` 使 `docs/releases/runtime/v0.13.2/` 的 12 份宿主证据 `behaviorSources` 全部过期（`capture_runtime_evidence.py --check` 报 12 项 stale）。按 S6 冻结的发布范围处理：S2 不改写历史证据，重捕获并入 S6（见 [E-004](../02-execution/E-004-s2-layer-semantics.md)）。
