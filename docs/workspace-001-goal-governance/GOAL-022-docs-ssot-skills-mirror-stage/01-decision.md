---
id: GOAL-022-docs-ssot-skills-mirror-stage
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.3.0
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

## D-003 · 响应 A-001：F-001/F-002 residual + F-003 fixed；阶段 F 关门（2026-07-30）

- **状态**：accepted
- **确认来源**：用户 `/govern` 选择题书面确认（F-001 residual / F-002 residual / F-003 fixed Root 现行说明 / 闭合后 self close-out → done）

**决定**：

| Finding | 闭合路径 | 决议 |
|---------|----------|------|
| **F-001** | `accepted-residual` **R-022-ORPHAN-PRUNE** | 不在本目标实现 stage orphan prune。当前工作树 orphans=0；接受机制缺口。 |
| **F-002** | `accepted-residual` **R-022-INSTALL-TEMPLATES-COPY** | 不改 install `-All` 物化 `skills/templates/` 行为。包内权威源仍为 `core/docs/templates`；`-All` 输出为派生副本。 |
| **F-003** | `fixed` | 更新 Root 现行说明（GOAL-001 `00-meta` 三层交付句 + D-007/D-008 **现时注**）；历史审计节保留原貌。 |
| **阶段 F** | 关门 | 自审 A-003 close-out → status **`done`**；progress 6/6=100%；**不** tag/Release；**不**改 Root/Charter/VP status。 |

### Residual 明细（用户书面接受）

#### R-022-ORPHAN-PRUNE（F-001）

| 字段 | 值 |
|------|-----|
| **级别** | non-blocking |
| **范围** | `stage_skills_mirrors` 仅校验/复制 `planned_pairs`；不自动删除「canonical 已删、镜像仍在」的孤儿文件（`tech-stack` 与 legacy `skills/templates/*` 特例除外） |
| **风险** | 日后从 `docs/templates/**` / `docs/contracts/**` / 白名单 architecture 删除文件时，镜像侧可能残留；`--check` 不会因此失败 |
| **缓解 / 操作约定** | 删除 canonical 后须**人工**删除对应镜像路径，并跑 `stage --check` / CI；或另立 follow-up 实现白名单树 orphan prune |
| **复审触发** | 再出现 orphan 计数 > 0；或做大规模删除迁移；或用户要求实现 prune |
| **状态** | open · residual accepted |

#### R-022-INSTALL-TEMPLATES-COPY（F-002）

| 字段 | 值 |
|------|-----|
| **级别** | non-blocking |
| **范围** | `skills/install.{sh,ps1}` 的 `-All`/`--all` extras 仍将 `core/docs/templates` 复制到 `$SkillsDir/templates` |
| **风险** | 消费仓或 monorepo 对 `./skills` 跑 `-All` 可再造可手改副本，冲掉 monorepo 指针 README 策略 |
| **缓解 / 操作约定** | 包内权威 = `skills/core/docs/templates`；`skills/templates` 派生副本**禁止手维**、**不得**反向定义协议；**禁止**在 monorepo 把对 `./skills` 的 `-All` 当镜像同步手段 |
| **复审触发** | 消费方/维护者把 `skills/templates` 当上游修改；或产品要求取消 extras 物化 templates |
| **状态** | open · residual accepted |

**未选方案**：本轮实现 orphan prune（F-001 fixed）；本轮改 install 不再复制 templates（F-002 fixed）；仅 residual F-003 不修 Root 叙述；跳过自审直接 done。

**影响**：GOAL-022 可完成阶段 F 并 `done`；open required findings = 0；两条 residual 不阻断关门。I-004 / AGENTS 生成链仍 out of scope。
