---
id: GOAL-011-multi-workspace-directory-migration
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-20
version: 0.3.0
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
