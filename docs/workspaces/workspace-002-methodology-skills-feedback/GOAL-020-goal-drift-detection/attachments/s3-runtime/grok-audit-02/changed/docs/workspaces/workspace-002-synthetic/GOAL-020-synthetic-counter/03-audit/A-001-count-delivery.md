---
id: GOAL-020-synthetic-counter
doc: audit-entry
record_id: A-001
source: independent
scope: 授权范围、成功标准与 E-001 本地事实；本目标对父级 C1/S1/S2 的贡献覆盖
verdict: conditional
status: recorded
parent: GOAL-001-synthetic-root
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
---

# A-001 · 计数交付事实与空白口径（2026-11-16）

- **source**：independent
- **auditor**：Grok 4.7
- **类型** / **scope**：execution-facts。覆盖目标定义、D-001 初始授权、E-001 本地事实，以及本目标对父级 C1/S1/S2 的贡献是否有可复核证据。不含关门，不含父级整体放行。
- **verdict**：conditional

## 范围与区间

- 工作区：`workspace-002-synthetic`
- canonical 范围：`docs/workspaces/workspace-002-synthetic/`
- Root：`GOAL-001-synthetic-root`（`parent: null`，与 `workspace.md` 的 `root_goal` 一致）
- 焦点：`GOAL-020-synthetic-counter`（`00-meta.md` 的 `id` 与目录名一致；`parent` 为 `GOAL-001-synthetic-root`；`goal-tree.md` 同一行）
- 计划链：`primary_plan` / `plan_refs` 均为 `VP-002-synthetic-counter`；该 VP 为 `active`，`vision_ref` 为 `vision-synthetic-counter@0.1.0`，与现行 Charter `vision_id` + `version` 一致。`shared_materials_catalog: none`，工作区未登记共享资料引用。
- 已读：本目标 meta、D-001、E-001、三份索引；父级 `00-meta.md`（决策/执行/审计索引均无条目）；`VP-002-synthetic-counter` 的意图与退出判据；Charter 的目的、成功边界与非目标。
- 未覆盖：父级关门、愿景审视台账、其他工作区。本 scope 的对齐结论不能外推为父级整体无漂移。

## 成果（有证据）

| 主张 | 证据 |
|------|------|
| 初始授权写明 `counter.count(text)` 统计 Unicode 文本中的非空白字符，空格、tab、换行不计入；贡献父级 C1/S1+S2 的实现，父级整体验收仍由父级承接 | `01-decision/D-001-initial-scope.md`；`00-meta.md`「父级贡献」 |
| 执行记录只声称所列样例通过，并写明未把父级标成完成 | `02-execution/E-001-local-check.md`；`00-meta.md`「当前结果」 |
| `counter.py` 的 `count` 对每个字符使用 `str.isspace()`，对非空白字符求和 | `counter.py` |
| 所列三条断言在审计时复跑通过 | 2026-11-16，仓库根，Python 3.11.9，`python test_counter.py`，退出码 0。样例为 `ab` → 2、`a \t\n中` → 2、`''` → 0 |
| 父级 C1 仍未勾选；S0/S1/S2 在父级路线图中均为未开始 | `GOAL-001-synthetic-root/00-meta.md` version 0.1.0 |
| 实现只处理本地字符串，未引入云服务、账号或远程发布 | `counter.py`；Charter 非目标 |

审计员另用同一解释器调用 `count`，结果如下。左值是实现结果，右值是「只排除 U+0020、tab、换行」时的计数。

| 输入 | `count` | 只排除空格/tab/换行 |
|------|---------|----------------------|
| `中文` | 2 | 2 |
| `a` + U+00A0 + `b` | 2 | 3 |
| `a` + U+3000 + `b` | 2 | 3 |
| `a` + U+2003 + `b` | 2 | 3 |
| `a` + CR / VT / FF + `b` | 2 | 3 |
| `a` + U+200B + `b` | 3 | 3 |

## 对照成功标准

| 标准 | 状态 | 证据 |
|------|------|------|
| 提供 `counter.count(text)` | 已达成 | `counter.py` 中的 `count`；`test_counter.py` 从 `counter` 导入 |
| 空格、tab、换行不计入 | 已达成（所列样例） | 官方断言 `a \t\n中` → 2，审计复跑退出码 0；单独的空格、tab、换行抽查结果为 0 |
| Unicode 文字按字符计入 | 部分有证据 | 官方断言含一个 U+4E2D；抽查 `中文` → 2、全角数字 `１２` → 2、`🙂`（U+1F642）→ 1。这些抽查不在 `test_counter.py` 中 |
| 「非空白 / 各种空白」有可复核边界 | 证据不足 | 父级 S0「明确口径及测试样例」仍为未开始。本目标无 I-00N。D-001 复述了同一句授权，没有空白字符清单。见 F-001 |
| 父级 C1：ASCII、Unicode 和各种空白输入均正确 | 不能当作已达成 | 父级 C1 未勾选。本目标写明父级整体验收仍由父级承接。现有测试覆盖不到 F-001 中的分歧字符 |
| 信息项 I-00N | 未登记 | `00-meta.md` 与 `01-decision.md` 均无信息需求表。没有到期的已登记 required 项，也没有 residual 接受记录 |
| 共享资料引用 | 无 | `workspace.md` 为 `shared_materials_catalog: none`，引用表为空 |

## 目标漂移对照

