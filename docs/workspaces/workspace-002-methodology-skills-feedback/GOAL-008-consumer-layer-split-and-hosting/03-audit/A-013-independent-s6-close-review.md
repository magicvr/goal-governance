---
id: A-013
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-013
source: independent
provider: grok build / grok-4.6 / reasoning-effort high（本地 CLI `grok` 1.0.30）
scope: S6 关门与发布准备（12 格证据 / 发布门禁 / required 闭合 / 必达便利边界）
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-013 · S6 独立关门复审（grok build · grok-4.6 · high，2026-09-13）

> 独立会话**只读**核对，结论**未**直接写入本目标；编排器代贴落盘并保留 `source: independent`，正文未改写（仅去流程旁白）。
> 基线：HEAD `37ca560`（`docs: land v0.13.3 changelog and package version ledger`），分支 `dev`；`main` 停 `d073f44`；本地仅 `v0.13.2` tag。核对时工作树含未提交的 `00-meta`/索引改动与未跟踪的 D-012/E-008。

## verdict

**conditional**

12 格 `v0.13.3` runtime 证据**真实、全部 `pass`、均被矩阵引用**，没有 fail/blocked 格被当成通过。发布范围（D-011）已冻结，但 **S6 不能关门、也不能打 `v0.13.3` tag**：公开版本台账把未打 tag 的版本写成已发布；A-005 F-001 的层语义宿主探针被 12 格 dispatch 重捕获从「待完成」里拿掉；S6 决策/执行台账（D-012、E-008）尚未入库，当前 HEAD 在 `dev` 而非 `main`。

## 独立核对结果

### 1. 12 格证据表（consumer × entrypoint → verdict）

矩阵 `candidateRevision = v0.13.3`，`requiredEntrypoints` 仍四入口；每格 `status: runtime-verified`，evidence 指向 `docs/releases/runtime/v0.13.3/<consumer>-<entrypoint>-2026-09-13.json`；契约三 adapter 同为四入口、`verificationStatus: verified`。

| consumer | 宿主版本 | govern | audit | vision | vision-audit |
|----------|----------|--------|-------|--------|--------------|
| claude-code-cli | 2.1.270 | pass | pass | pass | pass |
| grok-build-cli | 1.0.30 / grok-4.6 | pass | pass | pass | pass |
| github-copilot-cli | 1.0.75 / gemini-3.8-flash-high | pass | pass | pass | pass |

抽查（12/12 同构）：`result.verdict=pass`、`markerObserved=true`、断言策略 `marker+entrypoint+nontrivial-stdout@1` 三条 assertion `observed=true`、`behaviorSources` = `AGENTS.md` + `skills/prompts/00-govern-orchestrator.md`。**探针类型均为 dispatch marker，不是 CE1–CE10 层语义 corpus。**

**有无 fail/blocked 被当通过？没有。** 矩阵 12 条路径与目录内 12 份 JSON 一一对应，全部 pass。`/commit` **不在**这 12 格中。

### 2. 发布门禁对照（D-011 §6 × 00-meta S6 行 × 只读 git）

| 项 | 状态 |
|----|------|
| I-006 范围冻结 | 决定已写（D-011）；**I-006 台账仍 `open`** |
| 全量回归 / `--require-ready` / rehearsal | 主张已完成；独立会话**禁用运行测试**，不能独立证实 |
| 12 格 runtime 重捕获 | **完成（证据在 git）** |
| 隔离仓冷启动 + 升级 | **完成（附件在 git）** |
| 版本落地 CHANGELOG + docs/README | 文件已改，但**身份超前** |
| S6 self 关门意见 | **未完成**（当时 `03-audit/` 无 S6 条目） |
| S6 independent 关门意见 | 本意见即此 |
| PR / merge 到 `main` | **未完成**（HEAD 在 `dev`） |
| annotated tag + tag workflow | **未执行** |
| Release 资产核对 | **未执行** |
| `/commit` 单列宿主证据 | **未完成** |

D-011 §1：tag 必须指向**合入 `main` 后的 merge commit** → **现在打 tag 会直接违反冻结规则。**

### 3. required 逐项判定（独立会话）

| Finding | 可否闭合 | 判定 |
|---------|----------|------|
| A-001 F-005（I-006） | **否（部分满足）** | 字段已冻结；revision/tag/Release 不存在；I-006 表仍 open |
| **A-005 F-001（宿主层语义行为）** | **否** | 12 格是**入口 dispatch**，不分类 CE1–CE10；不能证明「AI 已不再混淆」。工作树 00-meta 的待完成列表已把「宿主行为探针」收成只剩 `/commit` —— **这是用重捕获掩盖未验证行为** |
| A-005 F-002（runtime 锚点过期） | **实质可闭合，台账未改** | 12 份新证据 + 矩阵改指 v0.13.3；A-005 正文仍 open |
| A-006 / A-008 F-001（冷启动/升级） | **主要路径可闭合，子项仍缺** | 未做闭合句要求的「缺列/legacy 不判不完整安装」；附件 §5 的「runtime 未重捕获 / I-006 未冻结」已过期 |
| A-009 F-001（`/commit` 宿主调用） | **否** | 12 格不含 commit |

**没有把 fail 格写成 pass。**

