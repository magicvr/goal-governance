---
doc_type: vision-plan
id: VP-004-mcp-file-dual-channel-delivery
title: 消费交付双通道（MCP + File）与可配置治理根
status: closed
vision_ref: vision-goal-governance@0.2.0
lead_workspace: workspace-003-mcp-file-dual-channel
created: 2026-08-07
updated: 2026-08-07
version: 0.5.0
---

# VP-004 · 消费交付双通道（MCP + File）与可配置治理根

## 意图

在 Charter `vision-goal-governance@0.2.0` 下，为 **Agent 消费适配** 建立 **File 资产通道** 与 **MCP 资产通道** 的**双通道一等公民**交付：同一协议、同一治理入口语义，分发形态与证据分列。

- **File 通道**：保留并继续发布现行 skills zip / install 体系；服务无 Docker、强离线、仓内可审 prompts，以及 **本 monorepo 生产自举**（不以「本仓 MCP 镜像治本仓协议」为唯一路径，避免循环依赖）。
- **MCP 通道**：以 MCP Server（推荐 Docker；合同上为可运行的 MCP 进程，**不**强制 Docker-only）+ **薄 Skills / 薄宿主入口** 承载编排与方法论正文，降低消费仓 footprint 与升级噪音。
- **推荐姿态**：新装/文档可 **推荐** MCP 通道；**不**以废除 File 通道或取消 file 发布资产为本 VP 成功条件。
- **不**另立远端权威目标状态（实例真相仍在仓库内治理记录）。
- **不**以本仓 Web / VP-003 为驱动。
- **协议本体**：方法论与对齐不变量仍以 `docs/architecture/` + `docs/vision/alignment.md` 等 canonical 为准；本 VP **不**发明第二套目标状态协议。R3 引起的**路径/安装叙述**修订须走下方「R3 协议面变更车辆」，不得仅用 MCP 运行时行为静默改写权威面。

### 承诺宿主与 P0 / P1（本 VP 约定）

四者均为本 VP **承诺面**；不得移出承诺面而不修订本文件。

| 宿主 | 波次 | 约定级验证地板（退出判据 #5） |
|------|------|------------------------------|
| Claude Code | **P0** | 该宿主至少：通道分列 **L1**（File 与/或 MCP 按已交付通道）+ **一条 L3 抽稀真探针**（覆盖四治理入口的 dispatch/角色边界，不要求完整治理长剧 + 真模型全链路） |
| Grok Build | **P0** | 同上 |
| OpenAI Codex | **P0** | 同上 |
| GitHub Copilot | **P1** | 至少通道分列 **L1**；L3 探针鼓励但不强制。若 P1 仅 L1 / stub，完整关门前须用户书面 **accepted-residual**（范围 + 复审触发） |

**非目标宿主（本 VP）**：Google Antigravity、Open Code——不进矩阵与退出判据；有需要时另开目标或修订本 VP / 后续 VP。

### 入口面

| 入口 | 级别 | 说明 |
|------|------|------|
| `vision` | **治理必达** | 决策层 |
| `vision-audit` | **治理必达** | 独立 Vision Review |
| `govern` | **治理必达** | 实现编排 |
| `audit` | **治理必达** | Goal 交叉审计 |
| `commit` | **便利可选** | 参考 monorepo [`.github/prompts/commit.prompt.md`](../../../.github/prompts/commit.prompt.md)：安全暂存 + 中文 Conventional Commit；**与目标治理正交**；**不**进入完整治理安装 MUST / consumer 治理 entrypoints 必选集 |

### 交付容器

- **主交付工作区（已开）**：`workspace-003-mcp-file-dual-channel` + Root `GOAL-001-mcp-file-dual-channel-delivery`，挂本 VP 为 `primary_plan`；`vision_role: delivery`；**lead** = 本区。
- **不**在 `workspace-001-goal-governance` 的已 done Root 下开本 VP 子目标；**不**改写 `workspace-002` 的 `primary_plan`（VP-002 并行）。
- **生产仓**：协议与 skills **源码树** 仍为 File 权威；MCP 仅可作兼容 dogfood，不替代自举。

### 空转声明（alignment §5.1）

| 项 | 值 |
|----|-----|
| 空转状态 | **已结束**（2026-08-07 挂区） |
| 空转起算 | 不适用（激活同时挂区，未经历 active 且 0 区） |
| 挂区日 | **2026-08-07** · `workspace-003-mcp-file-dual-channel` |
| 说明 | 挂区后不再适用「0 区空转 fail closed」；交付证据在工作区目标内 |

