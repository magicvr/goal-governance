---
title: GOAL-015 阶段 A · N1 导航范围与元数据白名单冻结
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-015-n1-workspace-navigation
version: 1.0.1
type: design-freeze
accepted_by: D-002
errata: D-007 / A-009 (F-001)
sources:
  - docs/architecture/workspace-protocol.md
  - GOAL-009 R-003 / 验证包 Q1·§3（N1）
  - GOAL-009 D-011 / D-019
  - GOAL-015 D-001
---

# R-015-A · N1 导航范围与元数据白名单（阶段 A）

> 本文件为 GOAL-015 **阶段 A 退出产物**。阶段 B～E 实现不得削弱下列硬边界。  
> 冲突时以 **D-002 + 本文** 为准。上游：`workspace-protocol`、GOAL-009 [R-003 验证包](../../GOAL-009-ai-assisted-governance-workbench/attachments/r-003-verification-package.md) Q1 / §3。

## 1. 范围与非目标

| 在范围内（本目标有界交付） | 不在范围内 |
|---------------------------|------------|
| 实例内工作区 **列表**（仅 N1 白名单字段） | 共享资料列表 / CRUD / AI 读资料（→ X-SM） |
| **选择**当前工作区；详情与受控写绑定选中区 | 跨工作区混合目标/候选/AI 上下文 |
| **有界创建**：新目录 + `workspace.md` + Root 骨架 + 空 `goal-tree`（模板） | 从他区复制过程目标树 / dogfood 过程数据当客户样例 |
| **归档 / 取消归档**：N1 `status` 翻转；**不**删除 canonical | 物理删除工作区目录（本目标禁止） |
| 跨区读写 **fail closed** 正反测 | 多用户账号、角色、协作权限 |
| 平台导航索引（可重建、非权威） | 索引内缓存五件套正文 / progress 权威副本 |
| 与 α 单配置绑定 **兼容**（见 §5） | 默认静默扫描 monorepo 猜「当前工作区」 |
| | GOAL-009 I-009 **整项** `verified`；阶段 6 终态宣称；关 Root |

### 1.1 「创建」裁决（I-005）

**纳入本目标（有界 · service）**：在**产品数据根**下，通过 `WorkspaceRegistryService.create_workspace`（及等价 API/调用方）生成符合 `workspace-protocol` 的最小骨架（`workspace.md`、Root GOAL-001 占位或用户给定 slug、`goal-tree.md`）。阶段 B 已交付该 service 与 unittest。

**Web 表单一键建区**：**不**在本目标有界关门范围内交付；见 residual **R-015-CREATE-UI**（`00-meta` / D-006）。历史措辞「用户可在 Web 发起」易被读成 UI 已交付，以本勘误与 residual 为准（A-008 F-001 / D-007）。

**不纳入**：导入外部仓库全量过程树、跨实例联邦、批量迁移向导；物理删除。

## 2. 硬边界（不可削弱）

1. **一个工作区 ↔ 一个 Root Goal**（`parent: null`）；`workspace.md.root_goal` 必须与磁盘唯一 Root 完整 id 一致。  
2. **canonical_scope** = 该工作区根目录；目标状态仅存在于该根内五件套 + `goal-tree.md`。  
3. **无第二真相源**：平台列表/注册表**不得**成为 status/progress/finding 权威；与 Markdown 冲突时以该区 canonical 为准，索引标 invalid 或重建。  
4. **无跨区混合**：列表、详情、AI、受控写的焦点工作区必须一致；请求他区路径 → 拒绝且不返回他区正文。  
5. **打包 / dogfood**（D-011）：发布物不含本仓过程树；无配置 fail closed；禁止静默 `DEV_DOGFOOD` 以外回落 monorepo。  
6. **受控写**：仍遵守 GOAL-009 A-030 双门闩 + 产品数据根 + R-F008；N1 不降低写门禁。  
7. **单用户**：无账号体系；确认边界仍在人（P-004 不因导航而自动化）。

## 3. 导航元数据白名单（N1）

### 3.1 列表 / API 允许暴露的字段

| 字段 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `workspace_id` | string | `workspace.md` → `id` | 稳定 ID；选择键 |
| `display_name` | string | `workspace.md` → `title`（缺省则 = id） | 人读名 |
| `root_goal` | string | `workspace.md` → `root_goal` | 完整 Root Goal id |
| `status` | enum | 平台注册或 `workspace.md` 扩展 | **仅** `active` \| `archived` |

**可选（实现内部解析，默认可不进列表 JSON）**：

| 字段 | 用途 | 约束 |
|------|------|------|
| `canonical_path` | 解析绑定用绝对/相对路径指针 | **不得**在 UI 展示他区目标正文；日志可截断路径 |
| `updated` | 导航排序用时间戳 | 来自 `workspace.md` frontmatter；非目标 progress |

