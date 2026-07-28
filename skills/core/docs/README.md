---
title: 文档体系说明
status: active
created: 2026-07-18
updated: 2026-07-28
parent: null
version: 0.10.1
---

# docs/ · 文档体系

本目录是 **Goal Governance** 的核心规范与运行记录来源：方法论、文档协议、目标、决策、执行、审计与架构说明均以 Markdown 维护。具体目标实例的状态真相只存在于各自 `docs/workspace-<NNN>-<slug>/` 根。仓库级愿景与规划对齐在 `docs/vision/`（**不是**第二套目标状态）。

## 目录结构

```text
docs/
├── README.md                 # 本文件：文档架构与使用规范
├── vision/                   # 仓库级愿景：Charter → VP → 工作区对齐
│   ├── charter.md
│   ├── roadmap.md
│   ├── plans/VP-*.md
│   └── alignment.md
├── standalone-bootstrap.md   # 核心包独立启用与空 Git 验证
├── tests/                    # 核心文档层的可重复验证
├── workspace-001-example/    # 工作区根（目标在其中扁平存放）
│   ├── workspace.md          # 显式工作区上下文（不保存目标状态）
│   ├── goal-tree.md          # 本工作区树状结构与进展总览
│   ├── GOAL-001-example-root/
│   │   ├── 00-meta.md
│   │   ├── 01-decision.md
│   │   ├── 02-execution.md
│   │   ├── 03-audit.md
│   │   └── attachments/
│   └── GOAL-002-.../
├── shared-materials/         # 工作区外的资料候选库存
├── templates/                # 核心 canonical 文档模板
│   ├── README.md
│   └── goal-folder/          # 五件套模板
├── contracts/                # 消费适配器的 canonical 机读兼容契约
│   ├── skills-consumer-contract.schema.json
│   ├── skills-consumer-contract.json
│   ├── skills-consumer-compatibility-matrix.schema.json
│   ├── skills-consumer-compatibility-matrix.json
│   └── runtime-evidence.schema.json
├── architecture/             # 架构与技术约定
│   ├── overview.md
│   ├── principles.md         # 治理原则（元规则）
│   ├── workspace-protocol.md # 工作区/共享资料/愿景对齐协议
│   └── tech-stack.md
└── _index/                   # 预留：索引、术语等（可扩展）
```

## 核心规则

1. **工作区内目标平铺**：所有目标直接放在各自 `docs/workspace-<NNN>-<slug>/` 根，**禁止**用嵌套文件夹表达层级。
2. **GOAL-001 为工作区总目标**：每个工作区的 `GOAL-001-*` 是 Root Goal；`parent` 必须为 `null`。
3. **工作区内编号**：新编号 = 当前最大编号 + 1（三位）。编号**单调不复用**（含 `cancelled`）；历史空洞可保留；**禁止**把已取消编号赋予新含义。`GOAL-*` 仅工作区内唯一，**不**把工作区编号嵌进 goal id。跨区引用见 [architecture/workspace-protocol.md](architecture/workspace-protocol.md) §2.6：文档默认 **Q2** canonical 路径，对话默认 **Q3** 标签；裸 id 仅限已绑定当前工作区。
4. **层级字段**：父子关系只写在各目标 `00-meta.md` 的 `parent` 中。
5. **总览同步**：任何新建/完成/改 parent/改状态，必须更新当前工作区的 `goal-tree.md`。
6. **标准五件套**：每个目标文件夹必须包含：
   - `00-meta.md` — 元信息与概述
   - `01-decision.md` — 决策（写清「为什么」）
   - `02-execution.md` — 执行（时间线、事实）
   - `03-audit.md` — 审计/复盘
   - `attachments/` — 附件（可为空，保留目录）
