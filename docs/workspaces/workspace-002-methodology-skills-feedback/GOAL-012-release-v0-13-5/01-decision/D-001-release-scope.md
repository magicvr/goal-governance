---
id: D-001
goal: GOAL-012-release-v0-13-5
doc: decision
title: v0.13.5 发布范围与证据策略
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
---

# D-001 · 发布范围

用户明确要求发布新版本资产。当前最新正式版 v0.13.4，已合入的 GOAL-011 是兼容性分发修复，不改变 protocol 0.1.0、consumer contract 或 MUST，采用下一 patch **v0.13.5**。不覆盖旧 Release，不移动既有 tag。

发布沿用已建路径：版本清单/矩阵 → 回归与 rehearsal → 会话指定 Codex independent 候选审计 → PR CI → main merge → annotated tag → strict gate → push tag → 现有 release Environment 人工审批 → Release 九项资产 + GHCR → 真实下载验收。

现有 v0.13.4 的 12 格宿主 capture 与工作流 L3 的 4 份 capture 已实际 `--check` 通过，当前 compatibility ready。复用原始证据而不复制改名或修改捕获日期；矩阵 candidateRevision 改为 v0.13.5，evidenceScope 明示复用。清单变更后再校验；出现 stale 或新行为来源时先处理，不静默放行。

模式 independent（release / compatibility scope），provider 沿用本会话用户指定的干净 Codex 子代理。GitHub Environment 现有 reviewer magicvr + 5 分钟 wait timer 不改；用户审批是独立的最后发布门禁，AI 不代批或绕过。

未选：覆盖 v0.13.4 资产（破坏已有版本身份）；无实际行为变化却伪造新 capture（破坏证据事实）；修改 workflow 绕过人工审批（不在授权与本轮范围）。
