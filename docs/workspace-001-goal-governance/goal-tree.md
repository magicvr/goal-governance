---
title: Goal Tree · 目标树与进展总览
status: active
created: 2026-07-18
updated: 2026-07-21
parent: null
version: 0.42.0
---

# Goal Tree

## 2026-07-21 · GOAL-009 F-003/F-004 有界关闭

D-020-A / A-038：路径 A；**F-003/F-004 closed** + R-F003/R-F004 residual；路线图 B finding 有界退出。GOAL-009 progress **80%**。

## 2026-07-21 · GOAL-009 WS+SM 核心矩阵执行

A-036：WS/SM 核心 **pass**。其后 F-003/F-004 已有界关闭（见上节）。

## 2026-07-21 · GOAL-009 R-003 验证包（F-003/F-004）

D-019/A-035：冻结 R-003 验证包；其后 WS/SM 已执行（见上节）。

## 2026-07-21 · GOAL-009 F-002 有界关闭

D-018-A / A-034：路径 A；**F-002 closed** + R-F002-1～3。其后 R-003 验证包已冻结（见上节）。

## 2026-07-21 · GOAL-009 FA-001～006 执行

A-032：`fact_admission` + unittest；**68 passed, 1 skipped**；FA-001～006 **pass**。其后 F-002 已有界关闭（见上节）。

## 2026-07-21 · GOAL-009 R-002 验证包（F-002）

D-017/A-031：冻结 [r-002-verification-package](GOAL-009-ai-assisted-governance-workbench/attachments/r-002-verification-package.md)；其后 FA 已执行（见上节）。
## 2026-07-21 · 本地产品工作区部署（ALLOW=true）

配置 `data/product-workspace` + `web/.env`（ALLOW=true，非 dogfood）。`/api/health` 显示 `controlled_write_enabled=true`。GOAL-009 progress 当时 **60%**。
## 2026-07-21 · GOAL-009 A-030 生产受控写入授权

D-016/A-030：规划锁默认关闭；须 `ALLOW_CONTROLLED_WRITE=true` + 产品数据根 + 单进程 residual。GOAL-009 progress **60%**。

## 2026-07-21 · GOAL-009 A-029 I-003/I-004/I-006 α verified

用户选 V1：I-003/I-004/I-006 **verified（α 有界）**。F-007/F-008 closed。其后 A-030 授权生产写（见上节）。

## 2026-07-21 · GOAL-009 A-028 审视 I-003/I-004/I-006

A-028 / D-015 proposed；其后用户选 V1（见上节）。

## 2026-07-21 · GOAL-009 A-027 有界关闭 F-008

用户选路径 A：接受 R-F008-1～3 residual；**F-008 closed（有界）**。I-003/I-004/I-006 非 verified；生产写入仍关。GOAL-009 progress **48%**。

## 2026-07-21 · GOAL-009 A-026 F-008 residual 审视

GOAL-009 落盘 F-008 residual 路径 A/B/C（A-026 / D-014 proposed）。其后用户选路径 A（见上节）。

## 2026-07-21 · GOAL-009 A-025 关闭 F-007

GOAL-009 **F-007 closed**（确认/信任边界）。**F-008 仍 open**（process-local CT-009、最小 CT-011 等）。I-003/I-004/I-006 非 verified；生产写入仍关。GOAL-009 progress **42%**。

## 2026-07-21 · GOAL-013 阶段 E 有界关门与 A-024 门禁审视

GOAL-013 `done / 100%`（实现证据交付完成）。最终回归 **61 passed, 1 skipped**。GOAL-009 A-024 当时 F-007/F-008 仍 open；现 F-007 已由 A-025 关闭。

## 2026-07-21 · GOAL-013 阶段 D F-008 CT

GOAL-013 完成 CT-008/009/010/011 可运行证据，progress **75%**；CT-009 明确限于 process-local lock。GOAL-009 F-007/F-008 仍 open，生产写入仍关。

## 2026-07-21 · GOAL-009 A-022 阶段 C CT 回写

GOAL-009 将 CT-001/003/006/012/014/015 标为覆盖（GOAL-013 阶段 C）。**F-007/F-008 仍 open**；生产写入仍关。GOAL-009 progress **35%**。

## 2026-07-21 · GOAL-013 阶段 C F-007 CT

GOAL-013 完成 CT-001/003/006/012/014/015 可运行用例；progress **55%**。生产门禁默认仍关；F-007/F-008 关闭仍归 GOAL-009。

## 2026-07-21 · CT-007 台账回写

GOAL-012 F-003 residual **closed**（A-004）；GOAL-009 A-021 将 CT-007 标为覆盖。**F-007/F-008 仍 open**；生产写入仍关。GOAL-009 progress **33%**。

## 2026-07-21 · GOAL-013 阶段 B 跨进程幂等

GOAL-013 完成 CT-007 持久化重放与 CT-008 部分冲突；progress **30%**。生产门禁默认仍关。F-007/F-008 关闭仍归 GOAL-009。

