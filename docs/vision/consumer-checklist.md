---
doc_type: vision-consumer-checklist
title: 愿景体系消费方检查清单
status: active
created: 2026-07-28
updated: 2026-07-28
version: 0.1.0
---

# 消费方检查清单

> 政策以 [alignment.md](alignment.md) 为准。本清单只做操作映射；变更规则时先改 alignment，再同步本页。

## A. 仓库发现

- [ ] 存在 `docs/vision/README.md` 与 `docs/vision/charter.md`
- [ ] 存在 `docs/vision/roadmap.md`、`revisions.md`、`workspaces.md`、`alignment.md`、`consumer-checklist.md`
- [ ] 至少存在一个 `docs/vision/plans/VP-*.md`
- [ ] Charter：`doc_type: vision-charter`，`vision_id`、`version` 有值，`status` ∈ {`active`,`superseded`}（**不是** `done`）

## B. 当前工作区

- [ ] 已定位焦点 `workspace.md`（多区未指定则 fail closed）
- [ ] 非 sandbox opt-out 时：存在 `vision_role`、`plan_refs`、`primary_plan`
- [ ] `primary_plan` ∈ `plan_refs`（逗号分隔列表）
- [ ] `primary_plan` 对应文件 `docs/vision/plans/<primary_plan>.md` 存在
- [ ] Root `00-meta` 的 plan 字段与 workspace 一致（或可解释的同步中状态）

## C. VP 链

- [ ] VP `status` ∈ {`planned`,`active`,`closed`,`abandoned`}
- [ ] VP `vision_ref` 等于 `{charter.vision_id}@{charter.version}`（精确匹配）
- [ ] 若 VP `active` 且绑定工作区为 0：告警或询问，不静默当作健康推进
- [ ] 多区时优先确认 `lead_workspace`（推荐）

## D. 门禁动作

- [ ] 新建区/Root/关键推进/关门前跑完 A–C
- [ ] Charter strategic 修订后检查 VP 与区 re-align
- [ ] 不把 vision 目录内容当作 progress 或 finding 关闭证据
- [ ] Primary 声明（workspace / workspaces.md / charter.primary_workspace）无互相矛盾；若矛盾已 fail closed 并待用户裁决
- [ ] `active` VP 若零工作区：已告警；未超 14 日空转宽限，或已有继续空转书面留痕
- [ ] VP 关门要求区证据链接；有界 residual 已点名

## E. 编排器读序（最小）

1. 若存在 `docs/vision/charter.md` → 读 charter 版本与 alignment 要点  
2. 定位并校验当前 `workspace.md`（含 plan 字段）  
3. 解析 `primary_plan` → 读对应 VP  
4. 再扫该区 `goal-tree` 与目标五件套 / 审计意见  

缺 vision 树且仓库已声明多工作区或显式依赖本协议时：报告不完整安装或 fail closed（见 alignment），不得发明第二套愿景路径。