### Charter 叙事选择（本 VP 阶段 · V-F-015）

| 项 | 书面选择 |
|----|----------|
| 是否改 Charter @0.2.0 | **否**（本 VP 阶段不触发 Charter editorial/strategic） |
| 「推荐 MCP」含义 | **安装/bootstrap 便利推荐**；**不是**废除 File；**不是**把「现行主消费适配器 = Skills」改写成 MCP-only |
| Skills 语义 | Skills（含薄 Skills / 薄宿主入口）仍为 Agent 侧协议消费主面；MCP 是**交付通道**，承载同一编排语义 |
| File 地位 | **一等通道**保留；File-classic（无 Docker / 无 MCP）仍须可发布、可验证 |
| 对外文档约束 | 凡写「推荐 MCP」须同屏/同节声明 File 仍一等且非日落 |
| 若未来写入 Charter | 仅当要把「双通道适配器族」升格进目的/假设时，另走 **strategic + Vision Review + re-align**（可选，非本 VP 自动完成） |

## 方向级路线图（纲领阶段 · 非 progress%）

### R1 · MCP 通道并行达标 + 最小共享测试内核（伴生）

**目标**：在**不必**安装 File 大包的前提下，MCP + 薄入口可完成与现行四治理入口等价的目标治理工作（实例仍落本地文件约定路径）。

**伴生必达 · 最小统一测试内核**（靠前交付，**不是**收官阶段）：

| 层 | 要求 |
|----|------|
| **L2 共享** | 一份工作区 fixture + 协议/编排行为套件；File 与 MCP **共用**内核断言（优先引用下方「入口等价检查点」） |
| **L1 MCP** | mock MCP 确定性验证薄壳 / prompts → tool 名与关键参数 |
| **L1 File** | 与 MCP **分列**；**禁止**用 MCP mock 顶替厚 File 入口证据 |
| **L3** | 承诺宿主 × 通道的抽稀真探针（不要求每格完整治理长剧 + 真模型跑通编排） |
| **合同可读** | 证据与 contract 按 `deliveryChannel: files \| mcp` 分列；标注 L1/L2/L3，避免 mock 冒充全链路 |

#### R1 · 四治理入口「等价」检查点（V-F-016 · L2 可引用）

「等价」= 下列检查点在 File 与 MCP 通道上均可核对（允许实现形态不同，**语义与台账边界**不得漂移）：

1. 四治理入口名可发现：`vision` / `vision-audit` / `govern` / `audit`（`commit` 不计入必达等价集）。
2. 角色边界：`vision` = 决策层；`vision-audit` = 独立 Vision Review（只出意见）；`govern` = 实现编排；`audit` = Goal 交叉审计。
3. Vision Review 只写入 `docs/vision/reviews.md` + `reviews/VRev-*`（或 `{governance_root}/vision/...`）；**禁止**写入 Goal `03-audit`。
4. Goal 审计只写入目标 `03-audit`；**禁止**写入 vision reviews 台账。
5. 实例真相在仓库内治理记录树（默认 `docs/` 或已配置的 `governance_root` 下工作区）；MCP/DB **不得**成为权威状态库。
6. 缺 active Charter、缺 `plan_refs`/`primary_plan`、`vision_ref` 与 Charter 不一致 → **fail closed**（引导补齐除外）。
7. 独立审计默认**不**直接改 Charter / VP / Goal `status`。
8. 单愿景不变量：不引入第二 active Charter / 第二套目标状态协议。
9. 工作区角色仅 `primary` / `delivery`；无 plan opt-out。
10. 生产仓自举不以「仅 MCP」为唯一路径（File 源码树权威保留）。

**R1 非目标**：六宿主外扩；证据农场/矩阵自动化产品化（更大范围可另开后续 VP）；多存储后端。

### R2 · 双通道产品化

**目标**：File 与 MCP **均为一等发布通道**。

