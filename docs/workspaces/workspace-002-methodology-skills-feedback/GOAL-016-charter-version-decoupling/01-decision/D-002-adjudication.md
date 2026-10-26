---
id: GOAL-016-charter-version-decoupling
doc: decision-entry
record_id: D-002
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

## D-002 · 方案、primary 语义、历史 VP 校验与版本号冻结（2026-10-26）

### 触发

[D-001](D-001-scope-and-roadmap.md) 登记了 Q-001～Q-004；2026-10-26 同步询问卡片收到真实答复。S1 的退出条件（issue 复核 + 用户裁决）已满足，需冻结写集后进入 S2/S3。

### 用户裁决

| 问题 ID | 原题 / 选项 | 真实答复 |
|---------|-------------|----------|
| Q-001 | 方案：A（A1+A3+A2）/ A1+A3 / B（`alignment_version`） | **A：A1+A3+A2** |
| Q-002 | `primary` 语义：稳定 monorepo 身份 / 当前活跃工作区 / **单一权威（仅 workspace.md）** | **单一权威（仅 `workspace.md`）** |
| Q-003 | `closed` VP 历史 ref：**仅 `vision_id` 相同** / 还要 `revisions.md` 可追溯 / 完全不校验 | **仅 `vision_id` 相同** |
| Q-004 | 发布版本号：**patch `v0.13.8`** / minor `v0.14.0` / S5 前再定 | **patch `v0.13.8`** |

### 决定

1. **A1 · Charter 去注册表**
   - 删除 `docs/vision/charter.md` frontmatter 的 `primary_workspace`，删除「现行版本」表中的 Primary 工作区 / 现行 active VP / 组合编排登记行；改为链接 `workspaces.md` / `roadmap.md`。
   - 模板 `docs/templates/vision/charter.md` 同步删除该字段与登记行。
   - **primary 唯一权威 = `workspace.md` 的 `vision_role: primary`**。`workspaces.md` 仅保留派生展示（role/map_status），**不参与门禁**。至多一个 primary 由扫描全部 `workspaces/workspace-*/workspace.md` 校验。
   - 旧 Charter 残留的 `primary_workspace` 作为 **legacy hint 读取/忽略**，不作为门禁、不作为不完整安装判据、不要求消费仓立即删除。
   - 当前焦点用 `workspaces.md` 的 `map_status: active` 表达；不把 primary 解释为「当前活跃工作区」。

2. **A3 · VP 生命周期分层**
   - `planned` / `active` VP：`vision_ref` 必须精确等于现行 Charter `{vision_id}@{version}`。
   - `closed` / `abandoned` VP：保留关门时 `vision_ref`，**只校验 `vision_id` 相同**，不要求等于当前版本，也不要求版本在 `revisions.md` 可追溯（Q-003）。
   - `closed` VP 若 reopen 为 `planned`/`active`，恢复 current-match。
   - `validate_vision_stack()` 与 workspace `plan_refs` 校验均按 VP status 过滤；不得再全量精确匹配历史 VP。

3. **A2 · 版本语义**
   - Charter `version` = **战略对齐版本**，不是每次文档编辑版本。
   - 仅 `strategic` 变更 bump（至少 minor）；`editorial` 只更新 `updated` 并追加 `revisions.md` 的 `VR-` 记录，**不 bump**、不要求 `planned`/`active` VP 重钉。
   - 保留 `vision_ref` 精确匹配；**不引入 semver 范围匹配**（P-006 §6.10 非目标）。
   - `strategic` 后 `planned`/`active` VP 的旧 ref 必须被门禁判失败，re-align 后通过；`closed`/`abandoned` 保持旧 ref 仍通过。

4. **发布**：`v0.13.8`（patch）。协议 `0.1.0` 与 consumer contract 数据结构保持不变；发布流程按仓库既有 release 链路，Environment `release` 由用户人工审批。

