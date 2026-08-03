---
id: GOAL-001-methodology-skills-feedback-evolution
doc: decision
status: active
parent: null
created: 2026-07-31
updated: 2026-08-03
version: 0.3.0
---

# 决策记录 · GOAL-001

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同源；关键项：

| ID | 级别 | 状态 | 影响 |
|----|------|------|------|
| I-001 | required | **verified**（2026-07-31） | GOAL-002 已收口；证据见子目标 attachments + D-002；A-002 F-004 → 本表同步 |
| I-002 | non-blocking | **verified**（2026-08-03） | FB-001～FB-005 已由 GOAL-003 承接；R2 启动 |
| I-003 | non-blocking | 已裁决（本轮） | primary 仍为 workspace-001 |

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
