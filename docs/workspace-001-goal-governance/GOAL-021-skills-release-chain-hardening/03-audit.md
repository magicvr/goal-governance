---
id: GOAL-021-skills-release-chain-hardening
doc: audit
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.3.0
---

# 审计 · GOAL-021

## 信息就绪核对（按 scope）

| 核对项 | 状态 | 备注 |
|--------|------|------|
| 影响本 scope 的 I-00N | I-001～I-003 closed | 见 00-meta / D-002 / D-003 |
| 到期 required 信息项 | 无 | — |
| 资料引用 | 无 | 本目标不依赖 shared-materials 固定引用 |

## 意见台账索引

| A-ID | 日期 | source | scope | verdict | 开放 required |
|------|------|--------|-------|---------|---------------|
| A-001 | 2026-07-30 | independent | 规则→分发→证据→发布 执行链 | fail（相对「可安全发版」主张） | 0（响应后） |
| A-002 | 2026-07-30 | self | 响应 A-001 F-001～F-005 | pass（关闭证据） | 0 |
| A-003 | 2026-07-30 | self | close-out 目标整体 A～G | pass | 0 |

---

## A-001 · Skills 执行链对抗性独立审计（2026-07-30）

- **source**：`independent`
- **auditor**：会话对抗审（用户粘贴结论；立项后由编排器正式落盘；**不**由本编排器冒充独立审重新出具）
- **类型**：`ad-hoc`（release-chain quality · path D）
- **scope**：Skills / core 分发、运行证据采集与兼容性消费、打包与发布工作流、P-006 相关通用验证器、安装器与工作区结构校验。**不含** Web R-009-X、方法论叙事层（GOAL-020 已关）、Root 终态。
- **verdict**：`fail`（相对「可发布新 Skills 包 / 当前 runtime 证据可作充分发布证明」）；核心原则总体自洽，**执行链**不足。
- **长文**：无单独附件；正文即完整意见（用户提供的审计结论结构化落盘）。

### 范围与区间

- **覆盖**：core 模板 mirror、`capture_runtime_evidence` / `compatibility_report`、`pack_skills_release` 与 Ubuntu pack workflow、vision/workspace 协议测试与安装脚本。
- **不覆盖**：证明既有 evidence 文件已被伪造；仅证明**机制**不足以证明真实运行行为。
- **与既有意见**：与 GOAL-008/018/019 历史关门 **无冲突**——不追溯否定其当时证据；本意见针对 **当前** 链路上的 P1 风险与负例缺口。

### 总评摘要

核心原则总体自洽，但「规则 → 分发 → 证据 → 发布」存在 **4 项 P1** 风险；修复前 **不建议** 发布新的 Skills 包，或把当前运行证据当作充分的发布证明。现有文档测试 22、Skills 测试 39、脚本测试 46 均绿，**不足以**覆盖本意见负例。Git 受跟踪工作树保持干净；兼容性检查曾刷新忽略目录中的 `artifacts/compatibility-report.json`（过程备注，非本目标交付物）。

### 成果（有证据 · 正面项）

| 主张 | 证据路径 / 说明 |
|------|-----------------|
| `docs/architecture` 与 `skills/core/docs/architecture` 一致（有意排除 `tech-stack.md`） | 审计会话核对 |
| `docs/contracts` 与 `skills/contracts` 一致 | 审计会话核对 |
| 既有 docs / skills / scripts 绿测通过 | 22 + 39 + 46 passed（会话时点） |

### Findings

#### F-001 · core 模板说明语义漂移（P1）

| 字段 | 值 |
|------|-----|
| **级别** | `required` |
| **严重度** | `high` |
| **影响门禁** | 阶段 B；对外分发「模板说明与 canonical 一致」；发版前 |
| **状态** | `fixed` |
| **描述** | Canonical 模板 README 为 `0.6.0`，安装给消费者的 core mirror 仍为 `0.5.0`；旧版把阶段描述成串行子目标，并遗漏 `progress` 不得放行/关闭 finding 的约束。安装器会直接复制该旧 README。 |
| **证据** | `docs/templates/README.md`（canonical）；`skills/core/docs/templates/README.md`（mirror）；`skills/install.ps1`（复制路径，约 L260） |
| **关闭要求** | 立即同步 mirror 至 canonical；增加「全文件 hash/语义一致性」测试覆盖 core mirror，防止再漂移 |
| **闭合留痕** | D-002 / A-002；mirror = 0.6.0；hash 测试 |

#### F-002 · 运行证据可被「退出码 0 + 任意 marker」伪造（P1）

| 字段 | 值 |
|------|-----|
| **级别** | `required` |
| **严重度** | `high` |
| **影响门禁** | 阶段 C；将 runtime evidence 作为发布证明 |
| **状态** | `fixed` |
| **描述** | `capture_runtime_evidence` 只检查调用方指定字符串是否出现在 stdout；仅打印 marker 的临时命令可获得 schema-valid 的 `pass`。后续兼容性报告只校验元数据、摘要与 `verdict: pass`，不验证技能是否实际加载或行为正确。**不**证明现有证据造假，但说明**不足以**证明真实运行行为。 |
| **证据** | `scripts/capture_runtime_evidence.py`（判定逻辑，约 L298）；`scripts/compatibility_report.py`（消费校验，约 L248）；审计会话临时命令复现 |
| **关闭要求** | 改为宿主输出的结构化、版本绑定断言；增加「只打印 marker 必须失败」负例；兼容性侧不得仅凭摘要/pass 字面接受弱证据 |
| **闭合留痕** | D-002 / A-002；`assertions` + 重算；marker-only 负例 |

