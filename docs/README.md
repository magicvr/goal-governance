---
title: 文档体系说明
status: active
created: 2026-07-18
updated: 2026-07-20
parent: null
version: 0.9.0
---

# docs/ · 文档体系

本目录是 **Goal Governance** 的核心规范与运行记录来源：方法论、文档协议、目标、决策、执行、审计与架构说明均以 Markdown 维护。具体目标实例的状态真相只存在于各自 `docs/workspace-<NNN>-<slug>/` 根。

## 目录结构

```text
docs/
├── README.md                 # 本文件：文档架构与使用规范
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
│   ├── workspace-protocol.md # 工作区/共享资料固定引用协议
│   └── tech-stack.md
└── _index/                   # 预留：索引、术语等（可扩展）
```

## 核心规则

1. **工作区内目标平铺**：所有目标直接放在各自 `docs/workspace-<NNN>-<slug>/` 根，**禁止**用嵌套文件夹表达层级。
2. **GOAL-001 为工作区总目标**：每个工作区的 `GOAL-001-*` 是 Root Goal；`parent` 必须为 `null`。
3. **工作区内顺序编号**：新目标从 `GOAL-002` 起递增，不可跳号占用、不可复用已取消编号作新含义（可标注 cancelled）。
4. **层级字段**：父子关系只写在各目标 `00-meta.md` 的 `parent` 中。
5. **总览同步**：任何新建/完成/改 parent/改状态，必须更新当前工作区的 `goal-tree.md`。
6. **标准五件套**：每个目标文件夹必须包含：
   - `00-meta.md` — 元信息与概述
   - `01-decision.md` — 决策（写清「为什么」）
   - `02-execution.md` — 执行（时间线、事实）
   - `03-audit.md` — 审计/复盘
   - `attachments/` — 附件（可为空，保留目录）
7. **可执行性与路线图（P-001）**：若目标尚不能直接执行（明显需要拆解），须先在该目标的 `00-meta.md` 或 `01-decision.md` 写清高层路线图（阶段与先后关系），再创建与执行子目标。
8. **治理闭环与交叉审计（P-002～P-004）**：阶段质量意识；独立审计出意见、编排器响应全部意见；「是否自审」与意见冲突由用户裁决（编排器给建议）。**正式审计意见**写入被审目标 `03-audit.md`（`A-00N` + `source`；长文可链 `attachments/`）。详见 [architecture/principles.md](architecture/principles.md)。
9. **信息就绪与未知项门禁（P-005）**：目标可带未知立项，但在 `00-meta.md` 或 `01-decision.md` 记录 I-00N、`required`/`non-blocking` 级别、影响门禁、最晚需要阶段、验证动作、状态、延期复核与证据。到期 required 信息项阻断受影响阶段；残余风险须有用户书面接受，且不等于已验证。
10. **核心模板、契约与分发镜像**：规范模板位于 `docs/templates/goal-folder/`，消费适配器契约位于 `docs/contracts/`；`skills/templates/goal-folder/` 与 `skills/contracts/` 是供安装脚本和离线复制使用的同步镜像。新目标实例写入当前工作区根，不把镜像目录当作目标状态或第二版本真相。
11. **独立启用**：不安装 `skills/`、不启动 `web/` 时，按 [standalone-bootstrap.md](standalone-bootstrap.md) 从核心文档层复制并建立第一个 Root Goal。
12. **工作区与共享资料协议**：显式工作区可从 `docs/templates/workspace-context.md` 创建 `docs/workspace-<NNN>-<slug>/workspace.md`，绑定一个 Root Goal 与该工作区根 canonical 范围；没有显式工作区根但保留 `docs/goals/` 的旧仓库才是 legacy 隐式单工作区。共享资料候选库存和固定引用不能形成第二套目标状态或跨工作区上下文通道。完整约束见 [architecture/workspace-protocol.md](architecture/workspace-protocol.md)。

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

