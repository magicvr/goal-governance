---
id: GOAL-007-information-readiness-governance
title: 信息就绪与未知项治理
status: done
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.2.1
progress: 100%
---

# GOAL-007 · 信息就绪与未知项治理

## 概述

将“设立目标时不一定已知所有必需信息”纳入核心目标治理协议。目标可以带未知项立项，但未知项必须可追踪，并在影响规划、实施或关门前以证据、决策或经用户接受的残余风险处理。

本目标只演进核心文档协议、模板与 Skills 适配器；不在本轮改变 Web 的 Markdown 解析数据合同或新增 Web 写入能力。

## 成功标准

- [x] P-005 明确允许带未知项立项，并定义未知项登记、阶段门禁与残余风险接受规则
- [x] canonical 五件套模板提供信息需求、阶段门禁、收集事实与审计核对的写作起点
- [x] `/govern`、创建/决策/执行/审计原语与 `/audit` 能按 P-005 发现、记录和审查未知项
- [x] 根规则、安装源与 Skills 分发说明同步 P-005，不遗留 P-001～P-004 的过时表述
- [x] 自动化测试覆盖协议文本、模板镜像与独立核心包复制场景

## 信息就绪概览

| ID | 级别 | 所需澄清 | 影响门禁 | 最晚阶段 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|----------|----------|----------|------|-------------|-------------|
| I-001 | non-blocking | 本轮是否必须扩展 Web 的结构化数据合同 | 实施范围 | 阶段 A | verified | 不适用 | 当前 Web 仅解析固定元数据；本目标先保持协议文本层，由 D-001 界定 |

## 高层路线图

| 阶段 | 主题 | 状态 | 退出证据 |
|------|------|------|----------|
| A | 定义 P-005、未知项登记与阶段门禁 | 已完成 | `AGENTS.md`、`docs/architecture/principles.md` 与 D-001 一致 |
| B | 更新 canonical 文档、模板与分发镜像 | 已完成 | canonical/mirror 模板经契约测试逐字节核对；独立核心包测试通过 |
| C | 更新 Skills 编排、原语、审计与宿主入口 | 已完成 | `00`～`05` prompts、Claude/Grok/Copilot 安装源和宿主副本均含 P-005 |
| D | 运行契约测试并进行关门自审 | 已完成 | 26 + 3 + 20 项测试通过；语义契约防回归；A-001 无开放 required finding；根目标 A-005 关闭 F-004 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 相关路径

- [P-005 原则](../../architecture/principles.md)
- [根目标审计 A-004](../GOAL-001-main-vision/03-audit.md)
- [核心 canonical 模板](../../templates/goal-folder/)
