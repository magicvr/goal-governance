---
title: 文档体系说明
status: active
created: 2026-07-18
updated: 2026-10-17
parent: null
version: 0.15.0
---

# docs/ · 文档体系

本目录是 **Goal Governance** 的核心规范与运行记录来源：方法论、文档协议、目标、决策、执行、审计与架构说明均以 Markdown 维护。具体目标实例的状态真相只存在于各自 `{governance_root}/workspaces/workspace-<NNN>-<slug>/` 根。仓库级愿景与规划对齐在 `{governance_root}/vision/`（**不是**第二套目标状态）。

**现行消费路径**：以 **Skills** 为主（Charter `vision-goal-governance@0.2.0`）。冻结 Web 资产已物理退役；VP-003 保持 `planned` 并正式挂起，未来 UI 重新激活须新书面决策。

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
├── workspaces/               # 显式工作区统一父容器（非第二状态层）
│   └── workspace-001-example/
│       ├── workspace.md          # 显式工作区上下文（不保存目标状态）
│       ├── goal-tree.md          # 本工作区树状结构与进展总览
│       ├── GOAL-001-example-root/
│       │   ├── 00-meta.md
│       │   ├── 01-decision.md
│       │   ├── 02-execution.md
│       │   ├── 03-audit.md
│       │   └── attachments/
│       └── GOAL-002-.../
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

1. **工作区内目标平铺**：所有目标直接放在各自 `{governance_root}/workspaces/workspace-<NNN>-<slug>/` 根，**禁止**用嵌套文件夹表达层级。
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
8. **治理闭环与交叉审计（P-002～P-004）**：阶段质量意识（含 P-001 路线图槽位）；按风险选择 `none` / `self` / `independent` / `cross`，独立审计只出意见、编排器响应全部意见；finding 合法闭合为 `fixed` / `accepted-residual` / `user-overruled`；模式/provider 歧义、意见冲突、单条必改否决/residual、信息 residual 由用户裁决。**正式审计意见**写入被审目标 `03-audit.md` 索引与 `03-audit/A-NNN-*.md`（`source` 必填；长证据可链 `attachments/`）。详见 [architecture/principles.md](architecture/principles.md)。
9. **信息就绪与未知项门禁（P-005）**：目标可带未知立项，但在 `00-meta.md` 或 `01-decision.md` 记录 I-00N、`required`/`non-blocking` 级别、影响门禁、最晚需要阶段、验证动作、状态、延期复核与证据。到期 required 信息项阻断受影响阶段；残余风险须有用户书面接受，且不等于已验证。
10. **愿景、组合治理与级联对齐（P-006）**：**单愿景**；完整安装必有 Charter；冷启动 **Charter → VP → 工作区**；对齐递归（每节点对齐上一级）；组合编排 / 意图(VP) / 纲领路线图 / 阶段计划；结构选型判定树；Vision Review 使用 `reviews.md` 稳定索引 + `reviews/VRev-NNN-*.md` 独立报告；工作区角色仅 `primary` / `delivery`。全文 [architecture/principles.md](architecture/principles.md) P-006；门禁 [vision/alignment.md](vision/alignment.md)。
11. **核心模板、契约与分发镜像**：规范模板位于 `{governance_root}/templates/`（含 `goal-folder/`、`workspace-context.md`、`vision/`），消费适配器契约位于 `{governance_root}/contracts/`。Skills 包镜像由 **`python scripts/stage_skills_mirrors.py`** 生成到 `skills/core/docs/` 与 `skills/contracts/`（GOAL-022）；pack/CI 强制 stage。`skills/core/docs/README.md` 为消费方**手维精简稿**。新目标实例写入当前工作区根，不把镜像目录当作目标状态或第二版本真相。
12. **独立启用**：不安装 `skills/` 时，按 [standalone-bootstrap.md](standalone-bootstrap.md) 从核心文档层复制并建立第一个 Root Goal（须遵守 P-006 冷启动顺序）。
13. **工作区与共享资料协议**：显式工作区可从 `{governance_root}/templates/workspace-context.md` 创建 `{governance_root}/workspaces/workspace-<NNN>-<slug>/workspace.md`，绑定一个 Root Goal、canonical 范围与**必填** `plan_refs`/`primary_plan`。`workspaces/` 只是父容器；旧直属 `{governance_root}/workspace-*/` 仅触发迁移阻断，新旧并存 fail closed。仅在两类显式布局都不存在且保留 `{governance_root}/goals/` 时，才是 legacy 隐式单工作区。完整约束见 [architecture/workspace-protocol.md](architecture/workspace-protocol.md)。
14. **愿景体系（Charter → VP → Workspace）**：`{governance_root}/vision/` 维护不可 Goal-`done` 的唯一 Charter、可关门的意图 VP、组合编排索引、Vision Review 与对齐门禁。愿景**不是** goal-tree 或 progress 权威。见 [vision/alignment.md](vision/alignment.md)。

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
2. 在 `{governance_root}/workspaces/workspace-<NNN>-<slug>/` 创建 `GOAL-NNN-short-slug/`。
3. 写入五件套，并设置正确的 `parent`。
4. 更新 `goal-tree.md` 的树与表格。
5. 如影响架构，同步更新 `architecture/`。

