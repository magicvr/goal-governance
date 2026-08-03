---
id: GOAL-003-consumer-governance-ergonomics
doc: audit-entry
record_id: A-004
source: independent
scope: GOAL-003 close-out intention + consumer upgrade README at HEAD 7c4548b
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# A-004 · 意图达成与消费仓升级指南复核

## 范围与区间

- **auditor**：Codex `$audit`（当前独立入口会话）
- **audit_type**：close-out + ad-hoc
- **workspace**：`workspace-002-methodology-skills-feedback`
- **revision**：本地 `HEAD 7c4548b`；正式消费版本对照 `v0.11.0`
- **covered**：FB-001～FB-005、六条成功标准、I-001～I-007、S1～S7、当前实现与测试、消费仓 README 升级指南、正式 Release / compatibility 门禁边界
- **excluded**：创建 tag / Release、修改 lifecycle 状态、替用户接受 residual；这些不属于独立审计写权限
- **保证边界**：本意见属于 P-003 的 L0 入口分离，不等于外部鉴证

## 成果（有证据）

1. **producer / consumer 证据边界已落到源码与消费安装回归**：`docs/contracts/skills-consumer-contract.json` 的 `evidenceBoundary` 只把 consumer contract + schema 列为消费必需；真实 Windows installer 更新回归确认三个 producer-only 文件不进入消费包。
2. **ledger 新布局与兼容读取已落地**：新目标使用 D/E/A 平铺目录；Web reader 合并 legacy inline 与目录条目；GOAL-003 自身保留 D-001～D-008 inline，并从 D-009/E-001/A-001 起 dogfood additive migration。
3. **风险审计与 checkpoint 契约已落地，并有本目标实用证据**：`skills/prompts/00-govern-orchestrator.md` 固定四级风险表、provider fail-closed 与 owned-path checkpoint；本目标实际形成 `51872c9`、`ef39f9c`、`ac6a741`、`c1736b8`、`d4442e1` 等有界提交。
4. **事务 updater 已实现并通过当前回归**：`skills/update.py` 覆盖 fixed/latest、在线/离线 SHA-256、zip 安全、协议 minor 守卫、managed-file 冲突、备份、失败恢复与安装状态；相关离线、真实 installer、冲突和恢复测试通过。
5. **当前源码 README 已有消费仓升级指南**：`skills/README.md`「已安装 Skills 更新（无需重装）」给出 PowerShell/Bash 的固定版本、`--latest`、`--dry-run`、离线 `--zip-path` 命令，并说明 Python 3、摘要/协议/本地修改检查、备份、自动恢复和显式 override 边界。
6. **本轮复跑**：docs `26 passed`；Web `143 passed, 1 skipped`；Skills/pack/bootstrap/updater/mirror `66 passed, 2 skipped`；mirror `34 pairs matched`。skip 分别是 Windows symlink privilege 与不可用 WSL Bash，未伪装为通过。

## 对照成功标准

| 成功标准 | 本轮判定 | 证据与边界 |
|----------|----------|------------|
| consumer 不继承 producer runtime 门禁 | **达成（当前源码）** | consumer contract、installer allowlist、真实消费更新回归；producer 门禁仍独立存在 |
| ledger 确定规则、索引、迁移与旧格式兼容 | **达成 additive migration；自动迁移证据不足** | 模板/reader/GOAL-003 dogfood 通过；见 F-003 |
| 四级审计与 provider / P-004 | **达成（Skills 契约 + dogfood）** | orchestrator 规则、A-001～A-003 cross close-out；provider 失败仍 fail closed |
| 长流程安全 checkpoint | **达成（Skills 契约 + 实际提交）** | owned paths / validation 规则；本目标提交链可核对 |
| 已安装 Skills 可发现并应用兼容更新 | **部分达成** | 当前源码和测试具备 updater；最新正式消费版本不含 updater，见 F-001 |
| canonical / mirrors / tests / 发布准备一致 | **部分达成** | 本地回归与 mirror 通过；producer compatibility readiness 当前失败，见 F-001 |

## README 版本升级指南确认

**当前 `dev` 源码中已经补充，位置正确且核心操作足够可执行**：

- `skills/README.md` 第 141～162 行：消费仓更新命令与安全边界；
- `scripts/bootstrap/README.md` 第 77～79 行：首次安装用 bootstrap，包含 updater 的包之后走 `skills/update.*`；
- 根 `README.md` 第 20、90 行可进入 `skills/README.md`。

但这只能证明**源码文档已补充**，不能证明正式消费包已经交付该指南和 updater。当前根/Skills README 仍 pin `v0.11.0`，而该 tag 不含 `skills/update.py`、`update.ps1` 或 `update.sh`；详见 F-001。

## Findings

### F-001 · 正式消费版本未承载 updater，且当前 producer compatibility 门禁失败

