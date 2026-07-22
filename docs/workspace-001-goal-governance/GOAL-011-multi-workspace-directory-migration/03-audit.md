---
id: GOAL-011-multi-workspace-directory-migration
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-21
version: 0.5.0
---

# 审计 · GOAL-011

## A-001 · 多工作区目录迁移关门自审（2026-07-20）

- **source**：self
- **auditor**：`/govern`（Codex）
- **类型**：close-out
- **scope**：GOAL-011 的工作区根迁移、共享资料候选索引、消费者路径同步与回归验证。
- **verdict**：pass

### 成果（有证据）

| 成功标准 | 状态 | 证据 |
|----------|------|------|
| 目标迁入唯一显式工作区根 | 已完成 | `workspace-001-goal-governance/workspace.md`、`goal-tree.md`、11 个 `GOAL-*`；迁移断言通过。 |
| core、Skills、Web 使用工作区 scope | 已完成 | 工作区协议、模板/镜像、`GoalsRepository.DEFAULT_WORKSPACE_DIR` 与回归测试。 |
| 共享资料候选库存可重建 | 已完成 | `docs/shared-materials/`、`rebuild_shared_materials_index.py`、6 项索引测试。 |
| 不自动确认资料或建立第二状态 | 已完成 | 协议第 5 节、索引 `inventoryOnly: true` 和脚本测试。 |
| 路径与回归验证 | 已完成 | docs 10、Skills 32、scripts 36、Web 21 项通过；`git diff --check` 通过。 |

### Findings

本 scope 没有开放 required finding。Windows 环境未授予符号链接创建权限，两个既有/新增的符号链接负向用例均被明确跳过，未被计为通过；其它路径 containment 与索引拒绝测试通过。

### 信息门禁

I-001～I-003 已有迁移、实现与测试证据，允许关门。I-004 为 non-blocking/open，明确属于 GOAL-009 的多工作区产品模型和导航工作，不阻断本目标。

### 结论

目录迁移和共享资料索引骨架符合 D-001 与所有成功标准。GOAL-011 可标记为 `done / 100%`；这不关闭 GOAL-009 的 I-009/I-010、F-003/F-004 或任何 Web CRUD/AI 读取门禁。

## A-002 · 已关门目标的目录迁移回归影响独立审计（2026-07-20）

- **source**：independent
- **auditor**：Codex `/audit`
- **类型**：ad-hoc
- **scope**：GOAL-011 从 `docs/goals/` 到 `docs/workspace-001-goal-governance/` 的目录迁移，以及它对已关门 GOAL-002～GOAL-010 的产物完整性、当前消费者与闭环证据的影响。
- **verdict**：pass

### 成果与证据