7. **可执行性与纲领路线图（P-001）**：若目标尚不能直接执行（明显需要拆解），须先在该目标的 `00-meta.md` 或 `01-decision.md` 写清**纲领路线图**（阶段与先后关系），再创建与执行子目标。纲领阶段通常串行；**同一纲领阶段内**可并行子目标。
8. **治理闭环与交叉审计（P-002～P-004）**：阶段质量意识（含 P-001 路线图槽位）；独立审计出意见、编排器响应全部意见；finding 合法闭合为 `fixed` / `accepted-residual` / `user-overruled`；「是否自审」、意见冲突、单条必改否决/residual、信息 residual 由用户裁决。**正式审计意见**写入被审目标 `03-audit.md`（`A-00N` + `source`；长文可链 `attachments/`）。详见 [architecture/principles.md](architecture/principles.md)。
9. **信息就绪与未知项门禁（P-005）**：目标可带未知立项，但在 `00-meta.md` 或 `01-decision.md` 记录 I-00N、`required`/`non-blocking` 级别、影响门禁、最晚需要阶段、验证动作、状态、延期复核与证据。到期 required 信息项阻断受影响阶段；残余风险须有用户书面接受，且不等于已验证。
10. **愿景、组合治理与级联对齐（P-006）**：**单愿景**；完整安装必有 Charter；冷启动 **Charter → VP → 工作区**；对齐递归（每节点对齐上一级）；组合编排 / 意图(VP) / 纲领路线图 / 阶段计划；结构选型判定树；Vision Review（`reviews.md`）；**无 sandbox plan opt-out**。全文 [architecture/principles.md](architecture/principles.md) P-006；门禁 [vision/alignment.md](vision/alignment.md)。
11. **核心模板、契约与分发镜像**：规范模板位于 `docs/templates/`（含 `goal-folder/`、`workspace-context.md`、`vision/`），消费适配器契约位于 `docs/contracts/`；`skills/templates/` 与 `skills/contracts/` 是供安装脚本和离线复制使用的同步镜像。新目标实例写入当前工作区根，不把镜像目录当作目标状态或第二版本真相。
12. **独立启用**：不安装 `skills/`、不启动 `web/` 时，按 [standalone-bootstrap.md](standalone-bootstrap.md) 从核心文档层复制并建立第一个 Root Goal（须遵守 P-006 冷启动顺序）。
13. **工作区与共享资料协议**：显式工作区可从 `docs/templates/workspace-context.md` 创建 `docs/workspace-<NNN>-<slug>/workspace.md`，绑定一个 Root Goal、canonical 范围与**必填** `plan_refs`/`primary_plan`；**仅当**没有显式工作区根且保留 `docs/goals/` 的旧仓库才是 legacy 隐式单工作区——否则不得猜测工作区根。完整约束见 [architecture/workspace-protocol.md](architecture/workspace-protocol.md)。
14. **愿景体系（Charter → VP → Workspace）**：`docs/vision/` 维护不可 Goal-`done` 的唯一 Charter、可关门的意图 VP、组合编排索引、Vision Review 与对齐门禁。愿景**不是** goal-tree 或 progress 权威。见 [vision/alignment.md](vision/alignment.md)。

## Frontmatter 约定

每个文档建议至少包含：

```yaml
---
status: active          # draft | active | blocked | done | cancelled
created: YYYY-MM-DD
updated: YYYY-MM-DD
parent: null            # 或父目标 ID，如 GOAL-001-main-vision
version: 0.1.0
---
```

目标类文件另含 `id`；决策/执行/审计可用 `doc: decision|execution|audit`。

## 如何新增目标

1. 定位当前工作区的 `goal-tree.md` 确定下一个编号。
2. 在 `docs/workspace-<NNN>-<slug>/` 创建 `GOAL-NNN-short-slug/`。
3. 写入五件套，并设置正确的 `parent`。
4. 更新 `goal-tree.md` 的树与表格。
5. 如影响架构，同步更新 `architecture/`。

## 核心包独立启用

需要在空 Git 仓库中只使用核心方法论与模板时，按 [核心包独立启用说明](standalone-bootstrap.md) 操作。该说明明确复制来源、生成路径和核对结果；仓库内的可重复验证位于 `docs/tests/test_standalone_bootstrap.py`。

## 可复制包版本与变更范围

- **当前核心文档版本**：`0.9.1`（含 workspace-protocol **0.5.0** A0 限定引用）。工作区根与共享资料协议已就位。
- **最近发布基线**：`v0.7.0` / `v0.8.0` / `v0.9.0` / **`v0.9.1`**（冻结候选；annotated tag 以合并 `main` 后推送为准）。
- **快照日期**：2026-07-28。
- **快照身份**：矩阵 **`candidateRevision: v0.9.1`**；六 CLI runtime 2026-07-28 已对当前行为源重采；正式 GitHub Release 仍以 annotated `v0.9.1` + release evidence 为准。
- **当前工作树边界**：六 CLI 入口 **ready-for-release-evidence**；Web parser 仍为 automated-verified。Copilot 重采因 GitHub 月度配额耗尽，经 `COPILOT_PROVIDER_BASE_URL` BYOK 完成（宿主仍为 Copilot CLI）。
- **本轮变更范围（0.9.1）**：GOAL-010 D-003 A0 限定引用；finding 三路径/愿景门禁；Charter→VP 对齐；详见根 `CHANGELOG.md`。

### canonical → Skills 同步台账

`docs/templates/goal-folder/` 与 `docs/contracts/` 分别是模板和消费适配器兼容契约的唯一上游。本轮先更新 canonical 层，再同步覆盖 `skills/templates/goal-folder/` 与 `skills/contracts/`；以下为同步后的字节级台账：

