---
id: D-002
goal: GOAL-011-standalone-bootstrap-distribution
doc: decision
title: 方案 A 与 Codex 独立子代理
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
---

# D-002 · 方案与 provider 冻结

## 用户裁决

用户回复「a」，选择随包分发并保持 Recommended；同步问答中选择「Codex 独立子代理 (Recommended)」为 independent provider。用户随后确认已恢复 GitHub 登录；非沙箱 `gh issue view 24` 成功回读 OPEN。

## 决定与实施计划

1. canonical `docs/standalone-bootstrap.md` 进入 stage → `skills/core/docs/standalone-bootstrap.md`，随 core-only 与 Skills ZIP 分发；pack 必须保证新发布资产包含它。
2. alignment 明列说明为 Recommended；principles、consumer-checklist、说明同步澄清：操作要求对齐 MUST 表，不把说明文件本身变成完整安装门禁。修正说明中 monorepo 与解压包的操作来源边界。
3. Skills README 链接改到包内 `core/docs/standalone-bootstrap.md`；两个安装器在来源存在时复制到配置的治理根；纳入受管路径渲染、冲突检查与回滚。旧包没有该 Recommended 文件时继续兼容。
4. 验证 stage 正反例、两 ZIP 包含及逐字节一致、消费仓默认/自定义治理根安装、旧包升级补齐与手改冲突保护；运行现有相关文档和分发回归。
5. self 审计 + 干净 Codex 子代理 independent 只读核验，主代理代贴原始意见并响应；所有 required 合法闭合后交付 GitHub，再关闭并回读 issue。目标范围为源码修复交付，不新增版本/tag/Release；正式资产仍保持原发布 pin。

## 理由与未选方案

本地说明可离线核对，符合 core-only 用途；Recommended 保持既有完整安装门禁。未选 MUST：会把旧消费仓缺文件变成新的阻断；未选固定版本外链：离线不可读，且需额外维护版本链接。包的完整性校验与消费仓的 MUST 门禁是两个不同范围。

## 审计与边界

模式 cross，provider = Codex 独立子代理，保证等级为默认 L0。子代理仅探索/独立核验，不改文件、不作状态裁决；主代理负责实现与最终验证。Root/VP 保持长期 active，Root progress 仍为 67%。
