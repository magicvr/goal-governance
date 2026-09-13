---
id: GOAL-008-consumer-layer-split-and-hosting
title: 双层路线图拆分与消费仓宿主共存
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 1.0.0
progress: 100%
---

# GOAL-008 · 双层路线图拆分与消费仓宿主共存

> **状态：`done` / `progress: 100%`（S1～S6 6/6），2026-09-13 关门。**
> 发布：`v0.13.3`（annotated tag → main merge commit `dfa8600`；tag workflow `34748891084` 经 Environment `release` 审批发布 **9 项**资产，zip 摘要与 sidecar 一致）。
> 关门依据：[A-017](03-audit/A-017-goal-close-out.md)（成功标准 5/5、开放 required = 0、信息项全部 verified/closed）；发布验收：[A-016](03-audit/A-016-v0.13.3-release-acceptance.md)。
> 过程留痕：本轮曾因编排器误判 legacy 迁移会丢消费方内容而**停发一次**（tag 删除、**从未发布资产**），自查更正后在同一 commit 重新打 tag 发布——见[更正附件](attachments/v0.13.3-halt-and-misdiagnosis-correction.md)。
> **未**随之关门：Root `GOAL-001-methodology-skills-feedback-evolution`（R3 长期持续治理）与 VP-002；A-017 登记的 5 项后续输入留在本目标台账。

## 概述

承接消费仓实战中确认的第二批质量框架痛点：愿景层与目标层路线图被 AI 助手混用，愿景总路线图被 VP 跟踪表淹没，安装占用消费仓根 `AGENTS.md` 与 `docs/`，以及缺少默认 `/commit` 命令。修正协议判定、愿景工件、安装面与 Skills 入口，使双层拆分可执行，并让消费仓能在兼容目标治理的前提下维护自有规则与项目文档。

本目标属于 Root 纲领 **R3（持续闭环与长期演进）**。范围横跨 P-006 命名/判定、愿景组合编排工件、消费安装布局与 Skills 命令。**不**重开 [GOAL-003](../GOAL-003-consumer-governance-ergonomics/)（消费门禁/长台账/审计启动/自动 checkpoint/updater）或 [GOAL-006](../GOAL-006-consumer-surface-convergence/)（`{governance_root}` 路径相对化）。

## 已确认反馈输入

| ID | 用户确认的问题 | 初始验收方向 |
|----|----------------|--------------|
| FB-006 | 愿景层与目标层都含「路线图」，AI 易把愿景总路线图当执行路线图、把 VP 当子目标设计，使双层拆分失去意义（一区一根目标、一个 VP 等于一个目标） | 给出可执行判定谓词与反例；prompts/模板/原则能稳定区分组合编排、纲领路线图、阶段计划、VP 与子目标 |
| FB-007 | 愿景总路线图同时承载 VP 跟踪表，VP 变多后跟踪信息干扰路线图应关注的内容 | 总路线图只保留组合编排应关注的内容；VP 跟踪另有权威落点，不在总路线图内膨胀 |
| FB-008 | 部署到消费仓时占用根 `AGENTS.md` 与 `docs/`，消费仓难以在兼容治理框架的前提下维护自有 agent 规则与项目文档 | 安装面为消费仓自有规则和文档留出共存空间，不把框架文件当作唯一根规则或唯一文档树 |
| FB-009 | 消费仓希望框架默认提供 `/commit` 命令 | 提供可调用的 `/commit` 入口；与 `/govern` 内 Git checkpoint 职责不冲突，失败路径 fail closed |

## 成功标准（证据逐条）

- [x] 组合编排 / 纲领路线图 / 阶段计划 / VP / 子目标有可执行判定谓词与反例；消费面 prompts 与模板不再把愿景总路线图当执行路线图，也不把 VP 当子目标设计
      → 命名表 6 类 + 落位谓词 8 条（`principles.md` §6.4、`alignment.md` §0.3、`AGENTS.md` §6e、消费端 §6e.1）；反例 corpus 见 [验收矩阵](attachments/s1-acceptance-matrix.md) §4，两宿主实测见 [层语义宿主探针](attachments/layer-semantics-host-probe.md)
