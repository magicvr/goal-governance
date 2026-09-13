---
id: GOAL-008-consumer-layer-split-and-hosting
doc: audit
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.9.0
---

# 审计 · GOAL-008

> 本文件是稳定索引和信息核对入口。每条正式意见完整写在 `03-audit/A-NNN-<slug>.md`。
> 未关闭的 required 信息项应作为后续审计 finding 的候选来源，不得被写成“已知”或“已完成”。

## 信息就绪核对（按 scope）

| 核对项 | 状态 | 备注 |
|--------|------|------|
| 影响本 scope 的 I-00N | I-001 / I-002 / I-004 **verified**；I-005 **closed**（provider = grok build / grok-4.6 / effort high）；**I-003 `partially-verified`**（选型待用户裁决，S4 方案冻结前阻断）；I-006 **open**（S6 前冻结） | 不阻断立项与 S2/S3；I-003 未决即阻断 S4 方案冻结 |
| 到期 required 是否已 verified / residual | A-001 F-001～F-004 全 `fixed`，**F-005 open**（I-006，S6 前）；**A-004 F-001（I-003 选型）已由用户裁决 D-009 闭合**；**A-005 F-001/F-002 open**（宿主行为证据、runtime evidence 锚点过期）；**A-006 / A-008 F-001 open**（隔离仓冷启动与真实升级实测）；A-007 无 required（2 recommended 已 fixed） | 开放 required = **4**；均不阻断 S5，S6 前必须闭合 |
| 资料引用（若有）是否固定且用户确认 | 无 | 表空 |

## 意见台账索引

| A-ID | 日期 | source | scope | verdict | 开放 required | 文件 |
|------|------|--------|-------|---------|---------------|------|
| A-001 | 2026-09-13 | independent | design-plan · S1-S6 纲领路线图 | conditional | 5（原文）；响应后开放 3 | [A-001-roadmap-design-plan.md](03-audit/A-001-roadmap-design-plan.md) |
| A-002 | 2026-09-13 | self | 响应 A-001 F-001～F-005 | conditional | 3（F-002、F-003、F-005） | [A-002-govern-response-a001.md](03-audit/A-002-govern-response-a001.md) |
| A-003 | 2026-09-13 | independent | design-plan · D-002 后路线图复审 | conditional | 沿用 3；无新增 required | [A-003-roadmap-reassessment.md](03-audit/A-003-roadmap-reassessment.md) |
| A-004 | 2026-09-13 | self | stage · S1 现状复现与契约冻结 | conditional | 1（本审 F-001：I-003 选型） | [A-004-s1-stage-self.md](03-audit/A-004-s1-stage-self.md) |
| A-005 | 2026-09-13 | self | stage · S2 双层路线图语义拆分 | conditional | 2（宿主行为证据、runtime evidence 锚点过期） | [A-005-s2-stage-self.md](03-audit/A-005-s2-stage-self.md) |
| A-006 | 2026-09-13 | self | stage · S3 愿景总路线图与 VP 跟踪解耦 | conditional | 1（冷启动端到端演练） | [A-006-s3-stage-self.md](03-audit/A-006-s3-stage-self.md) |
| A-007 | 2026-09-13 | independent | S1 盘点基线核验 + S2/S3 修复自洽（grok build / grok-4.6 / high） | pass | 0（2 recommended 已 fixed） | [A-007-independent-cross-review-s1-s3.md](03-audit/A-007-independent-cross-review-s1-s3.md) |
| A-008 | 2026-09-13 | self | stage · S4 消费仓 AGENTS.md 共存 | conditional | 2（真实升级实测、runtime 证据） | [A-008-s4-stage-self.md](03-audit/A-008-s4-stage-self.md) |
| A-009 | 2026-09-13 | self | stage · S5 默认 `/commit` 便利入口 | conditional | 2（宿主实测、runtime 证据） | [A-009-s5-stage-self.md](03-audit/A-009-s5-stage-self.md) |
| A-013 | 2026-09-13 | independent | S6 关门与发布准备（grok build / grok-4.6 / high） | conditional | 3（层语义宿主 probe、台账发布身份、台账入库）+1 recommended | [A-013-independent-s6-close-review.md](03-audit/A-013-independent-s6-close-review.md) |
| A-014 | 2026-09-13 | self | 响应 A-013 全部 findings | conditional | 4（F-002/F-003/F-004 fixed；层语义 probe 保持 open） | [A-014-response-a013.md](03-audit/A-014-response-a013.md) |

## 结论状态

A-001 已由 A-002 响应。F-001、F-004 **fixed**；F-002、F-003、F-005 **open**（分别阻断 S2–S4 冻结/并行与 S6 发布）。S1 只读盘点可继续。`status` / `progress` 未改。独立意见不直接改状态；本响应为编排器 self 侧记录。

