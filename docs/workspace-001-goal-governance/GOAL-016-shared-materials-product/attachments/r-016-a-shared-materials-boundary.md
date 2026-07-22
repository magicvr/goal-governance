---
title: GOAL-016 阶段 A · 共享资料产品范围与存储/安全边界冻结
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-016-shared-materials-product
version: 1.0.1
type: design-freeze
accepted_by: D-002
errata: D-007 / A-009 (F-001)
sources:
  - docs/architecture/workspace-protocol.md
  - GOAL-009 D-004 / D-011 / I-010
  - GOAL-009 R-003 验证包 §4～§5.2（SM-001～006）
  - GOAL-014 R-014-A（AI 边界）
  - GOAL-016 D-001
---

# R-016-A · 共享资料产品范围与存储/安全边界（阶段 A）

> 本文件为 GOAL-016 **阶段 A 退出产物**。阶段 B～E 实现不得削弱下列硬边界。  
> 冲突时以 **D-002 + 本文** 为准。上游：workspace-protocol、GOAL-009 [R-003 验证包](../../GOAL-009-ai-assisted-governance-workbench/attachments/r-003-verification-package.md) SM 节、[D-004 产品规则](../../GOAL-009-ai-assisted-governance-workbench/01-decision.md)。

## 1. 范围与非目标

| 在范围内（本目标有界交付） | 不在范围内 |
|---------------------------|------------|
| 实例内**共享资料库**产品存储（字节 + 元数据） | monorepo dogfood `docs/shared-materials/` 过程库存当生产库 |
| 单用户 **Create / List / Read 字节 / Delete**（有引用检查） | 多用户账号、协作 ACL、角色 |
| **MaterialVersion** 不可变版本 + sha256 | 静默改已有 version 的字节却保留同 version |
| 工作区 **MaterialRef** 固定引用（protocol 字段） | 把引用或资料当 canonical 目标状态 |
| 删除前受影响引用检查 + 可追溯历史（最小） | 物理粉碎审计到法证级（可 residual） |
| 跨区隔离：资料 API **不得**读写他区 goal 路径 | 跨**部署实例**共享资料 |
| 与 N1 焦点工作区衔接（引用写入当前焦点区） | 重做 N1 导航（GOAL-015） |
| 正反 unittest（扩展 SM 产品路径） | 浏览器 DOM 全矩阵 E2E（可 residual） |
| | GOAL-009 I-010 **整项** verified；阶段 6 终态；Root 关门 |

### 1.1 AI 读资料裁决（I-004）

| 决策 | 内容 |
|------|------|
| **本目标默认** | 阶段 **B–C** 不交付 AI 自动读资料运行时；焦点为用户 CRUD + 引用 + 隔离。 |
| **阶段 D 可选有界** | 若实现：仅用户触发；当**数据**；**不**执行资料内指令；**不**默认外传；须遵守 GOAL-014 R-014-A 与 D-004。 |
| **若 D 未交付** | 登记 residual **R-016-AI-READ**（复审：宣称 AI 读资料产品前）；**不**阻断用户 CRUD 有界关门。 |

## 2. 硬边界（不可削弱）

1. **无第二真相源**：资料库与索引**不得**保存目标 `status`/`progress`/五件套权威副本；目标状态仅在各工作区 canonical 根。  
2. **固定引用 fail closed**：缺 `material_id` / `version` / 有效 64 位 hex `sha256`，或哈希与存储字节不一致，或 `workspace_id` 不匹配 → **不得**作证据、候选升格输入、跨区上下文。  
3. **资料当数据**：任何 AI/自动化路径不得把资料正文当指令执行，不得默认外传（D-004 / SM-004）。  
4. **隔离**：共享资料 API **禁止**以 goal 相对路径读写他区五件套（SM-006）；工作区彼此仍不可见目标树。  
5. **打包 / dogfood**（D-011）：发布物**不含**本仓过程资料树；产品库在**部署 data_root 旁路**，非 monorepo dogfood 默认。  
6. **受控写门禁不削弱**：向工作区写入 MaterialRef（若写入 workspace.md 或受控记录）仍须遵守 GOAL-009 A-030 双门闩与确认语义；资料字节库本身不是 goal-tree 权威。  
7. **单用户**：无账号体系；删除/覆盖须用户明确动作。

## 3. 存储拓扑（I-001 冻结）

| 项 | 冻结决定 |
|----|----------|
| **产品资料根** | `{DATA_ROOT}/shared-materials/`（与产品工作区并列，**在**配置的 `GOAL_GOVERNANCE_DATA_ROOT` 下） |
| **禁止默认** | 静默使用仓库 `docs/shared-materials/` 作为可写生产库（该路径可为 dogfood/候选库存只读输入，**非**本产品写目标） |
| **字节布局（最小）** | `{materials_root}/objects/{material_id}/{version}/{sha256_prefix}/blob` 或等价不可变路径；实现 B 可微调路径，但须 **version+sha256 定位且不可原地改 blob** |
| **元数据索引** | `{materials_root}/index/` 下可重建 JSON/目录索引；**非**目标状态权威；与 blob 冲突以 blob+重算 sha256 为准 |
| **工作区引用存放（产品实现 · B 选定）** | **权威索引**：`{materials_root}/refs/{workspace_id}.json`（可审计文件；**非**目标五件套、**非** goal-tree 状态）。**不是**默认写入各区 monorepo/焦点 `workspace.md` 引用表。protocol 表升格 / 同步写入 `workspace.md` = 后续扩展（非本有界关门必交）。**禁止**仅用 DB 权威存引用而无可审计文件副本。 |