- [02-execution.md](02-execution.md#2026-07-20--显式工作区迁移资料索引与验证完成) 记录了单一显式工作区根、`docs/goals/` 已不存在、消费者默认根及相关测试已同步；[workspace.md](../workspace.md) 与 [workspace-protocol.md](../../architecture/workspace-protocol.md) 现在一致地固定当前 canonical scope。
- 本轮复跑迁移相关回归：`docs/tests` 10 项、Skills 32 项、从 `web/` 运行的 Web 21 项、`scripts/tests` 36 项均通过；两个 Windows 符号链接负向用例显式 skipped，未误记为通过。
- 当前 Web 默认根和断言分别见 `web/services/goals_repo.py:45-51`、`web/tests/test_goals_repo.py:23-26`；协议测试还固定 `canonical_scope: docs/workspace-001-goal-governance/`。未发现丢失的已关门目标文件、失效的当前读取路径或由迁移导致的测试失败。

### Findings

#### F-001 · recommended / medium · open — 处理“当前规范”与迁移前历史记录之间的路径语义错位

- [goal-tree.md](../goal-tree.md#2026-07-20--阶段-6-web-工作台规划) 仍称 `docs/goals/` “继续是 canonical 真相源”，而同一文件的 GOAL-011 段已说明迁移到 `docs/workspace-001-goal-governance/`；这会误导后续消费者，但不是当前运行路径失效的证据。
- GOAL-010 `02-execution.md:24` 与已关门 GOAL-002～GOAL-008 中的旧路径主要是迁移前事实、设计快照或宿主运行证据。例如 GOAL-004 `01-decision.md:37,80,110` 描述的是当时的数据模型，GOAL-008 `02-execution.md:42` 是创建时的时间线事实。不能为了表面一致性改写这些历史证据。
- 建议 `/govern` 建立最小的迁移说明/现时入口修正：更新仍作为当前规范的叙述，必要时给历史记录加迁移前语境；不要批量改写附件、历史运行证据或已关门目标状态。

### 信息门禁与关闭边界

I-001～I-003 的迁移、索引和消费者适配证据仍可核对；I-004 继续是 `non-blocking / open` 的 GOAL-009 产品模型/导航问题。本审计没有把资料候选库存、路径扫描或历史运行证据当成用户确认的事实、共享资料引用或 GOAL-009 门禁关闭证据。

### 结论与建议

GOAL-011 没有对其他已关门目标产生需要回归修正的功能性影响；无需重开或修改它们的状态。F-001 是应由 `/govern` 排期的非阻塞文档一致性修正，完成前也不影响本目标既有的 `done / 100%` 事实。

### 声明

本独立审计仅追加意见；未修改任何目标的 `status`、`progress`、决策正文或 `goal-tree.md` 状态。

## A-003 · 关门后回归交叉审计（迁移产物与 F-001 状态）（2026-07-21）

- **source**：independent
- **auditor**：Grok `/audit`
- **类型**：close-out / ad-hoc 回归
- **scope**：GOAL-011 成功标准与 D-001 是否仍可核对；共享资料候选索引是否仍 fail-closed；A-002 F-001 是否关闭；不把本目标重开为实现目标。
- **verdict**：pass

### 范围与区间

| 项 | 值 |
|----|-----|
| 工作区 | `workspace-001-goal-governance`（`docs/workspace-001-goal-governance/`） |
| Root Goal | `GOAL-001-main-vision` |
| 共享资料表 | `workspace.md` 固定引用表为空；`docs/shared-materials/index.json` 为 `inventoryOnly: true`、`files: []` |
| 不含 | 不审 GOAL-012 实现质量；不关闭 GOAL-009 I-009/I-010/F-003/F-004 |

### 成果（有证据）

| 主张 | 核对结果 | 证据路径 |
|------|----------|----------|
| 无并行 `docs/goals/` 真相源 | 通过 | 仓库 `docs/` 下仅有 `workspace-001-goal-governance/` 目标树；不存在 `docs/goals/` |
| 工作区上下文与协议一致 | 通过 | `workspace.md`：`root_goal: GOAL-001-main-vision`，`canonical_scope: docs/workspace-001-goal-governance/`；`docs/architecture/workspace-protocol.md` 同口径 |
| 共享资料候选索引骨架 | 通过 | `docs/shared-materials/index.json`（`inventoryOnly: true`）；`scripts/rebuild_shared_materials_index.py` 拒绝路径逃逸/符号链接 |
| 消费者默认根 | 通过 | `web/services/workspace_config.py` dogfood 路径指向 `docs/workspace-001-goal-governance/`；`GoalsRepository.from_config()` fail-closed，不再静默绑定过程树 |
| 本轮 Web 回归 | 通过 | 在 `web/` 运行 unittest：**43 passed, 1 skipped**（Windows 符号链接负向用例跳过，未记为通过） |

I-001～I-003 在 00-meta 仍为 `verified` 且证据路径可定位；I-004 仍为 `non-blocking / open`（GOAL-009 产品模型），不阻断本目标已完成的目录迁移。

### 对照成功标准

五条成功标准在当前仓库状态下仍成立。工作区目标数已从关门时的 11 增至 12（含 GOAL-012），属后续立项事实，**不**构成 GOAL-011 交付回退。

### Findings（F-00N）

#### F-001 · recommended / medium · open（延续 A-002）— 历史路径叙述与现时入口的文档一致性仍未正式关闭

- **证据**：
  - 当前 [goal-tree.md](../goal-tree.md) **已不再**把 `docs/goals/` 写成现时 canonical 真相源（A-002 当时点名的现时叙述错位，本轮未复现）。
  - 已关门目标（如 GOAL-002/004/006 的决策、执行、附件）仍含迁移前 `docs/goals/` 路径；按 A-002 约定，这些多为历史事实，**不应**为表面一致性批量改写。
  - A-002 建议的「现时入口修正 / 历史语境标注」**尚未**在 GOAL-011 或编排响应中记为 F-001 关闭证据。
- **严重度**：medium；**级别**：recommended（非本目标成功标准回归失败）。
- **不构成**：重开 `status: done`、要求改写历史附件、或把候选索引当共享资料固定引用。

本 scope **无新增 high/required finding**。

### 必改项汇总

无（无开放 required 必改项）。

### 与既有意见的异同

| 条目 | 关系 |
|------|------|
| A-001 self pass | 一致：迁移、索引、回归仍可核对 |
| A-002 independent pass + F-001 recommended | 一致：无功能回退；F-001 部分事实改善（goal-tree 现时叙述）但正式关闭证据仍缺 |

### 结论 + 建议给编排器/用户的下一步

GOAL-011 关门主张在 2026-07-21 回归下仍成立；**verdict: pass**。建议 `/govern`：

1. 可选关闭 A-002/A-003 F-001：在 goal-tree 或 docs 入口补一句「历史记录中的 `docs/goals/` 为迁移前路径；现时 canonical 为 `docs/workspace-001-goal-governance/`」，并在本 `03-audit` 写关闭证据；**不要**批量改写已关门目标附件。
2. 不把 GOAL-011 的完成当作 GOAL-009 多工作区导航或资料 CRUD 门禁关闭。

### 声明

本意见不修改 status/progress；响应由 `/govern` 处理。

## A-004 · 响应 A-002/A-003 · 关闭 F-001（现时入口标注）（2026-07-21）

- **source**：self
- **auditor**：`/govern`（Grok）
- **类型**：response
- **scope**：响应 A-002 / A-003 的 recommended F-001；不重开 GOAL-011，不改已关门目标历史附件。
- **verdict**：pass

### 响应摘要

| Finding | 原状态 | 动作 | 现状态 |
|---------|--------|------|--------|
| F-001（A-002/A-003） | recommended / open | 在 [goal-tree.md](../goal-tree.md) 增加「路径语义说明」：现时 canonical = 本工作区根；历史 `docs/goals/` = 迁移前叙述；禁止批量改写已关门附件 | **closed** |

### 关闭证据

- [goal-tree.md · 路径语义说明](../goal-tree.md#路径语义说明迁移后现时入口)（version 0.24.0）
- 未改写 GOAL-002～010 历史五件套中的迁移前路径（符合 A-002「历史事实保留」约束）
- 本目标 `status` / `progress` 保持 `done` / `100%`；不关闭 GOAL-009 多工作区/资料门禁

### Findings

本响应无新增 finding。A-002/A-003 **F-001 closed**。

### 结论

现时入口与历史语境已可区分；GOAL-011 维持关门。后续若 docs 根 README 需交叉链接，可作为文档维护，不阻断本目标。
