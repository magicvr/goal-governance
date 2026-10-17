---
id: GOAL-001-methodology-skills-feedback-evolution
title: 真实项目反馈驱动的协议与 Skills 演进
status: active
parent: null
plan_refs: VP-002-methodology-skills-feedback-evolution
primary_plan: VP-002-methodology-skills-feedback-evolution
serves_summary: delivery Root；服务 VP-002 / vision-goal-governance@0.2.0；承接真实项目与消费方反馈修正协议与 Skills
created: 2026-07-31
updated: 2026-10-17
version: 0.14.35
progress: 67%
---

# GOAL-001 · 真实项目反馈驱动的协议与 Skills 演进

## 概述

GOAL-013 先提交 e37cad3，再完成 S4 cross/全部意见响应/关门审视；A-002 independent/pass、A-004 fixed、A-005 pass，开放 required/recommended 0。子目标 active / 100%（4/4），尚未正式改 done，无待答；见 E-012。Root R3 active / 67% 保持。

在 Charter `vision-goal-governance@0.2.0` 与 **VP-001 奠基有界关** 之后，以**真实项目 / 消费方使用中发现的问题**为触发，持续修正核心方法论与 Skills，使协议在实战中保持可复制、可审计、可安装。

本 Root 是 [workspace-002-methodology-skills-feedback](../workspace.md) 的唯一 `parent: null` 总目标；**不**以本仓 Web 产品清单驱动（人类 UI 见 VP-003）。

## 成功标准（Root 方向级 · 暂定）

- [x] 至少完成 **一轮** 有界「反馈 → 协议/Skills 修正 → 可核对验证」闭环（子目标证据链完整）
- [x] 修正后的协议/Skills 仍满足完整安装与发布门禁（GOAL-003 `v0.12.0` formal Release；A-004 F-001 fixed）
- [ ] 无阻断本波次退出的 required 协议缺口；未关闭项显式 residual（**D-008 退出挂起**；F-006 / R-001 已由 [GOAL-006](../GOAL-006-consumer-surface-convergence/) 于 2026-08-08 关闭；后续 deferred 见 02-execution「后续波次候选」——Codex 矩阵 I-003、matrix candidateRevision R-001、Web writer F-003 等，关门时 residual 留痕）
- [ ] **不**要求「永远修到完美」或关闭 Web 终态

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **R1** | 消费宿主补齐与入口一致 | **完成**（2026-07-31） | claude / copilot / grok 既有；Codex 经 [GOAL-002](../GOAL-002-codex-skills-entry/) 补齐（install 面 + 主入口 runtime）；用户 `/govern` 确认收口（D-003） |
| **R2** | 反馈驱动的协议 / Skills 修正 | **完成**（2026-08-04） | [GOAL-003](../GOAL-003-consumer-governance-ergonomics/) `v0.12.0` 正式 Release / consumer update / A-006 independent pass；F-001 fixed，开放 required = 0 |
| **R3** | 持续闭环与长期演进（原「有界闭环验证与 VP 退出准备」；退出挂起，D-008） | **进行中** | [GOAL-004](../GOAL-004-frozen-web-asset-retirement/) 至 [GOAL-008](../GOAL-008-consumer-layer-split-and-hosting/) 已 done；[GOAL-009](../GOAL-009-info-deadlock-and-managed-placeholders/) 已于 2026-10-01 关门（`done` / 100%，不包含正式发布），开放 required 为无；[GOAL-010](../GOAL-010-release-gate-recapture-and-v0-13-4/) 于 2026-10-01 立项并**同日关门**（`done` / 100%），承载发布门禁转绿与 **`v0.13.4` 正式发布**；**D-008：长期持续治理，退出挂起**，Root/VP-002 保持 active |

同一纲领阶段内可并行多个子目标；阶段间通常串行。

## 派生进度展示

