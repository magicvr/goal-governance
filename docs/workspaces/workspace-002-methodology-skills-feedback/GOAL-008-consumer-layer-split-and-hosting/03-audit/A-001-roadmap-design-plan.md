---
id: A-001
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-001
source: independent
scope: design-plan · GOAL-008 纲领路线图 S1-S6
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-001 · GOAL-008 路线图合理性独立审计

## 范围与区间

- **auditor**：Codex `audit` skill（independent entry）
- **type**：`design-plan`
- **工作区**：`[workspace-002-methodology-skills-feedback]`
- **covered**：GOAL-008 `00-meta.md` 的 S1-S6 纲领路线图、D-001、I-001～I-006、Root R3 对齐、VP-002/Charter 链，以及与 S2-S6 相关的原则、安装面和 `/commit` 边界。
- **excluded**：实现正确性、代码修改、阶段关门和其他工作区上下文。
- **区间**：2026-09-13；GOAL-008 为 `active / 0%`，此前没有正式 A-00N 意见，I-001～I-006 均为 `open`。

## 成果（有证据）

| 主张 | 证据 |
|------|------|
| 工作区绑定、Root 归属和愿景规划链一致 | `docs/workspaces/workspace-002-methodology-skills-feedback/workspace.md:2-12,26-36`；Root `GOAL-001/00-meta.md:2-8`；`docs/vision/plans/VP-002-methodology-skills-feedback-evolution.md:2-10`；`docs/vision/charter.md` 现行版本 `0.2.0` |
| GOAL-008 是同区 Root R3 内的合法子目标，目标五件套和 ledger 索引已建立 | `docs/workspaces/workspace-002-methodology-skills-feedback/goal-tree.md:15-17,121-143`；GOAL-008 `00-meta.md:2-9`、`01-decision.md:17-32`、`02-execution.md:17-24`、`03-audit.md:16-32` |
| 高层顺序满足 P-001/P-002 的基本形状 | GOAL-008 `00-meta.md:37-48`；`docs/architecture/principles.md:43-74,88-110`；`docs/architecture/workspace-protocol.md:61-68` |
| `/commit` 当前已有 monorepo Copilot prompt，但尚未成为 Skills 包四宿主的默认入口 | `.github/prompts/commit.prompt.md:1-35`；`skills/install.sh:612-629`；`skills/install.ps1:695-717`（当前默认只列 `govern/audit/vision/vision-audit`） |
| 安装器和 updater 存在 S4/S5 可能共同触及的集中写入面 | `skills/install.sh:632-644`；`skills/install.ps1:720-735`；`skills/update.py:156-183` |

## 对照成功标准

| 范围 | 结论 |
|------|------|
| S1 先行、S2→S3 串行、S6 汇总 | **通过（结构层）**：依赖方向清楚，且没有用 `progress` 冒充放行依据。 |
| 双层语义、VP 跟踪、消费共存和 `/commit` 的可验证交付 | **有条件**：目标已登记对应 required 信息，但阶段退出条件尚未达到可重复核验的粒度。 |
| 对齐链 | **通过（当前状态）**：未发现当前 Workspace → Root → VP → Charter 机读或明显语义断裂；这不替代后续实现审计。 |

## Findings

### F-001 · I-005 的 S1/S2 闸门时序未唯一化

| 字段 | 值 |
|------|-----|
| level | required |
| severity | medium |
| status | open |
| impact_gate | S1 退出 / S2 实施前的 `cross` 审计门禁 |
| evidence | GOAL-008 `00-meta.md:41,62`；`01-decision/D-001-scope-and-roadmap.md:21-24`；`docs/architecture/principles.md:159-171,250-264` |
| closure | 由 `/govern` 在决策/响应中明确并保留留痕；未明确前不得把 S2 当作可实施。 |

事实是：S1 退出条件写成 I-001～I-005 都完成当前阶段收集，而 I-005 的影响门禁又写成 S2 实施、provider 为“待用户指定”；D-001 则写明 provider 在 S2 实施前指定。当前文本因此允许两种读法：provider 选择是 S1 退出条件，或只是在 S2 实施临界点阻断。建议明确为“provider 选择可作为 S1 退出条件；independent 输出/可核对结果在 S2 实施前必须到位”，或反之明确 S1 可结束但 S2 不得开始。provider 失败、超时或不可核对时仍不得静默降级。

### F-002 · S1-S4 退出条件缺少可重复的验收载体

| 字段 | 值 |
|------|-----|
| level | required |
| severity | medium |
| status | open |
| impact_gate | S2/S3/S4 方案冻结、实施与阶段放行 |
| evidence | GOAL-008 `00-meta.md:41-44,56-60`；`docs/architecture/principles.md:88-110,316-343` |
| closure | 在 S1 方案/计划记录中补验收矩阵、证据路径和责任/审视方式，并把其关键字段反映到各阶段退出条件。 |

当前路线图的方向是正确的，但关键退出语句仍是 gate-shaped：

- S1 未规定矩阵字段、可复现路径的定义、责任边界的证据和验收人；
- S2 的“AI 不再混淆”没有固定 probe/corpus、正反例集合、通过阈值和覆盖的宿主/提示词面；
- S3 没有在退出条件中锁定跟踪权威落点、既有数据迁移/兼容读取和重复信息不存在的核验；
- S4 的“兼容完整安装 MUST”没有选定共存模型，也没有明确保护消费方已有规则/文档的负例测试。

