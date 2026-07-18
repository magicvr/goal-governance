# Goal Governance Web

基于 FastAPI、Jinja2、Tailwind CSS 和 HTMX 的目标治理 Web 应用。

当前版本提供页面与路由骨架，包含三个模块：

- **Decision（决策）**
- **Execution（执行）**
- **Audit（审计）**

## 目录结构

```text
web/
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

建议在**项目根目录**维护虚拟环境（`.venv`），在 `web/` 下运行应用。

## 安装

在项目根目录创建并激活虚拟环境：

```bash
# 在项目根目录 goal-governance/ 下执行
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r web\requirements.txt
```

macOS / Linux：

```bash
source .venv/bin/activate
pip install -r web/requirements.txt
```

## 启动

### 方式一：进入 web/ 后启动（推荐）

Windows PowerShell：

```powershell
# 在项目根目录
.\.venv\Scripts\Activate.ps1
cd web
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

macOS / Linux：

```bash
source .venv/bin/activate
cd web
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 方式二：在项目根目录启动

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --app-dir web --reload --host 127.0.0.1 --port 8000
```

macOS / Linux：

```bash
source .venv/bin/activate
uvicorn main:app --app-dir web --reload --host 127.0.0.1 --port 8000
```

### 方式三：不 activate，直接用虚拟环境解释器

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir web --reload --host 127.0.0.1 --port 8000
```

macOS / Linux：

```bash
.venv/bin/python -m uvicorn main:app --app-dir web --reload --host 127.0.0.1 --port 8000
```

启动后访问：<http://127.0.0.1:8000>

模块页面：

- <http://127.0.0.1:8000/decision>
- <http://127.0.0.1:8000/execution>
- <http://127.0.0.1:8000/audit>

## 测试

从 `web/` 目录使用项目虚拟环境运行：

```powershell
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

macOS / Linux：

```bash
../.venv/bin/python -m unittest discover -s tests -v
```

## 技术说明

- `main.py` 通过 `Path(__file__).resolve().parent` 定位 `static/` 与 `templates/`，可在任意工作目录启动。
- Tailwind CSS 和 HTMX 当前通过 CDN 加载。
- `static/` 已挂载到 `/static`。
- `services/goals_repo.py` 已提供目标的 List/Get/Create/Update 与 `repair_goal_tree()`；Web 路由接入留待目标详情与首页阶段。
