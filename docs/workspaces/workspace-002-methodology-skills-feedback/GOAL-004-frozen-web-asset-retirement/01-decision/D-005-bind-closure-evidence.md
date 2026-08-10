---
id: GOAL-004-frozen-web-asset-retirement
doc: decision-entry
record_id: D-005
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# D-005 · 以父提交绑定模型响应 A-002

## 触发

A-002 independent finding-closure 实际重跑全部命令并通过，但维持 `conditional`：已提交的第一代 evidence 绑定实现提交 `9ae56da`，而整改 ledger checkpoint 是 `1416aa2`；provider 同时报告了与主工作树权威状态矛盾的 dirty snapshot。

## 决定

1. 继续选择 **fixed**，不把 A-002 视为 pass，也不把 F-001 静默关闭。
2. evidence 采用有限的父提交绑定：在 clean `1416aa2` 上执行命令，JSON 的 `source.commit` 必须为 `1416aa2`；后继 Git checkpoint 保存这些证据字节。要求 JSON 自指包含自身的后继 commit 会形成不可满足的哈希循环，因此不是关门判据。
3. 新增两份 `closure-1416aa2` machine-readable evidence；后继 independent provider 应核对 source commit 存在、是证据 checkpoint 的祖先，且二者间无 producer 行为变化，并在 clean checkpoint 上独立重跑。
4. A-002 的 dirty observation 原样保留；当前主工作树在生成新 evidence 前 `git status --short` 为空，生成后只出现两份预期附件。最终 clean 状态必须由 evidence checkpoint 后的新 independent provider 再核对。
5. F-001 在新的 independent `pass` 前继续按 required/open 处理；目标保持 `active / 75%`。
