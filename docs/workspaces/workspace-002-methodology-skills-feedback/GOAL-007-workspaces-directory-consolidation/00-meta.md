---
id: GOAL-007-workspaces-directory-consolidation
title: 工作区目录统一收敛与正式发布
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-10
updated: 2026-08-11
version: 0.5.0
progress: 80%
---

# GOAL-007 · 工作区目录统一收敛与正式发布

## 概述

修订核心方法论，将显式工作区从治理根直属的 `workspace-<NNN>-<slug>/` 统一收敛到 `{governance_root}/workspaces/workspace-<NNN>-<slug>/`，同步更新发现、校验、安装、打包与消费适配面；随后迁移本仓三个显式工作区，经全量验证与 cross 审计无开放 required finding 后，通过 PR 合入 `main`，创建 annotated tag 并发布、核验 Release 资产。

本目标属于 Root R3「持续闭环与长期演进」阶段，承接用户在实际多工作区使用中发现的治理根可查阅性问题。

## 成功标准

1. 核心方法论、愿景对齐、目录布局、模板和消费入口统一采用 `{governance_root}/workspaces/workspace-<NNN>-<slug>/`；兼容与 fail-closed 规则明确且可测试。
2. 本仓 `workspace-001`、`workspace-002`、`workspace-003` 完整迁移到 `docs/workspaces/`，canonical scope、Q2 链接、愿景投影、MCP/安装/打包路径与测试同步，无第二套目标真相或遗留活动路径。
3. canonical → Skills 镜像经 stage 刷新且 `--check` 无漂移；仓库全量测试、静态路径扫描和 whitespace 检查通过。
4. cross 审计完成：至少一条 self 与一条指定 provider 的 independent 意见均落盘；所有 required findings 合法闭合。
5. PR 在 CI 全绿后合入 `main`；annotated tag 指向合并后的 main；正式 Release 资产、sha256 与 release evidence 均完成核验。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **S1** | 影响面盘点与方案冻结 | **完成**（2026-08-10） | D-002 冻结唯一新 canonical + 旧布局迁移门禁；D-003 冻结 v0.13.2；D-004 指定 Grok Build independent provider |
| **S2** | 核心方法论与实现面修订 | **完成**（2026-08-11） | 只改 canonical 后 stage 镜像；同步 prompts、install、MCP、packaging 与测试 |
| **S3** | 本仓工作区迁移与全量验证 | **完成**（2026-08-11） | 迁移三个显式工作区，修正 canonical scope/Q2/愿景投影；运行全量回归与路径/whitespace 核验 |
| **S4** | cross 审计与 finding 闭环 | **完成**（2026-08-11） | A-001 self pass；A-002 Grok conditional；A-003 将 F-001 fixed，开放 required = 0 |
| **S5** | PR、main、tag 与 Release 资产 | 未开始 | PR CI 全绿后合并；annotated tag；正式资产发布、下载后 digest/evidence 验收；关门审计 |

阶段间串行；S2 内可并行修改独立消费面，S4 未通过不得进入 S5。

## 派生进度展示

`progress: 80%` = 路线图检查点 S1～S5 已完成 **4 / 5**（等权）。progress 仅展示，不放行阶段、不关闭 finding、不覆盖信息门禁，也不自动推导 `done`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 从旧直属路径迁移到 `workspaces/` 的兼容策略：原位拒绝、迁移检测、是否支持短期双读，以及消费仓升级行为 | S1 方案冻结 / S2 实施 | S1 | 盘点协议、安装器、MCP、打包、现有三工作区与历史链接；形成 D-002 | **verified**（2026-08-10） | 新旧布局并存或迁移工具需求变化时复核 | D-002：新路径唯一 canonical；旧布局只检测/引导迁移；混合布局 fail closed；安装/更新不静默移动 |
| I-002 | required | cross 审计的 independent provider | S2 实施 | S1 | 用户按 P-004 指定 provider；记录失败不降级规则 | **verified**（2026-08-10） | provider 失效时回到门禁 | 用户书面指定 Grok Build；D-004 |
| I-003 | required | 发布版本、tag 与候选 revision 如何与当前 `dev`/Release 基线对齐 | S5 发布 | S3 验收前 | 读取版本源、矩阵、release workflow 与当前远端基线；冻结发布版本 | **verified**（2026-08-10） | 若 main/tag 基线前移则重算 | D-003：下一补丁版 `v0.13.2`；更新 matrix candidateRevision、CHANGELOG、pins 与 release evidence |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)（R3 纲领阶段内子目标）

## 台账布局

本目标使用平铺 ledger：`01-decision/`、`02-execution/`、`03-audit/`；稳定索引文件只登记条目，附件保存在 `attachments/`。
