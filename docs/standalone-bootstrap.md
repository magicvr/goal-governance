---
title: 核心包独立启用说明
status: active
created: 2026-07-19
updated: 2026-07-29
parent: null
version: 0.8.0
---

# 核心包独立启用说明

本说明验证 Goal Governance 的核心方法论、文档协议与 canonical 模板可以在一个**空 Git 仓库**中独立使用。它只复制核心文档层，不安装 `skills/`，也不启动 `web/`。

**完整独立启用必须遵守 P-006 冷启动顺序**（与 Skills 路径一致）：

```text
最小完备 Charter → 首个 VP 落盘 → 显式工作区 + Root（必填 plan_refs / primary_plan）
```

仅复制 architecture/templates、却跳过愿景与 plan 字段 = **不完整安装**，不得标为「完整独立启用成功」。

**Minimal Complete Install（MUST）** 唯一权威表见 [vision/alignment.md §0.2](vision/alignment.md#02-完整安装与冷启动)；本说明与 [consumer-checklist](vision/consumer-checklist.md)、[principles §6.2](architecture/principles.md#62-完整安装与冷启动) **同表**。下文章节是操作步骤，**不**另立较弱的「建议」完整集。

## 适用边界

复制来源：

| 来源 | 复制到目标仓库 | 用途 |
|------|----------------|------|
| `AGENTS.md` | 根目录 `AGENTS.md` | AI 与协作者的强制规则 |
| `docs/README.md` | `docs/README.md` | 核心文档入口与协议索引 |
| `docs/architecture/` | `docs/architecture/` | 架构约定与 **P-001～P-006** |
| `docs/templates/` | `docs/templates/` | 五件套、workspace 上下文、**vision/** 模板 |
| `docs/contracts/` | `docs/contracts/` | 消费适配器机读契约 |
| `docs/vision/alignment.md` | `docs/vision/alignment.md` | 愿景对齐**规则权威**（P-006 门禁细则） |

`skills/` 与 `web/` 不是本场景前置条件。dogfood 过程树、本仓 `charter.md` 实例、`plans/VP-001-…` 等**不要**整树复制；Charter/VP 从 `docs/templates/vision/` 在目标仓新建。

**与 Skills 双入口的关系（GOAL-023）**：若需要 AI Skills，请用 **skills zip（内嵌 core）** 的 bootstrap 或包内 install（见根 README / `skills/README.md`），**不要**把本 standalone 路径当作默认 Skills 安装。并行发布的 **core-only** zip（`goal-governance-core-v*.zip`，`scripts/pack_core_release.py`）与 monorepo `docs/` / `skills/core` 对齐，可作无 Skills 时的方法论快照来源。
**结构完整 ≠ 行为自动治理**：本说明验证文件、引用链与模板可独立建立，并提供默认 L0 规则；未安装 Skills 时，不存在自动扫描、提醒或写入门禁执行器。人或其他工具仍须实际按 AGENTS / principles / alignment 执行 P-004、P-005 与审计闭合，才能声称治理行为发生。

## 1. 建立空 Git 仓库并复制核心层

```powershell
$source = (Resolve-Path '.').Path
$target = Join-Path $env:TEMP ("goal-governance-core-" + [guid]::NewGuid())

New-Item -ItemType Directory -Path $target | Out-Null
git -C $target init

New-Item -ItemType Directory -Path (Join-Path $target 'docs') | Out-Null
New-Item -ItemType Directory -Path (Join-Path $target 'docs\vision') | Out-Null
Copy-Item (Join-Path $source 'AGENTS.md') (Join-Path $target 'AGENTS.md')
Copy-Item (Join-Path $source 'docs/README.md') (Join-Path $target 'docs/README.md')
Copy-Item -Recurse (Join-Path $source 'docs/architecture') (Join-Path $target 'docs/architecture')
Copy-Item -Recurse (Join-Path $source 'docs/templates') (Join-Path $target 'docs/templates')
Copy-Item -Recurse (Join-Path $source 'docs/contracts') (Join-Path $target 'docs/contracts')
Copy-Item (Join-Path $source 'docs/vision/alignment.md') (Join-Path $target 'docs/vision/alignment.md')
```

目标仓不应出现 `skills/` 或 `web/`。

## 2. 冷启动上环：Charter → VP

slug 与 `vision_id` **由项目自定**；下例仅演示。

### 2.1 Charter

```powershell
$vision = Join-Path $target 'docs\vision'
Copy-Item (Join-Path $target 'docs\templates\vision\charter.md') (Join-Path $vision 'charter.md')
New-Item -ItemType Directory -Path (Join-Path $vision 'plans') | Out-Null
```

将 `charter.md` 改写为真实项目：`vision_id`、目的、方向级成功边界、非目标（建议 ≥3）、`status: active`、`version`、`effective_date`。不可使用 Goal 的 `done`。

最小骨架示例字段：

```yaml
doc_type: vision-charter
vision_id: vision-example-project
status: active
version: 0.1.0
```

### 2.2 首个 VP

```powershell
Copy-Item (Join-Path $target 'docs\templates\vision\vision-plan.md') (Join-Path $vision 'plans\VP-001-example-intent.md')
```

将 `id`、文件名、`vision_ref: {vision_id}@{version}`（**精确匹配** Charter）、意图与退出判据改成真实值。`status` 可用 `planned` 或 `active`。

### 2.3 愿景树 MUST 文件（可极简，但必须存在）

完整独立启用在开区前还须具备 alignment MUST 表中的愿景树文件（**不是**可选建议）：

| 文件 | MUST 要求 |
|------|-----------|
| `docs/vision/README.md` | 目录入口（可从本包 `docs/vision/README.md` 复制后改写，或极简自拟） |
| `docs/vision/roadmap.md` | 组合编排索引；至少列出本 VP |
| `docs/vision/revisions.md` | Charter 修订台账（可仅表头 + 初建一行） |
| `docs/vision/reviews.md` | Vision Review 台账；Charter 初建后**宜**有一条 VRev（可为 self），文件本身为 MUST |
| `docs/vision/workspaces.md` | 工作区贡献图（开区前可写「尚无区」；开区后更新） |
| `docs/vision/consumer-checklist.md` | 与 alignment MUST 表一致的勾选（可从本包复制） |

```powershell
# 示例：从源仓复制愿景树骨架后改写（路径按实际调整）
foreach ($name in @('README.md','roadmap.md','revisions.md','reviews.md','workspaces.md','consumer-checklist.md')) {
  Copy-Item (Join-Path $source "docs\vision\$name") (Join-Path $vision $name) -ErrorAction SilentlyContinue
}
```

若源仓复制不可用，可手写极简占位文件，但**不得**省略文件名后仍宣称完整启用。规则权威仍是已复制的 `alignment.md`，不是 dogfood 过程记录。

## 3. 工作区 + Root（必须挂 VP）

**仅在** Charter 与可挂接 VP 存在后，再建工作区与 Root。

```powershell
$rootId = 'GOAL-001-main-vision'
$vpId = 'VP-001-example-intent'
$workspace = Join-Path $target 'docs\workspace-001-main-vision'
$root = Join-Path $workspace $rootId
$template = Join-Path $target 'docs\templates\goal-folder'

New-Item -ItemType Directory -Path $workspace | Out-Null
New-Item -ItemType Directory -Path $root | Out-Null
Copy-Item (Join-Path $template '00-meta.md') $root
Copy-Item (Join-Path $template '01-decision.md') $root
Copy-Item (Join-Path $template '02-execution.md') $root
Copy-Item (Join-Path $template '03-audit.md') $root
Copy-Item -Recurse (Join-Path $template 'attachments') $root
Copy-Item (Join-Path $target 'docs\templates\workspace-context.md') (Join-Path $workspace 'workspace.md')
```

### 3.1 `workspace.md` 必填字段

| 字段 | 要求 |
|------|------|
| `id` | 工作区稳定 id |
| `root_goal` | = Root 完整 id，且 Root `parent: null` |
| `canonical_scope` | 如 `docs/workspace-001-main-vision/` |
| `shared_materials_catalog` | 路径或 `none` |
| `vision_role` | `primary` \| `delivery` |
| `plan_refs` | **必填**；至少一个 VP id |
| `primary_plan` | **必填**；∈ `plan_refs`；对应 `docs/vision/plans/<id>.md` |

**禁止**省略 `plan_refs` / `primary_plan`（无 opt-out）。

### 3.2 Root 五件套

```yaml
id: GOAL-001-main-vision
title: <项目总目标>
status: active
parent: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
```

建议在 Root `00-meta` 同步 `plan_refs` / `primary_plan` 与短 `serves_summary`。四个 Markdown 与 `attachments/` 必须齐全；模板示例 id（如 `GOAL-042`）不得原样留下。

若已识别关键未知，立即建立 P-005 信息需求表。

## 4. 建立 `goal-tree.md`

在工作区根写入树与状态表，与 Root `id` / `parent` / `status` 一致。新 Root 尚无显式检查点时，`progress` 省略并显示 `—`；建立检查点后再按 P-001 派生规则重算。

````markdown
---
title: Goal Tree · 目标树与进展总览
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
parent: null
version: 0.1.0
---

# Goal Tree

```text
GOAL-001-main-vision · <项目总目标> [active]
```

| ID | 标题 | Parent | Status | Progress | 路径 |
|----|------|--------|--------|----------|------|
| GOAL-001-main-vision | <项目总目标> | — | active | — | GOAL-001-main-vision/ |
````

## 5. 核对清单与证据记录

完整独立启用须留下：

1. **来源**：核心层复制路径与版本（含 `alignment.md` 与愿景树 MUST 文件来源）。  
2. **生成路径**：alignment MUST 表所列愿景文件、`docs/vision/plans/<VP>.md`、`workspace.md`、`goal-tree.md`、Root 五件套。  
3. **核对结果**：
   - `git rev-parse --is-inside-work-tree` → `true`
   - Charter `status: active`；VP `vision_ref` 精确匹配 Charter
   - 愿景树 MUST 文件均存在：`README`、`roadmap`、`revisions`、`reviews`、`workspaces`、`consumer-checklist`、`alignment`
   - `workspace.md` 含 `plan_refs` 与 `primary_plan`，且 VP 文件存在
   - Root `parent: null`；`id` = 文件夹名；五件套齐全  
4. **边界**：无 `skills/` / `web/`；本验证不代表 Skills 安装或 Web 发布完成；保证等级默认 **L0**（见 principles P-003）。

**半安装**（仅 architecture、无 Charter/plan、或缺愿景树 MUST 文件）只可用于阅读原则，**不得**记为完整独立启用通过，也不得非引导推进/放行/关门。

可重复验证：

```powershell
python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v
```

该测试在临时目录执行 `git init`，按 **Charter → VP → 工作区+Root** 生成合规骨架，并断言 plan 字段与愿景文件存在。
