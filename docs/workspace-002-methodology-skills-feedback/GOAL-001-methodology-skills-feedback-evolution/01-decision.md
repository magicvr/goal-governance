---
id: GOAL-001-methodology-skills-feedback-evolution
doc: decision
status: active
parent: null
created: 2026-07-31
updated: 2026-08-08
version: 0.7.0
---

# 决策记录 · GOAL-001

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同源；关键项：

| ID | 级别 | 状态 | 影响 |
|----|------|------|------|
| I-001 | required | **verified**（2026-07-31） | GOAL-002 已收口；证据见子目标 attachments + D-002；A-002 F-004 → 本表同步 |
| I-002 | non-blocking | **verified**（2026-08-03） | FB-001～FB-005 已由 GOAL-003 承接；R2 启动 |
| I-003 | non-blocking | 已裁决（本轮） | primary 仍为 workspace-001 |

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-008 | 2026-08-08 | 长期持续治理决策：Root 与 VP-002 暂不关门（退出挂起） | accepted | `01-decision/D-008-long-running-governance.md` |

## D-001 · 开区 workspace-002 + Root 服务 VP-002（2026-07-31）

**决定**：

1. Scaffold **`docs/workspace-002-methodology-skills-feedback/`** 为 VP-002 主交付区。
2. Root = **`GOAL-001-methodology-skills-feedback-evolution`**，`parent: null`，`primary_plan` = `VP-002-methodology-skills-feedback-evolution`。
3. `vision_role` = **`delivery`**；**不**改 Charter `primary_workspace`；workspace-001 仍 monorepo **primary**（奠基封存）。
4. 纲领路线图 R1→R2→R3 写入 Root meta；首子目标 **GOAL-002-codex-skills-entry** 进入 R1。
5. 结束 VP-002「0 区空转」：本区为 `lead_workspace`。

**为什么**：

- VP-001 / workspace-001 Root 已有界 done；协议禁止在 done Root 下为 VP-002 开子目标。
- Charter 0.2.0 + H-EVOL-01：下一阶段价值来自方法论 + Skills 问题回流。
- 用户本轮书面确认 slug、Root slug、delivery 角色与首子目标范围。

**未选方案**：

- **在 workspace-001 继续 GOAL-024+**：违反封存纪律与 VRev-006。
- **002 立刻改 primary**：用户本轮明确 001 仍 primary。
- **无 Root 只建子目标**：违反工作区绑定（须有唯一 `parent: null` Root）。

## D-002 · 首子目标聚焦 Codex Skills 入口（2026-07-31）

**决定**：

R1 首交付为 **GOAL-002-codex-skills-entry**：为 Codex 增加与现有 Claude / Copilot / Grok 对等的 **Skills 入口**（安装面 + 可调用编排入口），使消费方可在 Codex 宿主中使用 `/govern` 等主路径。

**为什么**：

- 现 Skills 包已有 `install/claude`、`install/copilot`、`install/grok`；**无** Codex 专用入口。
- 用户明确本轮意图：补 Codex 可用 skills 入口，作为演进波可见的第一刀。

**未选方案**：

- **先做协议大改再补宿主**：无具体反馈前成本高；宿主缺口已明确。
- **只写文档不落 install 适配**：无法在 Codex 中实际调用。

## D-003 · 确认 R1 收口（2026-07-31）

**状态**：accepted
**触发**：用户 `/govern` 工作区2 · **确认 R1 收口**  
**依据**：GOAL-002 `done` + A-001/A-002 pass + A-003 响应；Root I-001 verified

### 决定

1. 纲领阶段 **R1（消费宿主补齐与入口一致）** 标为 **完成**。
2. **收口范围**（本决定所宣称的「完成」仅指下列边界）：
   - 既有宿主：claude / copilot / grok 安装面与入口（开区前已具备，不在本波重验）。
   - 本波补齐：Codex 经 [GOAL-002-codex-skills-entry](../GOAL-002-codex-skills-entry/) — 包内 install 源四入口、`--codex` 脚本、主入口 `$govern` dispatch-readonly 探针证据链完整，关门意见无开放 required。
