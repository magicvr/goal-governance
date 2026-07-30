---
id: GOAL-023-skills-core-dual-asset-install
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.4.0
---

# 审计 · GOAL-023

## 信息就绪核对（按 scope）

| 核对项 | 状态 | 备注 |
|--------|------|------|
| 影响本 scope 的 I-00N | I-001～I-004 **closed**（D-002） | 阶段 C～E 无新增 required 信息门禁 |
| 到期 required 是否已 verified / residual | 是（策略已决） | 实现证据见阶段 B 单测；关门 scope 无到期开放 required |
| 资料引用（若有）是否固定且用户确认 | 无 | — |
| 工作区绑定 | OK | `workspace-001-goal-governance` · Root `GOAL-001-main-vision` · `plan_refs`/`primary_plan` = VP-001 |

## 意见台账索引

| ID | 日期 | source | scope | verdict | 开放必改 |
|----|------|--------|-------|---------|----------|
| A-001 | 2026-07-30 | independent | GOAL-023 C～E 交付、回归与关门前检查 | conditional | F-001 曾 required；现 **fixed**（见 A-002/A-003） |
| A-002 | 2026-07-30 | independent | F-001 finding-closure 复审；GOAL-023 关门前回归证据 | pass | 无；F-001 **fixed** |
| A-003 | 2026-07-30 | self | 响应 A-001/A-002；F-001 关闭证据 | pass | 0 |
| A-004 | 2026-07-30 | self | close-out 目标整体 A～F | pass | 0 |

---

## A-001 · 双资产与双入口关门前独立交叉审计（2026-07-30）

- **source**：independent
- **auditor**：GitHub Copilot
- **类型** / **scope**：execution-facts / close-out precheck；GOAL-023 阶段 C～E、双资产打包、bootstrap 离线安装、文档与 CI 发布挂接。
- **verdict**：conditional

### 范围与区间

- 工作区：`workspace-001-goal-governance`；Root 为 `GOAL-001-main-vision`，canonical 范围为 `docs/workspace-001-goal-governance/`，与本目标的 parent 一致。
- 本 scope 无共享资料固定引用。I-001～I-004 均为 `closed`；其中 I-004 的同版本 core-only 与 skills 内嵌 core 字节一致性由下列单测覆盖。
- 审计不改 `00-meta` status/progress、决策、执行记录或 `goal-tree.md`。

### 成果（有证据）

- `scripts/tests/test_pack_core_release.py`：6 passed。覆盖 core-only zip + digest、`tech-stack.md` 排除、完整性拒绝，以及 core-only 成员与 skills zip `core/` 成员逐字节一致（I-004）。
- `scripts/tests/test_bootstrap_install_online.py`：5 passed，1 skipped。PowerShell 离线 bootstrap 成功安装 core 与至少一个宿主入口；摘要不匹配时在安装前失败关闭。bash 完整脚本有结构断言；本机 WSL 无可用 bash 发行版，离线 e2e 按 `R-023-BASH-HOST` skip。
- `scripts/tests/test_pack_skills_release.py`：6 passed，1 skipped。既有 skills pack 仍含内嵌 core；Windows 无创建 symlink 权限，symlink 拒绝用例 skip。
- `.github/workflows/skills-pack-release.yml` 明确打包并上传 skills/core zip 与各自 digest、两个 bootstrap 脚本；发布上传步骤还 fail-closed 要求双 zip 和双 digest。

### 对照成功标准

- 双资产命名、core-only 内容边界、skills 内嵌 core 与 digest 校验均有实现和自动化证据。
- PowerShell bootstrap 的绝对本地路径流程及摘要失败关闭有可重复测试证据。
- CI 资产集合和发布上传门禁与 D-002 的双入口、同版本双资产模型一致。

### Findings

#### F-001 · 文档示例的相对 `-ZipPath` 与 `-TargetDir` 组合不可执行

