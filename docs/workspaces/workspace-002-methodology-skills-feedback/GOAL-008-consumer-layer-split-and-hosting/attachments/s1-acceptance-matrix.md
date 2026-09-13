---
id: GOAL-008-consumer-layer-split-and-hosting
doc: attachment
title: S1 验收矩阵 · 证据边界 · 审视人 · probe corpus
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# 附件 · S1 验收矩阵与 probe corpus（2026-09-13）

> 本文件是 A-001/F-002 所要求的**验收载体**：可复现路径、责任边界证据、验收人/审视方式、各阶段证据路径、probe/corpus、正反例与通过阈值。
> 它描述**怎么验**，不宣称任何阶段已实施。执行结果只写入各阶段自己的 E/A 条目。

## 1. 验收总则

| 项 | 值 |
|----|-----|
| 适用目标 | `GOAL-008-consumer-layer-split-and-hosting`（workspace-002） |
| 基线 | 本地 `dev` 分支；S1 产物提交后以该提交 hash 为审计基线 |
| 阶段顺序 | S1 → S2 → S3 →（S4 → S5）→ S6；S4/S5 串行依据见 [D-006](../01-decision/D-006-s4-s5-owned-paths-and-serial-decision.md) |
| 审计模式 | S1 `self` + 一次 independent 复审；S2/S3 `cross`；S4/S5 按改动风险定 `self`/`independent`；S6 `cross`（provider = 本地 grok build / grok-4.6 / reasoning-effort high，用户 2026-09-13 指定） |
| 全局回归命令 | `python scripts/stage_skills_mirrors.py` → `--check` → `python -m unittest skills/tests/test_skills_orchestrator.py -v` → `python -m unittest discover -s docs/tests -p 'test_standalone_bootstrap.py' -v` → `python -m unittest discover -s scripts/tests -p 'test_*.py' -v` → `git diff --check` |
| 镜像门禁 | 改动 C6 白名单路径（`docs/architecture/{principles,workspace-protocol,overview,directory-layout}.md`、`docs/templates/**`、`docs/vision/alignment.md`、`docs/contracts/**`）后，stage 产物必须纳入**同一提交**，否则 CI「Stage skills mirrors and fail on drift」红 |
| 证据归属 | consumer 侧证据（真实消费仓安装/升级）与 producer 侧证据（本 monorepo 测试/CI/发布）分列，不得互相顶替 |

## 2. 逐阶段验收矩阵

### 2.A S2 · 双层路线图语义拆分

| 字段 | 内容 |
|------|------|
| 退出判据 | 判定谓词与 prompts/模板落地；固定 probe/corpus、正反例、通过阈值、覆盖的宿主/提示词面可核对 |
| 可复现路径 | `docs/architecture/principles.md` §6.4/§6.5/§6.6、`docs/vision/alignment.md` §0.3、`AGENTS.md` §6d/§6e、`skills/prompts/{00,06}-*.md`、消费端规则面 `skills/AGENTS.template.md` + `skills/install/{claude,copilot}/AGENTS*` |
| 责任边界证据 | 判定谓词只判**职责与权威**（C1），不判节点数量；VP 不作 `parent`、不建五件套（C2） |
| 验收人 / 审视方式 | self 阶段审视 + independent（`cross`），provider = grok build；复核方式 = 按 §4 corpus 逐例核对判定谓词的输出 |
| 证据落点 | 本目标 `02-execution/E-00N-*.md`（实施事实）、`03-audit/A-00N-*.md`（意见）、`attachments/`（corpus 运行输出） |
| 通过阈值 | §4 的 10 例全部判定正确（含 4 例合法结构**不得**被误报）；防再犯静态断言在 CI 通过 |
| 已知缺口（须在 S2 消除） | ①`总路线图` 与 canonical 无映射；②命名表缺「子目标」「VP 内阶段结构」行；③消费端规则面无消歧表；④目标/愿景模板无对应槽位；⑤机器层只判 `roadmap.md` 存在 |

### 2.B S3 · 愿景总路线图与 VP 跟踪解耦