### 3.2 明确禁止出现在导航列表 / 跨区响应中的内容

| 禁止项 | 原因 |
|--------|------|
| 他区 `goal-tree` 全文或目标标题列表（超出 Root id） | 第二状态 / 泄漏 |
| 任一目标 `00-meta`～`03-audit` 正文、attachments | 隔离 |
| open finding / 审计意见正文 | 隔离 |
| AI 候选、未确认事实、prompt 历史 | 隔离 |
| 共享资料正文、未固定引用的字节 | X-SM / D-004 |
| `status`/`progress` **目标级**权威副本（以索引冒充） | 第二真相源；WS-006 |
| 密钥、`.env`、API key | 安全 |

对照 GOAL-009 验证包：**WS-004**（N1 字段过宽则契约失败）为本目标必测继承项。

## 4. 生命周期最小规则（产品语义；实现在 B–D）

| 动作 | 最小规则 |
|------|----------|
| **定位 / 列表** | 仅**已注册或配置声明**的工作区集合；禁止「扫描整个 git 仓猜默认」。 |
| **选择** | 用户显式选择 `workspace_id` → 设为当前焦点；后续 GET/写仅该 `canonical_scope`。 |
| **创建** | 新产品目录 + 合法 `workspace.md` + 单 Root + 空/最小 goal-tree；新 `workspace_id` 不得与他区冲突。 |
| **归档** | N1 `status=archived`；canonical **保留**；列表默认可隐藏 archived（须可「显示已归档」）。 |
| **取消归档** | `status=active`；不自动改目标 status。 |
| **删除** | **本目标不做**物理删除；若未来需要另立目标。 |

## 5. 当前工作区绑定原则（阶段 C 实现输入）

| 模式 | 规则 |
|------|------|
| **α 兼容** | 若仅配置 `GOAL_GOVERNANCE_WORKSPACE_DIR`（或 DATA_ROOT 单区）且注册表为空/单条 → 行为与 GOAL-012 一致。 |
| **多区** | 注册表（或配置声明的多路径）提供列表；**当前焦点**优先：显式用户选择（session / 安全 cookie / 服务端 session）> 配置默认 id > fail closed（多区未选时拒绝「假装有默认」）。 |
| **校验** | 焦点 `workspace_id` 必须能解析到合法 `workspace.md`，且 `root_goal` / `canonical_scope` 校验通过（继承 WS-001/002）。 |
| **AI** | 若 AI 启用，上下文**仅**当前焦点工作区（GOAL-014 边界不削弱）。 |

**阶段 A 不冻结**具体 cookie 名或 session 库；阶段 C 选定并测 fail closed。

## 6. 平台注册表原则（阶段 B 实现输入）

1. 注册表是**导航索引**：至多 N1 字段 + 可重建路径指针。  
2. 权威仍在各区 `workspace.md` + 五件套；注册表与磁盘冲突 → 拒写 / 标 invalid / 触发重建。  
3. 存放于**产品数据根**侧（非 monorepo dogfood 过程树默认写入）。  
4. 可用 SQLite **仅**作可重建索引（D-011）；**禁止** DB 存目标 status/progress/五件套权威副本。  
5. 具体 schema 与扫描 vs 手写注册 在阶段 B 定稿；不得违反 §2–§3。

## 7. 与 GOAL-009 I-009 对照

| I-009 子问题 | 本冻结 | 仍非 verified |
|--------------|--------|----------------|
| 工作区 ↔ Root / canonical | §2 硬边界 | 产品实现 + 多区发布验收前，GOAL-009 I-009 整项仍 collecting |
| 平台列表/创建/归档 | §1 + §4 有界纳入 | 全文 UX E2E / 人类试点 → R-009-X / X-PILOT |
| 导航元数据例外 | §3 N1 白名单 | — |
| 跨区不可见 | §2.4 + 禁止表 | 运行 CT 在阶段 D |

**本阶段 A 退出 ≠** GOAL-009 I-009 `verified`；**≠** 关闭 R-009-X。

## 8. 阶段 B 入口清单（非本拍交付）

- [ ] 注册表/发现 service 骨架 + 校验  
- [ ] 列表 DTO 严格白名单序列化（WS-004）  
- [ ] 跨区读写拒绝用例骨架  
- [ ] 有界创建骨架（目录 + workspace.md）  

## 9. 版本

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-07-22 | 阶段 A 初冻；D-002 接受 |
| 1.0.1 | 2026-07-22 | §1.1 勘误：有界创建=service；Web 表单 → R-015-CREATE-UI（A-008 F-001 / D-007） |
