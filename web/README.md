# Goal Governance Web

基于 FastAPI、Jinja2、Tailwind CSS 和 HTMX 的目标治理 Web 应用。它是核心方法论与文档协议的**人类消费适配器**，不拥有独立的目标状态或生命周期定义。

当前版本提供只读的目标工作台，直接从仓库 `docs/goals/` 的 Markdown 真相源加载数据：

- **目标概览**：展示可读取 Goal、状态、进度和文档/目标树诊断。
- **目标详情**：展示成功标准、附件、Decision、Execution 和 Audit 的基础信息与原始 Markdown 回退内容。
- **兼容入口**：原 `/decision`、`/execution`、`/audit` 地址会跳回目标工作台；写入操作尚未在 Web 中开放。

目标实例必须符合 `docs/README.md`、`docs/architecture/` 和 `docs/templates/goal-folder/` 定义的核心协议。Web 当前只读取实例文档；未来若开放写入，必须通过同一协议、保留事务证据并由独立目标承接。

## 目录结构

```text
web/
├── main.py
├── requirements.txt
├── README.md
├── services/
│   └── goals_repo.py
├── static/
│   └── .gitkeep
└── templates/
    ├── base.html
    ├── index.html
    └── goal_detail.html
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

常用页面：

- <http://127.0.0.1:8000/> — 目标概览
- <http://127.0.0.1:8000/goals/GOAL-004-core-data-model> — 目标详情示例

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
- 首页与 `/goals/{goal_id}` 通过 `GoalsRepository` 读取 `docs/goals/`；目录扫描为运行时列表权威，`goal-tree.md` 的差异会显示为诊断。
- Tailwind CSS 和 HTMX 当前通过 CDN 加载。
- `static/` 已挂载到 `/static`。
- `services/goals_repo.py` 提供目标的 List/Get/Create/Update 与 `repair_goal_tree()`；本阶段 Web 只接入只读 List/Get，写入交互留待后续目标。