- Bootstrap / 在线安装：**双入口**文档与脚本路径；可推荐 MCP（须遵守上方 Charter 叙事选择），**保留** file zip 安装。
- MCP：薄 Skills 的 install / upgrade / uninstall 可由 MCP 工具管理；managed paths allowlist；默认确认写盘。
- 消费仓薄入口：**默认建议 gitignore**（不进仓库）；提供官方 ignore 片段 + `doctor`；**允许**团队可选将薄壳锁进 git。
- **AGENTS.md**（及等价规则文件）：治理相关段落用机器可解析标记包裹，更新/卸载 **只改标记内**，不触碰用户自有配置。示意：

  ```markdown
  <!-- goal-governance:begin managed -->
  …
  <!-- goal-governance:end managed -->
  ```

- 生产仓继续 File 自举；File 通道完整可用（含无 Docker、无 MCP 的 **File-classic** 路径）。
- MCP 运行时：推荐 Docker；允许本地 stdio 等非容器进程，避免「无 Docker = 不能用 MCP」。

### R3 · 可配置 `governance_root` 与消费面收敛

**目标**：

1. 可配置 **治理根路径** `governance_root`（默认 `docs`）：即默认的 `docs/` 可改为仓库内其他相对根（如 `governance/`）。
2. **`governance_root` 以下内部相对布局不可改**（`vision/`、`workspace-*`、`goal-tree`、五件套形状等保持协议约定）。
3. 合法 root：相对仓库根；**禁止**指向仓外（fail closed）。
4. root 与 MCP/协议 pin 须落在 **可提交的项目配置**（推荐如 `.goal-governance.json`）和/或 AGENTS managed 段，避免仅环境变量导致团队漂移。
5. 消费侧与目标治理相关、**预期进 git** 的集合收敛为：项目配置（若使用）+ AGENTS managed 段 + 治理记录树；方法论正文与厚 skills 不强制进消费仓（视通道而定）。

**R3 非目标**：任意打散多根、修改内部文件夹名字/形状、存储迁 DB。

#### R3 · 协议面变更车辆（V-F-013 路径 A）

R3 是**交付能力**，但落地会触及 alignment 等权威路径的 **`docs/` 硬编码假设**。分工如下（完整关门前两边都要有证据链接）：

| 负责面 | 做什么 | 权威落点 |
|--------|--------|----------|
| **本 VP 交付（挂区目标 / `/govern`）** | `governance_root` 解析与默认值；仓外路径 fail closed；项目配置 / managed 段 pin；双通道 runtime 与安装面消费该 root；产品化与验证证据 | 工作区目标五件套 + 发布/contract 证据 |
| **协议/规则权威修订（canonical）** | 将「路径相对于 `governance_root`（默认 `docs`）」写进规则，避免只改运行时 | **必须**改：`docs/vision/alignment.md`（至少 Minimal Complete Install 路径叙述）；按影响面改 `docs/architecture/workspace-protocol.md`、根 `AGENTS.md` 操作摘要、相关 `docs/templates/**`。有 stage 脚本时同一任务 stage Skills 镜像（AGENTS §8c） |
| **与 VP-002 的关系** | 协议**内容**问题驱动演进仍主要归 **VP-002**；本 VP 的 R3 权威面修订可作为 **挂区实施的必做协议补丁**，或与 VP-002 并行目标协同，但**不得**用「归 VP-002」推迟到本 VP 已宣称 R3 退出满足之后 | 退出判据 #4 证据须同时指向：交付实现 **与** canonical 规则 diff/链接 |
| **Charter** | 仅默认 root 仍为 `docs`、目的/非目标不变 → **不**因 R3 自动 strategic。若把可配置根升格为愿景目的/成功边界措辞，另走 strategic + Review + re-align | `charter.md` / `revisions.md`（仅在真正改边界时） |

**禁止**：仅 MCP/工具实现识别 `governance_root`，而 alignment / 模板 / AGENTS 仍写死「必须是仓库根下 `docs/`」且无例外说明——视为 R3 **未**满足退出判据 #4。

## 方向级退出判据

在同时满足下列方向时，本 VP **可以**有界或完整关门（证据在挂接工作区目标内）：