| 类别 | 文件 | canonical SHA-256 | Skills mirror SHA-256 |
|------|------|------------------|----------------------|
| 模板 | `00-meta.md` | `5800252F8AF11CE741B90B04DA15D6FA8A71FBD8A253CB0D60C0AE270CA1F712` | `5800252F8AF11CE741B90B04DA15D6FA8A71FBD8A253CB0D60C0AE270CA1F712` |
| 模板 | `01-decision.md` | `C86403B96BA69E9E84B6662FF5B41EF0E637ABE5B2E57D8369E00FBA19F5B796` | `C86403B96BA69E9E84B6662FF5B41EF0E637ABE5B2E57D8369E00FBA19F5B796` |
| 模板 | `02-execution.md` | `7864D87F7AE97B0AA2E0E1D14E290AC21110CC9C20BDD70382BACDEBCF9EB132` | `7864D87F7AE97B0AA2E0E1D14E290AC21110CC9C20BDD70382BACDEBCF9EB132` |
| 模板 | `03-audit.md` | `44C72913995F8E27646C57555469A28B4FA06BCCDDBF2799B9D773C7F8920B4C` | `44C72913995F8E27646C57555469A28B4FA06BCCDDBF2799B9D773C7F8920B4C` |
| 模板 | `workspace-context.md` | `B9A6C8E731A3B9E7751994EDA1AEB2198779869E56EEF3947D63A84CF728DDB5` | `B9A6C8E731A3B9E7751994EDA1AEB2198779869E56EEF3947D63A84CF728DDB5` |
| 契约 | `skills-consumer-contract.schema.json` | `AA18EFE1AE85D3A37678DA435B82E1E572E06AD1EA5FFCA84287195C7840D309` | `AA18EFE1AE85D3A37678DA435B82E1E572E06AD1EA5FFCA84287195C7840D309` |
| 契约 | `skills-consumer-contract.json` | `5624F92DA6A7ED0BD3B72083619437452DAABFA5441ADCD52AF5E0784EF6177D` | `5624F92DA6A7ED0BD3B72083619437452DAABFA5441ADCD52AF5E0784EF6177D` |
| 契约 | `skills-consumer-compatibility-matrix.schema.json` | `60E604F9D8847CC592B7E62B0C2B277F6E44050B09EFF79338E3BC5B2EAC9901` | `60E604F9D8847CC592B7E62B0C2B277F6E44050B09EFF79338E3BC5B2EAC9901` |
| 契约 | `skills-consumer-compatibility-matrix.json` | `0A0D31CFDD5CC927C5AECD1782FC6186A0400C50F11A23B7B562A659E8C9BC0E` | `0A0D31CFDD5CC927C5AECD1782FC6186A0400C50F11A23B7B562A659E8C9BC0E` |
| 契约 | `runtime-evidence.schema.json` | `515B86C1FD7E69C8304DACADF7D9E5BE8014F8C1587705149AFB574D1779D4F5` | `515B86C1FD7E69C8304DACADF7D9E5BE8014F8C1587705149AFB574D1779D4F5` |

核验命令：`python -m unittest skills/tests/test_skills_orchestrator.py -v`（包含模板/契约镜像、契约正反 fixtures、安装输出与 P-005 分发断言）；当前工作树应显示 canonical 与 Skills 镜像的同向更新，而非“模板未变更”。

`contractSchemaId` 指向 schema 的 canonical `$id`；安装包中的 manifest 通过 `canonical.schemaPath` 指向随包的本地 schema。`supportBaseline` 记录首个/上一支持协议，adapter 的 `supportCommitment` 区分已声明范围与当前承诺，`verificationStatus` 只表示版本固定的实际入口运行时证据是否已经取得；它不替代其他入口、manifest 解析、CI 或 release 验收。该 `$id` 是 schema 身份而不是当前 release 的承诺；I-003 仍负责把提交、tag/release、digest 和可重放证据关联起来。

## 三层交付关系

| 形态 | 职责 | 路径 |
|------|------|------|
| 核心方法论、模板与契约 | 生命周期、治理原则、文档协议、canonical 五件套与工作区上下文模板、消费适配器兼容契约；可独立应用，不依赖 Skills 或 Web | `docs/README.md`、`docs/architecture/`、`docs/templates/`、`docs/contracts/` |
| 文档实例 | 每个工作区的目标与过程权威记录 | `docs/workspace-<NNN>-<slug>/` |
| Web 应用 | 当前仅解析/浏览目标文档；完整闭环能力留待后续阶段，且与 Skills 为独立辅助工具体系 | `web/` |
| Skills / 提示词 | 独立的 AI 辅助闭环工具体系，按核心协议读写与推进目标，并分发模板/契约镜像 | `skills/`、根目录 `AGENTS.md` 等 |

## 推荐阅读顺序

1. [workspace-001-goal-governance/goal-tree.md](workspace-001-goal-governance/goal-tree.md) — 当前工作区进展
2. [workspace-001-goal-governance/GOAL-001-main-vision/00-meta.md](workspace-001-goal-governance/GOAL-001-main-vision/00-meta.md) — 当前工作区总目标
3. [architecture/overview.md](architecture/overview.md) — 架构概览  
4. [architecture/principles.md](architecture/principles.md) — 治理原则  
5. [templates/README.md](templates/README.md) — 核心文档模板
6. [contracts/skills-consumer-contract.json](contracts/skills-consumer-contract.json) — 消费适配器版本与兼容声明
7. 仓库根 [AGENTS.md](../AGENTS.md) — AI 协作强制规则
