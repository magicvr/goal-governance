---
id: GOAL-008-consumer-layer-split-and-hosting
title: 双层路线图拆分与消费仓宿主共存
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.4.0
progress: 33.3%
---

# GOAL-008 · 双层路线图拆分与消费仓宿主共存

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

## 成功标准（暂定，可验证）

- [ ] 组合编排 / 纲领路线图 / 阶段计划 / VP / 子目标有可执行判定谓词与反例；消费面 prompts 与模板不再把愿景总路线图当执行路线图，也不把 VP 当子目标设计
- [ ] 愿景层总路线图只保留组合编排应关注的内容；VP 跟踪信息不在该文件内膨胀
- [ ] 消费仓可在兼容目标治理的前提下维护自有 agent 规则与项目文档，不必把框架 `AGENTS.md` / `docs/` 当作唯一占用面
- [ ] 在已支持的消费宿主上默认提供 `/commit` **便利入口**；**不**进入完整治理安装 MUST、治理入口必达集，也**不**替代 `/govern` checkpoint；失败路径 fail closed
- [ ] canonical 文档、模板、prompts、契约、安装面及生成镜像保持一致；相关测试与发布门禁通过（范围以 I-006 冻结的版本/资产/回归/证据归属为准）

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 现状复现与契约冻结 | **完成**（2026-09-13） | I-001～I-004 完成当前阶段收集（I-001/I-002/I-004 `verified`；**I-003 `partially-verified`**，共存模型选型待用户裁决）；验收矩阵含可复现路径、责任边界证据、验收人/审视方式、各阶段证据路径；S4/S5 owned paths 已列并判定 **S4→S5 串行**（[D-006](01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md)）。本轮不要求 I-005 provider 或 independent 输出（independent 复审 A-005 待执行，未完成前不得宣称 S1 契约已获交叉验证） |
| **S2** | 双层路线图语义拆分 | **完成**（2026-09-13） | I-005 provider 已书面指定（本地 grok build / grok-4.6 / effort high，2026-09-13）；判定谓词与 prompts/模板落地；固定 probe/corpus、正反例、通过阈值、覆盖的宿主/提示词面可核对（corpus 已登记于 [验收矩阵](attachments/s1-acceptance-matrix.md) §4，静态执行结果见 [E-004](02-execution/E-004-s2-layer-semantics.md)）。**未**跑真实宿主 probe，故不宣称「AI 已不再混淆」（[A-005](03-audit/A-005-s2-stage-self.md) F-001，S6 闭合） |
| **S3** | 愿景总路线图与 VP 跟踪解耦 | 未开始 | 跟踪权威落点锁定（模型 = **A1 索引承载投影**，[D-005](01-decision/D-005-s3-consumer-compat.md)）；既有数据迁移/兼容读取规则落盘；重复信息不存在可核验 |
| **S4** | 消费仓 `AGENTS.md` / `docs/` 共存 | 未开始 | 已选定共存模型（候选 A～E 见 [盘点 §2.C](attachments/s1-inventory-evidence.md)，**选型须用户裁决后才可冻结方案**）；安装面为消费仓自有规则与项目文档留出共存空间；完整安装 MUST 与保护既有规则/文档的负例测试通过 |
| **S5** | 默认 `/commit` 便利入口 | 未开始 | 已支持宿主可调用；非完整安装 MUST、非治理入口必达、非 checkpoint 替代；owned paths / 既有用户改动 / 无改动或非 Git / 验证失败 / 提交失败 / 用户禁用的负例 fail closed |
| **S6** | 回归、审计与发布 | 未开始 | I-006 已冻结（版本、tag/revision、资产清单、回归矩阵、cross 覆盖、consumer vs producer 证据归属）；canonical/镜像无漂移；cross 无开放 required；正式发布证据可核对 |

S1、S2 **已完成**。S3 依赖 S2 的命名与权威落点（现均已就位）。S4 与 S5 经写集判定为 **S4→S5 串行**（[D-006](01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md)：安装器/更新器/契约/机读守卫四处写集重叠且 S5 依赖 S4 的安装面决策）。S6 汇总验收。**S2～S5 不另开子目标**：用户 2026-09-13 裁决「先等 S1 结论再按需拆」，S1 结论为各阶段写集与证据可在本目标内闭环（P-006 §6.6 停止条件），故留在 GOAL-008 内按阶段推进（[E-003](02-execution/E-003-s1-inventory.md)）。A-001 F-005 未闭合前不得宣称 S6 可发布；I-003 选型未裁决前不得冻结 S4 方案；宿主行为证据与 runtime evidence 锚点（A-005 F-001/F-002）在 S6 闭合前不得宣称「AI 已不再混淆」或发布就绪。

## 派生进度展示

