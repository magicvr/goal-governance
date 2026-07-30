---
id: GOAL-021-skills-release-chain-hardening
doc: audit
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.1.0
---

# 审计 · GOAL-021

## 信息就绪核对（按 scope）

| 核对项 | 状态 | 备注 |
|--------|------|------|
| 影响本 scope 的 I-00N | I-001～I-003 open（均 non-blocking） | 见 00-meta |
| 到期 required 信息项 | 无 | 实施前无到期 required I |
| 资料引用 | 无 | 本目标不依赖 shared-materials 固定引用 |

## 意见台账索引

| A-ID | 日期 | source | scope | verdict | 开放 required |
|------|------|--------|-------|---------|---------------|
| A-001 | 2026-07-30 | independent | 规则→分发→证据→发布 执行链 | fail（相对「可安全发版」主张） | **4**（F-001～F-004） |

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
| **状态** | `open` |
| **描述** | Canonical 模板 README 为 `0.6.0`，安装给消费者的 core mirror 仍为 `0.5.0`；旧版把阶段描述成串行子目标，并遗漏 `progress` 不得放行/关闭 finding 的约束。安装器会直接复制该旧 README。 |
| **证据** | `docs/templates/README.md`（canonical）；`skills/core/docs/templates/README.md`（mirror）；`skills/install.ps1`（复制路径，约 L260） |
| **关闭要求** | 立即同步 mirror 至 canonical；增加「全文件 hash/语义一致性」测试覆盖 core mirror，防止再漂移 |
| **闭合留痕** | — |

#### F-002 · 运行证据可被「退出码 0 + 任意 marker」伪造（P1）

| 字段 | 值 |
|------|-----|
| **级别** | `required` |
| **严重度** | `high` |
| **影响门禁** | 阶段 C；将 runtime evidence 作为发布证明 |
| **状态** | `open` |
| **描述** | `capture_runtime_evidence` 只检查调用方指定字符串是否出现在 stdout；仅打印 marker 的临时命令可获得 schema-valid 的 `pass`。后续兼容性报告只校验元数据、摘要与 `verdict: pass`，不验证技能是否实际加载或行为正确。**不**证明现有证据造假，但说明**不足以**证明真实运行行为。 |
| **证据** | `scripts/capture_runtime_evidence.py`（判定逻辑，约 L298）；`scripts/compatibility_report.py`（消费校验，约 L248）；审计会话临时命令复现 |
| **关闭要求** | 改为宿主输出的结构化、版本绑定断言；增加「只打印 marker 必须失败」负例；兼容性侧不得仅凭摘要/pass 字面接受弱证据 |
| **闭合留痕** | — |

#### F-003 · Skills 打包跟随符号链接，可能打入包外文件（P1）

| 字段 | 值 |
|------|-----|
| **级别** | `required` |
| **严重度** | `high` |
| **影响门禁** | 阶段 D；任何 zip 发布 / pack CI |
| **状态** | `open` |
| **描述** | 打包器以 `is_file()` 收集后直接 `zf.write()`，未拒绝 symlink，也未检查 `resolve()` 后路径仍在 `skills/` 内。发布工作流在 Ubuntu 上运行，风险真实；Windows 因缺 symlink 权限，动态复现被跳过。 |
| **证据** | `scripts/pack_skills_release.py`（收集与写入，约 L138）；`.github/workflows/skills-pack-release.yml`（Ubuntu pack，约 L33） |
| **关闭要求** | 拒绝 symlink，或对 resolve 路径做根目录 containment；在 Linux CI 增加负例 |
| **闭合留痕** | — |

#### F-004 · P-006 fail-closed 门禁未被通用验证器完整执行（P1）

| 字段 | 值 |
|------|-----|
| **级别** | `required` |
| **严重度** | `high` |
| **影响门禁** | 阶段 E；宣称协议验证可执行；消费方/文档测试作为门禁 |
| **状态** | `open` |
| **描述** | 文档要求 active Charter、每个 VP 精确对齐 Charter、所有工作区必须有计划；但验证器会接受 `status: superseded` 的 Charter，只检查 VP 文件存在而不校验每个 `vision_ref`，并提供 `require_plans=False` 绕过。临时反例确认三种情况均可通过。 |
| **证据** | `docs/architecture/workspace-protocol.md`（规则）；`docs/tests/test_vision_protocol.py`（Charter 校验约 L55；工作区校验约 L98） |
| **关闭要求** | Charter 必须 active；逐个 plan ref 校验 `vision_ref`；删除通用 opt-out；验证真实 Root 与 canonical scope |
| **闭合留痕** | — |

#### F-005 · 工作区校验与安装升级可复现性不足（P2）

| 字段 | 值 |
|------|-----|
| **级别** | `recommended`（P2；默认纳入路线图 F，关门前须闭合或 residual） |
| **严重度** | `med` |
| **影响门禁** | 阶段 F；非交互 CI/升级可复现 |
| **状态** | `open` |
| **描述** | 结构校验接受空 `workspace id`、不存在的 Root Goal；安装器在已有目录时依赖交互输入，缺少明确的 `--non-interactive` / `--force` / `--dry-run` 语义。 |
| **证据** | `docs/tests/test_workspace_protocol.py`（约 L69）；`skills/install.ps1`（约 L157）；`skills/install.sh`（约 L115） |
| **关闭要求** | 收紧工作区结构校验；为安装器定义非交互失败、显式覆盖与 dry-run 行为并测覆盖 |
| **闭合留痕** | — |

### 必改项汇总（required）

- [ ] **F-001** · core 模板 mirror 语义漂移（open）
- [ ] **F-002** · 运行证据可伪造（open）
- [ ] **F-003** · 打包 symlink 逃逸（open）
- [ ] **F-004** · P-006 验证器未完整 fail-closed（open）

### 建议项（recommended）

- [ ] **F-005** · 工作区校验 + 安装器非交互语义（open；默认路线图阶段 F）

### 建议修复顺序（与纲领对齐）

1. 同步 `skills/core/docs/templates/README.md` + hash/语义一致性测试 → **F-001 / 阶段 B**
2. 运行证据结构化断言 + marker-only 负例 → **F-002 / 阶段 C**
3. 打包器 symlink/containment + Linux CI 负例 → **F-003 / 阶段 D**
4. 收紧 P-006 验证 → **F-004 / 阶段 E**
5. 安装器非交互 + 工作区校验 → **F-005 / 阶段 F**

### 结论与下一步

- **一句话结论**：执行链在发布证明意义上 **fail**；4×P1 未闭合前不建议新 Skills 包发布，也不宜把现有 runtime 证据当作充分证明。
- **建议编排器下一步**：用户确认后按阶段 B 起修 F-001（可一句「按建议顺序修」）；P-004 仅在要 residual/overruled 某 finding 或跳过 F-005 时触发。
- **声明**：本意见 `source: independent`，只追加台账，**不**修改本目标或其它目标的 `status`/`progress`（立项写入的派生 progress 14% 为路线图检查点，非本审计裁定）。
