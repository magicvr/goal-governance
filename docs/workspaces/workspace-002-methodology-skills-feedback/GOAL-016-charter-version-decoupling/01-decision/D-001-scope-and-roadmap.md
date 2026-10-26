---
id: GOAL-016-charter-version-decoupling
doc: decision-entry
record_id: D-001
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

## D-001 · 立项范围、路线图与审计/变更流程（2026-10-26）

### 触发

1. 用户 2026-10-26 `/govern` 指令：「在工作区2开设一个新的子目标，解决 issue #34，并发布新的版本。在需要交叉审计时候，调用本地 codex cli（模型：gpt-6.1-sol，思考强度 high）进行独立审计。」
2. [issue #34](https://github.com/magicvr/goal-governance/issues/34) 于 2026-10-26T02:15:24Z 创建，状态 `OPEN`，无评论。主张：Charter 同时承担愿景契约与可变注册表；`vision_ref` 精确钉文档 `version`；全量校验不按 VP status 过滤；primary 三处声明放大耦合。结果是每新建 VP/工作区都要改 Charter 并 bump 版本，进而重写全部历史 VP 的 `vision_ref`。
3. 基线：`dev` 分支 `ec088c996a07a31972a10f00bc0875650cfe7af1`，工作树干净；最新 tag `v0.13.7`；远端 Release 最新 `v0.13.7`。
4. 现有行为与 issue 描述一致：`docs/tests/test_vision_protocol.py` 的 `validate_vision_stack()` 全量校验 `plans/VP-*.md`，`validate_workspace_vision_alignment()` 对每个 `plan_refs` 全量精确匹配；`docs/vision/charter.md` 有 `primary_workspace` 与「现行版本」登记行；`alignment.md` §3.1 把 primary 分散在三处；`/vision` V1 未区分注册表更新与规范内容更新。

### 决定

1. **创建 [GOAL-016-charter-version-decoupling](00-meta.md)**，`parent` = `GOAL-001-methodology-skills-feedback-evolution`，状态 `active`，初始 `progress: 0%`（S1～S5 0/5）。范围 = issue #34 的协议修正 + 校验/测试/文档/模板/Skills 消费面 + 一次新版本发布 + 关闭 issue。
2. **结构选型**：同 Root 目的与边界内的协议演进，按 P-006 §6.6 建**子目标**；不新开 VP/工作区，不改 Charter 目的/边界/非目标。
3. **变更流程**：本目标不触发 Charter `strategic`，因此不强制 Vision Review（P-006 §6.7 仅对 Charter 初建/strategic 强制）；alignment 的语义变更由本目标 S4 的 cross 审计覆盖，不另立 VRev。此判断记录于本条，若用户认为需要 Vision Review，可按 P-004 改派。
4. **审计模式**：`cross`（元规则/协议、跨边界语义变更）。至少 A-001 self + A-002 independent；independent provider = 本地 codex CLI（`gpt-6.1-sol`，`model_reasoning_effort="high"`），按正式入口 `/audit workspace-002 goal-016` 派发，不附加 scope/文件清单/结论预期，不复制编排历史。provider 失败/超时/无可核对输出时门禁保持未满足，不降级、不冒充。
5. **路线图 S1～S5**：S1 问题复核与裁决冻结；S2 协议与 canonical 文档修正；S3 校验实现、回归与消费面同步；S4 cross 审计与意见响应；S5 发布与关门。阶段串行；`progress` 只由该 5 个检查点等权派生。
6. **初步方案（待 Q-001 裁决，不作为既成结论）**：推荐 issue 方案 A：
   - **A1**：删除 Charter `primary_workspace` 与「现行版本」中的可变登记行；primary 权威收敛到 `workspace.md` + `workspaces.md` 派生投影；旧字段作为 legacy hint 读取/忽略，不参与门禁。
   - **A3**：`planned`/`active` VP 精确匹配现行 Charter；`closed`/`abandoned` 保留关门 ref，仅校验 `vision_id` 相同；校验按 status 过滤。
   - **A2**：Charter `version` 仅表达战略对齐版本，仅 `strategic` bump；`editorial` 只更新 `updated` + `revisions.md` VR 记录，不 bump、不要求重钉。
   - 保留 `vision_ref` 精确匹配，不引入 semver 范围（P-006 §6.10 非目标）。
7. **发布边界**：S5 按仓库既有 release 流程执行——CHANGELOG/清单、必要的 16 格运行证据重捕获、本地门禁与 strict rehearsal、PR 双平台 CI、合并 `main`、annotated tag、tag workflow 的 `pack` 与 `Publish GitHub Release (gated)`、9 项资产逐项验收；Environment `release` 由用户人工审批，AI 不代批、不改环境配置。
8. **Git checkpoint**：长流程默认 auto；只在信息/方案冻结、S3 验证切片、required finding 闭合、S5 关门前验证后提交；只 `git add -- <owned paths>`，禁止 `git add -A`；验证失败或路径混入既有用户改动时 fail closed。
9. **历史只读**：不重写 GOAL-002～GOAL-015 的历史记录与既有审计意见；历史 `vision_ref`/`primary_workspace` 按事实保留，不回填。

### 为什么

- issue 的主诉是「协议耦合」而非单次文档笔误；只做 A3 最小止血（方案 C）不能阻止新 VP 仍触发 Charter bump 与 active/planned VP 重钉。
- A1+A3+A2 同时消除注册表重复权威、历史 VP 被改写与 editorial 误 bump 三条因果链；保留精确匹配避免战略漂移失察。
- 子目标而非新 VP：变更仍在 VP-002「真实项目反馈驱动的协议与 Skills 演进」意图内，不构成新的纲领波次。
- 发布而非只改源码：用户明确要求新版本；消费仓复制模板后同样受益，需要发货资产与运行证据闭环。

### 未选方案

- **新开 VP 或工作区**：同 Root/VP 目的内，不选；会增加组合编排与审计成本。
- **只做 A3（方案 C）**：不能消除新建 VP 触发 Charter bump 的主诉，不选为完整方案。
- **方案 B（新增 `alignment_version`）**：多一个版本概念、模板/工具/消费文档都要解释；issue 作者也将其列为备选。除非 Q-001 选择 B，否则不采用。
- **方案 D（`vision_ref` 改 semver 范围）**：违反 P-006 §6.10 非目标，不选。
- **直接改 alignment 不建目标/不审计**：违反 P-002/P-003 与用户指令，不选。
- **由 AI 代批 Environment `release`**：不选；仍须用户人工放行。

### 用户裁决留痕

| 问题 ID | 原题 / 选项 | 影响门禁 | 真实答复 |
|---------|-------------|----------|----------|
| Q-001 | 方案：A（A1+A3+A2，推荐）/ A1+A3 / B（`alignment_version`） | S1 退出与 S2 写集 | 待答 |
| Q-002 | `primary` 语义：稳定 monorepo 身份（推荐）/ 当前活跃工作区（另设 focus） | A1 权威与校验 | 待答 |
| Q-003 | `closed` VP 历史 ref：仅 `vision_id`（推荐）/ 还要 `revisions.md` 可追溯 | A3 校验强度 | 待答 |
| Q-004 | 发布版本号：patch `v0.13.8`（推荐）/ minor `v0.14.0` | S5 清单、tag、资产身份 | 待答 |

> 真实答复到达后逐题留痕；未答复前 S1 不退出，不把推荐项写成已裁决事实。
