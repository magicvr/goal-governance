---
id: GOAL-022-docs-ssot-skills-mirror-stage
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.3.0
---

# 审计 · GOAL-022

## 信息就绪核对（按 scope）

| 核对项 | 状态 | 备注 |
|--------|------|------|
| 影响本 scope 的 I-00N | I-001～I-003 **closed**（D-002）；I-004 **closed (out of scope)** | 与 00-meta / 01-decision 一致 |
| 到期 required 是否已 verified / residual | 无到期未关闭 required 信息项 | 阶段 F 已由 A-003 + D-003 闭合 |
| 资料引用（若有）是否固定且用户确认 | 无 | 本目标不依赖 shared-materials 固定引用 |
| 工作区绑定 | OK | `workspace-001-goal-governance` · Root `GOAL-001-main-vision` · `plan_refs`/`primary_plan` = VP-001 |

## 意见台账索引

| A-ID | 日期 | source | scope | verdict | 开放 required |
|------|------|--------|-------|---------|---------------|
| A-001 | 2026-07-30 | independent | 阶段 A～E 执行事实 + 关门前（F）就绪核对 | conditional | 0（F-001～F-003 recommended；响应后已闭合） |
| A-002 | 2026-07-30 | self | 响应 A-001 F-001～F-003 | pass（关闭证据） | 0 |
| A-003 | 2026-07-30 | self | close-out 目标整体 A～F | pass | 0 |

---

## A-001 · 方法论 SSOT / Skills 镜像 stage 独立交叉审计（2026-07-30）

- **source**：`independent`
- **auditor**：Grok Build · `/audit` 独立交叉审计（本会话）
- **类型**：`execution-facts`（主）+ 关门前 `close-out` 就绪核对（**不**授予阶段 F / `done`）
- **scope**：`GOAL-022-docs-ssot-skills-mirror-stage` 目标定义、D-001/D-002、纲领 A～E 交付主张、stage/pack/CI/install 与相关测试；工作区 `workspace-001-goal-governance`。**不含** tag/Release、Root/Charter/VP 变更、I-004 AGENTS 生成链、其他工作区。
- **verdict**：`conditional`
- **完整意见**：本文件本节（无单独附件）

### 范围与区间

| 项 | 内容 |
|----|------|
| 工作区 | `docs/workspace-001-goal-governance/` · `workspace_id: workspace-001-goal-governance` · Root `GOAL-001-main-vision` |
| 已读 | `00-meta` / `01-decision` / `02-execution` / 本 `03-audit`（写前）；`workspace.md`；`scripts/stage_skills_mirrors.py` + 单测；`pack_skills_release.py` stage 挂接；`.github/workflows/ci.yml`、`skills-pack-release.yml`；`skills/templates`、`skills/core/docs`、contracts `mirrorPath`、install.{sh,ps1} 模板源；`docs/README` 镜像说明 |
| 复跑核验（2026-07-30 本机） | `stage_skills_mirrors.py --check` → ok（28 pairs）；docs **26** OK；skills orchestrator **39** OK；scripts **52** OK（2 skip）；planned_pairs 全量 sha256 一致；orphan mirrors **0**；`tech-stack.md` 不在 core；`skills/templates` 仅 `README.md` |
| 不覆盖 | 正式 GitHub Release 身份；在未装依赖的干净 clone 上重放完整 web 套件；伪造 CI 远端结果 |

### 成果（有证据）