### 3.1 勘误（A-008 F-001 / D-007 · 2026-07-22）

| 读者易混点 | 现时真相 |
|------------|----------|
| 「固定引用」= 已写入 `workspace.md` 协议表 | **否** · 产品 ref = `shared-materials/refs/*.json` |
| protocol `source` 字段 | 产品有界路径 **省略**（SM-001 最小：material_id/version/sha256）；`source` 升格 = residual / 后续 |
| Web「改版本」/ 对已有 material 上传新版 | **service** `put_bytes(material_id=)` 支持；**Web** 上传表单不传 material_id → 仅新建；Web 追加版本 = **R-016-UX** |

## 4. 数据模型（规范最小 · 实现须覆盖）

| 对象 | 最小字段 | 规则 |
|------|----------|------|
| **Material** | `material_id`、显示名、`created_at`、当前版本指针 | 逻辑资料；id 稳定 |
| **MaterialVersion** | `material_id`、`version`、`sha256`（64 hex）、`byte_size`、`storage_path`、`created_at` | **不可变**；新内容 → 新 version |
| **MaterialRef（产品有界）** | `reference_id`、`workspace_id`、`material_id`、`version`、`sha256`、`purpose`、`local_record`、`status` | SM-001 最小三字段强制；**不**强制 protocol `source`（见 §3.1） |
| **LocalAnnotation**（可选本目标） | 指向固定 `reference_id`（版本固定） | 不得改资料字节；可 residual 后置 |

### 4.1 版本与哈希（I-002 原则冻结；细节 B 可细化）

| 规则 | 说明 |
|------|------|
| 上传/更新 | 计算 sha256（文件字节）；生成新 `version`（建议单调：`v`+递增或 UTC 时间戳+短哈希；B 定稿） |
| 禁止 | 同 `version` 下替换 blob 而不改 version/sha256 |
| 校验 | 读/引用时可选重算；**引用建立时必须**与登记 sha256 一致 |

## 5. 操作契约（产品语义）

| 操作 | 允许 | 必须 | 禁止 |
|------|------|------|------|
| Create（上传） | 是 | 新 Material 或新 Version；登记 sha256 | 无校验写盘 |
| List / 元数据读 | 是 | 仅元数据默认；下载字节显式 | 列表返回他区 goal 正文 |
| Delete | 是 | 删除前枚举受影响 MaterialRef；用户确认；保留历史记录（tombstone 或 history 日志） | 静默抹掉引用痕迹（SM-005） |
| 建立 Ref | 是（当前焦点工作区） | 完整字段 + fail closed | 跨 workspace_id 伪造引用 |
| 经资料 API 读写 goal 路径 | **否** | — | SM-006 |

## 6. 安全与信任

| 主题 | 冻结 |
|------|------|
| 路径 | 拒绝 `..`、符号链接逃逸出 materials_root / data_root |
| 内容 | 当数据；MIME 嗅探可选；**不**执行脚本/宏 |
| AI | 见 §1.1；启用时禁止把资料注入为系统指令而不经用户触发 |
| 密钥 | 资料库不存放 API key；日志不打印完整 sha 以外的密钥类字段 |

## 7. 与既有层关系

| 层 | 关系 |
|----|------|
| `shared_materials.py` SM-001～006 | **保留**为纯校验原语；产品 service **必须调用或等价实现** 这些失败模式 |
| `rebuild_shared_materials_index.py` | 候选库存工具；**不是**产品 CRUD 权威；产品索引独立于 dogfood 脚本 |
| GOAL-015 N1 | 引用操作绑定**当前焦点** `workspace_id`；不重做列表导航 |
| GOAL-012/013 受控写 | 若 Ref 写入 workspace 文件，走受控路径或明确文件事务；不绕过双门闩改 goal status |

## 8. 阶段 B 入口清单（非本拍交付）

- [ ] MaterialsStore service：put/list/get/delete + sha256  
- [ ] Ref store：attach/list/withdraw + SM-001～003  
- [ ] 删除引用检查 SM-005  
- [ ] 路径隔离 SM-006  
- [ ] unittest 合成 fixture（产品 data_root 形态）  

## 9. 版本

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-07-22 | 阶段 A 初冻；D-002 接受 |
| 1.0.1 | 2026-07-22 | §3 引用落点 / `source` / Web 版本勘误（A-008 F-001 / D-007） |
