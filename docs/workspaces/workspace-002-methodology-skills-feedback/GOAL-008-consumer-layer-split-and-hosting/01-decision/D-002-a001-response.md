---
id: D-002
goal: GOAL-008-consumer-layer-split-and-hosting
status: accepted
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-002 · 响应 A-001：唯一化闸门、并行写集与 `/commit` 边界（2026-09-13）

**状态**：accepted

**触发**：用户书面要求响应独立审计 [A-001](../03-audit/A-001-roadmap-design-plan.md)（Codex `audit` · `conditional` · F-001～F-005 required）。无意见冲突；路径为 `fixed`（能当场改的）或继续收集（不能假装已有产物）。

## 决定

1. **F-001 闸门唯一化（本轮 `fixed`）**
   - **S1 退出**：I-001～I-004 完成当前阶段收集，并产出 F-002 所要求的验收载体骨架。S1 **不**要求 I-005 independent 输出，也**不**把 provider 指定当作 S1 退出条件。
   - **S2 实施前**：I-005 必须已由用户书面指定 independent provider；未指定不得开始 S2。provider 失败、超时、不可用或无可核对输出时不得静默降级，S2 保持阻断。
   - **independent 可核对输出**：S6 `cross` close-out 才要求到位（self + 指定 provider），不是 S1 退出条件，也不是 S2 开工的第二份审计前置。
   - 取代 D-001 §6 中「I-005 在 provider 指定前阻断 S2」与 00-meta「S1 退出含 I-001～I-005」并存的两种读法。

2. **F-002 验收载体（保持 open）**
   - 采纳审计列出的可重复字段，写入各阶段退出条件。
   - 实际矩阵、probe/corpus、正反例、通过阈值、权威落点核验、负例测试仍是 **S1 产物**。F-002 在这些产物落盘前保持 required/open，继续阻断 S2/S3/S4 方案冻结与放行。

3. **F-003 并行写集（保持 open；取消无条件并行）**
   - 取代 D-001 §4「S4/S5 可并行」的无条件读法。
   - S1 必须列出 S4/S5 owned paths。写集重叠，或 S5 依赖 S4 共存模型 → **S4→S5 串行**。仅当写集可分离时才并行，并同时写明分支边界、合并顺序、冲突处理和集成验证责任。
   - F-003 在 owned paths 与并行/串行决定落盘前保持 required/open，阻断 S4/S5 并行授权。

4. **F-004 `/commit` 便利可选（本轮 `fixed`）**
   - 「默认提供」只表示：在已支持的消费宿主上**默认安装/可调用**便利入口。
   - **不得**把 `/commit` 升格为完整治理安装 MUST、治理入口必达集，或 `/govern` checkpoint 的替代物。
   - 与 FB-009 兼容：消费仓仍能默认用到该命令；缺少它不使安装不完整，也不阻断 `/govern`。
   - I-004 其余命令形状、宿主覆盖与 fail-closed 负例仍待 S1 收集；本条只冻结治理边界。

5. **F-005 发布范围（保持 open）**
   - S6 退出条件必须能重现：版本、tag/revision 关系、资产清单、回归矩阵、cross 覆盖面、consumer vs producer 证据归属。
   - I-006 仍 open。F-005 在 I-006 冻结前保持 required/open，阻断 S6 发布。

6. **不**因本响应改 `status` / `progress` / 检查点完成态。S1 只读盘点可继续；S2～S6 对应门禁在相关 finding 合法闭合前保持关闭。

## 为什么

- 用户点名响应 A-001，且五条 required 同向、无冲突，不触发 P-004.2。
- F-001、F-004 是路线图/边界措辞缺口，可在决策层当场唯一化，满足 `fixed` 的可核对修正。
- F-002、F-003、F-005 要求尚未存在的产物（矩阵、写集、版本基线）；把它们标成 `fixed` 或 `accepted-residual` 会伪装完成。保持 open 并收紧退出条件，才是合法响应。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 五条全部标 `fixed` | F-002/F-003/F-005 尚无产物，属于编造闭合 |
| 五条全部 `accepted-residual` / `user-overruled` | 用户未书面接受残余或驳回；编排器不得代裁 |
| 采用「provider 选择 + independent 输出都作为 S1 退出」 | 会把 S6 才需要的 cross 输出提前到立项后第一阶段，成本与 A-001 已完成的 design-plan 审计重复 |
| 维持 S4/S5 无条件并行 | 安装器/updater 写集明显可能重叠，正是 F-003 要挡的 |
| 把 `/commit` 写入完整安装 MUST | 与 VP-004「便利可选 / 与治理正交」冲突；用户选择响应本审计即走 `fixed` 而非 overruled |

## 影响

- 00-meta 路线图退出条件、I-004/I-005/I-006 行、成功标准第 4 条。
- D-001 §4、§6 闸门读法以本决定为准；D-001 其余立项范围仍有效。
- 审计响应见 A-002。
