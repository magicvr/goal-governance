---
title: Skills · 目标治理可复用包
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.2.2
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
│       ├── copilot-instructions.md  # GitHub Copilot 安装用规则
│       └── prompts/          # Copilot 斜杠命令 wrapper（轻量入口）
│           ├── new-goal.md
│           ├── log-decision.md
│           ├── update-execution.md
│           └── write-audit.md
├── prompts/                  # 核心提示词（唯一真相；修改此处全局生效）
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

**支持工具**：GitHub Copilot、Claude Code。  
**提示词统一位置**：包内 [`prompts/`](prompts/)（安装后位于你选择的 skills 目录下）。

推荐流程：先把整个包复制进目标项目，再装规则文件。  
手动安装透明可审计；[install.sh](install.sh) / [install.ps1](install.ps1) 为可选快捷方式（**离线**）。

### 0. 准备：复制 skills 包到目标项目

在目标项目**根目录**执行（路径按本仓库实际位置调整）：

```bash
# Bash：整包复制（目录名可改）
cp -R /path/to/goal-governance/skills ./skills
# 或改名：
# cp -R /path/to/goal-governance/skills ./my-governance-skills
```

```powershell
# PowerShell
Copy-Item -Recurse path\to\goal-governance\skills .\skills
# 或改名：
# Copy-Item -Recurse path\to\goal-governance\skills .\my-governance-skills
```

说明：

- 复制后，提示词在 `./skills/prompts/`（或你改名后的 `./my-governance-skills/prompts/`）。
- 后续步骤中的「skills 目录」= 你复制后的一级目录；脚本参数 `--skills-dir` / `-SkillsDir` 默认 `./skills`。
- 无论手动还是脚本，请先 `cd` 到**目标项目根目录**。

### 1. 手动安装（推荐）

#### Claude Code

```text
<skills-dir>/install/claude/AGENTS.md  →  <your-repo>/AGENTS.md
```

```bash
# Bash（在目标项目根；skills 目录名按实际修改）
cp ./skills/install/claude/AGENTS.md ./AGENTS.md
```

```powershell
# PowerShell
Copy-Item .\skills\install\claude\AGENTS.md .\AGENTS.md
```

也可从可编辑源 [AGENTS.template.md](AGENTS.template.md) 复制后自行适配（替换 `{{...}}` 占位符）。

#### GitHub Copilot

`.github/` **必须**建在目标项目根目录：

```text
<skills-dir>/install/copilot/copilot-instructions.md
  →  <your-repo>/.github/copilot-instructions.md
```

```bash
# Bash
mkdir -p .github
cp ./skills/install/copilot/copilot-instructions.md .github/copilot-instructions.md
```

```powershell
# PowerShell
New-Item -ItemType Directory -Force -Path .github | Out-Null
Copy-Item .\skills\install\copilot\copilot-instructions.md .github\copilot-instructions.md
```

##### Copilot 斜杠命令 wrapper（可选）

位置：[install/copilot/prompts/](install/copilot/prompts/)。这是**轻量交互入口**，核心逻辑仍在 [prompts/](prompts/)。

| Wrapper 文件 | 斜杠命令 | 对应核心提示词 |
|--------------|----------|----------------|
| [new-goal.md](install/copilot/prompts/new-goal.md) | `/new-goal` | [01-create-new-goal.md](prompts/01-create-new-goal.md) |
| [log-decision.md](install/copilot/prompts/log-decision.md) | `/log-decision` | [02-record-decision.md](prompts/02-record-decision.md) |
| [update-execution.md](install/copilot/prompts/update-execution.md) | `/update-execution` | [03-update-execution.md](prompts/03-update-execution.md) |
| [write-audit.md](install/copilot/prompts/write-audit.md) | `/write-audit` | [04-write-audit.md](prompts/04-write-audit.md) |

启用方式（在目标项目根）：

1. 确保已安装 `copilot-instructions.md`，且整包中有 `skills/prompts/`（或你改名后的 skills 目录）。
2. 将 wrapper 复制到 `.github/prompts/`。VS Code / Visual Studio 的自定义 prompt 通常要求 **`.prompt.md` 后缀**，例如：

```bash
# Bash
mkdir -p .github/prompts
cp ./skills/install/copilot/prompts/new-goal.md .github/prompts/new-goal.prompt.md
cp ./skills/install/copilot/prompts/log-decision.md .github/prompts/log-decision.prompt.md
cp ./skills/install/copilot/prompts/update-execution.md .github/prompts/update-execution.prompt.md
cp ./skills/install/copilot/prompts/write-audit.md .github/prompts/write-audit.prompt.md
```

