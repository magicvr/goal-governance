---
title: 工作区与共享资料区协议
status: active
created: 2026-07-20
updated: 2026-07-28
parent: null
version: 0.3.0
---

# 工作区与共享资料区协议

本协议定义核心文档、Skills 和后续消费适配器共同使用的工作区边界。它保留目标五件套和目标平铺，但不再以全局 `docs/goals/` 作为当前 canonical 布局：每个显式工作区在自己的根目录内保存唯一目标状态。

仓库级愿景体系见 [../vision/](../vision/)：Charter → 愿景规划（VP）→ 工作区/Root 三层对齐；愿景**不是**第二套 goal-tree 或 progress 权威。规则细节以 [../vision/alignment.md](../vision/alignment.md) 为准。

## 1. 范围与术语

| 术语 | 含义 | 不是 |
|------|------|------|
| **工作区根** | `docs/workspace-<NNN>-<slug>/`，其中包含 `workspace.md`、`goal-tree.md` 与平铺的 `GOAL-*`。 | `parent` 层级、页面缓存、审计 `scope` 或第二套目标状态。 |
| **工作区上下文文档** | 工作区根内的 `workspace.md`，从 [workspace-context.md](../templates/workspace-context.md) 复制。 | 每个目标重复保存的元数据，或全局工作区注册表。 |
| **legacy 隐式单工作区** | 外部旧仓库没有显式工作区根、但保留 `docs/goals/` 与唯一 Root Goal 时的兼容模式。 | 多工作区发现、共享资料访问或跨目录自动搜索许可。 |
| **共享资料目录** | 位于工作区根之外的资料集合；当前项目为 `docs/shared-materials/`。 | 目标树、目标状态库或任一工作区可写的隐式公共区。 |
| **共享资料候选库存** | 重建脚本生成的路径、大小和 SHA-256 清单。 | 固定资料引用、canonical 事实、证据或用户确认。 |
| **共享资料引用** | 工作区内指向资料 ID、来源、版本和哈希的可追溯记录。 | 已确认事实、可执行指令或其他工作区的上下文通道。 |
| **愿景 Charter** | `docs/vision/charter.md`：仓库级目的与边界；可演进；status 仅 `active` \| `superseded`。 | Goal；不可使用 Goal 的 `done`。 |
| **愿景规划 VP** | `docs/vision/plans/VP-*.md`：可 planned/active/closed/abandoned 的纲领规划；对齐 Charter。 | 目标五件套；progress% 权威；第二套审计台账。 |

每个工作区根内的 `goal-tree.md` 与 `GOAL-*` 五件套只承载该工作区的目标生命周期状态。共享资料候选库存或导航索引不能形成第二套状态；资料内容必须按事实准入和用户确认规则处理，不能仅因可读取而成为事实或关闭证据。

## 2. 工作区不变量

1. 一个工作区恰好绑定一个 `parent: null` 的 Root Goal；`workspace.md` 的 `root_goal` 必须与该 Root Goal 完整 ID 一致。
2. `canonical_scope` 必须等于包含该 `workspace.md` 的工作区根，例如 `docs/workspace-001-goal-governance/`。该目录直接平铺 `GOAL-*` 与 `goal-tree.md`；层级只由 `parent` 字段表达。
3. 工作区之间不得混合目标、候选、草稿、审计意见、写入请求或 AI 上下文。多个工作区而没有明确焦点时，Skills 和消费适配器必须 fail closed，而非猜测默认工作区。
4. 平台或宿主可以提供导航，但导航缓存不能成为 canonical 目标状态；跨工作区导航字段、运行时授权和用户操作仍属于消费适配器/产品门禁。
5. 工作区上下文改变 Root Goal 绑定、canonical 范围或共享资料目录指针时，属于治理变更：必须有可追溯决定，并在受影响目标的执行记录中留下事实。

## 3. Root Goal 与串行阶段

Root Goal 表达稳定目的、初始边界和高层路线图，不要求在立项时穷尽所有未来阶段。MVP、后续阶段和扩展工作应更新该 Root Goal 的路线图并创建串行子目标；只有长期目的、成功边界或战略方向确实改变时，才记录决定后修改 Root Goal 定义。不得用工作区目录嵌套代替目标 `parent` 关系。

## 4. 工作区上下文文档

新建显式工作区时，从 `docs/templates/workspace-context.md` 复制为 `docs/workspace-<NNN>-<slug>/workspace.md`。frontmatter 的最小字段为：

| 字段 | 要求 |
|------|------|
| `id` | 工作区稳定标识；资料引用的 `workspace_id` 必须相同。 |
| `root_goal` | 当前工作区 Root Goal 的完整 ID，且该目标 `parent: null`。 |
| `canonical_scope` | 当前工作区根；格式为 `docs/workspace-<NNN>-<slug>/`。 |
| `shared_materials_catalog` | 共享资料目录的固定路径/URI，或 `none`。它只标识资料来源，不保存资料内容。 |
| `status`、`created`、`updated`、`version` | 与其他 core Markdown 一致的可追溯元信息。 |
| `vision_role` | `primary` \| `delivery` \| `sandbox`（仓库已安装 `docs/vision/` 时必填）。 |
| `plan_refs` | 对齐的愿景规划 id 列表（逗号分隔）。非 sandbox opt-out 时至少一项。 |
| `primary_plan` | 当前焦点 VP；必须出现在 `plan_refs` 中；对应 `docs/vision/plans/<id>.md`。 |