| 字段 | 内容 |
|------|------|
| 退出判据 | 跟踪权威落点锁定；既有数据迁移/兼容读取规则落盘；重复信息不存在可核验 |
| 可复现路径 | `docs/vision/roadmap.md`、`docs/vision/plans/VP-*.md`、`docs/vision/alignment.md` §0.2/§0.3、`docs/templates/vision/`（新增 roadmap 模板时）、`docs/standalone-bootstrap.md`、`docs/architecture/overview.md`（+镜像）、`docs/tests/test_vision_protocol.py` |
| 责任边界证据 | 权威 = VP frontmatter（`status`/`vision_ref`/`lead_workspace`）；`roadmap.md` 的 `status` 列**显式标注为派生投影**且无门禁用途（[D-005](../01-decision/D-005-s3-consumer-compat.md)） |
| 验收人 / 审视方式 | self + independent（`cross`）；另由 `docs/tests/` 新增「投影列不得用于门禁」类静态断言 |
| 证据落点 | 本目标 E/A 条目；`docs/vision/reviews/` 若产生口径说明则另记 VRev（愿景层审视，不得写入目标 `03-audit`） |
| 通过阈值 | ①本仓 `roadmap.md` 无未标注的重复权威字段；②`docs/tests/test_vision_protocol.py` 全绿且新增断言生效；③消费仓兼容：缺新文件/残留旧列**不**触发「不完整安装」（负例测试绿）；④两处漏 VP-004 的漂移已修正；⑤`standalone-bootstrap` 不再把生产仓 VP 行带入消费仓 |
| 已知缺口 | ①`templates/vision/` 无 roadmap 模板；②`standalone-bootstrap.md` 整文件复制；③`overview.md:70`（+镜像）与 `GOAL-001-main-vision/00-meta.md:50` 漏 VP-004；④`06-vision-orchestrator.md:76` 的「索引与 plans 一致」措辞含混；⑤roadmap 自带的「再更新本表 status」双写义务 |

### 2.C S4 · 消费仓 `AGENTS.md` / `docs/` 共存

| 字段 | 内容 |
|------|------|
| 退出判据 | 已选定共存模型；安装面为消费仓自有规则与项目文档留出共存空间；完整安装 MUST 与保护既有规则/文档的负例测试通过 |
| 可复现路径 | `skills/install.sh`、`skills/install.ps1`、`skills/update.py`、`mcp/lifecycle.py`（managed block 先例）、`skills/AGENTS.template.md`、`docs/vision/alignment.md` §0.2 |
| 责任边界证据 | 写入面清单（目标路径 / 写入方 / 覆盖策略）见 [E-003](../02-execution/E-003-s1-inventory.md) §3；安装器/updater 不得静默移动用户工作区（`workspace-protocol.md:99`） |
| 验收人 / 审视方式 | **选型先由用户裁决**；材料/数据/安装面高影响 → 至少 `independent`（grok build）；负例测试须在 Windows 与 Linux 两侧可复现 |
| 证据落点 | 本目标 E/A 条目；测试落在 `skills/tests/`、`scripts/tests/`；consumer 侧隔离安装证据落 `attachments/` |
| 通过阈值 | §3 负例 1～13 中适用于所选模型的全部通过（含「消费仓既有内容字节不变」「失败无半写状态」「重复安装幂等」）；`test_install_ps1_isolated.ps1` 与 `test_skills_update.py` 全绿 |
| 已知缺口（盘点确认，均**未实现**） | ①安装/更新不读 `.goal-governance.json`（pin 后双治理根分叉、无一致性检查）；②`{{GOVERNANCE_ROOT}}` 无安装期替换；③无大小写碰撞处理（`agents.md` vs `AGENTS.md`）；④无写权限预检/回滚；⑤File 通道无卸载；⑥updater 跳过点文件；⑦managed-block 合并只存在于 MCP 通道 |

### 2.D S5 · 默认 `/commit` 便利入口

