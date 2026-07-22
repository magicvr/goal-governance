# Goal Governance Web

基于 FastAPI、Jinja2 与 Tailwind CSS 的目标治理 Web 应用。它是核心方法论与文档协议的**人类消费适配器**，不拥有独立的目标状态或生命周期定义。

## 当前切片（GOAL-012）

- **配置化产品工作区**：通过环境变量绑定工作区根；**默认 fail closed**，不会静默加载本 monorepo 的过程树（dogfood）。
- **工作区详情**：以**目标树**为主要导航，展示所选工作区内目标的 canonical 上下文（诊断为计算视图）。
- **受限提案**：用户可提交 `user-provided` 候选执行事实，生成仅追加 `02-execution.md` 的提案 diff。
- **受控写入门禁（GOAL-009 A-030）**：**F-007/F-008 closed**；**I-003/I-004/I-006 verified（α）**。规划锁默认 **关闭**（`PRODUCT_GATES_OPEN` 默认 `false`）。生产写入仍须第二门闩 `ALLOW_CONTROLLED_WRITE=true`，且数据根为产品工作区（非 dogfood）、单进程 residual（R-F008）。契约测试可用 `test_authorized` / `TEST_WRITE_MODE`。
- **R-004 覆盖边界**：Service 级关键路径 + GOAL-013 B/C/D CT 证据。CT-009=process-local；CT-011=最小可核对（accepted residual）。
- **幂等语义（CT-007/008）**：成功 `decide_and_execute` 将 receipt 原子写入工作区 `ops/receipts/{operation_id}.json`（非五件套）。新实例同 `operation_id`+同 request 返回既有 receipt；不同 request → `ERR_IDEM_CONFLICT` / `conflict`，不覆盖已提交 receipt。
- **F-007 向门禁（阶段 C）**：跨 workspace / path escape → `ERR_SCOPE_MISMATCH`；过期 → `ERR_DECISION_EXPIRED`；外部 trust → `ERR_TRUST_CONTEXT`；治理/脚本/路径内容 → `ERR_CONTENT_CONTRACT`。
- **F-008 向门禁（阶段 D）**：recovery pending → `ERR_RECOVERY_PENDING` / `recovery_pending`；同进程 workspace 锁竞争 → `ERR_CONCURRENT_WRITE` / `conflict`；不可复核 committed receipt → `ERR_RECEIPT_UNVERIFIABLE` / `failed`。
- **双门闩**：`PRODUCT_GATES_OPEN=true` **或** `ALLOW_CONTROLLED_WRITE` 未开 → 生产路径拒绝写入。
- **N1 工作区导航（GOAL-015 A–C）**：
  - service：`workspace_registry.py`（`DATA_ROOT` 下发现/注册；N1 字段；有界创建；归档索引）
  - 绑定：`workspace_binding.py` + cookie `gg_focus_workspace_id`（HttpOnly）
  - Web：`GET /workspaces` 列表、`POST /workspaces/select`、`POST /workspaces/status`（归档/恢复）、`GET /api/workspaces`；多区未选 **fail closed**
  - 归档只改索引 `active|archived`，**不**删除磁盘 canonical；归档当前焦点会清除 cookie
  - 注册表 `{data_root}/workspaces/registry.json` 仅为导航索引，不是目标状态权威
- **共享资料产品（GOAL-016 A–C）**：
  - store：`materials_store.py` → `{DATA_ROOT}/shared-materials/`（refs 权威：`shared-materials/refs/{workspace_id}.json`，**不是**各区 `workspace.md` 表）
  - Web：`GET /materials`、上传（新建）、附加到焦点工作区、软删、blob 下载、`GET /api/materials`
  - 须配置 `GOAL_GOVERNANCE_DATA_ROOT`；引用绑定 N1 焦点（或 α 单区）
  - service 可用 `put_bytes(material_id=)` 追加不可变版本；**Web 表单默认不传 material_id**（追加版本 = residual UX）
  - 复用 `shared_materials.py` SM 校验；**AI 读资料未交付**（residual `R-016-AI-READ`）；SM-004：当数据、不执行、不外传
- **非目标**：无 AI、无共享资料 CRUD、无多工作区 N1 列表产品化、无 SQLite；发布物不含 dogfood 过程树；fixture 使用合成 `GOAL-001-fixture-target`（`web/tests/fixtures/r004/workspace-ok/`，非本仓过程数据）。

