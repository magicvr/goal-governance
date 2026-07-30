---
title: 文档体系说明
status: active
created: 2026-07-18
updated: 2026-07-31
parent: null
version: 0.10.8
---

# docs/ · 文档体系

本目录是 **Goal Governance** 的核心规范与运行记录来源：方法论、文档协议、目标、决策、执行、审计与架构说明均以 Markdown 维护。具体目标实例的状态真相只存在于各自 `docs/workspace-<NNN>-<slug>/` 根。仓库级愿景与规划对齐在 `docs/vision/`（**不是**第二套目标状态）。

**现行消费路径**：以 **Skills** 为主（Charter `vision-goal-governance@0.2.0`）。本仓 `web/` 为冻结参考实现，见根 README 与 [vision/charter.md](vision/charter.md)。

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
   - `progress`（若有）仅由显式检查点确定性派生；默认等权，显式权重可覆盖。它不放行阶段、不关闭 finding、不覆盖 I-00N 或 `status`，也不进入愿景层。
8. **治理闭环与交叉审计（P-002～P-004）**：阶段质量意识（含 P-001 路线图槽位）；独立审计出意见、编排器响应全部意见；finding 合法闭合为 `fixed` / `accepted-residual` / `user-overruled`；「是否自审」、意见冲突、单条必改否决/residual、信息 residual 由用户裁决。**正式审计意见**写入被审目标 `03-audit.md`（`A-00N` + `source`；长文可链 `attachments/`）。详见 [architecture/principles.md](architecture/principles.md)。
9. **信息就绪与未知项门禁（P-005）**：目标可带未知立项，但在 `00-meta.md` 或 `01-decision.md` 记录 I-00N、`required`/`non-blocking` 级别、影响门禁、最晚需要阶段、验证动作、状态、延期复核与证据。到期 required 信息项阻断受影响阶段；残余风险须有用户书面接受，且不等于已验证。
10. **愿景、组合治理与级联对齐（P-006）**：**单愿景**；完整安装必有 Charter；冷启动 **Charter → VP → 工作区**；对齐递归（每节点对齐上一级）；组合编排 / 意图(VP) / 纲领路线图 / 阶段计划；结构选型判定树；Vision Review（`reviews.md`）；工作区角色仅 `primary` / `delivery`。全文 [architecture/principles.md](architecture/principles.md) P-006；门禁 [vision/alignment.md](vision/alignment.md)。
11. **核心模板、契约与分发镜像**：规范模板位于 `docs/templates/`（含 `goal-folder/`、`workspace-context.md`、`vision/`），消费适配器契约位于 `docs/contracts/`。Skills 包镜像由 **`python scripts/stage_skills_mirrors.py`** 生成到 `skills/core/docs/` 与 `skills/contracts/`（GOAL-022）；pack/CI 强制 stage。`skills/core/docs/README.md` 为消费方**手维精简稿**。新目标实例写入当前工作区根，不把镜像目录当作目标状态或第二版本真相。
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

- **文档入口版本**（本文件 frontmatter）：`0.10.6` — 描述 docs 树导航与协议索引的修订号。  
- **可复制核心包版本**（对外分发/发版候选身份）：`0.10.0`（四入口 runtime + stage SSOT + 双资产/bootstrap）。二者**刻意分离**：入口文可快于尚未 tag 的包身份。  
- **最近发布基线**：`v0.7.0` / `v0.8.0` / `v0.9.0` / `v0.9.1` / `v0.9.2` / **`v0.10.0`（冻结中）**；正式 GitHub Release 仍以 annotated tag + release evidence 为准。
- **快照日期**：2026-07-30。
- **快照身份**：矩阵 **`candidateRevision: v0.10.0`**；默认四入口 × 三宿主 runtime-verified（**2026-07-30** 证据；behaviorSources 对现树 fresh）；Web parser automated-verified。
- **当前工作树边界**：`/govern` `/audit` `/vision` `/vision-audit` 在 Claude Code `2.1.220`、Grok Build `0.2.114` 与 GitHub Copilot CLI `1.0.75`（BYOK）上 `runtime-verified`（`/vision-audit` 为只读 dispatch）。**不**宣称 Root 终态或 R-009-X closed。GOAL-021～023 done；发版身份 `v0.10.0`。

### canonical → Skills 镜像（GOAL-022）

`docs/architecture/`（白名单文件）、`docs/templates/`、`docs/vision/alignment.md` 与 `docs/contracts/` 是唯一上游。刷新镜像：

```bash
python scripts/stage_skills_mirrors.py
python scripts/stage_skills_mirrors.py --check
```

| 生成落点 | 说明 |
|----------|------|
| `skills/core/docs/architecture/*` | 排除 `tech-stack.md` |
| `skills/core/docs/templates/**` | 五件套 + workspace-context + vision 模板 |
| `skills/core/docs/vision/alignment.md` | 愿景规则 |
| `skills/contracts/**` | 契约与 fixtures 逐字节镜像 |
| **不**覆盖 | `skills/core/docs/README.md`、`skills/core/docs/vision/README.md`（消费方手维精简） |

**AI / 维护者硬要求（漏做 = 远端 CI 红）**：

1. 只改 `docs/` 侧 canonical，**不要**手改 `skills/core/docs/**` 或 `skills/contracts/**` 镜像正文来消漂移。
2. 改完白名单路径后，在**同一提交任务**内运行 stage + `--check`，并把 `skills/core`、`skills/contracts`（及若有 `skills/templates`）变更一并提交。
3. 只提交 `docs/`、漏交镜像 → CI「Stage skills mirrors and fail on drift」失败（`git diff` 脏树门禁）。
4. 操作约定摘要亦见根目录 `AGENTS.md` **§8c**（AI 工具强制入口）。

`pack_skills_release.py` 在 monorepo 下打包前会自动 stage。CI 在测试前 stage 并要求工作树无漂移。核验：`python -m unittest skills/tests/test_skills_orchestrator.py scripts/tests/test_stage_skills_mirrors.py -v`。

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
