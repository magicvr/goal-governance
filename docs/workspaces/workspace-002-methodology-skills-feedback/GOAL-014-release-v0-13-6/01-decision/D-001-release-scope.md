---
id: D-001
goal: GOAL-014-release-v0-13-6
doc: decision
title: v0.13.6 发布范围、证据策略与 provider 门禁
status: accepted
parent: GOAL-014-release-v0-13-6
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# D-001 · v0.13.6 发布范围与证据策略

## 决定

1. **版本与范围**：远端最新正式版为 `v0.13.5`，`v0.13.6` 未被占用。本轮发布下一个兼容性 patch **`v0.13.6`**，把 GOAL-013（自动审计派发白名单与缺答阻塞门禁）的已关门源码改进送进正式 Release。协议保持 `protocol 0.1.0`，consumer contract 数据结构、MUST 门禁与 File/MCP 渠道边界不变；**不**覆盖旧 Release，**不**移动既有 tag。
2. **承载方式**：GOAL-013 已按 [D-005](../GOAL-013-audit-dispatch-and-user-input-gates/01-decision/D-005-close-out.md) 关门且明确不含发布，因此发布另立本目标 GOAL-014 承载 PR、CI、main merge、annotated tag、gated Release 与真实资产验收。GOAL-013 的源码范围不重开；若发布过程发现源码缺陷，回到对应目标或按 P-004 裁决，不在发布目标内静默改验收口径。
3. **证据策略**：复用 GOAL-013 S3 在 2026-10-17 为当前工作树捕获的 `docs/releases/runtime/goal-013-s3-2026-10-17-current`（16 份，含 12 格宿主入口 + 4 份工作流/MCP L3）。**保持原捕获日期、原路径、原 JSON 与原始输出不变**；只把矩阵 `candidateRevision` 改为 `v0.13.6` 并在 `evidenceScope` 说明该批次现在作为 v0.13.6 候选基线。不复制改名，不伪造 v0.13.6 新采集。
   - 门禁前置：`capture_runtime_evidence.py --check` 与 `compatibility_report.py` 必须在清单变更前后都通过；出现 stale behavior source 或 protocol 变化时先处理，不静默放行。
   - 行为源核查：本批证据的 `behaviorSources` 只覆盖 `docs/architecture/{principles,workspace-protocol}.md`、`docs/vision/alignment.md`、`mcp/*.py`、`skills/AGENTS.template.md`、`skills/install/**`、`skills/prompts/**` 与 GOAL-013 的 catalog fixture；版本 pin（README/CHANGELOG）与矩阵本身不在其中，因此清单变更不使运行证据过期——该判断由实际 `--check` 结果确认，不靠推断。
4. **审计与 provider**：scope 属 release / compatibility 高影响门禁 → 审计模式 **independent**，至少一个独立 provider 意见，主代理不冒充。用户尚未在本会话指定 provider（I-003 `collecting`），按 P-004 询问用户后留痕；provider 失败时门禁保持未满足，**不**静默降级为 self，也不由编排器代填。
5. **发布顺序**：S1 基线冻结 → S2 清单/预演/独立审计（无开放 required）→ S3 PR 双平台 CI 全绿后合入 main、在 merge 上打 annotated tag、gated workflow 完成发布 → S4 下载真实资产逐项验收并关门。CI 未全绿不得合并；strict release 预检未过不得推 tag。
6. **人类审批边界**：Environment `release` 的放行由 magicvr 人工给出；AI 不代批、不改 Environment 配置、不代签审批。若审批结果为 skip/拒绝，如实记录，不写成 approved。

## 未选方案与风险边界

| 方案 | 未选原因 / 当前约束 |
|------|---------------------|
| 用 minor 或 major 版本号 | 无协议、consumer contract 数据结构或 MUST 变化，按既有惯例取下一个 patch |
| 重捕获 v0.13.6 新运行证据 | 现行 2026-10-17 captures 即当前工作树来源且 `--check` 通过，重捕获会制造无来源的新主张 |
| 把发布并入 GOAL-013 | GOAL-013 已关门且 D-005 明确不含发布；并入会重开已结项范围 |
| 由编排器自选 independent provider | 违反 P-004：provider 未指定时询问用户，不得自选或冒充 |
| 先 tag 再补资产核对 | tag 固定发行身份；未经验收就宣称已发布属于过度主张 |

当前 maxima：`progress` 只作派生展示；S1 完成不等于已冻结清单，S2～S4 未开始。本记录不预写尚未发生的 CI、merge、tag、审批或资产结果。
