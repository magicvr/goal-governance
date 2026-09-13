---
id: GOAL-008-consumer-layer-split-and-hosting
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.6.0
---

# 决策记录 · GOAL-008

## 信息需求与阶段门禁

> 本文件是稳定索引。信息台账与 [00-meta.md](00-meta.md) 同源；长决策写在 `01-decision/D-NNN-<slug>.md`。`accepted-residual` 必须指向用户书面决策或审计响应，且不等同于 `verified`。

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 决策 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 双层路线图命名与判定缺口 | S1 / S2 方案冻结 | S2 前 | 盘点 P-006 / alignment / prompts / 模板 + 最小反例 | **verified** | — | D-004：命名表缺「子目标」「VP 内阶段结构」；`总路线图` canonical 零出现；消费端规则面无消歧表；证据 `attachments/s1-inventory-evidence.md` §2.A |
| I-002 | required | 愿景总路线图与 VP 跟踪的权威落点 | S1 / S3 方案冻结 | S3 前 | 对照 roadmap.md、VP 正文、alignment 工件表 | **verified** | — | D-004/D-005：roadmap.md 4 列与 VP frontmatter 重复且 4/4 一致；无脚本解析；模型 = A1 索引承载投影；证据 §2.B |
| I-003 | required | 消费仓 `AGENTS.md` / `docs/` 共存模型 | S1 / S4 方案冻结 | S4 前 | 盘点 install / updater / 完整安装 MUST | **partially-verified** | 选型待用户裁决；S4 方案冻结前未决即阻断 | D-004：写入面/冲突面/13 条负例已核实；候选 A～E 未选优；证据 §2.C |
| I-004 | required | `/commit` 命令形状、宿主覆盖与 fail-closed 负例（治理边界已由 D-002 冻结） | S1 / S5 方案冻结 | S5 前 | 对照 checkpoint 契约、VP-004 入口面与现有 prompt | **verified** | — | D-004：现仅 monorepo 自用 prompt，安装面未实现；契约缺「默认安装不入必达」表达位；证据 §2.D |
| I-005 | required | cross 审计 independent provider | S2 实施 | S2 实施前 | 用户书面指定；失败不降级 | **closed** | provider 失效时回到门禁 | 用户 2026-09-13 指定本地 grok build（`grok` 1.0.30 / grok-4.6 / `--reasoning-effort high`）；E-003 |
| I-006 | required | 发布版本、tag/revision、资产清单、回归矩阵、cross 覆盖、consumer/producer 证据归属 | S6 发布 | S6 前 | 对齐当前版本源与远端基线 | open | 基线前移时重算 | F-005 绑定；待冻结 |

I-001～I-006 不阻断目标设立；未经验证不得把候选机制写成已选方案。
**2026-09-13 S1 结果**：I-001/I-002/I-004 `verified`、I-005 `closed`、I-003 `partially-verified`（选型待裁决）、I-006 仍 `open`（S6 前冻结）。

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-09-13 | 将四项消费仓痛点纳入同一 R3 大目标，并采用 S1 先行路线图 | accepted | `01-decision/D-001-scope-and-roadmap.md` |
| D-002 | 2026-09-13 | 响应 A-001：唯一化闸门、并行写集与 `/commit` 边界 | accepted | `01-decision/D-002-a001-response.md` |
| D-003 | 2026-09-13 | S1 契约冻结：共享不变量 C1～C7 与待冻结细案 | accepted | `01-decision/D-003-s1-freeze-shared-invariants.md` |
| D-004 | 2026-09-13 | I-001～I-004 盘点验收与 A-001 F-002 闭合 | accepted | `01-decision/D-004-s1-inventory-acceptance.md` |
| D-005 | 2026-09-13 | S3 权威模型（A1）与消费仓兼容裁决 | accepted | `01-decision/D-005-s3-consumer-compat.md` |
| D-006 | 2026-09-13 | S4/S5 owned paths 与串行调度判定 | accepted | `01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md` |
| D-007 | 2026-09-13 | S2 层级语义冻结：命名表补全为 6 类 + 落位谓词 8 条 | accepted | `01-decision/D-007-s2-layer-semantics-freeze.md` |
| D-008 | 2026-09-13 | S3 落地：投影标注、legacy 兼容读取与骨架复制修正 | accepted | `01-decision/D-008-s3-projection-and-legacy-compat.md` |
| D-009 | 2026-09-13 | S4 共存模型裁决：AGENTS.md 受管标记块（模型 A） | accepted | `01-decision/D-009-s4-agents-coexistence.md` |