| 字段 | 内容 |
|------|------|
| 退出判据 | 已支持宿主可调用；非完整安装 MUST、非治理入口必达、非 checkpoint 替代；负例 fail closed |
| 可复现路径 | `.github/prompts/commit.prompt.md`（先例）、`skills/install/{claude,grok,codex}/skills/*/SKILL.md`、`skills/install/copilot/prompts/*.md`、`skills/install.sh|ps1`、`skills/update.py`、`docs/contracts/skills-consumer-contract.json` |
| 责任边界证据 | 治理边界由 [D-002 §4](../01-decision/D-002-a001-response.md) 冻结；[VP-004 入口面](../../../../vision/plans/VP-004-mcp-file-dual-channel-delivery.md) 明示 `commit` = 便利可选、不入必达集 |
| 验收人 / 审视方式 | `self`；因触及契约与安装面，追加 `independent`（grok build）核对必达集未被污染 |
| 证据落点 | 本目标 E/A 条目；宿主可调用性证据走 `scripts/capture_runtime_evidence.py` 机制（`docs/releases/runtime/<ver>/`），并单列「便利入口」以免污染必达矩阵 |
| 通过阈值 | ①`docs/tests/test_file_l1.py` 的必达等式仍然成立（`entrypoints`/`hostEntrypoints` 仍为四入口）；②`contracts` 中 `commit` 只出现在便利登记位；③§3 负例 2/3/5/6/7/8/12/13 通过；④缺 `commit` 时安装仍判完整（负例）；⑤相对化守卫覆盖新壳 |
| 已知缺口（均**未实现**） | ①四个安装源目录无 `commit` 壳；②install 清单与契约必达字段是同一语义，缺「默认安装但不入必达集」表达位；③无 `/commit` 探针/证据；④`/commit` 侧 8 类 fail-closed 情形未规定（非 Git、验证范围、hook、禁用语义、detached HEAD/rebase、CRLF、push、以 commit 作放行依据） |

### 2.E S6 · 回归、审计与发布

| 字段 | 内容 |
|------|------|
| 退出判据 | I-006 冻结（版本、tag/revision、资产清单、回归矩阵、cross 覆盖、consumer vs producer 证据归属）；canonical/镜像无漂移；cross 无开放 required；正式发布证据可核对 |
| 可复现路径 | `CHANGELOG.md`、`docs/README.md`（版本台账）、`skills-pack-release.yml`、`scripts/{pack_skills_release,release_evidence,compatibility_report}.py`、`docs/releases/runtime/` |
| 验收人 / 审视方式 | `cross`：self + independent（grok build / grok-4.6 / high） |
| 证据落点 | 本目标 `03-audit/A-00N-*.md`；发布证据按 producer 归属落 `docs/releases/` |
| 通过阈值 | 全量回归绿（含 `git diff --check`、stage `--check`、矩阵证据新鲜度）；Release 资产可重下载核对；开放 required = 0 |
| 阻断项 | I-006 未冻结、A-001 F-005 未闭合前不得宣称发布就绪 |

## 3. S4/S5 责任边界与负例测试矩阵

> 负例均可复现；「现状」列说明该负例今天是红是绿，作为 S4/S5 的对照基线。

| # | 负例 | 期望行为 | 现状 | 归属 |
|---|------|----------|------|------|
| 1 | 消费仓已有**自有** `AGENTS.md` | 非交互安装：退出码 ≠ 0 且文件字节不变；共存模型下：自有内容按模型保留 | 现状绿（拒绝覆盖），共存模型下应改为「保留 + 追加受管段」 | S4 |
| 2 | 消费仓已有自有 `docs/README.md` / `docs/architecture/*.md` | 同上；额外同名文件（如 `adr-0001.md`）零改动 | 现状绿（拒绝覆盖） | S4 |
| 3 | 消费仓已有 `docs/design/**` 项目树 | 安装后逐字节不变 | 现状绿（目录合并不删） | S4 |
| 4 | pin `governance_root ≠ docs` | 安装/更新只写 `governance/`，不创建 `docs/` | **现状红**（安装器不读 `.goal-governance.json`） | S4 |
| 5 | 改过受管文件后再 update | 默认 fail closed 并报 `managed files have local changes`；`--force-managed` 后按共存模型保留自有内容 | 现状：fail closed 绿；force 后自有内容**被覆盖** | S4 |
| 6 | 消费仓存在 `agents.md`（大小写变体） | 不静默覆盖，显式报告并 fail closed | **现状红**（无大小写处理） | S4 |
| 7 | 非 Git 消费仓 | 安装/更新成功（防回归） | 现状绿（安装器不调用 git） | S4/S5 |
| 8 | 目标路径只读 / 不可写 | 退出码 ≠ 0、无部分写残留、错误可诊断 | **现状红**（无预检、无回滚） | S4 |
| 9 | 同包重复安装 | 第二次不提示、不写入、字节不变（幂等） | 现状绿（sha 短路） | S4/S5 |
| 10 | 消费方自有 `./skills/` 或 `.claude/skills/govern` | bootstrap 无 `-Force` 拒绝；有 `-Force` 先备份而非 `rm -rf` | **现状红**（直接删除） | S4 |
| 11 | 篡改受管点文件（`attachments/.gitkeep`） | 被检测为受管变更 | **现状红**（updater 跳过点文件） | S4 |
| 12 | 无改动可提交 / 暂存区含无关路径 | `/commit` 不提交并说明；不撤销、不覆盖 | 部分已规定（先例 prompt），待新壳继承 | S5 |
| 13 | 非 Git / 验证失败 / hook 拒绝 / detached HEAD / 用户禁用 | `/commit` fail closed，不宣称成功，不改治理门禁 | **未规定** | S5 |