5. **S1 退出**：I-001～I-004 置 `verified`；I-005（Environment 审批）保持 `open`，属 S5。路线图 S1 **完成**，S2 开始；派生 `progress` = 1/5 = **20%**。

### 写集（canonical 优先；镜像由 stage 生成）

| 类别 | 路径 |
|------|------|
| 愿景契约 | `docs/vision/alignment.md`、`docs/vision/charter.md`、`docs/vision/revisions.md`、`docs/vision/workspaces.md`、`docs/vision/consumer-checklist.md`、`docs/vision/README.md`、`docs/standalone-bootstrap.md` |
| 核心原则/协议 | `docs/architecture/principles.md`（P-006 §6.1/6.3/6.5/6.8/6.10）、`docs/architecture/workspace-protocol.md`（§4b/§4 摘要） |
| 根规则 | `AGENTS.md` §6d/§6e/§12；`.github/copilot-instructions.md`（若含对应摘要） |
| 模板 | `docs/templates/vision/charter.md`、其他引用 primary/version 的愿景模板 |
| 校验/测试 | `docs/tests/test_vision_protocol.py`、`docs/tests/test_standalone_bootstrap.py`（如涉及）、`docs/tests/fixtures/vision/**` |
| Skills 消费面 | `skills/prompts/00-govern-orchestrator.md`、`06-vision-orchestrator.md`、`07-independent-vision-review.md`、`skills/AGENTS.template.md`（如含摘要） |
| 镜像 | `skills/core/docs/architecture/*`、`skills/core/docs/vision/alignment.md`、`skills/core/docs/templates/vision/charter.md`（由 `python scripts/stage_skills_mirrors.py` 生成） |

**不写**：历史 GOAL-002～GOAL-015 的记录与审计意见；旧 Release 资产；旧 `vision_ref`/旧 `primary_workspace` 历史文本（只读保留）；consumer contract 数据结构。

### 验收（与 issue #34 对齐）

- 新增 VP + 工作区（delivery / primary 两种）后，`charter.md` 内容与 `version` 均不变，`validate_vision_stack()` 通过，现有 VP `vision_ref` 无需改动。
- 纯 `editorial` Charter 修改后 `version` 不变，`planned`/`active` VP 无需重钉，测试通过。
- `strategic` Charter 修改后版本 bump；`planned`/`active` 旧 ref 被门禁判失败，re-align 后通过；`closed` VP 保持旧 ref 仍通过。
- 至少一个 `closed` VP 的 `vision_ref` 指向历史版本，测试断言不被要求匹配当前 Charter。
- primary 仅 `workspace.md` 一个门禁权威；`workspaces.md` 为派生展示；扫描至多一个 primary；旧 Charter 字段不参与门禁。
- 文档/模板/技能/镜像同步；`stage_skills_mirrors.py --check` 通过；消费兼容旧仓 `primary_workspace` 与旧 `vision_ref` 不被误判。
- 新增回归：新建 VP 不改 Charter；closed VP 不重钉；strategic bump 仍阻断 active VP；primary 多声明/冲突 fail closed（按单一权威口径）。

### 未选方案

- **A1+A3（Q-001 未选）**：保留 editorial 可 bump，仍可能触发 active/planned VP 重钉，不能完整消除主诉。
- **B（Q-001 未选）**：多一个 `alignment_version` 概念；issue 作者列为备选。
- **primary 双权威或当前活跃区（Q-002 未选）**：需要额外 focus 语义与迁移，且会把「当前焦点」再次耦合到愿景文件。
- **closed VP 还要 revisions 可追溯（Q-003 未选）**：历史缺口可能造成新阻断；与本 issue「历史只读」目标相悖。
- **minor `v0.14.0`（Q-004 未选）**：本 change 不改变协议 0.1.0 与 consumer contract 数据结构，按 patch 发布。
- **方案 D（semver 范围）**：违反 P-006 §6.10，不选。
