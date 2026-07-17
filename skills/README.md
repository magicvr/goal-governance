---
title: Skills · 目标治理可复用包
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.2.0
---

# Skills

本目录提供可复制到**其他项目**的目标治理约定与模板。  
本仓库运行中的强制规则仍以根目录 [AGENTS.md](../AGENTS.md) 为准；此处是提炼后的**可复用交付物**。

**支持的目标工具**：Claude Code、GitHub Copilot。

## 目录结构

```text
skills/
├── README.md                 # 本文件：如何在其他项目中使用
├── AGENTS.template.md        # AI 助手规则模板（可编辑源）
├── install.sh                # 可选：Bash 安装脚本
├── install.ps1               # 可选：PowerShell 安装脚本
├── install/
│   ├── claude/
│   │   └── AGENTS.md         # Claude Code 安装用规则
│   └── copilot/
│       └── copilot-instructions.md  # GitHub Copilot 安装用规则
├── prompts/                  # 可复制的常用提示词模板
│   ├── README.md
│   ├── 01-create-new-goal.md
│   ├── 02-record-decision.md
│   ├── 03-update-execution.md
│   └── 04-write-audit.md
└── templates/
    └── goal-folder/          # 单个目标文件夹模板（含虚构示例，复制后改写）
        ├── 00-meta.md
        ├── 01-decision.md
        ├── 02-execution.md
        ├── 03-audit.md
        └── attachments/
```

## 安装

推荐**手动安装**（透明、可审计）；脚本为可选快捷方式。  
无论哪种方式，都请先 `cd` 到**目标项目根目录**。

### 1. 手动安装（推荐）

#### Claude Code

将 Claude 规则复制到目标项目根目录，文件名为 `AGENTS.md`：

```text
skills/install/claude/AGENTS.md  →  <your-repo>/AGENTS.md
```

示例（在目标项目根执行，路径按本仓库实际位置调整）：

```bash
# Bash
cp /path/to/goal-governance/skills/install/claude/AGENTS.md ./AGENTS.md
```

```powershell
# PowerShell
Copy-Item path\to\goal-governance\skills\install\claude\AGENTS.md .\AGENTS.md
```

也可从可编辑源 [AGENTS.template.md](AGENTS.template.md) 复制后自行适配（替换 `{{...}}` 占位符）。

#### GitHub Copilot

将 Copilot 规则复制到 `.github/copilot-instructions.md`：

```text
skills/install/copilot/copilot-instructions.md  →  <your-repo>/.github/copilot-instructions.md
```

示例：

```bash
# Bash
mkdir -p .github
cp /path/to/goal-governance/skills/install/copilot/copilot-instructions.md .github/copilot-instructions.md
```

```powershell
# PowerShell
New-Item -ItemType Directory -Force -Path .github | Out-Null
Copy-Item path\to\goal-governance\skills\install\copilot\copilot-instructions.md .github\copilot-instructions.md
```

#### 可选：一并复制 prompts/ 与 templates/

```text
skills/prompts/     →  <your-repo>/skills/prompts/
skills/templates/   →  <your-repo>/skills/templates/
```

用于常用提示词与「目标五件套」文件夹模板。复制后可按项目改路径与示例内容。

### 2. 脚本安装（可选）

提供 [install.sh](install.sh)（Bash）与 [install.ps1](install.ps1)（PowerShell）。  
在目标项目根目录执行；脚本从 `skills/` 包内复制文件，**不联网**。

| 参数 | 作用 |
|------|------|
| `--claude` / `-Claude` | 仅安装 Claude Code：`AGENTS.md` |
| `--copilot` / `-Copilot` | 仅安装 Copilot：`.github/copilot-instructions.md` |
| `--all` / `-All` | 安装两者，并复制 `prompts/` 与 `templates/` 到 `skills/` |
| `--help` / `-Help` | 显示帮助 |

基本用法：

