---
title: A-014 · GOAL-009 当前整体就绪与门禁一致性独立审计（全文）
status: active
created: 2026-07-21
updated: 2026-07-21
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.1.0
source: independent
verdict: conditional
---

# A-014 · GOAL-009 当前整体就绪与门禁一致性独立审计（全文）

- **source**：independent
- **auditor**：GitHub Copilot · Grok 4.5
- **日期**：2026-07-21
- **类型**：design-plan / ad-hoc
- **scope**：目标 9 整体现状——产品边界、路线图 A～E、信息门禁 I-00N、开放 findings、R-001/R-004 收集产物、D-006～D-008 裁决响应、以及与现有 `web/` 只读能力的一致性。不审计实现运行时、试点或关门。
- **verdict**：conditional

## 1. 范围与证据

工作区上下文：`workspace-001-goal-governance`（Root `GOAL-001-main-vision`，canonical `docs/workspace-001-goal-governance/`）。未读取或比较其他工作区。

| 证据 | 用途 |
|------|------|
| [workspace.md](../../workspace.md) | Root / canonical / 共享资料固定引用表为空 |
| [goal-tree.md](../../goal-tree.md) | GOAL-009 `active / 0%`；GOAL-010/011 `done` |
| [00-meta.md](../00-meta.md) | 成功标准、路线图、I-001～I-012、R-001/R-004 入口 |
| [01-decision.md](../01-decision.md) | D-001～D-008 |
| [02-execution.md](../02-execution.md) | 时间线与“未实现/未放行”声明 |
| [03-audit.md](../03-audit.md) A-001～A-013 | 既有意见、关闭范围与开放门禁 |
| [R-001](r-001-single-user-workflow-ia-vertical-journey.md) | 首切片与三页 IA 收集稿 |
| [R-004](r-004-controlled-change-contract.md) | 受控变更设计约束（含 D-007 §6） |
| [R-004 测试计划](r-004-contract-test-plan.md) | CT-001～CT-015 与实现前门禁 |
| [web/main.py](../../../../web/main.py) | 仅 GET 首页/详情；旧路由重定向 |
| [web/services/goals_repo.py](../../../../web/services/goals_repo.py) | 默认读 `workspace-001`；无 approval/operation_id |
| [web/.env.example](../../../../web/.env.example) | AI 配置范例；声明当前未加载 |
| 目录检查 | 工作区无 `ops/`、`ops/receipts/`；无已提交 `web/.env` |

本意见**不**修改 `status`/`progress`、方案正文或 `goal-tree.md`，**不**关闭既有 finding，**不**将任何 I-00N 标为 `verified`。

## 2. 成果（有证据）

1. **产品方向与纪律保持一致**：人主导、AI 协助、canonical 文档真相、受控写入前置确认、禁止自动 P-004/关门——贯穿 D-001～D-008 与执行记录，且未把计划文字标为实现。
2. **实现面诚实**：`web/main.py` 仅有 `GET /`、`GET /goals/{goal_id}` 与兼容重定向；仓库默认根为 `docs/workspace-001-goal-governance/`；无 `ops/receipts/`；无受控写入 API；`GoalsRepository` 未见 approval、provenance、operation_id、workspace lock 或幂等语义。与 `active / 0%` 一致。
3. **A-011 设计缺口已获用户裁决响应**：D-007/A-012 关闭 F-013～F-019 的设计 scope；R-004 §6 收敛为线性对象流、三层门禁、单文件追加、非 canonical receipt、串行化、local trust_context 与内容契约。A-012 明确这些关闭不等于实现证据——记录诚实。
4. **A-013 正确把下一步定为测试计划而非实现**：D-008 + CT-001～CT-015 是可审视收集输入；实现前门禁清单全部未勾选；F-007/F-008 仍 open。
5. **上游输入边界清楚**：GOAL-010/011 经 A-008/A-009 交接为 R-003 输入，不伪装为 F-003/F-004 关闭或路线图 B 放行。
6. **工作区协议 fail closed**：`workspace.md` 共享资料固定引用表为空；GOAL-009 未把 `shared-materials/index.json` 当作事实或 finding 关闭依据。
7. **无错误关门或错误放行迹象**：无 residual risk 接受；无 I-00N 被误标 `verified`；无把 CT 计划写成测试通过。

## 3. 对照门禁与开放项（当前真相）

| 项目 | 状态 | 判断 |
|------|------|------|
| 路线图 A | 进行中 | D-006 收敛首切片，但 F-001 仍阻断 A 退出；I-001 仍 collecting |
| 路线图 B | 未开始 | F-002/F-003/F-004、I-002/I-008/I-009/I-010 开放 |
| 路线图 C | 未开始 | F-007/F-008、I-003/I-004/I-006 开放；仅有设计与测试计划 |
| 路线图 D 立项 | 未开始 | F-005 仍 open；无实现子目标 |
| F-009 / F-010～F-012 / F-013～F-019 | closed（各自 scope） | 关闭证据分别为范围裁决、共享资料修订、R-004 设计裁决；均非实现/验收 |
| F-001～F-005、F-007、F-008 | open / required | 仍阻断对应阶段 |
| F-006 | open / recommended | 试点保障，后置合理 |
| I-007、I-012 | non-blocking / open | 不阻断当前发现 |
| Web/AI 写入、部署、试点 | 未开始 | 与门禁一致 |

