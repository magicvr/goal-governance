---
id: D-004
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-004
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-004 · I-001～I-004 盘点验收与 A-001 F-002 闭合（2026-09-13）

**状态**：accepted

**触发**：S1 只读盘点完成。四路盘点（I-001 双层语义命名、I-002 愿景跟踪权威、I-003 消费仓写入面、I-004 `/commit` 入口）均产出可复核的证据路径；需按 P-005 逐项判定信息项状态，并判定 A-001 F-002 是否具备合法闭合条件。

## 决定

### 1. 信息项逐项验收

| 信息项 | 结论（要回答的问题已被证据回答） | 状态 | 关键证据 |
|--------|----------------------------------|------|----------|
| I-001 | **不足以阻止三类混淆**。命名表存在三处但只覆盖 4～5 类工件，**无「子目标」行、无「VP 内阶段结构」行**；`总路线图` 在 canonical **零出现**；消费端安装的规则面（`skills/install/claude/AGENTS.md` §6e、`skills/AGENTS.template.md` §6e、copilot 说明）**完全没有**命名消歧表；目标与愿景模板无对应槽位；机器层只校验 `roadmap.md` 存在；in-repo 先例（VP-004 与 Root 同名同标签路线图）正在示范被投诉的混淆 | **verified** | 附件 §2.A；[E-003](../02-execution/E-003-s1-inventory.md) |
| I-002 | **愿景总路线图 = `docs/vision/roadmap.md`**（canonical 从不使用「总路线图」一词）；其 7 列中有 4 列与各 VP frontmatter 逐字段重复（当前 4/4 一致，故可无损收敛）；**无任何脚本/测试/契约解析该表**（只有 `is_file()` 存在性检查）；两处已有漂移（`docs/architecture/overview.md:70` 与其镜像、`GOAL-001-main-vision/00-meta.md:50` 均漏 VP-004）；`docs/standalone-bootstrap.md` 整文件复制该表，把生产仓 VP 行带进消费仓；`docs/templates/vision/` **没有 roadmap 模板** | **verified** | 附件 §2.B；[D-005](D-005-s3-consumer-compat.md) |
| I-003 | 写入面、覆盖策略、硬/软冲突面、完整安装 MUST 覆盖差距、共存候选 A～E 与 13 条负例候选均已可核对；**但共存模型属用户裁决项，盘点不能替代选型** | **partially-verified**（写入面/冲突面/负例=verified；**选型仍 open**，S4 方案冻结前须用户裁决） | 附件 §2.C |
| I-004 | `/commit` 现状盘点完成：**仅存在于 monorepo 自用 `.github/prompts/commit.prompt.md`，任何安装面都不产出它（未实现）**；宿主覆盖可核对集合 = 三契约宿主；checkpoint 契约已覆盖部分负例，`/commit` 侧仍有 8 类未规定（非 Git、验证范围、hook、禁用语义、detached HEAD/rebase、CRLF、push、以 commit 作放行依据）；契约层缺「默认安装但不入必达集」的表达位 | **verified** | 附件 §2.D |

`I-004` 的治理边界早已由 [D-002 §4](D-002-a001-response.md) 冻结（便利可选、非 MUST、非必达、非 checkpoint 替代）；本轮补齐的是命令形状素材与负例清单。

### 2. A-001 F-002 闭合判定

| 要求字段（A-001 原文 / D-002 §2） | 本轮产物 | 是否可核对 |
|-----------------------------------|----------|------------|
| 可复现路径 | 每条主张均带 `file:line`；附件 §2 证据列 | 是 |
| 责任边界证据 | 附件 §2.C 写入面表（目标路径 / 写入方 / 覆盖策略） | 是 |
| 验收人 / 审视方式 | 附件 §3 逐阶段列「验收人 / 审视方式」 | 是 |
| 各阶段证据路径 | 附件 §3 每阶段的证据落点 | 是 |
| probe / corpus、正反例、通过阈值 | 附件 §4：10 个 case + 判定键 + 阈值 | 是 |
| 权威落点核验 | 附件 §2.B 现状核验；S3 后核验判据见附件 §3 S3 行 | 是 |
| 负例测试 | 附件 §3 S4/S5 行 + 候选清单 | 是（实现留待 S4/S5） |

**判定：A-001/F-002 `fixed`。** 闭合依据 = [附件 S1 验收矩阵](../attachments/s1-acceptance-matrix.md) + [D-003](D-003-s1-freeze-shared-invariants.md) + 本决定。矩阵的**执行**（跑 probe、落地谓词）属于 S2 实施，不属于 F-002 的载体要求；F-002 阻断的「S2/S3/S4 方案冻结与放行」在各自阶段仍受 I-005 provider 门禁与本目标路线图约束。

### 3. 判定为不闭合的项

- **A-001/F-005**：保持 `open`。I-006 仍缺版本、tag/revision、资产清单与证据归属基线（S6 前冻结）。
- **I-003 选型**：保持 `open`（required，阻断 S4 方案冻结）。
- **A-003 F-006 / F-007**：`recommended`，本轮分别在 D-003 §3 与附件 §4（成对正反例）中响应。

## 为什么

- P-005 要求「信息项由证据关闭」：I-001/I-002/I-004 的问题「是什么 / 缺口在哪」已被逐条证据回答，可以 verified；I-003 的问题包含「选哪个模型」，用户尚未裁决，故只能部分关闭，不得写成 verified。
- F-002 要的是**载体**而非**执行结果**：矩阵、corpus、阈值、责任人与证据路径都已落盘可核对，故可闭合；若等到 S2 实施才闭合，就会把「S2 的输出」当成「允许开始 S2 的条件」，形成循环。
- 不把 F-005 顺势标成 fixed：S6 的版本与资产基线确实还没有，标记闭合属于伪装完成。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| I-003 整体标 verified | 选型未裁决；把候选写成已选方案即编造事实 |
| I-003 整体保持 open 且不问用户 | 盘点部分已可核对；无限期挂起会让 S4 无谓延后 |
| 把 F-002 与 F-003 一起标 fixed | F-003 的闭合依据是 owned paths 与串行判定，见 D-006；分开留痕便于独立审计逐条核对 |
| 让 S1 的独立复审替代 F-002 闭合 | 独立审计只出意见；闭合必须由编排器带证据响应（P-003） |

## 影响

- I-001/I-002/I-004 → `verified`；I-003 → `partially-verified`（选型 open）；I-005 → `closed`（provider 已指定）；I-006 保持 `open`。
- A-001 开放 required 从 3 降为 **1**（仅 F-005）。
- 00-meta 信息表、`01-decision.md` 索引、`03-audit.md` 结论段随之更新。
