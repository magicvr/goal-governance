---
id: GOAL-019-skills-consumer-workspace-bootstrap
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-24
updated: 2026-07-24
version: 1.0.0
---

# 审计 · GOAL-019

## 信息就绪核对（按 scope）

| ID | 级别 | 状态 | 本阶段影响 |
|----|------|------|------------|
| I-001 | non-blocking | **accepted-residual** | R-019-I001-INSTALL-SHAPE |
| I-002 | non-blocking | **closed**（D-006） | init-workspace 已交付 |
| I-003 | required | **closed**（D-005） | 已写入 S0/01/install |
| I-004 | required | **closed**（D-004） | 阶段 A 已验收 |
| I-005 | non-blocking | **accepted-residual** | R-019-STANDALONE-COPY |



## 阶段 A 结构核对（非正式 · 2026-07-24）

| 检查 | 结果 |
|------|------|
| core 四 architecture + templates + 精简 README | 有 |
| 无 tech-stack | 有 |
| install 默认 core | 有（sh/ps1） |
| pack required | 有 |
| install.ps1 无 docs\\goals Next steps | 有 |
| 隔离 install 冒烟 | 有（unittest OK） |

## 阶段 B 结构核对（非正式 · 2026-07-24）

| 检查 | 结果 |
|------|------|
| S0 先 scaffold 再 Root | 有（00 v0.7） |
| slug 用户确认 / 禁静默默认 | 有（D-005） |
| architecture 必备 / 不完整安装 | 有（AGENTS + 00 + wrappers） |
| 01 步骤 0 | 有 |
| 单测 portability required architecture | 有 |

## 阶段 C 结构核对（非正式 · 2026-07-24）

| 检查 | 结果 |
|------|------|
| install --init-workspace / -InitWorkspace | 有 |
| 强制 workspace-slug + root-slug | 有 |
| 不创建 GOAL 五件套 | 有（隔离冒烟） |
| 已存在路径 refuse | 有（代码路径；自动化覆盖见 A-001 F-002） |
| 隔离 PASS + unit tests | 有（本轮复跑见 A-001） |

## 决策一致性（自检 · 非正式）

| 项 | 结论 |
|----|------|
| D-002 → D-003 | D-002 superseded；D-003 accepted 且有用户书面确认 |
| 范围是否膨胀失控 | 有界：core 镜像 + 默认安装 + 工作区 scaffold；排除 dogfood / Web / Marketplace |
| 与 GOAL-006/018 | 006 standalone 降为次路径；018 边界扩展为 adapter+core 镜像，不重开 018 |

## 审计意见台账

| A-ID | source | 日期 | scope | verdict | 说明 |
|------|--------|------|-------|---------|------|
| A-001 | independent | 2026-07-24 | 全目标 A–C + 关门就绪 | conditional | findings F-001～F-004 |
| A-002 | self | 2026-07-24 | 关门审计（响应后） | **pass** | F-001/F-002 closed；residual 已接受 |
| A-003 | self | 2026-07-24 | 编排响应 A-001 | — | 响应节（非 independent） |

---

## A-001 · 独立交叉审计 · 阶段 A–C 交付 + 关门就绪（2026-07-24）

- **source**：independent  
- **auditor**：GitHub Copilot / Grok 4.5（`/audit` · skills/prompts/05-independent-audit.md）  
- **类型**：execution-facts + design-plan + close-out readiness  
- **scope**：GOAL-019 全目标；对照成功标准、D-003～D-006、I-001～I-005、阶段 A/B/C 实现与阶段 D 关门就绪  
- **verdict**：**conditional**  
- **工作区**：`workspace-001-goal-governance` · root `GOAL-001-main-vision` · canonical `docs/workspace-001-goal-governance/`（已校验；未读其他工作区）  
- **共享资料引用**：本目标未依赖固定 material 引用；`workspace.md` 引用表为空（合格）

### 范围与区间

- 只读扫描：`workspace.md`、`goal-tree` 中 GOAL-019 条目、五件套、`skills/core/**`、`skills/install.{sh,ps1}`、`skills/README.md`、`skills/prompts/00`/`01`、`skills/AGENTS.template.md`、`skills/install/**` 规则面、`scripts/pack_skills_release.py`、相关单测与隔离冒烟。  
- 本轮复跑证据：`python -m unittest skills.tests.test_skills_orchestrator scripts.tests.test_pack_skills_release` → **39 tests OK**；`skills/tests/test_install_ps1_isolated.ps1` → **PASS**（core + workspace-001-pilot-app skeleton；无 GOAL 五件套；无 tech-stack）。  
- **不**修改 `status` / `progress` / goal-tree 状态列。

### 成果（有证据）

