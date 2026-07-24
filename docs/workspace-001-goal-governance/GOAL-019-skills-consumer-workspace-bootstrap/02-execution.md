---
id: GOAL-019-skills-consumer-workspace-bootstrap
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-24
updated: 2026-07-24
version: 0.4.0
---

# 执行记录 · GOAL-019

## 时间线

### 2026-07-24 · 目标立项

- 用户确认开 **GOAL-019**；D-001/D-002；同步 `goal-tree.md`。

### 2026-07-24 · D-003 / D-004

- D-003：核心与 Skills 同级必备；zip 内嵌 core + install 默认安装。  
- D-004：关闭 I-004 清单（principles + workspace-protocol + overview/layout + templates + 精简 README；不装 tech-stack）。

### 2026-07-24 · 阶段 A 实现

**交付物（路径）**

| 项 | 路径 / 行为 |
|----|-------------|
| Core 镜像 | `skills/core/README.md`、`skills/core/docs/**`（architecture 四文件 + templates + 精简 README） |
| install.sh | `install_core_docs`：任意宿主安装后默认 `core/docs` → `./docs/`；Next steps 引导 workspace |
| install.ps1 | `Install-CoreDocs`：同上；**去掉** legacy `docs\goals\` Next steps |
| pack | `scripts/pack_skills_release.py` required 含 D-004 文件；拒绝 `tech-stack.md` |
| 文档 | `skills/README.md` v1.4.0：最小可运行集、core 同级必备、目录树含 `core/` |
| 测试 | `test_core_d004_mirror_is_complete`；pack 单测含 core；`test_install_ps1_isolated.ps1` 断言 docs 落点 |

**验证**

- `python -m unittest scripts.tests.test_pack_skills_release skills.tests.test_skills_orchestrator` → **39 passed**（含 Windows 隔离 install 冒烟）。  
- 隔离 install 断言：`docs/architecture/principles.md` 等存在；**无** `tech-stack.md`。

**未做（后续阶段）**

- S0 / `01` 空仓 scaffold 语义（B）  
- AGENTS.template「architecture 可选」话术清理（B）  
- `--init-workspace`（C）  
- monorepo `docs/standalone-bootstrap.md` 全文与 D-003 对齐（I-005 deferred）

## 待办（按路线图）

1. ~~**A**~~ **完成**  
2. **B**：S0 + `01` scaffold；AGENTS/prompts 话术  
3. **C**：可选 `--init-workspace`  
4. **D**：阶段审与有界关门  

## 进度评估

**约 45%**：阶段 A 实现与结构验证完成；B/C/D 未做。
