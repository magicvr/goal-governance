---
id: GOAL-017-on-demand-governance-context
title: 消费仓治理规则按需加载与新资产发布
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-03
updated: 2026-11-03
version: 0.1.0
progress: 75%
---

# GOAL-017 · 消费仓治理规则按需加载与新资产发布

## 概述

用户反馈：消费仓根 AGENTS.md 长期加载大量目标治理提示，即使当前任务不涉及目标治理。把框架常驻内容缩为必要的触发与导航入口，完整指南在需要时加载，并完成 dev 开发、PR 合入 main 与 CI 新资产发布。

父目标 R3 内承接真实消费反馈；继承 [Root](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md) → VP-002 → Charter 的边界，不新增 VP/工作区，不改变愿景方向。

## 成功标准

- [ ] 消费安装的治理常驻块有明确体积预算并显著缩减；非治理任务无需读取完整治理指南。
- [ ] 显式治理命令、自然语言治理意图和治理记录修改均能在操作前加载完整规则；缺失或非法根配置时停止受影响的治理操作。
- [ ] 新装、已有受管块升级、旧整文件迁移、自定义治理根及用户自有规则保留均有可核对验证。
- [ ] canonical、Skills/宿主入口、core-only 分发与实际打包资产一致，相关回归及 self + independent 审计通过，无开放 required。
- [ ] dev → PR → main CI → annotated tag → CI 发布完成，下载资产摘要、隔离消费安装及适用 GHCR 版本核对通过。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| S1 | 信息确认与加载契约 | 完成（D-003） | 触发边界、规则落点、体积预算、升级兼容与 cross provider 确定，冻结实施方案 |
| S2 | canonical 与消费面实施 | 完成（E-003） | 先更新架构约定，再同步模板、宿主入口、安装/升级与镜像，定向验证通过 |
| S3 | 验证与交叉审计 | 完成（E-004 / A-003） | 回归、隔离新装/升级、按需加载验证、运行证据刷新及 cross 意见闭环 |
| S4 | PR、CI 发布与验收 | 进行中 | dev PR 全绿合入 main，严格发布门禁通过，CI 发布与实际资产验收完成，关门结论落盘 |

S1 → S2 → S3 → S4 串行；每阶段允许独立探索并行。progress 按完成阶段数 / 4 等权派生，当前 3/4 = 75%，不作门禁依据。

## 信息就绪与门禁

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 规则生成、加载入口及旧安装保护边界 | S1 方案冻结 | S1 | 定位安装源、merge/update 与宿主入口 | verified | 实施写集冻结时复核 | D-003：加载链、stage 与递归安装映射已核对 |
| I-002 | required | 本会话 independent provider | 实施与 cross 审计 | S1 / 实施前 | 用户回答 Q-001 | verified | provider 失败时复核 | D-002：本地 Grok Build CLI，Grok 4.7 / xhigh |
| I-003 | required | 非治理不加载、治理必加载及升级兼容是否成立 | S3 验收 | S3 | 定向测试、隔离消费安装/升级与实际宿主探针 | verified | 实施后验证 | E-004 / A-003，代表配置实际加载对照与16格选用pass |
| I-004 | required | 发行版本、当前 behaviorSources、发布证据及审批 | S4 发布 | S4 | 检查远端 tag、刷新兼容矩阵/运行证据、strict 预检与 CI | collecting | 打 tag 前复核 | 基线 v0.13.8；新版本尚未冻结，Environment release 保留现有门禁 |

## 当前阻塞

Q-001 已由用户真实答复：本地 Grok Build CLI，Grok 4.7 / xhigh（D-002）。复核未见其他实施前待答或开放上游 required，已恢复 active；当前 S2 完成、S3 进行中，progress 50%；I-001 已 verified。CLI 帮助已确认 model/reasoning-effort/headless 参数存在；尚不宣称独立审计成功。S3 已取得部分运行证据，待完整集合与矩阵冻结；S4 尚未发布。

## 台账

- 决策：[01-decision.md](01-decision.md)
- 执行与待答：[02-execution.md](02-execution.md)
- 审计：[03-audit.md](03-audit.md)