## 4. probe corpus（双层语义判定）与通过阈值

**判定键**（正确分类，仅依据 P-006 与 [D-003](../01-decision/D-003-s1-freeze-shared-invariants.md) C1～C2；判定对象 = 决策责任 / 成功边界 / 状态权威，**不是节点数量**）：

| case | 场景 | 正确分类 | 期望行为 | 类别 |
|------|------|----------|----------|------|
| CE1 | 一区一 Root 一 VP，用户要求「推进 VP-002 的阶段」 | 合法（数量相同不构成混淆） | 在 Root 下按纲领路线图推进；**不**为 VP 建五件套、不把 VP 当 parent | 正例（防误报） |
| CE2 | 用户说「更新愿景总路线图」 | 术语需消歧 | 先解析到 `{governance_root}/vision/roadmap.md`（组合编排），**不**改 Root 的纲领路线图 | 歧义 |
| CE3 | 用户说「给 VP-002 补一个方向级路线图/阶段计划」 | 需按阶段结构归类 | 现状文本**不能唯一裁定**（命名表说阶段计划属目标内；VP 最小完备未禁止；先例已存在）→ S2 必须给出唯一答案 | 歧义 |
| CE4 | VP 内含 R1–R3，Root 也有同名 R1–R3 | 混淆风险 | 判定两条路线图的**权威层**：VP 只写意图与方向级退出判据；可执行纲领阶段归 Root | 反例 |
| CE5 | 把 VP 当成「可执行子目标」并挂 GOAL-* 目标 | 混淆 | 拒绝：VP 不得作 parent、不得建五件套、不得用目标 `03-audit` 替代 Vision Review 台账 | 反例 |
| CE6 | 把 `roadmap.md` 的 VP 跟踪表搬进目标 `00-meta.md` | 混淆 | 拒绝：组合编排留愿景层；目标层只写本目标纲领路线图 | 反例 |
| CE7 | 多 VP（如 3 个）绑同一工作区 | 合法 | 允许；`lead_workspace` 必填、`primary_plan` ∈ `plan_refs`；不因 VP 多而判失败 | 正例（泛化） |
| CE8 | 0 工作区的 `active` VP | 合法但需提示 | 按 alignment §5.1 空转规则告警/询问，不静默当健康推进 | 正例（边界） |
| CE9 | 在 `01-decision` 内写本阶段实施方案 | 合法 | 属「阶段计划」，非树节点、不建第二套状态源 | 正例（防误报） |
| CE10 | 把 VP 的 `status` 当成目标 `status`（如把 `closed` 读成 `done`） | 混淆 | 拒绝：VP status ∈ {planned, active, closed, abandoned}；Goal status 独立 | 反例 |

**通过阈值**：10 例**全部**判定正确；其中 CE1/CE7/CE8/CE9 四例合法结构**不得**被判为失败（A-003 F-007 要求的成对保护）。**执行方式**（S2 冻结）：以静态断言（对 canonical 文本与模板的判定谓词做机器可核对检查）+ 至少一个真实宿主 probe 复核；单一宿主通过不构成「AI 已不再混淆」的结论，须在 S2 审计中说明覆盖面与残余不确定性。

## 5. 证据归属与残余限制

- 本矩阵是**载体**：它证明验收字段齐全，**不**证明任何阶段已实施或已通过。
- S1 证据全部来自静态只读核对（文档 + 本地代码）；**未**运行安装、宿主 probe 或发布测试。
- 消费仓实测证据（真实消费仓安装/升级行为）在 S4/S6 才产生；producer 侧测试通过不得冒充 consumer 侧证据。
- 未关闭的 required（A-001/F-005、I-003 选型、I-006）在矩阵对应阶段仍为阻断项。
