---
id: E-002
goal: GOAL-012-release-v0-13-5
doc: execution
title: 版本清单与发布预演
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
---

# E-002 · 清单与预演

- S1 checkpoint `12b7ad9`。CHANGELOG 新增 0.13.5 节；根/Skills/bootstrap README 安装 pin 与 MCP 镜像示例对齐 0.13.5；文档使用 tag/Release 身份条件表述，没有提前声称已发布。
- canonical matrix candidateRevision = v0.13.5，evidenceScope 明示复用 2026-10-01 的原 capture；12 份 JSON 与原始输出未修改、未改名。受影响版本断言同步；stage 38 对，0 漂移，compatibility ready。
- README、CHANGELOG、MCP/Release 说明原缺 frontmatter，本轮补齐；created 使用其最早 Git 入库日期，updated 为当日。docs 入口版本及发布候选身份同步。
- 文档全量 67 tests OK；发布 rehearsal 内部的 Skills、standalone、scripts、whitespace 检查全部通过，`checks passed: True`。正式 annotated tag 与 clean-tree strict 验证尚属 S3。
- 首次 rehearsal 使用仓库 .venv Python，因其无法访问系统 TEMP 导致隔离安装用例失败。仅在执行子进程中设 TEMP/TMP 到仓库 artifacts/release-0.13.5-tmp、TMPDIR 为对应 Git Bash 路径、PYTHONUTF8=1，临时文件预检成功，原完整门禁重跑通过；未修改或跳过测试。原失败完整证据保留在 artifacts/release-0.13.5-failed-system-temp.json。
- 本地 v0.13.5 Skills/Core ZIP 已实际构建，86 / 27 个成员，core 字节子集、说明存在及 Skills README 包内链接核对 PASS。此为本地候选产物，不冒充未来 GitHub 资产。

可提交摘要及输出 hash 见 [s2-validation-summary.json](../attachments/s2-validation-summary.json)。完整本地 rehearsal 位于 artifacts/release-0.13.5-rehearsal.json，正式发布后以 Release strict evidence 为发行权威。

下一步：在稳定候选上执行独立审计并响应，之后 PR/CI/main、annotated tag、strict gate、人工 Environment 审批与真实资产验收。尚未创建或推送正式 tag。
