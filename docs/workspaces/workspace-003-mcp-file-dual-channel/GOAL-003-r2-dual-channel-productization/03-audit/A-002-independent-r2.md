---
id: A-002
goal: GOAL-003-r2-dual-channel-productization
title: R2 方案冻结与双通道产品化 · 独立交叉审计
status: recorded
source: independent
provider: grok-build / grok-4.5 / thinking-high
date: 2026-08-07
scope: R2 方案冻结（D-001/D-002）、薄壳 lifecycle、bootstrap 双入口、gitignore+doctor、server lifecycle 工具、测试真实性、生产仓 File 自举证据、A-001 落盘与索引
verdict: conditional
version: 0.1.0
parent: null
---

# A-002 · R2 独立交叉审计（independent · grok-build / grok-4.5 / thinking-high）

## 结论

**verdict: conditional**。

R2 **产品实现与验证**经亲自读码与复跑测试后，与 D-001/D-002 主张大体一致：allowlist 写面、confirm 门禁、managed 标记边界、bootstrap `-Channel mcp|files`、lifecycle CLI 单一真相源、真实 server 进程测试与 PS 脚本执行均成立；生产仓 File 自举日志可核对。

阻断「无条件 pass」的主因是 **P-003 审计台账不完整**：`A-001` 自审文件已存在，但 `03-audit.md` 索引仍写「尚未到达审计节点 / 无正式意见」，且索引内信息就绪表与 `00-meta` 冲突。实现可推进闭合，但 C6 在响应本意见前须先修台账并处理 findings。

本意见 **不**修改 `status` / `progress` / 决策或方案正文；响应归 `/govern`。

## 范围与区间

| 项 | 内容 |
|----|------|
| 工作区 | `workspace-003-mcp-file-dual-channel`（`root_goal: GOAL-001-mcp-file-dual-channel-delivery`，`primary_plan: VP-004`） |
| 目标 | `GOAL-003-r2-dual-channel-productization` |
| audit_type | design-plan + execution-facts（R2 冻结 + 实现证据） |
| 日期 | 2026-08-07 |
| auditor | independent · provider = grok-build / grok-4.5 / thinking-high |

**已读（只读）**：workspace.md；GOAL-003 五件套索引与 ledger（D-001/D-002、E-002、A-001）；`skills/mcp/{lifecycle,doctor,server,gitignore-fragment}.txt`；`scripts/bootstrap/{install-online.ps1,.sh,README.md}`；`skills/tests/test_mcp_lifecycle.py`；`scripts/tests/test_bootstrap_install_online.py` 相关段；生产仓自举日志路径。

## 亲自复跑 / 独立核验摘要

| 核验 | 结果 |
|------|------|
| `python -m pytest docs/tests scripts/tests skills/tests -q` | **179 passed, 3 skipped, 4 subtests**（~33s）。A-001 记 178 passed → 计数轻微漂移，非红。 |
| `pytest skills/tests/test_mcp_lifecycle.py scripts/tests/test_bootstrap_install_online.py -q` | **16 passed, 1 skipped** |
| `lifecycle.py` 读码 + 临时目录脚本 | `MANAGED_PATHS_ALLOWLIST == {AGENTS.md, .goal-governance}`；`confirm=False` 拒绝且不写盘；`replace`/`remove` 只动标记内；`..` 与绝对仓外路径 `_ensure_inside_repo` fail closed；uninstall 后用户 preamble/suffix 保留；**doctor 源码无 `write_text`（只读）** |
| allowlist 接线 | `_ensure_inside_repo` 在 install/upgrade/uninstall 写路径上调用；**`_validate_allowlist` 未接入写路径**（见 R-001）— 写面由硬编码路径实现，行为上仍只写 allowlist |
| `install-online.ps1` | **UTF-8 BOM 存在**（EF BB BF）；`-Channel mcp` 仅 materialize `mcp/` + contracts，再调 `lifecycle.py install --confirm`；**不**装 docs/architecture / prompts 全量；stdout 同屏英文 File 一等声明 |
| `install-online.sh` | 同构 mcp 薄通道 + lifecycle CLI；中文 File 一等声明；默认 `CHANNEL=files` |
| `scripts/bootstrap/README.md` | 推荐 MCP **同表/同节**声明 File 仍一等、非日落 |
| `test_mcp_lifecycle.py` | **真实** `subprocess.Popen(server.py)` + JSON-RPC；**无** mock/MagicMock/patch |
| `test_bootstrap_install_online.py` mcp 用例 | **真实** `_powershell(-File install-online.ps1 -Channel mcp …)`；断言无 File 大包、managed 段、install.json、File 一等 stdout |
| 生产仓 File 自举 | 日志存在：`…\grok-goal-321201478208\implementer\file-bootstrap.log`（pack → files 完整安装 → 产物 True → `stage --check` ok → **7 passed** L1 File） |

## 成果（有证据）

| 主张 | 独立证据 |
|------|----------|
| D-001 薄壳 allowlist + confirm + markers | `lifecycle.py` 常量与写路径；测试 + 手工脚本 |
| D-002 bootstrap 双入口 | ps1/sh `-Channel`；README；PS 集成测试 + 文档契约测试 |
| doctor 只读 + gitignore 片段 | `doctor.py` 无写盘；`gitignore-fragment.txt` 含 `.goal-governance/`；doctor 启发式检测 |
| server 暴露 install/upgrade/uninstall/doctor | `server.py` `LIFECYCLE_TOOLS` + `_handle_lifecycle_call`；confirm 默认 false |
| bootstrap 与 lifecycle **无双份 marker 内联** | ps1/sh 调用 `lifecycle.py install`（单一真相源）；仅 materialize 复制步骤重复 |
| 测试非 theater | 真实 server 进程 + 真实 PS bootstrap；全量 pytest 绿 |
| File 自举 | 上述 log 可指回路径与步骤 |

