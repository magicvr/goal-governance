---
id: E-003
goal: GOAL-011-standalone-bootstrap-distribution
doc: execution
title: 分发与安装实现及 S2 验证
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
---

# E-003 · 实现与验证

## Checkpoint

S1 方案 checkpoint `ecb243ecb6b3940145c2a31e7739460e7cd023dc`，分支 `codex/issue-24-bootstrap-guide`；owned scope 为本目标与工作区树/Root 子目标表。Git 写入经授权宿主操作成功。

## 实现事实

- 先改 canonical principles/alignment/standalone 说明与消费 checklist，保持说明文件 Recommended、既有 MUST 门禁不变。
- stage 新增说明映射；core pack 的生产资产完整性检查保证说明存在。Skills/core-only 包内容及包内引用由真实 ZIP 测试核对，core 子集字节一致。
- Skills README 改用包内链接；双安装器按配置治理根复制说明，旧包缺说明仍可安装；受管映射纳入渲染、手改冲突与新增路径回滚。
- 说明补充 monorepo/core-only/已安装 Skills 的来源差异，以及新 Root 的 ledger 目录复制。

## 验证

| 检查 | 结果 | 证据 |
|------|------|------|
| stage + --check | 38 对，0 漂移 | 主代理执行 `python scripts/stage_skills_mirrors.py` 与 `--check` |
| 文档全量 | 66 tests，OK | [docs-tests.txt](../attachments/docs-tests.txt) |
| Skills 编排包 | 45 tests，OK | [skills-tests.txt](../attachments/skills-tests.txt) |
| scripts 全量 | 146 tests，OK，4 skipped | [scripts-tests.txt](../attachments/scripts-tests.txt) |
| compatibility | ready-for-release-evidence | [compatibility-report.json](../attachments/compatibility-report.json) |
| whitespace | git diff --check 通过 | 主代理核对 |

scripts 的跳过项为默认 Bash 指向无发行版的 WSL（2 项）及 Windows 无符号链接权限（2 项）；自定义治理根的真实 PowerShell / Git Bash 安装和 updater 路径均通过。后续 GitHub Ubuntu CI 补足平台覆盖，不将本地跳过项称为通过。日志尾部 `checks passed: False` 来自预期失败的 release-evidence 负向用例；suite 结果为 OK。

初次沙箱定向回归中临时 `git init` 被环境拒绝；宿主回归通过。首次完整 scripts 回归暴露新增断言错误比较原始占位符与安装后的渲染内容，已修正断言并重跑全套通过。未修改 runtime behaviorSources 中的 AGENTS/prompts，未重捕获或伪造宿主证据。

S2 完成，I-004 verified；进度按完成阶段 2/3 → 67%。交叉审计及 GitHub 交付/issue 关闭仍属 S3，尚未完成。
