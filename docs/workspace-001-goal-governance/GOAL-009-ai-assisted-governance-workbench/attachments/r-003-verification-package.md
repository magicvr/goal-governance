---
title: R-003 · 工作区与共享资料验证包（契约冻结 + WS/SM 负向矩阵）
status: active
created: 2026-07-21
updated: 2026-07-21
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.3.0
type: verification-package
review_state: f-003-f-004-closed-bounded
accepted_by: D-019
ws_sm_executed: 2026-07-21
ws_sm_evidence: ws-sm-evidence-001-006-2026-07-21.md
f003_f004_closed_by: D-020-A
f003_f004_audit: A-038
response_group: R-003
closes_finding: F-003-F-004-bounded
---

# R-003 · 工作区与共享资料验证包

> 响应 [A-001 F-003 / F-004](../03-audit.md#a-001--web-第一阶段产品边界与计划一致性审计2026-07-20)（F-004 经 [A-007](../03-audit.md#a-007--对-a-005a-006-的合并响应共享资料区边界修订2026-07-20) 重定义）关闭要求：  
> **F-003**：工作区 → 独立 Root / canonical 映射、索引边界、跨工作区读写拒绝。  
> **F-004**：共享资料区用户 CRUD、版本/哈希固定引用、AI 读边界、删除历史与跨工作区/安全验证。  
> 本包由 [D-019](../01-decision.md#d-019--冻结-r-003-验证包不关闭-f-003f-0042026-07-21) 接受为路线图 B 设计冻结基线。  
> **不**关闭 F-003/F-004；**不**将 I-009/I-010 标 `verified`；**不**实现共享资料 CRUD 产品；**不**扩展 α 写动作集。

## 1. 范围与非目标

| 在范围内 | 不在范围内 |
|----------|------------|
| 工作区映射、N1 导航、隔离负向（WS） | 多用户 / 跨安装联邦云 |
| 共享资料对象模型、固定引用、SM 负向 | 本仓 dogfood 过程资料打入发布物 |
| F-003 / F-004 关闭条件与证据格式 | 把 GOAL-010/011 输入伪装为产品验证通过 |
| 与 workspace-protocol / D-004 / D-011 对齐 | 浏览器 E2E 全矩阵（可 residual） |
| 与 α 单工作区配置绑定的衔接 | 新 operation_kind；AI 工具接入 |

设计收集稿：[r-003-workspace-shared-materials.md](r-003-workspace-shared-materials.md)（D-011 设计默认）。  
核心协议输入：[docs/architecture/workspace-protocol.md](../../../architecture/workspace-protocol.md)（GOAL-010）。  
冲突时以 **D-019 + 本包** 为准；历史「只读贡献资料」语义以 **D-004 / A-007** 为准（已废弃）。

## 2. 冻结的设计裁决（D-004 / D-011 / D-019）

| # | 主题 | 冻结决定 |
|---|------|----------|
| Q1 | 导航元数据 | **N1**：仅 `workspace_id`、显示名、`root_goal` id、可选 `active\|archived`。禁止他区目标树/正文/finding/候选/AI 草稿/资料正文/progress 权威副本。 |
| Q2 | 资料字节存储 | **方案 A**：部署数据根旁路目录；**不是**从开源仓拷贝 dogfood 过程资料。 |
| Q3 | 打包 / dogfood | 发布物含产品/Skills/模板；**禁止**本仓 GOAL 过程树与本仓共享过程资料；无配置 fail closed；禁止静默回落 monorepo dogfood（除非显式 `DEV_DOGFOOD`）。 |
| Q4 | SQLite | 仅可重建的结构性非 canonical 索引；**禁止** DB 权威保存 status/progress/五件套；与 Markdown 冲突以 Markdown 为准。 |
| Q5 | 共享资料所有权（D-004） | 实例内：用户全权 CRUD；AI 边界内只读；版本+sha256 固定引用；注释指固定版本；删除前引用警示+历史；敏感资料不执行指令、不外传。 |
| Q6 | α 实现边界 | 配置选中的**单一**产品工作区详情 + 受限追加；**不含**列表产品化、资料 CRUD、AI、静默 dogfood 绑定。 |

## 3. 规范数据契约 · 工作区（F-003 / I-009）

### 3.1 核心映射（强制）

| 概念 | 定义 | fail closed 条件 |
|------|------|------------------|
| `workspace_id` | 稳定 ID；= `workspace.md` 的 `id` | 缺失或不匹配 |
| `root_goal` | 唯一 `parent: null` Root 完整 id | 缺失、多 Root、与磁盘不一致 |
| `canonical_scope` | 该工作区目标树与五件套根 | 与实际目录不符；跨区路径 |
| 部署 `data_root` / 配置工作区列表 | 实例内可见工作区集合 | 无配置却读写；静默 dogfood |

### 3.2 平台索引 vs 真相源

1. 索引至多缓存 N1 + 重建用路径指针。  
2. 索引与 `workspace.md` 冲突 → 禁止不确定写入；可降级配置扫描。  
3. 进入详情 → 从该工作区 canonical **重新加载**，不信索引正文缓存。

### 3.3 生命周期（设计冻结；产品实现可后置）

| 动作 | 最小规则 |
|------|----------|
| 创建 | 新目录 + `workspace.md` + Root + goal-tree；不得混入他区 id |
| 归档 | N1 状态 `archived`；不删除 canonical；索引可隐藏 |
| 定位 | 仅配置列表 / 显式 id；禁止「扫描仓库猜默认」 |

## 4. 规范数据契约 · 共享资料（F-004 / I-010）

### 4.1 对象（规范最小字段）

| 对象 | 最小字段 | 说明 |
|------|----------|------|
| **Material** | `material_id`、显示名、`created_at`、当前版本指针 | 逻辑资料 |
| **MaterialVersion** | `material_id`、`version`、`sha256`、`byte_size`、`storage_path`、`created_at` | 不可变版本 |
| **MaterialRef** | `reference_id`、`workspace_id`、`material_id`、`version`、`sha256`、`purpose`、`local_record`、`status` | 工作区内固定引用（对齐 workspace-protocol） |
| **LocalAnnotation** | `annotation_id`、`reference_id`（固定版本）、`body`、`created_at` | 不得改资料字节 |

### 4.2 固定引用规则（fail closed）

引用有效当且仅当：`workspace_id` 匹配 **且** `material_id`+`version`+有效 `sha256` 齐全 **且** 与存储版本一致 **且** 目录非 `none`。  
任一缺失 → 不得作证据、候选升格输入或跨区上下文。

### 4.3 操作契约（设计；实现未交付）

| 操作 | 允许 | 必须 | 禁止 |
|------|------|------|------|
| 用户 Create/Update | 是 | 新版本新 sha256；旧版本可保留历史 | 静默改已有 version 的字节却保留同 version 号 |
| 用户 Delete | 是 | 删除前列出受影响 `MaterialRef`；保留可追溯历史 | 静默抹掉引用痕迹 |
| AI 读取 | 边界内 | 当数据；不执行指令 | 自动外传；当指令执行 |
| 跨工作区 | 仅共享资料根（实例内） | 不得通过资料读写他区 goal 树 | 用资料通道混合他区 AI 上下文 |

## 5. 负向矩阵

> 状态：`planned` = 未执行。执行后改 `pass`/`fail` 并附证据。  
> **当前全部 planned**。核心集未全 pass 前不得关对应 finding。

### 5.1 工作区隔离 · 核心（F-003 关闭最小集）

| ID | 触发 | 预期 | 证据类型 | 关联 | 状态 |
|----|------|------|----------|------|------|
| **WS-001** | `root_goal` 与磁盘唯一 Root 不一致 | fail closed；拒绝对该区写入 | 配置/绑定校验 | I-009、F-003 | **pass** |
| **WS-002** | `canonical_scope` 与实际根不符 / 指向他区路径 | fail closed | 同上 | I-009、F-003 | **pass** |
| **WS-003** | 请求读写**另一**产品工作区目标树/五件套 | 拒绝且**不**返回他区正文 | 正反访问 | I-009、I-006、F-003 | **pass** |
| **WS-004** | N1 列表字段含 progress/finding/候选/资料正文 | 契约失败 / 拒序列化 | 视图契约 | I-009、F-003 | **pass** |
| **WS-005** | 无配置 / 无焦点却默认加载 monorepo dogfood | 拒绝（除非显式 DEV_DOGFOOD） | 配置 | I-009、D-011、F-003 | **pass** |
| **WS-006** | 索引宣称 status=done 与 goal-tree 冲突 | 以 Markdown 为准；索引 invalid | 冲突解析 | I-009、F-003 | **pass** |

### 5.2 共享资料 · 核心（F-004 关闭最小集）

| ID | 触发 | 预期 | 证据类型 | 关联 | 状态 |
|----|------|------|----------|------|------|
| **SM-001** | 引用缺 `material_id` / `version` / `sha256` | 拒绝作为引用/证据 | 校验 | I-010、F-004 | **pass** |
| **SM-002** | `sha256` 与存储字节不一致 | fail closed | 校验 | I-010、F-004 | **pass** |
| **SM-003** | `workspace_id` 与当前工作区不匹配的引用 | 拒绝 | 校验 | I-010、F-004 | **pass** |
| **SM-004** | 资料正文含提示注入，AI 试图执行 | 当数据；不执行、不外传 | 安全策略（可设计级） | I-010、D-004 | **pass** |
| **SM-005** | 删除资料前不检查受影响引用 | 必须阻断或强制警示+确认 | 操作契约 | I-010、F-004 | **pass** |
| **SM-006** | 通过共享资料 API 读写**他区** goal 路径 | 拒绝 | 隔离 | I-010、I-009、F-004 | **pass** |

证据：[ws-sm-evidence-001-006-2026-07-21.md](ws-sm-evidence-001-006-2026-07-21.md) · 实现 `workspace_isolation.py` / `shared_materials.py` · 全量 **80 passed, 1 skipped**。

### 5.3 扩展（建议；有界关闭时可 residual）

| ID | 触发 | 预期 | 关联 | 状态 |
|----|------|------|------|------|
| WS-007 | 发布物内出现本仓 GOAL 过程树 | 发布验收失败 | D-011、SM-008 | planned |
| WS-008 | 多工作区创建/归档产品路径 | 按 §3.3；可后置实现 | I-009 | planned |
| SM-007 | 用户 CRUD 全路径 E2E | 成功路径 + 历史保留 | I-010 | planned |
| SM-008 | 安装包含 dogfood 资料 | 失败 | D-011 | planned |
| SM-009 | AI 读未固定引用的索引条目当事实 | 拒绝升格 | I-010、F-002 | planned |
| SM-010 | SQLite 资料索引与 FS 哈希冲突 | 以字节哈希为准 | D-011 | planned |

### 5.4 证据记录格式（每个 WS/SM）

1. 用例 ID、本包 `version`、运行环境与命令。  
2. 输入（workspace 绑定 / 引用对象 / 请求）摘要。  
3. 预期拒绝码或断言；实际结果。  
4. 证明无越权 canonical 写入或他区泄漏（digest 或响应体检查）。  
5. UI/发布案例可附 fixture 路径。

## 6. Finding / 信息项关闭条件

### 6.1 F-003 关闭

须**同时**：

| # | 条件 | 本拍 |
|---|------|------|
| 1 | 本验证包工作区契约经接受 | **是**（D-019） |
| 2 | **WS-001～WS-006** 全部 pass + 证据 | **是**（2026-07-21） |
| 3 | 关闭声明写入 `03-audit` | **是**（A-038 / D-020-A） |

**F-003 状态：closed（有界）** + R-F003-1～2 accepted。

### 6.2 F-004 关闭

须**同时**：

| # | 条件 | 本拍 |
|---|------|------|
| 1 | 本验证包资料模型与 D-004 规则经接受 | **是**（D-019） |
| 2 | **SM-001～SM-006** 全部 pass + 证据 | **是**（2026-07-21） |
| 3 | 关闭声明写入 `03-audit` | **是**（A-038 / D-020-A） |

**F-004 状态：closed（有界）** + R-F004-1～3 accepted。

### 6.3 I-009 / I-010

| ID | 本包贡献 | verified？ |
|----|----------|------------|
| I-009 | 映射、N1、WS 矩阵 | **否**（仍 collecting） |
| I-010 | 对象模型、引用、SM 矩阵 | **否**（仍 collecting） |

### 6.4 与 α / 生产写

- α 已是**单配置工作区**；跨区拒绝部分可与现有 CT-003 对齐，但 **F-003 全文关闭仍须 WS 矩阵**。  
- 共享资料 **不在** α 功能承诺；F-004 关闭 ≠ 开放资料 CRUD 产品，仍可另立实现目标。  
- D-016 生产写门闩与 F-003/F-004 **独立**（写路径已 α 放行）；本包不改 env。

## 7. 实现前门禁清单（WS/SM 执行前）

- [x] R-003 设计默认已接受（D-011）  
- [x] 本验证包已接受为冻结基线（D-019）  
- [x] WS-001～WS-006 可运行（`workspace_isolation.py`）  
- [x] SM-001～SM-006 可运行（`shared_materials.py`）  
- [x] 证据按 §5.4 落盘（[ws-sm-evidence-001-006-2026-07-21.md](ws-sm-evidence-001-006-2026-07-21.md)）  
- [x] 用户确认路径 A：有界关闭 + residual（D-020-A / A-038）  

## 8. 建议下一拍

1. residual 复审触发时先复审再扩 UI/CRUD/发布。  
2. 需要产品 CRUD / 多区导航时按 P-001 另立实现目标。  
3. 可选：将校验挂入 HTTP/配置解析路径；路线图 E 试点。

## 9. 声明

- 本包 v0.3：**F-003/F-004 closed（有界）** + residual accepted（D-020-A / A-038）。  
- **I-009、I-010 仍 collecting**。  
- **未**实现共享资料 CRUD 产品；**未**修改生产 env；**未**接入 AI。  
- 旧「只读贡献资料」关闭要求已由 A-007/D-004 限定，不得用于关闭 F-004。