- **级别**：required；**严重度**：medium
- **影响范围**：阶段 C 的离线 bootstrap 用户路径；阶段 D 文档准确性；阶段 F 关门。
- **证据**：`scripts/bootstrap/README.md` 的离线 PowerShell 示例同时使用 `-TargetDir C:\path\to\empty-project` 和相对 `-ZipPath dist\goal-governance-skills-v0.0.0-testpack.zip`。但 `scripts/bootstrap/install-online.ps1` 的 `Resolve-FullPath $ZipPath $TargetDir` 将相对 zip 路径解析为 `<TargetDir>\dist\...`。独立隔离复现把 zip 放在调用目录的 `pack/`、目标仓设为其 sibling `consumer/` 后，报错 `ZipPath not found: ...\consumer\pack\goal-governance-skills-v0.0.0-audit.zip`。
- **风险**：按发布文档从维护仓或下载目录运行 bootstrap、同时指定另一个消费目标仓时会在摘要校验前失败；现有成功测试传绝对 `ZipPath`，未覆盖该文档组合。
- **要求的闭合证据**：由 `/govern` 选择并记录一种明确契约，再提供回归测试：
	- 将文档中的 `ZipPath` / `Sha256Path` 改为绝对路径或位于 `TargetDir` 下的路径；或
	- 调整脚本使相对 zip / digest 路径相对调用目录解析，并覆盖该行为。

### 必改项汇总

- **F-001**：在阶段 F 关门前闭合。当前没有用户书面 residual 或 overruled 决定，故不得以本意见无条件关门。

### 与既有意见的异同

- 本目标此前无 self 或 independent 正式意见。本意见认可 A～E 已有的自动化成果，但独立发现文档所示离线参数组合与 PowerShell 实现的路径基准不一致。

### 结论 + 建议给编排器/用户的下一步

结论为 **conditional**：核心双资产、摘要 fail-closed、PowerShell 离线主路径与 CI 挂接具有可核验证据；但 F-001 是影响实际离线安装说明的 required 缺口。建议 `/govern` 先选择路径语义并修正文档或实现，加入相应回归；随后复审 F-001，再进行 self close-out 和用户关门确认。

### 声明

本意见不修改 status/progress；响应、finding 闭合与阶段推进由 `/govern` 处理。

---

## A-002 · F-001 修复复审与关门前证据复核（2026-07-30）

- **source**：independent
- **auditor**：GitHub Copilot
- **类型** / **scope**：finding-closure / close-out precheck；复审 A-001 F-001，并抽检 GOAL-023 双资产、bootstrap、CI 与文档证据。
- **verdict**：pass

### 范围与区间

- 工作区仍为 `workspace-001-goal-governance`；Root `GOAL-001-main-vision`、canonical 范围和本目标 `parent` 一致。无共享资料固定引用。
- I-001～I-004 均为 closed；其中 I-004 的同版本 core-only 与 skills 内嵌 core 字节一致性在本次回归中重新验证。
- 本次仅复审审计意见及可执行证据；不改目标 `status`、`progress`、方案正文或 `goal-tree.md`。

### 成果（有证据）

- `scripts/bootstrap/install-online.ps1` 将相对 `-ZipPath` 与 `-Sha256Path` 明确解析为进程 CWD；`install-online.sh` 对 `--zip-path` 与 `--sha256-path` 使用同一契约。`scripts/bootstrap/README.md` 已据此更正离线示例。
- `scripts/tests/test_bootstrap_install_online.py` 的 `test_offline_relative_zip_resolved_against_cwd_not_target` 实际运行 PowerShell bootstrap，覆盖 CWD 下相对 zip/sidecar 与不同空 `TargetDir` 的组合并通过；摘要不匹配 fail-closed 与成功安装路径同轮通过。
- 聚焦 bootstrap 回归：**6 passed, 1 skipped**；跳过项为本机 WSL 无可用 bash 发行版，符合 `R-023-BASH-HOST` 的既有 non-blocking 残余，bash 完整脚本结构断言通过。
- 双资产 pack 回归：**12 passed, 1 skipped**；包括 I-004 core-only 与 skills 内嵌 core 字节一致性。跳过项为 Windows 无 symlink 创建权限的既有防御性用例。
- 文档/工作区/愿景契约回归：**26 passed**。CI 产物约束在 bootstrap 测试中检查，覆盖 skills/core zip 与 digest、两个 bootstrap 脚本的挂接。

