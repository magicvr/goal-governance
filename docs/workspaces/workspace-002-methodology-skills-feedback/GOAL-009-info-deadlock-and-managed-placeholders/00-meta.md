---
id: GOAL-009-info-deadlock-and-managed-placeholders
title: 未知信息门禁死锁与受管占位符升级
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-10-01
version: 0.5.8
progress: 75%
---

# GOAL-009 · 未知信息门禁死锁与受管占位符升级

## 概述

承接真实使用中的第三批反馈：未知信息环节被用成后继门禁，在研究类工作里形成「要知道结果才能开工，但只有做完才知道结果」的死锁；以及指定方法论目录与 skills 目录安装时，受管范围内替换占位符会导致升级脚本报错。本目标先把两条失败模式核对清楚，再分别修正规则语义和安装/升级行为。

本目标属于 Root 纲领 **R3（持续闭环与长期演进）**。P-005 的原文仍以 `docs/architecture/principles.md` 为唯一原则真相；奠基期引入该原则的已关门目标是 [workspace-001 的 GOAL-007](../../workspace-001-goal-governance/GOAL-007-information-readiness-governance/00-meta.md)，本目标不重开该节点。

## 已确认反馈输入

| ID | 用户确认的问题 | 初始验收方向 |
|----|----------------|--------------|
| FB-010 | 「未知信息」容易被异化为门禁。设计本意是：为达成目标，可能要先调查前置信息。实际常变成「必须先知道某些信息才能进入后继环节」，而这些信息里包含了做完后继工作才会知道的事实，于是死锁。编程等执行类场景较不明显，研究类场景很明显 | 调查本身可以是工作；只有做完后继工作才知道的事实，不得成为进入该后继工作的 required 门禁。真正先于工作存在的前置事实，在执行类场景仍可以是门禁 |
| FB-011 | 安装并指定方法论目录与 skills 目录时，受管（manage）范围内若替换了占位符，update 脚本报错。需要明确安装与升级各自怎么处理。若不替换占位符，还要判断会不会让 AI 认不出路径：会，则让 update 能处理已替换内容；不会，则改由安装侧用别的方式给出路径。用户原话在「尤其是让ai从」处截断，后半未给出 | 安装与升级对受管占位符有唯一、可升级的行为；AI 仍能定位方法论与 skills 路径。截断后的具体做法在选定「不替换」分支前补全 |

## 成功标准（暂定）

- [x] 研究型工作可以把「为达成目标而做的调查」当作工作本身推进；规则不再把「只有做完后继工作才知道的事实」写成进入该后继工作的 required 门禁。执行型场景中、真正先于工作存在的前置事实仍可以是门禁。证据：原则 P-005 第 5 条，及 `skills/tests/test_skills_orchestrator.py` 的 `test_research_result_is_not_a_gate_into_its_own_work`
- [x] 有一条可核对的死锁反例：按修订后的规则，该反例不会被它自己的结果挡住。同一测试在改文前 24 项失败，改文后通过；先于执行的事实仍会挡住进入执行
- [x] 指定方法论目录与 skills 目录之后，安装按这两个目录渲染受管占位符；升级把包内原文和这次渲染结果都视为干净，其余差异仍 fail closed。证据：[D-004](01-decision/D-004-render-placeholders-on-install.md)、[E-004](02-execution/E-004-render-placeholders.md)，以及 `test_install_ps1_rendered_placeholders_survive_update` / `test_install_sh_rendered_placeholders_survive_update`。不替换分支未采用
- [ ] 原则、编排提示、安装/升级脚本与受影响模板一致；相关测试覆盖死锁判定和安装后再升级。改了 stage 白名单时，镜像 `--check` 通过
- [ ] 消费面变更在宣称可安装使用前，经过与元规则 / 安装兼容相称的审计，开放 required 已合法闭合。发布版本不在立项时冻结

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 失败模式核对与边界冻结 | 已完成（2026-09-30） | 两条反馈都有可核对的失败模式（文件与行为，或「现有安装路径做不到用户描述的指定方式」这一负结果）；死锁反例与「真正的前置事实」反例分开写；占位符替换与 update 报错的关系写成证据或明确的未复现。本阶段不改原则正文、安装器或 Skills。证据：[D-002](01-decision/D-002-s1-evidence.md)、[附件](attachments/s1-failure-modes-2026-09-30.md) |
| **S2** | 未知信息语义修正 | 已完成（2026-09-30） | 原则、AGENTS 摘要与编排提示把「调查工作」和「后继门禁」拆开；研究类死锁反例不再被自己的结果阻断；执行类前置事实仍可设门禁。实施前已书面指定 cross 审计的 independent provider。证据：[D-003](01-decision/D-003-research-result-is-not-a-gate.md)、[E-003](02-execution/E-003-rule-distinction.md) |
| **S3** | 安装与升级的占位符策略 | 已完成（2026-09-30） | 用户选定安装时按方法论目录与 skills 目录渲染受管占位符（D-004）。升级把包内原文和这次渲染结果都视为干净，手改仍 fail closed。指定这两个目录的安装再跑升级，不再因该占位符差异报错。证据：[E-004](02-execution/E-004-render-placeholders.md) |
| **S4** | 验证、审计与消费面交付 | 进行中 | A-009（independent，pass）支持 A-008 对空后缀 F-002 的 fixed 判断。开放 required 为无。F-003 仍为 recommended。用户尚未书面确认关门，发布范围仍未冻结，本阶段未完成。未发布前不宣称消费方已经拿到修正 |