| 成果 | 证据 |
|------|------|
| D-003 产品定位：core 与 Skills 同级必备；D-002 superseded | [01-decision.md](01-decision.md) D-002/D-003 |
| D-004 core 清单落盘：architecture×4 + templates + 精简 README；无 tech-stack | `skills/core/docs/**`；`test_core_d004_mirror_is_complete` |
| install 默认装 core → `./docs/` | `install_core_docs` / `Install-CoreDocs`；隔离冒烟断言 docs 落点 |
| pack required core + 拒 tech-stack | [scripts/pack_skills_release.py](../../../scripts/pack_skills_release.py) inventoriable_files；pack 单测 |
| install Next steps 对齐 workspace 路径（非 legacy `docs\goals\`） | `install.ps1`/`install.sh` print_next_steps；`assertNotIn docs\goals\goal-tree` |
| README 最小可运行集 + core 同级必备 | [skills/README.md](../../../skills/README.md) |
| S0 / 01 scaffold + slug 用户确认（D-005 / I-003） | `00-govern-orchestrator` S0；`01-create-new-goal` 步骤 0；`test_portability_skills_pkg_and_required_architecture` |
| 消费方 AGENTS / wrappers：不完整安装 / 同级必备 | `AGENTS.template`、`install/claude|copilot|grok`；host govern skills |
| D-006 可选 InitWorkspace + 强制双 slug；不建五件套；已存在 refuse | install 实现 + 隔离冒烟（无 GOAL 目录）；refuse 见代码路径 |
| overview/layout 去 monorepo 专有路径；principles/protocol 去掉 dogfood 内链（允许的镜像适配） | core vs canonical diff（内链/示例路径，非规则掏空） |
| required 信息项 I-003/I-004 已关闭；I-002 closed；I-005 deferred 有复核说明 | 00-meta / 01-decision 信息表 |

### 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| Core 镜像（D-004） | **达成** | core 文件齐全；无 tech-stack |
| install 默认 core | **达成** | sh/ps1 + 隔离冒烟 |
| pack required + 拒 tech-stack + 单测 | **达成** | pack 脚本 + 39 tests OK |
| install.ps1 Next steps 对齐 workspace | **达成** | 冒烟输出 + 源码 |
| skills README 最小可运行 + core 必备 | **达成** | README + 单测 |
| S0/`01` 空仓 scaffold；slug 确认 | **达成** | prompts + portability 单测 |
| AGENTS / govern wrapper 必备话术 | **部分** | 消费安装面 OK；**monorepo 根 AGENTS §11 残留「可选补充」**（F-001） |
| 可选 `--init-workspace` | **达成** | D-006 + 冒烟 |
| 临时空目录隔离冒烟 | **达成**（Windows/ps1） | 本轮 PASS；sh 运行时未在本环境复跑（F-003） |
| 阶段/关门审计无未关闭 required finding | **未完成（阶段 D）** | 本意见提出 findings；待 `/govern` 响应 |

### Findings

#### F-001 · monorepo 根 AGENTS §11 残留「architecture 原则全文可选补充」

- **严重度**：med  
- **建议**：required  
- **关联**：成功标准「AGENTS … 去掉整体可选定位」；D-003  
- **描述**：消费方安装面（`skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、copilot-instructions 等）已写「同级必备 / 不完整安装」。但仓库根 [AGENTS.md](../../../AGENTS.md) §11 正确做法仍写「architecture 原则全文**可选补充**」，与同文件 §6/§6b 及 D-003 产品定位冲突。根 AGENTS 是 monorepo dogfood 规则面，不进 skills zip，但属于成功标准「AGENTS」字面范围与本仓日常执行入口。  
- **证据**：`AGENTS.md` 正确做法列表中「architecture 原则全文可选补充」；对比 `skills/install/claude/AGENTS.md` §11「architecture 原则全文**必备**」。  
- **状态**：**closed**（2026-07-24）— 根 `AGENTS.md` v0.8.1 已改；`test_monorepo_agents_architecture_not_optional_supplement` OK；见 A-003  

#### F-002 · 「已存在工作区 refuse overwrite」仅有代码路径，无自动化用例

- **严重度**：low  
- **建议**：recommended  
- **关联**：D-006 第 5 点；阶段 C 非正式核对「有（代码路径）」  
- **描述**：`init_workspace_skeleton` / `Initialize-WorkspaceSkeleton` 在路径已存在时 `die`/`Write-Err`，但 `test_install_ps1_isolated.ps1` 与 orchestrator 单测均未断言 refuse 行为。回归风险低但可测。  
- **证据**：install.sh / install.ps1 refuse 分支；`skills/tests/**` 无匹配。  
- **状态**：**closed**（2026-07-24）— `test_init_workspace_refuses_existing_path` + 源码 refuse 断言；见 A-003  

#### F-003 · install.sh 隔离运行时冒烟未在本轮复现

