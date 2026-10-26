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

台账见 [00-meta.md](00-meta.md#信息就绪与未知项)。I-001～I-004 已于 2026-10-26 置 `verified`（[D-002](01-decision/D-002-adjudication.md)）；I-005 为 S5 发布审批，保持 `open`。S1 已退出，S2 进行中。

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-10-26 | 立项范围、路线图与审计/变更流程 | accepted | `01-decision/D-001-scope-and-roadmap.md` |
| D-002 | 2026-10-26 | 方案、primary 语义、历史 VP 校验与版本号冻结 | accepted | `01-decision/D-002-adjudication.md` |
| D-003 | 2026-10-26 | S5 发布 v0.13.8：范围、证据与审批边界 | accepted | `01-decision/D-003-release-v0-13-8.md` |

> 编号在本目标内单调不复用；用户答复前不写 D-002 的结论，不把待答写成决策。
