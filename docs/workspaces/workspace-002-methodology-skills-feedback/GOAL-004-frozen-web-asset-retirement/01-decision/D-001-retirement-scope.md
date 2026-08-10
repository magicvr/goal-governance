---
id: GOAL-004-frozen-web-asset-retirement
doc: decision-entry
record_id: D-001
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.2.0
---

# D-001 · 冻结 Web 资产退役范围与保护门禁

## 决定

1. 删除整个 `web/` 所有 tracked 与本地遗留内容；不保留 archive、fixture 副本或可选 test profile。
2. 删除仅为 Web 存在的 CI 安装/测试步骤、`--include-web` 参数与 release-mode 强制、compatibility matrix 的 `web-readonly-parser` consumer、report 专属校验和对应测试断言。
3. 保留所有非 Web producer 门禁：Skills contract tests、standalone tests、scripts tests、diff whitespace、canonical/mirror parity、三宿主 runtime evidence freshness、coverage readiness、annotated-tag / clean-tree / changelog / candidateRevision 约束。
4. 现行文档改为“Web 资产已退役、VP-003 planned + 正式挂起”；历史 Goal、audit、attachments、旧 CHANGELOG release sections 和 runtime evidence 不批量改写。
5. 本次不改核心方法论、模板、Skills prompts/install/core，也不创建新 tag 或 Release。canonical matrix 的 mirror 由 stage 脚本生成，不手改。

## 关门门禁

- `web/` 路径不存在，且 active scan 不再发现可执行 Web 依赖。
- stage `--check` 和非 Web 全量测试通过。
- 基线保护路径 diff 为空；`skills/` 变化仅允许 matrix mirror。
- independent A-001 `pass` 且没有开放 required finding。

## 未选方案

- **保留源码、只跳过测试**：仍污染审计、依赖扫描和维护语义。
- **压缩到历史 archive**：仍是仓库资产，不能满足“彻底移除”。
- **改动 core/Skills 版本或发版**：没有方法论或消费者行为变化，不应扩大范围。

## 后续精化

[D-002](D-002-core-navigation-boundary.md) 发现 canonical `overview.md` / `directory-layout.md` 是现行 core 导航，删除后必须做 editorial 修正并 stage 对应镜像；canonical/mirror matrix 与 `skills/tests/test_skills_orchestrator.py` 只移除已退役 Web consumer 及断言。D-001 的方法论/Skills **行为不变与不发版**边界继续有效。

[D-003](D-003-runtime-evidence-retirement-boundary.md) 确认已发布 runtime capture 是 SHA 固定的历史时点证据，不批量改写；其中 Web 文字不再构成当前 consumer、支持声明或回归门禁。
