# Goal Governance

目标治理框架：交付可复用的核心方法论、文档协议与模板，并提供面向 AI/仓库协作的 Skills 和面向人的 Web 工作台，贯通 **目标 → 决策 → 执行 → 审计**。

## 从这里开始

| 想了解… | 去读 |
|---------|------|
| 全局目标与进展 | [docs/goals/goal-tree.md](docs/goals/goal-tree.md) |
| 文档怎么写、规则是什么 | [docs/README.md](docs/README.md) |
| 核心模板怎么用 | [docs/templates/README.md](docs/templates/README.md) |
| AI 必须遵守什么 | [AGENTS.md](AGENTS.md) |
| Skills 如何安装 | [skills/README.md](skills/README.md) |
| 技术栈与架构 | [docs/architecture/overview.md](docs/architecture/overview.md) |
| Web 如何启动 | [web/README.md](web/README.md) |

## 仓库结构

```text
goal-governance/
├── README.md                 # 本文件
├── AGENTS.md                 # Agent / AI 协作强制规则
├── docs/                     # 目标与架构文档（source of truth）
│   ├── README.md
│   ├── goals/                # 目标平铺 + goal-tree.md
│   ├── templates/            # 核心 canonical 文档模板
│   ├── architecture/
│   └── _index/
├── skills/                   # AI/Agent 消费适配器与分发包
│   ├── prompts/
│   ├── templates/            # docs/templates 的分发镜像
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

- **核心文档层**：`docs/README.md`、`docs/architecture/` 与 `docs/templates/` 定义方法论、协议和模板；`docs/goals/` 保存具体目标实例。
- **`skills/`**：AI/Agent 消费核心协议的编排、审计、原语、宿主适配和离线分发包。
- **`web/`**：FastAPI + Jinja2 + Tailwind CSS + HTMX 的人类工作台；当前直接读取 `docs/goals/`，提供只读浏览与文档树诊断，不维护独立状态，也不提供 Web 写入、创建/更新或后台同步入口。
- **三层交付共享一个真相源**：Skills 按协议读写、Web 当前读取同一套 `docs/goals` 文档，不建立独立状态。

## 目标模型（摘要）

1. 目标全部平铺在 `docs/goals/`，不用嵌套文件夹表示层级。
2. `GOAL-001` 为总目标（Root Goal）；其后顺序编号。
3. 层级写在每个目标 `00-meta.md` 的 `parent` 字段。
4. 树状与状态总览维护在 `docs/goals/goal-tree.md`。
5. 每个目标固定：`00-meta` / `01-decision` / `02-execution` / `03-audit` / `attachments/`。

当前目标：

- **GOAL-001-main-vision**：交付可复用的目标治理方法论、文档协议与消费工具
- **GOAL-002～005**：初始化、Skills 闭环、Goal 数据模型与 Web 只读基线均已结项；下一阶段按路线图从 `GOAL-006` 起立项

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

启动后访问：<http://127.0.0.1:8000>

## 当前 Web 模块

- **目标概览**：展示目标、状态、进度及目标树 / 文档诊断。
- **目标详情**：展示成功标准、附件、Decision、Execution 和 Audit 的基础信息，并在需要时回退到原始 Markdown。
- **兼容入口**：`/decision`、`/execution`、`/audit` 会跳回目标工作台。

当前 Web 是读取运行中目标文档的只读工作台，而非仅有页面与路由骨架。它直接以 `docs/goals/` 为真相源，不使用独立数据库或第二状态层，因此没有需要与目标文件“同步”的副本；当前也不提供 Web 写入、创建/更新或写入同步。任何写入能力须由独立目标实现，并遵守同一文档协议与审计约束。