若 `shared_materials_catalog: none`，工作区不得声明共享资料引用。对于旧仓库，只有没有显式工作区根且存在 `docs/goals/` 时才可作为 legacy 隐式单工作区处理；不得把该兼容路径复制到已迁移仓库中。

### 4b. 愿景对齐（三层链）

1. **Charter ← VP ← Workspace/Root**：Root 与工作区通过对齐 `plan_refs` / `primary_plan` 挂接 VP；VP 通过 `vision_ref: {vision_id}@{version}` 精确对齐 Charter。
2. **Fail closed**：缺 plan 字段、`primary_plan` 无法解析、VP `vision_ref` 与 charter 版本不一致、或 Charter/VP 使用非法 status 时，不得推进受影响的新建/放行/关门。
3. **Opt-out**：仅 `vision_role: sandbox` 可在留痕后省略 `plan_refs`；`primary` 禁止 opt-out。
4. **规划与工作区非 1:1**：一 VP 可由 0..N 个工作区推进（`planned` 允许 0）；一工作区可挂 1..N 个 VP，但必须标明 `primary_plan`。
5. **VP 关门**：轻量纲领确认 + 链接工作区证据；允许有界 closed（residual 点名到区/目标）；禁止把 progress% 或审计台账放进 `docs/vision/`。
6. 完整规则见 [../vision/alignment.md](../vision/alignment.md)；消费方勾选见 [../vision/consumer-checklist.md](../vision/consumer-checklist.md)。

## 5. 共享资料候选库存与固定引用

用户可手工把文件复制到资料目录。运行 `python scripts/rebuild_shared_materials_index.py` 后，`index.json` 只会记录相对路径、字节数和 SHA-256，并以确定性排序、原子替换写入。该清单有以下边界：

1. 它不自动分配业务 `material_id`、版本、用途、工作区归属或资料确认状态。
2. 它不读取、执行、外传或解释资料内容；索引脚本拒绝符号链接和目录逃逸。
3. 它不替代用户确认、P-004 裁决、P-005 信息门禁或任何 finding 关闭证据。

工作区只能在其上下文文档或受控的决策/执行记录中维护固定资料引用。每一条引用至少包含下列字段：

| 字段 | 要求 |
|------|------|
| `reference_id` | 工作区内唯一的引用 ID。 |
| `workspace_id` | 必须等于工作区上下文的 `id`。 |
| `material_id` | 用户确认的资料稳定标识。 |
| `source` | 可追溯的资料来源路径或 URI。 |
| `version` | 不可省略的资料版本。 |
| `sha256` | 该版本的 64 位十六进制 SHA-256 摘要。 |
| `purpose` | 该引用为何与当前工作区相关。 |
| `local_record` | 本地注释或派生记录路径；没有时明确为 `none`。 |
| `status` | `active`、`withdrawn` 或 `invalid`，不得把资料可读性写成事实已确认。 |

以下规则是 fail-closed 的：缺少 `material_id`、`source`、`version` 或有效 `sha256` 的资料不得作为共享资料引用使用；工作区不匹配、目录为 `none`、来源或摘要不一致时，Skills 和消费适配器不得读取、推理混合、引用为证据或写入目标记录。

本协议不规定资料上传、用户 CRUD、保留实现、AI 读取执行、版权/敏感数据处理流程、跨工作区导航或 Web 写入；这些由 GOAL-009 I-009/I-010/I-004 及后续产品目标在其门禁内定义和验证。

## 6. Skills 与消费适配器规则

1. 若存在 `docs/vision/charter.md`，先读取 Charter 版本与 [alignment](../vision/alignment.md) 要点，再定位工作区。
2. 定位用户指定或已配置的工作区 `workspace.md`，校验 Root Goal、canonical scope、共享资料引用，以及（非 sandbox opt-out 时）`plan_refs` / `primary_plan` 与对应 VP 文件后，再扫描该工作区 `goal-tree.md` 与目标记录。
3. 若仓库只有一个显式工作区，消费适配器可以使用它作为当前 scope；多个工作区而未指定焦点时必须拒绝受影响读取、写入和放行。
4. 没有显式工作区根时，只能将旧 `docs/goals/` 作为 legacy 单工作区；不得自动发现、合并或写入其他目录。
5. 任何创建、决策、执行、审计或提案都必须在已验证的当前工作区内。资料候选库存只补充可核对的文件摘要，不替代固定引用或事实确认。愿景目录不保存目标进度权威。
6. `/audit` 只在当前工作区目标台账追加 `source: independent` 意见；它不得凭资料目录、愿景规划或索引改变状态或关闭 finding。

## 7. 与后续产品的交接

GOAL-011 将当前项目迁移到显式工作区根并提供共享资料候选索引骨架。它为 GOAL-009 R-003 提供目录与资料盘点输入，但不建立工作区实体/动态索引、资料用户 CRUD、AI 读取执行、跨工作区导航例外、访问安全契约或正反访问测试。因此 GOAL-009 的 I-009/I-010、F-003/F-004 和路线图 B 仍保持开放。