## 2026-07-21 · GOAL-013 写入门禁 CT 与跨进程幂等立项

按 GOAL-009 A-020 创建 [GOAL-013-write-gate-ct-durable-idempotency](GOAL-013-write-gate-ct-durable-idempotency/)：补 CT 缺口与跨进程幂等；**生产门禁默认仍关**；F-007/F-008 关闭权仍在 GOAL-009 审视。

## 2026-07-21 · GOAL-009 A-020 写入门禁证据台账

GOAL-009 吸收 GOAL-012 关键路径证据并对照 CT-001～018；**F-007/F-008 仍 open**，缺口清单见 A-020。**未**开放生产写入；进度 **32%**。

## 2026-07-21 · GOAL-012 有界关门

GOAL-012 标为 `done / 100%`（α 实现）。**生产 Web/AI 写入仍关**。关门时 F-003 residual 后由 GOAL-013/A-004 **关闭**（CT-007 持久化）；不构成 F-008 整体关闭或生产放行。

## 路径语义说明（迁移后现时入口）

- **现时 canonical 目标状态根**：本目录 `docs/workspace-001-goal-governance/`（含本 `goal-tree.md` 与平铺 `GOAL-*`）。
- **历史记录**中出现的 `docs/goals/` 路径为 **GOAL-011 迁移前**的事实、设计快照或运行证据叙述；**不要**批量改写已关门目标附件，也**不要**把旧路径当成当前读取根。
- 旧外部仓库仅在无显式工作区根时按 legacy `docs/goals/` 隐式单工作区识别；本仓库不保留并行 `docs/goals/` 真相源。

## 2026-07-21 · 审计响应（GOAL-011 F-001 / GOAL-012 A-001）

`/govern` 响应 GOAL-011 A-003：关闭推荐项 F-001（上节现时入口标注）。响应 GOAL-012 A-001：self 阶段审与台账对齐；F-002/F-004 整改；F-003 接受为 α 门禁内 residual（幂等=进程内）；**生产 Web 写入**仍绑 GOAL-009 F-007/F-008 与 I-003/I-004/I-006。

## 2026-07-21 · 首垂直切片实现立项

GOAL-009 在用户接受设计默认（N1/存储 A/α/打包分栏/SQLite 分层）后关闭 F-005，并创建 GOAL-012 承接路线图 D。GOAL-012 实现配置化产品工作区详情与门禁内的受限执行事实追加；**生产 Web/AI 写入**仍受 GOAL-009 的 F-007/F-008 与 I-003/I-004/I-006 阻断。本仓 dogfood 过程记录不进入发布物（D-011）。

## 2026-07-20 · 阶段 6 Web 工作台规划

GOAL-009 启动 AI 协助的人类目标治理工作台的产品定义与信息发现。它不把只读浏览器定义为产品终态；工作区 canonical 根是运行时真相源。规划台账仍在 GOAL-009；实现交付在 GOAL-012 及后续目标。

## 2026-07-20 · 工作区与共享资料区核心协议

GOAL-010 已完成跨层的核心协议与 Skills 首先适配。它只为 GOAL-009 的 R-003 提供输入，不关闭 F-003/F-004 的产品验证。

## 2026-07-20 · 多工作区目录迁移与共享资料索引

GOAL-011 完成当前仓库到 `docs/workspace-001-goal-governance/` 的迁移与共享资料候选索引骨架。该过程数据为 dogfood，不随 Web/Skills 发布复制给其他项目。

> 所有目标平铺存放在本目录；层级仅通过各目标 `00-meta.md` 的 `parent` 字段维护。  
> **新建、修改状态或调整 parent 后，必须同步更新本文件。**

## 树状结构

> 根目标当前采用“三层交付、一个真相源”：核心方法论与模板、Skills 消费适配器、Web 人类工作台。核心 canonical 模板位于 `docs/templates/goal-folder/`；`skills/templates/goal-folder/` 为分发镜像。

```text
GOAL-001-main-vision · 交付可复用的目标治理方法论、文档协议与消费工具 [active]
├── GOAL-002-project-bootstrap · 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） [done 100%]
├── GOAL-003-skills-practice · 完善 Skills 并在本项目中实践验证 [done 100%]
├── GOAL-004-core-data-model · 实现核心数据模型与 Goal 基础管理 [done 100%]
├── GOAL-005-skills-closed-loop-audit · Skills 治理闭环与交叉审计 [done 100%]
├── GOAL-006-core-methodology-template-productization · 核心方法论、文档协议与 canonical 模板产品化 [done 100%]
├── GOAL-007-information-readiness-governance · 信息就绪与未知项治理 [done 100%]
├── GOAL-008-skills-consumer-adapter-release-consistency · Skills 消费适配器跨宿主/跨版本发布一致性 [done 100%]
├── GOAL-009-ai-assisted-governance-workbench · 规划 AI 协助的人类目标治理 Web 工作台 [active 80%]
├── GOAL-010-core-workspace-shared-materials-protocol · 建立工作区与共享资料区核心协议，并完成 Skills 首先适配 [done 100%]
├── GOAL-011-multi-workspace-directory-migration · 完成多工作区目录迁移与共享资料索引骨架 [done 100%]
├── GOAL-012-first-slice-workspace-detail · 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内） [done 100%]
└── GOAL-013-write-gate-ct-durable-idempotency · 补齐受控写入 CT 缺口与跨进程幂等（生产门禁默认仍关） [done 100%]
```

