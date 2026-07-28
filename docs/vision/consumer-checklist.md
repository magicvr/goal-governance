---
doc_type: vision-consumer-checklist
title: 愿景体系消费方检查清单
status: active
created: 2026-07-28
updated: 2026-07-28
version: 0.2.0
---

# 消费方检查清单

> 政策以 [alignment.md](alignment.md) 与 **P-006** 为准。本清单只做操作映射；变更规则时先改 alignment，再同步本页。

## A. 仓库发现与完整安装

- [ ] 存在 `docs/vision/README.md` 与 `docs/vision/charter.md`
- [ ] 存在 `docs/vision/roadmap.md`、`revisions.md`、`reviews.md`、`workspaces.md`、`alignment.md`、`consumer-checklist.md`
- [ ] 至少存在一个 `docs/vision/plans/VP-*.md`（冷启动在开区前必须落盘首个 VP）
- [ ] Charter：`doc_type: vision-charter`，`vision_id`、`version` 有值，`status` ∈ {`active`,`superseded`}（**不是** `done`）
- [ ] **至多一个** `status: active` 的 Charter（单愿景）
- [ ] 缺 Charter → 报告**不完整安装**；仅引导补齐，不非引导开区/推进/放行/关门

## B. 当前工作区

- [ ] 已定位焦点 `workspace.md`（多区未指定则 fail closed）
- [ ] 存在 `vision_role`、**必填** `plan_refs`、**必填** `primary_plan`（含 sandbox；**无 opt-out**）
- [ ] `primary_plan` ∈ `plan_refs`（逗号分隔列表）
- [ ] `primary_plan` 对应文件 `docs/vision/plans/<primary_plan>.md` 存在
- [ ] Root `00-meta` 的 plan 字段与 workspace 一致（或可解释的同步中状态）

## C. VP 链

- [ ] VP `status` ∈ {`planned`,`active`,`closed`,`abandoned`}
- [ ] VP `vision_ref` 等于 `{charter.vision_id}@{charter.version}`（精确匹配）
- [ ] 若 VP `active` 且绑定工作区为 0：告警或询问，不静默当作健康推进
- [ ] 多区绑定同一 VP 时 **`lead_workspace` 必填**

## D. 门禁动作

- [ ] 新建区/Root/关键推进/关门前跑完 A–C
- [ ] Charter strategic 修订后：Vision Review + VP/区 re-align；未完成前**宽阻断**
- [ ] 相关 Vision Review 的 required 已按三路径闭合（或尚无阻断本动作的开放项）
- [ ] 不把 vision 目录内容当作 progress 或 Goal finding 关闭证据
- [ ] Primary 声明（workspace / workspaces.md / charter.primary_workspace）无互相矛盾；若矛盾已 fail closed 并待用户裁决
- [ ] `active` VP 若零工作区：已告警；未超 14 日空转宽限，或已有继续空转书面留痕
- [ ] VP 关门要求区证据链接；多区由 lead 发起 + 用户确认；有界 residual 已点名

## E. 编排器读序（最小）

1. **完整安装？** 无 active Charter → 不完整；仅引导 Charter→VP  
2. 读 charter 版本与 alignment 要点（单愿景、无 opt-out、宽阻断）  
3. 定位并校验当前 `workspace.md`（含**必填** plan 字段）  
4. 解析 `primary_plan` → 读对应 VP；检查 `reviews.md` 开放 required（若影响本动作）  
5. 再扫该区 `goal-tree` 与目标五件套 / 审计意见  

不得发明第二套愿景路径；不得 sandbox 省略 plan。
