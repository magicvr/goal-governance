---
id: A-002
goal: GOAL-002-r1-mcp-equivalence-kernel
title: R1 方案冻结与双通道实现 · independent 交叉审计
status: recorded
source: independent
provider: grok-build / grok-4.5 / thinking-high
date: 2026-08-07
scope: R1 方案冻结（D-002/D-003/D-004 / I-001～I-003）、skills/mcp 实现、deliveryChannel 合同分列与镜像、L1/L2 测试、四宿主 L3 探针证据；C4 independent 审视
verdict: pass
version: 0.1.0
---

# A-002 · R1 independent 交叉审计（2026-08-07）

## 结论

**verdict: `pass`**

独立复跑测试与 stage 校验、抽查实现与 L3 原始 stdout/sha256 后：R1 方案冻结主张、MCP/File 分列证据、合同 0.4.0 分列与镜像、L3 四宿主探针（marker + 四入口名 + 非空输出）均可核对；**未发现证据造假、MCP mock 顶替 File、合同镜像漂移、或 `tools/call` 写盘**。

本意见 **不** 关闭 C4、**不** 将目标标 `done`、**不** 放行 R2。C4 需编排器响应本条 findings（若有 required 则先闭合）后，再由 `/govern` 更新检查点/status。

- **auditor**：grok build · 模型 grok-4.5 · 思考强度 high  
- **source**：`independent`  
- **类型**：execution-facts + design-plan（R1 方案冻结 + 实现与验证证据）

