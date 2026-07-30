---
title: Goal Tree · 目标树与进展总览
status: active
created: 2026-07-18
updated: 2026-07-30
parent: null
version: 1.1.15
---

# Goal Tree

## 2026-07-30 · GOAL-022 响应 A-001 + 阶段 F 关门（D-003）

`/govern`：F-001 **accepted-residual** R-022-ORPHAN-PRUNE；F-002 **accepted-residual** R-022-INSTALL-TEMPLATES-COPY；F-003 **fixed**（Root meta/decision 现时注）。A-002 response + A-003 self close-out **pass** → GOAL-022 **`done / 100%`**。开放 required = 0。关门前：docs 26 / scripts 52（2 skip）/ skills 39 OK；`stage --check` 28 pairs ok。**未** tag/Release；Root 仍 `active`。下一编号 **GOAL-023**。

## 2026-07-30 · GOAL-022 阶段 A～E 落地（D-002）

`/govern`：用户确认 I-001～I-003 推荐默认并立即实现。`stage_skills_mirrors.py` + pack/CI 挂接；`skills/templates` 收敛为指针；core 精简 README；契约 mirrorPath → `skills/core/docs/templates/goal-folder`。回归：docs 26 / scripts 52（2 skip）/ skills 39 OK；`stage --check` ok。status 曾为 `active / 83%`；关门见上节。**不** tag/Release。

## 2026-07-30 · 创建 GOAL-022（方法论 SSOT + Skills 镜像 stage）

`/govern` 路径 D 单点：新建 [GOAL-022-docs-ssot-skills-mirror-stage](GOAL-022-docs-ssot-skills-mirror-stage/)，承接「只维护 `docs/` canonical，pack/stage 生成镜像」改造。D-001 立项；其后 D-002 见上节。下一编号 **GOAL-023**。

## 2026-07-30 · GOAL-021 阶段 G 自审与确认关门

`/govern`：A-003 self close-out **pass**；D-003 用户确认 → GOAL-021 **`done / 100%`**。开放 required = 0；residual R-021-RUNTIME-RECAPTURE / R-021-SYMLINK-CI（non-blocking）。关门前回归：docs 26 / scripts 49（2 skip）/ skills 39 OK。**未** tag/Release；Root 仍 `active`。当前无未关门子目标。下一编号 **GOAL-022**。

## 2026-07-30 · GOAL-021 响应 A-001：F-001～F-005 fixed（D-002）

`/govern` 按建议顺序 **fixed** 闭合 A-001 全部 findings（含 P2 F-005）。[D-002](GOAL-021-skills-release-chain-hardening/01-decision.md) / [A-002](GOAL-021-skills-release-chain-hardening/03-audit.md)。其后阶段 G 关门见上节。

## 2026-07-30 · 创建 GOAL-021（Skills 执行链加固）

`/govern` 路径 D 单点：新建 [GOAL-021-skills-release-chain-hardening](GOAL-021-skills-release-chain-hardening/)，承接执行链对抗审 **A-001**。阶段 A 落盘后由 D-002 响应 F-001～F-005（见上节）。下一编号 **GOAL-022**。

## 2026-07-30 · 路径 D 授权 v0.9.2：本地 release-candidate 通过（D-026）

用户书面授权 annotated **`v0.9.2`**。首轮因 12 宿主证据 stale 失败 → 2026-07-30 全量 runtime 重采 pass → 矩阵/测试对齐 → tag `v0.9.2` @ `b491e3a` → `release_evidence --mode release` **checksPassed: true**（`artifacts/release-evidence-v0.9.2.json`）。**未** push tag / **未** GitHub Release（须 Environment `release`）。**不**改各 GOAL status/progress；Root 仍 `active`。

## 2026-07-30 · 路径 D 可选卫生（README 四入口装机树 + Goal 三入口历史注）

`/govern` 路径 D：修正 `skills/README.md` 装机树/手动安装/参数表为默认四入口（+ `vision-audit`）；GOAL-001 D-018/执行 D-018·D-019 历史「三入口」加现时注（指向 D-020）。**不**改各 GOAL status/progress；**不** tag；Root 仍 `active`。

## 2026-07-29 · GOAL-020 阶段 E 与用户确认关门

[GOAL-020-methodology-adversarial-audit-fix](GOAL-020-methodology-adversarial-audit-fix/) 已由 D-005/A-005 `done / 100%`：A-001 independent；A-002/A-003 响应；A-004 self close-out `pass`；F-001～F-009/F-011 closed；F-010 recommended non-blocking follow-up；I-001～I-003 closed。Docs 22 / Skills 39 passed，canonical/core 哈希一致。路径 D 单点协议质量工作；**不**重开 GOAL-006；**不**改 Root/Charter/VP status；阶段 7仍延期。下一编号 **GOAL-021**。

## 2026-07-29 · 响应 GOAL-001 A-018（D-025 · 路径 D）