## 核心包独立启用

需要在空 Git 仓库中只使用核心方法论与模板时，按 [核心包独立启用说明](standalone-bootstrap.md) 操作。该说明明确复制来源、生成路径和核对结果；仓库内的可重复验证位于 `docs/tests/test_standalone_bootstrap.py`。

## 可复制包版本与变更范围

- **文档入口版本**（本文件 frontmatter）：`0.15.0` — 描述 docs 树导航与 `workspaces/` 工作区容器协议的修订号。
- **可复制核心包版本**：[`0.13.6`](https://github.com/magicvr/goal-governance/releases/tag/v0.13.6) 正式发布（[GOAL-013](workspaces/workspace-002-methodology-skills-feedback/GOAL-013-audit-dispatch-and-user-input-gates/00-meta.md) 自动审计派发与用户答复阻塞门禁；[GOAL-014](workspaces/workspace-002-methodology-skills-feedback/GOAL-014-release-v0-13-6/00-meta.md) 完成正式发布与资产验收）。入口文修订号与发布身份分离，实际发行以 annotated tag 与 gated Release 为准。
- **最近发布基线**：`v0.7.0` / `v0.8.0` / `v0.9.0` / `v0.9.1` / `v0.9.2` / `v0.10.0` / `v0.11.0` / `v0.12.0` / `v0.12.1` / `v0.13.0` / `v0.13.1` / `v0.13.2` / `v0.13.3`（annotated tag 指向 main merge commit `dfa8600`；tag workflow run `34748891084` 经 Environment `release` 审批发布 **9 项** Release 资产，skills/core ZIP 重下载摘要与 sidecar 一致）/ **`v0.13.4`**（PR #23 → main merge commit `43479838`；tag workflow run `36808519534` 经 Environment `release` 审批发布 **9 项** Release 资产，skills/core ZIP 重下载摘要与 sidecar 一致）。
- **快照日期**：2026-10-17。
- **最新发布基线**：**`v0.13.6`**（PR #29 → main merge `97f6f1ea`；tag workflow [39000107099](https://github.com/magicvr/goal-governance/actions/runs/39000107099) 的 pack 与 gated publish 全绿，Environment API 记录 magicvr 人工 `skipped` 放行；9 项正式资产、双 ZIP SHA-256 与 sidecar 一致、实际下载的 bootstrap 隔离安装通过；GHCR `0.13.6` 拉取 digest 与发布日志一致、内置版本核对为 `0.13.6`）。上一基线 `v0.13.5`（PR #27 → main merge `1a6668e`）保留其历史身份。
- **发布快照身份**：`v0.13.6` 正式发布复用 GOAL-013 S3 于 2026-10-17 为当前工作树捕获、未修改的 16 份运行记录（`docs/releases/runtime/goal-013-s3-2026-10-17-current/`），矩阵 candidateRevision = `v0.13.6`；不宣称新宿主运行。Codex 不在承诺矩阵中。
- **当前工作树边界（2026-10-17）**：[GOAL-013](workspaces/workspace-002-methodology-skills-feedback/GOAL-013-audit-dispatch-and-user-input-gates/00-meta.md) S3 已为 Claude Code `2.1.301`、Grok Build `1.0.60`、GitHub Copilot CLI `1.0.75` 重取四入口 12 格证据，另有四宿主只读 MCP 目录角色探针（含 Codex `0.163.0`，不新增矩阵支持承诺）。16 份当前来源一致的记录位于 `docs/releases/runtime/goal-013-s3-2026-10-17-current/`，矩阵与 CI 一致性门禁已改指新记录；旧记录保留历史身份。当前对话真实同步卡片的 JSON/LF 提交、用户预选观察及部分答复/其他 blocker 保留已留痕；与后台 CLI 可见性严格区分。I-004 在 D-003 路径 A 及已列 profile 范围 verified，S3/S4 验证及关门审视完成，cross 意见与修正已落盘；GOAL-013 经 D-005 收尾为 done / 100%；v0.13.6 已由 GOAL-014 正式发布（PR #29 → main `97f6f1ea` → annotated tag → run 39000107099 → 9 项资产验收）并关门。静态规范不代表全平台硬拦截或穷尽所有 GUI 返回形态。`/commit` 不属于矩阵必达格；Root R3 终态未声明。
- **当前工作树边界补记（2026-10-17 · GOAL-015）**：[GOAL-015](workspaces/workspace-002-methodology-skills-feedback/GOAL-015-audit-command-labeled-form/00-meta.md) 把自动审计正式命令改为带标签形式 `/audit workspace-NNN goal-NNN` 与 `/vision-audit vp-NNN`（裸数字不再合法），并已按用户裁决（patch `v0.13.7`）在修正后的工作树上**重捕获 16 格运行证据**至 `docs/releases/runtime/v0.13.7/`（3 宿主 × 4 治理入口 + 四宿主 MCP 目录探针，探针正文即带标签命令，全部 `pass`）。矩阵 `candidateRevision` = `v0.13.7`，`capture_runtime_evidence --check` 与 `compatibility_report --require-ready`（`ready-for-release-evidence`、uncovered 0）通过；安装/GHCR 示例 pin、CI 证据目录与相关测试断言已同步。上条所述 GOAL-013 的 16 份记录保留其历史身份（其 `behaviorSources` 对当前树已过期）。`v0.13.7` 目前是**发布候选**，正式身份仍待 main merge、annotated tag、strict release evidence、Environment 人工审批与资产核对建立。

### canonical → Skills 镜像（GOAL-022）

`{governance_root}/architecture/`（白名单文件）、`{governance_root}/templates/`、`{governance_root}/vision/alignment.md`、`{governance_root}/standalone-bootstrap.md` 与 `{governance_root}/contracts/` 是唯一上游。刷新镜像：

```bash
python scripts/stage_skills_mirrors.py
python scripts/stage_skills_mirrors.py --check
```

| 生成落点 | 说明 |
|----------|------|
| `skills/core/docs/architecture/*` | 排除 `tech-stack.md` |
| `skills/core/docs/templates/**` | 五件套 + workspace-context + vision 模板 |
| `skills/core/docs/vision/alignment.md` | 愿景规则 |
| `skills/core/docs/standalone-bootstrap.md` | 独立启用说明（Recommended；随两个消费包分发） |
| `skills/contracts/**` | 契约与 fixtures 逐字节镜像 |
| **不**覆盖 | `skills/core/docs/README.md`、`skills/core/docs/vision/README.md`（消费方手维精简） |

**AI / 维护者硬要求（漏做 = 远端 CI 红）**：

1. 只改 `docs/` 侧 canonical，**不要**手改 `skills/core/docs/**` 或 `skills/contracts/**` 镜像正文来消漂移。
2. 改完白名单路径后，在**同一提交任务**内运行 stage + `--check`，并把 `skills/core`、`skills/contracts`（及若有 `skills/templates`）变更一并提交。
3. 只提交 `docs/`、漏交镜像 → CI「Stage skills mirrors and fail on drift」失败（`git diff` 脏树门禁）。
4. 操作约定摘要亦见根目录 `AGENTS.md` **§8c**（AI 工具强制入口）。

`pack_skills_release.py` 在 monorepo 下打包前会自动 stage。CI 在测试前 stage 并要求工作树无漂移。核验：`python -m unittest skills/tests/test_skills_orchestrator.py scripts/tests/test_stage_skills_mirrors.py -v`。

`contractSchemaId` 指向 schema 的 canonical `$id`；manifest 的 `evidenceBoundary` 机读区分默认 consumer profile 与 producer-only 证据。普通消费安装只携带 consumer contract + schema，不要求 compatibility matrix / runtime evidence，也不要求用户删除旧安装残留；生产仓发行验证仍使用完整 `{governance_root}/contracts/`。`supportBaseline` 记录首个/上一支持协议，adapter 的 `supportCommitment` 区分已声明范围与当前承诺，`verificationStatus` 只表示版本固定的实际入口运行时证据是否已经取得；它不替代其他入口、manifest 解析、CI 或 release 验收。

## 三层交付关系

| 形态 | 职责 | 路径 |
|------|------|------|
| 核心方法论、模板与契约 | 生命周期、治理原则、文档协议、canonical 五件套与工作区上下文模板、消费适配器兼容契约；可独立应用，不依赖 Skills 或 Web | `{governance_root}/README.md`、`{governance_root}/architecture/`、`{governance_root}/templates/`、`{governance_root}/contracts/` |
| 文档实例 | 每个工作区的目标与过程权威记录 | `{governance_root}/workspaces/workspace-<NNN>-<slug>/` |
| 人类 UI | VP-003 远期适配器类；当前无绑定实现，重新激活须新决策与通用基架边界 | `{governance_root}/vision/plans/VP-003-human-ui-workbench-deferred.md` |
| Skills / 提示词 | 独立的 AI 辅助闭环工具体系，按核心协议读写与推进目标，并分发模板/契约镜像 | `skills/`、根目录 `AGENTS.md` 等 |

## 推荐阅读顺序

1. [workspace-001-goal-governance/goal-tree.md](workspace-001-goal-governance/goal-tree.md) — 当前工作区进展
2. [workspace-001-goal-governance/GOAL-001-main-vision/00-meta.md](workspace-001-goal-governance/GOAL-001-main-vision/00-meta.md) — 当前工作区总目标
3. [architecture/overview.md](architecture/overview.md) — 架构概览  
4. [architecture/principles.md](architecture/principles.md) — 治理原则  
5. [templates/README.md](templates/README.md) — 核心文档模板
6. [contracts/skills-consumer-contract.json](contracts/skills-consumer-contract.json) — 消费适配器版本与兼容声明
7. 仓库根 [AGENTS.md](../AGENTS.md) — AI 协作强制规则
