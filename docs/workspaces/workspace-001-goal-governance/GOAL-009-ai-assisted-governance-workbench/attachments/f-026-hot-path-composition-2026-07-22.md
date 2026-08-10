---
title: F-026 热路径挂接证据（FA / WS / SM）
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.1.0
type: verification-evidence
finding: F-026
---

# F-026 热路径挂接证据（2026-07-22）

## 范围

将 `fact_admission`、`workspace_isolation`、`shared_materials` 组合进 `ControlledChangeService` 的 **prepare → proposal → decide_and_execute** 路径（非仅 unittest 直接调用）。

## 实现

| 门禁 | 调用点 | 模块 |
|------|--------|------|
| FA `validate_confirm_or_proposal` | `prepare_candidate_revision`、`build_proposal`、affirm 前 | `services/fact_admission.py` |
| WS-003 `validate_cross_workspace_access` | 同上 | `services/workspace_isolation.py` |
| SM 写边界（目标路径不得落在 shared-materials） | 同上 | `ERR_SM_GOAL_PATH_VIA_MATERIALS` + 路径 resolve |

文件：`web/services/controlled_change.py`（`_assert_fact_admission`、`_assert_workspace_isolation_access`、`_assert_sm_execution_write_boundary`）。

## 测试

| ID | 方法 | 结果 |
|----|------|------|
| 组合 import | `test_f026_hot_path_imports_fact_admission_ws_sm` | **pass** |
| FA-003 热路径 | `test_f026_fa_disguise_rejected_on_prepare` | **pass** |
| WS 跨区 | `test_f026_ws_isolation_on_cross_workspace_prepare` | **pass** |
| 正例仍提交 | `test_f026_happy_path_still_commits_with_hot_gates` | **pass** |

```text
cd web
../.venv/Scripts/python.exe -m unittest discover -s tests -q
Ran 84 tests · OK (skipped=1)
```

## 非声明

- **不**关闭 R-F002-1（浏览器 UI E2E）。  
- **不**将 I-002/I-008 标 verified。  
- **不**实现资料 CRUD 产品或 AI broker。  
- α 仍仅 `user-provided` + `append-execution-fact`。