## 对照成功标准（C1–C5 实现面）

| 检查点 | 独立判断 |
|--------|----------|
| C1 双入口 + 推荐/File 一等 | **满足**（脚本 + README + 测试） |
| C2 lifecycle allowlist + confirm | **满足**（硬编码写面 + confirm；见 R-001 接线完整性） |
| C3 gitignore + doctor | **满足**（片段 + 只读 doctor；gitignore 为启发式，见 R-003/self） |
| C4 managed 标记边界 | **满足**（函数 + 测试 + 手工） |
| C5 File-classic + 生产仓自举 | **满足**（files 通道测试 + log） |
| C6 self+independent + required 闭合 | **未完成**（本意见为 independent 一环；索引缺口 = 开放 required；闭合归 `/govern`） |

## Findings

### F-001 · required · med · P-003 台账：A-001 未入索引且索引自相矛盾

- **证据**：
  - 文件存在：`03-audit/A-001-r2-freeze-and-implementation-self.md`（`source: self`，`verdict: pass`，格式可用）。
  - 索引 `03-audit.md`（审计前状态）意见表为「— / 尚未到达审计节点」，结论写「当前无正式 Goal Audit 意见」；信息就绪表仍标 I-001～I-003 **open**，与 `00-meta.md` / D-001·D-002 **closed** 冲突。
- **要求**：编排器响应时更新 `03-audit.md`：登记 **A-001** 与 **A-002**、修正信息就绪核对表、改写结论；未登记的 A 条目不得当作「已正式入账可放行」的完整台账。
- **闭合路径**：`fixed`（改索引与表）即可；不要求改实现代码。

### R-001 · recommended · low · `_validate_allowlist` 未接入写路径

- **证据**：`install`/`upgrade`/`uninstall` 源码含 `_ensure_inside_repo`，**不含** `_validate_allowlist` 调用；写面靠硬编码 `AGENTS.md` / `.goal-governance`。
- **影响**：运行时行为仍只写 allowlist；单元测试直接测 helper 易被误读为「写路径动态校验」。非绕过、非证据造假。
- **建议**：写路径显式调用 `_validate_allowlist`，或文档标明「allowlist = 硬编码写集 + 仓内校验」。

### R-002 · recommended · low · doctor 合同路径与薄 MCP 落点不一致

- **证据**：bootstrap mcp 将合同装到 `skills/contracts/…`；`doctor.py` 查 ` {governance_root}/contracts/skills-consumer-contract.json`（默认 `docs/contracts/…`）。薄装后 `contract.present` 常为 false（代码已注明可选、不参与 `ok`）。
- **建议**：doctor 同时探测 `skills/contracts/`，或文档写清薄通道期望路径，避免运维误判。

### R-003 · recommended · low · bash `-channel mcp` 缺与 PS 对等的端到端用例

- **证据**：`test_mcp_channel_bootstrap_installs_thin_shell_only_…` 仅跑 **PowerShell**；bash 侧为结构声明 +（若有 bash）默认 **files** 离线安装；mcp 薄通道在 bash 上依赖结构对称 + lifecycle CLI，无独立 e2e。
- **建议**：在 bash 可用环境增加 `--channel mcp` 集成测试（可 skip）。

### R-004 · recommended · low · 自审计数与复跑不一致

- **证据**：A-001 写「178 passed」；本审复跑 **179 passed** / 3 skipped / 4 subtests。
- **建议**：闭合时以最新复跑为准刷新执行/审计数字。

### 与 A-001（self）的异同

| 维度 | A-001 self | A-002 independent |
|------|------------|-------------------|
| 实现与测试真实性 | pass，无 required | **同意**：非 mock、PS 真跑、lifecycle 行为成立 |
| 生产仓自举 | 引用 scratch log | **同意**：log 存在且步骤完整 |
| P-003 索引 | 自审落盘但未更新索引 | **升为 required F-001** |
| allowlist 接线 | 未强调 helper 未接入 | **R-001** |
| doctor 合同路径 | 未记 | **R-002** |
| verdict | pass | **conditional**（台账 required 未闭） |

## 必改项汇总

1. **F-001（required）**：补全 `03-audit.md` 索引（A-001 + A-002）并同步信息就绪表/结论，满足 P-003 正式台账。

无其他 required。未发现：allowlist 可写任意仓内路径绕过、confirm=false 仍写盘、uninstall 删标记外用户正文、测试以 mock 顶替真实 server/PS、mcp bootstrap 内联第二套 marker 逻辑与 lifecycle 漂移、doctor 写盘、生产仓自举 log 伪造。

## 建议给编排器 / 用户的下一步

1. `/govern` 响应 A-002：先 **fixed** F-001（只动审计索引/表，不必改产品代码）。
2. 按需接纳 R-001～R-004（可 residual / 后续目标）。
3. required 清空后闭合 C6 → R2 检查点 commit（若流程需要）。
4. **不要**用 `progress: 83%` 放行或关门。

## 声明

- `source: independent`；provider = grok-build / grok-4.5 / thinking-high。
- 本意见只追加审计 ledger，**不**修改目标 `status` / 检查点 / 派生 `progress` / 方案正文 / goal-tree 状态列。
- 响应、finding 闭合与阶段推进由 **`/govern`** 处理。