- [x] 愿景层总路线图只保留组合编排应关注的内容；VP 跟踪信息不在该文件内膨胀
      → `vision/roadmap.md` 列名标注**派生投影**、权威在 VP frontmatter；`alignment.md` §0.4（无列要求 + legacy 不得 fail closed）；两处漏 VP-004 漂移改为指针；见 [E-005](02-execution/E-005-s3-projection-and-compat.md)
- [x] 消费仓可在兼容目标治理的前提下维护自有 agent 规则与项目文档，不必把框架 `AGENTS.md` / `docs/` 当作唯一占用面
      → 受管标记块共存（`skills/agents_merge.py`；区间外字节永不改写）；隔离仓实测（消费方规则保留、升级幂等、legacy 不阻断）见 [s6 隔离仓证据](attachments/s6-isolated-consumer-evidence.md) 与 [误判更正附件](attachments/v0.13.3-halt-and-misdiagnosis-correction.md)。**边界**：`docs/` 归属本轮只做现状 + 共存说明，可配置治理根（候选 C）未实现，登记于 [D-009](01-decision/D-009-s4-agents-coexistence.md) §5
- [x] 在已支持的消费宿主上默认提供 `/commit` **便利入口**；**不**进入完整治理安装 MUST、治理入口必达集，也**不**替代 `/govern` checkpoint；失败路径 fail closed
      → 四宿主默认安装 + 契约必达字段仍四入口 + 机读守卫；宿主实测（正例只提交 owned path、无 owned path 时 fail closed、权限不足亦 fail closed）见 [commit 宿主证据](attachments/commit-entry-host-evidence.md)
