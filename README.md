# Goal Governance

一个基于 FastAPI、Jinja2、Tailwind CSS 和 HTMX 的目标治理框架 Web 应用基础骨架。

当前应用包含三个核心模块：

- **Decision（决策）**：明确目标、权衡取舍并记录关键决策。
- **Execution（执行）**：将目标拆解为行动并持续跟踪进展。
- **Audit（审计）**：回顾过程与结果，沉淀可复用的经验。

当前版本仅提供页面与路由骨架，暂不包含数据库、认证或 AI 功能。

## 项目结构

```text
goal-governance/
├── .editorconfig
├── .gitignore
├── main.py
├── requirements.txt
├── README.md
├── static/
│   └── .gitkeep
└── templates/
    ├── base.html
    ├── index.html
    ├── decision.html
    ├── execution.html
    └── audit.html
```

## 环境要求

- Python 3.10+
- pip

## 安装

建议始终在本项目的 **Python 虚拟环境** 中安装依赖与启动服务，避免污染系统或其他项目的全局 Python 环境。

在项目根目录创建虚拟环境：

```bash
python -m venv .venv
```

激活虚拟环境：

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
source .venv/bin/activate
```

激活成功后，终端提示符前通常会显示 `(.venv)`。然后安装依赖：

```bash
pip install -r requirements.txt
```

## 启动

**请先激活本项目的虚拟环境**（见上方），再启动服务。这样会使用 `.venv` 内的 `uvicorn` 与依赖，不会干涉系统或其他环境。

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

macOS / Linux：

```bash
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

也可以不先 `activate`，直接用虚拟环境里的解释器启动（同样不会影响其他环境）：

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

macOS / Linux：

```bash
.venv/bin/python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

启动后访问：<http://127.0.0.1:8000>

也可以直接使用以下地址查看各模块页面：

- <http://127.0.0.1:8000/decision>
- <http://127.0.0.1:8000/execution>
- <http://127.0.0.1:8000/audit>

退出虚拟环境（可选）：

```bash
deactivate
```

## 技术说明

- FastAPI 路由使用 `async def`。
- Jinja2 模板通过 `base.html` 统一继承基础布局。
- Tailwind CSS 和 HTMX 当前通过 CDN 加载，不需要 Node.js 或构建工具。
- `static/` 已挂载到 `/static`，后续可以放置 CSS、JavaScript、图片和 favicon 等资源。