`/govern` 按用户优先序 **fixed** 闭合 A-018 **F-012～F-015**（F-016 顺手）：standalone 冷启动对齐 P-006；core 分发 `vision/alignment.md`；权威面 P-006；AGENTS dogfood/消费门禁对齐。[D-025](GOAL-001-main-vision/01-decision.md#d-025--响应-a-018p-006-后核心包--standalone--agents-回流2026-07-29) / [A-019](GOAL-001-main-vision/03-audit.md#a-019--响应-a-018-f-012f-0152026-07-29)。测试：standalone 3 ok；skills orchestrator 38 ok。**不**改各 GOAL status/progress；**不** tag；Root 仍 `active`。

## 2026-07-28 · 路径 D：发版候选 runtime 验证（不发版）

`/govern` 路径 D：compatibility **ready-for-release-evidence**（12 宿主入口 runtime-verified，unreleased）；release rehearsal **checksPassed**。产物：`artifacts/compatibility-report-path-d-check.json`、`artifacts/release-evidence-path-d-rehearsal-2026-07-28.json`。修正 test 硬编码 v0.9.1→unreleased。**v0.9.1 已 tag**；下一 tag 须授权（建议 v0.9.2）。**无** tag/Release；**不**改各 GOAL status/progress。

## 2026-07-28 · 响应 GOAL-001 A-015 F-008（路径 D）

用户采用 **路径 D**（仅维护发版/协议，不关 Root）。[D-024](GOAL-001-main-vision/01-decision.md#d-024--a-015-f-008-路径-d仅维护发版协议不关-root2026-07-28) / [A-017](GOAL-001-main-vision/03-audit.md#a-017--响应-a-015--f-008路径-d契约2026-07-28) 关闭 **F-008**（`fixed`）。GOAL-018/019 归属 **Skills 维护波次**；阶段 7 **延期未开**；A/B/C 改道须新裁决。R-009-X 仍 accepted。**不**改各 GOAL status/progress；Root 仍 `active`。

## 2026-07-28 · 响应 GOAL-001 A-015 F-007（现时摘要刷新）

`/govern` 关闭 A-015 **F-007**（`fixed`）：Root [00-meta 现时摘要](GOAL-001-main-vision/00-meta.md#现时摘要2026-07-28-单一权威入口) 与 [02-execution 当前进展/下一步](GOAL-001-main-vision/02-execution.md#当前进展2026-07-28) 已对齐 018/019 done、D-016～D-023、愿景栈与 **下一编号 GOAL-020**。[A-016](GOAL-001-main-vision/03-audit.md#a-016--响应-a-015--f-007刷新-root-现时摘要2026-07-28)。其后 F-008 由路径 D 关闭（见上节）。**不**改各 GOAL status/progress；Root 仍 `active`。

## 2026-07-28 · 响应 V-F-001：独立 Vision Review 专用入口（GOAL-001 D-020；不发版）

用户按 P-004 选择新增 `/vision-audit`，不扩展 `/audit`。核心 `07`、三宿主默认安装与消费者契约已同步；[VRev-002](../vision/reviews.md#响应--v-f-0012026-07-28) 以 `fixed` 闭合入口缺口。新入口三宿主 runtime 仍 pending，矩阵为 `unreleased`。**不**改任何 Goal status/progress。详见 [D-020](GOAL-001-main-vision/01-decision.md#d-020--响应-v-f-001独立-vision-review-专用入口2026-07-28)。

## 2026-07-28 · `/vision` follow-through（GOAL-001 D-019；不发版）

Dual-pass runtime：Claude+Grok vision **pass**；Copilot **quota fail** → pending。VRev-001；消费 AGENTS 同步 P-006。**无**正式发版。详见 [D-019](GOAL-001-main-vision/01-decision.md#d-019--vision-follow-throughruntime--消费面--vrev不发版2026-07-28)。

## 2026-07-28 · Skills `/vision` 第二刀（GOAL-001 D-018）

落地 `06-vision-orchestrator` 与默认 install 三入口（govern/audit/vision；**当日**面，其后 D-020 扩为四入口）；契约矩阵 vision=pending-runtime-validation。**不**改各 GOAL status/progress。详见 [D-018](GOAL-001-main-vision/01-decision.md#d-018--skills-vision-决策层第二刀2026-07-28)。

## 2026-07-28 · P-006 愿景组合治理第一刀（GOAL-001 D-017）

用户确认 D0–D24 并落盘：P-006；alignment **0.3.0**；取消 sandbox opt-out；冷启动 Charter→VP→区；`reviews.md`；AGENTS **0.10.0**；编排器 **0.9.0**；vision 模板。**不**改各 GOAL status/progress；Root 仍 `active`。`/vision` skill 为第二刀。详见 [D-017](GOAL-001-main-vision/01-decision.md#d-017--p-006-愿景组合治理与级联对齐第一刀2026-07-28) / [执行](GOAL-001-main-vision/02-execution.md#2026-07-28--p-006-愿景组合治理第一刀d-017)。

## 2026-07-28 · 0.9.1 外部消费准备（A0 后）

外部仓需用 A0：CHANGELOG Unreleased 记 **0.9.1** 候选；预打包 `dist/goal-governance-skills-v0.9.1-rc.1.zip`。历史：**v0.9.1** 已 annotated tag。其后工作树矩阵为 **`unreleased`**（四入口 × 三宿主 runtime-verified；path-D 2026-07-28 验证 ready）。下一 tag 须另授权。

## 2026-07-28 · A0 目标限定引用（GOAL-010 D-003）

用户确认：短 id 不变；文档默认 **Q2** 路径、对话默认 **Q3** 标签；挂 [GOAL-010](GOAL-010-core-workspace-shared-materials-protocol/) **不重开**。workspace-protocol **0.5.0** §2.6；AGENTS **0.9.2**；Skills 00～05 与 core 镜像已同步。**未**做 Web A1/A2；**未**改各 GOAL status/progress。详见 [D-003](GOAL-010-core-workspace-shared-materials-protocol/01-decision.md#d-003--a0-限定引用与展示消歧不改-goal-id-形状2026-07-28) / [执行](GOAL-010-core-workspace-shared-materials-protocol/02-execution.md#2026-07-28--a0-限定引用落地d-003--不重开本目标)。

## 2026-07-28 · 核心协议逻辑一致性修订（GOAL-001 D-016）

用户审视并确认修订：P-003 finding 三路径闭合、P-004.3/4.4、legacy 隐式工作区唯一路径、纲领串行/阶段内并行、Primary 冲突与 VP 14 日空转等。权威：principles **0.6.0**、workspace-protocol（当时 **0.4.0**，其后 D-003 → **0.5.0**）、alignment **0.2.0**；AGENTS/编排器已同步。验证：workspace/vision/standalone + skills orchestrator 测试 OK。**不**改各 GOAL status/progress；Root 仍 `active`。详见 [GOAL-001 D-016](GOAL-001-main-vision/01-decision.md#d-016--核心协议逻辑一致性修订finding-闭合--隐式工作区--p-004-扩表2026-07-28) / [执行](GOAL-001-main-vision/02-execution.md#2026-07-28--核心协议逻辑一致性修订d-016)。

## 2026-07-24 · v0.9.0 发版冻结准备（PR）

CHANGELOG 0.9.0；矩阵 `candidateRevision: v0.9.0`；Copilot 两路 2026-07-24 runtime-verified；Claude/Grok 四格 pending（鉴权失败）。**正式 tag 前须补齐 pending 单元**。GOAL-019 仍 done。

## 2026-07-24 · GOAL-019 有界关门

D-007 / A-002–A-003：响应 A-001；F-001/F-002 closed；F-003/I-005/I-001 residual。GOAL-019 **`done / 100%`**。下一编号 **GOAL-020**。

## 2026-07-24 · GOAL-019 阶段 C 实现

D-006：可选 `--init-workspace`（显式 slug）；隔离冒烟 PASS。其后关门见上节。

## 2026-07-24 · GOAL-019 阶段 B 实现

S0 scaffold + D-005 slug 用户确认；AGENTS/00/01/wrapper 去掉 architecture「可选」定位。其后阶段 C 见上节。
## 2026-07-24 · GOAL-019 阶段 A 实现

`skills/core/` 镜像 + install 默认装 docs + pack 校验 + README 最小可运行集。其后阶段 B 见上节。
## 2026-07-24 · GOAL-019 D-004（Core 清单 · 关闭 I-004）

用户确认：principles + workspace-protocol + overview/layout（去 monorepo 段）+ templates + 精简 docs/README；**不装** tech-stack。其后阶段 A 见上节。
## 2026-07-24 · GOAL-019 D-003（核心与 Skills 同级必备）

用户裁决：方法论与 Skills 同级必备；方案 **A** = zip 内嵌 core + install 默认安装。D-002 superseded。其后 D-004 见上节。

## 2026-07-24 · 创建 GOAL-019（Skills 消费方工作区骨架）

D-001 / D-002（后被 D-003 修订）：立项关闭「装 Skills ≠ 有治理存储」缝隙。[GOAL-019-skills-consumer-workspace-bootstrap](GOAL-019-skills-consumer-workspace-bootstrap/) · 其后 D-003 见上节。下一编号 **GOAL-020**。

## 2026-07-22 · Skills v0.8.0 自动发版成功

PR #2 合并；annotated `v0.8.0`；Actions `29882635335` pack+publish success；Release 含 skills zip/sha256/evidence。R-018 closed。Skills 目标 003/005/006/007/008/010/018 均为 `done`。其后 GOAL-019 见上节。

## 2026-07-22 · Skills v0.8.0 发布准备

矩阵 `candidateRevision: v0.8.0`；六 CLI runtime 证据刷新；CHANGELOG 0.8.0。其后发版实战见上节。

## 2026-07-22 · GOAL-018 D-005 自动发版路径

用户方案 1：tag → pack → Environment `release` → 硬 release-evidence → 自动 create/挂资产。实现于 `skills-pack-release.yml` + `docs/releases`。GOAL-018 **仍 done**；R-018-FIRST-RELEASE 待首次实战。

## 2026-07-22 · 响应 GOAL-018 A-002（F-001～F-003）

D-004 / A-003：关闭 recommended F-001（CI artifact 名统一 NORM）、F-002（R-018-FIRST-RELEASE residual）、F-003（后续 self 模板约定）。**维持** GOAL-018 `done / 100%`。

## 2026-07-22 · GOAL-018 有界关门（Skills Release 打包）

D-003 / A-001：P0～P2 四项交付完成（文档 + pack + releases 约定 + tag CI pack）；`done / 100%`。未推真实公开 Release（Non-goal）。其后 A-002/A-003 见上节。

## 2026-07-22 · 创建 GOAL-018（Skills Release 打包）

D-001：用户要求建立新目标并完成 P0～P2 四项（消费文档、pack 脚本、Release 挂载约定、tag CI pack）。[GOAL-018-skills-release-packaging](GOAL-018-skills-release-packaging/) · 其后有界关门见上节。

## 2026-07-22 · Root 阶段 6 有界结项审视

GOAL-001 D-015 / A-014：阶段 6 **有界结项**（009 + 012～017）；**Root 仍 active**；**R-009-X 仍 accepted**。**未**宣称终态 / Root done。

## 2026-07-22 · GOAL-017 有界关门（X-PILOT）

D-004 / A-004–A-005：汇总 + close-out；`done / 100%`；**R-017-HUMAN-UX** residual。R-009-X 仍 accepted。

## 2026-07-22 · GOAL-017 阶段 B 会话证据

D-003 / A-003：SESSION-001/002 落盘（agent TestClient 实跑）；progress 当时 **65%**。

## 2026-07-22 · GOAL-017 阶段 A 冻结（R-017-A）

D-002 / A-002：试点范围 + 会话证据模板；progress 当时 **20%**。

## 2026-07-22 · 创建 GOAL-017（X-PILOT）

D-038 / A-064：用户 P1；[GOAL-017-human-pilot-feedback](GOAL-017-human-pilot-feedback/) · 其后阶段 A 见上节。R-009-X 仍 accepted。下一编号 **GOAL-018**。

## 2026-07-22 · R-009-X 下一扩展审视（X-PILOT · 待选定）

D-037 / A-063：选项 P1=X-PILOT（推荐）/ P2=详脚本 / P0=不立。其后用户选 P1（见上节）。

## 2026-07-22 · 响应 GOAL-016 A-008（F-001～F-003）

D-007 / A-009：关闭推荐项（R-016-A 引用落点勘误、I 证据指针、阶段条回填）。GOAL-016 仍 `done / 100%`（不重开）。

## 2026-07-22 · GOAL-016 有界关门（X-SM）

D-006 / A-006–A-007：阶段审 + close-out；`done / 100%`；R-016-AI-READ / E2E / UX residual。R-009-X 仍 accepted。全量 **142 passed, 1 skipped**。

## 2026-07-22 · GOAL-016 阶段 D 负向与 AI residual

D-005 / A-005：隔离负向矩阵 + **R-016-AI-READ** accepted；progress 当时 **85%**。

## 2026-07-22 · GOAL-016 阶段 C Web

D-004 / A-004：`/materials` 上传/引用；progress 当时 **65%**。

## 2026-07-22 · GOAL-016 阶段 B service

D-003 / A-003：`materials_store` + tests；progress 当时 **40%**。

## 2026-07-22 · GOAL-016 阶段 A 冻结（R-016-A）

D-002 / A-002：共享资料范围/存储/安全边界冻结；progress 当时 **15%**。

## 2026-07-22 · 创建 GOAL-016（X-SM）

D-036 / A-062：用户 S1；[GOAL-016-shared-materials-product](GOAL-016-shared-materials-product/) · 其后阶段 A 见上节。GOAL-009 仍 `done`；R-009-X 仍 accepted。下一编号 **GOAL-017**。

## 2026-07-22 · R-009-X 下一扩展审视（X-SM / 试点 · 待选定）

D-035 / A-061：选项 S1=X-SM（推荐）/ S2=X-PILOT / S3=SM+PILOT / S4=X-CREATE / S0=不立。其后用户选 S1（见上节）。

## 2026-07-22 · 响应 GOAL-015 A-008（F-001～F-003）

D-007 / A-009：关闭推荐项（R-015-A 勘误、I 证据指针、编号速查→GOAL-016）。GOAL-015 仍 `done / 100%`（不重开）。

## 2026-07-22 · GOAL-015 有界关门（X-NAV）

D-006 / A-006–A-007：阶段审 + close-out；`done / 100%`；**R-015-E2E** / **R-015-CREATE-UI** residual。R-009-X 仍 accepted。全量 **126 passed, 1 skipped**。

## 2026-07-22 · GOAL-015 阶段 D 归档与负向矩阵

D-005 / A-005：归档 UX + 跨区 404 不泄漏；progress 当时 **85%**。

## 2026-07-22 · GOAL-015 阶段 C Web 绑定

D-004 / A-004：`/workspaces` + focus cookie；progress 当时 **65%**。

## 2026-07-22 · GOAL-015 阶段 B service

D-003 / A-003：`workspace_registry` + tests；progress 当时 **40%**。

## 2026-07-22 · GOAL-015 阶段 A 冻结（R-015-A）

D-002 / A-002：N1 白名单与范围冻结；progress 当时 **15%**；阶段 A 完成。

## 2026-07-22 · 创建 GOAL-015（X-NAV）

D-034 / A-060：用户 E1；[GOAL-015-n1-workspace-navigation](GOAL-015-n1-workspace-navigation/) · 其后阶段 A 见上节。GOAL-009 仍 `done`；R-009-X 仍 accepted；Root 仍 active。下一编号 **GOAL-016**。

## 2026-07-22 · R-009-X 下一扩展立项审视（待选定）

D-033 / A-059：选项 E1=X-NAV（推荐）/ E2=X-SM / E3=X-PILOT / E4=NAV+PILOT / E5=NAV+SM / E0=不立。其后用户选 E1（见上节）。

## 2026-07-22 · 响应 GOAL-009 A-057（F-029 / F-030）

D-032 / A-058：关闭推荐项 F-029/F-030。刷新 GOAL-001 / GOAL-012 / workspace 现时叙述；GOAL-009 collecting I 责任方 → **R-009-X**。GOAL-009 仍 `done / 100%`（有界）；Root 仍 active。

## 2026-07-22 · GOAL-009 有界关门

D-031-A / A-056：路径 A；`done / 100%`；**R-009-X** accepted；R-E-3-X closed。Root 仍 active。

## 2026-07-22 · 审视 GOAL-009 有界关门（待裁决）

A-055 / D-031 proposed：可有界关门；其后用户选 A。

## 2026-07-22 · GOAL-009 AI 成功标准有界勾选

D-030-A / A-054：AI 成功标准 **[x] 有界**；progress **98%**；仍 active。

## 2026-07-22 · 审视 GOAL-009 AI 成功标准勾选（待裁决）

A-053 / D-030 proposed：可有界勾选；其后用户选 A。

## 2026-07-22 · GOAL-014 有界关门

D-007 / A-006：GOAL-014 `done / 100%`；GOAL-009 仍 active。

## 2026-07-22 · GOAL-014 D-skip 关闭 R-014-D

D-006 / A-005：R-014-D closed；progress 当时 **85%**。

## 2026-07-22 · GOAL-014 阶段审视（不关门）

A-004 / D-005：阶段审 conditional；progress 当时 **75%**。

## 2026-07-22 · GOAL-014 阶段 C 候选确认链

D-004 / A-003：候选确认链；progress 当时 **65%**。

## 2026-07-22 · GOAL-014 阶段 B broker 骨架

D-003 / A-002：broker 骨架；progress 当时 **35%**。

## 2026-07-22 · GOAL-014 阶段 A 边界冻结

D-002 / A-001：R-014-A 冻结；progress 当时 **15%**。

## 2026-07-22 · 创建 GOAL-014（X-AI）

D-029 / A-052：创建 GOAL-014 · 当时 `active / 0%`。GOAL-009 仍 active **97%**。

## 2026-07-22 · GOAL-009 扩展立项选项（保持 active）

D-028 / A-051：扩展选项表；其后 R1 已建 GOAL-014。

## 2026-07-22 · GOAL-009 阶段审视（不关门）

A-050：self stage · **conditional**；α 有界交付可用；**禁止** done（R-E-3-X）。progress **97%**。

## 2026-07-22 · GOAL-009 R-E-3 有界关闭 + R-E-3-X

D-027-A / A-049：**R-E-3 closed（有界）**；**R-E-3-X accepted**。progress 当时 **96%**。

## 2026-07-22 · GOAL-009 审视 R-E-3 有界关闭（待裁决）

A-048 / D-027 proposed：可有界关闭；路径待确认。progress 当时 **95%**。

## 2026-07-22 · GOAL-009 R-E-2 有界关闭 + R-E-2-H

D-026-A / A-047：**R-E-2 closed（有界）**；**R-E-2-H accepted**。progress **95%**。

## 2026-07-22 · GOAL-009 审视 R-E-2 有界关闭（待裁决）

A-046 / D-026 proposed：可有界关闭；路径待确认。progress 当时 **94%**。

## 2026-07-22 · GOAL-009 R-E-1 HTTP 表单冒烟

D-025 / A-045：**R-E-1 closed**；HTTP proposal→decide **committed**。progress **94%**。

## 2026-07-22 · GOAL-009 F-026 热路径挂接

D-024 / A-044：**F-026 closed**；FA/WS/SM 组合进 `controlled_change`。progress 当时 **92%**。

## 2026-07-22 · GOAL-009 路线图 E 有界退出（E-α）

D-023-A / A-043：路径 A；**E 有界退出（E-α）** + R-E-1～3 accepted；GOAL-009 仍 active。progress 当时 **90%**。

## 2026-07-22 · GOAL-009 审视路线图 E 有界退出（待裁决）

A-042 / D-023 proposed：E-α 证据支持有界退出；路径待确认。GOAL-009 progress 当时 **85%**。

## 2026-07-22 · GOAL-009 E-α 受控追加冒烟

D-022 / A-041：产品根生产路径 append **committed**（`op_e_alpha_smoke_20260722`）；E 全文未退出。GOAL-009 progress **85%**。

## 2026-07-22 · GOAL-009 响应 A-039（F-025 / E-α）

D-021 / A-040：**F-025 closed**；F-027 closed；F-026 open recommended；E-α 入口已定。GOAL-009 progress 当时 **82%**。

## 2026-07-21 · GOAL-009 F-003/F-004 有界关闭

D-020-A / A-038：路径 A；**F-003/F-004 closed** + R-F003/R-F004 residual；路线图 B finding 有界退出。GOAL-009 progress 当时 **80%**。

## 2026-07-21 · GOAL-009 WS+SM 核心矩阵执行

A-036：WS/SM 核心 **pass**。其后 F-003/F-004 已有界关闭（见上节）。

## 2026-07-21 · GOAL-009 R-003 验证包（F-003/F-004）

D-019/A-035：冻结 R-003 验证包；其后 WS/SM 已执行（见上节）。

## 2026-07-21 · GOAL-009 F-002 有界关闭

D-018-A / A-034：路径 A；**F-002 closed** + R-F002-1～3。其后 R-003 验证包已冻结（见上节）。

## 2026-07-21 · GOAL-009 FA-001～006 执行

A-032：`fact_admission` + unittest；**68 passed, 1 skipped**；FA-001～006 **pass**。其后 F-002 已有界关闭（见上节）。

## 2026-07-21 · GOAL-009 R-002 验证包（F-002）

D-017/A-031：冻结 [r-002-verification-package](GOAL-009-ai-assisted-governance-workbench/attachments/r-002-verification-package.md)；其后 FA 已执行（见上节）。
## 2026-07-21 · 本地产品工作区部署（ALLOW=true）

配置 `data/product-workspace` + `web/.env`（ALLOW=true，非 dogfood）。`/api/health` 显示 `controlled_write_enabled=true`。GOAL-009 progress 当时 **60%**。
## 2026-07-21 · GOAL-009 A-030 生产受控写入授权

D-016/A-030：规划锁默认关闭；须 `ALLOW_CONTROLLED_WRITE=true` + 产品数据根 + 单进程 residual。GOAL-009 progress **60%**。

## 2026-07-21 · GOAL-009 A-029 I-003/I-004/I-006 α verified

用户选 V1：I-003/I-004/I-006 **verified（α 有界）**。F-007/F-008 closed。其后 A-030 授权生产写（见上节）。

## 2026-07-21 · GOAL-009 A-028 审视 I-003/I-004/I-006

A-028 / D-015 proposed；其后用户选 V1（见上节）。

## 2026-07-21 · GOAL-009 A-027 有界关闭 F-008

用户选路径 A：接受 R-F008-1～3 residual；**F-008 closed（有界）**。I-003/I-004/I-006 非 verified；生产写入仍关。GOAL-009 progress **48%**。

## 2026-07-21 · GOAL-009 A-026 F-008 residual 审视

GOAL-009 落盘 F-008 residual 路径 A/B/C（A-026 / D-014 proposed）。其后用户选路径 A（见上节）。

## 2026-07-21 · GOAL-009 A-025 关闭 F-007

GOAL-009 **F-007 closed**（确认/信任边界）。**F-008 仍 open**（process-local CT-009、最小 CT-011 等）。I-003/I-004/I-006 非 verified；生产写入仍关。GOAL-009 progress **42%**。

## 2026-07-21 · GOAL-013 阶段 E 有界关门与 A-024 门禁审视

GOAL-013 `done / 100%`（实现证据交付完成）。最终回归 **61 passed, 1 skipped**。GOAL-009 A-024 当时 F-007/F-008 仍 open；现 F-007 已由 A-025 关闭。

## 2026-07-21 · GOAL-013 阶段 D F-008 CT

GOAL-013 完成 CT-008/009/010/011 可运行证据，progress **75%**；CT-009 明确限于 process-local lock。GOAL-009 F-007/F-008 仍 open，生产写入仍关。

## 2026-07-21 · GOAL-009 A-022 阶段 C CT 回写

GOAL-009 将 CT-001/003/006/012/014/015 标为覆盖（GOAL-013 阶段 C）。**F-007/F-008 仍 open**；生产写入仍关。GOAL-009 progress **35%**。

## 2026-07-21 · GOAL-013 阶段 C F-007 CT

GOAL-013 完成 CT-001/003/006/012/014/015 可运行用例；progress **55%**。生产门禁默认仍关；F-007/F-008 关闭仍归 GOAL-009。

## 2026-07-21 · CT-007 台账回写

GOAL-012 F-003 residual **closed**（A-004）；GOAL-009 A-021 将 CT-007 标为覆盖。**F-007/F-008 仍 open**；生产写入仍关。GOAL-009 progress **33%**。

## 2026-07-21 · GOAL-013 阶段 B 跨进程幂等

GOAL-013 完成 CT-007 持久化重放与 CT-008 部分冲突；progress **30%**。生产门禁默认仍关。F-007/F-008 关闭仍归 GOAL-009。

## 2026-07-21 · GOAL-013 写入门禁 CT 与跨进程幂等立项

按 GOAL-009 A-020 创建 [GOAL-013-write-gate-ct-durable-idempotency](GOAL-013-write-gate-ct-durable-idempotency/)：补 CT 缺口与跨进程幂等；**生产门禁默认仍关**；F-007/F-008 关闭权仍在 GOAL-009 审视。

## 2026-07-21 · GOAL-009 A-020 写入门禁证据台账

GOAL-009 吸收 GOAL-012 关键路径证据并对照 CT-001～018；**F-007/F-008 仍 open**，缺口清单见 A-020。**未**开放生产写入；进度 **32%**。

## 2026-07-21 · GOAL-012 有界关门

GOAL-012 标为 `done / 100%`（α 实现）。**生产 Web/AI 写入仍关**。关门时 F-003 residual 后由 GOAL-013/A-004 **关闭**（CT-007 持久化）；不构成 F-008 整体关闭或生产放行。

## 路径语义说明（迁移后现时入口）

- **现时 canonical 目标状态根**：本目录 `docs/workspace-001-goal-governance/`（含本 `goal-tree.md` 与平铺 `GOAL-*`）。
- **历史记录**中出现的 `docs/goals/` 路径为 **GOAL-011 迁移前**的事实、设计快照或运行证据叙述；**不要**批量改写已关门目标附件，也**不要**把旧路径当成当前读取根。
- 旧外部仓库仅在无显式工作区根时按 legacy `docs/goals/` 隐式单工作区识别；本仓库不保留并行 `docs/goals/` 真相源。

## 2026-07-21 · 审计响应（GOAL-011 F-001 / GOAL-012 A-001）

`/govern` 响应 GOAL-011 A-003：关闭推荐项 F-001（上节现时入口标注）。响应 GOAL-012 A-001：self 阶段审与台账对齐；F-002/F-004 整改；F-003 接受为 α 门禁内 residual（幂等=进程内）；**生产 Web 写入**仍绑 GOAL-009 F-007/F-008 与 I-003/I-004/I-006。

## 2026-07-21 · 首垂直切片实现立项

GOAL-009 在用户接受设计默认（N1/存储 A/α/打包分栏/SQLite 分层）后关闭 F-005，并创建 GOAL-012 承接路线图 D。GOAL-012 实现配置化产品工作区详情与门禁内的受限执行事实追加；**生产 Web/AI 写入**仍受 GOAL-009 的 F-007/F-008 与 I-003/I-004/I-006 阻断。本仓 dogfood 过程记录不进入发布物（D-011）。

## 2026-07-20 · 阶段 6 Web 工作台规划

GOAL-009 启动 AI 协助的人类目标治理工作台的产品定义与信息发现。它不把只读浏览器定义为产品终态；工作区 canonical 根是运行时真相源。规划台账仍在 GOAL-009；实现交付在 GOAL-012 及后续目标。

## 2026-07-20 · 工作区与共享资料区核心协议

GOAL-010 已完成跨层的核心协议与 Skills 首先适配。它只为 GOAL-009 的 R-003 提供输入，不关闭 F-003/F-004 的产品验证。

## 2026-07-20 · 多工作区目录迁移与共享资料索引

GOAL-011 完成当前仓库到 `docs/workspace-001-goal-governance/` 的迁移与共享资料候选索引骨架。该过程数据为 dogfood，不随 Web/Skills 发布复制给其他项目。

> 所有目标平铺存放在本目录；层级仅通过各目标 `00-meta.md` 的 `parent` 字段维护。
> **新建、修改状态或调整 parent 后，必须同步更新本文件。**

## 树状结构

> 根目标当前采用“三层交付、一个真相源”：核心方法论与模板、Skills 消费适配器、Web 人类工作台。核心 canonical 模板位于 `docs/templates/goal-folder/`；包内分发为 `skills/core/docs/templates/`（stage；GOAL-022）。

```text
GOAL-001-main-vision · 交付可复用的目标治理方法论、文档协议与消费工具 [active]
├── GOAL-002-project-bootstrap · 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） [done 100%]
├── GOAL-003-skills-practice · 完善 Skills 并在本项目中实践验证 [done 100%]
├── GOAL-004-core-data-model · 实现核心数据模型与 Goal 基础管理 [done 100%]
├── GOAL-005-skills-closed-loop-audit · Skills 治理闭环与交叉审计 [done 100%]
├── GOAL-006-core-methodology-template-productization · 核心方法论、文档协议与 canonical 模板产品化 [done 100%]
├── GOAL-007-information-readiness-governance · 信息就绪与未知项治理 [done 100%]
├── GOAL-008-skills-consumer-adapter-release-consistency · Skills 消费适配器跨宿主/跨版本发布一致性 [done 100%]
├── GOAL-009-ai-assisted-governance-workbench · 规划 AI 协助的人类目标治理 Web 工作台 [done 100%]
├── GOAL-010-core-workspace-shared-materials-protocol · 建立工作区与共享资料区核心协议，并完成 Skills 首先适配 [done 100%]
├── GOAL-011-multi-workspace-directory-migration · 完成多工作区目录迁移与共享资料索引骨架 [done 100%]
├── GOAL-012-first-slice-workspace-detail · 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内） [done 100%]
├── GOAL-013-write-gate-ct-durable-idempotency · 补齐受控写入 CT 缺口与跨进程幂等（生产门禁默认仍关） [done 100%]
├── GOAL-014-ai-collaboration-runtime · 实现 AI 协作运行时与用户确认链（有界） [done 100%]
├── GOAL-015-n1-workspace-navigation · 实现 N1 多工作区导航（列表 / 选择 / 归档） [done 100%]
├── GOAL-016-shared-materials-product · 实现共享资料区产品（CRUD / 固定引用 / 隔离） [done 100%]
├── GOAL-017-human-pilot-feedback · 人类多会话试点与反馈证据（有界） [done 100%]
├── GOAL-018-skills-release-packaging · Skills Release 打包与对外安装路径（文档 + pack + CI） [done 100%]
├── GOAL-019-skills-consumer-workspace-bootstrap · Skills 消费方工作区骨架落地（空仓可运行） [done 100%]
├── GOAL-020-methodology-adversarial-audit-fix · 核心方法论对抗性审计与纠错 [done 100%]
├── GOAL-021-skills-release-chain-hardening · 加固 Skills「规则→分发→证据→发布」执行链 [done 100%]
└── GOAL-022-docs-ssot-skills-mirror-stage · 方法论单一真相源与 Skills 镜像 stage 化 [done 100%]
```

## 状态总览

| ID | 标题 | Parent | Status | Progress | 路径 |
|----|------|--------|--------|----------|------|
| GOAL-001-main-vision | 交付可复用的目标治理方法论、文档协议与消费工具 | — | active | — | [GOAL-001-main-vision/](GOAL-001-main-vision/) |
| GOAL-002-project-bootstrap | 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） | GOAL-001-main-vision | done | 100% | [GOAL-002-project-bootstrap/](GOAL-002-project-bootstrap/) |
| GOAL-003-skills-practice | 完善 Skills 并在本项目中实践验证 | GOAL-001-main-vision | done | 100% | [GOAL-003-skills-practice/](GOAL-003-skills-practice/) |
| GOAL-004-core-data-model | 实现核心数据模型与 Goal 基础管理 | GOAL-001-main-vision | done | 100% | [GOAL-004-core-data-model/](GOAL-004-core-data-model/) |
| GOAL-005-skills-closed-loop-audit | Skills 治理闭环与交叉审计 | GOAL-001-main-vision | done | 100% | [GOAL-005-skills-closed-loop-audit/](GOAL-005-skills-closed-loop-audit/) |
| GOAL-006-core-methodology-template-productization | 核心方法论、文档协议与 canonical 模板产品化 | GOAL-001-main-vision | done | 100% | [GOAL-006-core-methodology-template-productization/](GOAL-006-core-methodology-template-productization/) |
| GOAL-007-information-readiness-governance | 信息就绪与未知项治理 | GOAL-001-main-vision | done | 100% | [GOAL-007-information-readiness-governance/](GOAL-007-information-readiness-governance/) |
| GOAL-008-skills-consumer-adapter-release-consistency | Skills 消费适配器跨宿主/跨版本发布一致性 | GOAL-001-main-vision | done | 100% | [GOAL-008-skills-consumer-adapter-release-consistency/](GOAL-008-skills-consumer-adapter-release-consistency/) |
| GOAL-009-ai-assisted-governance-workbench | 规划 AI 协助的人类目标治理 Web 工作台 | GOAL-001-main-vision | done | 100% | [GOAL-009-ai-assisted-governance-workbench/](GOAL-009-ai-assisted-governance-workbench/) |
| GOAL-010-core-workspace-shared-materials-protocol | 建立工作区与共享资料区核心协议，并完成 Skills 首先适配 | GOAL-001-main-vision | done | 100% | [GOAL-010-core-workspace-shared-materials-protocol/](GOAL-010-core-workspace-shared-materials-protocol/) |
| GOAL-011-multi-workspace-directory-migration | 完成多工作区目录迁移与共享资料索引骨架 | GOAL-001-main-vision | done | 100% | [GOAL-011-multi-workspace-directory-migration/](GOAL-011-multi-workspace-directory-migration/) |
| GOAL-012-first-slice-workspace-detail | 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内） | GOAL-001-main-vision | done | 100% | [GOAL-012-first-slice-workspace-detail/](GOAL-012-first-slice-workspace-detail/) |
| GOAL-013-write-gate-ct-durable-idempotency | 补齐受控写入 CT 缺口与跨进程幂等（生产门禁默认仍关） | GOAL-001-main-vision | done | 100% | [GOAL-013-write-gate-ct-durable-idempotency/](GOAL-013-write-gate-ct-durable-idempotency/) |
| GOAL-014-ai-collaboration-runtime | 实现 AI 协作运行时与用户确认链（有界） | GOAL-001-main-vision | done | 100% | [GOAL-014-ai-collaboration-runtime/](GOAL-014-ai-collaboration-runtime/) |
| GOAL-015-n1-workspace-navigation | 实现 N1 多工作区导航（列表 / 选择 / 归档） | GOAL-001-main-vision | done | 100% | [GOAL-015-n1-workspace-navigation/](GOAL-015-n1-workspace-navigation/) |
| GOAL-016-shared-materials-product | 实现共享资料区产品（CRUD / 固定引用 / 隔离） | GOAL-001-main-vision | done | 100% | [GOAL-016-shared-materials-product/](GOAL-016-shared-materials-product/) |
| GOAL-017-human-pilot-feedback | 人类多会话试点与反馈证据（有界） | GOAL-001-main-vision | done | 100% | [GOAL-017-human-pilot-feedback/](GOAL-017-human-pilot-feedback/) |
| GOAL-018-skills-release-packaging | Skills Release 打包与对外安装路径（文档 + pack + CI） | GOAL-001-main-vision | done | 100% | [GOAL-018-skills-release-packaging/](GOAL-018-skills-release-packaging/) |
| GOAL-019-skills-consumer-workspace-bootstrap | Skills 消费方工作区骨架落地（空仓可运行） | GOAL-001-main-vision | done | 100% | [GOAL-019-skills-consumer-workspace-bootstrap/](GOAL-019-skills-consumer-workspace-bootstrap/) |
| GOAL-020-methodology-adversarial-audit-fix | 核心方法论对抗性审计与纠错 | GOAL-001-main-vision | done | 100% | [GOAL-020-methodology-adversarial-audit-fix/](GOAL-020-methodology-adversarial-audit-fix/) |
| GOAL-021-skills-release-chain-hardening | 加固 Skills「规则→分发→证据→发布」执行链 | GOAL-001-main-vision | done | 100% | [GOAL-021-skills-release-chain-hardening/](GOAL-021-skills-release-chain-hardening/) |
| GOAL-022-docs-ssot-skills-mirror-stage | 方法论单一真相源与 Skills 镜像 stage 化 | GOAL-001-main-vision | done | 100% | [GOAL-022-docs-ssot-skills-mirror-stage/](GOAL-022-docs-ssot-skills-mirror-stage/) |

阶段 6：**有界结项**（GOAL-001 D-015 / A-014；009 + 012～017 done 有界）。**≠ 终态**。现行路径 **D-024 · 路径 D**（仅维护；阶段 7 延期；A/B/C 须改道）。**GOAL-022** `done / 100%`（residual R-022-ORPHAN-PRUNE / R-022-INSTALL-TEMPLATES-COPY non-blocking）；GOAL-020/021 `done`。下一编号 **GOAL-023**。GOAL-001 仍为 `active`（终态 / residual 见 **R-009-X**）。GOAL-018/019 = Skills 维护波次 done。

## 状态图例

| Status | 含义 |
|--------|------|
| `draft` | 草稿，尚未正式启动 |
| `active` | 进行中 |
| `blocked` | 阻塞 |
| `done` | 已完成 |
| `cancelled` | 已取消 |

## 编号规则速查

1. `GOAL-001` 固定为 Root Goal（`parent: null`）。
2. 新目标从现有最大编号 +1 顺序分配（当前下一个：`GOAL-023`）。
3. 文件夹命名：`GOAL-NNN-short-slug`（英文短横线 slug）。
4. 每个目标必须包含：`00-meta.md`、`01-decision.md`、`02-execution.md`、`03-audit.md`、`attachments/`。