## 4. Findings

### F-020 · CT 计划未把 D-007 已接受的关键边界场景全部显式编号

- **级别**：required；**严重度**：medium
- **关联信息项**：I-003、I-004、I-006
- **关联既有 finding**：F-007、F-008（关闭路径）
- **证据**：
  - [R-004 §6.2/§6.6](r-004-controlled-change-contract.md) 明确：目标存在 open required finding 时，操作策略通过后仍可受限追加事实，且不得关闭 finding 或推进阶段。
  - [测试计划](r-004-contract-test-plan.md) CT-001～CT-015 覆盖缺字段、跨范围、写集、基线、过期、幂等、并发、恢复、receipt、内容违规、产品实现门禁、治理指令、外部 trust；**没有**独立 CT 断言“open required finding + 策略通过 → 允许受限追加且 finding 仍 open”。
  - 内容规范化（UTF-8/LF 后再算 digest）在 R-004 §6.5 为必须，但无 CT 覆盖“换行/规范化前后 digest 不一致”的失败或接受路径。
  - `affirm` 与执行同请求衔接是 D-007 核心简化，无 CT 区分“仅确认不执行”或“二次执行动作”的错误 API 形态。
- **影响**：后续实现者可能只测拒绝路径，漏测“门禁分层后仍允许记事实”的正向边界，导致 F-014 设计裁决在验收时被再次抹平，或把 open finding 误做成禁止记事实。
- **关闭要求**：在实现前修订测试计划（或后续 D-00N），至少新增：
  1. CT 案例：fixture 目标带 open required finding → 受限追加成功 → canonical 仅 `02-execution.md` 变化 → finding/status 不变；
  2. CT 案例：非规范化换行/内容规范化后 digest 重算规则；
  3. CT 或接口契约：UserDecision.affirm 与执行同请求，禁止拆成无重校验的第二步写入口。
  上述仍是计划完善，不是测试通过。

### F-021 · R-001 / D-006 与 D-007 对象命名及状态模型未同步

- **级别**：recommended；**严重度**：medium
- **关联信息项**：I-001、I-003、I-011
- **证据**：
  - D-007/R-004 §6 权威对象为 `CandidateRevision`、`Proposal`、`UserDecision`、`ExecutionReceipt`。
  - [D-006](../01-decision.md)、[R-001 §2](r-001-single-user-workflow-ia-vertical-journey.md)、[02-execution.md](../02-execution.md) 2026-07-20 条目仍写 `Candidate` / `Confirmation` 与“四类对象待定义”。
  - R-004 §2～§4 仍保留旧细粒度状态机作为“原始收集基线”，虽声明与 §6 冲突以 §6 为准，但 R-001 未交叉引用该优先级。
- **影响**：后续 fixture、API 命名或 UX 文案可能混用两套模型，重复 A-011 已关闭的状态机膨胀问题。
- **建议关闭要求**：由 `/govern` 在 R-001 与相关执行摘要中增加 D-007 映射表（Confirmation = UserDecision；线性流优先），或明确“历史命名仅追溯、实现以 R-004 §6 为准”。不要求重写全部历史审计。

### F-022 · 收集重心偏向 R-004，R-001/R-002/R-003 仍不足以支撑对应阶段退出

- **级别**：required；**严重度**：medium
- **关联信息项**：I-001、I-002、I-008、I-009、I-010、I-011
- **关联既有 finding**：F-001、F-002、F-003、F-004、F-005
- **证据**：
  - R-004 已完成用户设计裁决 + 测试计划收集；R-001 仍为收集稿，F-001/F-005 open；R-002（事实准入/AI）几乎无契约产物；R-003 仅有 GOAL-010/011 输入交接，无产品模型/导航例外/共享资料 CRUD 契约。
  - 门禁表仍正确阻断：A 退出靠 F-001；B 靠 F-002～F-004；D 立项靠 F-005；C/写入靠 F-007/F-008。
  - D-008 下一步写“审视 fixture 后再另立实现子目标”，若编排器只跟 R-004 深度而跳过 F-005/I-001 审视，会与 A-004 响应组顺序冲突。
- **影响**：不是否定 R-004 推进，而是指出**并行缺口**：即使 CT 计划完善，仍不能仅凭 R-004 退出路线图 A 或立项实现；否则会重复 F-009 曾警告的“抽象契约很长、用户旅程未审视”风险。
- **关闭要求**：`/govern` 在排期中显式保留：
  1. 完成或明确拒绝路径的 R-001 用户审视结论（至少支撑 F-001/F-005 的可核对证据策略）；
  2. R-002/R-003 的下一收集动作或“首切片不需要的部分延后但门禁保留”的书面范围；
  3. 禁止在 F-005 仍 open 时创建实现子目标或开放写入。

### F-023 · 测试计划尚未下沉为可执行契约规格（fixture / 接口 / 错误码 / 证据格式）