S1 先做。S1 退出后，S2（原则与提示）和 S3（安装与升级）在写集不重叠时可以并行。S4 等 S2 与 S3 都退出。`progress` 只来自本表：已完成阶段数 / 4。

## 派生进度展示

`progress: 75%` = 上表 4 个阶段完成 **3 / 4**（S1、S2、S3 已完成，S4 进行中、未完成）。progress 只展示，不放行阶段、不关闭 finding、不推导 `done`。

## 信息就绪与未知项

S1 已经核对过这些项。I-001、I-002、I-004 的证据见 D-002。I-003 已由 D-004 闭合：用户不走「不替换占位符」那一支。不得把「做完该阶段才会知道的事实」再登记成进入该阶段的门禁。

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 现行 P-005、AGENTS 第 6b 节和编排提示里，哪些句子把「为达成目标而调查」写成「未知道则不得进入后继」；其中哪些事实只有做完后继工作才存在 | S2 方案冻结 | S2 前 | S1 对照原则、编排器与一条研究类反例 | **verified**（2026-09-30） | — | [D-002](01-decision/D-002-s1-evidence.md) 与 [附件 §1](attachments/s1-failure-modes-2026-09-30.md)。研究结论死锁反例与先于执行的事实反例已分开写。原则正文尚未改 |
| I-002 | required | 指定方法论目录与 skills 目录时，受管范围内哪些占位符会被替换；update 报错的具体路径与比较规则是什么。若当前安装器不能同时指定这两个目录，该不能也是结论 | S3 方案冻结 | S3 前 | S1 读安装/升级脚本并做最小复现或记录负结果 | **verified**（2026-09-30） | — | [附件 §2](attachments/s1-failure-modes-2026-09-30.md)。S1 当时不能用安装参数指定方法论目录；替换受管占位符后 `modified_managed_files` 列出 2 个路径，对照为 0。策略已由 [D-004](01-decision/D-004-render-placeholders-on-install.md) 选定 |
| I-003 | required | 若不替换占位符，已安装提示是否仍让 AI 找到方法论与 skills 路径。用户后半句在「尤其是让ai从」处截断 | S3 方案冻结里「不替换」那一支 | 选定不替换之前 | 用户选定分支；只有走不替换时才补全截断句 | **verified**（2026-09-30） | 不走该分支后，截断句不再构成门禁 | 用户书面选择安装时渲染，并书面拒绝不替换分支。见 [D-004](01-decision/D-004-render-placeholders-on-install.md)。这不是不替换时的路径实测 |
| I-004 | required | S2/S3 改元规则和安装兼容，审计模式为 `cross`；independent provider 是谁 | S2 或 S3 的实施（取先开始者） | 实施前 | 用户书面指定；失败不降级、不由编排器冒充 | **verified**（2026-09-30） | CLI 不能以该模型与强度给出可核对意见时，门禁回到未满足 | 用户书面指定本地 codex CLI，模型 `gpt-6.1-sol`，思考强度 `high`。见 D-002。A-001 与 [A-005](03-audit/A-005-f001-f002-reaudit.md) 均已落盘。用户随后选择继续修正，见 [D-007](01-decision/D-007-a005-continue-fix.md) 与 [A-006](03-audit/A-006-a005-response.md)。[A-007](03-audit/A-007-a006-reaudit.md) 对该修正的复审 verdict 为 fail：F-001、F-004 的关闭证据成立，F-002 的空后缀重新开放。用户于 2026-10-01 选择继续修正，见 [D-008](01-decision/D-008-a007-empty-suffix.md) 与 [A-008](03-audit/A-008-a007-response.md)。[A-009](03-audit/A-009-a007-reaudit.md) 对该修正的复审 verdict 为 pass。开放 required 为无。用户尚未书面确认关门 |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)（R3 纲领阶段内子目标）

## 台账布局

本目标使用平铺 ledger：`01-decision/`、`02-execution/`、`03-audit/`。索引文件只登记条目。

## 备注

- S1、S2、S3 已完成。原则区分见 D-003。占位符行为见 D-004 与 E-004。S4 进行中：A-009 对空后缀修正的复审为 pass，开放 required 为无。F-003 仍为 recommended。用户尚未书面确认关门。未发布前不宣称消费方已经拿到这次安装行为。
- 涉及 `docs/architecture`、`docs/templates`、`docs/contracts` 或 `docs/vision/alignment.md` 时，同一任务内 stage 镜像并 `--check`。
- S1 没有出现必须拆出才能取证或关门的范围。按用户「无必要则不开」，不另立子目标；S2 与 S3 仍在本目标内。
