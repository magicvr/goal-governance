---
id: A-002
goal: GOAL-020-goal-drift-detection
source: independent
auditor: Grok 4.7
scope: S1–S3 drift contract, consumption, and cited evidence before release
verdict: pass
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
---

# A-002 · S1–S3 漂移防护的独立审计

- **source**：independent
- **auditor**：Grok 4.7。项目配置 `.goal-governance.json` 的 `independent_audit` 为 provider `grok`、model `grok-4.7`、reasoning_effort `xhigh`。本会话执行的正式命令是 `/audit workspace-002 goal-020`。
- **类型 / scope**：design-plan 与 execution-facts，覆盖 S1 根因、S2 契约与消费入口、S3 已落盘的静态契约、16 格入口边界和 6 项语义宿主结果，以及本目标对父级 R3 的贡献与授权连续性。不含 S4 的 PR、main、annotated tag、正式资产验收或关门。
- **verdict**：pass

## 范围与区间

工作区 `workspace-002-methodology-skills-feedback`，canonical 范围 `docs/workspaces/workspace-002-methodology-skills-feedback/`，Root `GOAL-001-methodology-skills-feedback-evolution`。焦点 `GOAL-020-goal-drift-detection` 的 `id` 与目录名一致，`parent` 为同区 Root。`goal-tree.md` 同一行：active，50%，父级为该 Root。

计划链：工作区与 Root 的 `plan_refs` / `primary_plan` 均为 `VP-002-methodology-skills-feedback-evolution`。该 VP 为 active，`vision_ref` 为 `vision-goal-governance@0.2.0`，与现行 Charter `0.2.0` 一致。`lead_workspace` 指向本区。全仓仅 workspace-001 声明 `vision_role: primary`。本目标未登记共享资料引用；工作区引用表为空。

已读：本目标 meta、D-001、E-001～E-003、A-001，以及 `attachments/root-cause.md`、`semantic-results.md`、`s3-selected-runtime-evidence.json` 和其中点名的 6 份语义意见。父级对照读到 Root 的目的、成功标准、R3、D-008 所指向的长期治理约束，以及现行 Charter / VP-002 的意图边界。沿父链到 Root 后再向上是 VP，未加载其他子目标正文。

## 成果（有证据）

- `81913d2` 上的入口缺口与 [root-cause.md](../attachments/root-cause.md) 的行号一致。当时 `04` 第 66、68、79 行要求通读当前目标并对照其成功标准；`05` 第 58、80 行要求自主通读本目标台账；`01` 第 70、74 行创建 parent 与成功标准；`02` 第 65 行在改范围后同步 meta；`03` 第 57–72 行记录本目标事实并勾选成功标准。这些步骤都没有强制保留父级结果、原始授权和实际交付的对照。
- 现行 `docs/architecture/principles.md` 有单一 `#goal-drift` 锚点及 GD-01～GD-08。`governance-guide.md`、`alignment.md`、根 `AGENTS.md`、目标模板、prompts `00`～`05` 和 `mcp/entries.py` 的 govern/audit guidance 都要求这条对照。显著偏离或关键证据不足形成 required，并在合法闭合前挡住受影响门禁。合法阶段子集、调查阶段和已批准变更仍被保留。
- 本审计复跑 `skills.tests.test_goal_drift_contract`：5 项通过。`python scripts/stage_skills_mirrors.py --check`：44 对一致。
- [s3-selected-runtime-evidence.json](../attachments/s3-selected-runtime-evidence.json) 列出 16 份文件，SHA-256 均与磁盘一致，信封 verdict 均为 pass。组合是三宿主（claude-code-cli、github-copilot-cli、grok-build-cli）的 audit/govern/vision/vision-audit，加上 claude、codex、copilot、grok 四份 catalog。该 pass 是入口与台账边界。抽查 `claude-audit-02` 的正式意见 verdict 为 conditional，与信封 pass 是两件事实。
- [semantic-results.md](../attachments/semantic-results.md) 点名的 6 份意见与摘要一致：Codex 对未授权 ASCII 缩减给出 fail，F-001 写明显著漂移并阻断验收/关门；Copilot 对 README 标题替代计数给出 fail，F-001 required 写明验收替代和父级计数结果无覆盖；合法 ASCII 子集、书面批准的含空白口径、仅 S0 样例三案都保留了对应 required 证据缺口，并写明未见范围漂移。文档未改而 `len` 计入空白的一案，Codex verdict 为 fail，必改项是实现不符合已授权计数语义，原文写的是实现和验证缺陷。
- E-003 记载 Skills 113、docs 76、scripts 156 与 rehearsal `checksPassed=true`。本审计未重跑这四项，只核对了上面的契约测试、镜像和 16 份摘要。

