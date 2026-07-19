---
id: GOAL-008-skills-consumer-adapter-release-consistency
title: Skills 消费适配器跨宿主/跨版本发布一致性
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-20
version: 1.3.0
progress: 20%
---

## 2026-07-20 - CLI evidence correction

GitHub Copilot CLI `1.0.71` is now the Copilot candidate evidence source. The VS Code plugin is historical context only and is not used for this replay. Two bounded, read-only CLI replays passed and are bound to behavior-source and stdout/stderr digests:

- `/govern`: `attachments/runtime/copilot-cli-govern-2026-07-20.json`
- `/audit`: `attachments/runtime/copilot-cli-audit-2026-07-20.json`

I-002 remains `collecting / required` because the Web parser CI replay is still uncovered. I-003 and upstream GOAL-001 F-005 remain `collecting/open / required` because coverage is not ready and no clean, annotated release candidate is authorized. GOAL-008 therefore remains `active / 20%` and is not eligible for closure.

# GOAL-008 · Skills 消费适配器跨宿主/跨版本发布一致性

## 概述

按 [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19) 承接阶段 5：在不产生第二状态源的前提下，定义并验证 Skills 消费适配器的机读协议/模板版本、兼容声明和跨宿主/跨版本发布契约，形成可复核的兼容矩阵、fixtures、CI 与发行证据。

## 当前交付取舍与恢复（2026-07-19）

历史上，用户曾确认当前使用场景只需“可安装、可使用”的最低基线：canonical 契约与安装分发受测试覆盖，Claude Code `2.1.215`、Grok Build `0.2.103`、Copilot VS Code `1.129.1` / `copilot-chat 0.57.0` 均已有 `0.1.0` current `/govern` 的实际调度证据。该历史结论只允许声明**当前三宿主的 `/govern` 最低可用**，不等同于完整兼容验收、`/audit` 运行时、manifest 解析、CI 或 release 通过。

用户现已明确要求完整关门本目标，并在阶段 5 完成前不推进 Web 深化。[D-005](01-decision.md#d-005--重启完整发布一致性关门路径2026-07-19) 因此恢复 I-002、I-003 与上游 F-005 的 required 工作；最低可用证据保留为历史基线，不再作为延期理由。

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

> I-001～I-003 由 GOAL-001 D-010 登记为 `required`；I-001 已 `verified`。D-004 的历史延期已由用户在 D-005 中解除，I-002、I-003 当前均为 `collecting / required`，且没有 residual risk 接受。兼容矩阵、自动化与 rehearsal 已形成，但候选 runtime 与正式发行证据未闭环。

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|------------------|------|-------------|-------------|
| I-001 | required | 哪个 canonical 位置和字段承载机读协议/模板版本与兼容声明；版本演进和兼容判定采用什么语义？ | 阶段 5 方案与发布范围冻结 | 方案冻结前 | 按 D-002 创建 canonical schema/manifest、同步分发镜像，并以正反 fixtures 和适配器契约测试验证 | verified | 无延期；已于方案审视复核 | [D-002](01-decision.md#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；`python -m unittest skills/tests/test_skills_orchestrator.py -v`（29 passed）与 `python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`（3 passed） |
| I-002 | required | 哪些宿主/wrapper/Web 解析器版本必须支持当前与上一协议版本；兼容矩阵和 fixtures 的边界是什么？ | 受影响实施与兼容验收 | 阶段 5 兼容验收前 | 建立 canonical 矩阵、当前与 negative fixtures、跨宿主安装/消费重放；对固定版本的 `govern` 与 `audit` 分别取得可观察 dispatch | collecting | 2026-07-19 用户明确恢复完整关门；责任人：项目维护者；不再延期。`previousSupportedProtocol: null` 仅允许“首个基线无前身”的显式 N/A 与负例，不得伪造 predecessor。 | [D-003](01-decision.md#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)、[D-005](01-decision.md#d-005--重启完整发布一致性关门路径2026-07-19)、[D-008](01-decision.md#d-008--候选运行时证据契约与宿主配置边界2026-07-19)；Claude Code 与 Grok Build 的 `/govern`、`/audit` 已由机读证据验证。Copilot 两个入口与 Web parser CI replay 仍未覆盖，当前报告剩 3 个 uncovered 单元。 |
| I-003 | required | 发行物如何唯一标识，CI 如何重放 canonical/mirror、测试报告、变更日志与 tag/release 证据？ | 阶段 5 发布验收、F-005 关闭和阶段 7 输入 | 阶段 5 发布验收前 | 定义发行物身份和流水线产物，实施 CI 与发布演练，并核对可追溯 tag/release | collecting | 2026-07-19 用户明确恢复完整关门；责任人：项目维护者；不再延期。首次 annotated tag/release 或等价可追溯演练仍需维护者授权。 | [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19)、[D-005](01-decision.md#d-005--重启完整发布一致性关门路径2026-07-19)；`.github/workflows/ci.yml`、`scripts/compatibility_report.py`、`scripts/release_evidence.py`、`docs/releases/`、`CHANGELOG.md` 与本地 rehearsal 已形成；当前仍无 clean-tree CI 归档、ready coverage 或 annotated release tag。 |

## 高层路线图

| 阶段 | 主题 | 状态 | 退出证据 |
|------|------|------|----------|
| A | 信息发现与方案冻结：关闭 I-001，定义协议/兼容语义和发行证据契约 | 已完成（I-001） | 单一机读声明、兼容判定语义、canonical 所有者和契约测试方案 |
| B | 支持范围、兼容矩阵与 fixtures：按 I-002 冻结当前/上一版本边界 | 进行中（Claude/Grok 双入口已验证；Copilot 待人工证据） | 固定宿主版本、current `0.1.0` 与“无 predecessor”负例；每宿主 `govern` / `audit` 的可观察 dispatch |
| C | 跨宿主/跨版本验证与漂移校验 | 进行中（自动化、本地重放与 runtime freshness 校验已实现） | 可重复的安装/消费测试、canonical/mirror 校验和兼容性报告；当前报告仍列 Copilot 两项与 Web CI replay 共 3 个 uncovered 单元 |
| D | 发行证据与关门审计：按 I-003 形成可追溯发布证据并响应 F-005 | 进行中（rehearsal 工具链已实现） | CI 重放结果、报告、变更日志、矩阵 `candidateRevision` 与 annotated tag 相互绑定的 release-candidate 证据及阶段/关门审计结论 |

## 父目标

- [GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)

## 当前状态

本目标已按 D-010 建立。2026-07-19 已完成 I-001 的行业实践收集、设计、schema/manifest、镜像和契约测试；D-003 已冻结 I-002 的初始支持边界。D-005 之后已建立 canonical/Skills 兼容矩阵、负例 fixtures、Ubuntu/Windows CI、兼容/发行报告工具与本地 rehearsal；D-008 又以机读 schema、行为源/输出摘要和脱敏 transcript 验证 Claude Code、Grok Build 的 `/govern` 与 `/audit` 四个候选单元；2026-07-20 已用 GitHub Copilot CLI `1.0.71` 完成 `/govern` 与 `/audit` 机读重放。当前仅 Web CI replay 仍为 uncovered，且工作树不干净、无 annotated tag。I-002、I-003 与上游 F-005 继续为 `collecting / required`，阻断阶段 5 发布验收、GOAL-008 关门、阶段 6 Web 深化、阶段 7 验收和根目标关门；因此保持 `active / 20%`。
