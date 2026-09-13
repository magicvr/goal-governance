---
id: D-003
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-003
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-003 · S1 契约冻结：本轮共享不变量与留待各阶段的细案（2026-09-13）

**状态**：accepted

**触发**：I-001～I-004 四路只读盘点完成（证据见 [E-003](../02-execution/E-003-s1-inventory.md) 与 [附件 S1 验收矩阵](../attachments/s1-acceptance-matrix.md)）。A-003 F-006 要求 S1 输出必须**分列**「本轮已冻结的共享不变量/验收契约」与「留待对应阶段冻结的局部细案」，否则执行者会把后续细节提前塞入 S1，或把仅完成盘点解释成所有方案已冻结。

## 决定

### 1. 本轮（S1）已冻结的共享不变量

以下各项为 S2～S5 的共同约束，**任一阶段不得单方面改写**；要改必须回到本目标决策层并留痕。

| # | 共享不变量 | 依据 |
|---|------------|------|
| C1 | **双层层级判定对象是职责与权威，不是节点数量**：判定「组合编排 / 纲领路线图 / 阶段计划 / 意图(VP) / 子目标」时，看决策责任、成功边界与状态权威；数量相同（如一区一 Root 一 VP）本身既不是合法证据也不是失败证据 | A-003 F-007；[alignment §2](../../../../vision/alignment.md) |
| C2 | **VP 不是目标节点**：VP 不得作 `parent`，不得建 Goal 五件套，不得用目标 `03-audit` 替代 Vision Review 台账 | [principles.md:484](../../../../architecture/principles.md)；[alignment.md:81](../../../../vision/alignment.md) |
| C3 | **`{governance_root}` 与根下布局不可改**：`vision/`、`workspaces/workspace-*`、`goal-tree.md`、目标五件套形状、`contracts/` 的相对布局固定；仓外路径 fail closed | [alignment.md §0](../../../../vision/alignment.md)；[workspace-protocol.md §4b](../../../../architecture/workspace-protocol.md) |
| C4 | **治理必达入口集合不变**：`vision` / `vision-audit` / `govern` / `audit` 四入口；新增便利入口（如 `commit`）不得进入必达集、不得进入完整安装 MUST、不得替代 `/govern` checkpoint | [VP-004 入口面](../../../../vision/plans/VP-004-mcp-file-dual-channel-delivery.md)；[D-002 §4](D-002-a001-response.md) |
| C5 | **安全暂存契约共通**：只 `git add -- <owned paths>`；禁止 `git add -A` / `git add .`；owned path 含任务开始前用户改动或与无关改动不可分离时停止并报告，不覆盖、不回退、不夹带；checkpoint 是恢复点，不是审计/实现/发布通过证据 | [principles.md P-002](../../../../architecture/principles.md) |
| C6 | **canonical 改动必须同轮 stage 镜像**：`docs/architecture/{principles,workspace-protocol,overview,directory-layout}.md`、`docs/templates/**`、`docs/vision/alignment.md`、`docs/contracts/**` 改动后同轮 `python scripts/stage_skills_mirrors.py`、`--check` 通过，并把 `skills/core`、`skills/contracts` 变更纳入同一提交 | AGENTS §8c |
| C7 | **消费仓兼容优先于形式洁癖**：S2～S5 的任何新规则不得让「已按前版安装的消费仓」在升级瞬间被判**不完整安装**而冻结治理推进；新增文件/字段一律按 non-MUST + legacy 回退处理，除非用户另行书面裁决 | 见 [D-005](D-005-s3-consumer-compat.md) |

### 2. S1 退出条件与本轮覆盖

| S1 退出要求 | 本轮结果 | 证据 |
|-------------|----------|------|
| I-001～I-004 完成当前阶段收集 | 四项均 `verified` | [D-004](D-004-s1-inventory-acceptance.md) 逐项结论；[附件](../attachments/s1-acceptance-matrix.md) 证据列 |
| 验收矩阵含可复现路径、责任边界证据、验收人/审视方式、各阶段证据路径 | 已落盘 | [附件 S1 验收矩阵](../attachments/s1-acceptance-matrix.md) |
| 列出 S4/S5 owned paths 并决定并行或 S4→S5 | owned paths 已列；判定 **S4→S5 串行** | [D-006](D-006-s4-s5-owned-paths-and-serial-decision.md) |
| **不**要求 I-005 provider 或 independent 输出 | 遵守；I-005 已由用户书面指定（本轮另记），其输出仍在 S6 | [D-002 §1](D-002-a001-response.md) |