### 对照成功标准

- A～E 的成功标准都有实现路径与聚焦自动化证据；在线默认仍仅下载内嵌 core 的 skills zip，未引入单独 core 网络依赖。
- 双入口文档与脚本路径语义一致；bootstrap 在摘要错误时先失败，未从坏包安装。
- 阶段 F 的独立审计要求已满足；本意见不替代 `/govern` 的响应流程、任何自审选择或用户关门确认。

### Findings

#### F-001 · 文档示例的相对 `-ZipPath` 与 `-TargetDir` 组合不可执行

- **原级别**：required；**严重度**：medium
- **闭合状态**：**fixed**
- **闭合证据**：`02-execution.md` 的“Bootstrap 相对路径修复（skeptic）”记录了 CWD 解析契约、PS/bash 对齐与新增回归；本次重新执行 `test_offline_relative_zip_resolved_against_cwd_not_target` 并通过。脚本和 `scripts/bootstrap/README.md` 的契约也一致。
- **复审结论**：A-001 所述的 `TargetDir\\pack-here` 错误解析不再可复现；相对路径与不同目标仓组合已被直接覆盖。

### 必改项汇总

- 无开放 required finding。A-001 的 F-001 已按 `fixed` 路径闭合；本审计未发现新的 required finding。

### 与既有意见的异同

- A-001 的 conditional 结论仅因 F-001 的路径基准不一致而受限。本复审确认修复、文档和回归三者一致，因此针对相同关门前 scope 给出 pass，不构成冲突。

### 结论 + 建议给编排器/用户的下一步

结论为 **pass**：GOAL-023 目前无开放 required finding，已登记 I-00N 不阻断关门。请使用 `/govern GOAL-023` 汇总 A-001/A-002、询问是否需要 self close-out，并在用户确认后决定是否标记 `done`。`R-023-BASH-HOST` 仍为 non-blocking 环境残余，应在可用 bash/CI Linux 环境复审，但不阻断本目标当前关门门禁。

### 声明

本意见不修改 status/progress；响应、finding 闭合与阶段推进由 `/govern` 处理。

---

## A-003 · 响应 A-001 / A-002 · F-001 关闭证据（2026-07-30）

- **source**：`self`
- **auditor**：`/govern` 编排器（Grok Build）
- **类型**：`response`
- **scope**：A-001 F-001 与 A-002 复审结论；不替代独立审
- **verdict**：`pass`（相对「F-001 是否已按 fixed 合法闭合」）

### 关闭证据表

| Finding / 意见 | 闭合路径 | 证据 |
|----------------|----------|------|
| A-001 **F-001** | **fixed** | 相对 `-ZipPath`/`--zip-path`（及 sha 路径）相对**进程 CWD** 解析：`scripts/bootstrap/install-online.ps1`、`install-online.sh`；`scripts/bootstrap/README.md` 契约与示例；`02-execution`「Bootstrap 相对路径修复」；单测 `test_offline_relative_zip_resolved_against_cwd_not_target` |
| A-002 | 独立复审 **pass** | A-002 确认 F-001 不可复现旧错误路径；本拍关门前复跑见 A-004 |

### 仍开放项（A-003 出具时 · 关门前）

- 阶段 F 自审 + 用户确认 `done` → 见 **A-004**（用户本拍确认路径 **OK A**）
- residual **R-023-BASH-HOST**（non-blocking；Windows 无可用 bash 时 e2e skip + 结构断言）

### 冲突

- 无。A-001 `conditional` 仅因 F-001；A-002 为同 scope 复审 **pass**，与 fixed 路径一致。

### 声明

本条为编排响应记录，**不是** `source: independent` 复审。

---

## A-004 · self close-out · 阶段 F（2026-07-30）