3. **不**因 R1 收口而：
   - 将 Root `status` 改为 `done`；
   - 勾选 Root 方向级成功标准全表（「一轮反馈闭环」属 R2/R3 / VP 退出判据，尚未满足）；
   - 自动开始 R2 或创建 GOAL-003（须另拍 `/govern`）；
   - 将 consumer 矩阵 Codex 标为 `committed` / 全入口 `runtime-verified`（GOAL-002 I-003 与 F-002 residual 仍 open）。
4. 派生 `progress` 按检查点重算为 **1/3 ≈ 33%**（仅展示）。

### 为什么

- R1 名称与 D-002 范围一致：补齐缺失的 Codex 消费入口，使四宿主安装面对齐策略成立。
- 子目标已合法关门且独立复审 pass；用户本轮书面确认整段收口，结束「进行中」悬置。
- 把「宿主入口」与「真实问题回流修正 / VP 退出」拆开，避免 R1 完成被误读为 VP-002 可关。

### 未选方案

| 方案 | 未选理由 |
|------|----------|
| 等矩阵 committed 再标 R1 完成 | I-003 属发版宣称门禁，非 R1 成功定义；会无限期阻塞宿主补齐收口 |
| 要求四入口均 Codex runtime-verified 才收口 | 超出 GOAL-002 成功标准与 A-001/A-002 residual 边界；用户未扩大标准 |
| 顺带标 R2 开始 | 无 I-002 反馈清单与用户立项意图；禁止空转开阶段 |

### 影响

- meta 路线图 R1 → **完成**；`progress` 0% → **33%**。
- R2 仍 **未开始**；下一拍由用户指定（开 GOAL-003 / 收集 I-002 / 其它）。

## D-004 · 启动 R2 并创建 GOAL-003（2026-08-03）

**状态**：accepted

**触发**：用户 `$govern` 在 workspace-002 提交五项真实项目问题并明确要求新建目标解决

### 决定

1. Root I-002 从 `open` 改为 **verified**：首批 R2 反馈清单已经由用户直接提供。
2. 创建 [GOAL-003-consumer-governance-ergonomics](../GOAL-003-consumer-governance-ergonomics/)，统一承接消费仓证据门禁、长记录布局、审计启动、Git checkpoint 与 Skills 更新五类问题。
3. Root 纲领 R2 从“未开始”改为 **进行中**；GOAL-003 先写 P-001 路线图和 required 信息项，不在立项时伪造具体方案。
4. Root `progress` 仍为 **1/3 = 33%**：R2 开始不等于 R2 完成，百分比不作放行依据。

### 为什么

- 用户反馈直接满足 I-002 的收集动作，且范围与 VP-002 的真实问题回流意图一致。
- 五项问题跨多个门禁域并包含多块可独立验收工作，须先在大目标内建立纲领路线图。
- 先作为一个 R2 目标冻结共同边界，可在 S1 后再按依赖与并行价值决定是否拆子目标。

### 未选方案

| 方案 | 未选理由 |
|------|----------|
| 维持 R2 未开始，只把问题留在聊天 | 反馈会丢失，且不满足用户明确的新建目标指令 |
| 直接创建五个平级子目标 | 尚未冻结共同契约、兼容矩阵与阶段依赖，违反 P-001 |
| 因 R2 启动把 Root progress 提高到 67% | progress 仅按完成纲领阶段计数；R2 尚未完成 |

## D-005 · 完成 R2 反馈修正阶段（2026-08-04）

**状态**：accepted

**依据**：[GOAL-003 D-009](../GOAL-003-consumer-governance-ergonomics/01-decision/D-009-close-out.md)；A-001 self / A-002 Grok Build independent 均 pass；A-003 响应后开放 required = 0。

### 决定

