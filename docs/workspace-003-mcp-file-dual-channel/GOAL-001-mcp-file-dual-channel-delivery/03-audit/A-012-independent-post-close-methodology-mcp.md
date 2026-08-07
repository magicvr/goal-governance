---
id: A-012
goal: GOAL-001-mcp-file-dual-channel-delivery
title: 关门后独立审计 · 核心方法论/Skills 完整性 + MCP server 体系
status: recorded
source: independent
provider: grok-build / independent session / no skills loaded
date: 2026-08-07
scope: workspace-003 实施后的核心方法论文档与 skills 体系完整性；仓库根 mcp/ server 体系正确性与证据链可复核性；不改 status/progress/VP/workspace 状态
verdict: pass
version: 0.1.0
---

# A-012 · 关门后独立审计：方法论/Skills + MCP 体系（2026-08-07）

## 结论

**verdict: `pass`**

在 **不加载任何 Skill** 的独立会话中，对 workspace-003（VP-004 / R1–R4）实施完成后的两类对象做交叉审视：

1. **核心方法论文档与 Skills 体系**是否被双通道交付改坏、语义漂移或镜像破坏；
2. **MCP server 体系本身**是否存在协议/安全/发布/证据面问题。

**独立核验结果（本审亲自执行）**：

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests skills/tests scripts/tests -q` | **198 passed**, 4 skipped, 4 subtests passed（~40s） |
| `python scripts/stage_skills_mirrors.py --check` | **ok**（36 pairs；skills mirrors match docs/） |
| `pack_skills_release.py --version 0.0.0-audit` | zip **80 成员**；**0** 条 `mcp/` 实现路径；无 `server.py` 进 File 包 |
| L2 `kernel.check_equivalence` 现场 | 检查点 **1–10 全部 ok** |
| `config.resolve_governance_root` | 默认 `docs`；`../`、绝对路径、盘符路径 **fail closed** |
| lifecycle `confirm=false` | 拒绝写盘（ok） |
| MCP `tools/list` | `vision` / `vision-audit` / `govern` / `audit` + install/upgrade/uninstall/doctor；**无 `commit`** |
| `audit` 缺 `goal_id` | 拒绝（required 参数门禁 ok） |
| 关键资产存在性 | 四治理 prompts、core principles/protocol/alignment、contract 0.4.0、`mcp/{server,entries,kernel,config,lifecycle,Dockerfile}` 均存在 |
| L3 `behaviorSources` vs 当前树 | 见 F-001（路径过期；非宿主探针语义失败） |

**无 required / 阻断 findings。** 按用户本轮授权规则：仅落盘意见，**不**回退 Root `done` / 子目标 done / VP-004 `closed` / workspace closed / goal-tree 状态。

- **auditor**：grok build · 独立会话 · **未加载** govern/audit/vision 等 Skill  
- **source**：`independent`  
- **类型**：close-out + ad-hoc（方法论完整性 + MCP 体系）

## 范围与区间

| 项 | 内容 |
|----|------|
| 工作区 | `workspace-003-mcp-file-dual-channel`（closed） |
| Root | `GOAL-001-mcp-file-dual-channel-delivery`（done · progress 100%） |
| 子目标 | GOAL-002～005 均 done（本审不逐条重做子目标关门文书，聚焦跨切面完整性） |
| 方法论权威面 | `docs/architecture/{principles,workspace-protocol}.md`、`docs/vision/alignment.md`、根 `AGENTS.md`、`docs/templates/**`、stage 镜像 `skills/core/**` / `skills/contracts/**` |
| Skills 分发面 | `skills/prompts/**`、`skills/install*`、`skills/AGENTS.template.md`、pack zip 成员 |
| MCP | 仓库根 `mcp/**`、bootstrap `-Channel mcp`、release workflow Docker 步骤、L1/L2/L3 证据 |
| 排除 | 不改任何目标 status/progress；不写 Vision Review；不加载 Skills；不代为修代码 |

## 一、核心方法论与 Skills 体系（实施后完整性）

### 1.1 是否「被破坏」

| 检查面 | 独立判断 | 说明 |
|--------|----------|------|
| P-001～P-006 元规则正文 | **未破坏** | `principles.md` 仅增 `governance_root` 定义句；原则语义与门禁未改写成第二套协议 |
| 工作区协议 / 对齐链 | **未破坏** | R3 车辆将路径叙述相对化为 `{governance_root}/…`（默认 docs）；fail closed / 单愿景 / primary\|delivery 仍在 |
| Skills 镜像 | **未破坏** | stage `--check` 36 对 0 漂移；禁止手改镜像的纪律在本树上仍成立 |
| 四治理入口 File 正文 | **未破坏** | `prompts/00,05,06,07` 存在；L2 从真实 prompt 文本提取角色短语并通过 |
| File 通道发布 | **未破坏** | pack 80 成员、无 MCP 实现；通道资产分离（R4 意图）在 File 侧成立 |
| 合同双通道 | **未破坏** | `contractFormatVersion` 0.4.0；`deliveryChannels` files\|mcp 均为 `first-class` |
| monorepo 生产仓固定 docs | **成立** | AGENTS / alignment 例外说明与本仓布局一致 |

**结论**：workspace-003 对方法论的改动是 **R3 授权的路径叙述相对化 + R4 通道布局迁出**，不是语义改写或 skills 体系崩坏。全量测试绿 + 镜像无漂移支持该判断。

### 1.2 引入但属范围外/残余的摩擦（非阻断）

| 观察 | 级别 | 是否算「方法论破坏」 |
|------|------|----------------------|
| `skills/AGENTS.template.md` 与 `skills/prompts/**` 仍大量裸写 `docs/…`（未用 `{governance_root}`） | recommended | **否**。R3 车辆（D-002）必改清单为 alignment / protocol / 根 AGENTS / templates；消费模板/编排正文相对化属后续收敛（与 A-009 R-001 同类） |
| `directory-layout.md` 未登记仓库根 `mcp/` | recommended | **否**。布局说明滞后，不改变协议不变量 |
| File zip 仍含 `tests/test_mcp_*.py`（实现已迁出） | recommended | **否**。实现未混入；测试在纯 File 解包环境会因缺 `mcp/` 失败（F-003） |

## 二、MCP server 体系审计

### 2.1 符合 VP-004 / 既有冻结方案的部分

| 意图面 | 独立判断 | 证据 |
|--------|----------|------|
| 最小 stdio、零第三方、非 Docker-only | **符合** | `server.py` JSON-RPC over stdio；本地 `python mcp/server.py` 合法；Docker 为 R4 推荐形态 |
| 四治理工具 + 无 commit | **符合** | 现场 tools 列表 |
| 薄入口 = 结构化 dispatch（角色/台账/只读元数据） | **符合** | `tools/call` 返回 entrypoint/layer/role/readonly/writesTo/promptPath；**不**写 goal-tree/五件套 |
| lifecycle allowlist + 默认确认写盘 | **符合** | 仅 AGENTS managed + `.goal-governance/`；`confirm=false` 拒写 |
| `governance_root` fail closed | **符合** | `config.py` + 本审现场 |
| L2 十条等价 | **符合** | 现场 10/10 ok |
| 通道资产分离 + Dockerfile | **符合（结构）** | 根 `mcp/`；File zip 无实现；workflow `context: mcp/` + GHCR tag；**真实 GHCR pull 证据仍 open（I-007 / 既有 F-001）** |
| 实例真相不在 MCP | **符合** | server instructions + 治理 call 不写仓 |

### 2.2 问题与严重度

#### required（必改 / 阻断）

**无。**

未发现：解析绕过 fail closed、lifecycle 默认可写、四入口缺失、commit 进工具集、File 包回混 MCP 实现、镜像 stage 漂移、L2 等价失败、方法论原则被改写为第二套状态协议、或迫使 Root/VP 退出判据整体失效的实现级故障。

#### recommended（非阻断）

| ID | 严重度 | 说明 | 建议 |
|----|--------|------|------|
| **F-001** | med | **L3 `behaviorSources` 与当前树字面不一致（R4 迁路径后证据账本过期）**。四条 `*-l3-four-entry-2026-08-07.json` 仍绑定 `skills/mcp/{entries,kernel,server}.py`（路径 **不存在**）。将路径 remap 到 `mcp/` 后：`entries.py`/`kernel.py` 哈希仍匹配；**`server.py` 哈希不匹配**（R2/R4 后合法演进）。宿主探针 prompt 哈希 **仍 OK**。Root `00-meta` 宿主表备注写「behaviorSources 哈希与当前树一致」在 **字面路径层已不成立**。 | 维护轮：要么重捕获 L3 并将 `behaviorSources` 改为 `mcp/*` 当前哈希；要么在 GOAL-002 runtime README / Root 宿主备注写明「R1 捕获点绑定历史路径；R4 后以 remap + L1/L2 为 MCP 面复核」。**不**据此宣称宿主 L3 当时 verdict 作废。 |
| **F-002** | med | **`mcp/__version__ = "0.1.0"` 与发布 tag 体系（如 0.13.x）脱节**。`initialize.serverInfo.version` 与 MCP 工具 `install`/`upgrade` 默认写入版本均来自该常量；bootstrap `-Channel mcp` 虽用 `--version $NORM` 覆盖 lifecycle CLI，但 **经 MCP tools 安装会写入 0.1.0**。镜像 tag 与进程自报版本可长期漂移。 | 发布时用构建参数/环境/`__version__` 与 pack version 同源钉死；或明确「server 内部 layout version ≠ 产品 release version」并在 doctor 分列报告。 |
| **F-003** | low | **File zip 内 `tests/test_mcp_*.py` 在纯 skills 解包环境无法通过**（`REPO_ROOT/mcp/server.py` 不存在；本审隔离解包 6 failed）。通道实现已分离，但测试资产仍假设 monorepo 并列 `mcp/`。 | pack 排除 MCP 集成测试，或文档标明「仅 monorepo CI」；避免消费者把失败当 File 通道损坏。 |
| **F-004** | low | **MCP 协议严格性：未强制 `initialize` 后再 `tools/list|call`**（`initialized` 标志可仍为 false 时工具仍可用）。多数宿主会先 initialize，但严格客户端可能依赖顺序。 | 可选：未 initialize 时拒绝 tools 并返回明确错误。 |
| **F-005** | low | **lifecycle 的 `root` 参数可指向任意本机目录并写 AGENTS.md**（allowlist 相对 *该* root 生效，非绑定 server `--repo-root`）。Docker 固定 `/workspace` 时风险较低；stdio 本地进程下等同「客户端指定写盘根」。 | 文档声明信任模型；可选：默认强制 `root` ⊆ server.repo_root。 |
| **F-006** | low | **消费面路径收敛未完成**：`skills/AGENTS.template.md`、四治理 prompts 仍硬编码 `docs/…`。monorepo 默认 docs 可用；`governance_root≠docs` 的 File 消费仓依赖 AI 自觉读 alignment 定义句，易误读。 | 归 VP-002 / 消费面维护：模板与 prompts 改为 `{governance_root}` 或安装时按 pin 展开。 |
| **F-007** | low | **`directory-layout.md` 未反映 R4 根目录 `mcp/`**（仍停在 skills 包内布局叙事）。 | 增补 monorepo 布局一行；与 README 对齐。 |
| **F-008** | info | **真实 GHCR 发布物仍未在本审环境验证可 pull**（与 GOAL-005 I-007 / A-002 F-001 同构；non-blocking 已登记）。 | 首次 `v*` 正式发布后回填 digest/URL。 |

## 三、对关门状态的处理决定

| 项 | 决定 | 理由 |
|----|------|------|
| Root / 子目标 status | **不回退** | 无 required finding；退出判据能力与实现证据链（测试、pack、L2、fail closed、workflow 结构）仍可复核 |
| VP-004 / workspace | **不回退** | 同上；发布验收 I-007 已为 non-blocking open |
| 本意见 | **仅落盘** | 用户授权：无阻断项 → 只写审计意见 |

## 四、与既有意见的关系

| 既有 | 关系 |
|------|------|
| A-009（关门复审 pass） | 本审在 **R4 迁路径之后**复做同类范围；确认方法论权威面仍成立；新增 F-001（R4 后 L3 路径账本过期） |
| GOAL-005 A-002 F-001～F-005 | F-002 已 fixed（workflow 契约）；F-003 路径字面已 fixed（A-011）；GHCR 实测仍 open → 本审 F-008 |
| A-011 复关 | 复关依据在实现/管线层仍成立；**未**同步刷新 L3 behaviorSources 路径 → 本审 F-001 |

**无**与既有 independent 的 required 冲突（既有亦无 open required）。

## 五、给编排器 / 用户的建议

1. **无需**为本次意见回退 workspace-003 关门。  
2. 建议后续维护轮（不必 reopen VP-004，除非用户希望正式重捕获 L3）响应 **F-001～F-003** 优先：证据账本路径、server 版本钉、File 包测试边界。  
3. **F-006** 适合挂 VP-002 消费面/协议正文收敛，而非再开双通道交付区。  
4. 独立审计默认不改 status；响应与是否修代码归 `/govern`（或人工）。

### 建议的下一句（可选）

```text
/govern 响应 workspace-003 Root A-012（independent pass）：无 required；登记 F-001～F-008；优先维护 L3 behaviorSources 路径与 mcp.__version__ 发布钉
```
