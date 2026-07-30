---
id: GOAL-021-skills-release-chain-hardening
title: 加固 Skills「规则→分发→证据→发布」执行链
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.1.0
progress: 14%
---

# GOAL-021 · 加固 Skills「规则→分发→证据→发布」执行链

## 概述

闭合一条独立对抗审对 **Skills 执行链** 的发现：核心原则本身总体自洽，但「规则 → 分发 → 证据 → 发布」存在 **4 项 P1** 与 **1 项 P2** 风险；在修复前，**不建议**发布新的 Skills 包，或把当前运行证据当作充分的发布证明。

本目标是路径 D（[D-024](../GOAL-001-main-vision/01-decision.md#d-024--a-015-f-008-路径-d仅维护发版协议不关-root2026-07-28)）下用户授权的 **Skills 分发/证据/门禁质量** 单点子目标：在目标生命周期内落盘意见、按阶段 fixed，并回归验证。

**不**重开已 `done` 的 GOAL-008 / 018 / 019 / 020 的历史关门；**不**自动改 Charter/VP/Root status；**不**开启阶段 7。

## 范围

### 在范围内

1. 将本轮执行链对抗审意见正式写入本目标 `03-audit.md`（A-00N + findings）。
2. 按建议顺序修复：
   - **F-001**：core 模板 README mirror 语义漂移（canonical 0.6.0 vs mirror 0.5.0）+ 全文件 hash/语义一致性测试。
   - **F-002**：运行证据不可仅凭「退出码 0 + 任意 marker」伪造；结构化/版本绑定断言 + 负例。
   - **F-003**：Skills 打包拒绝 symlink 或对 `resolve()` 做根目录 containment；Linux CI 负例。
   - **F-004**：P-006 fail-closed 在通用验证器完整执行（active Charter、逐 plan `vision_ref`、取消通用 opt-out、真实 Root/canonical）。
   - **F-005**（P2）：工作区结构校验（非空 id、真实 Root）与安装器 `--non-interactive` / `--force` / `--dry-run` 语义。
3. 相关回归：docs / skills / scripts 测试与负例覆盖；修复后**不**自动宣称可发版——发版仍须 Root 路径 D 授权与 release evidence。

### 不在范围内

- 追溯否定 GOAL-008/018/019 历史关门证据，或宣称既有 runtime 证据「已造假」。
- Web 产品 residual（R-009-X）、阶段 7、Charter strategic 改版。
- 无授权自动 `git tag` / GitHub Release。
- 把 progress% 当作放行/关闭 finding 的依据。

## 成功标准

- [ ] 对抗审正式意见已落本目标 `03-audit.md`（`A-00N` + `source`）；长文可链 `attachments/`。
- [ ] **F-001～F-004**（required）均已按 `fixed` / `accepted-residual` / `user-overruled` 合法闭合，并有决策或响应留痕。
- [ ] **F-005** 已闭合，或经用户书面 `accepted-residual` / `user-overruled` 并写明范围与复审触发。
- [ ] 负例测试覆盖：core mirror 漂移、仅打印 marker 的 runtime 证据、打包 symlink 逃逸、P-006 三类反例（至少）。
- [ ] 相关 docs/skills/scripts 回归通过；修复说明可指回本目标执行/审计证据。
- [ ] 自审或独立复审确认 required=0 后，经用户确认方可 `done`（不自动关门）。

## 纲领路线图（P-001）

| 阶段 | 内容 | 完成标记 |
|------|------|----------|
| **A · 审计落盘** | 执行链对抗审写入本目标台账；明确 P1/P2 与影响门禁 | [x] A-001（2026-07-30） |
| **B · core mirror** | 同步 `skills/core/docs/templates/README.md`；全文件 hash/语义一致性测试 | [ ] F-001 |
| **C · 运行证据** | 结构化/版本绑定断言；「只打印 marker 必须失败」负例；兼容性消费侧不认伪 pass | [ ] F-002 |
| **D · 打包围堵** | 拒绝 symlink 或 containment；Linux CI 负例 | [ ] F-003 |
| **E · P-006 验证** | Charter 须 active；逐 plan `vision_ref`；删除通用 `require_plans=False` opt-out；真实 Root/canonical | [ ] F-004 |
| **F · 安装/工作区可复现** | 非空 workspace id、存在的 Root；install 非交互失败 / force / dry-run | [ ] F-005 |
| **G · 回归与关门** | 全量相关测试 + self（+ 可选 independent）关门审；用户确认 status | [ ] |

纲领阶段 **串行**；同一阶段内可并行改多文件。大块若需独立证据再拆子目标（非默认）。

**派生 progress**：A～G 共 7 个等权检查点，当前 **1/7 ≈ 14%**。progress 仅为展示；**不得**放行阶段、关闭 finding、覆盖信息门禁或推导 `done`。

## 信息就绪与未知项（P-005）

| ID | 级别 | 所需信息 / 问题 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | non-blocking | 运行证据「结构化断言」的最小 schema：字段集合、是否强制宿主能力探测、与现有 `runtime-evidence.schema.json` 兼容策略？ | 阶段 C 方案冻结 | 阶段 C 前 | 读现有 schema/capture 脚本；必要时 D-00N 书面定案 | open | 实施时可边探边冻；不阻断阶段 B | 待阶段 C |
| I-002 | non-blocking | F-005 是否必须进本目标关门，还是 P1 全闭后可 residual 延后？ | 阶段 F / 关门 | 阶段 G 前 | 用户 P-004 若要 residual | open | 默认 **纳入本目标路线图 F**；若用户书面 residual 再改 | 默认 in-scope |
| I-003 | non-blocking | 修复后是否立即申请新 Skills tag/Release？ | 发版（Root 路径 D） | 本目标 done 后 | Root D-0xx 授权；非本目标默认交付 | open | **本目标不授权发版**；仅消除「不建议发布」的 P1 阻断 | 见 Non-goal |

## 阶段门禁

- **阶段 B～E**：对应 F-001～F-004 为 **required**；未合法闭合不得宣称「可发版执行链已稳」或进入阶段 G 关门。
- **阶段 C**：I-001 宜在改断言语义前书面/决策冻结（non-blocking：可先写 failing 负例再定 schema）。
- **阶段 G**：F-001～F-004 closed；F-005 closed 或合规 residual；相关回归绿；建议至少一次 self close-out。

## 父目标与对齐

- **Parent**：[GOAL-001-main-vision](../GOAL-001-main-vision/00-meta.md)
- **工作区**：`workspace-001-goal-governance`
- **关系**：Skills 维护波次之后的 **执行链安全/一致性** 加固；与 GOAL-008（发布一致性）、GOAL-018（打包）、GOAL-019（消费骨架）、GOAL-020（方法论对抗审）互补，不互相否定历史关门。

## 备注

- 正式审计意见**只**写本目标 `03-audit.md`。
- 正面已验证项（architecture/core 排除 tech-stack 一致、contracts 一致、现有绿测）见 A-001 成果表；绿测不覆盖本轮负例。
