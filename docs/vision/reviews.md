---
doc_type: vision-reviews
title: 愿景审视台账（Vision Review）
status: active
created: 2026-07-28
updated: 2026-07-28
version: 0.1.0
parent: null
---

# 愿景审视台账 · Vision Review

> 权威规则见 [alignment.md](alignment.md) §9 与 [principles.md](../architecture/principles.md) P-006。  
> **不是** Goal `03-audit`；不汇总 progress%；默认不直接改 Charter/VP status。  
> 编号：`VRev-00N`（与 [revisions.md](revisions.md) 的修订号 `VR-` 区分）。

## 使用说明

| 项 | 约定 |
|----|------|
| 强制时机 | Charter 初建；每次 Charter `strategic` 修订后 |
| source | `self` \| `independent` |
| verdict | `pass` \| `conditional` \| `fail` |
| required 闭合 | `fixed` / `accepted-residual` / `user-overruled` + 留痕 |
| 阻断 | 未闭合 required 可阻断开区、VP 关门、宣称「方向已稳」 |

## 条目索引

| id | date | source | scope | verdict | summary |
|----|------|--------|-------|---------|---------|
| — | — | — | — | — | （尚无条目；初建 Charter 的补录 Review 可在此追加） |

---

## 条目正文

（按 `VRev-00N` 追加节。模板：）

```markdown
### VRev-00N · <短标题>（YYYY-MM-DD）

| 字段 | 值 |
|------|-----|
| source | self \| independent |
| scope | charter-init \| charter-strategic \| portfolio \| other |
| verdict | pass \| conditional \| fail |
| auditor | <工具或人> |

**摘要** …

**Findings**
- [required|recommended] …

**建议 class**：editorial | strategic | no-change

**闭合**（若有 required）：路径 / 证据链接 / 用户裁决
```