1. **双通道一等**：File 与 MCP 均可按发布约定取得；文档与 bootstrap 双入口清晰；**未**将废除 File 通道设为隐性成功条件；对外「推荐 MCP」遵守上方叙事选择。
2. **R1 能力**：MCP 通道在「无 File 大包」前提下，四治理入口「等价」检查点可核对；最小共享测试内核（L2 共享 + 分通道 L1 + 抽稀 L3）已落地且 contract 可读。
3. **R2 产品化**：薄壳 lifecycle（MCP 管理）、gitignore 默认策略、AGENTS managed 标记、生产仓 File 自举边界均有证据。
4. **R3**：`governance_root` 可配置且内部布局冻结规则可验证；路径越界 fail closed；**且**「R3 协议面变更车辆」表中 canonical 权威修订已落盘（或用户书面 residual 点名未改条目与复审触发）。
5. **宿主**：四承诺宿主均有明确适配状态；**P0** 达到上表约定级验证地板；**P1** 至少 L1，缺 L3 须用户书面 residual。
6. **非目标未偷渡**：无 Antigravity/Open Code 假承诺；无 DB/多 backend 必达；`commit` 未绑架治理完整安装。
7. **不**要求关闭 VP-002/VP-003，**不**要求 Charter 可完成。
8. **R4 发布资产面（2026-08-07 reopen 增补）**：File 发布资产**不**包含 MCP 实现源码（通道资产分离，`mcp/` 实现不进 skills zip）；MCP server 以 **Docker 镜像**发布到本仓 GHCR，与 File 资产**同 tag 同时发布同版本**（随 `skills-pack-release.yml` tag 流程）；仓库与 README（根 README + `mcp/README.md`）提供安装 MCP server 的命令与指南，且文档与实现一致（无「Dockerfile 可选」类空头文案）。

## 明确非目标（本 VP）

| 项 | 说明 |
|----|------|
| Google Antigravity / Open Code | 不支持；以后另议 |
| 废除 File 通道 / 停止 file 发布 | 非成功条件；日落须另决策 |
| 生产仓仅靠 MCP 自举 | 禁止作为唯一路径 |
| Docker-only MCP | 不强制；stdio 等进程形态合法 |
| DB / SQLite / Mongo / PG / SQL Server | **不入本 VP**；有需要另开 VP |
| 超范围证据平台 | 矩阵农场、证据归档产品化等另开 VP |
| 修改 `governance_root` 以下内部树形 | 禁止 |
| 远端权威状态库 | MCP/DB 皆不得替代仓内实例真相 |
| 人类 UI 终态 | 见 VP-003 |
| 将 `/commit` 设为治理 MUST | 禁止 |

## 与其它 VP / Charter 的关系

| 对象 | 关系 |
|------|------|
| Charter @0.2.0 | 落在「可复用消费适配 + 实例本地」内；**本 VP 阶段不改 Charter**（见「Charter 叙事选择」）。双通道适配器族写入目的/假设 = 可选后续 strategic。 |
| VP-001 | 奠基 File Skills 可复用；本 VP 继承 File 通道并 **增加** MCP 通道。 |
| VP-002 | 协议/Skills **内容**反馈演进主波次；本 VP 管 **交付与验证骨架**。R3 权威路径补丁见「R3 协议面变更车辆」——可与 VP-002 协同，但本 VP 完整关门不得甩开未改的 hardcode。可并行；实现勿无故合并退出条件。 |
| VP-003 | 人类 UI；无关。 |
| 未来存储 VP | file+DB 等后端；本 VP 最多预留扩展点，**不**交付。 |
| 未来证据平台 VP | 超出最小共享内核的自动化/平台化。 |

## 工作区绑定

| workspace_id | root_goal | role | joined | notes |
|--------------|-----------|------|--------|-------|
| workspace-003-mcp-file-dual-channel | GOAL-001-mcp-file-dual-channel-delivery | delivery / **lead** | 2026-08-07 | 用户 `/govern` 确认新区 slug；Root R1–R3 纲领；R1/R2/R3 子目标全部 `done`（GOAL-002/003/004）；**R4 reopen 后复关**：GOAL-005-r4-mcp-docker-release `done`（2026-08-07 回退 + 当日复关） |

## 关门记录

