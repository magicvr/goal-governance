---
id: GOAL-010-core-workspace-shared-materials-protocol
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-28
version: 0.3.0
---

# 执行记录 · GOAL-010

## 时间线

### 2026-07-28 · A0 限定引用落地（D-003 · 不重开本目标）

- 用户确认：方案 A / 范围 A0 / 挂 GOAL-010 / 文档 Q2 / 对话 Q3。
- 协议：`docs/architecture/workspace-protocol.md` → **0.5.0**，§2.6 扩写裸 id 条件、Q1/Q2/Q3、禁止嵌 ws 号；§6.7 对齐。
- 同步：`docs/README.md` **0.10.1**、`directory-layout.md` **0.6.1**、根 `AGENTS.md` **0.9.2**、`skills/AGENTS.template.md` **0.9.2**、install Claude/Copilot 规则摘要、`skills/core/docs` 镜像（protocol / layout / README）、`skills/prompts/00`～`05`。
- **本目标仍 `done / 100%`**；未改 Web 路由/展示（A1/A2 未做）。
- 验证：`python -m unittest docs.tests.test_workspace_protocol skills.tests.test_skills_orchestrator -v` → **42 passed**（含 §2.6 Q2/Q3 与 prompts A0 契约）。

### 2026-07-28 · 交叉引用：协议逻辑一致性修订（不重开本目标）

- Root [GOAL-001 D-016](../GOAL-001-main-vision/01-decision.md#d-016--核心协议逻辑一致性修订finding-闭合--隐式工作区--p-004-扩表2026-07-28) 修订了核心协议，其中与本目标相关的部分包括：  
  - `workspace-protocol` **0.4.0**（纲领串行 / 阶段内并行；legacy 隐式工作区唯一路径；跨区 Goal id；Primary 冲突指针）  
  - principles / AGENTS 与编排器对工作区 fail closed 与 finding 闭合的对齐  
- **本目标保持 `done / 100%`**，不因本次元规则维护重开、不改成功标准勾选、不宣称新的产品门禁关闭。  
- 现行协议以 `docs/architecture/workspace-protocol.md` 与 principles **0.6.0** 为准；本目标 2026-07-20 关门结论仍为当时基线事实。

### 2026-07-20 · 目标立项与协议边界登记

- 用户明确要求创建本目标并完成闭环，目标是将工作区和共享资料区纳入核心文档体系，先完成 Skills 适配。
- 依据 [D-001](01-decision.md#d-001--将工作区与共享资料引用定义为核心协议并由-skills-先适配2026-07-20) 建立五件套、路线图和 I-001～I-005；初始状态为 `active / 0%`。
- 已明确本目标不实现 Web、资料物理存储、用户 CRUD、AI 读取执行或跨工作区导航，也不关闭 GOAL-009 的 F-003/F-004、I-009/I-010。
- 已登记核心协议、Skills 适配和验证所需的 required 信息项；尚未将任何 required 项标为 `verified`。

### 2026-07-20 · 实现、验证与 GOAL-009 协议交接

- 新增 canonical [工作区与共享资料区协议](../../architecture/workspace-protocol.md) 与可复制的 [工作区上下文模板](../../templates/workspace-context.md)。协议将工作区绑定到一个 Root Goal 和 `docs/goals/` canonical 范围；将串行 MVP/后续阶段放在 Root Goal 路线图与子目标中；共享资料只能通过固定的版本/哈希引用进入，并对缺失、范围不匹配和不可固定来源 fail closed。
- 更新核心文档、standalone 启用说明、目录布局、AGENTS 规则和 Skills 入口/原语/宿主规则镜像；`skills/templates/workspace-context.md` 是 canonical 模板的分发镜像，未新增第二真相源。
- 用户手动安装官方 CPython 3.14.6 后，以 `C:\\Users\\magicvr\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe` 重建 `.venv`。新的 `pyvenv.cfg` 指向原生 `win-amd64` 基解释器，`pip check` 和 `fastapi`/`frontmatter`/`jsonschema` 导入均通过。
- 在原生 `.venv` 中执行 `python -m unittest discover -s docs\\tests -v`，8 项 core/standalone/负向引用测试通过；执行 `python -m unittest skills\\tests\\test_skills_orchestrator.py -v`，32 项镜像、工作区语义和宿主表面测试通过；执行 `powershell -NoProfile -ExecutionPolicy Bypass -File .\\skills\\tests\\test_install_ps1_isolated.ps1`，F-018 isolated `-All` 安装 smoke 通过。`web/` 中的 `python -m unittest discover -s tests -v` 也为 20 passed / 1 Windows symlink 权限跳过。
- `scripts` 回归中的 release-evidence 组在 30 项里出现 4 failures / 11 errors；原因是本次对 `skills/install/claude/skills/govern/SKILL.md` 的工作区校验语义改动使 GOAL-008 的历史运行时证据行为源摘要过期。该 fail-closed 检查不能通过更新摘要消除：任何下次发布必须先同步宿主 skill、重新获取真实宿主 `/govern` 运行时证据并生成新的 release evidence。它不是 GOAL-010 的 core/Skills 协议 required 门禁，也不重写历史 `v0.7.0` 发布结论。
- 依据 D-002 将 I-001～I-004 标为 `verified`；I-005 继续 `non-blocking / open`。协议输入和非放行边界已追加至 GOAL-009 的执行记录与 A-008；没有关闭 GOAL-009 的 F-003/F-004、I-009/I-010 或任何 Web 门禁。

## 后续边界

- 物理共享资料存储、用户 CRUD、AI 读取执行、跨工作区导航与 Web 访问/安全模型由 GOAL-009 R-003、I-009/I-010 及后续实现目标承接。
- 本目标关门不构成上述产品能力、Web 写入、试点或部署的验证或放行。

## 进度评估

**100%**：D-001 的 core/Skills 协议范围、I-001～I-004 的 required 门禁、模板/镜像/安装/standalone/语义验证和自审均已形成闭环；I-005 保持下游 `non-blocking / open`。