```powershell
# PowerShell
New-Item -ItemType Directory -Force -Path .github\prompts | Out-Null
Copy-Item .\skills\install\copilot\prompts\new-goal.md .github\prompts\new-goal.prompt.md
Copy-Item .\skills\install\copilot\prompts\log-decision.md .github\prompts\log-decision.prompt.md
Copy-Item .\skills\install\copilot\prompts\update-execution.md .github\prompts\update-execution.prompt.md
Copy-Item .\skills\install\copilot\prompts\write-audit.md .github\prompts\write-audit.prompt.md
```

3. 在 Copilot Chat 输入 `/`，选择 `/new-goal`、`/log-decision` 等；或通过 `#prompt:` 引用 prompt 文件。
4. Wrapper 会先引导你补齐参数，再要求 AI 阅读并执行 `./skills/prompts/` 下对应核心提示词。

**维护约定**：只改 [skills/prompts/](prompts/) 核心文件即可全局生效；wrapper 仅收集参数与引用路径，勿在 wrapper 中复制整份核心正文。

#### 提示词与目标模板

整包复制后，以下路径已在项目内，无需再拷：

```text
<skills-dir>/prompts/      # 01 新目标 / 02 决策 / 03 执行 / 04 复盘
<skills-dir>/templates/    # goal-folder 五件套示例
```

若只从本仓库零散拷贝，请保证提示词仍落在同一 skills 目录下，便于统一引用。

### 2. 脚本安装（可选）

在**目标项目根**执行；源文件读自**脚本所在包**；规则写入**当前工作目录**；`prompts/` 与 `templates/` 写入 `--skills-dir`。

| 参数 | 作用 |
|------|------|
| `--claude` / `-Claude` | 安装 Claude Code：`./AGENTS.md` |
| `--copilot` / `-Copilot` | 安装 Copilot：`./.github/copilot-instructions.md`（自动创建 `.github/`） |
| `--all` / `-All` | 安装两者，并把 `prompts/`、`templates/` 放到 `--skills-dir` |
| `--skills-dir DIR` / `-SkillsDir DIR` | skills 目录（默认 `./skills`；相对路径相对项目根） |
| `--help` / `-Help` | 显示帮助 |

```bash
# Bash
cd /path/to/your-project

# 已复制为 ./skills
bash ./skills/install.sh --copilot --skills-dir ./skills
bash ./skills/install.sh --claude --skills-dir ./skills
bash ./skills/install.sh --all --skills-dir ./skills

# 已改名为 my-governance-skills
bash ./my-governance-skills/install.sh --all --skills-dir ./my-governance-skills

# 也可直接指向本仓库包（无需先复制整包；--all 会把 prompts/templates 写入 --skills-dir）
bash /path/to/goal-governance/skills/install.sh --all --skills-dir ./skills
```

```powershell
# PowerShell
cd C:\path\to\your-project

# 已复制为 .\skills
.\skills\install.ps1 -Copilot -SkillsDir .\skills
.\skills\install.ps1 -Claude -SkillsDir .\skills
.\skills\install.ps1 -All -SkillsDir .\skills

# 已改名
.\my-governance-skills\install.ps1 -All -SkillsDir .\my-governance-skills

# 直接指向本仓库包
& C:\path\to\goal-governance\skills\install.ps1 -All -SkillsDir .\skills
```

安全与行为：

- 目标文件/目录已存在时会询问是否覆盖；源文件缺失则报错退出。
- 若 `--skills-dir` 与脚本包内 `prompts/` 为同一路径（整包复制后的常见情况），脚本会提示 **Already present**，不重复覆盖。
- 安装完成后按终端提示检查规则文件，并建立 `docs/goals/`。

## 在其他项目中快速启用

### 1. 安装规则文件

见上方「安装」：先复制整包（可改名），再装 Claude Code → 根目录 `AGENTS.md`，或 GitHub Copilot → `.github/copilot-instructions.md`。  
提示词使用包内 `prompts/`。按项目实际情况调整路径与可选节。

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

日常操作可直接复制 [prompts/](prompts/) 中的**核心提示词**给 AI 使用：

| 文件 | 用途 |
|------|------|
| [01-create-new-goal.md](prompts/01-create-new-goal.md) | 创建新目标（五件套 + goal-tree） |
| [02-record-decision.md](prompts/02-record-decision.md) | 记录决策（决定了什么 / 为什么） |
| [03-update-execution.md](prompts/03-update-execution.md) | 更新执行时间线与进度 |
| [04-write-audit.md](prompts/04-write-audit.md) | 阶段性复盘 |

用法详见 [prompts/README.md](prompts/README.md)。

GitHub Copilot 还可使用 [install/copilot/prompts/](install/copilot/prompts/) 下的斜杠命令 wrapper（见上方「安装 → GitHub Copilot」），减少每次复制粘贴。

## 尚未包含（后续可扩展）

- 完整 VS Code / Copilot Marketplace Skill 包
- 编号 / parent / goal-tree 一致性校验工具

当前交付定位：**可复制的规则 + 安装脚本 + 提示词 + 含示例的目标文件夹模板**（工具：Claude Code、GitHub Copilot）。
