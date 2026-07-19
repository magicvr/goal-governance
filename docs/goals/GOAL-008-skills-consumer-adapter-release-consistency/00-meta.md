---
id: GOAL-008-skills-consumer-adapter-release-consistency
title: Skills 消费适配器跨宿主/跨版本发布一致性
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 1.0.0
progress: 20%
---

# GOAL-008 · Skills 消费适配器跨宿主/跨版本发布一致性

## 概述

按 [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19) 承接阶段 5：在不产生第二状态源的前提下，定义并验证 Skills 消费适配器的机读协议/模板版本、兼容声明和跨宿主/跨版本发布契约，形成可复核的兼容矩阵、fixtures、CI 与发行证据。

## 当前交付取舍（2026-07-19）

用户确认当前使用场景只需“可安装、可使用”的最低基线：canonical 契约与安装分发受测试覆盖，Claude Code `2.1.215`、Grok Build `0.2.103`、Copilot VS Code `1.129.1` / `copilot-chat 0.57.0` 均已有 `0.1.0` current `/govern` 的实际调度证据。该结论只允许声明**当前三宿主的 `/govern` 最低可用**，不等同于完整兼容验收、`/audit` 运行时、manifest 解析、CI 或 release 通过。

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

> I-001～I-003 由 GOAL-001 D-010 登记为 `required`；I-001 已 `verified`。用户于 2026-07-19 确认 I-002、I-003 在当前最低可用范围内改为 `deferred`，但未接受 residual risk，也没有把它们写成 `verified`。`deferred required` 在其复核触发或受影响门禁到达时仍按开放 required 处理。

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|------------------|------|-------------|-------------|
| I-001 | required | 哪个 canonical 位置和字段承载机读协议/模板版本与兼容声明；版本演进和兼容判定采用什么语义？ | 阶段 5 方案与发布范围冻结 | 方案冻结前 | 按 D-002 创建 canonical schema/manifest、同步分发镜像，并以正反 fixtures 和适配器契约测试验证 | verified | 无延期；已于方案审视复核 | [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；`python -m unittest skills/tests/test_skills_orchestrator.py -v`（29 passed）与 `python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`（3 passed） |
| I-002 | required | 哪些宿主/wrapper/Web 解析器版本必须支持当前与上一协议版本；兼容矩阵和 fixtures 的边界是什么？ | 受影响实施与兼容验收 | 首次支持新的宿主/版本，或首次对外/可复现发布前 | 触发时扩展兼容矩阵、未覆盖入口和自动化重放；以版本固定的 current / negative fixture 与可观察 dispatch 完成验收 | deferred | 延期理由：当前只声明三宿主 current `/govern` 最低可用；责任人：项目维护者（本轮用户确认）；复核触发：首次支持新宿主/版本或首次对外/可复现发布，以先到者为准 | [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)、[D-004](01-decision.md#d-004--当前最低可用基线与发布一致性延期2026-07-19)；[runtime fixture 结果](attachments/i-002-runtime-fixture-2026-07-19.md)：Claude Code `2.1.215`、Grok Build CLI `0.2.103 (89c3d36fb6)` 与 Copilot VS Code `1.129.1` / built-in `GitHub copilot-chat 0.57.0` 均有归档 screenshot 显示实际调度 `/govern`，三条 manifest adapter 均为 `verified`；该结论仅覆盖 `0.1.0` current `/govern` fixture。 |
| I-003 | required | 发行物如何唯一标识，CI 如何重放 canonical/mirror、测试报告、变更日志与 tag/release 证据？ | 阶段 5 发布验收、F-005 关闭和阶段 7 输入 | 首次对外/可复现发布前 | 触发时定义发行物身份和流水线产物，实施 CI 与发布演练，并核对可追溯 tag/release | deferred | 延期理由：当前不进行对外/可复现发布；责任人：项目维护者（本轮用户确认）；复核触发：首次对外/可复现发布 | [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19)、[D-004](01-decision.md#d-004--当前最低可用基线与发布一致性延期2026-07-19)；当前 `0.5.0` 尚无 release tag |

## 高层路线图

| 阶段 | 主题 | 状态 | 退出证据 |
|------|------|------|----------|
| A | 信息发现与方案冻结：关闭 I-001，定义协议/兼容语义和发行证据契约 | 已完成（I-001） | 单一机读声明、兼容判定语义、canonical 所有者和契约测试方案 |
| B | 支持范围、兼容矩阵与 fixtures：按 I-002 冻结当前/上一版本边界 | deferred | 当前三宿主 `/govern` 最低可用已有证据；完整矩阵在首次支持新宿主/版本或首次对外/可复现发布时复核 |
| C | 跨宿主/跨版本验证与漂移校验 | deferred | 触发后形成可重复的安装/消费测试、canonical/mirror 校验和兼容性报告 |
| D | 发行证据与关门审计：按 I-003 形成可追溯发布证据并响应 F-005 | deferred | 首次对外/可复现发布时形成 CI 重放结果、报告、变更日志、tag/release 证据及阶段/关门审计结论 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 当前状态

本目标已按 D-010 建立。2026-07-19 已完成 I-001 的行业实践收集、设计、schema/manifest、镜像和契约测试；D-003 已冻结 I-002 的初始支持边界，三宿主的固定版本 current `/govern` runtime fixture 也已由归档证据验证，故保持 `active / 20%`。用户随后确认当前交付只声明该最低可用范围：I-002、I-003 与上游 F-005 均为 `deferred required`，在相应触发到来前不投入完整兼容矩阵、自动化重放或发布演练；它们未关闭，仍阻断阶段 5 发布验收、阶段 7 验收和根目标关门。
