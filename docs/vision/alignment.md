---
doc_type: vision-alignment
title: 愿景对齐契约与门禁
status: active
created: 2026-07-28
updated: 2026-07-28
version: 0.2.0
parent: null
---

# 对齐契约 · Vision → VP → Workspace

本文件是愿景体系的**规则权威**。与实例声明冲突时，以本文件与 [charter.md](charter.md) 为准；`consumer-checklist.md` 不得宽于或严于本文件。

## 1. 类型与禁止

| 类型 | 允许 status | 禁止 |
|------|-------------|------|
| Charter (`doc_type: vision-charter`) | `active` \| `superseded` | Goal 的 `done` / `draft` / `blocked` / `cancelled` 语义；progress%；goal-tree |
| Vision Plan (`doc_type: vision-plan`) | `planned` \| `active` \| `closed` \| `abandoned` | Goal 的 `done` 作为 VP status；完整五件套；progress% 权威 |
| 工作区目标 | 既有 Goal status | 把 vision/VP 目录当目标父节点 |

愿景体系**不是**第二套目标状态源；不汇总各区 progress，不关闭 finding。

## 2. 三层对齐链

```text
Charter: vision_id@version
    ↑  VP.vision_ref 精确匹配（v1 不做 semver 范围）
Vision Plan: VP-NNN-slug
    ↑  workspace/Root.plan_refs 包含该 VP；primary_plan 必填且 ∈ plan_refs
Workspace + Root Goal
```

- 默认 Root **不强制**再抄 `vision_ref`；经 VP 间接对齐 Charter。
- 子目标默认继承 Root 的规划语境；显式偏离须用户确认（P-004）并留痕。

## 3. 工作区声明（`workspace.md` frontmatter）

| 字段 | 要求 |
|------|------|
| `vision_role` | `primary` \| `delivery` \| `sandbox` |
| `plan_refs` | 非 sandbox 例外时至少一 个 VP id；多个用逗号分隔 |
| `primary_plan` | **必填**（非 opt-out）；必须出现在 `plan_refs` 中 |
| `vision_opt_out_reason` 等 | 仅当 sandbox 且无 `plan_refs` 时 |

- **primary 禁止 opt-out。**
- 至多一个工作区 `vision_role: primary`（与 [workspaces.md](workspaces.md) 一致）。

### 3.1 Primary 声明冲突裁决

Primary 可能出现在三处：`workspace.md` 的 `vision_role: primary`、[workspaces.md](workspaces.md) 的 `role: primary`、Charter 的 `primary_workspace`。

| 情形 | 行为 |
|------|------|
| 三处一致 | 通过 |
| 仅一处声称 primary，其它未声明或为空 | 以**已声明**处为准，并应在下一维护回合补齐另外两处 |
| 两处或以上**互相矛盾**（不同 `workspace_id`） | **fail closed**：不得推进受影响的新建 Root/放行/关门；展示冲突；按 P-004 等用户裁决后留痕再改 |
| Charter `primary_workspace` 指向不存在的工作区 | fail closed，直至修正 Charter 或创建/声明该区 |

权威顺序（仅用于**修复建议**，不能静默覆盖用户已确认的矛盾）：`alignment` 本文件规则 → 用户书面裁决 → 再改 Charter / workspaces.md / workspace.md。实例与本文件冲突时仍以本文件 + charter 为准。

## 4. Root Goal 声明

Root `00-meta.md` 应含与 workspace 一致的 `plan_refs`、`primary_plan`，以及简短 `serves_summary`（可写在 frontmatter 或「愿景对齐」节）。  
`primary_plan` 必须能解析为 `docs/vision/plans/<id>.md`（id 与文件名一致）。

## 5. VP 与工作区绑定

| VP status | 工作区绑定 |
|-----------|------------|
| `planned` | 允许 0 个工作区 |
| `active` | 期望 ≥1；若为 0，见下「空转」规则 |
| `closed` | 保留历史绑定；默认不接新区，除非 reopen + 用户确认 |
| `abandoned` | 不要求绑定 |

- 一规划 : 0..N 工作区；一工作区 : 1..N 规划（须标 `primary_plan` 焦点）。
- 多区并行同一 VP 时**推荐** `lead_workspace`；关门提案默认由 lead 侧发起并经用户确认。

### 5.1 `active` VP 零工作区（空转）

`status: active` 且绑定工作区数为 0 时：

1. 编排器**必须告警**，并询问用户：挂接工作区 / 改回 `planned` / 接受有时限的空转。
2. **空转宽限**：自 VP 标为 `active` 或自上次「零区复核」起 **14 个日历日**（以 `updated` 或决策留痕日期较晚者为准）。宽限内可扫描与规划，但**不得**把该 VP 当作已在推进的交付证据。
3. **超过宽限**仍无工作区、且无用户书面「继续空转」记录（须含下一复核日 ≤ 再 14 日）：对该 VP 相关的新建挂接以外的**放行/关门** fail closed，直到挂区、降为 `planned`/`abandoned`，或留下新的有界空转接受。
4. 「长期空转」即指超过上述宽限且无合规留痕。

## 6. 门禁时机（fail closed）

在下列时机，Skills / 编排器 / 适配器应校验对齐链；失败则不得假装推进或关门：

1. 新建工作区或新建 Root  
2. 新建子目标（继承检查）  
3. 推进影响成功边界/非目标的阶段  
4. 目标 close-out 前  
5. Charter **strategic** 修订后：受影响 VP 与挂接工作区须 re-align  

失败模式：缺 `plan_refs` / `primary_plan`、`primary_plan` 不在列表中、VP 文件缺失、`vision_ref` 与 charter 版本不一致、primary 无规划、Charter/VP 使用非法 status。

## 7. 规划关门（轻量）

1. 退出判据方向满足；**证据链接**指向工作区目标的 done / 有界结项路径。  
2. 允许**有界 closed**：residual 必须点名到具体 workspace / goal id。  
3. 无区证据不得将 VP 标为 `closed`。  
4. **禁止**为 VP 建立 Goal 五件套或独立 `03-audit` 台账替代区内审计。

## 8. Charter 修订

| class | 含义 | version | 工作区 |
|-------|------|---------|--------|
| `editorial` | 措辞、链接，不改方向/边界/非目标 | 可补丁级 | 不强制 re-align |
| `strategic` | 目的、边界、非目标、原则优先级 | 至少 minor | impact 所列 VP/区必须 re-align |

流程：更新 charter → 追加 [revisions.md](revisions.md) → 更新 VP `vision_ref` → 刷新工作区声明。

## 9. 引用格式

- 愿景：`{vision_id}@{version}`，例 `vision-goal-governance@0.1.0`
- 规划：`VP-NNN-slug`，路径 `docs/vision/plans/VP-NNN-slug.md`

## 10. 非目标（本契约）

- 双段目标编号、多愿景、pillars、`vision_ref` 的 semver 范围匹配  
- Web UI / CT 专为愿景的写入流程（只读发现与校验即可）  
- 将执行流水或 progress 写入 vision 目录  
