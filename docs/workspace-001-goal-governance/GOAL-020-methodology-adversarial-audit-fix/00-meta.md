---
id: GOAL-020-methodology-adversarial-audit-fix
title: 核心方法论对抗性审计与纠错
status: active
parent: GOAL-001-main-vision
created: 2026-07-29
updated: 2026-07-29
version: 0.2.0
progress: 80%
---

# GOAL-020 · 核心方法论对抗性审计与纠错

## 概述

对 `docs/` 内**愿景–目标治理框架的核心方法论**做对抗性审计，并把意见与纠错收敛在本目标生命周期内：定义层漏洞、模板与原则漂移、权威面多头、完整安装定义分裂、progress/sandbox 等可被「合规章法」绕过的缝。

本目标是用户授权的**路径 D 单点 residual / 协议质量**子目标（见 Root [D-024](../GOAL-001-main-vision/01-decision.md#d-024--a-015-f-008-路径-d仅维护发版协议不关-root2026-07-28) 单点 residual 条款），**不**重开 GOAL-006 阶段 4 关门，**不**自动改 Charter，除非用户确认 editorial/strategic class。

## 范围

### 在范围内

1. 对抗性审计并落盘：`principles`、`workspace-protocol`、`alignment`、愿景入口、`templates`、`standalone-bootstrap`、`docs/README` 等权威面。
2. 按 P-003 三路径响应本目标 `03-audit` 中的 findings；优先 fixed。
3. 纠错：可判定谓词、保证等级、Minimal Complete Install 统一表、`03-audit` 模板 A-00N 骨架、并行表述、§2.6 锚点、progress/sandbox 策略等（以审计台账为准）。
4. 触及 Charter 成功边界/「方向已稳」主张时，经 `/vision` 决定是否另写 `VRev` 或 editorial；**默认主台账仍是本目标**。

### 不在范围内

- 追溯否定 GOAL-006 A-005 在 2026-07-19 的阶段 4 关门证据。
- Skills 多宿主 runtime 发版、Web 产品 residual（R-009-X）、阶段 7 开道。
- 静默改 Charter strategic 或宣称 Root `done`。

## 成功标准

- [x] 对抗性审计正式意见已落本目标 `03-audit.md`（`A-00N` + `source`），长文可链 `attachments/`。
- [x] 本目标开放 **required** findings 均已按 `fixed` / `accepted-residual` / `user-overruled` 合法闭合，并有决策或响应留痕（A-002/A-003）。
- [x] 与 required 对应的 core 文档/模板纠错已落盘；canonical 模板与 Skills/core 镜像同步，相关回归通过。
- [x] Minimal Complete Install 在 bootstrap / checklist / alignment 三处一致可核对。
- [ ] 关门审计确认：不对外宣称「核心方法论文档层已关门级稳健」除非本目标 required 已闭合；不重开 GOAL-006。

## 纲领路线图（P-001）

| 阶段 | 内容 | 完成标记 |
|------|------|----------|
| **A · 审计落盘** | 对抗审意见写入本目标台账；明确 required/recommended 与影响门禁 | [x] A-001（2026-07-29） |
| **B · 定义与权威面** | 谓词最小充分条件、保证等级、权威冲突消解、完整安装 MUST 表 | [x] F-002～F-004 required（2026-07-29） |
| **C · 模板与协议对齐** | `03-audit` A-00N 骨架、串行/并行表述、§2.6 标题化、I/A 交叉引用约定等 | [x] F-001 required + canonical/mirror 对齐（2026-07-29） |
| **D · 策略裁决** | progress% 删或门禁化；sandbox 差异化或降级；primary/strategic impact 软规则收紧（P-004） | [x] D-004：派生 progress + 移除 sandbox（2026-07-29） |
| **E · 回归与关门** | 文档自洽抽检 + 相关 docs/tests；self（+ 可选 independent）关门审计 | [ ] |

纲领阶段 **串行**；同一阶段内可并行改多份 docs。大块纠错若需独立证据，再拆子目标（非默认）。

**派生 progress**：当前 A～D 共 4/5 个等权纲领检查点完成，故展示 `80%`。该数值不表示阶段 E 已放行、recommended 已关闭或目标可 `done`。

## 信息就绪与未知项（P-005）

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 用户对 progress%：删除 vs 门禁化上限？ | 阶段 D 方案冻结 | 阶段 D 前 | P-004 书面裁决 | closed (fixed policy) | 用户选择保留非权威展示；D-004 将其收敛为显式检查点派生规则 | D-004；principles P-001「派生进度展示」 |
| I-002 | required | sandbox：补差异化门禁 vs 降为非规范备注？ | 阶段 D 方案冻结 | 阶段 D 前 | P-004 书面裁决 | closed (removed) | 用户选择全面移除；角色枚举收缩为 primary/delivery | D-004；alignment 0.5.0 / workspace-protocol 0.7.0 |
| I-003 | non-blocking | 本轮 required 是否触发 Charter editorial（保证等级/成功边界措辞）？ | 宣称方向已稳 / VP 叙事 | 阶段 E 前 | 阶段 B/C 后评估；必要时 `/vision` | closed (verified: no Charter change) | 方法论与角色枚举收紧，不改 Charter 目的/边界/非目标 | D-004；不触发 strategic/re-align/VRev |

## 阶段门禁

- **阶段 D**：I-001 / I-002 已由 D-004 书面裁决并实施，门禁解除；F-005/F-006 响应见 A-003。
- **阶段 E**：用户已按 P-004.1 选择在阶段 E 做覆盖 A～D 的同 scope self audit；该审计完成前不关门。

## 父目标与对齐

- **Parent**：[GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
- **工作区**：`workspace-001-goal-governance`
- **关系**：承接 P-006 落地后的方法论质量债；与 GOAL-006（历史产品化关门）并列，不互相否定。

## 备注

- 正式审计意见**只**写本目标 `03-audit.md`；不向 GOAL-006 追加死后 required。
- 愿景层 `VRev` 仅在用户/`/vision` 确认需要时补写，避免双台账空转。