| date | outcome | summary | evidence_links | residuals |
|------|---------|---------|----------------|-----------|
| 2026-08-07 | **closed**（工作区完整关门） | File+MCP 双通道一等交付（R1 四入口等价内核 + 合同 `deliveryChannel` 分列；R2 bootstrap 双入口 + 薄壳 lifecycle + AGENTS managed；R3 可配置 `governance_root` + canonical 权威面相对化）；P0×3 + P1×1 宿主达标（L1 + 抽稀 L3 探针全 pass）；非目标未偷渡；不要求 VP-002/VP-003 或 Charter 完成。 | 退出判据 1–7 证据链见 Root `03-audit/A-007-independent-close-out.md` 与 A-008 响应；R1/R2/R3 检查点 commits `1a89575` / `ae614db` / `560669e`（+ 关门 commit）；子目标 GOAL-002/003/004 五件套与 A 序列；`goal-tree.md`（全 done/100%）。 | 无（recommended 已响应；L3 探针为宿主入口面，MCP 进程面由 L1/L2 覆盖——边界记录于 GOAL-002 `attachments/runtime/README.md`）。 |
| 2026-08-07 | **reopened → active**（发布资产面缺口） | A-009 关门复审后，发布面核查（用户指令）发现关门范围外缺口：File zip 混入 `skills/mcp/` 源码（通道资产未分离）；MCP server 无 Docker 发布资产（无 Dockerfile / 无 GHCR 步骤 / README 无安装指南）；`skills/mcp/README.md` 空头文案。用户书面确认「全套方案」：VP 回退 active，Root 回退 active，新开 **GOAL-005-r4-mcp-docker-release**（R4），退出判据 #8 增补。 | 缺口核查与回退留痕：Root `03-audit/A-010`（响应）+ 03-audit 结论状态段；Root `00-meta` 备注；workspace.md；goal-tree.md（Root active 75% + GOAL-005）。 | 无（R4 完成后按退出判据 1–8 复关）。 |
| 2026-08-07 | **closed**（R4 增补后复关） | R4（GOAL-005）完成：通道资产分离（File zip 80 成员 / 0 MCP 实现 + 防御断言）；MCP server Docker 镜像同 tag 发布管线（workflow GHCR + 契约测试断言 `test_publish_job_pins_r4_docker_release_steps`）；`-Channel mcp` 薄装重定义；README 安装指南与实现一致。退出判据 1–8 证据链完整。 | GOAL-005 五件套（A-001 self + A-002 independent 均 pass；A-003 合并响应；E-001/E-002）；Root `03-audit/A-011-r4-reclose-self.md`；本文件 #8 路径字面修正（F-003：`skills/mcp/` → `mcp/`）；goal-tree（Root 及子目标全 done/100%）。 | I-007（GHCR 权限可达性）open（non-blocking）——首次真实 tag 发布验收时关闭（GOAL-005 A-001 R-002 / A-002 F-001）；真实 push 证据（digest/URL）回填 GOAL-005 `attachments/`。 |

## 规划修订短史

| date | change |
|------|--------|
| 2026-08-07 | **初创草案** `planned`：双通道（File+MCP）、四承诺宿主、四治理入口 + 可选 `commit`；R1 含最小共享测试内核；R2 产品化；R3 仅 `governance_root`；明确排除 Antigravity/Open Code 与 DB 波次。用户 `/vision` 讨论后确认落盘。 |
| 2026-08-07 | **VRev-007 响应**（v0.1.1）：R3 协议面变更车辆（V-F-013 A）；P0/P1 与约定级验证地板（V-F-014）；Charter 叙事选择不改 Charter（V-F-015）；R1 入口等价检查点（V-F-016）；退出判据 #4/#5 同步可判定表述。 |
| 2026-08-07 | **激活 + 挂区**（v0.2.0）：`status: active`；lead = `workspace-003-mcp-file-dual-channel`；Root `GOAL-001-mcp-file-dual-channel-delivery`；空转结束。 |
| 2026-08-07 | **关门**（v0.3.0）：`status: closed`；工作区完整关门（退出判据 1–7 证据链见 Root 03-audit A-007/A-008）；关门记录表填写。 |
| 2026-08-07 | **reopen → active**（v0.4.0）：发布面核查（用户指令）发现关闭范围外缺口——File zip 混入 `skills/mcp/` 源码、MCP 无 Docker 发布资产、README 无安装指南 + 空头文案；用户书面确认「全套方案」：VP/workspace/Root 回退 active，新开 GOAL-005-r4-mcp-docker-release（R4），退出判据 #8 增补。 |
| 2026-08-07 | **复关**（v0.5.0）：R4（GOAL-005）完成——退出判据 #8 满足（实现 + 发布管线 + 本地可构建证据层面；真实 GHCR push 属发布验收 I-007，non-blocking）；#8 路径字面 `skills/mcp/` → `mcp/`（F-003，语义不变）；Root/workspace 复关，本 VP `status: closed`；关门记录表增补复关行。 |
