<!-- goal-governance:begin managed -->
---
title: Goal Governance · 按需入口
status: active
created: 2026-11-03
updated: 2026-11-03
parent: null
version: 1.0.0
---

## 目标治理（按需加载）

- 仅在调用 `/govern`、`/audit`、`/vision`、`/vision-audit`（含 `$` 形式/原语）、用户要求目标/愿景治理，或准备修改治理记录（Charter、VP、workspace、goal-tree、GOAL 台账/审计）时加载完整规则。普通业务代码与一般文档任务不要求读取治理全文或自动更新目标。
- 触发后先检查仓库 `.goal-governance.json`：存在时校验 JSON、`governance_root` 为仓内相对路径及解析后的符号链接边界；仅无配置才用 `{{GOVERNANCE_ROOT}}`（默认 `docs`）。配置非法立即停止治理操作，不回退。
- 在已验证根完整读取 `architecture/governance-guide.md`（安装时路径：[完整指南]({{GOVERNANCE_ROOT}}/architecture/governance-guide.md)），并按指南读取必备权威，再扫描/修改治理记录。指南缺失或不可读时停止治理并补装 core，不凭本入口或包内镜像继续。
- 目标状态只以已验证工作区的 `goal-tree.md` 与目标五件套为准；遵守完整指南的 P-001～P-006 与用户裁决门禁。框架只更新 managed 标记内内容，标记外由项目维护。
<!-- goal-governance:end managed -->