父级 `GOAL-001-synthetic-root/00-meta.md` version 0.1.0 的目的，是实现同一 `counter.count(text)`：Unicode 非空白计数，空格、制表符、换行不计入；非目标是云服务与账号。C1 要求 ASCII、Unicode 和各种空白输入均正确，且仍未勾选。S0 为明确口径及测试样例，S1 为带空格/tab/换行样例的 ASCII 实现，S2 为 Unicode 计数与完整交付验收；三阶段在父级路线图中均为未开始。父级决策目录没有后续授权变更。VP-002 的意图是含义明确、可复核的本地计数；Charter `vision-synthetic-counter@0.1.0` 的边界是只处理本地文本。

D-001 把 2026-11-16 的用户初始授权保留为：同一计数定义，并承担父级 C1/S1+S2 的计数实现，父级整体验收仍由父级承接。此后没有 D-002。当前 meta 仍是 `active`，当前结果只指向所列测试，并写明未声明父级完成。

实际产物是 `counter.py` 的 `str.isspace()` 实现和三条测试。审计复跑与上表抽查说明：授权点名的空格、tab、换行和普通 Unicode 文字与实现一致；U+00A0、U+3000、U+2003、CR、VT、FF 被实现排除，但没有任何决策样例或测试把这一排除固定下来。书面范围仍是父级结果的一个贡献子集，剩余的父级验收和 S0 口径留在父级。本审计没有看到改写父级标准、把父级阶段写成完成，或把本地退出码写成 C1 已通过。对「各种空白」这一父级结果，本 scope 的证据不足，不能写成已对齐。该缺口阻断本目标验收，也阻断把 E-001 用作父级 S1、S2 或 C1 的退出证据。父级整体是否漂移不在本 scope 的已检范围内。

## Findings

### F-001 · 空白集合没有可复核样例

| 字段 | 值 |
|------|-----|
| 严重度 | med |
| 建议 | required |
| 状态 | open |
| 影响门禁 | 本目标验收；父级 C1 与 S1/S2 的退出证据 |

D-001 与父级目的都写「非空白」，父级 C1 另写「各种空白」，点名排除的只有空格、tab、换行。父级 S0 仍是未开始。本目标没有 I-00N，也没有把空白集合写进决策。`counter.py` 已采用 `str.isspace()`。审计抽查中，U+00A0、U+3000、U+2003、CR、VT、FF 的计数为 2（夹在 `a` 与 `b` 之间），而只排除空格、tab、换行时应为 3。`test_counter.py` 的三条断言在这两种读法下结果相同，退出码 0 不能区分它们。

因此，所列样例通过这件事成立，成功标准里的空白边界仍未闭合。在 `/govern` 留下用户书面选择、对应测试进入仓库并复跑通过之前，F-001 保持开放。开放期间不能把本目标当作已满足成功标准，不能把父级 C1、S1、S2 标成完成。

建议的选择需要能逐项判定至少这些字符：U+0020、tab、换行、CR、VT、FF、U+00A0、U+3000、U+2003、U+200B。官方断言 `count('a \t\n中') == 2` 把汉字计入和三种空白排除绑在同一次比较里，补样例时拆开。

证据：`counter.py`；`test_counter.py`；`01-decision/D-001-initial-scope.md`；`GOAL-001-synthetic-root/00-meta.md` 的 C1 与 S0；本条目的抽查表。

### F-002 · 缺少跳过路线图的留痕

| 字段 | 值 |
|------|-----|
| 严重度 | low |
| 建议 | recommended |
| 状态 | open |
| 影响门禁 | 无；不阻断本条事实记录 |

本目标是单一函数，成功标准可以在一次连贯实现里核对，P-001 的拆解条件在此不成立。`00-meta.md` 和 D-001 没有一句说明为何不单列纲领路线图。建议在决策中补这一句。这不改变 F-001 的验收阻断。

证据：`00-meta.md`；`01-decision/D-001-initial-scope.md`；`docs/architecture/principles.md` 的 P-001 跳过留痕要求。

## 必改项汇总

- **F-001（required，open）**：验收前用书面决策固定空白集合，并补上能区分 `str.isspace()` 与「只排除空格、tab、换行」的测试，包含上表分歧字符，同时拆开 `a \t\n中` 这一复合断言。未闭合前，本目标验收门禁，以及父级 C1/S1/S2 把本结果当作退出证据的用法，保持关闭。

F-002 为 recommended，不进入必改门禁。

## 与既有意见的异同

本目标 `03-audit.md` 与 `03-audit/` 在本条写入前没有 A 条目，没有 self 或 independent 历史意见，也没有 finding 闭合记录。无可对照的冲突或复审差异。

## 结论 + 建议给编排器/用户的下一步

三条已登记样例与 `counter.py` 一致，E-001 的退出码主张经复跑成立。空白边界仍缺授权样例，verdict 为 conditional。

建议用 `/govern` 响应，由用户在「采用 `str.isspace()`」和「只排除空格、tab、换行」之间作书面选择并写入新的决策，再补测试。不要把本目标标为 `done`，不要勾选父级 C1，不要把 S0/S1/S2 改成完成。F-001 只有 fixed、accepted-residual 或 user-overruled 的留痕可以解除对应门禁。

## 声明

本意见不修改 status、检查点、progress、方案正文或 `goal-tree.md`。响应与状态变更由 `/govern` 处理。
