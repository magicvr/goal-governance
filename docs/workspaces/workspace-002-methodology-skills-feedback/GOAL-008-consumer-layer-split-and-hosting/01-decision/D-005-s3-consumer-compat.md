---
id: D-005
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-005
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-005 · S3 权威模型与消费仓兼容裁决（2026-09-13）

**状态**：accepted

**触发**：I-002 盘点发现 `docs/vision/roadmap.md` 的 `status` / `vision_ref` / `title` / `workspace_count` 与各 VP frontmatter 逐字段重复且当前 4/4 一致，但 **canonical 从未规定谁是权威**；同时 `docs/standalone-bootstrap.md` 以**整文件复制**方式把生产仓 `roadmap.md`（含 VP-001～VP-004 行）带进消费仓。这两点都属 P-004 的用户裁决项，由用户本轮书面裁决。

## 决定

1. **权威模型 = A1「索引承载投影」**（用户本轮选定）：
   - **状态与跟踪权威**：各 `{governance_root}/vision/plans/VP-*.md` 的 frontmatter（`status`、`vision_ref`、`lead_workspace`）。
   - **`roadmap.md` 保留 `status` 列，但必须显式标注为「派生投影」**，且**不得用于任何门禁判定**、不得作为 VP 状态的第二权威。
   - 该形状与既有先例一致：[alignment.md:217](../../../../vision/alignment.md)「`reviews.md` 保留 frontmatter、使用约定、当前 `open required` 投影与条目链接，不内联新 VRev 正文」+「索引与报告**共同**构成唯一正式台账」。
   - **不采用** B（roadmap 完全去掉 status）与 C（另开独立跟踪文件）。
2. **存量消费仓必须兼容，不得因本次解耦 fail closed**（用户本轮选定）：
   - 遗留列/遗留行只能作 **legacy 提示**，不得用于门禁、不得阻断推进、不得单独判「不完整安装」。
   - 兼容读取顺序：**VP frontmatter 优先**；`roadmap.md` 残留单元仅在 VP 文件缺失时作提示，且不得据此宣告 VP 状态。
   - 若 S3 新增任何文件（例如 roadmap 模板或索引辅助件），一律按 **non-MUST / recommended** 处理；把新增文件升为 MUST 属**改边界**，须回到用户并留痕。
3. **`docs/standalone-bootstrap.md` 的整文件复制缺陷在 S3 内修正**（scoped fix）：消费仓 bootstrap 不得把生产仓的 VP 行带入本地组合编排；修法（改为模板复制 / 占位生成 / 复制后清理）在 S3 方案冻结时确定，并须给出对**已按旧版安装**的仓的兼容读法。
4. **两处既有漂移事实**在 S3 内处理：`docs/architecture/overview.md:70`（及其镜像 `skills/core/docs/architecture/overview.md`）与 `docs/workspaces/workspace-001-goal-governance/GOAL-001-main-vision/00-meta.md:50` 的组合编排摘要**均漏 VP-004**。前者在 stage 白名单内，改后必须同轮 stage（C6）。
5. **解耦后 VRev 审计口径同步**：`docs/vision/reviews/VRev-003/004/007` 曾以「roadmap 与 VP 文件一致」作为一致性证据；S3 须在 alignment 或 vision README 明确新口径（投影列不作门禁证据），避免后续独立愿景审视按旧口径报「索引不含 status」。

## 为什么

- **A1 优于 A2/B**：与 `reviews.md` 的既有工程形状同构（稳定索引 + 分片正文、索引承载投影），因此不引入第二套心智模型；消费仓改动最小，FB-007 的诉求（跟踪信息淹没路线图）可通过「列瘦身 + 明标投影 + 波次区去状态叙述」达成，无需删除索引上的可读状态。
- **A1 优于 C**：C 要新增 MUST 行，而 [alignment.md:30](../../../../vision/alignment.md)「缺任一 MUST 行 = **不完整安装**」+ [:169](../../../../vision/alignment.md) 门禁时机 1 会让**所有存量消费仓在升级瞬间被冻结治理推进**——这正是 D-005 §2 要避免的。
- **两类风险必须分开处置**：数据风险≈0（两套记录逐字段一致，可无损收敛）；真正的风险在消费侧（整文件复制 + 新增 MUST 的连锁），所以先裁决兼容口径，再让 S3 设计迁移。
- 用户同时选定「必须兼容」，因此 S3 的验收里「重复信息不存在」是**本仓**要求，对消费仓是**宽松兼容**要求（见附件矩阵 S3 行）。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| A2：roadmap 删除 status 列，VP 单一权威 | 与 `reviews.md` 先例语义不同（先例是索引仍承载投影），且需同步改 VRev 审计口径；收益不抵一致性成本 |
| A3：另开独立 VP 跟踪索引文件 | 新增文件入 MUST 会瞬时冻结所有存量消费仓；定为非 MUST 又要额外维护回退分支 |
| 允许 fail closed 强制对齐 | 会阻断由 `standalone-bootstrap` 整文件复制产生的存量仓；用户明确选择兼容 |
| 在 S1 直接改 `roadmap.md` 与 alignment | S1 只盘点；改协议正文属 S3，且 alignment/principles 属 stage 白名单，必须与实现同轮提交 |
| 把 `workspace_count` 等无定义列一并写入方案 | 该列在 canonical 无任何定义句，属实现细节；在 S3 方案冻结时决定去留 |

## 影响

- S3 的成功判据变为：投影列显式标注且无门禁用途；VP frontmatter 为唯一权威；遗留行/列有兼容读法；两处漂移修正；bootstrap 复制缺陷收口。
- `docs/vision/alignment.md`、`docs/architecture/principles.md`、`docs/templates/**` 若在 S3 被改动，须按 C6 同轮 stage 并提交镜像。
- I-002 保持 `verified`（信息已获得）；S3 的方案冻结以本决定为前提。
