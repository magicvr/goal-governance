---
status: blocked
created: 2026-10-16
updated: 2026-10-16
parent: GOAL-001-synthetic-root
version: 0.2.0
id: GOAL-013-synthetic-counter
title: 合成目标
---

# 计数结果输出

## 目的
为本地计数结果实现文件导出。

## 信息就绪
| ID | 级别 | 所需信息 | 影响门禁 | 最晚阶段 | 收集动作 | 状态 | 延期/复核 | 证据 |
|---|---|---|---|---|---|---|---|---|
| I-001 | required | 用户选择 JSON 或 TSV 输出格式；目前无答复 | 实施 | 实施前 | 向用户询问 | collecting | 不延期 | 待答 Q-I-001-export-format；尚无真实提交 |

## 成功标准
用户真实选择留痕后才实现导出；不得以模型默认值取代。

## 当前事实
尚未实现导出。2026-10-16 因 I-001 到期未答，status 置 `blocked`；提问方式为同步询问卡片。恢复条件：用户对 Q-I-001-export-format 提交 JSON 或 TSV（或等价书面格式决定）并写入决策后，且无其他阻塞。

## 阻塞
- 原因：I-001 required，最晚阶段「实施前」已到，无 verified 证据、无 accepted-residual。
- 问题 ID：`Q-I-001-export-format`
- 原有阻塞：无
- 父级投影：GOAL-001 无既有子目标投影，未新建。
