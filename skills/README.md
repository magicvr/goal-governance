---
title: Skills · 目标治理可复用包
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.3.1
---

# Skills

本目录提供可复制到**其他项目**的目标治理约定与模板。  
本仓库运行中的强制规则仍以根目录 [AGENTS.md](../AGENTS.md) 为准；此处是提炼后的**可复用交付物**。

**支持的目标工具**：Claude Code、GitHub Copilot。

## 产品模型（必读）

| 层级 | 是什么 | 用户怎么用 |
|------|--------|------------|
| **主入口（primary）** | 编排器：扫描项目 / goal-tree → 分类情境 → 引导设立总目的 **或** 提议下一步并确认 → 调用原语 | 默认只走这一条：`00-govern-orchestrator` / Copilot **`/govern`** |
| **原语（primitives）** | 创建目标、记决策、更执行、写审计 | 由编排器调用；熟练用户可 advanced 直调 |
| **规则** | AGENTS / copilot-instructions | 结构、编号、P-001、goal-tree 同步 |

生命周期：**设立目标 → 推进目标 → 阶段性审计 / 关门审计**。  
**不是**「先选四张表再填」。

## 目录结构

```text
skills/
├── README.md                 # 本文件
├── AGENTS.template.md        # AI 助手规则模板
├── install.sh / install.ps1  # 可选安装脚本
├── install/
│   ├── claude/AGENTS.md
│   └── copilot/
│       ├── copilot-instructions.md
│       └── prompts/
│           ├── govern.md              # PRIMARY → /govern
│           ├── new-goal.md            # advanced
│           ├── log-decision.md        # advanced
│           ├── update-execution.md    # advanced
│           └── write-audit.md         # advanced
├── prompts/
│   ├── README.md
│   ├── 00-govern-orchestrator.md      # PRIMARY 核心提示词
│   ├── 01-create-new-goal.md          # primitive
│   ├── 02-record-decision.md          # primitive
│   ├── 03-update-execution.md         # primitive
│   └── 04-write-audit.md              # primitive
├── tests/
│   └── test_skills_orchestrator.py    # 结构与契约测试
└── templates/goal-folder/             # 五件套示例
```

## 安装

**支持工具**：GitHub Copilot、Claude Code。  
**提示词统一位置**：包内 [`prompts/`](prompts/)。

推荐：先把整个包复制进目标项目，再装规则文件。脚本可选（**离线**）。

### 0. 复制 skills 包

```bash
cp -R /path/to/goal-governance/skills ./skills
```

```powershell
Copy-Item -Recurse path\to\goal-governance\skills .\skills
```

### 1. 手动安装

#### Claude Code

```text
<skills-dir>/install/claude/AGENTS.md  →  <your-repo>/AGENTS.md
```

默认工作流：打开或粘贴 [`prompts/00-govern-orchestrator.md`](prompts/00-govern-orchestrator.md) 的「提示词正文」。

#### GitHub Copilot

```text
copilot-instructions.md → .github/copilot-instructions.md
**默认** slash：.github/prompts/govern.prompt.md  （仅 /govern）
```

| Wrapper | 斜杠 | 何时安装 | 核心提示词 |
|---------|------|----------|------------|
| [govern.md](install/copilot/prompts/govern.md) | **`/govern`** | **默认**（`--copilot` / `--all`） | [00-govern-orchestrator.md](prompts/00-govern-orchestrator.md) |
| new-goal.md | `/new-goal` | 仅 `--with-primitives` | 01-create-new-goal.md |
| log-decision.md | `/log-decision` | 仅 `--with-primitives` | 02-record-decision.md |
| update-execution.md | `/update-execution` | 仅 `--with-primitives` | 03-update-execution.md |
| write-audit.md | `/write-audit` | 仅 `--with-primitives` | 04-write-audit.md |

**默认不把四个填表 slash 装进用户菜单**，避免与「单一主入口」冲突。  
包内仍保留 advanced wrapper 源文件；`prompts/01`～`04` 原语始终在（编排器调用）。

手动示例（推荐）：

```bash
mkdir -p .github/prompts
cp ./skills/install/copilot/copilot-instructions.md .github/copilot-instructions.md
cp ./skills/install/copilot/prompts/govern.md .github/prompts/govern.prompt.md
# 一般不要复制下面四条；仅在明确需要 advanced 时再装
# cp ./skills/install/copilot/prompts/new-goal.md .github/prompts/new-goal.prompt.md
```

### 2. 脚本安装

| 参数 | 作用 |
|------|------|
| `--claude` / `-Claude` | `./AGENTS.md` |
| `--copilot` / `-Copilot` | copilot-instructions + **仅** `govern.prompt.md`（`/govern`） |
| `--with-primitives` / `-WithPrimitives` | **可选**：额外安装四个 advanced slash |
| `--all` / `-All` | 两者 + prompts/templates 到 `--skills-dir`（slash 仍默认仅 govern） |
| `--skills-dir` / `-SkillsDir` | 默认 `./skills` |

```bash
bash ./skills/install.sh --all --skills-dir ./skills
# 可选 advanced slash：
# bash ./skills/install.sh --copilot --with-primitives --skills-dir ./skills
```

```powershell
.\skills\install.ps1 -All -SkillsDir .\skills
# 可选 advanced slash：
# .\skills\install.ps1 -Copilot -WithPrimitives -SkillsDir .\skills
```

安装完成后：用户路径 **只有 `/govern`**（或粘贴 `00-govern-orchestrator`）。

## 在其他项目中快速启用

1. 安装规则 + 主入口（见上）。
2. 建立 `docs/goals/goal-tree.md`（可先空）。
3. 调用编排器：助手会扫描并引导第一个总目的，或分析未关门目标的下一步。
4. 不要手工猜编号流程——让编排器 / 原语遵守 AGENTS。

## 核心约定（摘要）

| 规则 | 说明 |
|------|------|
| 扁平存储 | 目标平铺在 `docs/goals/` |
| 编号 | `GOAL-001` 为 Root；之后顺序编号 |
| 层级 | 仅 `parent` 字段 |
| 总览 | 变更后必须更新 `goal-tree.md` |
| 五件套 | meta / decision / execution / audit / attachments |
| P-001 | 大目标先路线图，再按阶段拆子目标 |

## 与本仓库的关系

| 路径 | 角色 |
|------|------|
| 根 [AGENTS.md](../AGENTS.md) | 本仓库生效规则 |
| [skills/](.) | 可复用包 |
| [docs/goals/](../docs/goals/) | 真实目标数据 |
| [web/](../web/) | Web 应用（可选） |

## 测试

```bash
python skills/tests/test_skills_orchestrator.py
```

校验主入口与原语文件存在、编排器含生命周期/分类契约、安装脚本安装 `govern`。

## 尚未包含

- Marketplace 完整 Skill 包
- 编号 / parent / goal-tree 自动校验工具
- 独立 Agent 运行时

当前交付：**规则 + 单一编排主入口 + 文档原语 + 安装脚本 + 示例模板**（Claude Code、GitHub Copilot）。
