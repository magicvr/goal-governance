---
title: E-α 产品工作区受控追加冒烟证据
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.1.0
type: verification-evidence
decision: D-021
audit: A-041
---

# E-α 受控追加冒烟证据（2026-07-22）

## 范围（D-021）

| 项 | 值 |
|----|-----|
| 数据根 | `data/product-workspace`（合成产品根，**非** dogfood 过程树） |
| 目标 | `GOAL-001-fixture-target` |
| 路径 | 生产受控写：`test_authorized=False`；`ALLOW_CONTROLLED_WRITE=true`；`PRODUCT_GATES_OPEN=false`；`DEV_DOGFOOD=false` |
| 动作 | `append-execution-fact` · user-provided · `decide_and_execute(affirm)` |
| operation_id | `op_e_alpha_smoke_20260722` |

## Health 等价检查

```json
{
  "workspace_configured": true,
  "workspace_source": "GOAL_GOVERNANCE_WORKSPACE_DIR",
  "workspace_path": "…/data/product-workspace",
  "product_gates_open": false,
  "controlled_write_enabled": true,
  "dev_dogfood": false
}
```

## 冒烟结果

| 检查 | 结果 |
|------|------|
| `result` | **committed** |
| 标记写入 `02-execution.md` | **pass**（`E-alpha smoke 2026-07-22: user-provided append via production gate path`） |
| meta digest 不变 | **pass** |
| goal-tree digest 不变 | **pass** |
| receipt 落盘 | **pass** · `data/product-workspace/ops/receipts/op_e_alpha_smoke_20260722.json` |
| 负向：`PRODUCT_GATES_OPEN=true` 时 `production_controlled_write_allowed` 为 false | **pass** |
| 未写 dogfood `docs/workspace-001-goal-governance` | **pass**（配置路径校验） |

### Digest 摘要

| 字段 | 值 |
|------|-----|
| proposal_digest | `sha256:71ab5baf3462c378b96f36b1d08abe00daa20e81485d227b8f295ee3fd6e9104` |
| pre_write_digest | `sha256:0887194ffb325e0ada298c7d939f3310cd0b3902ec1fa7d086b7d1987e8a6b0e` |
| post_write_digest | `sha256:35cc63e21353e537e883238fee44fa48dd8538d6a8dfa9796da66c792d7fb5ec` |

## 回归

冒烟后 `web` unittest：`Ran 80 tests` · **OK (skipped=1)**。

## 非声明

- **不**等于路线图 E 全文退出（缺持续真实使用、全矩阵、阶段关门审）。  
- **不**关闭 residual R-F002/F003/F004/F008。  
- **不**将 I-002/I-008/I-009/I-010 标 `verified`。  
- **不**关闭 F-026（热路径挂接仍 recommended）。  
- 调用方式为 **service 生产路径**（非浏览器 E2E）；HTTP 表单路径未在本拍单独跑。
