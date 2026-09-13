---
id: D-008
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-008
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-008 · S3 落地：投影标注、legacy 兼容读取与骨架复制修正（2026-09-13）

**状态**：accepted

**触发**：用户已在 [D-005](D-005-s3-consumer-compat.md) 裁决 S3 权威模型 = **A1 索引承载投影**、存量消费仓**必须兼容不得 fail closed**。S1 盘点另发现两处漂移（`docs/architecture/overview.md:70` + 镜像、`workspace-001` Root `00-meta.md:50` 均漏 VP-004）与 `docs/standalone-bootstrap.md` 的**整文件复制**缺陷。本决定记录 S3 的落地形态。

## 决定

1. **投影标注落到表头**：`docs/vision/roadmap.md` 的列名改为 `status（派生投影）`，并在表前写明权威在 **VP frontmatter**、投影「不得用于任何门禁判定」。仅改正文不列表头视为未落地。
2. **写入顺序固定**：关门流程改为「**先**在 VP 文件写关门摘要并改其 frontmatter `status` → **再**刷新本表投影列」，并新增「列的去留」说明（`status` 列可删、`workspace_count` 等自定义列可增删，均不影响完整安装）。
3. **规则落盘为 alignment §0.4**（新节）：投影定义、无列要求、legacy 兼容（不得 fail closed）、兼容读取顺序（**VP frontmatter 优先**）、骨架复制要求。MUST 表 roadmap 行补「**不要求任何特定列**」。
4. **骨架复制修正**：`docs/standalone-bootstrap.md` §2.3 的复制示例**移除** `roadmap.md` 的整文件复制，改为复制 `docs/templates/vision/roadmap.md` 骨架并按本仓 VP 重写；同时新增「不得整文件照搬」与复制后核对要求。
5. **两处漂移改为指针**：`docs/architecture/overview.md` 与 `workspace-001` Root `00-meta.md` 的组合编排摘要不再复写 VP 状态清单，改为指向 `vision/roadmap.md` + `plans/VP-*.md` 并声明权威在各 VP frontmatter。
6. **零新增 MUST**：不新增任何 MUST 文件或列；因此**不存在**「升级即判不完整安装」的路径（对齐 C7）。
7. **实例改写范围**：本轮**不**改 `docs/vision/plans/VP-004`（`closed`）与 `workspace-003` Root 的「纲领路线图」措辞——S2 已使**规则**唯一；实例仅影响先例可读性，登记为 A-005 F-003 的后续项，不阻断本目标。

## 为什么

- 只写正文声明、不改表头列名，AI 与人类读者仍会先看到 `status` 列并按列取值——投影标注必须出现在**取值处**才有效。
- 兼容规则必须写进**规则权威**（alignment）而非只写实例文件，否则消费仓无法据此判断「残留学他仓行不算不完整安装」。
- 骨架复制是缺陷根因：不修示例代码块，则每次冷启动都会重新引入他仓 VP 行，S3 的「重复信息不存在」判据永远不成立。
- 漂移改为指针而不是补全 VP-004：补全会再次产生「同一状态两处维护」，与 A1 模型冲突。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 直接删除 `roadmap.md` 的 `status` 列（A2 模型） | 用户已裁决 A1；且与 `reviews.md` 先例（索引承载投影）不同构 |
| 新增独立 VP 跟踪索引文件（A3 模型） | 新增 MUST 会瞬时冻结存量消费仓（D-005 §2 已排除） |
| 给 `roadmap.md` 增机读 schema 校验 | 现无任何脚本解析该表；先加 schema 会把文档级迁移升级为工具级迁移，超出 S3 需要 |
| 用 fail closed 强制消费仓清理他仓行 | 与用户「必须兼容」裁决直接冲突 |
| 本轮改写 VP-004 / workspace-003 实例措辞 | 属跨区目标记录与已 `closed` 的 VP；规则已唯一，实例整理留后续并已登记 |

## 影响

- canonical：`docs/vision/roadmap.md`、`docs/vision/alignment.md` §0.2/§0.4、`docs/architecture/overview.md`（stage 白名单 → 镜像）、`docs/standalone-bootstrap.md`、`docs/vision/README.md`。
- 测试与 fixture：`docs/tests/test_vision_protocol.py` 新增 `CompositionRoadmapAuthorityTests`（6 项）；`docs/tests/fixtures/vision/valid-stack/roadmap.md` 由 3 列升为带投影标注的 6 列。
- 工作区实例：`workspace-001` Root `00-meta.md`（漂移修正）。
- 不触发 `vision_ref` / Charter 变更；不产生 VRev（本轮为 editorial 级文档与规则细化，不改方向/边界/非目标）。
