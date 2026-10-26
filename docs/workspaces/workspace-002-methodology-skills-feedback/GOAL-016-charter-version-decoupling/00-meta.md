---
id: GOAL-016-charter-version-decoupling
title: Charter 注册表解耦与 vision_ref 版本语义修正（issue #34）
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
progress: 60%
---

# GOAL-016 · Charter 注册表解耦与 vision_ref 版本语义修正（issue #34）

## 概述

承接 [GitHub issue #34](https://github.com/magicvr/goal-governance/issues/34)（OPEN，2026-10-26T02:15:24Z）：Charter 同时承担「愿景契约」与「组合/工作区注册表」，且 `vision_ref` 精确钉住文档 `version`，导致新建 VP/工作区、甚至仅更新 Charter 登记表就触发版本 bump，进而迫使全部 `planned`/`active`/`closed` VP 重写 `vision_ref`，历史审计链被改写、新建成本随 VP 数量上升。

本目标修正协议语义、校验实现、模板/文档/Skills 消费面与回归测试，并以一个新版本发布收口；同时按仓库惯例关闭 issue #34。变更属元规则/协议面，审计模式 `cross`（self + independent），独立审计 provider 由用户指定为本地 codex CLI（模型 `gpt-6.1-sol`，思考强度 `high`）。

## 成功标准

- [ ] **A1 去注册表**：Charter 不再承载可变注册表（`primary_workspace` 与「现行版本」中的 Primary / active VP / 组合编排行）；模板与消费面同步；旧 Charter 残留字段作为 legacy hint 读取/忽略，不参与门禁，不要求消费仓立即迁移。
- [ ] **A3 生命周期分层**：`planned`/`active` VP 的 `vision_ref` 仍精确匹配现行 Charter；`closed`/`abandoned` VP 保留关门时 ref，仅校验 `vision_id` 相同；`validate_vision_stack` 与 workspace `plan_refs` 校验均按 status 过滤。
- [ ] **A2 版本语义**：Charter `version` 只表达战略对齐版本，仅 `strategic` 变更 bump（至少 minor）；`editorial` 只更新 `updated` 并追加 `revisions.md`（VR-）记录，不 bump、不要求 active/planned VP 重钉。
- [ ] **primary 收敛**：primary 仅由 `workspace.md` 的 `vision_role: primary` 与 `workspaces.md` 的派生投影表达；两者冲突 fail closed；至多一个 primary；Charter 字段删除后不再参与裁决。
- [ ] **回归与消费兼容**：新增「新建 VP 不改 Charter」「closed VP 不重钉」「strategic bump 仍阻断 active VP」「primary 两处冲突 fail closed」测试；旧仓 `primary_workspace` 与旧 `vision_ref` 不被新校验误判；文档/模板/Skills 镜像同步且 `stage_skills_mirrors.py --check` 通过。
- [ ] **发布与关门**：按用户确认的版本号完成 CHANGELOG/清单/运行证据/回归/PR/CI/main/tag/受门禁发布；Release 资产逐项验收；issue #34 关闭；目标经 cross 审计与用户确认后关门。

## 纲领路线图（P-001）

| 阶段 | 名称 | 状态 | 退出条件 |
|------|------|------|----------|
| **S1** | 问题复核与裁决冻结 | **完成**（2026-10-26） | issue #34 主张在代码/文档中可复现；Q-001～Q-004 获真实答复并落 D-002；范围、验收与审计模式冻结 |
| **S2** | 协议与 canonical 文档修正 | **完成**（2026-10-26） | `alignment.md`、`principles.md` P-006、`workspace-protocol.md`、`AGENTS.md`、Charter、模板与 consumer 文档按 D-002 同步；语义无自相矛盾 |
| **S3** | 校验实现、回归与消费面同步 | **完成**（2026-10-26） | validator/测试/fixtures 实现 A1/A3/A2；新增回归测试与 docs/skills 回归通过；Skills prompts/模板/契约镜像同步且 `stage_skills_mirrors.py --check` 通过；旧仓兼容用例通过。release/compatibility 门禁因 behavior source 变更保持红，按 E-003 移交 S5 重捕获 |
| **S4** | cross 审计与意见响应 | 进行中 | A-001 self 与 A-002 independent（codex CLI `gpt-6.1-sol` / high）落盘；全部相关 required 按三路径合法闭合；无冲突；发布就绪意见可核对 |
| **S5** | 发布与关门 | 未开始 | 版本清单、运行证据（如需重捕获）、本地门禁与 strict rehearsal 通过；PR 双平台 CI 全绿并合入 `main`；annotated tag；tag workflow 的 pack 与 gated publish 全绿（Environment `release` 由用户人工审批）；9 项 Release 资产逐项验收；issue #34 关闭；关门审计与用户确认完成 |

阶段先后为串行；S2/S3 内部可按文件批次并行，S4 必须在 S2/S3 事实冻结后。`progress` 仅由本表 5 个检查点等权派生；不用于放行、关闭 finding 或推导 `done`。

## 派生进度展示

`progress: 60%` = S1～S5 中完成 3 / 5（S1～S3 完成，S4 进行中）。检查点变化后重算并同步 `goal-tree.md`。

## 信息就绪与未知项

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 选 A（A1+A3+A2）、A1+A3（仅消除主诉）还是 B（新增 `alignment_version`） | S2 方案冻结 / 写集 | S1 | 用户按 Q-001 书面裁决；记录 D-002 | **verified**（2026-10-26） | 若后续改选 B 则重新裁决 | 用户答复 **A：A1+A3+A2**；见 [D-002](01-decision/D-002-adjudication.md) |
| I-002 | required | `primary` 语义 = 稳定 monorepo 身份，还是「当前活跃工作区」 | A1 的 primary 权威与校验 | S1 | 用户按 Q-002 裁决；记录 D-002 | **verified**（2026-10-26） | 若改选双权威则重新裁决 | 用户答复 **单一权威（仅 `workspace.md`）**；见 [D-002](01-decision/D-002-adjudication.md) |
| I-003 | required | `closed` VP 历史 `vision_ref` 只校验 `vision_id`，还是还要求版本在 `revisions.md` 可追溯 | A3 校验强度 | S1 | 用户按 Q-003 裁决；记录 D-002 | **verified**（2026-10-26） | 若改选 revisions 可追溯则重新裁决 | 用户答复 **仅 `vision_id` 相同**；见 [D-002](01-decision/D-002-adjudication.md) |
| I-004 | required | 发布版本号：patch `v0.13.8` / minor `v0.14.0` / 其他 | S5 版本清单、tag 与资产身份 | S5 清单前 | 用户按 Q-004 裁决；记录 D-002 | **verified**（2026-10-26） | 清单后不得静默改号 | 用户答复 **patch `v0.13.8`**；见 [D-002](01-decision/D-002-adjudication.md) |
| I-005 | required | GitHub Environment `release` 的发布审批是否由用户人工完成 | S5 gated publish | S5 发布 | 用户在 GitHub 人工审批；AI 不代批、不改环境配置 | open | 到期未批则 S5 保持未满足 | 待确认 |

## 父目标

- [GOAL-001-methodology-skills-feedback-evolution](../GOAL-001-methodology-skills-feedback-evolution/00-meta.md)（`parent` 完整 id；Root 为 `active`，R3 持续演进）
- 规划对齐：`primary_plan` = `VP-002-methodology-skills-feedback-evolution`；Charter `vision-goal-governance@0.2.0`

## 台账布局

本目标三个可追加台账使用平铺目录：`01-decision/`、`02-execution/`、`03-audit/`。索引文件保留 frontmatter、摘要与条目索引；独立记录使用 `D-NNN-*`、`E-NNN-*`、`A-NNN-*` 文件。`attachments/` 存放长证据。

## 备注

- **变更流程判定**：本目标同属 Root GOAL-001 目的与边界内（协议/Skills 反馈演进），按 P-006 §6.6 选择**子目标**，不新开 VP/工作区；不触发 Charter `strategic`，因此不强制 Vision Review。alignment 的语义变更由本目标的 cross 审计覆盖，不另立 VRev。
- **审计模式** `cross`（元规则/协议变更）：A-001 self + A-002 independent；provider = 本地 codex CLI（`gpt-6.1-sol`，思考强度 `high`）。provider 失败/超时/无可核对输出时门禁保持未满足，不降级、不由编排器冒充 independent。
- **发布边界**：版本号、tag、Release 与资产验收按仓库既有 release 流程；Environment `release` 审批由用户完成，AI 不代批、不改环境配置；不覆盖旧 Release。
- **历史只读**：不重写已关门 GOAL-002～GOAL-015 的历史记录与既有审计意见；旧 `vision_ref`/旧 `primary_workspace` 记录按历史事实保留。
