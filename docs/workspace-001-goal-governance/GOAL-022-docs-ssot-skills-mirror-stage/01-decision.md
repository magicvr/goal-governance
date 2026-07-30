---
id: GOAL-022-docs-ssot-skills-mirror-stage
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.2.0
---

# 决策记录 · GOAL-022

## 信息需求与阶段门禁

与 [00-meta.md](00-meta.md) 信息表同一套 I-00N。I-001～I-003 已由 **D-002** 关闭；I-004 out of scope。

## D-001 · 立项：方法论 SSOT + Skills 镜像 stage 化（2026-07-30）

**决定**：

1. 新建 `GOAL-022-docs-ssot-skills-mirror-stage`，`parent: GOAL-001-main-vision`，status **`active`**。
2. 目标范围：字节一致的方法论/模板/契约镜像改为「**只维护 `docs/` + stage/pack 生成**」。
3. **保留** GOAL-019 D-003/D-004：skills zip **仍内嵌** `core/`，install **仍默认**装到消费仓 `docs/`。
4. 纲领阶段 **A→F**；**不** tag/Release；**不**改 Root/Charter/VP。

**确认来源**：用户指令「开启一个新目标，进行此修改」（2026-07-30）。

## D-002 · 方案冻结 + 立即实现 B～E（2026-07-30）

- **状态**：accepted

**决定**（用户选择题书面确认）：

| 项 | 决议 |
|----|------|
| **I-001** | 生成物**仍提交 git**（`skills/core`、`skills/contracts`）；CI 在测试前 `stage` 并 `git diff --exit-code` 防漂移；pack 前自动 stage |
| **I-002** | **取消手维** `skills/templates/goal-folder`；包内唯一模板分发源 = `skills/core/docs/templates/`；`skills/templates/README.md` 仅指针；契约 `templateSet.mirrorPath` → `skills/core/docs/templates/goal-folder` |
| **I-003** | **手维真正精简** `skills/core/docs/README.md`（不镜像 monorepo 长文/台账）；`vision/README.md` 同为手维例外 |
| **I-004** | **本目标 out of scope**（AGENTS.template / install AGENTS 另跟进） |
| **实现** | 同轮推进 B～E：stage 脚本、pack/CI 挂接、收敛 templates、文档与测试 |

**Stage 白名单（生成）**：

- `docs/architecture/{principles,workspace-protocol,overview,directory-layout}.md` → `skills/core/docs/architecture/`
- `docs/templates/**` → `skills/core/docs/templates/`
- `docs/vision/alignment.md` → `skills/core/docs/vision/alignment.md`
- `docs/contracts/**` → `skills/contracts/**`

**Stage 禁止 / 不覆盖**：

- `tech-stack.md`
- monorepo dogfood vision 实例、workspace 过程树
- `skills/core/docs/README.md`、`skills/core/docs/vision/README.md`

**为什么**：与会话分析一致；用户确认推荐默认并要求立刻实现。

**未选方案**：gitignore 生成物；stage 双写 skills/templates；脚本裁剪 monorepo README；本轮做 AGENTS 生成链。

**确认来源**：用户 ask 四题答案（I-001/I-002/I-003 推荐 + 立刻实现）。
