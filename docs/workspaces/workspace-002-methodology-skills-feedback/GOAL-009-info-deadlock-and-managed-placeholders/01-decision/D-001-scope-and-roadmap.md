---
id: D-001
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: decision
title: 两条反馈纳入同一 R3 子目标，S1 先行
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# D-001 · 两条反馈纳入同一 R3 子目标，S1 先行（2026-09-30）

**状态**：accepted

**触发**：用户 `/govern` 要求在工作区 2 添加一个子目标，解决未知信息门禁死锁，以及指定安装目录后受管占位符导致升级报错。

## 决定

1. 在 Root 纲领 **R3** 内创建 **`GOAL-009-info-deadlock-and-managed-placeholders`**。
2. 编号用区内下一可用 **GOAL-009**；`parent` = `GOAL-001-methodology-skills-feedback-evolution`；不嵌工作区号。
3. FB-010 与 FB-011 由这一个子目标承载。路线图为 S1 核对 → S2 规则语义 / S3 安装升级（S1 之后写集不重叠则可并行）→ S4 验证、审计与消费面交付。
4. **S1 完成前不改**原则正文、AGENTS、编排提示、安装器、update 脚本或 Skills。
5. 本目标自己的信息表不得把「调查才会知道的事实」写成进入调查的门禁。I-001～I-003 只约束后续方案冻结。
6. S2 与 S3 的实施审计模式预定为 **`cross`**（元规则 + 安装/升级兼容）。provider 未指定，因此现在不实施；S1 只读不需要 provider。
7. Root / VP-002 保持 `active`；Root progress 保持 **67%（2/3）**。不把跟踪写进愿景 `roadmap.md`。

## 为什么

- D-008 已确认本区按反馈随时立项。GOAL-008 已 `done`，下一编号是 GOAL-009。
- 两条都是使用中的新摩擦。FB-010 是 P-005 在研究场景被用成死锁；FB-011 是安装结果与升级比较撞车。它们还没有共享到可以立刻改代码的方案。
- 用户要的是一个子目标，不是先拆成两个再开工。

## 待核对假设（不是根因）

立项时只读了现行脚本，**没有**复现升级报错：

- `skills/install.sh` 可用 `--skills-dir` 指定 skills 目录；核心方法论目前写死安装到 `./docs/`（脚本注释与 “Installing core methodology → ./docs/”）。用户说的「同时指定方法论文件夹和 skills 文件夹」是否还有另一条路径，S1 要核对；若没有，这本身就是 I-002 的负结果。
- `skills/update.py` 在受管目标与包内源字节不一致、且未传 `--force-managed` 时，抛出 `managed files have local changes`。若安装把占位符替换进受管文件，字节会和包内源不同。这能否解释用户看到的报错，S1 再证。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 立刻改 P-005 和 update 脚本 | 两条的改法都还没冻结；FB-011 后半句还不完整 |
| 拆成两个并列子目标再开工 | 用户要求一个子目标；写集是否必须拆开要等 S1 |
| 重开 workspace-001 已 done 的 GOAL-007 | 该 Root 已封存；禁止跨区 `parent`。原则正文仍改 canonical，不把旧目标当状态源 |
| 把跟踪写入 VP-002 或愿景 roadmap | 与本区既有决定一致：反馈跟踪留在目标台账 |

## 用户原话中尚未写完的部分

FB-011 的另一支在「尤其是让ai从」处截断。已记录的分叉是：不替换若会损害 AI 认路径，就让 update 更智能；若不会，就改安装侧的给路径方式。截断后的具体做法待用户补全，不阻断 S1。