## 状态总览

| ID | 标题 | Parent | Status | Progress | 路径 |
|----|------|--------|--------|----------|------|
| GOAL-001-main-vision | 交付可复用的目标治理方法论、文档协议与消费工具 | — | active | — | [GOAL-001-main-vision/](GOAL-001-main-vision/) |
| GOAL-002-project-bootstrap | 完成项目初始化（文档体系 + Web 基础框架 + Skills 方向） | GOAL-001-main-vision | done | 100% | [GOAL-002-project-bootstrap/](GOAL-002-project-bootstrap/) |
| GOAL-003-skills-practice | 完善 Skills 并在本项目中实践验证 | GOAL-001-main-vision | done | 100% | [GOAL-003-skills-practice/](GOAL-003-skills-practice/) |
| GOAL-004-core-data-model | 实现核心数据模型与 Goal 基础管理 | GOAL-001-main-vision | done | 100% | [GOAL-004-core-data-model/](GOAL-004-core-data-model/) |
| GOAL-005-skills-closed-loop-audit | Skills 治理闭环与交叉审计 | GOAL-001-main-vision | done | 100% | [GOAL-005-skills-closed-loop-audit/](GOAL-005-skills-closed-loop-audit/) |
| GOAL-006-core-methodology-template-productization | 核心方法论、文档协议与 canonical 模板产品化 | GOAL-001-main-vision | done | 100% | [GOAL-006-core-methodology-template-productization/](GOAL-006-core-methodology-template-productization/) |
| GOAL-007-information-readiness-governance | 信息就绪与未知项治理 | GOAL-001-main-vision | done | 100% | [GOAL-007-information-readiness-governance/](GOAL-007-information-readiness-governance/) |
| GOAL-008-skills-consumer-adapter-release-consistency | Skills 消费适配器跨宿主/跨版本发布一致性 | GOAL-001-main-vision | done | 100% | [GOAL-008-skills-consumer-adapter-release-consistency/](GOAL-008-skills-consumer-adapter-release-consistency/) |
| GOAL-009-ai-assisted-governance-workbench | 规划 AI 协助的人类目标治理 Web 工作台 | GOAL-001-main-vision | active | 80% | [GOAL-009-ai-assisted-governance-workbench/](GOAL-009-ai-assisted-governance-workbench/) |
| GOAL-010-core-workspace-shared-materials-protocol | 建立工作区与共享资料区核心协议，并完成 Skills 首先适配 | GOAL-001-main-vision | done | 100% | [GOAL-010-core-workspace-shared-materials-protocol/](GOAL-010-core-workspace-shared-materials-protocol/) |
| GOAL-011-multi-workspace-directory-migration | 完成多工作区目录迁移与共享资料索引骨架 | GOAL-001-main-vision | done | 100% | [GOAL-011-multi-workspace-directory-migration/](GOAL-011-multi-workspace-directory-migration/) |
| GOAL-012-first-slice-workspace-detail | 实现首个垂直切片：配置化工作区详情与受控执行事实追加（门禁内） | GOAL-001-main-vision | done | 100% | [GOAL-012-first-slice-workspace-detail/](GOAL-012-first-slice-workspace-detail/) |
| GOAL-013-write-gate-ct-durable-idempotency | 补齐受控写入 CT 缺口与跨进程幂等（生产门禁默认仍关） | GOAL-001-main-vision | done | 100% | [GOAL-013-write-gate-ct-durable-idempotency/](GOAL-013-write-gate-ct-durable-idempotency/) |

阶段 6：GOAL-009 `active / 80%`（A-038：**F-002～F-004 closed 有界**；路线图 B finding 有界退出；α 写入门禁已闭环）；GOAL-012/013 `done / 100%`。GOAL-001 仍为 `active`。

## 状态图例

| Status | 含义 |
|--------|------|
| `draft` | 草稿，尚未正式启动 |
| `active` | 进行中 |
| `blocked` | 阻塞 |
| `done` | 已完成 |
| `cancelled` | 已取消 |

## 编号规则速查

1. `GOAL-001` 固定为 Root Goal（`parent: null`）。
2. 新目标从现有最大编号 +1 顺序分配（当前下一个：`GOAL-014`）。
3. 文件夹命名：`GOAL-NNN-short-slug`（英文短横线 slug）。
4. 每个目标必须包含：`00-meta.md`、`01-decision.md`、`02-execution.md`、`03-audit.md`、`attachments/`。