`progress: 33.3%` = 上方 6 个显式阶段完成 **2 / 6**（等权；S1、S2 完成）。progress 仅展示，不放行阶段、不关闭 finding、不推导 `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 当前原则、alignment、prompts、模板中，组合编排 / 纲领路线图 / 阶段计划 / VP / 子目标的命名与判定是否足以阻止把 VP 当子目标、把愿景路线图当执行路线图；缺口在哪些文件 | S1 / S2 方案冻结 | S2 前 | 盘点 P-006、alignment、`/govern` `/vision` prompts、目标与愿景模板；构造最小反例（一区一 Root 一 VP） | **verified** | — | 结论：**不足**。命名表缺「子目标」「VP 内阶段结构」行；`总路线图` canonical 零出现；消费端规则面无消歧表；in-repo 先例示范混淆。[证据](attachments/s1-inventory-evidence.md) §2.A |
| I-002 | required | 愿景「总路线图」当前承载了哪些 VP 跟踪信息；权威应落在 `roadmap.md`、VP 正文、还是独立索引；解耦后的最小完备字段是什么 | S1 / S3 方案冻结 | S3 前 | 对照 `docs/vision/roadmap.md`、各 `VP-*.md`、alignment 工件表与消费模板 | **verified** | — | roadmap.md = 愿景总路线图；4 列与 VP frontmatter 重复且 4/4 一致；无脚本解析；权威模型 = **A1 索引承载投影**（[D-005](01-decision/D-005-s3-consumer-compat.md)）。[证据](attachments/s1-inventory-evidence.md) §2.B |
| I-003 | required | 消费安装如何写入根 `AGENTS.md` 与 `docs/`；与消费仓自有 agent 规则、项目文档的冲突面；可行共存模型（覆盖 / 合并 / 命名空间 / overlay / 可配置治理根之外的项目文档树）及完整安装 MUST 约束 | S1 / S4 方案冻结 | S4 前 | 盘点 install 脚本、`AGENTS.template`、core→docs 复制、updater 覆盖策略与已安装消费仓样本 | **partially-verified**（选型仍 open） | 选型未裁决时 S4 方案冻结保持阻断 | 写入面/硬软冲突/13 条负例已核实（[证据](attachments/s1-inventory-evidence.md) §2.C）；候选 A～E **尚未选优** |
| I-004 | required | `/commit` 命令形状、宿主覆盖与 fail-closed 负例（治理边界已由 D-002 冻结：便利可选，非 MUST / 非治理必达 / 非 checkpoint 替代） | S1 / S5 方案冻结 | S5 前 | 对照 GOAL-003 D-006、VP-004 入口面、`.github/prompts/commit.prompt.md`；列出命令契约与负例 | **verified** | — | 现仅 monorepo 自用 prompt，安装面未实现；契约缺「默认安装但不入必达集」表达位；8 类 fail-closed 未规定。[证据](attachments/s1-inventory-evidence.md) §2.D |
| I-005 | required | S2/S3 触及元规则与协议，关门审计模式为 `cross`；independent provider 是谁；失败是否 fail closed | S2 实施 | S2 实施前 | 用户书面指定 provider；失败/超时/无可核对输出不降级 | **closed** | provider 失效时回到门禁 | 用户 **2026-09-13** 指定：本地 grok build（`grok` 1.0.30 / **grok-4.6** / `--reasoning-effort high`）；本机已核对 `grok --version` 与 `grok models` |
| I-006 | required | 正式发布版本、tag/revision、资产清单、回归矩阵、cross 覆盖面、consumer vs producer 证据归属，以及与当前 `dev`/Release 基线的对齐 | S6 发布 | S6 前 | 读取版本源、矩阵、release workflow 与当前远端基线后冻结 | open | 基线前移时重算 | 待 S1 后或发布前冻结；F-005 绑定本项（仍阻断 S6 发布） |

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
- **S2 结果（2026-09-13，D-007 / E-004 / A-005）**：命名表由 4 类扩为 **6 类**（补「子目标」「VP 内阶段结构」）并新增**落位谓词 8 条**与「职责/权威非节点数量」守卫；`总路线图` 口语映射四处落盘；消费端规则面新增 **§6e.1**（三宿主同文）；新增 `docs/templates/vision/roadmap.md` 与目标/愿景模板槽位；机器守卫测试 2 套新增。回归：skills 43 OK、docs 56 OK、consumer-surface+mcp 25 OK、镜像 37 对一致、`git diff --check` 洁净。`progress` **33.3%（2/6）**。副作用：根 `AGENTS.md` 变更使 12 份 runtime evidence 锚点过期 → **S6 重捕获**（A-005 F-002）。S1/S2 的 independent 复审（grok build）**待出具**，未完成前不得宣称已获交叉验证。
