---
id: A-002
goal: GOAL-004-r3-configurable-governance-root
title: R3 方案冻结与 governance_root 实现 · independent 交叉审计
status: recorded
source: independent
provider: grok-build / grok-4.5 / thinking-high
date: 2026-08-07
scope: R3 方案冻结（D-001/D-002）、config 解析实现与 schema、doctor 接线、canonical 权威面修订与镜像、C1–C4 测试与 v0.13.0 runtime evidence 抽查；C5 independent 审视
verdict: pass
version: 0.1.0
---

# A-002 · R3 independent 交叉审计（2026-08-07）

## 结论

**verdict: `pass`**

独立复跑全量测试与 stage 校验、亲自读 `config.py` fail closed 分支、抽查 alignment MCI 相对化、doctor `governanceRootError` 接线，以及 3 条 v0.13.0 runtime evidence 的 `verdict`/`behaviorSources` 哈希后：R3 方案冻结主张、解析实现、canonical 权威面相对化与镜像一致性、C1–C4 可核对证据均可成立。**未发现**解析绕过 fail closed、canonical 权威 MUST 表仍裸硬编码无例外、镜像漂移、证据哈希不匹配或测试整批 theater。

本意见 **不** 关闭 C5、**不** 将目标标 `done`、**不** 改 `status`/`progress`/方案正文。C5 需编排器响应本条 findings 后由 `/govern` 处理检查点与合法闭合。

- **auditor**：grok build · 模型 grok-4.5 · 思考强度 high  
- **source**：`independent`  
- **类型**：design-plan + execution-facts（R3 方案冻结 + 实现与验证证据）

## 范围与区间

| 项 | 内容 |
|----|------|
| 工作区 | `workspace-003-mcp-file-dual-channel` · Root `GOAL-001-mcp-file-dual-channel-delivery` · `vision_role: delivery` · `primary_plan: VP-004-…` |
| 被审目标 | `GOAL-004-r3-configurable-governance-root` |
| 决策 | `D-001`（配置/解析）、`D-002`（canonical 改写清单） |
| 实现 | `skills/mcp/config.py`、`governance-root.schema.json`、`doctor.py` |
| 权威面 | `docs/vision/alignment.md`、`docs/architecture/workspace-protocol.md`、根 `AGENTS.md` 0.13.0、相关 templates |
| 验证 | `test_mcp_config.py`、`test_governance_root_canonical.py`、全量 pytest、`stage_skills_mirrors.py --check`、v0.13.0 evidence 抽查 |
| 既有 self | `03-audit/A-001-r3-freeze-and-implementation-self.md`（verdict pass；索引当时未登记——见 R-001） |

