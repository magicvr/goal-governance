---
id: GOAL-003-consumer-governance-ergonomics
title: 修复消费仓门禁与长流程治理摩擦
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-03
updated: 2026-08-04
version: 0.2.0
progress: 14%
---

# GOAL-003 · 修复消费仓门禁与长流程治理摩擦

## 概述

承接真实项目使用中确认的五类问题，修正消费仓与生产仓的证据边界、长记录存储、审计启动、长流程 Git 回溯以及 Skills 更新体验，使治理协议在长目标和实际消费仓中既可审计，也可持续使用。

本目标属于 Root 纲领 **R2（反馈驱动的协议 / Skills 修正）**。范围横跨核心原则、目标模板、Skills 编排、消费契约与安装/更新路径，尚不可直接执行；先按 P-001 冻结问题与契约，再分阶段实施。当前立项不代表任一方案已经实现或通过审计。

## 已确认反馈输入

| ID | 用户确认的问题 | 初始验收方向 |
|----|----------------|--------------|
| FB-001 | 消费仓门禁错误要求 Skills runtime 证据；该证据属于生产仓发布/验证职责，且不应要求消费仓手工删门禁 | 明确 producer / consumer 角色与证据责任；消费仓默认不产生、不删除生产证据门禁 |
| FB-002 | `03-audit.md` 等单文件随记录增长而过长，显著降低可读性；其它多记录文件可能同样受影响 | 建立可量化、可迁移、可索引的多记录存储规则，并评估“达到阈值再拆”与“预期多记录即分目录” |
| FB-003 | 每次都要求用户手工决定 self / independent audit，阻碍“一次性推进到关门” | 按风险与阶段分级选择无需审计 / self / independent / cross-audit；需要独立工具但未指定时再向用户请求 |
| FB-004 | 长目标不会在合理节点自动 Git 提交，失败后难以回溯 | 在明确、可恢复且不会卷入无关用户改动的节点创建治理 checkpoint commit |
| FB-005 | 已安装 Skills 缺少自动更新路径，重复完整安装成本高 | 提供可版本化、可校验、可回滚的更新/同步机制，避免每次完整重装 |

## 成功标准（可验证）

- [ ] producer / consumer 证据责任已成为可执行契约；消费仓回归证明不再要求生产仓 runtime evidence，也不需要手工删除门禁
- [ ] 多记录文件的存储选择有确定性规则、量化阈值或明确的默认目录策略；`03-audit` 及其它适用记录支持索引、迁移与旧格式兼容
- [ ] 审计启动策略能按风险和阶段稳定选择 `none` / `self` / `independent` / `cross`，支持用户指定一个或多个独立工具，并保留 required finding、冲突与 residual 的 P-004 裁决
- [ ] `/govern` 长流程能在已定义的安全节点创建可追溯 Git checkpoint；脏工作树、无关改动、验证失败、提交失败和用户禁用均有 fail-closed 行为
- [ ] 已安装 Skills 可发现并应用兼容更新，保留版本固定、来源校验、离线/回滚路径，不要求每次完整重装
- [ ] canonical 文档、模板、prompts、契约、安装/更新实现及生成镜像保持一致，相关单元、集成与消费仓 fixture 回归通过

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 现状复现与契约冻结 | **完成**（2026-08-04） | I-001～I-007 完成当前阶段所需收集；五项问题均有可复现路径、责任边界与验收矩阵 |
| **S2** | producer / consumer 证据门禁修正 | **进行中** | 消费仓不再继承生产 runtime evidence 门禁；生产发布证据要求未被削弱 |
| **S3** | 可扩展记录布局与迁移 | **进行中** | 拆分谓词、索引/平铺布局、编号、迁移与兼容读取落地并验证 |
| **S4** | 风险分级审计编排 | **进行中** | 审计模式选择、独立工具路由、多意见合并及缺工具交互规则落地并验证 |
| **S5** | Git checkpoint 工作流 | **进行中** | 合理节点、提交范围、失败/恢复和脏树保护落地并验证 |
| **S6** | Skills 更新与同步路径 | **进行中** | 版本发现、校验、兼容判断、增量更新与回滚落地并验证 |
| **S7** | 集成回归、迁移与发布准备 | 未开始 | canonical / 镜像无漂移；当前与兼容消费 fixture 通过；关门证据可核对 |