### 3. 留待对应阶段冻结的局部细案（不得在 S1 假装已冻结）

| 阶段 | 仍需在**该阶段**冻结的细案 | 依赖的信息项 | 期限 / 证据要求 |
|------|---------------------------|--------------|-----------------|
| S2 | 判定谓词的最终措辞与落点；probe/corpus 的执行方式（真实宿主探针 vs 静态断言）；`总路线图` 术语映射的正式措辞；VP 内阶段结构的命名归类 | I-001（已 verified，结论待 S2 兑现） | S2 方案冻结时；正反例通过阈值见附件 §3 |
| S3 | 权威模型落地形态（A1 索引承载投影）与遗留列清理、兼容读取顺序、`standalone-bootstrap` 整文件复制缺陷的修法 | I-002（已 verified；模型选择见 [D-005](D-005-s3-consumer-compat.md)） | S3 方案冻结时；重复信息「不存在」需可核验 |
| S4 | `AGENTS.md` / `docs/` 共存模型的最终选型（候选 A～E 见盘点报告）；负例测试的实现与平台覆盖；大小写碰撞与非原子写入的处理 | I-003（盘点完成，**选型仍由用户裁决**） | S4 方案冻结前须用户裁决；负例测试须可复现 |
| S5 | `/commit` 命令契约（参数、输出、禁用语义）；「默认安装但不入必达集」的契约表达位；宿主探针与证据 | I-004（盘点完成，命令形状待冻结） | S5 方案冻结时；负例 fail closed 须可复现 |
| S6 | 版本、tag/revision、资产清单、回归矩阵、cross 覆盖面、consumer vs producer 证据归属 | I-006（open） | S6 前冻结；F-005 绑定 |

### 4. S1 的审计模式

S1 为只读盘点 + 文档冻结，不触及元规则正文，按 P-003 定为 **`self`**；因要闭合 A-001 的 required finding F-002/F-003，另安排一次 **independent 复审**（provider = 本地 grok build / grok-4.6 / reasoning-effort high，用户本轮书面指定）。S2/S3 的 `cross` 模式不变（[D-001 §6](D-001-scope-and-roadmap.md)）。

## 为什么

- A-003 F-006 直接要求这种分列；不区分「已冻结」与「待冻结」，S1 就会变成两种错误之一：要么把未定型的模型写成方案（编造），要么把已可复用的共同约束也推迟（返工）。
- C1～C6 全部有 canonical 依据，属既有规则的显式化，不是新造规则；因此可以在 S1 冻结而不越权。
- C7 来自用户本轮裁决，见 D-005；它把「消费仓兼容」从各阶段的临时考虑提升为共同不变量。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 在 S1 直接冻结 S2～S5 的方案细节 | 盘点是事实，选型是决策；把候选写成方案会制造不可审计的既成事实（A-003 F-006 明确点名的错误） |
| 只写「S1 已完成盘点」，不列已冻结项 | 同样违反 F-006 的另一半：后续阶段将无共同约束，可能各自改协议 |
| 把 S1 审计模式定为 `cross` | S1 不改元规则正文，按 P-003 风险分级无 `cross` 依据；`cross` 留给 S2/S3 与 S6 |
| 等到 S2 再指定 provider | D-002 §1 已冻结「S2 实施前指定」；用户本轮已指定，提前落盘可避免 S2 被身份门禁挡住 |

## 影响

- 本决定冻结共享不变量 C1～C7，并显式列出各阶段待冻结细案。
- 00-meta 路线图 S1 退出条件、I-001～I-004 状态、`progress` 随之更新。
- A-001 F-002（验收载体）与 F-003（owned paths）在本轮获得可核对产物，闭合判定见 [D-004](D-004-s1-inventory-acceptance.md)。