A-003 独立复审：总体路线图合理，无需重排；支持上述两项 fixed 结论，三项 required 继续保留。新增 recommended F-006（S1 冻结粒度）、F-007（合法一对一结构的正反例验收），无新 required、无意见冲突。尚未验证实现或发布就绪；响应归 `/govern`。

**2026-09-13 · S1 阶段结果（A-004 self，`conditional`）**：S1 四路只读盘点完成，验收矩阵与 probe corpus 落盘；**A-001 F-002 / F-003 由 D-004 / D-006 合法闭合（`fixed`）**，F-001/F-004 早已闭合；**A-003 F-006 / F-007 分别由 D-003 §3 与矩阵 §4 成对正反例闭合**。开放 required 降为 **2**：A-001 **F-005**（I-006 发布基线，S6 前）与本审 **F-001**（I-003 共存模型选型，S4 方案冻结前）。D-005 记录用户对 S3 权威模型（A1 索引承载投影）与消费仓兼容（不得 fail closed）的裁决。S1 判定关门，`status` 保持 `active`、`progress` **17%**（1/6）；S1 契约的 independent 复审（grok build）待执行，**在此之前不得宣称已获交叉验证**。

**2026-09-13 · S2 阶段结果（A-005 self，`conditional`）**：命名表扩为 **6 类**、落位谓词 **8 条**、`总路线图` 映射四处落盘、VP 内阶段结构受限期、消费端 **§6e.1** 三宿主同文、新增 roadmap 模板与目标/愿景模板槽位；机器守卫测试 2 套。回归全绿（skills 43 / docs 56 / consumer-surface+mcp 25、镜像 37 对、`git diff --check` 洁净）。开放 required **升为 4**：新增本审 F-001（真实宿主行为证据缺失，S6 cross 回归闭合）与 F-002（**根 `AGENTS.md` 变更使 `docs/releases/runtime/v0.13.2/` 12 份证据锚点过期**，`capture_runtime_evidence.py --check` 12 problems；S6 在 I-006 冻结 revision 上重捕获），两项均**不阻断 S3**，但阻断 S6 发布与「AI 已不再混淆」宣称。S2 判定关门 → `progress` **33.3%**（2/6）。

**2026-09-13 · S3 阶段结果（A-006 self，`conditional`）**：按用户裁决的 **A1 索引承载投影** 落地——`roadmap.md` 列名与正文均标注派生投影、权威指向 VP frontmatter、写入顺序改为「先 VP 后投影」；兼容读取规则写入规则权威 alignment **§0.4**（legacy 不得 fail closed、VP frontmatter 优先、MUST 表不要求任何特定列）；`standalone-bootstrap` 不再整文件复制组合编排索引；两处漏 VP-004 的漂移改为指针；新增 `CompositionRoadmapAuthorityTests`（6 项），docs **62 OK**、skills 43 OK、镜像 37 对、`git diff --check` 洁净。**未新增 MUST**。开放 required **升为 5**：新增本审 F-001（骨架复制修正尚无端到端消费仓演练，S6 前闭合）；仍**均不阻断 S4/S5**。S3 判定关门 → `progress` **50.0%**（3/6）。S1/S2/S3 的 independent 复审（grok build）**尚未出具**，不得宣称已获交叉验证。

**2026-09-13 · independent 交叉复审（A-007 · grok build / grok-4.6 / reasoning-effort high · `pass`）**：在**基线快照 `b90b2d8`** 上核对 S1 盘点：抽查 12 条带 `file:line` 的主张**全部一致**，I-001/I-002/I-003（S1 时点）结论**成立**，S3 修复**自洽且未新增「不完整安装」路径**（MUST 表不要求列、新模板未入 MUST、bootstrap 不再整文件复制）。**无 required**；2 条 recommended（`workspace_count` 表述、D-003 把 I-003 写成 verified）已 `fixed`。该意见同时确认 **A-004 F-002 闭合**（S1 交叉验证已出具），并明确要求「不得因本审 pass 放行 S4」——S4 实际在用户裁决 D-009 之后才实施。

**2026-09-13 · S4 阶段结果（A-008 self，`conditional`）**：用户裁决共存模型 **A（受管标记块）**；框架规则进入受管区间、**区间外字节永不改写**、半写标记 fail closed、无 Python 时拒绝覆盖；安装器与 updater 共用 `skills/agents_merge.py`；根 `AGENTS.md` 不再列入 updater 托管文件；三个规则源面加外层受管标记；新增 `scripts/tests/test_agents_merge.py`（12 例）。回归：**skills 89 OK / docs 62 OK / PowerShell 隔离安装 PASS / `git diff --check` 洁净**；scripts 仅剩既有 runtime 证据过期项。**A-004 F-001（I-003 选型）闭合**。开放 required = **4**（A-001 F-005、A-005 F-001/F-002、A-006+A-008 F-001），均不阻断 S5。S4 关门 → `progress` **66.7%**（4/6）。