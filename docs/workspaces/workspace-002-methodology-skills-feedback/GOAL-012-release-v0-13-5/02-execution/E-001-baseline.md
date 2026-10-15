---
id: E-001
goal: GOAL-012-release-v0-13-5
doc: execution
title: 发布前只读基线核对
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
---

# E-001 · 基线核对

- 起始 HEAD `e820103c3a434eb936c60f5d6cb17b56ad9ab36d`，工作树干净，已同步 origin/main；创建分支 `codex/release-v0.13.5`。
- GitHub 最新正式 Release 为 v0.13.4；v0.13.5 tag 未存在。当前工作区最大号 011，创建 GOAL-012 并同步 Root 子目标表/goal-tree；R3 与 VP-002 语义对齐，相关 VRev 索引 open required 为 0。
- `capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.4` 返回 12 份一致；工作流指定 L3 目录返回 4 份一致；`compatibility_report.py --require-ready` 返回 ready-for-release-evidence。
- strict release mode 实现要求 matrix candidateRevision 等于 annotated tag，并在干净树上实际执行检查；capture JSON 不携带 release tag 身份，按 protocol、behaviorSources hash、原始 stdout/stderr hash 等验证。
- GitHub API 回读 Environment release：reviewer magicvr、wait_timer 5、自定义 branch policy；未修改设置或执行代审批。
- S1 完成，progress 1/4 = 25%。尚未修改发布清单、创建 v0.13.5 tag 或发布资产。
