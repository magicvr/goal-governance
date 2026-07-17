# Goal Governance

目标治理框架：文档驱动的目标/决策/执行/审计体系，以及配套的 Web 应用骨架。

## 仓库结构

```text
goal-governance/
├── README.md                 # 本文件（项目级说明）
├── AGENTS.md                 # Agent / 协作约定（如有）
├── docs/                     # 目标、架构等文档（独立演进）
├── web/                      # FastAPI Web 应用
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── static/
│   └── templates/
├── .editorconfig
├── .gitignore
└── ...
```

- **`docs/`**：项目文档与目标治理内容，暂与 Web 应用解耦。
- **`web/`**：基于 FastAPI、Jinja2、Tailwind CSS 和 HTMX 的 Web 应用。

## Web 应用快速启动

详细说明见 [web/README.md](web/README.md)。

```powershell
# 1. 在项目根目录创建/激活虚拟环境（首次）
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r web\requirements.txt

# 2. 启动（任选其一）
# 推荐：进入 web 目录
cd web
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# 或在根目录指定 app-dir
# uvicorn main:app --app-dir web --reload --host 127.0.0.1 --port 8000
```

启动后访问：<http://127.0.0.1:8000>

## 当前 Web 模块

- **Decision（决策）**：明确目标、权衡取舍并记录关键决策。
- **Execution（执行）**：将目标拆解为行动并持续跟踪进展。
- **Audit（审计）**：回顾过程与结果，沉淀可复用的经验。

当前版本仅提供页面与路由骨架，暂不包含数据库、认证或 AI 功能。