I-001～I-003 已正确登记为 required，故这不是要求立项前知道全部方案；但在对应阶段放行前，必须把上述未知转成有限、可重复核对的产物和测试，否则不能仅凭阶段文字宣称方案冻结或实施完成。

### F-003 · S4/S5 的“可并行”缺少共享写集与集成门禁

| 字段 | 值 |
|------|-----|
| level | required |
| severity | medium |
| status | open |
| impact_gate | S4/S5 并行授权、合并和 S6 回归 |
| evidence | GOAL-008 `00-meta.md:48`、I-003/I-004 `00-meta.md:60-61`；`skills/install.sh:612-644`；`skills/install.ps1:695-735`；`skills/update.py:156-183` |
| closure | 在 S1 后列出 S4/S5 owned paths；若仍重叠则串行化，若可分离则写明分支边界、合并顺序、冲突处理和集成验证。 |

P-001/工作区协议允许同一纲领阶段并行，但前提是依赖和门禁可追踪。当前安装器把宿主入口复制、Copilot prompt 列表、core 文档安装和 updater managed pairs 集中在同一批文件/路径；S4 必然要重新定义安装/更新共存面，S5 又要把 `/commit` 暴露到宿主入口。路线图没有证明两者写集不重叠，也没有规定谁在合并后负责重新跑统一安装/更新回归。若 S5 依赖 S4 的共存模型，应改为 S4→S5；若确实能并行，须先落盘不重叠写集和集成 checkpoint。

### F-004 · S5 未显式保留 `/commit` 的“便利可选”边界

| 字段 | 值 |
|------|-----|
| level | required |
| severity | medium |
| status | open |
| impact_gate | S5 方案冻结、完整安装判定和发布验收 |
| evidence | GOAL-008 `00-meta.md:34,45,61`；`.github/prompts/commit.prompt.md:8-28`；`docs/vision/plans/VP-004-mcp-file-dual-channel-delivery.md:41-47,164-177`；`docs/architecture/principles.md:129-136` |
| closure | 在 S1/I-004 或 S5 决策中写明“默认提供”仅指已支持宿主的便利入口；不得把 `/commit` 升格为完整治理安装 MUST、治理入口必达或 `/govern` checkpoint 的替代物，并补齐负例验收。 |

VP-004 已将 `commit` 定义为与目标治理正交的“便利可选”，并明确禁止将其设为治理 MUST。GOAL-008 当前要求默认提供入口、分离 checkpoint 和失败 fail closed，这可以兼容该边界，但没有把“默认安装/可调用”与“完整安装必需/治理放行条件”区分开。S5 的可核对契约还应覆盖 owned paths、既有用户改动、无改动/非 Git、验证失败、提交失败、用户禁用自动 checkpoint 以及所有承诺宿主；现有 monorepo prompt 已体现部分安全暂存规则，但不能替代消费包四宿主交付证据。

### F-005 · S6 的发布与证据范围尚未封闭

| 字段 | 值 |
|------|-----|
| level | required |
| severity | medium |
| status | open |
| impact_gate | S6 回归、cross close-out 和正式发布 |
| evidence | GOAL-008 `00-meta.md:35,46,63`；`docs/architecture/principles.md:129-142`；`docs/vision/alignment.md:170-182` |
| closure | 在 I-006 关闭及 S6 方案中固定目标版本、tag/revision 关系、资产清单、回归矩阵、cross 审计覆盖面和 consumer/producer 证据归属；基线前移时重新核对。 |

“canonical / 镜像无漂移、cross 审计无开放 required、正式发布证据可核对”方向正确，但目前无法从路线图重现验收边界：I-006 仍未决定版本/tag/dev 基线，未列 release asset set、精确测试/宿主矩阵，也未说明本目标只证明 consumer contract/安装证据，还是会触及 producer compatibility/release gate。P-002 要求事实可指回证据，且 producer 与 consumer 证据职责不能混淆；这些字段应在 S6 前冻结，而不是留给关门时临时解释。

## 必改项汇总

未关闭的 required findings 为 **F-001～F-005**。它们不阻断 GOAL-008 进行 S1 的只读现状复现与信息收集，但分别阻断对应的 S2/S3/S4/S5/S6 方案冻结、并行授权、实施或关门放行。当前没有证据表明目标已进入任何后续阶段。

## 与既有意见的异同

`03-audit.md` 在本审计前登记为“尚无正式 A-00N”，因此没有可比较的 self/independent 历史意见，也没有发现意见冲突。

## 结论 + 建议给编排器/用户的下一步

**verdict：`conditional`。** S1 先行、S2→S3、S6 汇总的高层结构合理，当前 Workspace → Root → VP-002 → Charter 对齐也通过；但 S1 结束和后续实施所需的门禁、验收证据、并行写集及 `/commit`/发布边界尚未被写成足够可复核的方案。建议由 `/govern` 响应 F-001～F-005，先完成 S1 方案审视与验收矩阵，再决定 S4/S5 是否并行，并在相应 finding 合法闭合前保持后续门禁关闭。

## 声明

本意见的 `source` 为 `independent`；本轮只追加 Goal 审计意见，不修改目标 `status`、`progress`、检查点、方案正文或 `goal-tree`。响应与任何状态/阶段变更由 `/govern` 按 P-003/P-004 处理。