## 独立核验（亲自执行）

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests scripts/tests skills/tests -q` | **168 passed**, 3 skipped, 4 subtests passed（~28s） |
| `python scripts/stage_skills_mirrors.py --check` | **ok**: skills mirrors match docs/（36 pairs） |
| 合同 canonical↔`skills/contracts` 字节比对 | `skills-consumer-contract.json` / schema / matrix 镜像 **byte-identical**；`contractFormatVersion=0.4.0`；`deliveryChannels: files \| mcp` |
| L3 JSON×4 | claude / grok / codex / copilot：`verdict=pass`，`markerObserved=true` |
| L3 stdout×4 | marker 均在 stdout；均含 `vision` / `vision-audit` / `govern` / `audit`；`stdoutSha256` 与文件内容一致 |
| L3 `behaviorSources` sha256 vs 当前树 | 四 prompt + `entries.py` / `kernel.py` / `server.py` **全部 match**（无捕获后漂移） |
| MCP 真进程抽查 | 工具集恰好四名；`commit` 未暴露；`audit`/`vision-audit` `readonly=true` 且 `writesTo` 台账边界符合 D-002；临时目录无新增文件 |

## 证据（可指回）

| 主张 | 独立判断 | 证据路径 |
|------|----------|----------|
| I-001 关闭（运行时 + 四入口映射） | **成立** | `01-decision/D-002-*.md`；`skills/mcp/{entries,server}.py` 与 D-002 表一致 |
| I-002 关闭（L2 内核 + 合同分列） | **成立** | `01-decision/D-003-*.md`；`kernel.py`；`docs/contracts/*` 0.4.0；`test_dual_channel_l2.py` / `test_contract_delivery_channels.py` |
| I-003 关闭（provider） | **成立** | `01-decision/D-004-*.md`；本条即该 provider 落盘 |
| I-004 关闭（四宿主 L3） | **成立（抽稀）** | `attachments/runtime/evidence/*-l3-four-entry-2026-08-07.json` + `.d/stdout.txt` |
| L1 MCP 真进程、非 mock | **成立** | `skills/tests/test_mcp_l1.py` 子进程启动 `server.py`；无 `unittest.mock` |
| L1 File 真资产、无 MCP mock 顶替 | **成立** | `docs/tests/test_file_l1.py` 直接读 `skills/prompts/*`、install 面、合同 `files` 分列 |
| `tools/call` 不写治理文件 | **成立** | `server.py::handle_tools_call` 仅读 prompt 算 sha256 并写 stdout JSON；现场抽查无写盘 |
| A-001（self）落盘格式 | **符合** P-003 最低字段 | `source`/`date`/`scope`/`verdict`/findings；索引表有 A-001 |

### 实现 vs D-002 对照（亲自读代码）

| D-002 要求 | 代码事实 |
|------------|----------|
| Python 3 stdio、换行 JSON-RPC 2.0 | `server.py` `_read_message` / `_write` |
| 四工具：vision / vision-audit / govern / audit | `entries.ENTRYPOINT_NAMES` + `tool_definitions()` |
| 关键参数边界（audit 必填 `goal_id` 等） | `TOOL_PARAMETERS`；缺参 → `-32602` |
| `commit` 不暴露 | `tools/list` 仅四名；`tools/call commit` 拒识 |
| audit / vision-audit 只读 dispatch | `READONLY_DISPATCH_ENTRIES`；`structuredContent.readonly=true` |
| 实例真相在仓内 | 元数据声明 + `writesTo` 仅 ledger 路径提示；server 自身不写 |

## Findings

### required findings

**无。**

### recommended（非阻断 · 建议 `/govern` 响应）

| ID | 严重度 | 说明 | 可核对修正建议 |
|----|--------|------|----------------|
| **R-001** | med | **L2 深度分层**：`kernel.describe_*` 对角色文本、`ledger_targets`、`fail_closed`/`single_charter`/`workspace_roles` 等多取自 `entries.py` 同源常量或硬编码声明；`check_equivalence` 对 CP2–4/5–9 的「两通道一致」有相当部分是 **SSOT 自洽**，而非从 File prompt 正文与 MCP `tools/list` **双侧独立抽取**后再比。CP1（真 prompt 存在 + 真 tool 存在）与 L1 分列测试承担了主要真实通道证据。与 A-001 self R-001 同向，独立侧升格为「L2 语义深度」说明。 | 在 D-003/README 或 `kernel.py` 文档明确：哪些检查点是「SSOT 防漂移」、哪些是「双侧资产抽取」。可选增强：File 侧从 prompt 正文/ frontmatter 抽取角色关键词；MCP 侧仅从 `tools/list` description/schema 抽取后再比。**不**要求为 R1 重写整核。 |
| **R-002** | low | **台账/正文陈旧句**：`00-meta.md`「实施前治理门禁」仍写 provider 未指定、未实施放行；Root `GOAL-001` `00-meta` 路线图表仍写「方案未冻结」、备注仍写 provider 待指定——与信息表 **closed** 及 D-002～D-004 矛盾。`E-002` 进度评估仍写 I-004 待探针，而 meta/索引已 closed。 | `/govern` 刷新过时 prose；L3 捕获可补 `E-003` 事实条（证据已在 attachments，不构成造假）。 |
| **R-003** | low | **L3 通道面**：四宿主探针 prompt 为 File/宿主 skill 面（`/govern` 四入口角色核对），**不是**宿主作为 MCP 客户端连接 `skills/mcp/server.py` 的 stdio 路径。MCP 通道运行证据主要在 L1 真进程 + L2。符合 VP-004「抽稀」字面，但合同标注 L3 时宜写清「宿主入口面 / MCP 进程面」覆盖边界。 | 在 I-004 证据备注或合同 `deliveryChannels[].notes` 标明 L3 探针面；MCP 宿主绑定 L3 可 defer 到 R2 产品化或 residual。 |
| **R-004** | low | `skills/mcp/README.md`「目录」表列出 `lifecycle.py` / `doctor.py` / `config.py`（R2/R3），当前目录不存在；L3 路径表述指向 `docs/releases/runtime/`，本目标证据实际在 `attachments/runtime/evidence/`。 | 标注「计划 / 非 R1」或改指向真实证据路径，避免读者以为已交付。 |

## 与 A-001（self）的异同

| 点 | self A-001 | independent A-002 |
|----|------------|-------------------|
| verdict | pass | **pass**（独立复跑后确认） |
| required | 无 | **无** |
| 测试/镜像 | 声称 168 / stage ok | **亲自复跑一致** |
| L3 | 四宿主 pass | **stdout/sha/marker/入口名亲自核对；behaviorSources 哈希未漂移** |
| L2 同源角色 | R-001 recommended | **R-001 保留并扩展**（含声明式 CP 深度） |
| 文档陈旧句 | 未强调 | **R-002** |
| L3 通道边界 | R-003（他机/CI） | **R-003**（File 宿主面 vs MCP 进程面）；CI 他机仍不在本证据范围 |

## 必改项汇总

- **required：无。**  
- recommended：R-001～R-004（见上），不阻断将 C4 在「响应 recommended 或书面接受」后继续推进；编排器不得把 recommended 静默当 required 阻断，也不得把本 `pass` 直接改写成目标 `done`（C4 闭合与检查点更新属 `/govern`）。

## 结论 + 建议给编排器/用户的下一步

1. 用 **`/govern`** 响应 A-002：确认无 required；对 R-001～R-004 选择修正 / 接受残余 / 记入后续阶段。  
2. 响应后更新 GOAL-002 C4 检查点与（若适用）goal-tree；**勿**在本 independent 意见中改 status。  
3. Root R1 阶段门禁：子目标 C4 合法闭合后，再审 Root 纲领 R1 是否可标完成（见 Root A-002）。  
4. R1 检查点 git commit 仍建议在 independent 响应完成后进行（self A-001 边界一致）。

## 声明

本意见 `source: independent`，**不**修改任何目标 `status` / `progress` / 方案正文 / goal-tree 状态列；响应、finding 闭合与推进由 **`/govern`** 处理。
