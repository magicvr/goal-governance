---
title: 核心包独立启用说明
status: active
created: 2026-07-19
updated: 2026-07-19
parent: null
version: 0.3.0
---

# 核心包独立启用说明

本说明验证 Goal Governance 的核心方法论、文档协议与 canonical 模板可以在一个**空 Git 仓库**中独立使用。它只复制核心文档层，不安装 `skills/`，也不启动 `web/`。

## 适用边界

复制来源只有以下五类：

| 来源 | 复制到目标仓库 | 用途 |
|------|----------------|------|
| `AGENTS.md` | 根目录 `AGENTS.md` | AI 与协作者的强制规则 |
| `docs/README.md` | `docs/README.md` | 核心文档入口与协议索引 |
| `docs/architecture/` | `docs/architecture/` | 架构约定与 P-001～P-005 |
| `docs/templates/` | `docs/templates/` | canonical 五件套模板 |
| `docs/contracts/` | `docs/contracts/` | canonical 机读协议/模板版本与兼容声明 |

`skills/` 是后续的消费适配器与分发镜像，`web/` 是可选的人类工作台；两者都不是本场景的前置条件。

## 1. 建立空 Git 仓库

下面以 PowerShell 为例。`$source` 是本仓库根目录，`$target` 必须是一个新的、位于 `$source` 之外的目录。

```powershell
$source = (Resolve-Path '.').Path
$target = Join-Path $env:TEMP ("goal-governance-core-" + [guid]::NewGuid())

New-Item -ItemType Directory -Path $target | Out-Null
git -C $target init

New-Item -ItemType Directory -Path (Join-Path $target 'docs') | Out-Null
Copy-Item (Join-Path $source 'AGENTS.md') (Join-Path $target 'AGENTS.md')
Copy-Item (Join-Path $source 'docs/README.md') (Join-Path $target 'docs/README.md')
Copy-Item -Recurse (Join-Path $source 'docs/architecture') (Join-Path $target 'docs/architecture')
Copy-Item -Recurse (Join-Path $source 'docs/templates') (Join-Path $target 'docs/templates')
Copy-Item -Recurse (Join-Path $source 'docs/contracts') (Join-Path $target 'docs/contracts')
```

复制完成后，目标仓库不应出现 `skills/` 或 `web/`。若目标已有同名核心文件，应先确认版本与变更范围，再决定是否覆盖。

## 2. 建立第一个 Root Goal

Root 编号固定为 `GOAL-001`，英文 slug 由项目自行决定。下面使用 `main-vision`；实际项目可以换成其他小写短横线 slug，但 `id`、文件夹名和引用必须保持一致。

```powershell
$rootId = 'GOAL-001-main-vision'
$goals = Join-Path $target 'docs/goals'
$root = Join-Path $goals $rootId
$template = Join-Path $target 'docs/templates/goal-folder'

New-Item -ItemType Directory -Path $goals | Out-Null
New-Item -ItemType Directory -Path $root | Out-Null
Copy-Item (Join-Path $template '00-meta.md') $root
Copy-Item (Join-Path $template '01-decision.md') $root
Copy-Item (Join-Path $template '02-execution.md') $root
Copy-Item (Join-Path $template '03-audit.md') $root
Copy-Item -Recurse (Join-Path $template 'attachments') $root
```

把复制出的模板示例改成真实 Root Goal，至少核对以下值：

```yaml
id: GOAL-001-main-vision
title: <项目总目标>
status: active
parent: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0
progress: 0%
```

四个 Markdown 文件和 `attachments/` 必须全部保留。`01-decision.md`、`02-execution.md` 与 `03-audit.md` 的 `id`、`parent`、日期和版本也要与 Root 对齐；模板中的示例 `GOAL-042`、`GOAL-040` 不能原样留下。

若 Root 已识别出尚未知悉的关键事实，在 `00-meta.md` 或 `01-decision.md` 立即建立 P-005 信息需求表：写清问题、`required`/`non-blocking` 级别、影响门禁、最晚需要阶段、验证动作、状态、延期复核和证据。目标可带未知立项，但不可把未知写成已验证结论；影响当前阶段的 required 信息项应先澄清或获得用户书面接受的残余风险。

## 3. 建立 `goal-tree.md`

在 `docs/goals/goal-tree.md` 写入包含 Root 的树和状态表。最小可用骨架如下：

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
GOAL-001-main-vision · <项目总目标> [active 0%]
```

| ID | 标题 | Parent | Status | Progress | 路径 |
|----|------|--------|--------|----------|------|
| GOAL-001-main-vision | <项目总目标> | — | active | 0% | GOAL-001-main-vision/ |
````

树和表必须与 Root `00-meta.md` 的 `id`、`parent`、`status`、`progress` 一致。后续新目标仍平铺在 `docs/goals/`，编号从当前最大编号递增。

## 4. 核对清单与证据记录

完成独立启用时，在执行记录或交付报告中留下以下事实：

1. **来源**：列出复制的 `AGENTS.md`、`docs/README.md`、`docs/architecture/`、`docs/templates/` 与 `docs/contracts/` 的来源路径和版本。
2. **生成路径**：列出目标仓库、`docs/goals/goal-tree.md`、Root 文件夹及五件套路径。
3. **核对结果**：确认 `git -C <target> rev-parse --is-inside-work-tree` 为 `true`，Root `parent: null`，`id` 与文件夹名一致，四个 Markdown 文件和 `attachments/` 均存在。
4. **边界**：确认没有依赖 `skills/` 或 `web/`；本验证不代表 Skills 安装或 Web 发布已经完成。

仓库内可重复运行的验证为：

```powershell
python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v
```

该测试每次在临时目录执行 `git init`，从当前 canonical 核心层复制材料，生成一个合规 Root，再在结束时清理临时目录。
