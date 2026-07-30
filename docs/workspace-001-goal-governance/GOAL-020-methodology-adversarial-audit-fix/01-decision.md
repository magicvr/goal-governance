---
id: GOAL-020-methodology-adversarial-audit-fix
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-29
updated: 2026-07-29
version: 0.3.0
---

# 决策记录 · GOAL-020

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同一套 I-00N；阶段 D 前须闭合 I-001 / I-002（或 residual）；阶段 E 前评估 I-003。

## D-001 · 立项目标作为对抗审与纠错主台账（2026-07-29）

**决定**：

1. 新建 `GOAL-020-methodology-adversarial-audit-fix`，`parent: GOAL-001-main-vision`，status `active`。
2. **正式审计意见主落点**为本目标 `03-audit.md`（可链 `attachments/`），**不**向已 `done` 的 GOAL-006 追加本轮 required。
3. 默认**不**强制同步写 `docs/vision/reviews.md`；仅当纠错触及 Charter 成功边界/「方向已稳」且用户或 `/vision` 确认时，再开 `VRev` 或 Charter editorial/strategic。
4. 本目标定位为路径 D 下用户授权的**协议/方法论质量**单点工作，不重开阶段 7，不宣称 Root 终态。

**为什么**：

- GOAL-006 已正式 close-out；死后加 required 破坏 P-003 与历史关门语义。
- 对抗审 + 多阶段纠错范围大，需要独立生命周期、纲领路线图与成功标准。
- 主台账单一，避免 Goal 台账与 Vision Review 双份空转。

**未选方案**：

- **挂 GOAL-006 追加 A-00N**：简单，但污染已关门目标。
- **只写 VRev、不建 Goal**：愿景台账装不下模板/bootstrap 类实现纠错，且响应路径应走 `/govern`。
- **拆成多个子目标再审**：违反「先审计落盘再按阶段纠错」；先本目标纲领，必要时再拆。

**确认来源**：用户确认「新目标作为更合理落盘方向」后指令「立项」。

## D-002 · 纲领五阶段与首轮审计同轮落盘（2026-07-29）

**决定**：

采用 00-meta 路线图阶段 A→E（审计落盘 → 定义/权威面 → 模板/协议 → 策略裁决 → 回归关门）。立项当轮将会话中的对抗性审计以 **A-001 / `source: independent`** 写入本目标，作为阶段 A 完成证据；**不**因 A-001 自动改 status 为 done，也不自动执行 B–E 文档修改。

**为什么**：立项目的即承接该审计；同轮落盘避免「空目标 + 审计仍在聊天」。响应与纠错仍归后续 `/govern` 与用户 P-004（I-001/I-002 等）。

**未选方案**：只建五件套、审计另开一轮——增加一次往返，无额外独立性收益（同会话上下文）。

## D-003 · F-001～F-004 纠错并保留阶段 D 门禁（2026-07-29）

**决定**：

1. 按用户「先修 F-001～F-004」指令：F-001 模板重写；F-002 谓词最小充分条件写入 principles；F-003 保证等级写入 principles；F-004 MUST 表写入 alignment 并同步 checklist/standalone。
2. 阶段 B/C 的 required 范围完成；F-005 与 I-001/I-002 保持开放，等待 P-004 书面裁决。
3. A-001 为独立审计；A-002 仅是响应记录，不冒充同 scope self audit。

**为什么**：先闭合可直接修正的 required，再把 progress 与 sandbox 的方法论取舍留给用户裁决，避免编排器静默决定。

**未选方案**：直接关闭 F-005/F-006；静默补 self audit；向已关门 GOAL-006 回写 required。

**确认来源**：用户明确要求先修 F-001～F-004。

## D-004 · 阶段 D 策略裁决：派生 progress、移除 sandbox、阶段 E 自审（2026-07-29）

- **状态**：accepted

**决定**：

1. `progress` 保留为**非权威派生展示**：仅由目标内显式路线图/计划检查点确定性计算；默认等权，显式权重可覆盖。它不放行阶段、不关闭 finding、不覆盖 I-00N 或 `status`，也不进入愿景层。F-005 走 `fixed`。
2. 当前规范**全面移除 sandbox 支持**：`vision_role` 仅允许 `primary` / `delivery`；高不确定探索按 P-005 建有界信息收集阶段/目标，需独立树时使用正常 delivery 工作区。F-006 走 `fixed`。
3. 同 scope self audit 安排在**阶段 E**，覆盖阶段 A～D 的全部修正；A-002/A-003 仍只作为响应记录。
4. I-001、I-002 以本决策关闭；I-003 经评估关闭为 `verified · no Charter change`：本轮只收紧实现层方法论与角色枚举，不改变 Charter 的目的、成功边界或非目标，不触发 strategic/re-align/VRev。
5. F-007～F-011 保持 recommended open，进入阶段 E 评估；不阻断阶段 D 完成。

**为什么**：派生规则消除手填百分比形成第二状态通道；移除未被框架实际采用的 sandbox 角色，比保留空心标签或新增差异化门禁更清晰。阶段 E 统一自审能覆盖最终文档栈，避免在已知修正尚未完成时重复审计。

**未选方案**：删除所有目标 progress；设置“开放 required 时百分比上限”；仅在 GOAL-020 排除 sandbox；保留 sandbox 并接受 residual；现在立即做同 scope self audit。

**影响与后续**：更新 canonical 权威、模板、Skills core/宿主入口与测试；同步 GOAL-020/Root/goal-tree。阶段 E 运行回归并追加 self audit，之后再评估关门。

## D-005 · 接受 A-004 建议并确认 GOAL-020 关门（2026-07-29）

- **状态**：accepted

**决定**：

1. 接受 A-004 `self / close-out / pass` 建议，将 GOAL-020 从 `active` 改为 `done`；派生 progress 保持 `100%`。
2. F-010 保留为 `recommended / open / non-blocking follow-up`，不改写为 fixed、accepted-residual 或 user-overruled；它不影响当前实例对齐，也不阻断本目标成功标准。
3. 本次不追加独立 targeted 复审；按框架默认 L0 关门。未来仍可用 `/audit` 做只读复审。
4. 不重开 GOAL-006，不修改 Root/Charter/VP 状态，不开启阶段 7。

**为什么**：A～E 全部完成；A-004 已核对 required=0、到期信息项=0、成功标准与回归证据通过。用户在 `/govern` 关门裁决中明确选择“确认关门”。

**未选方案**：先独立复审；保持 `active / 100%`；在本次关门中静默收紧 F-010 的 primary/strategic 规则。

**后续**：若要处理 F-010，另走 `/govern` P-004 裁决并更新 alignment/tests；不得借本次 `done` 宣称该 recommended 已关闭。