## 独立核验（亲自执行）

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests scripts/tests skills/tests -q` | **194 passed**, 4 skipped, 4 subtests passed（~36.5s） |
| `python scripts/stage_skills_mirrors.py --check` | **ok**: skills mirrors match docs/（36 pairs） |
| `python scripts/compatibility_report.py --require-ready` | **coverage status: ready-for-release-evidence** |
| 亲自读 `skills/mcp/config.py` | 默认 `docs`；`.goal-governance.json` 覆盖；绝对路径 / `..` / 空串 / 非法 JSON / 非对象 → `GovernanceRootError`；`resolve()` + `relative_to` 防越界 |
| 手工临时仓复现 fail closed | 绝对路径、`../out`、`a/..`、非法 JSON 均 raise；默认与 override 正确 |
| doctor 接线 | 非法 JSON → `governanceRootError` 非空、`ok=False`、issues 含 `governance_root resolution failed`；合法 pin → `governanceRoot=governance`、err=None |
| R3 专项测试 | `test_mcp_config` **9** 条 + `test_governance_root_canonical` **6** 条 = **15** 全绿（非 E-002/A-001 所称 10+8） |
| alignment MCI 表 | 路径列均为 `` `{governance_root}/…` ``；定义节含默认 docs、`.goal-governance.json`、fail closed、monorepo 固定 docs 例外 |
| 镜像字节抽查 | `alignment.md`、`workspace-protocol.md` canonical ↔ `skills/core/docs/…` **byte-identical** |
| v0.13.0 evidence ×12 | 全部 `result.verdict=pass` |
| behaviorSources 哈希抽查 ×3 | `grok-build-cli-govern`、`claude-code-cli-audit`、`github-copilot-cli-vision` 所列源文件（含 `AGENTS.md` = `449cd566…`）**全部 match** 当前树 |
| A-001 落盘字段 | 文件内 `source/date/scope/verdict/findings` 齐全；**索引表当时未登记 A-001** |

### 实现 vs D-001 对照（亲自读代码）

| D-001 要求 | 代码事实 |
|------------|----------|
| pin 载体 `.goal-governance.json`，缺文件/缺字段 → `docs` | `load_project_config` / `resolve_governance_root` 成立 |
| 绝对路径 fail closed | `_validate_root_name`：`is_absolute`、`/`/`\` 前缀、盘符 `X:` |
| `..` 越界 fail closed | 路径分段含 `..` 或 `""` 即拒；另 `resolve().relative_to(repo)` |
| 非法 JSON fail closed | `json.JSONDecodeError` → `GovernanceRootError` |
| schema 随包 | `skills/mcp/governance-root.schema.json`；pattern 拒 `..` 与绝对形 |
| 内部布局冻结 | **协议+配置面**：只配置根前缀，无 API 改内部名；**测试**仅为「配置根下可承载约定形状」演示（见 R-003） |
| doctor 报告解析失败 | `governanceRootError` + issues；失败时 fallback 字符串 `"docs"` 仅用于继续收集其它诊断，`ok=False` |

### canonical vs D-002 / C4

| 清单项 | 独立判断 |
|--------|----------|
| `alignment.md` 治理根定义 + MCI 相对化 + 例外 | **成立** |
| `workspace-protocol.md` 定义 + 术语/路径相对化 | **成立** |
| 根 `AGENTS.md` §1 表 + 治理根定义（0.13.0） | **成立**；§6c/§8c 等仍有 monorepo/生产语境裸 `docs/`（定义句声明相对化 + monorepo 固定 docs 例外；**非** MCI 级裸硬编码） |
| templates（workspace-context / charter / vision-plan / goal-folder 00-meta） | **成立**（`{governance_root}/…`） |
| stage `--check` | **通过** |
| `consumer-checklist.md` | 已用 `{governance_root}/…`（A-001 R-002 对该文件的「仍写 docs/」判断**不成立**） |
| `standalone-bootstrap.md` | 顶部有治理根说明 + 源→目标对照表；拷贝命令仍以 monorepo 源 `docs/` 为默认示例（可接受；见 R-006） |

## 证据（可指回）

| 主张 | 独立判断 | 证据路径 |
|------|----------|----------|
| I-001 关闭（配置 schema + 解析） | **成立** | `01-decision/D-001-*.md`；`skills/mcp/config.py`；`skills/tests/test_mcp_config.py` |
| I-002 关闭（canonical 清单） | **成立** | `01-decision/D-002-*.md`；alignment/protocol/AGENTS/templates 正文；`docs/tests/test_governance_root_canonical.py` |
| C1 解析 + fail closed | **成立** | 上表手工 + 单元测试；**布局冻结机读断言偏弱**（R-003，非阻断） |
| C2 pin 载体 | **成立** | `.goal-governance.json` + schema；doctor 消费解析结果 |
| C3 canonical + 镜像 | **成立** | 相对化正文 + stage check + 镜像字节一致 |
| C4 无裸硬编码（权威面） | **成立（按 D-002 范围）** | canonical 测试 6 绿；MCI/协议/§1 表已相对化 |
| v0.13.0 evidence 刷新 | **抽查成立** | `docs/releases/runtime/v0.13.0/*.json` 12×pass；3 条 behaviorSources 哈希全 match |
| A-001 self 格式 | 文件合格；**索引漏登** | `03-audit/A-001-*.md` vs 当时 `03-audit.md` 空表 |

## Findings

### required findings

**无。**

### recommended（非阻断 · 建议 `/govern` 响应）

| ID | 严重度 | 说明 | 可核对修正建议 |
|----|--------|------|----------------|
| **R-001** | med | **审计台账索引滞后**：`03-audit/A-001-*.md` 已落盘且 verdict=pass，但独立审开始时 `03-audit.md` 意见表仍写「尚未到达审计节点」，信息表 I-001/I-002 仍写 open——与 `00-meta`/`01-decision` 的 closed 及 A-001 文件矛盾。违反 P-003「索引 + A 条目共同构成正式台账」的完整登记习惯，增加「只读索引会漏掉 self 意见」风险。 | `/govern` 同步索引：登记 A-001（及本 A-002）；信息表对齐 closed；结论段更新。本 independent 落盘时会登记 A-002，但 **A-001 行仍须编排器或本轮索引修补写全**。 |
| **R-002** | low | **测试条数误报**：E-002 / A-001 写「`test_mcp_config` 10 条 + canonical 8 条」。独立复跑为 **9 + 6 = 15** 全绿。断言内容有效，计数不准确。 | 修正 E-002/A-001 数字或接受 residual；后续勿用错误条数作进度话术。 |
| **R-003** | low | **「布局冻结」测试标题强于断言**：`test_internal_layout_is_frozen_under_configured_root` 仅在配置根下 mkdir 约定形状并 `assertTrue` 存在，**不**证明系统拒绝改内部文件夹名，也未对「不可配置内部布局」做负例。协议层（D-001「只改根前缀」）与代码面（无改布局 API）仍成立。 | 改测试名/注释为「配置根下可承载冻结形状」；或增加「配置不暴露 layout 键 / schema additionalProperties:false」等显式断言。 |
| **R-004** | low | **doctor `governanceRootError` 无专用自动测试**：行为经手工验证正确；回归网仅覆盖 `config.py` 解析。 | 在 `skills/tests` 增加 doctor 非法 JSON / 越界 pin 的结构化字段断言。 |
| **R-005** | low | **`skills/mcp/README.md` 陈旧**：目录表仍写 `config.py` 为「R2/R3 **计划**落点（本 R1 版本尚未交付）」——与 R3 已交付事实冲突。 | 更新 README 为已交付（R3）并指向 `config.py` / schema / doctor 字段。 |
| **R-006** | low | **A-001 R-002 部分过时**：`consumer-checklist.md` 已是 `{governance_root}/…` 勾选，并非「仍写 docs/」。`standalone-bootstrap.md` 顶部有治理根说明与对照表，下方拷贝命令仍以 monorepo 源树 `docs/` 为默认示例——在「生产仓固定 docs + 源路径」语境可接受，但宜明确「源路径 vs 目标 `{governance_root}`」。 | 响应 A-001 R-002 时修正对该 checklist 的判断；bootstrap 可选加一句「命令示例默认源=本 monorepo docs」。 |
| **R-007** | low | **AGENTS 文档 version `0.13.0` 与发布标签 v0.13.0 同名**（与 A-001 R-001 同向）：易被误读为「AGENTS 版号 ≡ 发行版」。本仓 AGENTS 可独立演进。 | CHANGELOG/发布说明注明两套编号；或 AGENTS 用不同主次版本策略。 |

## 必改项汇总

- **required：无。**  
- recommended：R-001～R-007（见上）。**R-001** 建议在 C5 闭合前处理台账索引，避免正式索引与磁盘 A 文件不一致。

## 与 A-001（self）的异同

| 点 | self A-001 | independent A-002 |
|----|------------|-------------------|
| verdict | pass | **pass**（独立复跑后确认） |
| required | 无 | **无** |
| 测试/镜像 | 声称 10+8、stage ok | **亲自 194 全量 + 15 R3 专项；stage ok；镜像字节一致**；纠正条数为 9+6 |
| fail closed | 声称 | **代码读 + 临时仓手工复现** |
| doctor | 声称 governanceRootError | **手工确认字段与 ok=False** |
| evidence | 声称 12 条刷新 | **12×pass；3 条 behaviorSources 哈希全 match** |
| 台账索引 | 未自检索引空表 | **R-001** |
| consumer-checklist | R-002 称未改仍写 docs/ | **R-006：checklist 已相对化；bootstrap 为源路径示例** |
| 布局冻结测试深度 | 未质疑 | **R-003** |
| README 陈旧 | 未提 | **R-005** |

## 结论 + 建议给编排器/用户的下一步

1. 用 **`/govern`** 响应 A-002：确认无 required；处理 R-001（索引补 A-001 + 本 A-002 + 信息表 closed）优先；R-002～R-007 可选修正 / 接受残余并留痕。  
2. 响应后更新 GOAL-004 **C5** 检查点与（若适用）goal-tree；**勿**把本 `pass` 直接写成目标 `done`。  
3. Root 纲领 R3 阶段门禁：子目标 C5 合法闭合后再审 Root 是否可标 R3 完成。

## 声明

本意见 `source: independent`，**不**修改目标 `status` / 检查点 / 派生 `progress` / 方案正文 / goal-tree 状态列。响应、finding 闭合与推进由 **`/govern`** 处理。
