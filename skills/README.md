---
title: Skills · 目标治理可复用包
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.5.0
---

# Skills

本目录提供可复制到**其他项目**的目标治理约定与模板。  
本仓库运行中的强制规则仍以根目录 [AGENTS.md](../AGENTS.md) 为准；此处是提炼后的**可复用交付物**。

**支持的目标工具**：Claude Code、Grok Build、GitHub Copilot。

## 产品模型（必读）

| 层级 | 是什么 | 用户怎么用 |
|------|--------|------------|
| **主入口（primary）** | 编排器：扫描 / 意见台账 / 分类 / P-004 裁决 / 确认 / 原语 | **`/govern`** |
| **交叉入口** | 独立审计：只出意见（`source: independent`） | **`/audit`** |
| **原语（primitives）** | 创建目标、记决策、更执行、写审计 | 由编排器调用；Copilot advanced 可选 |
| **规则** | AGENTS / copilot-instructions | 结构、编号、P-001～P-004、goal-tree |

生命周期：**设立 →（可审视）→ 方案 → 实施 → 审计/整改 → 关门**。  
交叉意见由 `/audit` 写入；**响应与放行**由 `/govern` 处理。

| 工具 | 安装位置 | 斜杠 |
|------|----------|------|
| Claude Code | `.claude/skills/govern/` + `audit/` | `/govern` · `/audit` |
| Grok Build | `.grok/skills/govern/` + `audit/` | `/govern` · `/audit` |
| GitHub Copilot | `.github/prompts/govern.prompt.md` + `audit.prompt.md` | `/govern` · `/audit` |

核心行为：

- 编排：[`prompts/00-govern-orchestrator.md`](prompts/00-govern-orchestrator.md)
- 交叉：[`prompts/05-independent-audit.md`](prompts/05-independent-audit.md)

## 目录结构

```text
skills/
├── README.md
├── AGENTS.template.md
├── install.sh / install.ps1
├── install/
│   ├── claude/
│   │   ├── AGENTS.md
│   │   └── skills/{govern,audit}/SKILL.md
│   ├── grok/
│   │   └── skills/{govern,audit}/SKILL.md
│   └── copilot/
│       ├── copilot-instructions.md
│       └── prompts/
│           ├── govern.md               # primary
│           ├── audit.md                # cross-audit (default install)
│           └── new-goal.md …           # advanced only
├── prompts/
│   ├── 00-govern-orchestrator.md       # PRIMARY core
│   ├── 01–04 …                         # primitives
│   └── 05-independent-audit.md         # cross-audit core
├── tests/
└── templates/goal-folder/
```

## 安装

推荐：先整包复制进目标项目，再装规则与主入口。脚本**离线**。

### 0. 复制包

```bash
cp -R /path/to/goal-governance/skills ./skills
```

```powershell
Copy-Item -Recurse path\to\goal-governance\skills .\skills
```

### 1. 手动安装

#### Claude Code

```text
install/claude/AGENTS.md
  →  <repo>/AGENTS.md
install/claude/skills/govern/SKILL.md
  →  <repo>/.claude/skills/govern/SKILL.md
```

```bash
mkdir -p .claude/skills/govern
cp ./skills/install/claude/AGENTS.md ./AGENTS.md
cp ./skills/install/claude/skills/govern/SKILL.md .claude/skills/govern/SKILL.md
```

#### Grok Build

```text
install/grok/skills/govern/SKILL.md
  →  <repo>/.grok/skills/govern/SKILL.md
```

（建议同时有根 `AGENTS.md` 作项目规则；可与 Claude 共用。）

```bash
mkdir -p .grok/skills/govern
cp ./skills/install/grok/skills/govern/SKILL.md .grok/skills/govern/SKILL.md
```

#### GitHub Copilot

```text
copilot-instructions.md → .github/copilot-instructions.md
**默认** slash：.github/prompts/govern.prompt.md
```

| Wrapper | 斜杠 | 何时安装 |
|---------|------|----------|
| govern.md | `/govern` | **默认**（主入口） |
| audit.md | `/audit` | **默认**（交叉审计） |
| new-goal … write-audit | advanced | 仅 `--with-primitives` |

### 2. 脚本安装

| 参数 | 作用 |
|------|------|
| `--claude` / `-Claude` | `AGENTS.md` + `.claude/skills/govern/SKILL.md` |
| `--grok` / `-Grok` | `.grok/skills/govern/SKILL.md` |
| `--copilot` / `-Copilot` | copilot-instructions + **仅** govern prompt |
| `--with-primitives` / `-WithPrimitives` | 可选：四个 advanced Copilot slash |
| `--all` / `-All` | Claude + Grok + Copilot + prompts/templates |
| `--skills-dir` / `-SkillsDir` | 默认 `./skills` |

```bash
bash ./skills/install.sh --all --skills-dir ./skills
bash ./skills/install.sh --claude --skills-dir ./skills
bash ./skills/install.sh --grok --skills-dir ./skills
```

```powershell
.\skills\install.ps1 -All -SkillsDir .\skills
.\skills\install.ps1 -Claude -SkillsDir .\skills
.\skills\install.ps1 -Grok -SkillsDir .\skills
```

安装后：使用 **`/govern`** 推进；需要交叉审计时用 **`/audit`**，再用 `/govern` 响应意见。

## 在其他项目中快速启用

1. 安装规则 + `/govern` + `/audit` skill（见上）。  
2. 建立 `docs/goals/goal-tree.md`（可先空）。  
3. 调用 `/govern`：扫描并引导总目的，或分析未关门目标的下一步。  
4. 调用 `/audit`：对指定目标写独立审计意见（不改 status）。

## 核心约定（摘要）

| 规则 | 说明 |
|------|------|
| 扁平存储 | 目标平铺在 `docs/goals/`（本包约定） |
| 编号 | `GOAL-001` 为 Root；slug 自定 |
| 层级 | 仅 `parent` 字段 |
| 总览 | 变更后更新 `goal-tree.md` |
| 五件套 | meta / decision / execution / audit / attachments |
| 代码布局 | 普遍在仓库根；子目录仅项目自定 |
| 包目录名 | 常为 `skills/`，可改名；按含 `prompts/00-…` 定位 |

## 测试

```bash
python skills/tests/test_skills_orchestrator.py
```

## 尚未包含

- Marketplace 完整包  
- 编号 / parent 自动校验工具  

当前交付：**规则 + 编排主入口 `/govern` + 交叉入口 `/audit` + 文档原语 01～05 + 安装脚本 + 示例模板**。
