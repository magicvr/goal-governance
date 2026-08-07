---
id: GOAL-006-consumer-surface-convergence
title: 消费面路径收敛（F-006 承接 + R-001 扫尾）
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-08
updated: 2026-08-08
version: 0.4.0
progress: 100%
---

# GOAL-006 · 消费面路径收敛（F-006 承接 + R-001 扫尾）

## 概述

将 `skills/AGENTS.template.md` 与四治理 prompts（00/05/06/07）中硬编码的 `docs/…` 路径相对化为 `{governance_root}` 语义（或安装时按 pin 展开），使 `governance_root≠docs` 的 File 消费仓不再依赖 AI 自觉读 alignment 定义句而误读路径；与 R-001 裸路径扫尾（overview/directory-layout/docs-README）合并跟踪。

承接来源：[workspace-003] GOAL-001 Root A-012 F-006（independent）、A-013 登记、2026-08-08 跨区移交并入 VP-002 消费面承接路线图（见 `docs/vision/plans/VP-002-…md`）；R-001 由 [workspace-003] A-009/A-010 留痕归本波次。

## 成功标准（暂定，可验证）

1. `skills/AGENTS.template.md` 与四治理 prompts 无裸 `docs/…` 硬编码（全部经 `{governance_root}` 语义或安装 pin 展开）
2. 消费仓安装/展开链路（install 脚本、薄壳、pin 展开逻辑，如适用）与相对化方案一致；`governance_root≠docs` 场景有测试覆盖
3. 全量测试绿 + stage `--check` 0 漂移（§8c 镜像同步）
4. 既有已安装消费仓不回滚、不破坏（兼容面）
5. F-006（workspace-003 台账）与 R-001 扫尾登记项关闭留痕

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 说明 |
|------|------|------|------|
| **S1** | 盘点与方案冻结 | **完成**（2026-08-08） | E-002 影响面清单（14 文件约 240 处 `docs/`）；D-001 冻结 **A+C 混合**（prompts/薄壳/canonical 字面 `{governance_root}`；模板路径并入 `{{GOVERNANCE_ROOT}}` 占位）；I-001 closed |
| **S2** | 实施 | **完成**（2026-08-08） | E-004：prompts/模板/薄壳/安装形态/canonical 相对化（≈390 处引用）；防再犯测试 5 条；12 宿主矩阵证据重捕获 + matrix cells 刷新；239 测试绿 + stage 0 漂移 |
| **S3** | 回归与审计 | **完成**（2026-08-08） | A-001 self pass + A-002 independent（grok build / grok-4.5）pass；A-003 合并响应（F-001/F-002/F-004 fixed、F-003 deferred）；I-002 closed；F-006/R-001 关闭留痕；**GOAL-006 done** |

同一阶段内可并行；阶段间通常串行。

## 派生进度展示

`progress: 100%` = 路线图检查点 S1～S3 已完成 **3 / 3**（等权）。progress **仅展示**，不放行阶段、不关闭 finding、不推导 `done`（关门依据为 A-001/A-002/A-003 证据链）。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | `{governance_root}` 占位符在安装展开链路中的处理方式：纯文档语义（消费方 AI 解释）vs 安装时按 pin 替换 | S1 方案冻结 | S1 方案 | 盘点 install 脚本/薄壳/消费仓展开逻辑 + 对照 alignment 定义句 | **closed**（2026-08-08） | — | E-002 盘点 + D-001（A+C 混合；无机器展开） |
| I-002 | non-blocking | 相对化对已发布 zip / 已安装消费仓的兼容面影响（不回滚、不破坏） | S3 验收 | S3 | 对照已发布资产清单与消费方样例 | **closed**（2026-08-08） | — | A-001/A-002 验收：无 zip 重打包、install 物理路径保留、`{governance_root}` 默认 docs 语义等价 |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)（R3 纲领阶段内子目标）

## 台账布局

本目标为三个可追加台账创建同名平铺目录：`01-decision/`、`02-execution/`、`03-audit/`；索引文件保留 frontmatter、摘要和条目索引；独立记录使用 `D-NNN-*`、`E-NNN-*`、`A-NNN-*` 文件。

## 备注

- 2026-08-08 用户 `/govern` 确认立项参数包（slug `consumer-surface-convergence`、标题、成功标准、路线图 S1/S2/S3、I-001/I-002、初始 active 0%）。
- 跨区来源引用使用 Q2 路径（`docs/workspace-003-mcp-file-dual-channel/…`）；对话中为 `[workspace-003] GOAL-001`。
