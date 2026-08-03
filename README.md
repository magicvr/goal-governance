# Goal Governance

目标治理框架：交付可复用的核心方法论、文档协议与模板，并以 **Skills**（AI / Git 仓库协作）为**现行主消费适配器**，贯通 **目标 → 决策 → 执行 → 审计**。

**愿景波次**（Charter `vision-goal-governance@0.2.0`）：

1. **VP-001** 奠基 — **closed**（`workspace-001` Root 有界 **done**，过程树封存）  
2. **VP-002** 真实项目反馈演进 — **active**（`workspace-002` delivery 已承接）
3. **VP-003** 人类 UI — **planned**（本仓 `web/` 为冻结参考；预期通用基架）

## 从这里开始

| 想了解… | 去读 |
|---------|------|
| 当前工作区目标与进展 | [docs/workspace-001-goal-governance/goal-tree.md](docs/workspace-001-goal-governance/goal-tree.md) |
| 仓库愿景 / 投资面 | [docs/vision/charter.md](docs/vision/charter.md) |
| 文档怎么写、规则是什么 | [docs/README.md](docs/README.md) |
| 核心模板怎么用 | [docs/templates/README.md](docs/templates/README.md) |
| AI 必须遵守什么 | [AGENTS.md](AGENTS.md) |
| Skills 如何安装 / 升级 | [skills/README.md](skills/README.md)（**双入口**：在线 bootstrap 或包内 `install.*`；安装后用 `update.*`；skills zip **内嵌** core） |
| Skills 如何打包 / 发布附件 | [docs/releases/README.md](docs/releases/README.md)、`scripts/pack_skills_release.py`、`scripts/pack_core_release.py` |
| 技术栈与架构 | [docs/architecture/overview.md](docs/architecture/overview.md) |
| Web（冻结参考） | [web/README.md](web/README.md) |

## 在其他项目中安装 Skills（双入口）

其他仓库**不要**依赖 clone 整个 monorepo。从 GitHub Release 取 **skills** 安装包（**内嵌** core 方法论；安装**不必**再从网上拉 core）。

另有并行 **core-only** 资产 `goal-governance-core-vX.Y.Z.zip`（无 Skills / standalone 方法论）；**不是**默认 Skills 安装路径。

### 入口 1 · 在线 / 本地 bootstrap（推荐）

从 **GitHub Release 固定 tag** 拉取 bootstrap 脚本（无需浏览器另存），脚本再下载**已内嵌 core 的 skills zip**、校验 SHA-256，并调用包内 install（等价 `-All`）。  
**当前示例 pin 最新正式 tag `v0.12.0`**（发新版时同步改本节与 [skills/README.md](skills/README.md)；**不是**无版本锁的 always-latest，也**不用** branch raw URL）。仓库内源：`scripts/bootstrap/`。

```powershell
# 在目标项目根：从 Release 拉 bootstrap，再在线安装（当前最新 tag）
Invoke-WebRequest -Uri "https://github.com/magicvr/goal-governance/releases/download/v0.12.0/install-online.ps1" `
  -OutFile .\install-online.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-online.ps1 -Version 0.12.0 -Force

# 离线：已有 skills zip + .sha256 时（脚本同样可从同 tag Release 拉取）
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-online.ps1 `
  -Version 0.12.0 -ZipPath .\goal-governance-skills-v0.12.0.zip -Force
```

```bash
# 在目标项目根：从 Release 拉 bootstrap，再在线安装（当前最新 tag）
curl -fsSL -o install-online.sh \
  "https://github.com/magicvr/goal-governance/releases/download/v0.12.0/install-online.sh"
chmod +x install-online.sh
bash ./install-online.sh --version 0.12.0 --force

# 离线：
bash ./install-online.sh --version 0.12.0 --zip-path ./goal-governance-skills-v0.12.0.zip --force
```

说明见 [scripts/bootstrap/README.md](scripts/bootstrap/README.md)。默认**不**推荐 `curl | bash` / `irm | iex` 管道直跑（先落盘再执行，便于审阅）。

### 入口 2 · 包内 install（解压后离线）

```powershell
# 1. 下载 goal-governance-skills-vX.Y.Z.zip（及 .sha256）到目标项目根
# 2. 解压并命名为 skills
Expand-Archive .\goal-governance-skills-vX.Y.Z.zip -DestinationPath .
Rename-Item .\goal-governance-skills-vX.Y.Z skills

# 3. 包内安装（默认四入口 + core → docs/）
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
维护者正式发版：annotated `v*` tag + Environment `release` 审批 + 严格 release-evidence（见 [docs/releases/README.md](docs/releases/README.md)）。本地调试：

```text
python scripts/pack_skills_release.py --version X.Y.Z --output-dir dist/
python scripts/pack_core_release.py --version X.Y.Z --output-dir dist/
```

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
├── web/                      # 冻结参考：有界 FastAPI 工作台（非现行投资面）
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── static/
│   └── templates/
├── .editorconfig
└── .gitignore
```

- **核心文档层**：`docs/README.md`、`docs/architecture/`、`docs/templates/` 与 `docs/contracts/` 定义方法论、协议、模板和消费适配器兼容契约；每个 `docs/workspace-<NNN>-<slug>/` 保存自身目标实例。
- **`skills/`**：**现行主消费适配器**——AI/Agent 编排、审计、愿景入口、宿主安装与离线分发。
- **`web/`**：**冻结参考实现**（阶段 6 有界成果）。可读 + 受控写契约样本仍在，**默认不**作为产品推进面；详情见 [web/README.md](web/README.md)。
- **一个真相源**：Skills（及任何未来 UI）消费同一工作区文档协议，不建立独立状态。

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

## Web（冻结参考 · 非默认路径）

本仓 Web **不是**当前产品投资面。若需查阅历史有界实现或跑参考回归，见 [web/README.md](web/README.md)（含启动方式）。日常协作请用 **Skills**（`/govern`、`/audit`、`/vision`、`/vision-audit`）。

## 当前 Web 模块

- **目标概览**：展示目标、状态、进度及目标树 / 文档诊断。
- **目标详情**：展示成功标准、附件、Decision、Execution 和 Audit 的基础信息，并在需要时回退到原始 Markdown。
- **兼容入口**：`/decision`、`/execution`、`/audit` 会跳回目标工作台。

当前 Web 是读取运行中工作区目标文档的只读工作台，而非仅有页面与路由骨架。它直接以 `docs/workspace-001-goal-governance/` 为当前真相源，不使用独立数据库或第二状态层，因此没有需要与目标文件“同步”的副本；当前也不提供 Web 写入、创建/更新或写入同步。任何写入能力须由独立目标实现，并遵守同一文档协议与审计约束。
