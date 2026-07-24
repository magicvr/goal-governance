# Goal Governance

目标治理框架：交付可复用的核心方法论、文档协议与模板，并提供面向 AI/仓库协作的 Skills 和面向人的 Web 工作台，贯通 **目标 → 决策 → 执行 → 审计**。

## 从这里开始

| 想了解… | 去读 |
|---------|------|
| 当前工作区目标与进展 | [docs/workspace-001-goal-governance/goal-tree.md](docs/workspace-001-goal-governance/goal-tree.md) |
| 文档怎么写、规则是什么 | [docs/README.md](docs/README.md) |
| 核心模板怎么用 | [docs/templates/README.md](docs/templates/README.md) |
| AI 必须遵守什么 | [AGENTS.md](AGENTS.md) |
| Skills 如何安装 | [skills/README.md](skills/README.md)（推荐：从 [Releases](https://github.com/magicvr/goal-governance/releases) 下载 skills-only zip） |
| Skills 如何打包 / 发布附件 | [docs/releases/README.md](docs/releases/README.md)、`scripts/pack_skills_release.py` |
| 技术栈与架构 | [docs/architecture/overview.md](docs/architecture/overview.md) |
| Web 如何启动 | [web/README.md](web/README.md) |

## 在其他项目中安装 Skills（Release zip）

其他仓库**不要**依赖 clone 整个 monorepo。从 GitHub Release 取 **skills-only** 安装包：

```powershell
# 1. 下载 goal-governance-skills-vX.Y.Z.zip（及可选 .sha256）到目标项目根
# 2. 解压并命名为 skills
Expand-Archive .\goal-governance-skills-vX.Y.Z.zip -DestinationPath .
Rename-Item .\goal-governance-skills-vX.Y.Z skills

# 3. 安装 /govern + /audit 到当前仓库（Claude / Grok / Copilot）
.\skills\install.ps1 -All -SkillsDir .\skills
```

```bash
unzip goal-governance-skills-vX.Y.Z.zip
mv goal-governance-skills-vX.Y.Z skills
bash ./skills/install.sh --all --skills-dir ./skills
```

**Windows 注意**：若执行 `.ps1` 报 `running scripts is disabled`，先在**当前窗口**放宽策略（仅本进程，不改系统默认），再重试：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

或不改策略、单次绕过：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\skills\install.ps1 -All -SkillsDir .\skills
```

详情、单宿主参数与工作区初始化见 [skills/README.md](skills/README.md)。  
维护者正式发版：annotated `v*` tag + Environment `release` 审批 + 严格 release-evidence（见 [docs/releases/README.md](docs/releases/README.md)）。本地调试：`python scripts/pack_skills_release.py --version X.Y.Z --output-dir dist/`。

## 仓库结构

```text
goal-governance/
├── README.md                 # 本文件
├── AGENTS.md                 # Agent / AI 协作强制规则
├── docs/                     # 目标与架构文档（source of truth）
│   ├── README.md
│   ├── workspace-001-goal-governance/ # 当前工作区：目标平铺 + goal-tree.md
│   ├── shared-materials/     # 工作区外的共享资料候选库存
│   ├── templates/            # 核心 canonical 文档模板
│   ├── contracts/            # 消费适配器的 canonical 机读兼容契约
│   ├── architecture/
│   └── _index/
├── skills/                   # AI/Agent 消费适配器与分发包
│   ├── prompts/
│   ├── templates/            # docs/templates 的分发镜像
│   ├── contracts/            # docs/contracts 的分发镜像
│   └── install.*
├── web/                      # FastAPI Web 应用
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── static/
│   └── templates/
├── .editorconfig
└── .gitignore
```

- **核心文档层**：`docs/README.md`、`docs/architecture/`、`docs/templates/` 与 `docs/contracts/` 定义方法论、协议、模板和消费适配器兼容契约；每个 `docs/workspace-<NNN>-<slug>/` 保存自身目标实例。
- **`skills/`**：AI/Agent 消费核心协议的编排、审计、原语、宿主适配和离线分发包。
- **`web/`**：FastAPI + Jinja2 + Tailwind CSS + HTMX 的人类工作台；当前直接读取唯一已配置的工作区根，提供只读浏览与文档树诊断，不维护独立状态，也不提供 Web 写入、创建/更新或后台同步入口。
- **三层交付共享一个真相源**：Skills 按协议读写、Web 当前读取同一工作区文档，不建立独立状态。

## 目标模型（摘要）

1. 目标全部平铺在各自 `docs/workspace-<NNN>-<slug>/` 根，不用嵌套文件夹表示层级。
2. 每个工作区的 `GOAL-001` 为总目标（Root Goal）；其后在工作区内顺序编号。
3. 层级写在每个目标 `00-meta.md` 的 `parent` 字段。
4. 树状与状态总览维护在当前工作区的 `goal-tree.md`。
5. 每个目标固定：`00-meta` / `01-decision` / `02-execution` / `03-audit` / `attachments/`。

当前目标：

- **GOAL-001-main-vision**：交付可复用的目标治理方法论、文档协议与消费工具
- **GOAL-002～007**：初始化、Skills 闭环、Goal 数据模型、核心方法论与信息就绪治理均已结项。
- **GOAL-008**：当前三宿主 `/govern` 的最低可用已验证；完整跨宿主/跨版本发布一致性保持 deferred required，在首次支持新宿主/版本或首次对外/可复现发布时复核。

## Web 应用快速启动

详细说明见 [web/README.md](web/README.md)。

```powershell
# 1. 在项目根目录创建/激活虚拟环境（首次）
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r web\requirements.txt

# 2. 启动（任选其一）
cd web
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# 或在根目录：
# uvicorn main:app --app-dir web --reload --host 127.0.0.1 --port 8000
```

若 `Activate.ps1` 因执行策略被拒，可先 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`，或改用 `.\.venv\Scripts\activate.bat`。

启动后访问：<http://127.0.0.1:8000>

## 当前 Web 模块

- **目标概览**：展示目标、状态、进度及目标树 / 文档诊断。
- **目标详情**：展示成功标准、附件、Decision、Execution 和 Audit 的基础信息，并在需要时回退到原始 Markdown。
- **兼容入口**：`/decision`、`/execution`、`/audit` 会跳回目标工作台。

当前 Web 是读取运行中工作区目标文档的只读工作台，而非仅有页面与路由骨架。它直接以 `docs/workspace-001-goal-governance/` 为当前真相源，不使用独立数据库或第二状态层，因此没有需要与目标文件“同步”的副本；当前也不提供 Web 写入、创建/更新或写入同步。任何写入能力须由独立目标实现，并遵守同一文档协议与审计约束。
