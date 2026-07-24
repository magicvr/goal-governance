---
id: GOAL-019-skills-consumer-workspace-bootstrap
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-24
updated: 2026-07-24
version: 0.5.0
---

# 执行记录 · GOAL-019

## 时间线

### 2026-07-24 · 目标立项 / D-003 / D-004 / 阶段 A

见前序：core 镜像、install 默认装 docs、pack 校验、README 最小可运行集。

### 2026-07-24 · 阶段 B 实现 + D-005

**D-005**：关闭 I-003——工作区/Root slug **必须用户确认**，禁止静默默认。

| 项 | 变更 |
|----|------|
| 编排器 | `skills/prompts/00-govern-orchestrator.md` v0.7.0：core 完整性检查；S0 强制 scaffold 顺序；architecture 必备话术 |
| 原语 01 | `skills/prompts/01-create-new-goal.md` v0.5.0：步骤 0 工作区骨架；模板优先 `docs/templates` |
| AGENTS | `skills/AGENTS.template.md` v0.9.0 → install/claude + copilot-instructions；根 `AGENTS.md` 对齐必备表述 |
| 宿主 wrapper | claude/grok govern SKILL、copilot `govern.md`；同步 `.claude`/`.grok`/`.github` |
| 测试 | `test_portability_skills_pkg_and_required_architecture`；编排器断言 S0 scaffold |

**验证**：`python -m unittest skills.tests.test_skills_orchestrator` → **33 passed**。

**未做**

- `--init-workspace`（阶段 C）  
- standalone-bootstrap 全文（I-005 deferred）  
- 正式 A-00N 阶段审（阶段 D）

## 待办（按路线图）

1. ~~**A**~~ **完成**  
2. ~~**B**~~ **完成**  
3. **C**：可选 `--init-workspace`  
4. **D**：阶段审与有界关门  

## 进度评估

**约 70%**：A+B 完成；C/D 待做。
