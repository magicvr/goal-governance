---
id: D-001
goal: GOAL-008-consumer-layer-split-and-hosting
status: accepted
created: 2026-09-13
updated: 2026-09-13
version: 0.2.0
---

# D-001 · 将四项消费仓痛点纳入同一 R3 大目标（2026-09-13）

**状态**：accepted（§4 无条件并行、§6 I-005 闸门措辞由 [D-002](D-002-a001-response.md) 唯一化；其余范围决定仍有效）

**触发**：用户书面提交四项消费仓质量框架痛点，并要求在 workspace-002 新建子目标承载治理上下文。

## 决定

1. 创建 **`GOAL-008-consumer-layer-split-and-hosting`**，父目标为 `GOAL-001-methodology-skills-feedback-evolution`，初始状态 `active`，挂在 Root 纲领 **R3**。
2. 将用户列出的四项问题登记为已确认反馈 **FB-006～FB-009**；这证明问题已被提交，不证明根因、方案或实现已经验证。
3. 将它们放在一个 P-001 大目标内统一治理，因为共同表现为「消费仓质量框架在双层语义与宿主占用上失效」，并横跨原则、愿景工件、安装面与 Skills 入口。
4. 采用 S1 先行、S2→S3 串行、S4/S5 可并行、S6 汇总的路线图。S1 完成前不改协议正文、安装器或 Skills 实现。
5. 不预先冻结以下实现选择：判定谓词的落点与措辞、VP 跟踪权威文件、`AGENTS.md`/`docs/` 共存模型、`/commit` 与 checkpoint 的命令形状。
6. S2/S3 触及元规则与协议，关门审计模式为 **`cross`**（self + 指定 provider independent）。I-005 在 provider 指定前阻断 S2 实施；provider 失败不得静默降级。
7. required finding、意见冲突、residual / overruled 与信息冲突仍保留 P-004；减少 AI 混淆不得被实现为静默跳过愿景层或把 VP 写成可执行子目标。

## 为什么

- 四项均来自消费仓实际使用，直接服务 VP-002 与 Root R3 的「按反馈随时立项」。
- 至少四个可独立验收的交付块，且跨越协议命名、愿景工件、安装占用与命令入口，满足 P-001「尚不可直接执行 → 先写纲领路线图」。
- 先统一冻结双层语义与宿主共存不变量，可避免各自局部修补后互相冲突（例如只加 `/commit` 却仍把 VP 当子目标；或只改 roadmap 文案却仍覆盖消费仓 `AGENTS.md`）。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 立刻机械创建四个子目标 | S1 尚未冻结共享契约、命名谓词和验收矩阵；会制造编号与边界返工 |
| 本轮直接改 principles / roadmap / install / 新增 skill | 信息项 I-001～I-004 仍 open；边分析边改会造成不可审计的既成事实 |
| 把 FB-006/FB-007 当成「只改几句提示词」的小维护 | 用户指出双层拆分已失去意义，属于协议判定缺口，不是文案润色 |
| 重开 GOAL-003 或 GOAL-006 继续追加 | 上两目标已关门；本批问题是新的双层语义与宿主占用面，不是 runtime evidence、ledger 或 `{governance_root}` 相对化的回归 |
| 把四项写进愿景 `roadmap.md` 跟踪表 | 这正是 FB-007 要消除的膨胀；跟踪应留在本区目标台账 |
