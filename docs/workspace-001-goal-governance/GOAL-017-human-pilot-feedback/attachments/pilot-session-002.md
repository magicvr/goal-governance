---
title: 试点会话记录 · SESSION-002
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-017-human-pilot-feedback
version: 0.1.0
type: pilot-evidence
session_id: SESSION-002
---

# 试点会话 · SESSION-002

## 元数据

| 字段 | 值 |
|------|-----|
| session_id | SESSION-002 |
| 日期 | 2026-07-22 |
| 操作者 | Grok agent（**新** TestClient 实例；与 SESSION-001 进程客户端隔离） |
| 与上一条会话的区分 | 新 `TestClient` 进程状态；焦点改为 `workspace-002-pilot-b`；另起无 cookie 客户端测多区未选 |
| DATA_ROOT | 与 SESSION-001 **同一**临时产品根（共享资料库实例级） |
| 焦点 workspace_id | `workspace-002-pilot-b` |
| AI 是否启用 | false |
| 受控写是否启用 | true |

## 环境检查（R-017-A §2）

| 检查 | 结果 | 备注 |
|------|------|------|
| DATA_ROOT 产品根 | **pass** | 同上 |
| 工作区焦点明确 | **pass** | cookie 焦点 B |
| 写门闩 | **pass** | 同上 |
| AI 配置 | **pass** | 仍禁用 |

## 路径执行（R-017-A §3）

| 步骤 | 做了？ | 结果摘要 | 故障？ |
|------|--------|----------|--------|
| P1 焦点 | **是** | 焦点 B；另：无 cookie 客户端 `GET /` → 200，页面含需选择/未配置类引导（多区 fail closed） | 无 |
| P2 目标详情 | **是** | `GET /` 与 `GET /goals/GOAL-001-pilot-b` → 200 | 无 |
| P3b 受控追加 | **是** | proposal → decide affirm → 200 成功路径 | 无 |
| P4 AI | **是** | suggest → 200 fail closed | 无（期望） |
| P5 资料 | **是** | 实例级 materials 列表 count≥1（SESSION-001 上传）；**焦点 B 的 refs count=0**（跨焦点隔离） | 无 |

## 故障与摩擦

| ID | 复现步骤 | 期望 | 实际 | 严重度 |
|----|----------|------|------|--------|
| — | 无产品故障 | | | |

## 反馈与改进点

1. 多区无 cookie 时首页 fail closed 文案存在，利于防误进。  
2. 资料为实例级、引用按焦点隔离：B 看不到 A 的 ref，符合 R-016。  
3. **缺口（有意）**：人手浏览器多日使用手感、可访问性主观评价未收集 → 阶段 C 可列 residual 或 backlog，不伪装已做人感试点全文。  

## 对照草稿（I-007 / I-012）

| 项 | 观察 |
|----|------|
| 模型/延迟感（I-007） | AI 仍关 |
| AI 关时是否仍可工作（I-012） | **是**（详情 + 写 + 资料列表） |
| 错误信息是否可理解 | 多区未选与 AI 禁用均有可观察信号 |

## 声明

与 SESSION-001 为独立 TestClient 会话；操作者仍为 agent，非人类浏览器。未编造未执行步骤。