- **级别**：required；**严重度**：medium
- **关联信息项**：I-003、I-004、I-006
- **关联既有 finding**：F-007、F-008
- **证据**：
  - 测试计划 `review_state: govern-approved-collection-plan`，实现前门禁清单 0 勾选。
  - D-008 与 A-013 下一步正是“审视 fixture、契约接口、错误码和机器可读证据”，当前附件只有场景表与证据记录提纲，**没有**最小 API/服务边界、错误码枚举、fixture 目录约定或示例 receipt JSON/Markdown 形态。
  - 现有 `GoalsRepository` 仍是整文件 update 工具，不是带 proposal_digest 的受控写入门面。
- **影响**：若直接从 CT 表跳到编码，实现者会自行发明接口与错误语义，导致“测的是别的系统”；F-007/F-008 关闭将再次缺乏可重复核对标准。
- **关闭要求**：在另立实现目标前，形成用户可审视的最小规格包：fixture 布局、操作入口（即使仅 service-level）、错误码/结果码表、receipt 字段示例、pre/post digest 算法说明。规格通过审视 ≠ 测试通过 ≠ 写入放行。

### F-024 · 部分权威文案仍将 `docs/goals/` 表述为当前真相源路径

- **级别**：recommended；**严重度**：low
- **关联信息项**：I-009
- **证据**：
  - [D-001](../01-decision.md) 第 3 点仍写“`docs/goals/` 与 `goal-tree.md` 继续是唯一运行时真相”。
  - 迁移后 canonical 为 `docs/workspace-001-goal-governance/`（GOAL-011 / workspace.md / Web 默认根均已切换）。
  - 历史 A-001/A-002 等使用旧路径属可理解的历史记录；问题在于 **仍 active 的 D-001 决定正文**未标注“路径已被 workspace 根替代、原则不变”。
- **影响**：新读者或实现者可能硬编码已废弃全局路径，或与 I-009“工作区映射”问题混淆。
- **建议关闭要求**：在 D-001 影响说明或后续窄决策中注明：原则是“工作区 canonical 根 + goal-tree”，当前仓库路径为 `docs/workspace-001-goal-governance/`；不改写历史审计正文。

## 5. 必改项汇总

| Finding | 级别 | 阻断 / 影响 |
|---------|------|-------------|
| F-020 | required / medium | 完善 CT 计划后才能把测试范围视为覆盖 D-007 门禁分层；否则 F-007/F-008 验收标准不完整 |
| F-022 | required / medium | 不得仅凭 R-004 深度推进而绕过 F-001/F-005 与 R-002/R-003 门禁 |
| F-023 | required / medium | 实现前缺少 fixture/接口/错误码规格则不得声称契约可测或关闭 F-007/F-008 |
| F-021 | recommended | 命名同步，降低实现漂移 |
| F-024 | recommended | 路径术语澄清，降低硬编码旧路径风险 |

既有 **F-001～F-005、F-007、F-008** 保持 open；**F-006** 保持 recommended open；已关闭的 F-009～F-019 不在本意见重开。

## 6. 与既有意见的异同

- 与 A-001～A-004 **同向**：方向合理，阶段门禁仍在；本意见确认后续响应未违规放行。
- 与 A-005～A-007 **同向**：共享资料术语污染已在记录层修复；F-004/I-010 仍正确开放。
- 与 A-008/A-009 **同向**：GOAL-010/011 只是输入。
- 与 A-011/A-012 **同向**：R-004 设计裁决有效且有边界；本意见不重开 F-013～F-019，只检查裁决后的下游完整性。
- 与 A-013 **同向且补充**：肯定测试计划作为正确下一步，但指出 CT 覆盖缺口（F-020）与规格下沉缺口（F-023），以及并行收集失衡（F-022）。
- **无 P-004 意见冲突**：本意见不与既有 independent/self 在必改方向上相反；是否需要同范围 self 由 `/govern` 询问用户。

## 7. 结论与建议给编排器/用户的下一步

GOAL-009 当前是**纪律良好的产品发现与契约收集目标**：方向正确，进度 `0%` 诚实，未偷跑实现，A-011 设计 findings 已获用户裁决，A-013 测试计划是正确的收集增量。  
但 **required 信息与 finding 远未达到任何阶段退出或写入放行条件** → **verdict = conditional**。

建议 **`/govern`**：

1. P-004：是否对 A-014 做同范围 self 审视（已有 independent；本轮默认不强制）。
2. 响应 F-020/F-023：先补 CT 边界案例与最小 fixture/接口/错误码规格包，再谈实现目标。
3. 响应 F-022：并行排出 R-001 审视与 R-002/R-003 收集（或书面延后范围），禁止用 R-004 深度替代 F-001/F-005。
4. 可选处理 F-021/F-024 的文档同步。
5. **在 F-007/F-008 关闭且 I-003/I-004/I-006 verified 前**，不得开放 Web/AI 写入；**在 F-005 关闭前**不得立项实现子目标。

## 8. 声明

本意见只追加审计台账与本附件；不修改 GOAL-009 的 `status`、`progress`、方案正文或 `goal-tree.md`。finding 响应与阶段推进归 `/govern` 与用户。
