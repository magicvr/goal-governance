---
doc_type: vision-revisions
title: 愿景修订时间线
status: active
created: 2026-07-28
updated: 2026-07-31
version: 0.2.0
---

# 愿景修订时间线

> 只追加，不改写旧条。`class`：`editorial`（措辞/链接）或 `strategic`（目的、边界、非目标、原则优先级）。  
> 与 Vision Review 编号区分：本表用 `VR-`；审视台账用 `VRev-`（[reviews.md](reviews.md)）。

| revision_id | date | version | class | summary | rationale | source | impact | charter_status_after |
|-------------|------|---------|-------|---------|-----------|--------|--------|----------------------|
| VR-005 | 2026-07-31 | 0.2.0 | strategic | 投资面重规划：Skills 为现行主适配器；人类 Web 远期 + 本仓 FastAPI **冻结参考实现**；预期通用基架取代自建栈（H-WEB-01）；演进以实际项目问题驱动（H-EVOL-01）。目的/成功边界/非目标已改；版本 **0.1.0→0.2.0** | 用户确认判断合理并授权 S1+B1；避免未定形态 Web 与自建栈长期抢注意力 | 用户确认 `/vision` 包 S1+B1；Web=冻结参考 | VP-001 意图/退出判据；workspace-001 + Root re-align；**strategic 后须 VRev + re-align**；不删 `web/` 代码 | active |
| VR-004 | 2026-07-29 | 0.1.0 | editorial | Charter 成功边界与原则摘要显式纳入 **P-006**（措辞补全；目的/非目标/版本未改） | GOAL-001 A-018 F-014 fixed | GOAL-001 D-025 / A-019 | 权威面与 principles 索引一致；**不**触发 re-align | active |
| VR-003 | 2026-07-28 | 0.1.0 | editorial | 对齐/协议升级至 **P-006**：单愿景不变量；冷启动串行；取消 sandbox opt-out；`reviews.md`；组合编排命名；宽阻断与 lead 必填。Charter **正文目的/边界未改**（仍 0.1.0） | 用户确认 D0–D24 与第一刀落盘（GOAL-001 D-017） | GOAL-001 D-017 | 全仓完整安装与开区/推进门禁；Skills `/vision` 第二刀 | active |
| VR-002 | 2026-07-28 | 0.1.0 | editorial | `alignment.md` → 0.2.0：Primary 三处冲突裁决；`active` VP 零工作区 14 日空转宽限；consumer-checklist 勾选 | 核心协议逻辑审视（GOAL-001 D-016）；不改 Charter 目的/边界 | GOAL-001 D-016；用户确认修订 | 编排器/适配器 fail closed 与空转门禁可机读解释 | active |
| VR-001 | 2026-07-28 | 0.1.0 | strategic | 从 Root 叙述拆出仓库级愿景体系（Charter + VP + 对齐链） | 多工作区下各区 Root 易漂移；总目的应不可 done 且可演进，规划可关门并对齐愿景 | 用户确认的 Vision→VP→Workspace 冻结方案 | workspace-001-goal-governance 及后续新区须挂 VP | active |
