---
status: blocked
created: 2026-10-17
updated: 2026-10-17
parent: GOAL-001-synthetic-root
version: 0.1.0
id: GOAL-013-synthetic-counter
title: 合成目标
---

# 计数结果输出

## 目的
为本地计数结果实现文件导出。

## 信息就绪
| ID | 级别 | 所需信息 | 影响门禁 | 最晚阶段 | 收集动作 | 状态 | 延期/复核 | 证据 |
|---|---|---|---|---|---|---|---|---|
| I-001 | required | 用户选择 JSON 或 TSV 输出格式；目前无答复 | 实施 | 实施前 | 向用户询问（Q-I-001-export-format） | collecting | 不延期；待用户书面答复 | 无；见 E-001 |

## 阻塞
`blocked`：等待 `Q-I-001-export-format` 真实答复。恢复条件见 `02-execution/E-001-awaiting-export-format.md`。

## 成功标准
用户真实选择留痕后才实现导出；不得以模型默认值取代。

## 当前事实
尚未实现导出。未收到格式选择。
