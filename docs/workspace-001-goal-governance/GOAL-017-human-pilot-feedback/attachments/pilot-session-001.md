---
title: 试点会话记录 · SESSION-001
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-017-human-pilot-feedback
version: 0.1.0
type: pilot-evidence
session_id: SESSION-001
---

# 试点会话 · SESSION-001

## 元数据

| 字段 | 值 |
|------|-----|
| session_id | SESSION-001 |
| 日期 | 2026-07-22 |
| 操作者 | Grok agent（FastAPI TestClient 路径实跑；非浏览器人手） |
| 与上一条会话的区分 | 本目标首条会话 |
| DATA_ROOT | 临时产品根 `…/pilot017-*`（会话后由 OS 清理；路径形态符合 R-017-A） |
| 焦点 workspace_id | `workspace-001-pilot-a` |
| AI 是否启用 | false |
| 受控写是否启用 | true（`ALLOW_CONTROLLED_WRITE=true`，`PRODUCT_GATES_OPEN=false`） |

## 环境检查（R-017-A §2）

| 检查 | 结果 | 备注 |
|------|------|------|
| DATA_ROOT 产品根 | **pass** | 合成产品根，非 monorepo dogfood 默认可写 |
| 工作区焦点明确 | **pass** | cookie `gg_focus_workspace_id=workspace-001-pilot-a` |
| 写门闩（若测写） | **pass** | 双门闩按上表 |
| AI 配置（若测 AI） | **pass** | `AI_ENABLED=false`，测 fail closed |

## 路径执行（R-017-A §3）

| 步骤 | 做了？ | 结果摘要 | 故障？ |
|------|--------|----------|--------|
| P1 焦点 | **是** | `GET /workspaces` → 200，页面含「工作区」 | 无 |
| P2 目标详情 | **是** | `GET /` → 200 见 Pilot Root / GOAL-001-pilot-a；`GET /goals/GOAL-001-pilot-a` → 200 | 无 |
| P3b 受控追加 | **是** | proposal → digest → decide affirm → 200，响应含成功/committed 类结果 | 无 |
| P4 AI | **是** | `POST …/ai/suggest` → 200，正文含 ERR_AI / disabled 类 fail closed | 无（期望失败） |
| P5 资料 | **是** | `GET /materials` 200；upload 303；attach 303 | 无 |
| 隔离抽查 | **是** | 焦点 A 下 `GET /goals/GOAL-001-pilot-b` → **404** | 无 |

## 故障与摩擦

| ID | 复现步骤 | 期望 | 实际 | 严重度 |
|----|----------|------|------|--------|
| — | （本会话无产品故障） | | | |

## 反馈与改进点

1. TestClient 可完整覆盖 P1–P5 与跨区 404；浏览器人手手感、视觉与多日间隔未覆盖（见 SESSION-002 声明）。  
2. AI 关时 suggest 路径错误信息可被页面/正文捕获，利于 I-012 有界观察。  

## 对照草稿（I-007 / I-012）

| 项 | 观察 |
|----|------|
| 模型/延迟感（I-007） | AI 未启用；无模型调用 |
| AI 关时是否仍可工作（I-012） | **是**：详情、受控写、资料路径可用 |
| 错误信息是否可理解 | AI 禁用路径返回可识别 ERR_AI/disabled 类信息 |

## 声明

本记录仅含本 agent 实跑步骤；操作者为自动化客户端，**不是**人类浏览器多日试点。未粘贴密钥。
