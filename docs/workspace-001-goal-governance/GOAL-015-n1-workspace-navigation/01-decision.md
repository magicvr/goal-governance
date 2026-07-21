---
id: GOAL-015-n1-workspace-navigation
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.1
---

# 决策记录 · GOAL-015

## D-001 · 立项：X-NAV N1 多工作区导航（2026-07-22）

**状态**：accepted

**确认来源**：用户在 GOAL-009 D-033 / A-059 后选择 **E1**：`OK E1：创建 X-NAV（GOAL-015 N1 多工作区导航）`。

**决定**：

1. 创建本目标 `GOAL-015-n1-workspace-navigation`：  
   - `parent: GOAL-001-main-vision`  
   - `planning_source: GOAL-009-ai-assisted-governance-workbench`  
   - `expansion_code: X-NAV`  
   - `residual_source: R-009-X`  
2. 范围 = **有界 N1 导航**：列表 / 选择 / 归档（及阶段 A 裁决是否含「创建」）+ 跨区隔离正反测。  
3. **非目标**：共享资料 CRUD（X-SM）、人类多会话试点全文（X-PILOT）、部署硬化（X-DEPLOY）、I-009 全文 verified、阶段 6 终态宣称。  
4. 必须遵守：canonical 真相源仍在各工作区根；平台列表仅导航元数据；不自动 P-004 / 关门 / 混上下文。  
5. 高层路线图 A–E 已写入 `00-meta`；**阶段 A 未冻结前**不宣称多区产品可用。  
6. GOAL-009 保持 `done / 100%` 有界；**R-009-X 仍 accepted**（本立项消耗其子范围「N1 产品」的交付槽，不自动关闭 residual 全文）。

**为什么**：α 仅配置绑单区；多工作区是已定产品模型（GOAL-009 I-009 / F-003 有界）；E1 优先补最大 UX/产品表面缺口。

**未选方案**：

- E2 先 X-SM：资料产品更大，且隔离验收受益于可切换工作区。  
- E3 仅试点：不交付导航能力。  
- E5 同时 NAV+SM：本拍控制并行面。  
- 在 GOAL-009 内直接改代码不立项：违背规划/实现分离。

**影响与后续**：五件套 + goal-tree；下一步 `/govern 推进 GOAL-015 阶段 A：冻结 N1 导航范围与元数据白名单`。

## D-002 · 冻结阶段 A：N1 导航范围与元数据白名单（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-015 阶段 A：冻结 N1 导航范围与元数据白名`。

**决定**：

1. 接受 [attachments/r-015-a-n1-navigation-boundary.md](attachments/r-015-a-n1-navigation-boundary.md)（**R-015-A v1.0**）为阶段 A 权威冻结基线。  
2. 冻结内容包括：  
   - 范围/非目标（含 **有界创建** 纳入；X-SM / 物理删除 / 终态宣称排除）  
   - 硬边界（Root 绑定、无第二真相源、跨区隔离、dogfood、写门禁）  
   - **N1 白名单**：`workspace_id`、`display_name`、`root_goal`、`status`（active|archived）  
   - 禁止表（他区正文/finding/候选/资料/目标 progress 权威副本等）  
   - 生命周期最小语义；当前焦点绑定原则；注册表非权威原则  
3. **继承** `workspace-protocol` 与 GOAL-009 R-003 验证包 Q1 / WS-001～006 意图，不削弱 α 双门闩。  
4. 阶段 A **退出**；路线图 A → **完成**；成功标准第 1 条勾选；progress **15%**。  
5. I-001 → **verified（边界）**；I-005 / I-006 → **closed**（创建纳入；资料入口非目标）。  
6. I-002 / I-003 原则已写于 R-015-A，整项仍 open 至 B/C 实现。  
7. **不**实现列表/注册表代码；**不** verified GOAL-009 I-009 全文；**不**关 R-009-X。

**为什么**：范围与白名单先于 service，避免导航泄漏他区状态或做成第二真相源。

**未选方案**：阶段 A 并行写 UI；列表暴露目标树摘要；默认扫描 monorepo 猜工作区；本目标做物理删除。

**影响**：A-002；goal-tree progress；下一步阶段 B（注册/发现 + 隔离契约）。

## D-003 · 完成阶段 B：注册/发现与隔离契约 service（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-015 阶段 B：工作区注册/发现与隔离契约（service）`。

**决定**：

1. 实现 `web/services/workspace_registry.py`（**WorkspaceRegistryService**）：  
   - 仅在**产品 data_root** 下发现/注册工作区（禁止扫 monorepo 猜默认）  
   - 导航索引：`workspaces/registry.json`（schema `n1-workspace-registry/v1`；非目标状态权威）  
   - **list_n1**：严格四字段白名单（WS-004）  
   - **get / resolve_path / register_existing / set_status（归档）/ create_workspace（有界骨架）**  
   - 加载时校验 Root / scope（WS-001/002）；跨区访问 `assert_workspace_access`（WS-003）  
2. 测试：`web/tests/test_workspace_registry.py`；全量 `unittest discover` → **114 passed, 1 skipped**。  
3. 阶段 B **退出**；progress **40%**；I-002 → **verified（service）**。  
4. **不**实现 Web 列表/选择 UI（阶段 C）；**不** verified GOAL-009 I-009 全文；**不**关 R-009-X。

**为什么**：R-015-A 要求先可测 service，再 UI；索引与 canonical 分离避免第二真相源。

**未选**：阶段 B 绑 HTTP；默认扫描 git 仓；物理删除；DB 存五件套权威。

