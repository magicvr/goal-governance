---
id: GOAL-022-docs-ssot-skills-mirror-stage
title: 方法论单一真相源与 Skills 镜像 stage 化
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.2.0
progress: 83%
---

# GOAL-022 · 方法论单一真相源与 Skills 镜像 stage 化

## 概述

消除 monorepo 中「`docs/` canonical 与 `skills/core` / `skills/templates` / `skills/contracts` 镜像」的**人工双份（乃至三份）维护**：日常只改 `docs/`（及真正属于 Skills 适配器的 prompts/install），在 **pack / CI / 本地 stage** 时按白名单生成分发镜像；发布物 zip 内仍保留 `core/` 等路径（GOAL-019 D-003/D-004 不变），但源码树不再依赖手同步。

**有界**：本目标交付机制与测试/文档门禁，**不**授权 annotated tag / GitHub Release，**不**改 Root/Charter/VP status，**不**开启阶段 7。

## 成功标准

- [x] 已冻结 stage 白名单 / 排除表 / 不得盲拷的变换面（D-002）
- [x] 存在可重复的 `stage` 脚本（或等价入口），从 `docs/` 生成 core 必备文件与 contracts 镜像
- [x] `pack_skills_release`（及 CI pack 路径）在打包前强制 stage；缺 core / 误带 tech-stack 仍 fail closed
- [x] 五件套不再出现「docs + core + skills/templates」三边手维；`skills/templates` 已收敛为指针
- [x] 字节一致类镜像由自动化断言；消费方精简 README / vision 短说明为手维例外
- [x] docs / scripts / skills 相关测试绿；技能 README / core README / docs 同步说明已更新
- [ ] 阶段自审或关门审通过且用户确认（若选关门）

## 纲领路线图（P-001）

| 阶段 | 内容 | 完成标记 |
|------|------|----------|
| **A · 方案冻结** | 白名单、排除、git 是否提交生成物、templates 三副本策略、README 精简策略；关闭 I-001～I-003 | [x] |
| **B · stage 实现** | `scripts/stage_skills_mirrors.py` + 单测；生成 core architecture/templates/alignment + contracts | [x] |
| **C · pack / CI 挂接** | pack 前 stage；workflow 与本地 `pack_skills_release` 一致；防手改镜像漂移 | [x] |
| **D · 消冗余与文档** | 收敛 `skills/templates`；更新 skills/core README、docs 台账、install/开发者路径说明 | [x] |
| **E · 变换面（按 A 决议）** | 消费方 README 手维精简；vision README 保持手维；I-004 AGENTS residual | [x] |
| **F · 回归与关门** | 全量相关测试；自审/用户确认；开放 required=0 | [ ] |

**派生 progress**：5/6 = **83%**。progress 仅为展示，不构成放行或发版证明。

## 信息就绪与未知项（P-005）

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 生成镜像是否入库提交 | 方案冻结 A | A | 用户裁决 | **closed** | — | D-002：仍提交 git + CI 强制 stage |
| I-002 | required | `skills/templates/` 收敛策略 | 阶段 D | A | 用户裁决 | **closed** | — | D-002：取消手维；core/docs/templates 唯一分发源 |
| I-003 | required | core `docs/README` 策略 | 阶段 E | A | 用户裁决 | **closed** | — | D-002：手维真正精简稿 |
| I-004 | non-blocking | AGENTS 家族是否纳入本目标 | 可选范围 | F 前 | residual | **closed (out of scope)** | follow-up | D-002：本目标不纳入；可另立 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 关联

- 承接会话分析：canonical `docs/` vs 分发镜像双（三）份维护税。
- 不重开 GOAL-019（D-003/D-004 产品形态保留）。
- 与 GOAL-018/021 pack/证据链衔接。

## 备注

- 路径 D 单点工作。
- 非目标：dogfood vision 实例进 zip；tech-stack；静默 tag/Release。
