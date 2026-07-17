# Goal Governance

目标治理框架：以文档为真相来源，贯通 **目标 → 决策 → 执行 → 审计**，并配套 Web 应用与 AI Skills/提示词双交付。

## 从这里开始

| 想了解… | 去读 |
|---------|------|
| 全局目标与进展 | [docs/goals/goal-tree.md](docs/goals/goal-tree.md) |
| 文档怎么写、规则是什么 | [docs/README.md](docs/README.md) |
| AI 必须遵守什么 | [AGENTS.md](AGENTS.md) |
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
│   ├── architecture/
│   └── _index/
├── web/                      # FastAPI Web 应用
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── static/
│   └── templates/
├── .editorconfig
└── .gitignore
```

- **`docs/`**：目标治理内容与规范，独立演进。
- **`web/`**：FastAPI + Jinja2 + Tailwind CSS + HTMX 的 Web 应用。
- **双交付**：Web 应用（看与操作）+ Skills/提示词（写与推进），共享同一套 `docs/goals`。

## 目标模型（摘要）

1. 目标全部平铺在 `docs/goals/`，不用嵌套文件夹表示层级。
2. `GOAL-001` 为总目标（Root Goal）；其后顺序编号。
3. 层级写在每个目标 `00-meta.md` 的 `parent` 字段。
4. 树状与状态总览维护在 `docs/goals/goal-tree.md`。
5. 每个目标固定：`00-meta` / `01-decision` / `02-execution` / `03-audit` / `attachments/`。

当前目标：

- **GOAL-001-main-vision**：构建实用的目标治理框架  
- **GOAL-002-project-bootstrap**：项目初始化（约 70%，进行中）

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

- **Decision（决策）**
- **Execution（执行）**
- **Audit（审计）**

当前版本为页面与路由骨架，暂不包含数据库、认证或目标文件自动同步。
