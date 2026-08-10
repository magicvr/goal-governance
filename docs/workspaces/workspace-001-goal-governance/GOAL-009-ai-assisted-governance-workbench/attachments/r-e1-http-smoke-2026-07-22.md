---
title: R-E-1 HTTP 表单受控追加冒烟证据
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.1.0
type: verification-evidence
residual: R-E-1
---

# R-E-1 HTTP 表单受控追加冒烟（2026-07-22）

## 范围

| 项 | 值 |
|----|-----|
| 路径 | FastAPI **HTTP 表单**：`POST /goals/{id}/proposal` → `POST /goals/{id}/decide` |
| 客户端 | `fastapi.testclient.TestClient`（非 Selenium 浏览器 E2E） |
| 数据根（产品冒烟） | `data/product-workspace` |
| 门禁 | `ALLOW_CONTROLLED_WRITE=true`；`PRODUCT_GATES_OPEN=false`；`TEST_WRITE_MODE=false`；`test_authorized=False` |
| 目标 | `GOAL-001-fixture-target` |

## 产品根冒烟结果

| 检查 | 结果 |
|------|------|
| `GET /api/health` | configured · write enabled · dogfood false · gates closed |
| `GET /goals/...` | 200 · 表单页 |
| `POST .../proposal` | 200 · HTML 含 `proposal_digest` |
| `POST .../decide` affirm | 200 · **committed** |
| 标记写入 `02-execution.md` | **pass**（`R-E-1 HTTP smoke 2026-07-22: form proposal+decide on product workspace`） |
| meta / goal-tree | 字节不变 |
| receipt | `ops/receipts/op_ed694c6922dd.json` · `result=committed` |
| 负向 health | `PRODUCT_GATES_OPEN=true` → `controlled_write_enabled=false` |

### Digest

| 字段 | 值 |
|------|-----|
| proposal_digest | `sha256:0e079541e616c0784b2acdcb62a166eef44b207ca6a6cf10c6e7596fea2e40f7` |
| operation_id | `op_ed694c6922dd` |

## 可重复单元测试

| 测试 | 结果 |
|------|------|
| `test_r_e1_http_form_commit_when_write_authorized` | **pass**（temp fixture + ALLOW 生产路径） |
| `test_decide_http_rejects_when_product_gates_open` | **pass**（门禁阻断） |

```text
cd web && ../.venv/Scripts/python.exe -m unittest discover -s tests -q
Ran 85 tests · OK (skipped=1)
```

## 关闭 R-E-1

本证据关闭 residual **R-E-1**（HTTP/表单受控追加路径）。  
**不**等于全浏览器 DOM E2E、多会话试点（仍属 **R-E-2**）或 GOAL-009 关门（**R-E-3**）。
