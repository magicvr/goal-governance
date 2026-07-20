---
id: GOAL-012-first-slice-workspace-detail
title: 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内）
status: active
parent: GOAL-001-main-vision
created: 2026-07-21
updated: 2026-07-21
version: 0.1.0
progress: 0%
planning_source: GOAL-009-ai-assisted-governance-workbench
---

# GOAL-012 · 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内）

## 概述

承接 [GOAL-009](../GOAL-009-ai-assisted-governance-workbench/00-meta.md) 路线图 D / D-006 / D-011 路径 α：在 **Web** 中实现「配置选中的**产品工作区**详情（目标树核心）+ 用户提供候选执行事实 + 门禁内的受限 `append-execution-fact`」。

本目标**不是**完善只读浏览器终态；也**不是**多工作区总览、共享资料 CRUD、AI 接入或 SQLite 必选。发布物与 dogfood 分栏遵守 D-011。

## 成功标准

- [ ] Web 通过**显式配置**绑定数据根 / 工作区路径；默认**不**静默加载本仓 dogfood；开发可用显式开关
- [ ] 工作区详情以目标树为核心，只读展示所选产品工作区内目标的 canonical 上下文（与计算视图区分）
- [ ] 用户可提交 `user-provided` 候选执行事实，形成受限提案 diff（写集仅目标 `02-execution.md` 追加）
- [ ] Service 级契约对齐 R-004 规格包与 CT-001～CT-018：**在隔离 fixture 上**可运行正反测试并留下机器可读证据
- [ ] **生产路径**上的 `decide_and_execute`（或等价）仅在 GOAL-009 的 F-007/F-008 关闭且 I-003/I-004/I-006 `verified` 之后启用；此前测试环境可单独授权
- [ ] 无 AI 调用、无共享资料 CRUD、无跨工作区 N1 列表产品化、无 SQLite 依赖；不把 receipt 写入五件套
- [ ] 发布/安装说明写明：不含本仓过程树；合成 fixture 不使用真实 GOAL-001～011 过程数据当客户样例

## 范围（α）

| 在范围内 | 不在范围内 |
|----------|------------|
| 配置化 `data_root` / workspace 路径 | 总览页、工作区列表（N1 产品化可后续目标） |
| 单工作区详情 + 目标树 | 共享资料 CRUD、AI、工具调用 |
| R-004 对象流与 fixture CT | 生产写入在门禁未满足时启用 |
| 文件旁路 `ops/receipts`（测试/授权环境） | SQLite；本仓 dogfood 默认绑定 |
| 文档与测试证据 | 部署到公网、多用户 |

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 配置键名、默认 fail-closed 行为、DEV_DOGFOOD 开关语义 | 实现启动 | 编码前 | 写入 web README / 配置 schema | open | 无 | 继承 D-011 |
| I-002 | required | CT fixture 目录布局与运行命令 | 契约测试验收 | 首次 CT 合并前 | 按 R-004 规格包落地 | open | 无 | [规格包](../GOAL-009-ai-assisted-governance-workbench/attachments/r-004-executable-contract-spec.md) |
| I-003 | required | 生产写入启用检查清单（F-007/F-008、I-003/I-004/I-006） | 开放生产 `decide_and_execute` | 启用生产写入前 | 对照 GOAL-009 关闭证据 | open | 无 | 门禁未满足则保持关闭 |
| I-004 | non-blocking | 详情页最小 UI 线框与空态/失败态文案 | UX 打磨 | 试点前 | 实现中迭代 | open | 试点复核 | R-001 §4–5 |

## 依赖与门禁

- **规划输入**：GOAL-009 D-006/D-007/D-010/D-011/D-012；R-001/R-004；规格包已接受。
- **硬禁令**：不得在 GOAL-009 F-007/F-008 仍 open 或 I-003/I-004/I-006 未 `verified` 时，对真实用户数据根开放 Web/AI 写入。
- **打包**：实现与文档遵守 D-011 发布物边界。

## 高层实施顺序

1. 配置与数据根 fail-closed（无 dogfood 默认）
2. 只读：配置工作区详情 + 目标树
3. 合成 fixture + service 契约入口骨架
4. CT-001～CT-018 在测试环境落地（可授权写入 fixture）
5. UI：候选 → 提案 diff →（门禁满足后）确认执行
6. 文档：配置、非目标、门禁检查清单

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 规划来源

- [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md)
