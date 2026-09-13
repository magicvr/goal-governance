---
id: A-015
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-015
source: self
auditor: 编排主线程 /govern
scope: S6 阶段自审（回归、证据、发布准备）＋ A-005 F-001 / A-009 F-001 / A-006+A-008 F-001 子项闭合
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-015 · S6 阶段自审（2026-09-13）

## 头字段

- **source**：self
- **auditor**：编排主线程 `/govern`
- **类型 / scope**：stage · S6；含对 A-005 F-001、A-009 F-001、A-006/A-008 F-001 子项的闭合判定
- **verdict**：conditional

## 范围与区间

- covered：全量回归；12 格证据重捕获；`--require-ready` 与 rehearsal；隔离仓冷启动/升级/legacy 核对；`/commit` 宿主实测；层语义 CE1–CE10 宿主探针；A-013 响应后的台账一致性。
- excluded：**发布产出**（PR/merge/tag/tag workflow/Release 资产核对）——未执行；Grok/Codex/Copilot 上的 `/commit` 实测；「治理根改为 `governance/`」与大小写变体等 D-009 §5 未实现项。
- 用户裁决：S6 **含正式发布**、**本轮不开残余**（[D-011](../01-decision/D-011-s6-release-scope-freeze.md)）。

## 成果与证据

| 主张 | 证据 |
|------|------|
| 全量回归绿 | docs 65 / skills 89 / scripts 128（skipped=4）；镜像 37 对 0 漂移；`git diff --check` 洁净 |
| 12 格证据新鲜且 pass | `docs/releases/runtime/v0.13.3/`；`capture_runtime_evidence.py --check` 12/12；`compatibility_report.py --require-ready` 通过 |
| release rehearsal 通过 | `artifacts/release-evidence-rehearsal.json`（`release status: rehearsal`、`checks passed: True`） |
| 隔离仓冷启动/升级/legacy | [s6-isolated-consumer-evidence.md](../attachments/s6-isolated-consumer-evidence.md)、[commit-entry-host-evidence.md](../attachments/commit-entry-host-evidence.md) §2 |
| 层语义宿主探针 | [layer-semantics-host-probe.md](../attachments/layer-semantics-host-probe.md)（Claude + Grok，各 10 例） |
| `/commit` 宿主实测 | [commit-entry-host-evidence.md](../attachments/commit-entry-host-evidence.md) §1（正例 + 负例 + 权限不足负例） |

## Findings 闭合判定

### A-005 F-001 / A-013 F-001（宿主层语义行为）→ **fixed（含登记残余）**

- 要求：S2 通过阈值 = 静态谓词 **加上** 至少一个真实宿主按 CE1–CE10 复核（`A-005` 原文；`s1-acceptance-matrix.md` §4）。
- 交付：**两宿主 × 10 例**，原始输出留档；**行为层全部正确**（VP 不得作 parent／不建五件套／组合编排不写目标事实／阶段计划非树节点／VP status ≠ Goal status，两宿主一致）。
- 残余（已登记，不隐瞒）：单一标签口径噪声 —— Claude CE5、Grok CE1 各有一例 `verdict` 标签与 `action` 不一致（两例 action 均正确）；两宿主、单轮、静态只读，**不**支持「零歧义」的更强宣称。后续如需把本探针变门禁，应分列 `verdict` 与 `recommended_action` 两字段。
- 判定：**闭合**（要求已满足、残余已具名），但**不得**据此宣称「AI 已不再混淆层级」这一更强命题。

### A-009 F-001（`/commit` 宿主调用）→ **fixed**

- 要求：至少一个宿主实调 `/commit` + 一个 fail-closed 负例，且证据单列、不进 12 格矩阵。
- 交付：Claude `2.1.270` 正例（提交 `6d357ac`，`git show --stat` 仅 `a.txt`，`b.txt` 未被吞入）+ 负例（无 owned path → `COMMIT_ID: none`，HEAD 未变）+ 权限不足负例（拒绝执行、未提交）；证据单列于附件，**未**进入必达格。
- 残余：仅 Claude 一个宿主实测；其余宿主为落盘层验证。

### A-005 F-002（runtime 证据锚点过期）→ **fixed**

12 份 `v0.13.3` 证据全部 pass 且锚点对当前树有效；v0.13.2 快照保留为历史；矩阵/契约指向新目录。

### A-006 F-001 / A-008 F-001（隔离仓冷启动与升级）→ **fixed**

冷启动骨架复制不再泄漏生产仓 VP 行；消费方自有 `AGENTS.md` 保留 + 唯一受管区间；升级重放幂等；**legacy 缺列/他仓遗留行不改写、不阻断、不构成「不完整安装」**（后者由缺 MUST 文件驱动）。

### A-001 F-005（I-006 发布范围）→ **保持 open**

范围已在 [D-011](../01-decision/D-011-s6-release-scope-freeze.md) 冻结、I-006 标 `frozen`；但**发布产出不存在**（无 merge、无 tag、无 workflow 运行、无资产核对），故不闭合。

## 必改项汇总

| Finding | 来源 | 状态 | 仍阻断 |
|---------|------|------|--------|
| A-001/F-005（I-006 发布产出） | independent | **open** | S6 关门与发布 |
| A-005 F-001 / A-013 F-001（层语义宿主） | self + independent | **fixed**（残余已具名） | — |
| A-005 F-002（runtime 锚点） | self | **fixed** | — |
| A-006/A-008 F-001（隔离仓） | self | **fixed** | — |
| A-009 F-001（`/commit` 宿主） | self | **fixed** | — |
| A-013 F-002/F-003/F-004 | independent | **fixed**（见 A-014） | — |

**开放 required = 1**（A-001 F-005），其闭合条件 = 发布产出可核对。无 residual、无 overruled、无冲突。

## 与既有意见的异同

- 与 **A-013（independent，conditional）** 同向：其 3 条 required 已按 A-014 处理，其中 F-001 的补做证据由本审判定闭合。
- 与 **A-007（independent，pass）** 同向：其「S6 前须闭合」清单中，除发布产出外的各项均已处理。
- 无相反 verdict；不触发 P-004.2。

## 结论与下一步

**verdict：`conditional`。** S6 的技术工作与证据已完备：回归全绿、证据新鲜、门禁通过、隔离仓与宿主行为均有实测。**唯一开放 required 是发布产出本身**（A-001 F-005），它需要用户授权后才能执行：提交 → PR → merge 进 `main` → annotated tag 指向 merge commit → tag workflow（GitHub Environment `release` 审批）→ 逐项核对 Release 资产 sha256。

**在发布产出可核对之前：不打 tag、不标 `done`、不宣称 `v0.13.3` 已发布**（A-013 F-002 的教训已固化在 `CHANGELOG.md` 与 `docs/README.md` 的措辞里）。