## 工作区配置（fail closed）

| 变量 | 含义 |
|------|------|
| `GOAL_GOVERNANCE_WORKSPACE_DIR` | 显式产品工作区根（含 `goal-tree.md` 与 `GOAL-*`） |
| `GOAL_GOVERNANCE_DATA_ROOT` | 数据根：若内含 `goal-tree.md` 则直接使用；若恰有一个 `workspace-*` 子目录则选用它 |
| `GOAL_GOVERNANCE_DEV_DOGFOOD` | `true` 时加载本仓库 `docs/workspace-001-goal-governance/`（**仅开发**） |
| `GOAL_GOVERNANCE_PRODUCT_GATES_OPEN` | 默认 `false`（A-030 后）：规划锁关闭。设 `true` 可紧急再阻断生产写入 |
| `GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE` | 第二门闩；`true` 时允许生产受控写入（须产品数据根，非 dogfood） |
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

1. GOAL-009 **F-007** 与 **F-008** 均已关闭。**当前：均 closed**（F-008 有界 + residual）。
2. I-003 / I-004 / I-006 为 `verified`。**当前：均 verified（α，A-029）**。
3. `GOAL_GOVERNANCE_PRODUCT_GATES_OPEN=false`。**当前：代码默认 false（A-030）**；设 `true` 可再阻断。
4. `GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE=true`。**当前：默认 false — 部署时显式打开。**
5. 部署数据根为客户/产品工作区，**不是**本仓 dogfood 过程树（`DEV_DOGFOOD` 不得与生产写入同开）。
6. 部署形态仍为 **单进程 local-loopback**（或 residual 已按 R-F008 复审通过）。

### 推荐生产 env 片段

```powershell
$env:GOAL_GOVERNANCE_PRODUCT_GATES_OPEN = "false"
$env:GOAL_GOVERNANCE_ALLOW_CONTROLLED_WRITE = "true"
$env:GOAL_GOVERNANCE_DEV_DOGFOOD = "false"
$env:GOAL_GOVERNANCE_WORKSPACE_DIR = "C:\path\to\product-workspace"
```

或复制 `web/.env.example` → `web/.env`（gitignore）后编辑。应用启动时会加载 `web/.env`（不覆盖已有进程环境；unittest 不加载）。

本地示例产品数据根可用仓库内 `data/product-workspace/`（gitignore；由 R-004 fixture 复制，**不是** dogfood 过程树）。

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

## AI API 本地配置（GOAL-014 阶段 B）

范例字段见 `.env.example`。服务端可通过 `load_web_dotenv()` 加载 `web/.env`（unittest 不加载）。

| 变量 | 说明 |
|------|------|
| `GOAL_GOVERNANCE_AI_ENABLED` | 总开关；默认 `false` → 所有 AI 调用 fail closed |
| `GOAL_GOVERNANCE_AI_PROVIDER` | 提供方标识（如 `openai-compatible`） |
| `GOAL_GOVERNANCE_AI_BASE_URL` | API 根（…/v1） |
| `GOAL_GOVERNANCE_AI_API_KEY` | 密钥；**禁止**提交仓库或写入日志/HTML |
| `GOAL_GOVERNANCE_AI_MODEL` | 模型名 |
| `GOAL_GOVERNANCE_AI_REQUEST_TIMEOUT_SECONDS` | 超时，默认 30 |

实现：

- `web/services/ai_config.py` — 解析 + `public_dict` 无密钥  
- `web/services/ai_broker.py` — 门禁 + FakeTransport / OpenAI-compatible  
- `web/services/ai_candidates.py` — 进程内候选台账 + FA 确认 + R-004 提案  

`/api/health` 含 `ai` 对象（**无** key 明文）。  

**阶段 C UI/API**（目标详情 · 执行页）：

| 路由 | 作用 |
|------|------|
| `POST /goals/{id}/ai/suggest` | 用户触发生成 AI 候选（不写盘） |
| `POST /goals/{id}/ai/confirm` | FA + 生成受限提案（仍须 decide 才写） |
| `POST /goals/{id}/ai/reject` | 拒绝候选 |
| `POST /api/goals/{id}/ai/complete` | JSON 友好 suggest |

测试可用 `GOAL_GOVERNANCE_AI_TEST_TRANSPORT=fake` 注入 FakeTransport。真实密钥不得提交。
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