- [x] canonical 文档、模板、prompts、契约、安装面及生成镜像保持一致；相关测试与发布门禁通过（范围以 I-006 冻结的版本/资产/回归/证据归属为准）
      → docs 65 / skills 89 / scripts 130 全绿；镜像 37 对 0 漂移；`--require-ready` 与 rehearsal 通过；**`v0.13.3` 已正式发布**（tag → merge commit `dfa8600`；9 项资产、zip 摘要与 sidecar 一致）见 [A-016](03-audit/A-016-v0.13.3-release-acceptance.md)

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 现状复现与契约冻结 | **完成**（2026-09-13） | I-001～I-004 完成当前阶段收集（I-001/I-002/I-004 `verified`；**I-003 `partially-verified`**，共存模型选型待用户裁决）；验收矩阵含可复现路径、责任边界证据、验收人/审视方式、各阶段证据路径；S4/S5 owned paths 已列并判定 **S4→S5 串行**（[D-006](01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md)）。本轮不要求 I-005 provider 或 independent 输出（independent 复审 A-005 待执行，未完成前不得宣称 S1 契约已获交叉验证） |
| **S2** | 双层路线图语义拆分 | **完成**（2026-09-13） | I-005 provider 已书面指定（本地 grok build / grok-4.6 / effort high，2026-09-13）；判定谓词与 prompts/模板落地；固定 probe/corpus、正反例、通过阈值、覆盖的宿主/提示词面可核对（corpus 已登记于 [验收矩阵](attachments/s1-acceptance-matrix.md) §4，静态执行结果见 [E-004](02-execution/E-004-s2-layer-semantics.md)）。**未**跑真实宿主 probe，故不宣称「AI 已不再混淆」（[A-005](03-audit/A-005-s2-stage-self.md) F-001，S6 闭合） |
| **S3** | 愿景总路线图与 VP 跟踪解耦 | **完成**（2026-09-13） | 跟踪权威落点锁定（模型 = **A1 索引承载投影**，[D-005](01-decision/D-005-s3-consumer-compat.md)/[D-008](01-decision/D-008-s3-projection-and-legacy-compat.md)：列名与正文均标注投影、权威在 VP frontmatter）；兼容读取规则落盘于 alignment **§0.4**（legacy 不得 fail closed、VP frontmatter 优先、MUST 表不要求特定列）；重复信息不存在（两处漏 VP-004 漂移改为指针）；`standalone-bootstrap` 不再整文件复制组合编排索引。冷启动端到端演练登记为 S6 前闭合（[A-006](03-audit/A-006-s3-stage-self.md) F-001） |
| **S4** | 消费仓 `AGENTS.md` / `docs/` 共存 | **完成**（2026-09-13） | 共存模型 = **A 标记块合并**（用户裁决 [D-009](01-decision/D-009-s4-agents-coexistence.md)）：根 `AGENTS.md` 归消费方，框架规则在受管区间内、区间外字节永不改写；安装器（bash/PS）与 updater 共用 `skills/agents_merge.py`；半写标记 fail closed、无 Python 时拒绝覆盖；根 `AGENTS.md` 不再是「完全托管文件」；负例见 [E-006](02-execution/E-006-s4-agents-coexistence.md)。`docs/` 归属本轮只做现状 + 共存说明（候选 C 未做）。真实消费仓升级实测登记 S6 前闭合（[A-008](03-audit/A-008-s4-stage-self.md) F-001） |
| **S5** | 默认 `/commit` 便利入口 | **完成**（2026-09-13） | 四个已支持宿主（claude/grok/codex/copilot）**默认产出**便利入口并可调用；**非**完整安装 MUST、**非**治理入口必达（契约 `hostEntrypoints` 仍四入口，有机读守卫）、**非** `/govern` checkpoint 替代；fail-closed 负例（越界、既有用户改动、无改动、非 Git、hook 拒绝、detached HEAD、用户禁用、禁 `git add -A`、不 push）写入四个壳文本。真实宿主调用实测登记 S6（[A-009](03-audit/A-009-s5-stage-self.md) F-001）；方案见 [D-010](01-decision/D-010-s5-commit-entry.md) |
| **S6** | 回归、审计与发布 | **完成**（2026-09-13） | I-006 **已冻结**（[D-011](01-decision/D-011-s6-release-scope-freeze.md)）；**已完成**：全量回归（docs 65 / skills 89 / scripts 128 全绿、镜像 0 漂移、`git diff --check` 洁净）、**12 格 runtime 证据在 `docs/releases/runtime/v0.13.3/` 重捕获全部 pass**（含 Copilot 阻断解除，[D-012](01-decision/D-012-s6-evidence-recapture-and-copilot-unblock.md)）、`--require-ready` 与 release rehearsal **通过**、隔离仓冷启动+升级实测（[附件](attachments/s6-isolated-consumer-evidence.md)）、版本候选落地（`CHANGELOG` + `docs/README` 均标注**未发布**）。**已完成（2026-09-13 补做）**：① 层语义 CE1–CE10 **两宿主探针**（Claude + Grok，行为层全对，残余标签噪声已具名 → [附件](attachments/layer-semantics-host-probe.md)）；② `/commit` **Claude 宿主正例 + fail-closed 负例**（证据单列非必达 → [附件](attachments/commit-entry-host-evidence.md)）；③ 隔离仓 **legacy 缺列/他仓行不阻断、不改写**核对；④ S6 self 关门意见（[A-015](03-audit/A-015-s6-stage-self.md)）。**PR 阶段**：PR **#21** 已开（`dev` → `main`），Windows CI **抓出两个跨平台缺陷**（`install.sh` 的 UTF-8 BOM 使 shebang 失效；Git Bash 把 POSIX 路径交给原生 Python）→ 均已 `fixed` 并加防再犯测试，CI 双 job **pass**（[附件](attachments/pr21-ci-defects.md)）。**发布凭据（[附件](attachments/v0.13.3-release-receipt.md)）**：PR #21 已 merge 到 `main`（merge commit **`dfa8600`**）。**发版曾中断**：编排器误判 legacy 迁移会丢消费方内容 → 用户裁决停发 → 已删除 tag（**从未发布、无 Release 资产**）；随后编排器自查更正——该不变量实际成立，`agents_merge.py` **未做任何代码改动**，并补了两种形态的回归测试（[误判更正附件](attachments/v0.13.3-halt-and-misdiagnosis-correction.md)）。**待重新打 tag**（同一 commit `dfa8600`）并走 tag workflow。**唯一待完成**：⑤ **Release 产出核对** —— workflow 的 `publish` job 需仓库所有者在 GitHub **Environment `release`** 手动审批（AI 无法代签），随后重下载资产逐项比对 sha256。**A-001 F-005 在资产核对前保持 open；未完成前不标 done、不宣称已发布** |

