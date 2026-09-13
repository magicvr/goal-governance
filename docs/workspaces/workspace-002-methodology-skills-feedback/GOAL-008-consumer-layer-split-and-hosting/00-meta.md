---
id: GOAL-008-consumer-layer-split-and-hosting
title: 双层路线图拆分与消费仓宿主共存
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
progress: 0%
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
- [ ] 默认提供 `/commit` 命令；边界与 `/govern` checkpoint 不冲突；已支持的消费宿主可调用
- [ ] canonical 文档、模板、prompts、契约、安装面及生成镜像保持一致；相关测试与发布门禁通过

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 现状复现与契约冻结 | 未开始 | I-001～I-005 完成当前阶段所需收集；四项问题均有可复现路径、责任边界与验收矩阵；不预先冻结实现选型 |
| **S2** | 双层路线图语义拆分 | 未开始 | 判定谓词、反例与 prompts/模板修订落地；AI 不再把愿景总路线图当执行路线图、把 VP 当子目标 |
| **S3** | 愿景总路线图与 VP 跟踪解耦 | 未开始 | 总路线图与 VP 跟踪权威落点分离；跟踪信息不在总路线图内膨胀 |
| **S4** | 消费仓 `AGENTS.md` / `docs/` 共存 | 未开始 | 安装面为消费仓自有规则与项目文档留出共存空间，兼容完整安装 MUST |
| **S5** | 默认 `/commit` 命令 | 未开始 | `/commit` 可调用；与 checkpoint 职责分离；脏树/无关改动/失败 fail closed |
| **S6** | 回归、审计与发布 | 未开始 | canonical / 镜像无漂移；cross 审计无开放 required；正式发布证据可核对 |

S1 先行。S2 与 S3 通常串行（S3 依赖 S2 的命名与权威落点）。S4 与 S5 可在各自 required 信息项闭合后并行。S6 汇总验收。是否为 S2～S5 创建子目标，待 S1 按独立范围、依赖与并行价值判断，不在立项时机械拆分。

## 派生进度展示

`progress: 0%` = 上方 6 个显式阶段完成 **0 / 6**（等权）。progress 仅展示，不放行阶段、不关闭 finding、不推导 `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 当前原则、alignment、prompts、模板中，组合编排 / 纲领路线图 / 阶段计划 / VP / 子目标的命名与判定是否足以阻止把 VP 当子目标、把愿景路线图当执行路线图；缺口在哪些文件 | S1 / S2 方案冻结 | S2 前 | 盘点 P-006、alignment、`/govern` `/vision` prompts、目标与愿景模板；构造最小反例（一区一 Root 一 VP） | open | — | 待确认 |
| I-002 | required | 愿景「总路线图」当前承载了哪些 VP 跟踪信息；权威应落在 `roadmap.md`、VP 正文、还是独立索引；解耦后的最小完备字段是什么 | S1 / S3 方案冻结 | S3 前 | 对照 `docs/vision/roadmap.md`、各 `VP-*.md`、alignment 工件表与消费模板 | open | — | 待确认 |
| I-003 | required | 消费安装如何写入根 `AGENTS.md` 与 `docs/`；与消费仓自有 agent 规则、项目文档的冲突面；可行共存模型（覆盖 / 合并 / 命名空间 / overlay / 可配置治理根之外的项目文档树）及完整安装 MUST 约束 | S1 / S4 方案冻结 | S4 前 | 盘点 install 脚本、`AGENTS.template`、core→docs 复制、updater 覆盖策略与已安装消费仓样本 | open | — | 待确认 |
| I-004 | required | `/commit` 与 `/govern` Git checkpoint 的职责边界；提交范围（治理 owned paths vs 用户指定）；多宿主入口（claude / copilot / grok / codex）；脏树、无关改动、验证失败、用户禁用的 fail-closed 行为 | S1 / S5 方案冻结 | S5 前 | 对照 GOAL-003 D-006 checkpoint 契约与现有宿主 skill 入口；列出命令契约与负例 | open | — | 待确认 |
| I-005 | required | S2/S3 触及元规则与协议，关门审计模式为 `cross`；independent provider 是谁；失败是否 fail closed | S2 实施 | S1 | 用户按 P-004 指定 provider；记录失败不降级 | open | provider 失效时回到门禁 | 待用户指定 |
| I-006 | required | 正式发布版本、tag 与当前 `dev`/Release 基线如何对齐 | S6 发布 | S6 前 | 读取版本源、矩阵、release workflow 与当前远端基线后冻结 | open | 基线前移时重算 | 待 S1 后或发布前冻结 |

四项反馈本身已由用户书面提交，不构成「问题是否存在」的未知；上表只登记**如何改**所需的信息。开放 required 只阻断对应阶段，不阻断本目标设立。

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)（R3 纲领阶段内子目标）

## 台账布局

本目标使用平铺 ledger：`01-decision/`、`02-execution/`、`03-audit/`；稳定索引文件只登记条目，附件保存在 `attachments/`。

## 备注

- 本目标修正的是通用方法论与 Skills 产品边界，不要求消费仓自行打补丁。
- 涉及 `docs/architecture`、`docs/templates`、`docs/contracts` 或 `docs/vision/alignment.md` 的 canonical 变更时，必须同轮运行 mirror stage 与 `--check`。
- 立项只登记问题、路线图与信息门禁；S1 完成前不改协议正文、安装器或 Skills 实现。