- **当前核心文档版本**：`0.9.0`。本工作树将运行中目标实例迁入显式 `workspace-<NNN>-<slug>/` 根，并新增共享资料候选库存与重建索引脚本；受影响的宿主 runtime 矩阵仍明确为未发布候选，尚未宣称已形成新的 release。
- **最近发布基线**：`0.7.0`，对应 annotated `v0.7.0` release-candidate tag。
- **快照日期**：2026-07-19。
- **快照身份**：`0.4.0` 的已提交基线为 `2f54048db32b0e02194b0c0092e3e801b9532bc3`；`0.7.0` 候选 commit 为 `8a33ecd21d9183a680c9c0d63e471469f5e515a8`，由 `v0.7.0` annotated tag 绑定。
- **当前工作树边界**：`v0.7.0` 的发布证据继续绑定其历史 `candidateRevision`、候选 commit、CI 报告、变更日志和 annotated tag；GOAL-010 改变行为源后，当前矩阵为 `candidateRevision: unreleased`，受影响宿主入口须重新取得 runtime evidence，且不改写历史候选身份。
- **本轮变更范围**：新增信息需求、阶段门禁、残余风险接受和按规模拆分信息工作的核心规则；更新 canonical 五件套、消费适配器契约与矩阵、Skills 镜像、编排/审计提示词、宿主规则源、独立启用说明、CI/发行证据工具和契约测试。

### canonical → Skills 同步台账

`docs/templates/goal-folder/` 与 `docs/contracts/` 分别是模板和消费适配器兼容契约的唯一上游。本轮先更新 canonical 层，再同步覆盖 `skills/templates/goal-folder/` 与 `skills/contracts/`；以下为同步后的字节级台账：

| 类别 | 文件 | canonical SHA-256 | Skills mirror SHA-256 |
|------|------|------------------|----------------------|
| 模板 | `00-meta.md` | `5800252F8AF11CE741B90B04DA15D6FA8A71FBD8A253CB0D60C0AE270CA1F712` | `5800252F8AF11CE741B90B04DA15D6FA8A71FBD8A253CB0D60C0AE270CA1F712` |
| 模板 | `01-decision.md` | `C86403B96BA69E9E84B6662FF5B41EF0E637ABE5B2E57D8369E00FBA19F5B796` | `C86403B96BA69E9E84B6662FF5B41EF0E637ABE5B2E57D8369E00FBA19F5B796` |
| 模板 | `02-execution.md` | `7864D87F7AE97B0AA2E0E1D14E290AC21110CC9C20BDD70382BACDEBCF9EB132` | `7864D87F7AE97B0AA2E0E1D14E290AC21110CC9C20BDD70382BACDEBCF9EB132` |
| 模板 | `03-audit.md` | `44C72913995F8E27646C57555469A28B4FA06BCCDDBF2799B9D773C7F8920B4C` | `44C72913995F8E27646C57555469A28B4FA06BCCDDBF2799B9D773C7F8920B4C` |
| 模板 | `workspace-context.md` | `2DF812258D093012128F8AAF0E50D208481BE84EC67EBE43F493D9E5E32C4D1E` | `2DF812258D093012128F8AAF0E50D208481BE84EC67EBE43F493D9E5E32C4D1E` |
| 契约 | `skills-consumer-contract.schema.json` | `AA18EFE1AE85D3A37678DA435B82E1E572E06AD1EA5FFCA84287195C7840D309` | `AA18EFE1AE85D3A37678DA435B82E1E572E06AD1EA5FFCA84287195C7840D309` |
| 契约 | `skills-consumer-contract.json` | `5624F92DA6A7ED0BD3B72083619437452DAABFA5441ADCD52AF5E0784EF6177D` | `5624F92DA6A7ED0BD3B72083619437452DAABFA5441ADCD52AF5E0784EF6177D` |
| 契约 | `skills-consumer-compatibility-matrix.schema.json` | `60E604F9D8847CC592B7E62B0C2B277F6E44050B09EFF79338E3BC5B2EAC9901` | `60E604F9D8847CC592B7E62B0C2B277F6E44050B09EFF79338E3BC5B2EAC9901` |
| 契约 | `skills-consumer-compatibility-matrix.json` | `9768C7040969D8C28D0345D568A3323220FCA5AF6612C24F315FD972D2F918A5` | `9768C7040969D8C28D0345D568A3323220FCA5AF6612C24F315FD972D2F918A5` |
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