**影响**：A-003；goal-tree；下一步阶段 C。

## D-004 · 完成阶段 C：Web 列表/选择与焦点绑定（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-015 阶段 C：Web 列表/选择 UI 与当前工作区绑`。

**决定**：

1. 实现请求级焦点绑定 `web/services/workspace_binding.py`（R-015-A §5）：  
   - 多区：`gg_focus_workspace_id` cookie 或 `?workspace_id=` → 校验后绑定路径  
   - 单区 DATA_ROOT：自动焦点  
   - 多区未选：**fail closed**（不猜测）  
   - 无 DATA_ROOT：回退 α `WORKSPACE_DIR` / `from_config`  
2. HTTP/UI：  
   - `GET /workspaces` 列表页（仅 N1 字段）  
   - `POST /workspaces/select` 设 cookie → 首页  
   - `GET /api/workspaces` JSON N1  
   - 主导航「工作区」；首页显示焦点 id  
   - `get_goals_repository(request)` 按焦点解析，详情/写路径跟随  
3. 测试：binding + main 多区 select；全量 **120 passed, 1 skipped**。  
4. 阶段 C **退出**；progress **65%**；I-003 → **verified（Web 绑定）**。  
5. **不**做归档完整 UX（阶段 D）；**不** verified GOAL-009 I-009 全文。

**为什么**：B 已有 service；C 交付可切换的产品表面且保持隔离。

**未选**：默认猜第一个工作区；列表展示目标树/正文；本拍归档表单。

**影响**：A-004；goal-tree；下一步阶段 D。

## D-005 · 完成阶段 D：归档 UX 与跨区负向矩阵（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-015 阶段 D：归档 UX 与跨区负向矩阵`。

**决定**：

1. **归档 UX**（不物理删除）：  
   - `POST /workspaces/status` · `status=archived|active`  
   - `/workspaces` 分栏：active 可选择/归档；archived 可取消归档  
   - 归档当前焦点时 **清除** `gg_focus_workspace_id` cookie  
   - 已归档不可 `select`（400）  
2. **跨区负向矩阵**（可核对）：  
   - HTTP：焦点 A 访问 B 的 goal id → **404**，响应**不含**他区正文标记  
   - service：`assert_workspace_access` 正反矩阵  
   - API：`/api/workspaces` 严格 N1 四字段；`include_archived` 可选  
3. 测试：`web/tests/test_workspace_stage_d.py`；全量 **126 passed, 1 skipped**。  
4. 阶段 D **退出**；progress **85%**；I-004 → **verified（负向矩阵）**。  
5. **不**做物理删除；**不** verified GOAL-009 I-009 全文；下一步阶段 E 关门审。

**为什么**：R-015-A 要求归档保留 canonical；跨区失败必须可测且不泄漏正文。

**未选**：物理删除；归档后仍可 select；列表展示目标树。

**影响**：A-005；goal-tree；阶段 E。

## D-006 · 有界关门 GOAL-015（X-NAV）（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-015 阶段 E：阶段审计与有界关门`。

**决定**：

1. 执行有界 close-out（A-006 阶段审 + A-007 关门）：关闭范围 = **N1 导航有界交付**（白名单、registry、焦点绑定、列表/选择/归档 UX、跨区负向矩阵、回归绿）。  
2. GOAL-015 → `status: done` · `progress: 100%`。  
3. **接受 residual**（P-005）：

| ID | 残余 | 复审触发 |
|----|------|----------|
| **R-015-E2E** | 浏览器 DOM 全矩阵 / 人类多会话导航试点 | 宣称 UI 全矩阵或试点放行前 |
| **R-015-CREATE-UI** | Web 表单新建工作区（service 已有） | 产品要求浏览器内一键建区前 |

4. **不**因本条：GOAL-009 I-009 整项 verified；关 R-009-X 全文；Root done；阶段 6 终态；物理删除；X-SM。  
5. 有界创建以 **service** `create_workspace` 为交付；Web 建区表单显式 residual。

**为什么**：A–D 证据齐且复跑 126 绿；剩余为体验全矩阵与可选建区 UI，不阻断 N1 有界产品表面。

**未选**：无 residual 全文关；把 I-009 标 verified；物理删除。

**影响**：goal-tree；A-006/A-007；Root 子目标指向。

## D-007 · 响应 A-008：关闭 F-001～F-003（文档对齐，不重开）（2026-07-22）

**状态**：accepted

**确认来源**：用户 `响应 GOAL-015 A-008：关闭推荐项 F-001～F-003（文档对齐，不重开）`。

**决定**：

1. **关闭 F-001**：勘误 [R-015-A §1.1](attachments/r-015-a-n1-navigation-boundary.md) — 有界创建 = **service** `create_workspace`；Web 表单明确 **R-015-CREATE-UI residual**（v1.0.1）。  
2. **关闭 F-002**：`00-meta` 信息就绪改为完整 P-005 字段 + 证据指针（I-001～I-006）。  
3. **关闭 F-003**：`goal-tree.md` 编号规则速查「当前下一个」→ **GOAL-016**。  
4. GOAL-015 **保持** `done / 100%`；**不**重开；**不**改 residual 接受范围（R-015-E2E / CREATE-UI 仍 accepted）。

**为什么**：A-008 independent **pass（有界）**；三项均为 recommended 文档卫生，关闭不改变交付边界。

**影响**：A-009；R-015-A v1.0.1；goal-tree v0.74.0 日志。