#### F-003 · Skills 打包跟随符号链接，可能打入包外文件（P1）

| 字段 | 值 |
|------|-----|
| **级别** | `required` |
| **严重度** | `high` |
| **影响门禁** | 阶段 D；任何 zip 发布 / pack CI |
| **状态** | `fixed` |
| **描述** | 打包器以 `is_file()` 收集后直接 `zf.write()`，未拒绝 symlink，也未检查 `resolve()` 后路径仍在 `skills/` 内。发布工作流在 Ubuntu 上运行，风险真实；Windows 因缺 symlink 权限，动态复现被跳过。 |
| **证据** | `scripts/pack_skills_release.py`（收集与写入，约 L138）；`.github/workflows/skills-pack-release.yml`（Ubuntu pack，约 L33） |
| **关闭要求** | 拒绝 symlink，或对 resolve 路径做根目录 containment；在 Linux CI 增加负例 |
| **闭合留痕** | D-002 / A-002；refuse symlink + containment；Windows skip 动态负例 |

#### F-004 · P-006 fail-closed 门禁未被通用验证器完整执行（P1）

| 字段 | 值 |
|------|-----|
| **级别** | `required` |
| **严重度** | `high` |
| **影响门禁** | 阶段 E；宣称协议验证可执行；消费方/文档测试作为门禁 |
| **状态** | `fixed` |
| **描述** | 文档要求 active Charter、每个 VP 精确对齐 Charter、所有工作区必须有计划；但验证器会接受 `status: superseded` 的 Charter，只检查 VP 文件存在而不校验每个 `vision_ref`，并提供 `require_plans=False` 绕过。临时反例确认三种情况均可通过。 |
| **证据** | `docs/architecture/workspace-protocol.md`（规则）；`docs/tests/test_vision_protocol.py`（Charter 校验约 L55；工作区校验约 L98） |
| **关闭要求** | Charter 必须 active；逐个 plan ref 校验 `vision_ref`；删除通用 opt-out；验证真实 Root 与 canonical scope |
| **闭合留痕** | D-002 / A-002；require_active + plan vision_ref + no opt-out + root on-disk |

#### F-005 · 工作区校验与安装升级可复现性不足（P2）

| 字段 | 值 |
|------|-----|
| **级别** | `recommended`（P2；默认纳入路线图 F，关门前须闭合或 residual） |
| **严重度** | `med` |
| **影响门禁** | 阶段 F；非交互 CI/升级可复现 |
| **状态** | `fixed` |
| **描述** | 结构校验接受空 `workspace id`、不存在的 Root Goal；安装器在已有目录时依赖交互输入，缺少明确的 `--non-interactive` / `--force` / `--dry-run` 语义。 |
| **证据** | `docs/tests/test_workspace_protocol.py`（约 L69）；`skills/install.ps1`（约 L157）；`skills/install.sh`（约 L115） |
| **关闭要求** | 收紧工作区结构校验；为安装器定义非交互失败、显式覆盖与 dry-run 行为并测覆盖 |
| **闭合留痕** | D-002 / A-002；empty id + root on-disk；install force/non-interactive/dry-run |

### 必改项汇总（required）

- [x] **F-001** · core 模板 mirror 语义漂移（fixed · A-002）
- [x] **F-002** · 运行证据可伪造（fixed · A-002）
- [x] **F-003** · 打包 symlink 逃逸（fixed · A-002）
- [x] **F-004** · P-006 验证器未完整 fail-closed（fixed · A-002）

### 建议项（recommended）

- [x] **F-005** · 工作区校验 + 安装器非交互语义（fixed · A-002）

### 建议修复顺序（与纲领对齐）

1. 同步 `skills/core/docs/templates/README.md` + hash/语义一致性测试 → **F-001 / 阶段 B** — done
2. 运行证据结构化断言 + marker-only 负例 → **F-002 / 阶段 C** — done
3. 打包器 symlink/containment + Linux CI 负例 → **F-003 / 阶段 D** — done（Windows skip 动态）
4. 收紧 P-006 验证 → **F-004 / 阶段 E** — done
5. 安装器非交互 + 工作区校验 → **F-005 / 阶段 F** — done

### 结论与下一步

- **一句话结论（A-001 出具时）**：执行链在发布证明意义上 **fail**；4×P1 未闭合前不建议新 Skills 包发布。
- **响应后**：F-001～F-005 均 fixed；开放 required = 0。阶段 G 自审/用户确认关门仍待；**未**自动发版。
- **声明**：本意见 `source: independent`，只追加台账，**不**修改本目标或其它目标的 `status`/`progress`（立项写入的派生 progress 为路线图检查点，非本审计裁定）。