1. R2 标为 **完成**；Root progress 由 1/3 = 33% 派生为 2/3 = 67%。
2. GOAL-003 标为 `done`，构成首轮“真实反馈 → 协议/Skills 修正 → 全量验证 → cross close-out”闭环。
3. R3 仍未开始；Root 保持 `active`，不自动关闭 VP-002。
4. Web controlled-change legacy writer 作为子目标 recommended open 继续按触发条件复审，不提升为 Root required。

### 为什么

R2 的首批五项问题已有实现、兼容回归、consumer 包抽样与双来源审计；没有开放 required finding。R3 的 VP 退出准备是下一独立阶段，不能借 R2 完成静默启动或宣称方向关门。

## D-006 · 启动 R3 并创建 GOAL-004 退役冻结 Web 资产（2026-08-04）

**状态**：accepted

**触发**：用户决定彻底移除冻结 Web 资产、挂起对应 VP，并明确允许在 workspace-002 新建目标记录实施。

### 决定

1. 启动 Root **R3 有界闭环验证与 VP 退出准备**；创建 [GOAL-004-frozen-web-asset-retirement](../GOAL-004-frozen-web-asset-retirement/) 承接一次性删除、producer gate 收束、保护验证与 independent close-out。
2. GOAL-004 的 `primary_plan` 仍为 **VP-002**：这是本活动工作区的仓库卫生/退出准备，不是 VP-003 产品实施；VP-003 只作为跨区决策对象保持 `planned` 且正式挂起。
3. workspace-001 的历史所有权由其 Root **D-029** 后置授权；本区不跨区设置 `parent`，也不重开封存 Root。
4. R3 改为**进行中**，Root progress 保持 **2/3 = 67%**；GOAL-004 关门不自动等于 R3/Root/VP-002 关门，退出判据仍须另行核对。
5. 审计模式固定为 **independent**；不改核心方法论/Skills 行为，不发布新版本。

### 为什么

- 删除横跨 Web 源码、CI、release evidence、compatibility matrix 与现行叙事，具备独立范围、门禁和证据，应建立单独目标。
- R3 本来负责有界验证与 VP 退出准备；消除冻结资产造成的反复回归/审计成本，正是收束 producer 仓维护边界的一部分。

### 未选方案

| 方案 | 未选理由 |
|------|----------|
| 在 workspace-001 新建 GOAL-024 | archived Root 已 done，违反封存纪律 |
| 只写 VP、不建实施目标 | 无法追踪删除、测试和 independent audit 闭环 |
| 因启动 R3 把 progress 提高到 100% | progress 只按完成阶段计数；R3 尚未完成 |

## D-007 · 在 R3 创建 GOAL-005 修复 Vision Review 台账增长缺口（2026-08-06）

**状态**：accepted

**触发**：用户在实际使用中发现 `docs/vision/reviews.md` 仍把全部愿景审视与响应保存在单文件，并明确要求通过 `/govern` 在工作区 2 立项、完成修正和正式发布。

### 决定

1. 在 Root R3 内创建 [GOAL-005-vision-review-ledger-scaling](../GOAL-005-vision-review-ledger-scaling/)；parent 为本 Root，服务 VP-002。
2. 目标范围覆盖 canonical 协议、现有 VRev 迁移、Skills/模板/安装/测试同步、cross audit、PR/main 与正式 Release；不缩减为仅调整文档措辞或未来写入。
3. Root R3 保持进行中，progress 保持 2/3 = 67%；GOAL-005 立项或关门均不自动关闭 Root/VP-002，退出仍须独立审视。
4. 核心元规则与发布边界采用 `cross` 模式；GOAL-005 S4 需 self + independent，开放 required = 0 后才可发布。

### 为什么

该问题来自真实消费使用，符合 VP-002 与 R3 的协议缺口收束边界；影响规范、分发与历史权威记录，具备独立交付、验证和发布门禁，必须用单独目标承接。