S1 先行；S2～S6 可在各自 required 信息项闭合后并行；S7 汇总验收。是否为 S2～S6 创建子目标，待 S1 按独立范围、依赖与并行价值判断，不在立项时机械拆分。

## 派生进度展示

`progress: 14%` = 上方 7 个显式阶段完成 **1 / 7**（等权，四舍五入）。progress 仅展示，不放行阶段、不关闭 finding、不推导 `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 哪些规则、脚本或消费 fixture 将生产仓 runtime evidence 错施加到消费仓；producer / consumer 如何机读判定 | S1 / S2 方案冻结 | S2 前 | 建最小消费仓复现；追踪 gate / contract / validator 调用链；列职责矩阵与负例 | **verified**（2026-08-04） | — | `install -All` 无差别复制 `skills/contracts/**`；matrix / runtime-evidence schema 与消费契约混装。生产验证脚本只应留在生产/发行面 |
| I-002 | required | 哪些记录文件会持续增长；采用阈值拆分还是默认多文件目录；“内容较多”的量化谓词与迁移边界是什么 | S3 方案冻结 | S3 前 | 统计现有文件字节数、行数、A/D/时间线条目数与读取成本；比较两种布局及兼容解析 | **verified**（2026-08-04） | — | 最大 audit 229,150 B / 3,975 行 / 64 条；decision 90,354 B / 47 条。采用新目标默认 ledger 目录 + legacy 阈值迁移 |
| I-003 | required | 哪些风险/阶段允许无审计后继兜底，哪些要求 self、independent 或 cross-audit | S4 方案冻结 | S4 前 | 建风险因子、决策表、反例与 close-out 场景；验证 required finding / P-004 不被绕过 | **verified**（2026-08-04） | — | D-005 风险矩阵冻结；required finding / 冲突 / residual 继续 P-004 fail closed |
| I-004 | required | 独立审计工具如何由用户按会话指定一个或多个；能力、可用性、失败与未指定时如何处理 | S4 实施 | S4 实施前 | 盘点宿主可调用工具；定义 provider 列表、顺序/并行、结果归并与 fail-closed 契约 | **verified**（2026-08-04） | — | provider 为会话级有序集合；independent/cross 需要 provider，缺失时仅在实施前询问；本目标用户已指定 Grok Build |
| I-005 | required | “合理提交节点”的确定性定义，以及 staged/unstaged、无关用户改动、验证失败、无变更、commit 失败和禁用策略 | S5 方案冻结 | S5 前 | 构造脏树/部分失败/恢复矩阵；评估事务边界、提交 ownership 与可回滚证据 | **verified**（2026-08-04） | — | D-006 冻结阶段/独立切片/finding 闭合 checkpoint；仅显式 owned paths，验证失败或路径重叠不提交 |
| I-006 | required | Skills 更新源、版本发现、兼容判断、信任/摘要、增量覆盖、回滚、离线与各宿主约束 | S6 方案冻结 | S6 前 | 对照当前 pinned bootstrap/install；比较 update / sync / reinstall 模型并做威胁与兼容分析 | **verified**（2026-08-04） | — | D-007 选择包内 updater：latest/固定版、在线/离线、SHA-256、协议预检、备份、失败自动恢复 |
| I-007 | required | 新规则对现有仓库、旧五件套、当前/前一协议与安装面的兼容和迁移基线 | S7 验收 | S7 前 | 建 legacy/current fixture 矩阵、迁移 dry-run、回滚与发布证据要求 | **verified for plan**（2026-08-04） | S7 以 fixture 实测复核 | legacy inline 继续可读；新目录为 additive protocol；consumer 负例、legacy/current parser、updater rollback 纳入 S7 |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)

## 备注

- 本目标修正的是通用方法论与 Skills 产品边界，不要求消费仓自行打补丁。
- 在 S3 冻结并迁移前，本目标仍使用现行五件套和单一 `03-audit.md`，避免用未决方案承载自身权威记录。
- 涉及 `docs/architecture`、`docs/templates`、`docs/contracts` 或 `docs/vision/alignment.md` 的 canonical 变更时，必须同轮运行 mirror stage 与 `--check`。