`progress: 67%` = 纲领阶段 R1～R3 中已完成 **2 / 3**（等权：R1/R2 完成，R3 进行中，四舍五入）。R2 恢复完成的依据是 GOAL-003 D-011 与 A-006/A-007；progress **仅展示**，不把 R3 启动推导为 Root `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | Codex CLI / 宿主如何发现并加载 project skills（路径、清单、与 AGENTS 关系） | GOAL-002 方案冻结 | R1 方案 | 读官方/宿主文档 + 对照现有 install 适配器 | **verified**（2026-07-31） | 官方路径变更时复核 | 子目标 [GOAL-002](../GOAL-002-codex-skills-entry/)：I-001/I-002 verified + D-002；证据 [i-001-i-002-…](../GOAL-002-codex-skills-entry/attachments/i-001-i-002-codex-skills-loading-2026-07-31.md)；关门 A-001/A-002 pass（A-002 F-004 触发本台账同步） |
| I-002 | non-blocking | 下一轮真实项目反馈的首批问题清单 | R2 立项优先级 | R2 立项前 | dogfood / 用户提交 | **verified**（2026-08-03） | 新一批反馈出现时追加 | 用户提交 FB-001～FB-005；见 [GOAL-003 D-001](../GOAL-003-consumer-governance-ergonomics/01-decision.md#d-001--将五项实战摩擦纳入同一-r2-大目标2026-08-03) |
| I-003 | non-blocking | 是否需要将 Charter `primary_workspace` 迁到本区 | 叙事一致性 | 用户要求时 | P-004 | open | 用户本轮确认：**001 仍 primary** | 2026-07-31 确认 |
| I-004 | non-blocking | 第二批消费仓质量框架痛点清单 | R3 立项优先级 | 用户提交时 | dogfood / 用户提交 | **verified**（2026-09-13） | 再下一批反馈出现时追加 | 用户提交 FB-006～FB-009；见 [GOAL-008 D-001](../GOAL-008-consumer-layer-split-and-hosting/01-decision/D-001-scope-and-roadmap.md) |
| I-005 | non-blocking | 第三批使用反馈的问题清单 | R3 立项优先级 | 用户提交时 | dogfood / 用户提交 | **verified**（2026-09-30） | 再下一批反馈出现时追加 | 用户提交 FB-010～FB-011；见 [GOAL-009 D-001](../GOAL-009-info-deadlock-and-managed-placeholders/01-decision/D-001-scope-and-roadmap.md)。清单已收到，不证明方案已验证 |

## 愿景对齐

| 项 | 值 |
|----|-----|
| Charter | `vision-goal-governance@0.2.0` |
| primary_plan | [VP-002-methodology-skills-feedback-evolution](../../../vision/plans/VP-002-methodology-skills-feedback-evolution.md) |
| workspace | `workspace-002-methodology-skills-feedback` · `vision_role: delivery` |
| 奠基区 | [workspace-001](../../workspace-001-goal-governance/) · primary · Root done（只读指针） |

## 子目标

| id | title | status |
|----|-------|--------|
| [GOAL-002-codex-skills-entry](../GOAL-002-codex-skills-entry/00-meta.md) | 添加 Codex 可用的 Skills 入口 | done |
| [GOAL-003-consumer-governance-ergonomics](../GOAL-003-consumer-governance-ergonomics/00-meta.md) | 修复消费仓门禁与长流程治理摩擦 | done |
| [GOAL-004-frozen-web-asset-retirement](../GOAL-004-frozen-web-asset-retirement/00-meta.md) | 移除冻结 Web 资产并挂起 VP-003 | done |
| [GOAL-005-vision-review-ledger-scaling](../GOAL-005-vision-review-ledger-scaling/00-meta.md) | 愿景审视台账分片与正式发布 | done |
| [GOAL-006-consumer-surface-convergence](../GOAL-006-consumer-surface-convergence/00-meta.md) | 消费面路径收敛（F-006 承接 + R-001 扫尾） | done |
| [GOAL-007-workspaces-directory-consolidation](../GOAL-007-workspaces-directory-consolidation/00-meta.md) | 工作区目录统一收敛与正式发布 | done |
| [GOAL-008-consumer-layer-split-and-hosting](../GOAL-008-consumer-layer-split-and-hosting/00-meta.md) | 双层路线图拆分与消费仓宿主共存 | done |
| [GOAL-009-info-deadlock-and-managed-placeholders](../GOAL-009-info-deadlock-and-managed-placeholders/00-meta.md) | 未知信息门禁死锁与受管占位符升级 | done |
| [GOAL-010-release-gate-recapture-and-v0-13-4](../GOAL-010-release-gate-recapture-and-v0-13-4/00-meta.md) | 发布门禁转绿与 v0.13.4 正式发布 | done |
| [GOAL-011-standalone-bootstrap-distribution](../GOAL-011-standalone-bootstrap-distribution/00-meta.md) | 修复 issue #24：独立启用说明的消费分发与引用 | done |
| [GOAL-012-release-v0-13-5](../GOAL-012-release-v0-13-5/00-meta.md) | v0.13.5 正式发布与消费资产验收 | done |
| [GOAL-013-audit-dispatch-and-user-input-gates](../GOAL-013-audit-dispatch-and-user-input-gates/00-meta.md) | 独立审计命令派发与用户答复阻塞门禁 | done |
| [GOAL-014-release-v0-13-6](../GOAL-014-release-v0-13-6/00-meta.md) | v0.13.6 正式发布与消费资产验收 | done |
| [GOAL-015-audit-command-labeled-form](../GOAL-015-audit-command-labeled-form/00-meta.md) | 审计命令带标签形式修正（workspace-/goal-/vp-） | done |

## 备注

- **GOAL-015 立项与 S2/S3（2026-10-17）**：用户指出形式审计命令应为 `/audit workspace-<工作区编号> goal-<目标编号>` 与 `/vision-audit vp-<vp编号>`，而 [GOAL-013](../GOAL-013-audit-dispatch-and-user-input-gates/00-meta.md) 的契约写成了裸数字形式。创建 [GOAL-015](../GOAL-015-audit-command-labeled-form/00-meta.md) 恢复用户原始形式；[D-001](../GOAL-015-audit-command-labeled-form/01-decision/D-001-scope-and-roadmap.md) 冻结范围（含本次实施，不含运行证据重捕获与发布），[D-002](../GOAL-015-audit-command-labeled-form/01-decision/D-002-labeled-command-contract.md) 冻结带标签语法与写集。同步卡片真实返回 Q-001 = A、Q-002 = Grok Build，审计模式 `cross`。canonical、根 AGENTS、prompts、四宿主安装源、规则模板、MCP 与契约测试已同改，镜像 38 对一致、dogfood 16 对一致；skills 102 / docs 67 回归 OK。**已知后果**：16 份运行记录因 24 个 behaviorSources 变更全部过期，scripts 147 红（4 failures / 12 errors），release/compatibility 门禁在重捕获前保持红；重捕获按用户裁决留在本目标外。GOAL-015 经用户 2026-10-17 指令「闭门」收尾为 **done / 100%（S1～S5 5/5）**：S5 全链路完成——16 格运行证据重捕获 **16/16 pass**（一致性 `--check` 22 份、`compatibility_report` `ready-for-release-evidence`）、清单与 CHANGELOG `0.13.7` 同步、本地门禁 skills 102 / docs 67 / scripts 147 全绿、strict rehearsal 与 strict 预检 `checks passed: True`；检查点 `8f1315f` → [PR #31](https://github.com/magicvr/goal-governance/pull/31) 双平台 CI 全绿 → merge `6ca04ee` → annotated `v0.13.7`（tag object `6197ed6e`）→ tag run 39034827440 的 pack 与 gated publish 全绿（Environment `release` 由维护者 `magicvr` 人工审批，AI 未代批）→ [Release v0.13.7](https://github.com/magicvr/goal-governance/releases/tag/v0.13.7) 2026-10-17T13:10:14Z 发布 9 项资产；资产逐项验收通过（双 ZIP 摘要与 sidecar 一致、Core 27 成员为 Skills 86 成员的逐字节子集、下载资产驱动的隔离消费安装 exit 0 且消费者自有规则保留、GHCR digest 与日志一致且内置版本 `0.13.7`）。过程更正：Copilot 5 格首轮 401 系**编排侧派发环境未继承 `COPILOT_PROVIDER_API_KEY`**（User 作用域有、Process 为空），非凭据失效；runner 注入后以 `-r2` 重取全部 pass。审计：A-005 independent（Grok Build）对 S5 退出条件 a–f 判 `pass`、A-006 响应全部意见，**开放 required 0 / 开放 recommended 0**；[D-004](../GOAL-015-audit-command-labeled-form/01-decision/D-004-close-out.md) 记录关门决定与 L0 边界，[E-009](../GOAL-015-audit-command-labeled-form/02-execution/E-009-close-out-sync.md) 记录收尾同步。遗留非阻断项（矩阵下一轮 `candidateRevision` 准备、消费方自查面纳入命令形式）建议另立 GOAL-016。Root R3 / VP-002 保持长期 active，Root progress 67% 不变；下一编号 GOAL-016。

- **v0.13.6 正式发布与 GOAL-014 关门（2026-10-17）**：PR #29 经双平台 CI 全绿后合入 main（merge `97f6f1ea`），main CI 38999290522 success；annotated `v0.13.6` 指向该 merge，tag workflow 39000107099 的 pack 与 gated publish 全绿，Environment 回执为 magicvr 人工 `skipped`（AI 未代批）。[Release](https://github.com/magicvr/goal-governance/releases/tag/v0.13.6) 9 项资产、双 ZIP 摘要、Core 子集、隔离消费安装与 GHCR 镜像均核对通过；A-001 independent/pass、A-002 fixed、A-003 关门审视 pass，无开放 required，I-001～I-006 verified。D-003 将 [GOAL-014](../GOAL-014-release-v0-13-6/00-meta.md) 标为 **done / 100%（S1～S4 4/4）**，见 E-004/E-005 与附件。Root R3 / VP-002 保持长期 active，Root progress 67% 不变；下一编号 GOAL-015。

- **GOAL-014 立项与 S2 完成（2026-10-17）**：用户在 GOAL-013 关门后要求「提交 PR、CI 全绿后合并 main、打 tag 发布新资产」。另建 [GOAL-014](../GOAL-014-release-v0-13-6/00-meta.md) 承载下一个兼容性 patch **v0.13.6** 的正式发布与消费资产验收；[D-001](../GOAL-014-release-v0-13-6/01-decision/D-001-release-scope.md) 冻结范围与证据策略（复用 GOAL-013 S3 的 16 份现行运行证据，协议 0.1.0 与 consumer contract 不变）。E-001 基线：远端最新 v0.13.5、v0.13.6 未占用，证据 `--check` 与 compatibility ready。E-002/E-003：清单检查点 `5de854d`、本地 rehearsal 与 strict release 预检通过；provider 由用户指定为 Grok Build（D-002），`/audit 002 014` 返回 A-001 independent/pass、开放 required 0，建议项经 A-002 fixed。S1/S2 完成、S3 进行中，progress 50%。Root R3 / VP-002 保持长期 active，Root progress 67% 不变；下一编号 GOAL-015。

- **GOAL-013 关门（2026-10-17）**：用户指令闭门；[D-005](../GOAL-013-audit-dispatch-and-user-input-gates/01-decision/D-005-close-out.md) 依 A-001 self/pass、A-002 Grok independent/pass、A-004 全部 `fixed`、A-005 关门审视 pass（开放 required/recommended 0，I-001～I-005 在路径 A 范围内 verified）将子目标收尾为 **done / 100%（S1～S4 4/4）**。交付边界照 A-005：规范、现有入口消费与已列代表运行，保证等级 L0，不新增系统级硬拦截；本目标内未 tag、未发布，v0.13.6 正式发布另立目标。Root R3 / VP-002 保持长期 active，Root progress 67% 不变；见子目标 E-013。

- **GOAL-013 S2 完成（2026-10-16）**：路径 A 的 canonical、prompts、四宿主入口/MCP guidance、待答模板及镜像已同步并通过回归/隔离安装；子目标 active / 50%（2/4）。旧 12 份 runtime 证据对当前工作树过期，I-004 保持 S3 门禁；S3/S4 未开始，Grok Build provider 保持。Root R3 active / 67% 不变，见子目标 E-004。

- **GOAL-013 S1 完成（2026-10-16）**：用户同步卡片采纳 A 现有入口规范化、指定 Grok Build，子目标 D-003 冻结。真实答复解除待答阻塞，active / 25%（1/4），S2 未开始；实际宿主问答仍按 I-004 于 S3 验证。Root R3 active / 67% 保持。

- **GOAL-013 S1 调查（2026-10-16）**：命令契约、四宿主能力与验收用例已提出，D-002 待裁决；当前 blocked / 0%，等待真实用户答复后判断 S1 退出与后续实施路径。Root R3 active / 67% 保持。

- **独立审计与答复门禁反馈（2026-10-16）**：用户要求本区新建 [GOAL-013](../GOAL-013-audit-dispatch-and-user-input-gates/00-meta.md)，承载自动审计只输入正式命令与用户询问空答复暂停/目标 blocked 两项约束。active / 0%，先登记 S1～S4 与信息门禁，尚未实施；Root R3 进行中、progress 67% 保持，下一编号 GOAL-014。

- **v0.13.5 正式发布（2026-10-15）**：[GOAL-012](../GOAL-012-release-v0-13-5/00-meta.md) 完成 PR #27 → main `1a6668e` → annotated tag → run 38691121485 → 9 项资产验收及隔离消费安装，MCP 镜像拉取/内置版本通过；A-003 close-out pass，无开放 required，done / 100%。Root R3 / VP-002 保持长期 active，Root progress 67%，下一编号 GOAL-013；见子目标 E-004/E-005。

- **v0.13.5 发布立项（2026-10-15）**：用户要求将已合入的 GOAL-011 修复发布为新版本资产，另建 [GOAL-012](../GOAL-012-release-v0-13-5/00-meta.md) 承载正式发布与验收。Root R3 持续演进，progress 保持 67%；下一编号 GOAL-013。

- **GOAL-011 关门（2026-10-15）**：修复由 PR #25 经双平台 CI 合入 main，issue #24 已关闭并回读；子目标 A-004 pass、无开放 required，done / 100%。未发布新版本。R3 与 VP-002 保持长期 active，Root progress 仍为 67%，下一编号 GOAL-012；见子目标 E-005。

- **issue #24（2026-10-15）**：用户要求在本区建子目标、修复后关闭 issue；创建 [GOAL-011](../GOAL-011-standalone-bootstrap-distribution/00-meta.md) 承接独立启用说明的消费分发与引用问题。方案与 cross provider 尚待裁决，尚未实施。Root R3 持续进行、progress 仍为 67%；下一编号 **GOAL-012**。

- 开区决策见 [01-decision.md](01-decision.md) D-001；R1 收口见 **D-003**；R2 启动见 **D-004**；R3 启动见 **D-006**。
- 编号自 GOAL-001 起；**不**延续 workspace-001 的 GOAL-024+。
- R1 收口 **不**等于 Root 成功标准全勾、**不**等于 VP-002 可关门；GOAL-002 I-003（矩阵 committed）仍 non-blocking residual，不阻断 R1。
- **F-006 承接（2026-08-08）**：跨区移交的消费面路径收敛项（workspace-003 A-012 F-006）并入 VP-002 消费面承接路线图，与 R-001 裸路径扫尾合并跟踪；recommended 级，执行触发 = VP-002 推进或下一次协议面修订（登记见 `docs/vision/plans/VP-002-…md` 与 02-execution 待办 4）。GOAL-006 已于 2026-08-08 done，F-006/R-001 实现关闭。
- **长期持续治理（2026-08-08，D-008）**：用户确认 workspace-002 与 VP-002 为长期持续治理项目，暂不关门——退出判据挂起（核对结论留档 D-008）；R3 转为「持续闭环与长期演进」；Root/VP 保持 active；新工作按反馈随时立项。
- **工作区目录收敛（2026-08-10）**：用户反馈工作区直属 `docs/` 在多区后影响查阅，创建 GOAL-007；2026-08-11 已 `done`。
- **第二批消费仓痛点（2026-09-13，D-009）**：创建 [GOAL-008](../GOAL-008-consumer-layer-split-and-hosting/) 承载 FB-006～FB-009；该目标已于 2026-09-13 `done`。
- **第三批使用反馈（2026-09-30，D-010）**：创建 [GOAL-009](../GOAL-009-info-deadlock-and-managed-placeholders/) 承载 FB-010～FB-011；S1 完成前不改协议/安装/Skills；下一编号 **GOAL-010**。
- **GOAL-009 关门（2026-10-01）**：用户书面确认关门且不发布。GOAL-009 为 `done` / 100%，开放 required 为无。F-003 仍为 recommended。R3 仍进行中，Root progress 仍为 67%。关门后对齐回滚测试桩与本表 R3 当前说明，见 GOAL-009 [E-014](../GOAL-009-info-deadlock-and-managed-placeholders/02-execution/E-014-post-close-alignment.md)。
- **发布门禁转绿与 v0.13.4 发布（2026-10-01，D-011）**：GOAL-009 关门后发现 `dev` 顶端发布门禁为红——GOAL-009 S2 改根 `AGENTS.md` 与编排提示使 v0.13.3 的 12 格 runtime 证据全部过期，publish job 的 `--mode release` 首步即失败。创建 [GOAL-010](../GOAL-010-release-gate-recapture-and-v0-13-4/) 承载「重捕获 12 格证据 + 修 containment 测试 + 版本清单 + PR/合并/tag 发布」。版本 **`v0.13.4`（patch）**；修复走重捕获而非回滚。**同日关门**：GOAL-010 为 `done` / 100%，`v0.13.4` 已正式发布（PR #23 → merge `43479838…` → annotated tag `v0.13.4` → 9 项资产、zip 摘要与 sidecar 一致）；A-002 independent `pass`、开放 required = 0。Root R3 与 VP-002 保持 active、Root progress 保持 67%。下一编号 **GOAL-011**。