## 对照成功标准

| 标准 | 本 scope 的核对 |
|------|----------------|
| C1 | 成立。出处能回到 `81913d2`；用户历史实例留在 I-004，根因文档把它和已证实的规则缺口分开。 |
| C2 | 成立。canonical、模板、六个 prompt 与 MCP govern/audit 指导都要求父级贡献、授权基线/变更和实际交付对照，并用 required 挡住受影响门禁。 |
| C3 | 行为材料已齐，勾选仍留给响应。反例里，验收替代与无关产物被写成漂移；仅实施偏离被阻断验收，原文没有把它定性为漂移。合法子集与已批准调整没有被写成漂移。本 A-002 是指定 provider 的正式意见。开放 required 的响应、I-002 状态回写和「无开放 required」仍由 `/govern` 完成。 |
| C4 | 未开始。E-002、E-003 都写明尚未 PR 或发布。本 pass 不覆盖 C4。 |

I-001 的 verified 与根因、D-001、E-002 相符。I-002 仍标 open，证据栏仍是「待实际运行」；E-003 与语义附件已经给出运行事实，指定 provider 审计由本条目完成。I-003 最晚阶段是关门，继续 open，不挡住本次 S1–S3 意见。I-004 为 non-blocking，没有具体项目材料，结论停在协议缺口。

## 目标漂移对照

父级是同区 Root，基线为 D-001 所记的 version 0.14.45、Git `81913d2`、D-008。现行 Root meta 为 0.14.46，成功标准 1/2 与 R3「持续闭环与长期演进」仍在，退出继续挂起。父级要的是真实反馈变成可审计、可安装的协议与 Skills，并且不关闭 Root / VP-002。

原始授权在 D-001：调查漏审、补上立项/路线图/变更/审计防护、dev 修改、PR 合 main、发布新资产；Codex 取证指定 gpt-6-luna。此后没有第二条决策替换该范围。当前 C1～C4 与 S1～S4 仍是这组承诺。已交付的是规则、模板、六个 prompt、MCP 指导、契约测试、16 格边界证据和 6 项语义意见。PR、main 与正式发布仍留在 S4。Root/R3/VP 的长期治理继续由父级承接。

本 scope 内，实际交付对着原始授权，没有把本地全绿或子目标切片写成父级关门，也没有把用户未提供的历史实例写成已复现。仅实施偏离那一案的宿主原文保持「实现和验证缺陷」；语义摘要没有改写这个定性。

## Findings

### F-001 · 响应 I-002 时保持语义原文的定性

- 级别：recommended
- 严重度：low
- 关联：I-002、C3
- 证据：`00-meta.md` 信息表 I-002 仍写「待实际运行」；[semantic-results.md](../attachments/semantic-results.md) 与 `attachments/pasted-opinions/codex-audit-implementation-r2/A-001-readonly-opinion-pasted.md` 写明该案是实现不符合已授权计数语义。
- 影响：不阻断本意见。`/govern` 回写 I-002 时，把证据栏改到 E-003 与上述路径，并保留该案原文的定性。验收替代与无关产物两案可以计入「识别为漂移」。`len` 计入空白那一案计入「验收被 required 阻断」，不计入「已识别为漂移」。

无 required finding。

## 必改项汇总

无。

## 与既有意见的异同

A-001（self，conditional）的唯一 required 是 F-001：指定 provider 的正式独立审计尚未落盘。本 A-002 的落盘满足该条件。两份意见都把 S4/C4 留在门外，也都没有把合成探针当作本生产目标的业务缺陷。

这不是 P-004 的持续冲突。A-001 的 conditional 来自当时正式独立意见缺失；本条目返回后，该前提不再成立。F-001 的闭合留痕仍由 `/govern` 写入，本意见不改 A-001 原文，也不把该 finding 标成已闭合。

## 结论 + 建议给编排器/用户的下一步

**pass**。S1–S3 的契约、消费入口和已引用证据支持本 scope：规则缺口有出处，现行入口要求父级贡献与授权连续性，代表性宿主结果在已写明的 L0 边界内。保证等级是 L0，不表示每次模型都会把任意语义偏离标成漂移，也不表示系统级拦截。

建议 `/govern`：

1. 响应本 A-002，把 A-001 F-001 记为 fixed，证据指向本文件与更新后的索引。
2. 按 F-001 的边界更新 I-002 证据并标 verified。
3. 上述响应完成后，S3 可以退出。S4 仍要走已授权的 PR、main CI、annotated 发布和正式资产验收；I-003 继续挡住关门。

## 声明

本意见不修改 status、检查点、派生 progress 或方案正文。响应由 `/govern` 处理。