| 主张 | 证据 |
|------|------|
| 方案冻结 + I-001～I-003 关闭 | `01-decision.md` D-002；`00-meta` 信息表 closed |
| stage 脚本 + 白名单 / 保护面 | `scripts/stage_skills_mirrors.py`：`ARCHITECTURE_FILES`、templates/**、alignment、contracts/**；不覆盖 core README / vision README；删除 core `tech-stack.md`；剥离 legacy `skills/templates` 五件套 |
| stage 单测含漂移门禁 | `scripts/tests/test_stage_skills_mirrors.py`（3 测，含 monorepo `--check`） |
| pack 前 monorepo 自动 stage | `pack_skills_release.py` `_maybe_stage_mirrors`；CLI `--skip-stage`；缺 core / 带 tech-stack 仍 fail closed（既有 pack 校验） |
| CI 强制 stage + 脏树失败 | `.github/workflows/ci.yml` Ubuntu/Windows：stage → `--check` → `git diff` on `skills/core|contracts|templates` |
| pack workflow 打包前 stage | `skills-pack-release.yml` Stage skills mirrors step + pack 再 stage |
| templates 第三副本收敛 | 工作树仅 `skills/templates/README.md`；契约 `templateSet.mirrorPath` = `skills/core/docs/templates/goal-folder`；orchestrator 断言无 `skills/templates/goal-folder` |
| 字节一致自动化 | stage `--check`；`test_docs_readme_hash_ledger_matches_template_bytes` 对模板/契约；本机 28 pairs hash 全绿 |
| install 读 core 模板源 | `install.sh` `TEMPLATES_SRC=…/core/docs/templates`；`install.ps1` 同等 |
| 消费方 README 手维（非 monorepo 长文镜像） | `skills/core/docs/README.md` 与 `docs/README.md` 哈希不同（约 3.6KB vs 12KB）；stage 不覆盖 |
| 文档台账 | `docs/README` 0.10.6 含 GOAL-022 stage 节；`directory-layout` / `skills/README` / `templates/README` 已指向 stage |
| 进度展示自洽 | 路线图 A～E `[x]`、F `[ ]` → 5/6 = 83%；**progress 未当作放行证据** |
| 阶段 F 未宣称完成 | 成功标准最后一项与路线图 F 仍未勾选；02-execution 明确未做关门自审 |

### 对照成功标准

| # | 标准 | 结论 |
|---|------|------|
| 1 | 冻结白名单 / 排除 / 变换面 | **满足**（D-002 + 脚本常量） |
| 2 | 可重复 stage 脚本 | **满足** |
| 3 | pack/CI 强制 stage；缺 core / tech-stack fail closed | **满足**（pack 校验 + monorepo stage；CI 漂移门禁） |
| 4 | 无 docs+core+skills/templates 三边手维；templates 指针 | **满足（monorepo 源树）**；见 F-002 关于 install 再物化 |
| 5 | 字节一致类镜像自动化；README/vision 手维例外 | **满足** |
| 6 | 相关测试绿；README/docs 说明更新 | **满足**（本机复跑计数与执行记录一致：26 / 52(2skip) / 39） |
| 7 | 阶段自审或关门审 + 用户确认 | **未完成**（阶段 F 合法开放；本意见**不**替代 F） |

### Findings

#### F-001 · stage 不清理「canonical 已删、镜像仍在」的孤儿文件

| 字段 | 值 |
|------|-----|
| **级别** | `recommended` |
| **严重度** | `med` |
| **影响门禁** | 长期 SSOT 完整性；阶段 F 可 residual 接受 |
| **状态** | **closed** · `accepted-residual` · **R-022-ORPHAN-PRUNE**（D-003 / A-002） |
| **描述** | `stage_skills_mirrors` 只对白名单 pairs 做 copy/`--check`，并特例删除 `tech-stack.md` 与 legacy `skills/templates/*`。若日后从 `docs/templates/**` 或 `docs/contracts/**` **删除**某文件，镜像侧旧文件可残留，且 `--check` 不会失败（只校验仍在 planned_pairs 的路径）。当前工作树 orphan 计数为 **0**，属机制缺口而非现存漂移。 |
| **证据** | `scripts/stage_skills_mirrors.py` `stage_skills_mirrors()` 循环仅处理 `planned_pairs`；无「dest 树 − pairs」删除逻辑；本机扫描 orphans=0 |
| **建议** | 为 stage 增加可选/默认 orphan prune（限 `skills/core/docs/{architecture,templates,vision}` 与 `skills/contracts` 白名单树）+ 单测；或关门时书面 residual：删除 canonical 后须人工删镜像并跑 CI |

#### F-002 · install `-All` / `--all` 仍向 `skills/templates/` 物化完整模板树

| 字段 | 值 |
|------|-----|
| **级别** | `recommended` |
| **严重度** | `med` |
| **影响门禁** | 消费路径「单一分发源」叙事；monorepo 误跑 install 可破坏指针收敛 |
| **状态** | **closed** · `accepted-residual` · **R-022-INSTALL-TEMPLATES-COPY**（D-003 / A-002） |
| **描述** | 源已改为 `core/docs/templates`，但 extras 安装仍 `Copy-DirMerge` 到 `$SkillsDir/templates`（sh/ps1 对称）。隔离安装测试仍要求 `SkillsDest/templates/workspace-context.md` 存在。结果：包内权威源是 core，但 `-All` 会在 skills 树再造一份可手改副本；在 monorepo 对 `./skills` 执行 `-All` 会冲掉指针 README 策略。 |
| **证据** | `skills/install.ps1` L630–636；`skills/install.sh` `TEMPLATES_SRC` + extras 复制；`skills/tests/test_install_ps1_isolated.ps1` L56 仍断言 skills 下 templates 文件 |
| **建议** | （a）extras 不再复制 templates，仅依赖 core→docs 与包内 `core/docs/templates`；或（b）明确文档：skills/templates 仅为 install 派生、禁止手维，并避免在 monorepo 对 skills 跑 `-All`；同步改隔离测试期望 |

#### F-003 · 父目标 / 历史叙述仍指向旧 `skills/templates/goal-folder` 镜像

| 字段 | 值 |
|------|-----|
| **级别** | `recommended` |
| **严重度** | `low` |
| **影响门禁** | 非 GOAL-022 成功标准强制项；可读性 / 后续维护混淆 |
| **状态** | **closed** · `fixed`（D-003 / A-002） |
| **描述** | Root 等过程文件仍写「`skills/templates/goal-folder` 为分发镜像 / 须手同步」。GOAL-022 已改契约与 skills README，但未清扫 GOAL-001 现行 meta/decision 中的过时路径说明。 |
| **证据** | 如 `GOAL-001-main-vision/00-meta.md`（模板镜像句）、`01-decision.md` 镜像同步表；对比 `skills/templates/README.md`、contracts `mirrorPath` |
| **建议** | 关门 residual 记 follow-up；或由 `/govern` 小补丁更新 Root 现行说明（历史审计节可保留原貌） |

### 必改项汇总

- **开放 required（blocking）**：**无**。
- **建议在阶段 F 前处理或 residual 的 recommended**：F-001（orphan prune 或 residual）、F-002（install 再物化策略）、F-003（历史叙述 residual / 小补丁）。→ **已由 D-003 / A-002 处理**。

### 与既有意见的异同

- 本目标此前 **无** A-00N 正式意见（写前台账为空）。
- 与 GOAL-021 A-001（执行链对抗、发版证据）**无冲突**：本意见不否定 021 已关 findings；聚焦 022 的 SSOT stage 交付。
- 写前 `03-audit` 信息就绪节仍写 I-001～I-003 open —— 与 meta 矛盾；**本意见已刷新台账头部**，不另立 required finding。

### 结论 + 建议给编排器/用户的下一步

**结论**：阶段 **A～E 的交付主张总体可核对**，测试与镜像一致性在本机复跑下成立；**不得**据此将目标标为 `done` 或勾选阶段 F。verdict = **conditional**，因存在 SSOT 长期完整性与 install 路径再物化等 **recommended** 缺口，宜在关门前固定 / residual / 修代码三选一并留痕。

**建议 `/govern`**：

1. 汇总 A-001；对 F-001～F-003 逐条：`fixed` / `accepted-residual` / 排入 follow-up（用户书面）。  
2. 用户确认是否进入阶段 **F**（自审 A-00N 或独立审响应后关门）。  
3. **不要**用 progress 83% 放行；开放 required findings 仍为 0 时，F 的门禁主要是检查点 7 + recommended 处理策略。

### 声明

本意见 **不**修改目标 `status` / 检查点 / 派生 `progress` / goal-tree 状态列；响应、闭合 finding、推进或关门由 **`/govern`** 处理。

---

## A-002 · 响应 A-001 F-001～F-003（2026-07-30）

- **source**：`self`
- **auditor**：`/govern` 编排器（Grok Build）
- **类型**：`response`
- **scope**：A-001 / F-001～F-003 关闭证据
- **verdict**：`pass`（相对「是否已按 D-003 闭合」；**不是**独立复审）

### 关闭证据表

| Finding | 闭合路径 | 证据 |
|---------|----------|------|
| F-001 | `accepted-residual` · **R-022-ORPHAN-PRUNE** | D-003 residual 表：范围、缓解（删 canonical 后人工删镜像 + stage/CI）、复审触发；用户书面确认 |
| F-002 | `accepted-residual` · **R-022-INSTALL-TEMPLATES-COPY** | D-003 residual 表：权威=core；`-All` 派生禁手维；禁 monorepo 对 `./skills` 当同步；用户书面确认 |
| F-003 | `fixed` | `GOAL-001-main-vision/00-meta.md` 三层交付现行句；`01-decision.md` D-007/D-008 现时注；历史 A 节未改写 |

### 仍开放项（A-002 出具时）

- 阶段 F 自审 / 用户确认 `done` → 见 **A-003** / D-003  
- residual R-022-ORPHAN-PRUNE / R-022-INSTALL-TEMPLATES-COPY（**non-blocking**，不阻断关门）  
- I-004 AGENTS 生成链（仍 out of scope）

### 声明

本条为编排响应记录，**不是** `source: independent` 复审。

---

## A-003 · self close-out · 阶段 F（2026-07-30）

- **source**：`self`
- **auditor**：`/govern` 编排器（Grok Build）
- **类型**：`close-out`
- **scope**：GOAL-022 目标整体（阶段 A～F：方案冻结、stage/pack/CI、templates 收敛、文档、A-001 响应、回归与成功标准）
- **verdict**：`pass`
- **长文**：无

### 范围与区间

- **覆盖**：D-001/D-002/D-003；纲领 A～F；A-001 findings 闭合；关门前 stage `--check` 与相关测试；成功标准勾选。
- **不覆盖**：Root 终态、VP 关门、annotated tag / GitHub Release、I-004 AGENTS 生成链、实现 orphan prune / 取消 install templates 物化。
- **与既有意见**：与 A-001 **无冲突**——A-001 `conditional` 要求 F 前处理 recommended；已按 D-003 residual×2 + fixed×1 留痕。progress 未作放行证据。

### 信息就绪核对

| 核对项 | 状态 |
|--------|------|
| I-001～I-003 | closed |
| I-004 | closed (out of scope) |
| 到期 required I | 0 |
| 资料引用 | 无 |

### 对照成功标准

| 成功标准 | 状态 | 证据 |
|----------|------|------|
| 冻结白名单 / 排除 / 变换面 | 达成 | D-002 + `stage_skills_mirrors.py` 常量 |
| 可重复 stage 脚本 | 达成 | `scripts/stage_skills_mirrors.py` + 单测 |
| pack/CI 强制 stage；fail closed | 达成 | pack 挂接 + CI/workflow；既有 pack 校验 |
| 无三边手维；templates 指针 | 达成 | monorepo 仅 README 指针；`mirrorPath`→core；R-022-INSTALL 接受 install 派生 |
| 字节一致自动化；README 手维例外 | 达成 | stage `--check`；core README 手维 |
| 相关测试绿；文档更新 | 达成 | 关门前：docs **26** OK；scripts **52** OK（2 skip）；skills orchestrator **39** OK；`stage --check` 28 pairs ok |
| 自审 + 用户确认关门 | 达成 | 本 A-003 + D-003 用户选择题确认 |

### Findings

本 close-out **无新增 required**。  

Recommended residual（不阻断关门；已在 D-003 接受）：

#### R-022-ORPHAN-PRUNE · stage 无 orphan prune（来自 F-001）

| 字段 | 值 |
|------|-----|
| **级别** | recommended · residual accepted |
| **状态** | open · non-blocking |
| **关闭要求** | 实现白名单树 orphan prune + 单测；或持续按操作约定人工清理 |

#### R-022-INSTALL-TEMPLATES-COPY · install `-All` 物化 templates（来自 F-002）

| 字段 | 值 |
|------|-----|
| **级别** | recommended · residual accepted |
| **状态** | open · non-blocking |
| **关闭要求** | extras 停止复制 templates 并改隔离测试；或产品明确长期接受派生副本策略 |

### 必改项汇总（required）

- 无开放 required。

### 结论与下一步

- **一句话结论**：GOAL-022 成功标准已满足；open required = 0；可 `done / 100%`。
- **不构成**：可自动 tag/Release；Root `done`；R-022 residual 已修。
- **建议**：goal-tree 同步 done；路径 D 其他工作另开 GOAL-023+；可选 follow-up 闭合 residual。
- **声明**：self close-out；独立复审可选，非本拍强制。
