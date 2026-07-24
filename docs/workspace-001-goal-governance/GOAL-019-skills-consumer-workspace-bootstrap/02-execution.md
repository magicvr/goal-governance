---
id: GOAL-019-skills-consumer-workspace-bootstrap
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-24
updated: 2026-07-24
version: 0.6.0
---

# 执行记录 · GOAL-019

## 时间线

### 2026-07-24 · 阶段 A / B

见前序：core 镜像、install 默认装 docs、S0/01 scaffold 语义、AGENTS 必备话术、D-003～D-005。

### 2026-07-24 · 阶段 C 实现 + D-006

**D-006**：关闭 I-002——可选 install 工作区脚手架。

| 项 | 变更 |
|----|------|
| `install.sh` | `--init-workspace` + `--workspace-slug` / `--root-slug` / `--root-title` / `--workspace-nnn`；`init_workspace_skeleton` |
| `install.ps1` | `-InitWorkspace` + `-WorkspaceSlug` / `-RootSlug` / …；`Initialize-WorkspaceSkeleton` |
| 行为 | 写 `workspace.md` + `goal-tree.md`；不建 `GOAL-*`；已存在路径 refuse；可单独运行（仍装 core） |
| 文档 | `skills/README.md` 参数表与示例 |
| 测试 | 隔离冒烟带 InitWorkspace；编排器单测断言 flag 存在 |

**验证**

- `test_install_ps1_isolated.ps1` → **PASS**（core + workspace-001-pilot-app skeleton；无 GOAL 五件套）  
- `python -m unittest skills.tests.test_skills_orchestrator` → **33 passed**

**未做**

- standalone-bootstrap 全文（I-005 deferred）  
- 正式 A-00N 阶段审 / 有界关门（阶段 D）

## 待办（按路线图）

1. ~~**A**~~ **完成**  
2. ~~**B**~~ **完成**  
3. ~~**C**~~ **完成**  
4. **D**：阶段审与有界关门  

## 进度评估

**约 90%**：A+B+C 完成；仅关门审计待做。