- **source**：`self`
- **auditor**：`/govern` 编排器（Grok Build）
- **类型**：`close-out`
- **scope**：GOAL-023 目标整体（阶段 A～F：方案冻结、core-only 资产、在线 bootstrap、文档双入口、CI 挂接、F-001 响应、回归与成功标准）
- **verdict**：`pass`

### 范围与区间

- **覆盖**：D-001/D-002；纲领 A～F；I-001～I-004 closed；A-001/A-002/A-003；关门前聚焦回归；成功标准勾选。
- **不覆盖**：annotated tag / GitHub Release；Root / Charter / VP status；「always latest core」热更；静默覆盖消费仓 `docs/architecture`；R-023-BASH-HOST 在可用 bash/CI Linux 上的 e2e 强制通过。
- **与既有意见**：与 A-001 **无冲突**——required F-001 已 **fixed**；A-002 independent **pass**。progress 未作放行证据。
- **用户裁决**：本拍确认 **OK A**（需要 self close-out 后再关门）。

### 信息就绪核对

| 核对项 | 状态 |
|--------|------|
| I-001～I-004 | closed |
| 到期 required I | 0 |
| 开放 required finding | 0（F-001 fixed） |
| 资料引用 | 无 |
| R-023-BASH-HOST | non-blocking residual；不阻断关门 |

### 成果（有证据 · 关门前复跑 2026-07-30）

| 套件 | 结果 |
|------|------|
| `scripts.tests.test_pack_core_release` + `test_bootstrap_install_online` + `test_pack_skills_release` | **20** ran · **OK**（**2 skipped**：WSL bash stub；symlink 权限） |
| `docs/tests` | **26** OK |
| `skills.tests.test_skills_orchestrator` | **39** OK |
| 含 F-001 回归 | `test_offline_relative_zip_resolved_against_cwd_not_target` **ok** |

### 对照成功标准

| 成功标准 | 状态 | 证据 |
|----------|------|------|
| 产品模型冻结（双资产命名/版本、bootstrap 契约、与 D-003 关系） | 达成 | D-002；I-001～I-003 closed |
| core-only 打包入口（zip + SHA-256；D-004 级子集） | 达成 | `scripts/pack_core_release.py` + 单测 6 |
| skills zip 仍内嵌 core；包内 install 离线完整 | 达成 | pack skills 测试；I-004 字节一致断言 |
| 在线 bootstrap PS 完整 + bash 完整脚本；校验 → install `-All` | 达成 | bootstrap 脚本 + 离线单测；bash 结构断言 + R-023-BASH-HOST |
| 根 README / skills README / releases 双入口 | 达成 | 文档契约单测 + 手维路径见 02-execution |
| CI/pack/release 可挂双资产 + bootstrap | 达成 | `skills-pack-release.yml` 契约单测 |
| 独立审计通过 + 用户确认关门 | 达成 | A-001/A-002 independent；A-003 响应；本 A-004；用户 **OK A** |

### Findings

本 close-out **无新增 required**。

#### R-023-BASH-HOST · bash 离线 e2e 环境残余（non-blocking）

| 字段 | 值 |
|------|-----|
| **级别** | non-blocking residual（既有） |
| **状态** | open · 不阻断关门 |
| **说明** | Windows 本机 bash 可能为无 distro 的 WSL stub；`install-online.sh` 已完整交付并有结构断言；e2e 在 usable bash 上跑否则 skip |
| **复审触发** | CI Linux 或装好的 bash 环境跑 `install-online.sh` 离线 e2e |

### 必改项汇总（required）

- 无开放 required。

### 结论与下一步

- **一句话结论**：GOAL-023 成功标准已满足；open required = 0；可 `done / 100%`。
- **不构成**：自动 tag/Release；Root/VP `done`；R-023-BASH-HOST 已消除。
- **建议**：同步 meta / goal-tree `done`；路径 D 后续工作另开 GOAL-024+；可选在 CI Linux 强化 bash e2e。
- **声明**：self close-out；独立意见 A-001/A-002 已汇总；本条非 independent 复审。
