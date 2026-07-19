---
id: GOAL-008-skills-consumer-adapter-release-consistency
title: Skills 消费适配器跨宿主/跨版本发布一致性
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.6.0
progress: 20%
---

# GOAL-008 · Skills 消费适配器跨宿主/跨版本发布一致性

## 概述

按 [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19) 承接阶段 5：在不产生第二状态源的前提下，定义并验证 Skills 消费适配器的机读协议/模板版本、兼容声明和跨宿主/跨版本发布契约，形成可复核的兼容矩阵、fixtures、CI 与发行证据。

## 范围

### 纳入

- core docs / canonical 模板、Skills 安装产物，以及 Claude Code、Grok Build、GitHub Copilot wrappers 和 Web 只读解析器之间的兼容矩阵。
- 当前版本与上一版本的协议/模板 fixtures、跨宿主安装/消费测试和可重复的兼容性报告。
- canonical/mirror 漂移校验、测试报告、变更日志、发行物唯一身份和可追溯 Git tag/release 证据。

### 排除

- 不重新定义 canonical 方法论、P-001～P-005 或模板上游；必要的核心协议语义变更须另行按治理流程留痕。
- 不开发 Web 写入、创建/更新界面、独立数据库或同步机制；Web 深化属于阶段 6。
- 不承担三面联合发布、跨面漂移最终验收或 GOAL-001 关门；这些属于阶段 7 与根目标关门。
- 不把真实消费者采用度试点设为本目标的 required 成功标准；该证据留待后续独立试点或阶段 7 发布复盘。

## 成功标准

- [x] 形成唯一的、可机读的协议/模板版本与兼容声明，明确版本演进、兼容判定语义和 canonical 所有者，并以 schema 或契约测试验证。
- [ ] 建立覆盖 core docs / canonical 模板、Skills 安装产物、三类宿主 wrappers 与 Web 只读解析器的兼容矩阵，明确当前及上一协议版本支持范围。
- [ ] 建立当前版本与上一版本 fixtures，完成跨宿主安装/消费测试，并让报告区分已验证范围与未覆盖范围。
- [ ] 建立 canonical/mirror 漂移校验，由 CI 可重复生成校验结果、测试报告、变更日志和发行物身份记录。
- [ ] 完成至少一次可追溯的 tag/release 或等价发布演练，使版本、commit、测试报告和变更范围能够相互关联；不把阶段 7 最终验收写成本目标成果。

## 信息就绪与未知项（P-005）

> I-001～I-003 由 GOAL-001 D-010 登记为 `required / collecting`；本目标创建时承接其责任，但当前没有 residual risk 接受，也没有把任何项写成 `verified`。未关闭项只阻断其影响的门禁。

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|------------------|------|-------------|-------------|
| I-001 | required | 哪个 canonical 位置和字段承载机读协议/模板版本与兼容声明；版本演进和兼容判定采用什么语义？ | 阶段 5 方案与发布范围冻结 | 方案冻结前 | 按 D-002 创建 canonical schema/manifest、同步分发镜像，并以正反 fixtures 和适配器契约测试验证 | verified | 无延期；已于方案审视复核 | [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；`python -m unittest skills/tests/test_skills_orchestrator.py -v`（29 passed）与 `python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`（3 passed） |
| I-002 | required | 哪些宿主/wrapper/Web 解析器版本必须支持当前与上一协议版本；兼容矩阵和 fixtures 的边界是什么？ | 受影响实施与兼容验收 | 支持范围在实施前冻结；fixture 证据在验收前完成 | 按 D-003 冻结首个/上一协议基线、声明/承诺层级和 Web 边界；实现 canonical manifest/schema 与 contract fixtures；再收集精确宿主 release 的运行时证据 | collecting | 无延期；实施前与验收前分别复核 | [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)；[I-002 宿主与契约证据](attachments/i-002-host-compatibility-evidence-2026-07-19.md)；`docs/contracts/skills-consumer-contract.json`：`0.1.0` 为首个支持协议、无上一版本；Claude Code CLI 与 GitHub Copilot VS Code 为 committed，Grok Build CLI 为 declared，均仍 `unverified`；Web 不作为 adapter；30 项 Skills 契约测试与 3 项 standalone bootstrap 测试通过 |
| I-003 | required | 发行物如何唯一标识，CI 如何重放 canonical/mirror、测试报告、变更日志与 tag/release 证据？ | 阶段 5 发布验收、F-005 关闭和阶段 7 输入 | 证据契约在方案冻结前定义；实际证据在阶段验收前完成 | 定义发行物身份和流水线产物，实施 CI 与发布演练，并核对可追溯 tag/release | collecting | 无延期；方案冻结与阶段验收分别复核 | [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19)；当前 `0.5.0` 尚无 release tag |

## 高层路线图

| 阶段 | 主题 | 状态 | 退出证据 |
|------|------|------|----------|
| A | 信息发现与方案冻结：关闭 I-001，定义协议/兼容语义和发行证据契约 | 进行中 | 单一机读声明、兼容判定语义、canonical 所有者和契约测试方案 |
| B | 支持范围、兼容矩阵与 fixtures：按 I-002 冻结当前/上一版本边界 | 进行中 | 三宿主与 Web 只读消费者矩阵、当前/上一版本 fixtures、实施前复核记录 |
| C | 跨宿主/跨版本验证与漂移校验 | 待开始 | 可重复的安装/消费测试、canonical/mirror 校验和兼容性报告 |
| D | 发行证据与关门审计：按 I-003 形成可追溯发布证据并响应 F-005 | 待开始 | CI 重放结果、报告、变更日志、tag/release 证据及阶段/关门审计结论 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 初始状态

本目标已按 D-010 建立。2026-07-19 已完成 I-001 的行业实践收集、设计、schema/manifest、镜像和契约测试，故为 `active / 20%`；D-003 已冻结 I-002 的初始支持边界，但 I-002 仍阻断外部宿主运行时兼容验收，I-003 与 F-005 仍阻断阶段验收和关门。
