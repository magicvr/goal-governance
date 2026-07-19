---
title: Skills · 目标治理可复用包
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.9.0
---

# Skills

本目录提供可复制到**其他项目**的目标治理约定与模板。  
本仓库运行中的强制规则仍以根目录 [AGENTS.md](../AGENTS.md) 为准；此处是提炼后的**可复用交付物**。

Skills 是核心方法论与文档协议的消费适配器，不是独立真相源。在本仓库中，规范模板位于 [`docs/templates/goal-folder/`](../docs/templates/goal-folder/)；本包内的 `templates/goal-folder/` 是用于离线复制和安装脚本的同步镜像。消费适配器的机读版本/兼容声明以 [`docs/contracts/`](../docs/contracts/) 为 canonical，本包 `contracts/` 是逐字节分发镜像。安装到其他仓库后，镜像必须自包含可用。

**当前契约范围（D-003）**：Claude Code CLI 与 GitHub Copilot **VS Code** 插件为 `committed`；Grok Build CLI 为已纳入 manifest 的 `declared` 范围。三者当前都仍是 `unverified`：安装文件和官方发现语义不能替代固定产品版本的运行时验证。权威字段见 [`docs/contracts/skills-consumer-contract.json`](../docs/contracts/skills-consumer-contract.json)。

## 产品模型（必读）

| 层级 | 是什么 | 用户怎么用 |
|------|--------|------------|
| **主入口（primary）** | 编排器：扫描 / 意见台账 / 分类 / P-004 裁决 / 确认 / 原语 | **`/govern`** |
| **交叉入口** | 独立审计：只出意见（`source: independent`） | **`/audit`** |
| **原语（primitives）** | 创建目标、记决策、更执行、写审计 | 由编排器调用；Copilot advanced 可选 |
| **规则** | AGENTS / copilot-instructions | 结构、编号、P-001～P-005、goal-tree |

生命周期：**设立 → 信息发现与就绪判断 →（可审视）→ 方案 → 实施 → 审计/整改 → 关门**。
交叉意见由 `/audit` 写入；**响应与放行**由 `/govern` 处理。

| 工具 / 表面 | 安装位置 | 斜杠 | 当前契约层级 |
|------|----------|------|--------------|
| Claude Code CLI | `.claude/skills/govern/` + `audit/` | `/govern` · `/audit` | `committed / unverified` |
| Grok Build CLI | `.grok/skills/govern/` + `audit/` | `/govern` · `/audit` | `declared / unverified` |
| GitHub Copilot VS Code 插件 | `.github/prompts/govern.prompt.md` + `audit.prompt.md` | `/govern` · `/audit` | `committed / unverified` |

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
├── templates/goal-folder/              # docs/templates 的分发镜像
├── contracts/                          # docs/contracts 的分发镜像
└── tests/
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

**默认安装面**（与脚本一致）：每个所列安装产物都装 **`/govern` + `/audit`**。这描述可复制文件，不提升上表的声明/承诺层级或 `unverified` 运行时状态；填表类 advanced slash 仍为可选。

#### Claude Code

```text
install/claude/AGENTS.md
  →  <repo>/AGENTS.md
install/claude/skills/govern/SKILL.md
  →  <repo>/.claude/skills/govern/SKILL.md
install/claude/skills/audit/SKILL.md
  →  <repo>/.claude/skills/audit/SKILL.md
```

```bash
mkdir -p .claude/skills/govern .claude/skills/audit
cp ./skills/install/claude/AGENTS.md ./AGENTS.md
cp ./skills/install/claude/skills/govern/SKILL.md .claude/skills/govern/SKILL.md
cp ./skills/install/claude/skills/audit/SKILL.md .claude/skills/audit/SKILL.md
```

#### Grok Build

```text
install/grok/skills/govern/SKILL.md
  →  <repo>/.grok/skills/govern/SKILL.md
install/grok/skills/audit/SKILL.md
  →  <repo>/.grok/skills/audit/SKILL.md
```

（建议同时有根 `AGENTS.md` 作项目规则；可与 Claude 共用。）

```bash
mkdir -p .grok/skills/govern .grok/skills/audit
cp ./skills/install/grok/skills/govern/SKILL.md .grok/skills/govern/SKILL.md
cp ./skills/install/grok/skills/audit/SKILL.md .grok/skills/audit/SKILL.md
```

#### GitHub Copilot

```text
install/copilot/copilot-instructions.md
  →  .github/copilot-instructions.md
install/copilot/prompts/govern.md
  →  .github/prompts/govern.prompt.md
install/copilot/prompts/audit.md
  →  .github/prompts/audit.prompt.md
```

| Wrapper | 斜杠 | 何时安装 |
|---------|------|----------|
| govern.md | `/govern` | **默认**（主入口） |
| audit.md | `/audit` | **默认**（交叉审计） |
| new-goal … write-audit | advanced | 仅 `--with-primitives` |

### 2. 脚本安装

| 参数 | 作用 |
|------|------|
| `--claude` / `-Claude` | `AGENTS.md` + `.claude/skills/govern` + **`audit`**（`/govern` + `/audit`） |
| `--grok` / `-Grok` | `.grok/skills/govern` + **`audit`**（`/govern` + `/audit`） |
| `--copilot` / `-Copilot` | copilot-instructions + **默认双入口** `govern` + `audit` prompts |
| `--with-primitives` / `-WithPrimitives` | 可选：四个 advanced 填表 slash（new-goal 等） |
| `--all` / `-All` | Claude + Grok + Copilot + prompts/templates/contracts |
| `--skills-dir` / `-SkillsDir` | 默认 `./skills` |

```bash
bash ./skills/install.sh --all --skills-dir ./skills
bash ./skills/install.sh --claude --skills-dir ./skills
bash ./skills/install.sh --grok --skills-dir ./skills
bash ./skills/install.sh --copilot --skills-dir ./skills
```

```powershell
.\skills\install.ps1 -All -SkillsDir .\skills
.\skills\install.ps1 -Claude -SkillsDir .\skills
.\skills\install.ps1 -Grok -SkillsDir .\skills
.\skills\install.ps1 -Copilot -SkillsDir .\skills
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
| 信息就绪 | 可带未知立项；登记 I-00N、阶段门禁、证据与用户接受的残余风险 |
| 代码布局 | 普遍在仓库根；子目录仅项目自定 |
| 包目录名 | 常为 `skills/`，可改名；按含 `prompts/00-…` 定位 |

## 测试

```bash
# 结构契约 +（Windows）PowerShell 隔离安装冒烟（F-018）
python skills/tests/test_skills_orchestrator.py
```

```powershell
# 仅跑隔离安装冒烟（不经过 unittest）
powershell -NoProfile -ExecutionPolicy Bypass -File .\skills\tests\test_install_ps1_isolated.ps1
```

Windows 上 `test_install_ps1_isolated_all_produces_govern_and_audit` 会在临时目录执行 `install.ps1 -All`，断言默认产出 `/govern`+`/audit` 且不含填表 advanced slash。`install.sh` 的真实执行仍依赖 bash 环境（本仓库 Windows 主证据以 PS1 为准）。

## 尚未包含

- Marketplace 完整包  
- 编号 / parent 自动校验工具  

当前交付：**核心协议的 Skills 适配规则 + 编排主入口 `/govern` + 交叉入口 `/audit` + 文档原语 01～05 + 多宿主安装脚本 + 模板与机读契约分发镜像**。核心 canonical 方法论、模板与契约见仓库 `docs/` 层。