---

## A-002 · 响应 A-001 F-001～F-005（2026-07-30）

- **source**：`self`
- **类型**：`response`
- **scope**：A-001 / F-001～F-005 关闭证据
- **verdict**：`pass`（相对「是否已按 D-002 fixed」；**不是** Root/发版 close-out）

### 关闭证据表

| Finding / I-00N | 闭合路径 | 证据 |
|-----------------|----------|------|
| F-001 | fixed | `skills/core/docs/templates/README.md` = canonical 0.6.0；hash 测试 |
| F-002 | fixed | `capture_runtime_evidence` assertions；`compatibility_report` re-check；marker-only 负例 |
| F-003 | fixed | `pack_skills_release` refuse symlink + containment；`test_pack_skills_rejects_symlink` |
| F-004 | fixed | `test_vision_protocol` require_active / vision_ref / no opt-out；workspace root on-disk |
| F-005 | fixed | empty id 拒绝；install `--force`/`--non-interactive`/`--dry-run` |
| I-001 | closed (policy) | D-002 断言策略 |
| I-002 | closed | F-005 in-scope fixed |

### 仍开放项（A-002 出具时）

- 阶段 G 自审 / 用户确认 `done` → 已由 A-003 / D-003 处理
- I-003 / 全量 runtime 重采 → residual **R-021-RUNTIME-RECAPTURE**（非阻断）

### 回归

- docs **26** / scripts **49**（2 skipped）/ skills **39** — 均 OK（2026-07-30）

### 声明

本条为编排响应记录，**不是** independent 复审；不将本目标或 Root 标为 `done`。

---

## A-003 · self close-out · 阶段 G（2026-07-30）

- **source**：`self`
- **auditor**：`/govern` 编排器（Grok）
- **类型**：`close-out`
- **scope**：GOAL-021 目标整体（阶段 A～G：A-001 意见、D-002 修复、回归与成功标准）
- **verdict**：`pass`
- **长文**：无

### 范围与区间

- **覆盖**：A-001 findings F-001～F-005 闭合证据；纲领 A～F 产物；关门前全量相关测试；成功标准勾选。
- **不覆盖**：Root 终态、VP 关门、annotated tag / GitHub Release、12 宿主 runtime 全量重采、Web R-009-X。
- **与既有意见**：与 A-001 **无冲突**——A-001 当时 fail 的是「可安全发版」主张；本 close-out 仅确认 **机制修复与目标成功标准** 已达成，**不**宣称「已可发版」。

### 信息就绪核对

| 核对项 | 状态 |
|--------|------|
| I-001 / I-002 | closed |
| I-003 | closed (out of scope) · 发版见 residual R-021-RUNTIME-RECAPTURE |
| 到期 required I | 0 |

### 对照成功标准

| 成功标准 | 状态 | 证据 |
|----------|------|------|
| 审计意见落盘 A-00N | 达成 | A-001 independent |
| F-001～F-004 fixed | 达成 | A-002 关闭表 + 产物 |
| F-005 fixed | 达成 | A-002 |
| 负例覆盖 | 达成 | marker-only 测试；symlink 测试（有权限时）；P-006 反例 |
| docs/skills/scripts 回归 | 达成 | 关门前 26 / 49(2 skip) / 39 OK |
| 自审 + 用户确认关门 | 达成 | 本 A-003 + D-003 |

### Findings

本 close-out **无新增 required**。  
Recommended residual（不阻断关门）：

#### F-006 · 新断言策略下的发版级 runtime 重采（recommended）

| 字段 | 值 |
|------|-----|
| **级别** | `recommended` |
| **严重度** | `med` |
| **影响门禁** | 以新断言策略作**正式** Skills 发版证明时 |
| **状态** | `open` · non-blocking · **R-021-RUNTIME-RECAPTURE** |
| **描述** | 历史 matrix 证据无 structured `assertions`，现靠 legacy 路径通过。新 capture 已写 assertions；发版若主张「新策略充分证明」应全量重采。 |
| **关闭要求** | Root 路径 D 授权后全量 runtime 重采 + 矩阵更新；或书面 residual 接受「legacy 证据 + 机制已修」 |

#### F-007 · Windows 本机 symlink 动态负例 skip（recommended）

| 字段 | 值 |
|------|-----|
| **级别** | `recommended` |
| **严重度** | `low` |
| **状态** | `open` · non-blocking · **R-021-SYMLINK-CI** |
| **描述** | 实现已拒绝 symlink；本机无创建特权时动态测试 skip。Ubuntu 发布路径仍是真实面。 |
| **关闭要求** | 在 Linux CI 确认负例绿即可视为充分 |

### 必改项汇总（required）

- 无开放 required。

### 结论与下一步

- **一句话结论**：GOAL-021 成功标准已满足；open required = 0；可 `done`。
- **不构成**：可自动 tag/Release；Root `done`；R-009-X closed。
- **建议**：用户确认后 D-003 关门；发版另走 Root 路径 D + 可选 R-021-RUNTIME-RECAPTURE。
- **声明**：self close-out；独立复审可选，非本拍强制。