- **严重度**：low  
- **建议**：recommended  
- **关联**：成功标准「临时空目录隔离冒烟」；跨平台  
- **描述**：可复现隔离脚本与本轮复跑均针对 `install.ps1`。`install.sh` 靠静态单测（flag/函数名/core 路径）覆盖，Windows 本环境未执行 bash 端到端。阶段 C 宣称「隔离」对 sh 证据弱于 ps1。  
- **证据**：`skills/tests/test_install_ps1_isolated.ps1`；`test_core_d004_mirror_is_complete` 字符串断言 sh。  
- **状态**：**accepted-residual** → **R-019-SH-RUNTIME**（D-007；不阻塞关门）  

#### F-004 · 此前仅有非正式结构核对，无 self A-00N

- **严重度**：low  
- **建议**：recommended（流程 / P-004）  
- **描述**：A/B/C 仅有「非正式」核对表；正式台账本条 A-001 为首次。P-004：已有 independent、尚无 self 时，编排器须**询问**是否还要自审，不得静默跳过或未问即强制。  
- **证据**：本文件历史「非正式」段；无 `source: self` 条目。  
- **状态**：**closed**（2026-07-24）— 用户书面要求补 self；已写 **A-002**  

### 信息项与门禁

| ID | 判定 |
|----|------|
| I-001 open non-blocking | 不阻断关门；可 residual |
| I-002 closed | 与 D-006/实现一致 |
| I-003/I-004 closed required | 关闭证据充分（决策 + 实现 + 测试） |
| I-005 deferred non-blocking | 有延期说明；关门可不强制关闭；建议 residual 接受留痕 |

### 必改项汇总

1. **F-001（required）**：修正 monorepo 根 `AGENTS.md` §11 残留「architecture … 可选补充」，与 D-003 / §6 一致；或书面界定「GOAL-019 成功标准仅覆盖消费安装 AGENTS」并 residual 接受该 dogfood 残留（不推荐）。

### 与既有意见的异同

- 此前无 formal self/independent A-00N；仅有执行侧非正式核对。  
- 本意见**确认**非正式表中 A/B/C 主体结论，并**收紧**两点：根 AGENTS 残留（F-001）、refuse/sh 证据强度（F-002/F-003）。

### 结论 + 建议给编排器/用户的下一步

- **verdict = conditional**：消费方交付（core 镜像、默认 install、S0/01、InitWorkspace、pack、README、宿主 wrappers）证据充分，**不宜**在 F-001 未响应时无条件宣称成功标准「AGENTS 去掉整体可选」与阶段 D 关门全部通过。  
- **建议 `/govern`**：  
  1. P-004 询问是否补 **self** 关门审计；  
  2. 关闭 **F-001**（改根 AGENTS 或 residual 书面接受）；  
  3. F-002/F-003 可修可 residual；  
  4. 确认 I-005 deferred residual；  
  5. 通过后更新 progress/status 与 goal-tree，执行有界关门。

### 声明

本意见 **source: independent**，**不**修改目标 `status` / `progress` / 方案正文 / goal-tree 状态。响应、改状态与关门由 **`/govern`** 处理。

---

## A-002 · self · 关门审计（响应 A-001 后 · 2026-07-24）

- **source**：self  
- **auditor**：Grok Build /govern（用户书面要求补自审）  
- **类型**：close-out  
- **scope**：GOAL-019 全目标；对照成功标准与 A-001 findings 关闭证据  
- **verdict**：**pass**

### 成果

- 成功标准 A–C 与 A-001 成果表一致（core / install / pack / S0 / InitWorkspace / README / wrappers）。  
- **F-001 closed**：根 AGENTS v0.8.1；`test_monorepo_agents_architecture_not_optional_supplement` OK。  
- **F-002 closed**：`test_init_workspace_refuses_existing_path` OK。  
- **F-003 residual** R-019-SH-RUNTIME（D-007 书面接受）。  
- **F-004 closed**：本条 self。  
- **I-005 / I-001** accepted-residual。  
- **无未关闭 required finding**。编排器单测套件 35 passed（含新增用例）。

### 偏差 / residual

见 [00-meta residual 表](00-meta.md)。

### 结论

有界关门条件满足：`done / 100%`。

---

## A-003 · self · 响应 A-001 / 关闭 findings（2026-07-24）

- **source**：self（编排响应，**非** independent）  
- **关联**：A-001 independent conditional  
- **决策**：[D-007](01-decision.md)

| Finding | 动作 | 证据 | 结果 |
|---------|------|------|------|
| F-001 required | 改根 AGENTS | AGENTS.md v0.8.1；test_monorepo_agents_architecture_not_optional_supplement | **closed** |
| F-002 recommended | 补测 | test_init_workspace_refuses_existing_path；install refuse 文案断言 | **closed** |
| F-003 recommended | residual | R-019-SH-RUNTIME | **accepted-residual** |
| F-004 recommended | 补 self | A-002 | **closed** |
| I-005 deferred | residual | R-019-STANDALONE-COPY | **accepted-residual** |
| I-001 open | residual | R-019-I001-INSTALL-SHAPE | **accepted-residual** |

**放行**：无 open required finding → 有界关门已执行（status done / progress 100% / goal-tree 同步）。