### 4. 必达／便利边界

`/commit` **未**进入：契约 `hostEntrypoints`、`deliveryChannels.files.entrypoints`、矩阵 `requiredEntrypoints` 与 12 格 `entrypoints[].name`；MCP notes 亦声明不入工具集。
守卫：**能挡**四入口等式与 files/host 通道（`test_file_l1.py`）与矩阵每格 name（`test_skills_orchestrator.py`）；**不能单独挡**把 `commit` 写进 `deliveryChannels.mcp.entrypoints`（守卫缝，非当前越界）。

## Findings

### F-001 · 12 格 dispatch 重捕获不能闭合 A-005 F-001（层语义宿主探针仍缺）

| 字段 | 值 |
|------|-----|
| level | **required** |
| severity | high |
| status | open |
| evidence | `03-audit/A-005-s2-stage-self.md`（S2 通过阈值要求「静态谓词 + 至少一个真实宿主对 CE corpus 复核」）；`attachments/s1-acceptance-matrix.md`（同）；`docs/releases/runtime/v0.13.3/claude-code-cli-govern-2026-09-13.json`（dispatch marker，非 CE corpus）；工作树 `00-meta.md` 待完成列表已移除「宿主行为探针」 |
| 影响门禁 | S6 关门；「AI 已不再混淆」宣称；**不得**把 A-005 F-001 标 `fixed` |

### F-002 · 公开版本台账把未打 tag 的 `v0.13.3` 写成已发布

| 字段 | 值 |
|------|-----|
| level | **required** |
| severity | high |
| status | open |
| evidence | `CHANGELOG.md`（`Unreleased` 写「空；2026-09-13 **发布** v0.13.3」）；`docs/README.md`（「最近发布基线」把 `v0.13.3` 与已存在的 `v0.13.2` 并列；同节又写「发布**候选**」，自相矛盾）；`git tag -l` 无 `v0.13.3`；HEAD 不在 `main` |
| 影响门禁 | 发布身份 / S6 关门；D-011 §2「不得把计划资产写成已上传事实」 |

版本号可以先落 CHANGELOG（D-011 允许），但不能在 tag/workflow 之前写进「最近发布基线」或把 Unreleased 写成已发布。

### F-003 · S6 决策/执行台账未入库；当前 HEAD 不能当发布 revision

| 字段 | 值 |
|------|-----|
| level | **required** |
| severity | medium |
| status | open |
| evidence | 核对时 `D-012`、`E-008` 为未跟踪；`01-decision.md` 索引未含 D-011/D-012；`02-execution.md` 无 E-008；`03-audit/` 无 S6 self；HEAD 在 `dev` |
| 影响门禁 | 发布 / S6 关门 |

### F-004 · 便利入口守卫未覆盖 MCP 通道 entrypoints（recommended）

| 字段 | 值 |
|------|-----|
| level | recommended |
| severity | low |
| status | open |
| evidence | `docs/tests/test_file_l1.py` 只断言 `hostEntrypoints` 与 `files.entrypoints`，未断言 `deliveryChannels.mcp.entrypoints` |
| 影响门禁 | 无（当前未越界） |

## 与既有意见的异同

- **同向**：A-009 F-001、A-001 F-005 作为发布/关门阻断仍成立；A-005 F-002 的闭合路径已按 D-011 §4 执行且 12/12 pass；A-006/A-008 F-001 主路径已有附件证据；`/commit` 未进入必达集，与 A-001 F-004 / D-002 §4 / D-010 一致。
- **收紧**：A-005 F-002 **不能**连带闭合 A-005 F-001；工作树把「宿主行为探针」从待完成里拿掉，是**相对既有 self 记录的退步**。
- **新发现**：公开台账发布身份超前；D-012/E-008 未入库；无 S6 self 意见。
- **无「一要一否」冲突需要用户裁决**；用户已选「本轮不开残余」→ 上列 required 必须 `fixed`，不能 residual 放行。

## 范围与限制

只读指定路径；未跑测试、未装依赖、未联网，故**不能独立证实** unittest 计数、`--require-ready`、rehearsal 产物与 GitHub Release 页。未核 `behaviorSources` 的 sha256 是否等于当前 `AGENTS.md`（该文件不在允许清单）。

## 建议下一步（独立会话原文）

1. **不要**对当前 HEAD 打 `v0.13.3`，**不要**把 GOAL-008 标 `done`。
2. 响应时：A-005 F-001、A-009 F-001、A-001 F-005 保持 open；A-005 F-002 可标 `fixed`；A-006/A-008 F-001 若接受「缺列/legacy 子项不在本轮演示」须书面范围 + 复审触发，否则补核对。
3. 入库 D-012、E-008，补三个索引，纠正 I-003/I-006 表状态；写 S6 self 关门意见。
4. 公开台账：Unreleased 改回「尚未发布」；tag 存在前从「最近发布基线」去掉 `v0.13.3`。
5. 层语义：至少一个宿主按 CE corpus 做 probe（或用户书面 residual）；`/commit`：至少一个宿主实调 + 一个 fail-closed 负例，单列非必达。
6. 之后才是：提交 → PR merge 进 `main` → annotated tag 打在 **merge commit** → 跑 tag workflow → 逐项对 sha256。
