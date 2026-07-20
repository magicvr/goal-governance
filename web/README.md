# Goal Governance Web

基于 FastAPI、Jinja2 与 Tailwind CSS 的目标治理 Web 应用。它是核心方法论与文档协议的**人类消费适配器**，不拥有独立的目标状态或生命周期定义。

## 当前切片（GOAL-012）

- **配置化产品工作区**：通过环境变量绑定工作区根；**默认 fail closed**，不会静默加载本 monorepo 的过程树（dogfood）。
- **工作区详情**：以**目标树**为主要导航，展示所选工作区内目标的 canonical 上下文（诊断为计算视图）。
- **受限提案**：用户可提交 `user-provided` 候选执行事实，生成仅追加 `02-execution.md` 的提案 diff。
- **受控写入门禁**：生产路径 `decide_and_execute` 在 GOAL-009 **F-007/F-008 仍 open**（`GOAL_GOVERNANCE_PRODUCT_GATES_OPEN=true` 默认）时**拒绝写入**；契约测试可用 `test_authorized` / `GOAL_GOVERNANCE_TEST_WRITE_MODE`。
- **非目标**：无 AI、无共享资料 CRUD、无多工作区 N1 列表产品化、无 SQLite；发布物不含 dogfood 过程树；fixture 使用合成 `GOAL-001-fixture-target`（`web/tests/fixtures/r004/workspace-ok/`，非本仓过程数据），不用真实 GOAL-001～011 过程树当客户样例。

## 工作区配置（fail closed）

| 变量 | 含义 |
|------|------|
| `GOAL_GOVERNANCE_WORKSPACE_DIR` | 显式产品工作区根（含 `goal-tree.md` 与 `GOAL-*`） |
| `GOAL_GOVERNANCE_DATA_ROOT` | 数据根：若内含 `goal-tree.md` 则直接使用；若恰有一个 `workspace-*` 子目录则选用它 |
| `GOAL_GOVERNANCE_DEV_DOGFOOD` | `true` 时加载本仓库 `docs/workspace-001-goal-governance/`（**仅开发**） |
| `GOAL_GOVERNANCE_PRODUCT_GATES_OPEN` | 默认 `true`：产品写入门禁仍开放 → 生产写入关闭 |
| `GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE` | 仅当产品门禁关闭后，显式允许生产受控写入 |
| `GOAL_GOVERNANCE_TEST_WRITE_MODE` | 测试授权写入（勿用于生产） |

未设置工作区且未开 dogfood 时，首页显示配置错误，**不**读取本仓过程目标。

### 示例

```powershell
# 指向合成 fixture 或任意产品工作区
$env:GOAL_GOVERNANCE_WORKSPACE_DIR = "C:\path\to\workspace"
cd web
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

```powershell
# 仅本地 dogfood（可选）
$env:GOAL_GOVERNANCE_DEV_DOGFOOD = "true"
```

## 生产写入检查清单

在启用生产 `decide_and_execute` 之前必须全部满足：

1. GOAL-009 **F-007** 与 **F-008** 已关闭（有关闭证据）。
2. I-003 / I-004 / I-006 为 `verified`。
3. 设置 `GOAL_GOVERNANCE_PRODUCT_GATES_OPEN=false`。
4. 设置 `GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE=true`。
5. 部署数据根为客户/产品工作区，**不是**本仓 dogfood 过程树。

Receipt 写入工作区旁路 `ops/receipts/`（非五件套）。

## 目录结构

```text
web/
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── services/
│   ├── goals_repo.py
│   ├── workspace_config.py
│   ├── controlled_change.py
│   └── ...
├── templates/
├── tests/
│   └── fixtures/
│       ├── valid-goals/
│       └── r004/workspace-ok/   # synthetic R-004 fixture
└── static/
```

## 环境要求

- Python 3.10+
- pip

建议在项目根目录维护 `.venv`。

## AI API 本地配置（预留）

范例字段见 `.env.example`。当前应用**不会**为 AI 调用加载密钥；无 AI 页面。真实密钥不得提交。

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r web\requirements.txt
```

## 启动

必须先配置工作区（或 DEV dogfood），否则首页为 fail-closed 提示。

```powershell
.\.venv\Scripts\Activate.ps1
$env:GOAL_GOVERNANCE_WORKSPACE_DIR = (Resolve-Path web\tests\fixtures\r004\workspace-ok).Path
cd web
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- <http://127.0.0.1:8000/> — 工作区详情（目标树）
- <http://127.0.0.1:8000/goals/GOAL-001-fixture-target> — 目标详情 + 候选提案
- <http://127.0.0.1:8000/api/health> — 配置与门禁状态

## 测试

从 `web/` 目录：

```powershell
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

R-004 相关：`tests/test_controlled_change.py`、`tests/test_workspace_config.py`。

## 技术说明

- `GoalsRepository.from_config()` 解析工作区；默认构造不再静默绑定 dogfood。
- `ControlledChangeService` 实现 candidate → proposal → same-request affirm/execute → receipt。
- 多工作区选择器、共享资料、AI、SQLite 不在本切片范围。
