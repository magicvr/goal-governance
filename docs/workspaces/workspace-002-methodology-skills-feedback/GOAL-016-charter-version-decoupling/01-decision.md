---
id: GOAL-016-charter-version-decoupling
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

# 决策记录 · GOAL-016

## 纲领路线图与阶段计划（按需）

纲领路线图（P-001）写在 [00-meta.md](00-meta.md#纲领路线图p-001)，此处不重复。阶段方案与冻结契约落在 `01-decision/D-NNN-<slug>.md`（非树节点，不建第二套状态源）。

| 阶段 | 计划文件 / 落点 | 说明 |
|------|-----------------|------|
| S1 | [D-001](01-decision/D-001-scope-and-roadmap.md)、[D-002](01-decision/D-002-adjudication.md) | 范围/路线图 + 用户裁决冻结方案与写集（完成） |
| S2 | D-002 §写集 | 按冻结方案同步 canonical 协议与文档（完成） |
| S3 | D-002 §实现与测试 | validator、fixtures、回归、模板/Skills 与镜像（完成） |
| S4 | `03-audit/` | cross 审计（self + codex independent）与意见响应（完成） |
| S5 | [D-003](01-decision/D-003-release-v0-13-8.md) | 版本清单、运行证据、发布与资产验收（进行中） |

## 信息需求与阶段门禁

台账见 [00-meta.md](00-meta.md#信息就绪与未知项)。I-001～I-005 均已于 2026-10-26/27 置 `verified`（I-005 为用户书面 attestation + A-008 `user-overruled`；API 仅 `skipped`，见 [A-008](03-audit/A-008-response-a-007.md)）；S1～S4 已退出，S5 发布与资产验收完成，待用户关门确认。

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-10-26 | 立项范围、路线图与审计/变更流程 | accepted | `01-decision/D-001-scope-and-roadmap.md` |
| D-002 | 2026-10-26 | 方案、primary 语义、历史 VP 校验与版本号冻结 | accepted | `01-decision/D-002-adjudication.md` |
| D-003 | 2026-10-26 | S5 发布 v0.13.8：范围、证据与审批边界 | accepted | `01-decision/D-003-release-v0-13-8.md` |
| D-004 | 2026-10-27 | GOAL-016 关门决定（done / 100%） | accepted | `01-decision/D-004-close-out.md` |

> 编号在本目标内单调不复用；用户答复前不写 D-002 的结论，不把待答写成决策。