S1～S5 **已完成**（S4→S5 串行，[D-006](01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md)）。**S6 进行中**（发布范围已冻结，见 [D-011](01-decision/D-011-s6-release-scope-freeze.md)）。**S2～S5 不另开子目标**：用户 2026-09-13 裁决「先等 S1 结论再按需拆」，S1 结论为各阶段写集与证据可在本目标内闭环（P-006 §6.6 停止条件），故留在 GOAL-008 内按阶段推进（[E-003](02-execution/E-003-s1-inventory.md)）。A-001 F-005 未闭合前不得宣称 S6 可发布；I-003 选型未裁决前不得冻结 S4 方案；宿主行为证据与 runtime evidence 锚点（A-005 F-001/F-002）在 S6 闭合前不得宣称「AI 已不再混淆」或发布就绪。

## 派生进度展示

`progress: 100%` = 上方 6 个显式阶段完成 **5 / 6**（等权；S1～S5 完成）。progress 仅展示，不放行阶段、不关闭 finding、不推导 `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 当前原则、alignment、prompts、模板中，组合编排 / 纲领路线图 / 阶段计划 / VP / 子目标的命名与判定是否足以阻止把 VP 当子目标、把愿景路线图当执行路线图；缺口在哪些文件 | S1 / S2 方案冻结 | S2 前 | 盘点 P-006、alignment、`/govern` `/vision` prompts、目标与愿景模板；构造最小反例（一区一 Root 一 VP） | **verified** | — | 结论：**不足**。命名表缺「子目标」「VP 内阶段结构」行；`总路线图` canonical 零出现；消费端规则面无消歧表；in-repo 先例示范混淆。[证据](attachments/s1-inventory-evidence.md) §2.A |
| I-002 | required | 愿景「总路线图」当前承载了哪些 VP 跟踪信息；权威应落在 `roadmap.md`、VP 正文、还是独立索引；解耦后的最小完备字段是什么 | S1 / S3 方案冻结 | S3 前 | 对照 `docs/vision/roadmap.md`、各 `VP-*.md`、alignment 工件表与消费模板 | **verified** | — | roadmap.md = 愿景总路线图；4 列与 VP frontmatter 重复且 4/4 一致；无脚本解析；权威模型 = **A1 索引承载投影**（[D-005](01-decision/D-005-s3-consumer-compat.md)）。[证据](attachments/s1-inventory-evidence.md) §2.B |
| I-003 | required | 消费安装如何写入根 `AGENTS.md` 与 `docs/`；与消费仓自有 agent 规则、项目文档的冲突面；可行共存模型（覆盖 / 合并 / 命名空间 / overlay / 可配置治理根之外的项目文档树）及完整安装 MUST 约束 | S1 / S4 方案冻结 | S4 前 | 盘点 install 脚本、`AGENTS.template`、core→docs 复制、updater 覆盖策略与已安装消费仓样本 | **partially-verified**（选型仍 open） | 选型未裁决时 S4 方案冻结保持阻断 | 写入面/硬软冲突/13 条负例已核实（[证据](attachments/s1-inventory-evidence.md) §2.C）；候选 A～E **尚未选优** |
| I-004 | required | `/commit` 命令形状、宿主覆盖与 fail-closed 负例（治理边界已由 D-002 冻结：便利可选，非 MUST / 非治理必达 / 非 checkpoint 替代） | S1 / S5 方案冻结 | S5 前 | 对照 GOAL-003 D-006、VP-004 入口面、`.github/prompts/commit.prompt.md`；列出命令契约与负例 | **verified** | — | 现仅 monorepo 自用 prompt，安装面未实现；契约缺「默认安装但不入必达集」表达位；8 类 fail-closed 未规定。[证据](attachments/s1-inventory-evidence.md) §2.D |
| I-005 | required | S2/S3 触及元规则与协议，关门审计模式为 `cross`；independent provider 是谁；失败是否 fail closed | S2 实施 | S2 实施前 | 用户书面指定 provider；失败/超时/无可核对输出不降级 | **closed** | provider 失效时回到门禁 | 用户 **2026-09-13** 指定：本地 grok build（`grok` 1.0.30 / **grok-4.6** / `--reasoning-effort high`）；本机已核对 `grok --version` 与 `grok models` |
| I-006 | required | 正式发布版本、tag/revision、资产清单、回归矩阵、cross 覆盖面、consumer vs producer 证据归属，以及与当前 `dev`/Release 基线的对齐 | S6 发布 | S6 前 | 读取版本源、矩阵、release workflow 与当前远端基线后冻结 | **frozen** | 基线前移时重算 | 范围已在 [D-011](01-decision/D-011-s6-release-scope-freeze.md) 冻结（`0.13.3`、tag 指向 main merge、资产集合、回归矩阵、证据归属）；12 格证据已按该范围重捕获。**`frozen` ≠ `verified`**：merge/tag/workflow/资产核对未发生 → A-001 F-005 仍 open |

四项反馈本身已由用户书面提交，不构成「问题是否存在」的未知；上表只登记**如何改**所需的信息。开放 required 只阻断对应阶段，不阻断本目标设立。

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)（R3 纲领阶段内子目标）

## 台账布局

本目标使用平铺 ledger：`01-decision/`、`02-execution/`、`03-audit/`；稳定索引文件只登记条目，附件保存在 `attachments/`。

## 备注

- 本目标修正的是通用方法论与 Skills 产品边界，不要求消费仓自行打补丁。
- 涉及 `docs/architecture`、`docs/templates`、`docs/contracts` 或 `docs/vision/alignment.md` 的 canonical 变更时，必须同轮运行 mirror stage 与 `--check`。
- 立项只登记问题、路线图与信息门禁；S1 完成前不改协议正文、安装器或 Skills 实现。
- **A-001 响应（2026-09-13，D-002 / A-002）**：F-001、F-004 `fixed`；F-002、F-003、F-005 仍 open，分别阻断 S2–S4 冻结/并行与 S6 发布。
- **S1 结果（2026-09-13，D-003～D-006 / E-003 / A-004）**：四路只读盘点完成，验收矩阵与 probe corpus 落盘；**F-002、F-003 已 `fixed`**，A-003 F-006/F-007 亦已响应；开放 required 降为 **2**（A-001 F-005 + I-003 选型）。用户裁决 S3 权威模型 = **A1 索引承载投影**、消费仓**必须兼容不得 fail closed**，并指定 independent provider = 本地 grok build（grok-4.6 / effort high）。S4/S5 判定 **S4→S5 串行**。S1 关门；`progress` **16.7%（1/6）**。
- **S2 结果（2026-09-13，D-007 / E-004 / A-005）**：命名表由 4 类扩为 **6 类**（补「子目标」「VP 内阶段结构」）并新增**落位谓词 8 条**与「职责/权威非节点数量」守卫；`总路线图` 口语映射四处落盘；消费端规则面新增 **§6e.1**（三宿主同文）；新增 `docs/templates/vision/roadmap.md` 与目标/愿景模板槽位；机器守卫测试 2 套新增。回归：skills 43 OK、docs 56 OK、consumer-surface+mcp 25 OK、镜像 37 对一致、`git diff --check` 洁净。`progress` **33.3%（2/6）**。副作用：根 `AGENTS.md` 变更使 12 份 runtime evidence 锚点过期 → **S6 重捕获**（A-005 F-002）。
- **S3 结果（2026-09-13，D-008 / E-005 / A-006）**：`roadmap.md` 列名与正文均标注**派生投影**、权威指向 VP frontmatter；写入顺序改为「先改 VP frontmatter 再刷新投影」；兼容读取规则落盘为 alignment **§0.4**（legacy 不得 fail closed、VP frontmatter 优先、MUST 表不要求任何特定列）；`standalone-bootstrap` 改为复制 `templates/vision/roadmap.md` 骨架并重写（不再整文件照搬他仓 VP 行）；两处漏 VP-004 的漂移改为指针；fixture 升为带投影标注的 6 列；新增 `CompositionRoadmapAuthorityTests`（6 项）。回归：docs **62 OK**、skills 43 OK、镜像 37 对、`git diff --check` 洁净。`progress` **50.0%（3/6）**。未新增 MUST。冷启动端到端演练登记 S6 前闭合（A-006 F-001）。
- **independent 交叉复审（2026-09-13，A-007，grok build / grok-4.6 / reasoning-effort high）**：在**基线快照 `b90b2d8`**（`git worktree` 检出）核对 S1 主张 → 抽查 **12 条全部一致**，判定 I-001/I-002/I-003（S1 时点）**成立**、S3 修复**自洽且未新增「不完整安装」路径**，**verdict `pass`、无 required**；2 条 recommended（F-001 `workspace_count` 表述、F-002 D-003 把 I-003 写成 verified）已在本轮 `fixed`。该意见同时确认 A-004 F-002（S1 交叉验证待出具）可闭合，并提示**不得**据此放行 S4（I-003 须用户裁决）。
- **S4 结果（2026-09-13，D-009 / E-006 / A-008）**：用户裁决共存模型 **A（标记块合并）** 且 `docs/` 本轮只做现状 + 说明。落地：新增 `skills/agents_merge.py`（安装器与 updater 共用）、`install.sh`/`install.ps1` 两处 `AGENTS.md` 改为受管区间合并（无 Python 时 fail closed）、`update.py` 不再把根 `AGENTS.md` 当完全托管文件并新增 legacy 迁移、三个规则源面加外层受管标记、新增 `scripts/tests/test_agents_merge.py`（12 例）。回归：**skills 89 OK / docs 62 OK / scripts 除既有证据过期项外全绿 / PowerShell 隔离安装 PASS / `git diff --check` 洁净**；端到端隔离仓验证「消费方自有规则保留 + 受管区间写入」。`progress` **66.7%（4/6）**。S4 前 A-004 F-001（I-003 选型）由此**闭合**。
- **仍未闭合（均不阻断 S5，S6 前必须闭合）**：A-001 F-005（I-006 发布基线）、A-005 F-001（宿主行为证据）、A-005 F-002（12 份 runtime evidence 锚点过期 → S6 重捕获）、A-006/A-008 F-001（隔离仓冷启动与真实升级实测）。
- **S5 结果（2026-09-13，D-010 / E-007 / A-009）**：四个宿主面新增 `/commit`（`$commit`）壳并在安装时**默认产出**；安装输出显式区分 `governance-must` 与便利入口；**契约必达字段保持四入口不变**，边界由 README + `docs/tests/test_file_l1.py` 三个机读守卫固定（拒绝未来把 `commit` 混入必达集）；fail-closed 负例写入壳文本。回归：**docs 65 OK / skills 89 OK / PowerShell 隔离安装 PASS / 镜像 37 对一致 / `git diff --check` 洁净**；端到端隔离仓四路径均落盘。`progress` **83.3%（5/6）**。开放 required 仍为 4 项，全部属 S6 范围。- **S6 首轮（2026-09-13，D-011 / 附件）**：用户裁决 S6 **含正式发布**、**分轮推进不开残余**。I-006 冻结：版本 `0.13.3`、annotated tag 指向 main merge、资产集合沿用 v0.13.2 形态、回归矩阵与证据归属明确、cross 覆盖面（self + 新增一次 independent）；证据落 `docs/releases/runtime/v0.13.3/`（不改写历史快照）。隔离仓冷启动 + 升级重放实测完成（消费方规则保留、受管区间幂等、生产仓 VP 行不泄漏）。`skills/tests/test_skills_orchestrator.py` 的证据日期断言由硬编码 `-2026-08-` 改为**按实际捕获日期形状**断言。**S6 未完成项保持 open required，不得以 residual 关门。**- **S6 首轮（2026-09-13，D-011 / D-012 / E-008）**：回归全绿；12 格 runtime 证据在 `docs/releases/runtime/v0.13.3/` 重捕获（claude 2.1.270 / grok 1.0.30 / copilot 1.0.75，全部 pass），`capture_runtime_evidence --check` 12/12 一致，`compatibility_report --require-ready` 通过（`ready-for-release-evidence`），release rehearsal 通过。Copilot 首轮因 BYOK 模型失效而 fail（`deepseek-v4-flash` 已停用）→ 改为显式传 `--model gemini-3.8-flash-high` 后四格 pass，失败 JSON 保留但未被引用。版本落地 `0.13.3`。**仍未完成**：S6 independent 关门审计落盘、PR/merge、annotated tag + workflow、Release 资产核对、`/commit` 单列证据。