```bash
# Bash：进入目标项目根，再指向本仓库的脚本
cd /path/to/your-project
bash /path/to/goal-governance/skills/install.sh --claude
bash /path/to/goal-governance/skills/install.sh --copilot
bash /path/to/goal-governance/skills/install.sh --all
```

```powershell
# PowerShell
cd C:\path\to\your-project
& C:\path\to\goal-governance\skills\install.ps1 -Claude
& C:\path\to\goal-governance\skills\install.ps1 -Copilot
& C:\path\to\goal-governance\skills\install.ps1 -All
```

- 目标文件已存在时会询问是否覆盖。
- 源文件缺失时会报错并退出。
- 安装完成后按终端提示检查规则文件并建立 `docs/goals/`。

## 在其他项目中快速启用

### 1. 安装规则文件

见上方「安装」：Claude Code → 根目录 `AGENTS.md`；GitHub Copilot → `.github/copilot-instructions.md`。  
按项目实际情况调整路径与可选节。

### 2. 建立文档骨架

```text
docs/
├── README.md                 # 可参考本仓库 docs/README.md
├── goals/
│   └── goal-tree.md          # 先建空总览，再加目标
└── architecture/             # 可选
```

### 3. 创建第一个目标（Root Goal）

复制模板文件夹并重命名：

```text
skills/templates/goal-folder/
  → docs/goals/GOAL-001-main-vision/
```

然后：

1. 填写 `00-meta.md`：`id`、`title`，`parent: null`
2. 补全决策 / 执行 / 审计初稿（可简短）
3. 在 `docs/goals/goal-tree.md` 登记该目标

### 4. 后续目标

1. 查看 `goal-tree.md` 取下一个编号（如 `GOAL-002`）
2. 再复制一份 `goal-folder` → `docs/goals/GOAL-NNN-short-slug/`
3. 设置 `parent` 为父目标 ID
4. **同步更新** `goal-tree.md`

## 核心约定（摘要）

| 规则 | 说明 |
|------|------|
| 扁平存储 | 所有目标平铺在 `docs/goals/`，不用嵌套文件夹表示层级 |
| 编号 | `GOAL-001` 为 Root；之后顺序编号 |
| 层级 | 仅用 `00-meta.md` 的 `parent` 字段 |
| 总览 | 变更后必须更新 `goal-tree.md` |
| 五件套 | meta / decision / execution / audit / attachments |

完整条文见 [AGENTS.template.md](AGENTS.template.md)，或安装产物 [install/claude/AGENTS.md](install/claude/AGENTS.md) / [install/copilot/copilot-instructions.md](install/copilot/copilot-instructions.md)。

## 与本仓库的关系

| 路径 | 角色 |
|------|------|
| 根 [AGENTS.md](../AGENTS.md) | 本仓库生效的 AI 规则 |
| [skills/AGENTS.template.md](AGENTS.template.md) | 对外可复用的可编辑模板 |
| [skills/install/](install/) | 按工具适配的安装用规则 |
| [docs/goals/](../docs/goals/) | 本仓库真实目标数据 |
| [web/](../web/) | 本仓库 Web 应用（其他项目可选） |

## 提示词模板

日常操作可直接复制 [prompts/](prompts/) 中的提示词给 AI 使用：

| 文件 | 用途 |
|------|------|
| [01-create-new-goal.md](prompts/01-create-new-goal.md) | 创建新目标（五件套 + goal-tree） |
| [02-record-decision.md](prompts/02-record-decision.md) | 记录决策（决定了什么 / 为什么） |
| [03-update-execution.md](prompts/03-update-execution.md) | 更新执行时间线与进度 |
| [04-write-audit.md](prompts/04-write-audit.md) | 阶段性复盘 |

用法详见 [prompts/README.md](prompts/README.md)。

## 尚未包含（后续可扩展）

- 完整 VS Code / Copilot Marketplace Skill 包
- 编号 / parent / goal-tree 一致性校验工具

当前交付定位：**可复制的规则 + 安装脚本 + 提示词 + 含示例的目标文件夹模板**（工具：Claude Code、GitHub Copilot）。
