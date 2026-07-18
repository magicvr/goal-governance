---
title: 文档体系说明
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.4.0
---

# docs/ · 文档体系

本目录是 **Goal Governance** 的核心规范与运行记录来源：方法论、文档协议、目标、决策、执行、审计与架构说明均以 Markdown 维护。具体目标实例的状态真相仍只存在于 `docs/goals/`。

## 目录结构

```text
docs/
├── README.md                 # 本文件：文档架构与使用规范
├── standalone-bootstrap.md   # 核心包独立启用与空 Git 验证
├── tests/                    # 核心文档层的可重复验证
├── goals/                    # 目标（扁平存放）
│   ├── goal-tree.md          # 树状结构与进展总览（必维护）
│   ├── GOAL-001-main-vision/
│   │   ├── 00-meta.md
│   │   ├── 01-decision.md
│   │   ├── 02-execution.md
│   │   ├── 03-audit.md
│   │   └── attachments/
│   └── GOAL-002-.../
├── templates/                # 核心 canonical 文档模板
│   ├── README.md
│   └── goal-folder/          # 五件套模板
├── architecture/             # 架构与技术约定
│   ├── overview.md
│   ├── principles.md         # 治理原则（元规则）
│   └── tech-stack.md
└── _index/                   # 预留：索引、术语等（可扩展）
```

## 核心规则

1. **目标平铺**：所有目标直接放在 `docs/goals/` 下，**禁止**用嵌套文件夹表达层级。
2. **GOAL-001 为总目标**：`GOAL-001-main-vision` 是 Root Goal；`parent` 必须为 `null`。
3. **顺序编号**：新目标从 `GOAL-002` 起递增，不可跳号占用、不可复用已取消编号作新含义（可标注 cancelled）。
4. **层级字段**：父子关系只写在各目标 `00-meta.md` 的 `parent` 中。
5. **总览同步**：任何新建/完成/改 parent/改状态，必须更新 [goals/goal-tree.md](goals/goal-tree.md)。
6. **标准五件套**：每个目标文件夹必须包含：
   - `00-meta.md` — 元信息与概述
   - `01-decision.md` — 决策（写清「为什么」）
   - `02-execution.md` — 执行（时间线、事实）
   - `03-audit.md` — 审计/复盘
   - `attachments/` — 附件（可为空，保留目录）
7. **可执行性与路线图（P-001）**：若目标尚不能直接执行（明显需要拆解），须先在该目标的 `00-meta.md` 或 `01-decision.md` 写清高层路线图（阶段与先后关系），再创建与执行子目标。
8. **治理闭环与交叉审计（P-002～P-004）**：阶段质量意识；独立审计出意见、编排器响应全部意见；「是否自审」与意见冲突由用户裁决（编排器给建议）。**正式审计意见**写入被审目标 `03-audit.md`（`A-00N` + `source`；长文可链 `attachments/`）。详见 [architecture/principles.md](architecture/principles.md)。
9. **核心模板与分发镜像**：规范模板位于 `docs/templates/goal-folder/`；`skills/templates/goal-folder/` 是供安装脚本和离线复制使用的同步镜像。新目标实例仍写入 `docs/goals/`，不把模板目录当作目标状态。
10. **独立启用**：不安装 `skills/`、不启动 `web/` 时，按 [standalone-bootstrap.md](standalone-bootstrap.md) 从核心文档层复制并建立第一个 Root Goal。

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

1. 查看 [goals/goal-tree.md](goals/goal-tree.md) 确定下一个编号。
2. 在 `docs/goals/` 创建 `GOAL-NNN-short-slug/`。
3. 写入五件套，并设置正确的 `parent`。
4. 更新 `goal-tree.md` 的树与表格。
5. 如影响架构，同步更新 `architecture/`。

## 核心包独立启用

需要在空 Git 仓库中只使用核心方法论与模板时，按 [核心包独立启用说明](standalone-bootstrap.md) 操作。该说明明确复制来源、生成路径和核对结果；仓库内的可重复验证位于 `docs/tests/test_standalone_bootstrap.py`。

## 可复制包版本与变更范围

- **核心包版本**：`0.4.0`，与本入口文档的 `version` 一致。
- **快照日期**：2026-07-19。
- **快照性质**：当前工作树快照，尚未声明为 release 或已提交版本；后续语义变更应递增本入口版本并刷新本台账。
- **本轮变更范围**：新增 `standalone-bootstrap.md`、`tests/test_standalone_bootstrap.py` 与 GOAL-006 验收附件；更新本入口及 GOAL-006 的决策、执行、进度和目标树记录；`docs/templates/goal-folder/` 与 `skills/templates/goal-folder/` 的模板内容未改动。

### canonical → Skills 同步台账

`docs/templates/goal-folder/` 仍是唯一上游。本轮没有 canonical 内容变更，因此没有执行覆盖式复制；已在 2026-07-19 运行字节级一致性核验，确认分发镜像保持同步：

| 文件 | canonical SHA-256 | Skills mirror SHA-256 |
|------|------------------|----------------------|
| `00-meta.md` | `876375F56EE57F15DAEA3A67C43EDFAAF651B4BB1CF16DB24376FAEC3424AB43` | `876375F56EE57F15DAEA3A67C43EDFAAF651B4BB1CF16DB24376FAEC3424AB43` |
| `01-decision.md` | `C4A35BA90099026154072D41D0385066F160B37C08D985E08058E45C617FED9B` | `C4A35BA90099026154072D41D0385066F160B37C08D985E08058E45C617FED9B` |
| `02-execution.md` | `B9BAB71636E3F3AF49192430DC4DE8A62859481B41D716D08F4997D320078D4F` | `B9BAB71636E3F3AF49192430DC4DE8A62859481B41D716D08F4997D320078D4F` |
| `03-audit.md` | `E5FB3681F0ED9C332E6EF3C2C486E150718C842352E7D2831823172C9E52F2BE` | `E5FB3681F0ED9C332E6EF3C2C486E150718C842352E7D2831823172C9E52F2BE` |

核验命令：`python -m unittest skills/tests/test_skills_orchestrator.py -v`（21 项通过，包含模板镜像断言）；当前工作树的 `git diff --name-status HEAD -- docs/templates skills/templates` 为空，作为“模板未变更、镜像已核对”的范围证据。

## 三层交付关系

| 形态 | 职责 | 路径 |
|------|------|------|
| 核心方法论与模板 | 生命周期、治理原则、文档协议与 canonical 五件套模板 | `docs/README.md`、`docs/architecture/`、`docs/templates/` |
| 文档实例 | 目标与过程的权威记录 | `docs/goals/` |
| Web 应用 | 浏览目标与文档诊断（当前只读；写入待后续阶段） | `web/` |
| Skills / 提示词 | AI 按核心协议读写与推进目标 | `skills/`、根目录 `AGENTS.md` 等 |

## 推荐阅读顺序

1. [goals/goal-tree.md](goals/goal-tree.md) — 全局进展  
2. [goals/GOAL-001-main-vision/00-meta.md](goals/GOAL-001-main-vision/00-meta.md) — 总目标  
3. [architecture/overview.md](architecture/overview.md) — 架构概览  
4. [architecture/principles.md](architecture/principles.md) — 治理原则  
5. [templates/README.md](templates/README.md) — 核心文档模板
6. 仓库根 [AGENTS.md](../AGENTS.md) — AI 协作强制规则