| 字段 | 值 |
|------|-----|
| severity | med |
| level | required |
| status | open |
| 影响门禁 | GOAL-003 close-out 的「已安装 Skills 可升级」与 S7 发布准备主张 |

**证据**：

1. 2026-08-04 实时执行 `gh release list --repo magicvr/goal-governance`：最新正式 Release 仍为 `v0.11.0`（2026-07-30T22:31:57Z）。
2. `git ls-tree -r v0.11.0 -- skills/update.py skills/update.ps1 skills/update.sh skills/README.md` 只返回 `skills/README.md`；`git diff --name-status v0.11.0..HEAD` 显示三个 updater 文件为后续新增，升级指南也是后续修改。
3. 根 `README.md` 与 `skills/README.md` 仍把 `v0.11.0` 作为最新正式安装 pin；`CHANGELOG.md` 同时写着 `Unreleased` 为“无”。现有正式消费仓因此拿不到 updater，也拿不到本轮新增指南。
4. 当前执行 `python scripts/compatibility_report.py --require-ready` 失败：`runtime evidence behavior source is stale: skills/prompts/00-govern-orchestrator.md`。这正是 GOAL-003 修改过的行为源，说明 producer 发布门禁没有被本轮 26/143/66 回归替代。

**影响**：源码实现可以称为“implemented / locally verified”，但不能称为“现有消费仓已经可版本升级”或“发布准备门禁已满足”。A-001/A-002 把实际 Release 与 producer runtime evidence 排除出 close-out，而成功标准使用了已安装消费仓的现在时能力；两者口径不一致。

**关闭要求（建议 fixed）**：由 `/govern` 建立受控发布切片，冻结新的 SemVer/candidate identity 与 `CHANGELOG`，刷新受影响 behavior-source runtime evidence，使 `compatibility_report.py --require-ready` 与严格 release evidence 通过；经用户授权后创建 annotated tag / Release，并同步 README pin。最后从正式 Release zip 核对 updater、升级指南、consumer-only contract profile 与一次真实消费仓更新。若不准备交付正式版本，则须由用户书面选择 `accepted-residual` 或 `user-overruled`，并把目标主张收窄为“源码实现 / release-ready candidate”，不得保留“现有消费仓已可升级”的无条件表述。

### F-002 · 升级指南可发现性与人工回滚说明仍可加强

| 字段 | 值 |
|------|-----|
| severity | low |
| level | recommended |
| status | open |

`skills/README.md` 已覆盖常用升级命令和失败自动恢复，足以确认“指南已补充”。但根 README 的导航仍只写“Skills 如何安装”，没有直接标明“安装 / 升级”；README 也只说成功后输出 `rollback_path`，未说明成功更新后如何用该目录进行人工回滚。建议在 F-001 的版本发布修复中补一个根入口和最小人工恢复步骤，不阻断当前 required 门禁判断。

### F-003 · `migration dry-run` 记录强于现有可执行证据

| 字段 | 值 |
|------|-----|
| severity | low |
| level | recommended |
| status | open |

`01-decision.md` D-004 要求迁移工具先 dry-run，I-007 的验证动作也写有迁移 dry-run；本轮仓库检索未找到 ledger migrator 或对应 dry-run/equivalence 测试。当前可证明的是**additive migration + 兼容合并读取**，不是自动迁移工具。建议补迁移 dry-run/等价性测试，或在后续响应中明确把承诺收窄为 additive migration，避免把程序性约束写成已执行事实。本项不否定新布局与 legacy 兼容已落地。

## 必改项汇总

- **F-001（required / open）**：当前正式消费版本与 producer compatibility 门禁尚未承载本轮 updater/行为源变更；在 fixed、accepted-residual 或 user-overruled 留痕前，不应继续宣称 GOAL-003 的消费仓升级意图已无条件达成。

## 与既有意见的异同

- 与 A-001/A-002 一致：当前源码实现、主要测试、mirror、consumer/producer profile 与 updater 事务路径均真实存在。
- 与 A-001/A-002 不同：它们明确排除了实际 GitHub Release 与 producer runtime evidence；本轮按用户所问“确实达成意图”和“消费仓版本升级”核对了正式消费边界，发现 F-001。
- A-001/A-002 主张 close-out 可通过，而本意见以 open required F-001 阻断同一 close-out 口径，构成 P-004 的门禁意见冲突；独立审计不替用户裁决。

## 结论与建议

**verdict: conditional**。GOAL-003 的源码实现和本地验证大体达成，README 升级指南也确实已写入当前 `skills/README.md`；但正式消费版本仍是没有 updater 的 `v0.11.0`，当前 compatibility readiness 也失败，因此不能确认“我们的消费仓升级意图已经确实达成”。建议用 `/govern` 响应 A-004 F-001，优先走 fixed 的版本冻结与正式发布闭环。

## 声明

本意见只追加 independent audit ledger，不修改目标 `status`、检查点、`progress`、Root 或 `goal-tree.md`；响应与 lifecycle 处理由 `/govern` 和用户负责。
