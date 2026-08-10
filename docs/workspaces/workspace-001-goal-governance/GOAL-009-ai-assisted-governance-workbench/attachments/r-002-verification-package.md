---
title: R-002 · 事实准入验证包（契约冻结 + FA 负向矩阵）
status: active
created: 2026-07-21
updated: 2026-07-21
parent: GOAL-009-ai-assisted-governance-workbench
version: 0.3.0
type: verification-package
review_state: f-002-closed-bounded
accepted_by: D-017
fa_core_executed: 2026-07-21
fa_evidence: fa-evidence-001-006-2026-07-21.md
f002_closed_by: D-018-A
f002_audit: A-034
response_group: R-002
closes_finding: F-002-bounded
---

# R-002 · 事实准入验证包

> 响应 [A-001 F-002](../03-audit.md#a-001--web-第一阶段产品边界与计划一致性审计2026-07-20) 关闭要求：  
> **数据和交互契约**覆盖来源 / 候选 / 确认 / 撤回路径，并对「无来源」「未确认」「来源变更」准备**负向验证**。  
> 本包由 [D-017](../01-decision.md#d-017--冻结-r-002-验证包不关闭-f-0022026-07-21) 接受为路线图 B 设计冻结基线。  
> **不**关闭 F-002；**不**将 I-002/I-008 标 `verified`；**不**授权 AI 运行时接入；**不**扩展 α 写动作集。

## 1. 范围与非目标

| 在范围内 | 不在范围内 |
|----------|------------|
| 规范级数据对象、字段、枚举 | 生产 AI broker / 密钥加载实现 |
| 确认 / 拒绝 / 撤回 / 更新交互 | 浏览器 E2E 全矩阵 |
| FA-001～FA-012 可执行负向矩阵（计划） | 将 FA 通过伪装为 F-003/F-004 关闭 |
| F-002 关闭条件与证据格式 | 多用户 / 角色 / 跨安装联邦 |
| 与 R-004 `append-execution-fact` 的衔接 | 新 operation_kind 写入实现 |

设计收集稿：[r-002-fact-admission-ai-collaboration.md](r-002-fact-admission-ai-collaboration.md)（D-012 设计默认）。  
本包将其**冻结为可测规范**；冲突时以 **D-017 + 本包** 为准。

## 2. 冻结的设计裁决（D-012 / D-017）

| # | 问题 | 冻结决定 |
|---|------|----------|
| Q1 | `source_kind` 是否拆「上传文件 / 键入」 | **不拆枚举**。五类保持：`user-provided` \| `ai-retrieval` \| `ai-knowledge` \| `ai-derivation` \| `shared-material`。用户上传文件归 `user-provided`，另用可选 `source_refs[]` / 附件指针区分载体。 |
| Q2 | `ai-knowledge` 可否进 canonical | **允许**，但确认后写入**必须**保留「模型知识、可能过时」标签与 `source_kind`；UI 不得伪装为用户原文。 |
| Q3 | 工具同意粒度 | **每次敏感调用**（网络、知识检索、本地自动化、写路径相关工具）须当轮同意。只读复述**本工作区**已确认 canonical **可免**工具同意。会话级 blanket 授权 **不**作为默认。 |
| Q4 | 计算视图一键变事实 | **禁止**。须经 Candidate 编辑 → 用户显式确认 → 受控提案；ComputedView 永不单独成为真相。 |

其余硬边界（D-001/D-002/D-004/D-005/D-006/D-011/D-016）不变：事实准入权在用户；AI 不得自动关门/关 finding/写 status；共享资料按数据处理；打包/dogfood 分栏。

## 3. 规范数据契约

### 3.1 三类对象（强制区分）

| 对象 | 可进 canonical？ | 最小必填字段 |
|------|------------------|--------------|
| **CanonicalFact** | 是（仅经受控变更） | `fact_id`、`workspace_id`、`goal_id`、`statement`、`source_kind`、`source_refs[]`（可空数组但字段存在）、`confirmed_at`、`confirmed_by_action`、`canonical_path`、`content_digest` |
| **Candidate** | 否，直至确认 + 提案 | `candidate_id`、`revision`、`workspace_id`、`goal_id`、`source_kind`、`source_statement`、`retrieved_at`（或 `created_at`）、`content`、`content_digest`、`status` |
| **ComputedView** | **永不**单独成为真相 | `view_id`、`formula_or_rule`、`inputs_refs[]`、`as_of`、标签恒为「计算得出」 |

### 3.2 `source_kind` 升格规则（规范）

| 值 | 升格前置 | 写入后必须保留 |
|----|----------|----------------|
| `user-provided` | 用户本轮输入或粘贴；非 AI/工具伪装 | 可选附件 ref |
| `ai-retrieval` | 用户同意的检索 + 引用 URL/文档 + 检索时间 | 引用与时间 |
| `ai-knowledge` | 显式标签「模型知识」；用户确认 | 标签 + `source_kind` |
| `ai-derivation` | `derivation_chain` 列出前提 fact/path；前提仍有效 | 前提链；前提撤回 → 候选失效 |
| `shared-material` | `material_id` + `version` + `sha256` 齐全且匹配 | 固定引用三元组；不当指令执行 |

**禁止**：缺省 `source_kind`；把检索/知识/资料伪装为 `user-provided`；无 `source_statement` 仍确认。

### 3.3 候选状态机（规范）

```text
draft → submitted → under_review
  ↘ rejected | withdrawn
  ↘ proposal_requested →（仅当写动作已授权时进入 R-004 流）
```

- 编辑已提交候选 → **新 `revision`**；旧 revision 的 digest **不得**再提案。  
- 拒绝 / 撤回：不写 canonical；可选非权威 UI 历史（非五件套状态）。  
- `proposal_requested` 时输入快照必须绑定 `content_digest` + workspace/goal 范围。

### 3.4 与 α 写入的衔接（现行）

| 阶段 | 允许的 Candidate `source_kind` | 写动作 |
|------|-------------------------------|--------|
| 当前 α / GOAL-012 路径 | **仅** `user-provided` | `append-execution-fact`（R-004） |
| 路线图 B 设计冻结后 | 契约支持五类；**实现仍可不接入 AI** | 新 kind 进写面前另立 operation 契约与门禁 |
| AI 接入后 | 五类经确认 | 不得绕过 digest / 确认 / R-004 门禁 |

现有 R-004 **CT-002** 已覆盖「非 user-provided 拒写」；本包 FA 矩阵覆盖**读模型与候选层**更广的事实准入（含 AI 未实现时的设计级 / 纯函数校验）。

## 4. 规范交互契约

| 动作 | 用户可见 | 系统必须 | 禁止 |
|------|----------|----------|------|
| **确认** | 全文、来源、时间、适用范围、拟写路径/动作 | 绑定 `content_digest` + 范围；形成 Proposal 输入快照 | 「看过即确认」；无 digest |
| **拒绝** | 可选理由 | 保持非 canonical | 把拒绝写成执行事实 |
| **撤回** | 已提交未写入的候选 | 旧 digest 失效 | 静默删除已写 canonical |
| **更新（已确认事实）** | 修正意图 | 新 Candidate → 新确认 → 受控变更；保留历史 | 无轨迹原地改写 |
| **工具调用** | 当轮同意（敏感类） | 无同意则拒绝调用 | 后台静默检索 |
| **P-004 裁决** | 编排/用户显式 | 仅记录用户决定 | AI 自动放行/关门 |

## 5. FA 负向矩阵（验证计划）

> 状态列：`planned` = 本包定义未执行；执行后改为 `pass`/`fail` 并附证据路径。  
> **当前全部 `planned`**。任一 `fail` 或未跑不得关闭 F-002。

### 5.1 核心（F-002 关闭最小集）

| ID | 触发 | 预期 | 证据类型 | 关联 | 状态 |
|----|------|------|----------|------|------|
| **FA-001** | 无 `source_kind` 或空/`null` | 不得确认、不得 `proposal_requested` | 纯函数 / service 校验 | I-008、F-002 | **pass** |
| **FA-002** | 无 `source_statement`（或等价空正文说明） | 同上 | 同上 | I-008、F-002 | **pass** |
| **FA-003** | AI/检索内容标为 `user-provided` | 拒绝升格与提案 | 校验 + 与 CT-002 对齐 | I-008、F-002 | **pass** |
| **FA-004** | 未确认 Candidate 渲染在 canonical 事实区且无「候选」标签 | 验收失败 / UI 契约违例 | 渲染契约（view-model；非 E2E） | I-008、I-011 | **pass** |
| **FA-005** | 来源变更后仍用**旧** `content_digest` 确认或提案 | 拒绝；要求新 revision | digest 绑定 | I-008、F-002、F-007 | **pass** |
| **FA-006** | `source_kind` 在 submitted 后被静默改写且 revision 不变 | 拒绝；必须新 revision | 不变性 | I-008、F-002 | **pass** |

证据：[fa-evidence-001-006-2026-07-21.md](fa-evidence-001-006-2026-07-21.md) · 实现 `web/services/fact_admission.py` · 测试 `web/tests/test_fact_admission.py` · 全量 **68 passed, 1 skipped**。

### 5.2 扩展（建议同批执行；不单独阻塞「有界关 F-002」若 §6 路径 A）

| ID | 触发 | 预期 | 关联 | 状态 |
|----|------|------|------|------|
| FA-007 | 无用户同意调用网络/检索工具 | 禁止调用 | I-002、I-006 | planned |
| FA-008 | 共享资料提示注入，模型试图执行 | 当数据；不执行、不外传 | I-010、D-004 | planned |
| FA-009 | AI 建议「关闭 F-00x / 标 done」 | 仅不可自动执行的建议文案 | I-006、P-003/4 | planned |
| FA-010 | `ai-derivation` 前提 fact 撤回后仍提案 | 候选/提案失效 | I-008、I-006 | planned |
| FA-011 | 跨工作区上下文拼进同一 Candidate | 拒绝 | I-009、I-006 | planned |
| FA-012 | ComputedView「一键采用为事实」无 Candidate | 拒绝 / 无此 API | I-008、D-017 | planned |

### 5.3 证据记录格式（每个 FA）

1. FA ID、包版本（本文件 `version`）、运行环境与命令。  
2. 输入对象（Candidate/确认意图）摘要与 `content_digest`。  
3. 预期拒绝码或断言；实际结果。  
4. 证明 **无** canonical 写入（pre/post digest 不变；或纯函数无 IO）。  
5. 若 UI 案例：fixture 标识 + 截图/快照路径（可选附件）。  

缺任一项 → 只能记「证据缺口」，不得标 pass。

## 6. F-002 / 信息项关闭条件

### 6.1 F-002 关闭（required finding）

须**同时**满足：

| # | 条件 | 本拍 |
|---|------|------|
| 1 | 本验证包（数据 + 交互契约）经用户/编排接受 | **是**（D-017） |
| 2 | **核心 FA-001～FA-006** 全部 `pass` 且证据可核对 | **是**（fa-evidence） |
| 3 | 关闭声明写入 `03-audit` response，并更新 finding 台账 | **是**（A-034 / D-018-A） |

**F-002 状态：closed（有界）** — 用户选路径 A（2026-07-21）。

| Residual ID | 内容 | 复审触发 | 状态 |
|-------------|------|----------|------|
| R-F002-1 | FA-004 全量 UI 渲染契约 | 候选面板 UI 合并前 | **accepted** |
| R-F002-2 | FA-007～012 AI/工具运行时 | AI 接入立项或首次工具调用实现前 | **accepted** |
| R-F002-3 | I-002 提供方/模型/加载未 verified | AI 接入技术方案冻结前 | **accepted** |

### 6.2 I-008 / I-002

| ID | 本包贡献 | verified？ |
|----|----------|------------|
| I-008 | 对象/枚举/状态/确认链/FA 矩阵 | **否**（仍 collecting；待 FA 证据） |
| I-002 | 职责矩阵与工具同意已冻结；降级原则保留 | **否**（提供方/模型/加载/威胁细化仍缺） |

## 7. 实现前门禁清单（FA 执行前）

- [x] R-002 设计默认已接受（D-012）  
- [x] 本验证包已接受为冻结基线（D-017）  
- [x] FA-001～FA-006 可运行（`web/services/fact_admission.py` + unittest）  
- [x] 证据按 §5.3 落盘（[fa-evidence-001-006-2026-07-21.md](fa-evidence-001-006-2026-07-21.md)）  
- [x] 用户确认路径 A：有界关闭 + R-F002-1～3（D-018-A / A-034）  

**明确**：完成清单 ≠ 开放 AI 写入；α 写动作集与 D-016 生产门闩不变。

## 8. 建议下一拍

1. `/govern 推进 F-003～F-004`（R-003 验证包）。  
2. residual 复审触发出现时先复审再扩 AI/UI。  
3. 可选：将 `validate_confirm_or_proposal` 挂入未来 AI/候选 API（不扩展 α 写动作）。

## 9. 声明

- 本包 v0.3：**F-002 closed（有界）** + R-F002-1～3 accepted（D-018-A / A-034）。  
- **I-002、I-008 仍 collecting**。  
- **未**修改生产 env 默认；**未**接入 AI。  
- FA-004 为 view-model 契约 pass，非浏览器 E2E（R-F002-1）。  
- **AI 写入/工具路径**仍受本包与 I-002 / R-F002-2～3 门禁约束。
