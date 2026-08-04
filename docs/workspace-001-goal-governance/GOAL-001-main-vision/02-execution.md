---
id: GOAL-001-main-vision
doc: execution
status: done
parent: null
created: 2026-07-18
updated: 2026-08-04
version: 0.6.0
---

# 执行记录 · GOAL-001

## 执行索引（legacy inline + 新增平铺记录）

| E-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| E-001 | 2026-08-04 | D-029 授权后的 Web 资产退役交接至 workspace-002 | recorded | [02-execution/E-001-web-retirement-handoff.md](02-execution/E-001-web-retirement-handoff.md) |

> 既有日期时间线保留为 legacy inline；新事实从 `02-execution/` 写入。

总目标的执行通过子目标推进。本文件只记录根目标层的里程碑与协调事项。

## 当前进展（2026-07-31）· **有界关门**

> **现时权威**：与 [00-meta 现时摘要](00-meta.md#现时摘要2026-07-31-单一权威入口--有界关门) 对齐。本 Root **`done`**。

| 方向 | 状态 | 说明 |
|------|------|------|
| 核心方法论与模板 | 奠基 **done** | 后续修正 → VP-002 |
| Skills | 奠基 **done** | 四入口；F-006 → VP-002 |
| Web | **历史有界；资产已退役** | R-009-X → VP-003（正式挂起） |
| 愿景 | VP-001 **closed**；VP-002 **active**（0 区）；VP-003 **planned** | 见 roadmap |
| Root | **`done`** | [D-028](01-decision.md#d-028--root-有界关门奠基完成演进改挂-vp-002--workspace-0022026-07-31) / [A-021](03-audit.md#a-021--root-有界关门审计close-out2026-07-31) |
| 工作区 | **archived** | 禁止本树再开演进子目标 |

## 下一步（本 Root 已关）

1. 有真实反馈 → `/govern` 开 **workspace-002** + Root，挂 **VP-002**。  
2. VP-002 空转复核 ≤ **2026-08-14**。  
3. 本区仅只读过程与参考。  

## 2026-07-31 · Root 有界关门 D-028 + A-021

- **用户结构**：VP-001 有界关 + VP-002 active + VP-003 planned + WS-001 Root done；后继 WS-002↔VP-002。
- **决策**：[D-028](01-decision.md#d-028--root-有界关门奠基完成演进改挂-vp-002--workspace-0022026-07-31)。
- **关门审**：[A-021](03-audit.md#a-021--root-有界关门审计close-out2026-07-31) **pass**。
- **同轮愿景**：VP-001 closed；VP-002/VP-003 落盘；roadmap / workspaces / workspace.md archived。
- **未做**：scaffold workspace-002；关 R-009-X；删 `web/`。

## 2026-07-31 · 路径收束 D-027 + V-F-008 fixed

- **用户指令**：愿景 S1+B1 后「直接帮我操作」。
- **决策**：[D-027](01-decision.md#d-027--路径收束协议--skills-问题驱动演进本仓-web-冻结2026-07-31)。
- **审计响应**：[A-020](03-audit.md#a-020--响应-vrev-005-v-f-008路径收束与入口叙事2026-07-31) — V-F-008 **fixed**。
- **已写入**：Root 决策/审计/现时摘要；根 README + `web/README` 冻结叙事；goal-tree 日志。
- **未做**：删除 `web/`；改各 GOAL status；tag/Release；关闭 R-009-X。

## 2026-07-30 · 路径 D 授权：`v0.9.2` + release-mode evidence（D-026）

- **用户指令**：`/govern 授权路径 D 打 v0.9.2 并跑 release evidence`。
- **决策**：[D-026](01-decision.md#d-026--路径-d授权annotated-v092--release-mode-evidence2026-07-30)。
- **冻结内容**（本拍提交前）：
  1. `CHANGELOG.md` → `## 0.9.2 - 2026-07-30`（Unreleased 清空说明）。
  2. `docs/contracts` + `skills/contracts` 矩阵 `candidateRevision: v0.9.2`（字节镜像一致）。
  3. `scripts/tests/test_release_evidence.py`、`skills/tests/test_skills_orchestrator.py` 守卫对齐 `v0.9.2`。
  4. `skills/README.md` / `docs/README.md` 包身份与矩阵 SHA 同步。
  5. 含上一拍 README 四入口装机树卫生与 Goal「三入口」历史注。
- **计划命令**（冻结提交 + annotated tag 后）：
  - `python scripts/release_evidence.py --mode release --tag v0.9.2 --run-checks --include-web --output artifacts/release-evidence-v0.9.2.json`
  - 可选：`python scripts/compatibility_report.py --output artifacts/compatibility-report-v0.9.2.json`
- **执行结果（补记）**：
  1. 首轮 release-mode **失败**：12 宿主入口行为源相对 2026-07-28 evidence **stale**（AGENTS/编排器/wrappers 在 D-025 等维护后已变）。
  2. **2026-07-30** 全量重采 12 单元均 **pass**（产物 `attachments/runtime/*-2026-07-30-*-refresh.json`）；Grok CLI 宿主版本 **0.2.114**；矩阵证据指针已更新；coverage **ready-for-release-evidence**。
  3. 本地 annotated **`v0.9.2`** 落在 commit `b491e3a937c88d96caf65691e5a015d6d6fe5cb0`（runtime 重采 + 测试/ledger 对齐后）。
  4. `python scripts/release_evidence.py --mode release --tag v0.9.2 --run-checks --include-web --output artifacts/release-evidence-v0.9.2.json` → **releaseStatus: release-candidate**；**checksPassed: true**（skills / standalone / release-tool / diff-whitespace / web-parser 全过）；coverage **ready-for-release-evidence**；workingTree **clean**；candidate **v0.9.2**。
  5. 兼容报告：`artifacts/compatibility-report-v0.9.2.json`；本地 pack：`dist/goal-governance-skills-v0.9.2.zip`（+ `.sha256`）。
- **尚未**：`git push origin v0.9.2` / PR 合入 `main` / Environment **`release` 审批** / GitHub Release 资产上传。
- **不构成**：Root status 变更；R-009-X closed；无 push+Environment 审批则无正式 GitHub Release。

## 2026-07-30 · 路径 D 可选卫生：四入口装机树 + Goal「三入口」历史注

- **用户指令**：`/govern 实现层路径 D 可选卫生（skills README 装机树片段、Goal 历史「三入口」叙述）`。
- **范围（D-024 §2）**：文档卫生；**不**改 Root/子目标 status/progress；**不** tag；**不**改 Charter/VP 实质边界。
- **事实**：
  1. `skills/README.md` **1.5.2**：目录树、Claude/Grok 手动安装路径、脚本参数表、交付摘要对齐默认**四入口**（含 `vision-audit` 与 `07`）；去掉过时「三 skill / 三入口」装机片段与「Copilot vision 仍配额阻断」的未包含项措辞。
  2. GOAL-001 [D-018](01-decision.md#d-018--skills-vision-决策层第二刀2026-07-28) 与本文件 D-018/D-019 历史节追加**现时注**（当日三入口 → 现时四入口经 D-020）；**不**改写独立审计 A-015 正文中的历史观察句。
  3. `test_skills_readme_default_install_documents_govern_audit_vision` 守卫扩展为要求 README 含 `vision-audit`。
- **验证**：`python -m unittest skills.tests.test_skills_orchestrator.TestSkillsOrchestratorPackage.test_skills_readme_default_install_documents_govern_audit_vision` → **ok**。
- **未做**：runtime 重采；annotated tag；改 matrix `installationSurface` 细字段（非本拍点名范围）。

## 2026-07-29 · 响应 A-018（D-025 · 路径 D 协议回流）

- **用户指令**：`/govern 响应 GOAL-001 A-018：优先 F-012 + F-013，再 F-014/F-015`。
- **事实**：
  1. 重写 [standalone-bootstrap.md](../../standalone-bootstrap.md) 与测试：冷启动 Charter→VP→区+Root+plan。
  2. core 镜像增加 `vision/alignment.md`；install 默认安装；测试 38 项含 core/AGENTS 断言通过。
  3. 清除权威面「仅 P-001～P-005」；根/模板 AGENTS 门禁语义对齐。
  4. Charter editorial VR-004；决策 [D-025](01-decision.md#d-025--响应-a-018p-006-后核心包--standalone--agents-回流2026-07-29)；响应 [A-019](03-audit.md#a-019--响应-a-018-f-012f-0152026-07-29)。
- **验证**：`test_standalone_bootstrap` 3 ok；`skills.tests.test_skills_orchestrator` 38 ok。
- **未做**：tag/Release；Root status 变更；runtime 全量重采。

## 2026-07-28 · 路径 D：发版候选 runtime 验证（不发版）

- **用户指令**：`/govern 按路径 D 推进发版候选 runtime 重采`。
- **范围判定（路径 D）**：D-023 全量 refresh 之后，行为源（AGENTS / 编排器 / 四入口 wrappers）**未**因 F-007/F-008 台账变更而变脏；本拍执行 **freshness 验证 + 发版 rehearsal**，而非因 stale 再全量 12 单元 host re-dispatch。
- **事实**：
  1. 宿主版本：Claude Code `2.1.220`；Grok Build `0.2.112`；Copilot CLI `1.0.75`（与矩阵一致）。
  2. `python scripts/compatibility_report.py --output artifacts/compatibility-report-path-d-check.json --require-ready` → **exit 0**；coverage **ready-for-release-evidence**；uncovered **[]**；`candidateRevision: unreleased`；报告 commit `097ff2ce…`。
  3. 矩阵 12 宿主入口（govern/audit/vision/vision-audit × claude/grok/copilot）均为 **runtime-verified**，证据仍指向 2026-07-28 refresh/byok 文件；行为源 digest 与现树一致（报告未报 stale）。
  4. 修复推进中暴露的门禁：`scripts/tests/test_release_evidence.py` 将硬编码 `v0.9.1` 改为 `unreleased`（与 post-tag 工作树一致）；剥离 GOAL-001 文档 trailing whitespace。
  5. `python scripts/release_evidence.py --mode rehearsal --run-checks --include-web --compatibility-report artifacts/compatibility-report-path-d-check.json --output artifacts/release-evidence-path-d-rehearsal-2026-07-28.json` → **checksPassed: true**；`releaseStatus: rehearsal`；workingTree **不 clean**（含本拍台账，预期）。
- **不构成**：annotated tag；GitHub Release；`release_evidence --mode release`；Root/子目标 status 变更；R-009-X/F-006 closed；关闭 A-015 F-011（formal tag 仍 recommended open）。
- **计划（非本拍）**：用户授权后可设下一 tag（建议 **v0.9.2**，因 **v0.9.1** 已存在）并跑 release-mode。

## 2026-07-28 · 响应 A-015 F-008：路径 D 契约（D-024）

- **用户指令**：`/govern 响应 GOAL-001 A-015 F-008：采用路径 D`。
- **事实**：
  - 落盘 [D-024](01-decision.md#d-024--a-015-f-008-路径-d仅维护发版协议不关-root2026-07-28)：路径 D 最小交付/非目标、与 R-009-X·F-006 关系、018/019 归属、改道门槛。
  - 刷新 [00-meta 现时摘要](00-meta.md#现时摘要2026-07-28-单一权威入口) 与本节进展/下一步；[A-017](03-audit.md) 关闭 **F-008**（`fixed`）；F-009 recommended 对照表确认 closed。
  - **不**关 Root；**不** closed R-009-X；**不**开阶段 7；**不**建 GOAL-020；**不**改各子目标 status/progress。
- **计划（非本拍事实）**：后续默认 D 内维护，直至用户改道或点名单点 residual。

## 2026-07-28 · 响应 A-015 F-007：刷新 Root 现时摘要

- **用户指令**：`/govern 响应 GOAL-001 A-015 的 F-007，刷新 Root 现时摘要与下一步指向。`
- **事实**：
  - 重写 [00-meta.md](00-meta.md)「现时摘要（2026-07-28）· 单一权威入口」：三面状态、阶段 6 有界结项指针、018/019 作用、P-006/愿景栈与 VRev、开放门禁、下一编号 **GOAL-020**、R-009-X 对照表；历史「当前*」与早期路线图表标为不可作现时。
  - 刷新本节「当前进展 / 下一步」；追加 [A-016](03-audit.md) 响应，关闭 **F-007**（`fixed`）。
  - **不**关闭 F-008；**不**改 Root `status`/`progress`；**不**建 GOAL-020；**不**宣称阶段 6 终态。
- **计划（非本拍事实）**：下一拍处理 F-008 路径选择。

## 2026-07-28 · 三宿主 `/audit` 重采与 Copilot `/vision` 复核（D-023；不发版）

- 三宿主 `/audit` 均以当前行为源重采并通过：`claude-code-cli-audit-2026-07-28-refresh.json`、`grok-build-cli-audit-2026-07-28-refresh.json`、`copilot-cli-audit-2026-07-28-refresh.json`。三份旧 audit evidence 不再作为当前矩阵引用。
- GitHub Copilot CLI `1.0.75` 的 `/vision` 已通过 BYOK read-only dispatch：`copilot-cli-vision-2026-07-28-byok-refresh.json`；矩阵单元升级为 `runtime-verified`。
- 首次完整报告继续发现 Claude/Grok 的既有 `/vision` evidence 陈旧；两单元随后重采并通过：`claude-code-cli-vision-2026-07-28-refresh.json`、`grok-build-cli-vision-2026-07-28-refresh.json`。旧 vision evidence 不再作为当前矩阵引用。
- 完整报告 [artifacts/compatibility-report-runtime-refresh-2026-07-28.json](../../../artifacts/compatibility-report-runtime-refresh-2026-07-28.json) 已生成：canonical/Skills 镜像一致，12 个宿主 entrypoint 均可校验，coverage 为 `ready-for-release-evidence`；`candidateRevision` 保持 `unreleased`，未产生 tag、Release 或 release-mode evidence。
- 所有结果只证明 wrapper 路由、核心 prompt 加载与 repository-backed read-only 行为；未新增 Goal 或 Vision finding，未改变 Charter / VP / Goal status 或 progress，未执行 tag、Release 或 release-mode evidence。

## 2026-07-28 · Copilot BYOK replay 与 `/govern` freshness 重采（D-022；不发版）

- 检查发现用户级 BYOK 的 provider URL、模型与 provider API key 均已配置，但当前 VS Code 终端未继承。replay helper 现仅在子进程缺失时读取用户级变量，并把 provider/GitHub token 标记为 secret environment variables；未读取、显示或落盘任何值。
- GitHub Copilot CLI `1.0.75` 的 `/vision-audit` 已通过 BYOK read-only dispatch：`GOAL-008/attachments/runtime/copilot-cli-vision-audit-2026-07-28-byok-auth.json`。矩阵将该单元升级为 `runtime-verified`。
- 全矩阵 `/govern` freshness 已重采并通过：`claude-code-cli-govern-2026-07-28-refresh.json`、`grok-build-cli-govern-2026-07-28-refresh.json`、`copilot-cli-govern-2026-07-28-refresh.json`。三条旧 evidence 不再作为当前候选的矩阵引用。
- 全量 `compatibility_report.py` 已不再由 `/govern` evidence 阻断；它随后在既有 `.claude/skills/audit/SKILL.md` 的陈旧 `/audit` evidence 停止。该 `/audit` 单元不在本轮用户指定的 `/govern` freshness 范围内，仍需在完整候选验证时单独重采。
- Copilot `/vision` 仍为 `pending-runtime-validation`。未创建 VRev、未改变 Charter / VP / Goal status 或 progress，未执行 tag、Release 或 release-mode evidence。**计划**：在后续完整候选验证中按需重采其余陈旧单元。

## 2026-07-28 · `/vision-audit` 三宿主 runtime capture（D-021；不发版）

- `scripts/capture_runtime_evidence.py` 与 canonical/Skills `runtime-evidence.schema.json` 已接受 `vision-audit`；聚焦 unit test 验证 CLI 与 schema 都能生成该单元的有效 evidence。
- 新增三份只读 probe：`attachments/runtime/prompts/{claude,grok,copilot-cli}-vision-audit.txt`。它们要求实际加载宿主 wrapper 和 `07-independent-vision-review`，读取当前愿景/工作区事实并输出 marker；不写 `reviews.md` 或 Goal 记录。
- Claude Code `2.1.220` 通过：`GOAL-008/attachments/runtime/claude-code-cli-vision-audit-2026-07-28.json`。Grok Build `0.2.112` 通过：`GOAL-008/attachments/runtime/grok-build-cli-vision-audit-2026-07-28.json`。两单元已更新为 `runtime-verified`。
- GitHub Copilot CLI `1.0.75` 失败：`GOAL-008/attachments/runtime/copilot-cli-vision-audit-2026-07-28.json` 与其 stderr 记录“monthly quota”耗尽；单元保持 `pending-runtime-validation`，未将失败证据写入 verified evidence。
- `compatibility_report.py` 的全矩阵汇总仍被既有 `.claude/skills/govern/SKILL.md` 的陈旧 runtime evidence 阻断；直接调用 validator 已确认本轮 Claude/Grok `/vision-audit` evidence 有效且行为源新鲜。该报告阻断属于当前候选的既有重采工作，不把它误写为本入口失败。
- 未创建 VRev、未改变 Charter / VP / Goal status 或 progress，未执行 tag、Release 或 release-mode evidence。**计划**：配额恢复后仅重采 Copilot `/vision-audit` 单元。

## 2026-07-28 · 响应 V-F-001：独立 Vision Review 专用入口（D-020；不发版）

- **用户裁决**：采用专用 `/vision-audit`，不扩展 `/audit` 的 scope 路由。
- **产物**：`skills/prompts/07-independent-vision-review.md`；Claude/Grok/Copilot 的 `vision-audit` 安装源与当前 workspace wrapper；`install.ps1` / `install.sh` 默认四入口；消费者契约与 Skills README。
- **边界**：`/audit` 只写 Goal `03-audit.md`；`/vision-audit` 只写 `docs/vision/reviews.md`；`/vision` 保留 self Review、决策与 finding 响应。
- **已执行验证**：独立入口核心、原 `/vision`、Claude/Grok/Copilot 安装源、Windows PowerShell 隔离安装、消费者契约和 Skills 镜像的聚焦 `unittest` 均通过。
- **运行时证据**：新入口三宿主均 `pending-runtime-validation`；矩阵为 `unreleased`，未将安装结构测试记为 runtime-verified。
- **审视闭合**：[VRev-002 的 V-F-001 响应](../../../vision/reviews.md#响应--v-f-0012026-07-28) 记录为 `fixed`。Root 保持 `active`，不改 progress，不发版。

## 2026-07-28 · `/vision` follow-through（D-019；不发版）

- **决策**：[D-019](01-decision.md#d-019--vision-follow-throughruntime--消费面--vrev不发版2026-07-28)。
- **Runtime dual-pass（GOAL-008 attachments/runtime）**：
  - Claude：`claude-code-cli-vision-2026-07-28-pass1.json` + `…-2026-07-28.json` → **pass** / markerObserved
  - Grok：`grok-build-cli-vision-2026-07-28-pass1.json` + `…-2026-07-28.json` → **pass** / markerObserved
  - Copilot：两次 **fail**（stderr: monthly quota）；矩阵 vision 仍 pending；scratch `vision-capture-copilot.log`
- **矩阵/README**：Claude+Grok vision runtime-verified；Copilot pending；skills README 状态表已对齐。
- **消费面**：AGENTS.template / Claude install AGENTS / Copilot instructions 含 P-006 与**当时**三入口。
- **Dogfood**：[VRev-001](../../../vision/reviews.md) self pass；**无** tag/Release/release_evidence release-mode。
- 命令摘要见 GOAL-008 执行与 scratch `vision-capture-summary.txt`。
- **现时注（2026-07-30）**：D-019 当时默认面为三入口；**现时**默认四入口（+ `/vision-audit`，[D-020](01-decision.md#d-020--响应-v-f-001独立-vision-review-专用入口2026-07-28)）。本条不改历史 runtime 事实。

## 2026-07-28 · Skills `/vision` 第二刀（D-018）

- **决策**：[D-018](01-decision.md#d-018--skills-vision-决策层第二刀2026-07-28)。
- **产物**：
  - `skills/prompts/06-vision-orchestrator.md`
  - install：`claude`/`grok`/`copilot` vision wrappers；`install.ps1` / `install.sh` **当日**默认三入口
  - 本仓 `.grok/skills/vision/`（及若存在 `.claude/skills/vision/`）
  - 契约/矩阵含 `vision`（pending-runtime-validation）
  - 测试与 skills README / AGENTS 同步
- **未做**：各宿主 `/vision` runtime evidence 重采。
- Root 仍 `active`。
- **现时注（2026-07-30）**：其后 [D-020](01-decision.md#d-020--响应-v-f-001独立-vision-review-专用入口2026-07-28) 将默认 install 扩为**四入口**（+ `/vision-audit`）。本条「三入口」仅为 D-018 当日事实，非现行产品面。

## 2026-07-28 · P-006 愿景组合治理第一刀（D-017）

- **决策**：[D-017](01-decision.md#d-017--p-006-愿景组合治理与级联对齐第一刀2026-07-28)。
- **产物（核心）**：
  - `docs/architecture/principles.md` **0.7.0**（新增 P-006 全文）
  - `docs/vision/alignment.md` **0.3.0**；新建 `docs/vision/reviews.md`
  - `docs/architecture/workspace-protocol.md` **0.6.0**
  - 根 `AGENTS.md` **0.10.0**（§6d/6e）
  - vision README / consumer-checklist / roadmap / workspaces 同步
  - 模板：`docs/templates/vision/charter.md`、`vision-plan.md`；`workspace-context` **0.4.0**
  - 测试：`docs/tests/test_vision_protocol.py`（reviews 必选；sandbox 无 plan 拒绝；P-006 断言）
  - 编排器：`skills/prompts/00-govern-orchestrator.md` **0.9.0**（冷启动 Charter→VP→区；无 opt-out）
  - Skills core 镜像：principles、workspace-protocol、templates 已同步
- **未做（第二刀）**：独立 `/vision` skill 全文；Web 愿景写入 UI。
- **Root**：仍 `active`；本条不改 progress 宣称。

## 2026-07-28 · 核心协议逻辑一致性修订（D-016）

- **触发**：用户审视核心协议逻辑问题 → 确认修改 → 要求在合适处记录操作。
- **决策**：[D-016](01-decision.md#d-016--核心协议逻辑一致性修订finding-闭合--隐式工作区--p-004-扩表2026-07-28)。
- **已改权威/落地文件**（摘要）：
  - `docs/architecture/principles.md` → **0.6.0**（P-002 路线图槽位；P-003 finding 三路径；P-004.1～4.4；死链修正）
  - `docs/architecture/workspace-protocol.md` → **0.4.0**（纲领串行/阶段内并行；legacy 唯一路径；跨区 id；Primary 冲突指针）
  - `docs/architecture/overview.md` → **0.7.0**（现时叙述；去掉过期「只读 / GOAL-010 进行中」）
  - `docs/architecture/directory-layout.md`（约束与 protocol 对齐）
  - `docs/vision/alignment.md` → **0.2.0**（Primary 冲突裁决；active VP 14 日空转）
  - `docs/vision/consumer-checklist.md`（Primary / 空转勾选）
  - `docs/README.md`（编号、finding 闭合、legacy）
  - 根 `AGENTS.md`、`skills/AGENTS.template.md` → **0.9.1**
  - `skills/prompts/00-govern-orchestrator.md` → **0.8.1**（§3.3 单条 residual；闭合用语）
- **交叉引用**：GOAL-010 已 `done`，仅在其执行记录追加「协议修订不重开目标」说明，不改其 status/progress。
- **验证**：`python -m unittest docs.tests.test_workspace_protocol docs.tests.test_vision_protocol docs.tests.test_standalone_bootstrap` → OK；`python -m unittest skills.tests.test_skills_orchestrator` → OK（35）。
- **未做**：不改 Root/`goal-tree` 目标 status 表进度；不关 R-009-X；不建 GOAL-020；不刷 runtime evidence / release tag。
- **goal-tree**：仅追加本日志节（见 [goal-tree.md](../goal-tree.md)）。

## 2026-07-20 · GOAL-008 阶段 5 关门

- GOAL-008 完成 I-002/I-003：GitHub Actions run `29700051047` 在同一候选 commit `8a33ecd21d9183a680c9c0d63e471469f5e515a8` 通过 Ubuntu/Windows Web parser replay，coverage ready 且无 uncovered 单元。
- 已创建并推送 annotated `v0.7.0`，release mode evidence checks 全部通过；GOAL-008 `03-audit.md` A-016 与本目标 A-013 关闭阶段 5 required 门禁和 F-005。
- GOAL-001 保持 `active`，阶段 6 Web 深化未在本次范围内启动。

## 2026-07-20 · `dev` 到 `main` 阶段性整合

- 按 [D-013](01-decision.md#d-013--阶段性整合-dev-到-main-并在验证后删除-dev2026-07-20) 创建并合并 [PR #1](https://github.com/magicvr/goal-governance/pull/1)。PR head 为 `491152a64e2d2f27d148367f5a9c6bad4439273b`；两套 PR 检查的 `contract-and-report` 与 `windows-install-surface` 均为 `SUCCESS`。
- 使用普通 merge 生成 commit `2662c2551ea92a1d046d9658b0b9b55885f3e57f`，保留 annotated `v0.7.0` 及其候选提交 `8a33ecd21d9183a680c9c0d63e471469f5e515a8` 在 `main` 的祖先链中。
- `main` 的 GitHub Actions run `29701936833` 通过，包含 portable contract/report 与 Windows install-surface 两项 job；确认 `main` 包含 PR head 和 `v0.7.0` 后，删除 `origin/dev` 与本地 `dev`（原 head `491152a`）。
- 本次只完成分支整合与执行留痕；GOAL-001 继续 `active`，不改变阶段 6/7、F-006 或目标树状态。

## 2026-07-20 · 阶段 6 方向重定向与 GOAL-009 立项

- 用户明确否决将 Web 定位为“完善的只读工具”，要求其成为供人类工作时由 AI 协助的目标治理工作台。
- 已记录 [D-014](01-decision.md#d-014--阶段-6-重定向为-ai-协助的人类目标治理工作台2026-07-20)，保持 `docs/goals/` 的 canonical 地位，同时允许后续在确认、事务和审计约束下规划受控 Web 变更。
- 已创建 [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md) 作为产品定义与信息发现目标，初始 `active / 0%`；其 I-001～I-006 为受影响实施/验收门禁，当前均未被写成已验证。
- 本次未修改 Web 应用代码、未暴露写入 API、未开放 AI 自动写入或部署服务；现有 Web 只读页保留为历史基线，不再作为阶段 6 的产品终态。

## 时间线

### 2026-07-18 · 项目启动与规则定稿

- 明确根目标：构建实用的目标治理框架。
- 确定早期双交付形态：Web 应用 + Skills/提示词（该历史决策由 D-007 重述，不删除原记录）。
- 确定文档核心规则：扁平目标、`parent` 字段、`goal-tree.md`。
- 创建子目标 [GOAL-002-project-bootstrap](../GOAL-002-project-bootstrap/00-meta.md) 承接初始化工作。

### 2026-07-18 · 初始化完成，进入 Skills 阶段

- GOAL-002 标记为 `done`（文档体系 + Web 骨架 + Skills 基础结构）。
- 在根目标写入**高层路线图**（五阶段方向指引）。
- 创建子目标 [GOAL-003-skills-practice](../GOAL-003-skills-practice/00-meta.md)，承接 Skills 完善与实践验证（进度 0%）。

### 2026-07-18 · Skills 关门，阶段 3 推进

- GOAL-003 标记为 `done`（编排主入口 + 原语 + 多宿主安装）。
- 创建并推进 [GOAL-004-core-data-model](../GOAL-004-core-data-model/00-meta.md)（阶段 3）。
- GOAL-004 完成阶段 A：领域模型与存储约定设计说明与决策 D-004～D-007（进度 25%）。

### 2026-07-18 · 立项 Skills 闭环升级（阶段 2b）

- 创建子目标 [GOAL-005-skills-closed-loop-audit](../GOAL-005-skills-closed-loop-audit/00-meta.md)：治理闭环、交叉审计、意见冲突与自审问询由用户裁决。
- 路线图增加**阶段 2b**（与阶段 3 GOAL-004 可并行）；同步 `goal-tree.md`。

### 2026-07-19 · 同步 GOAL-005 结项状态

- GOAL-005 已完成 A-014 self close-out 与 A-016 independent close-out 双确认，状态为 `done / 100%`。
- 修正根目标路线图、子目标表与当前进展中的旧 `active / 85%` 描述；历史立项记录保持不变。
- F-019 继续作为 GOAL-005 结项后的 recommended residual，不阻塞 GOAL-001 或 GOAL-004 推进。

### 2026-07-19 · GOAL-004 阶段 C 完成

- GOAL-004 已完成阶段 A～C：领域模型、读取路径以及可恢复的 Create/Update 写入服务均有测试证据，子目标进度为 75%。
- 根目标路线图的阶段 3 仍为进行中；阶段 D 将把现有目标服务接入首页与详情页。

### 2026-07-19 · GOAL-004 阶段 D 完成

- GOAL-004 已将 Markdown 真相源接入首页和目标详情页，详情可查看 Decision / Execution / Audit 基础信息及文档诊断；阶段 D 自动化测试、编译/依赖检查与桌面/移动浏览器验证均已完成。
- GOAL-004 已完成 A～D 全部实施阶段并记录 A-005 self 阶段审计，进度为 `100%`；目标仍为 `active`，待关门审计和用户确认。

### 2026-07-19 · GOAL-004 关门

- A-006 independent close-out 审计为 `pass`，无开放 required finding；P-004 裁决由用户完成，选择跳过 self close-out 并接受 F-001～F-003 为 open / recommended residual。
- GOAL-004 以 D-016 和 A-007 留痕后标记为 `done / 100%`；根目标路线图阶段 3 随之完成。F-001～F-003 应在后续对应范围处理，不阻断本次关门。

## 当前进展 / 下一步（历史快照 · 阶段 6 规划起点）

> **不可作现时。** 下表曾写「Web 阶段 6 规划已启动 / 下一编号隐含 009 规划」；**现时**见文件顶部「当前进展（2026-07-28）」与 [00-meta 现时摘要](00-meta.md#现时摘要2026-07-28-单一权威入口)。

| 方向 | 快照状态（过时） | 说明（当时） |
|------|------------------|--------------|
| 核心方法论与模板 | 已完成（GOAL-006） | 核心交付形成；跨面联合发布留给后续 |
| Web 应用 | 阶段 6 规划已启动 | GOAL-009 定义工作台（**其后**有界结项） |
| Skills / 提示词 | 阶段 5 发布一致性已完成 | GOAL-008 关门（**其后** 018/019） |
| 核心数据模型 | 已完成 | GOAL-004 |

当时「下一步」要点（过时）：阶段 6 由 GOAL-009 做规划；按最小工作流另立实现子目标；F-006 recommended 跟踪。

### 2026-07-19 · 根目标重基线与核心模板归属

- 用户确认采用“三层交付、一个真相源”：核心方法论/文档协议与模板、Skills 消费适配器、Web 人类工作台。
- 在 `docs/templates/goal-folder/` 建立 canonical 五件套模板，并保留 `skills/templates/goal-folder/` 作为安装与离线复制镜像。
- 在 GOAL-001 的 `00-meta.md`、`01-decision.md`、`03-audit.md` 与本执行记录中记录 D-007 和本轮重基线；既有 GOAL-002～005 的状态与历史审计未重写。
- Web 的当前边界保持只读；本轮未开放写入，也未提前创建阶段 4 之后的细粒度子目标。
- 运行 `python skills/tests/test_skills_orchestrator.py`：**21 tests OK**，包含 canonical 模板与 Skills 镜像一致性检查、默认 `/govern` + `/audit` 安装面和 PowerShell 隔离安装冒烟。
- 在 `web/` 运行 `..\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v`：**20 tests OK**；1 个符号链接权限相关测试按 Windows 环境能力跳过。
- `git diff --check` 通过；未发现空白错误。
- 对照 `docs/goals/*/00-meta.md` 修正 `goal-tree.md` 的根进度占位和 GOAL-002 完整标题，Web 目标树诊断不再报告这两项既有投影漂移。

### 2026-07-19 · 响应 A-002 的入口边界与阶段 4 契约必改项

- 修正根 [README.md](../../../README.md) 的 Web 描述：当前 Web 直接读取 `docs/goals/`，提供目标浏览与文档树诊断；不维护第二状态层，也不提供 Web 写入、创建/更新或后台同步。
- 在 [D-008](01-decision.md#d-008--阶段-4-产品化与退出契约2026-07-19) 和 [00-meta.md](00-meta.md) 记录阶段 4 的最小交付包、canonical 所有者、独立复制场景、版本/镜像同步、非目标、验收证据及阶段 4 → 5 门槛。
- 复跑 `python skills/tests/test_skills_orchestrator.py`：**21 tests OK**；复跑 `web` 的 `unittest discover -s tests -v`：**20 tests OK**，1 项因 Windows 无创建符号链接权限跳过；`git diff --check` 通过。
- 本次没有改变根目标 `status` / `progress`，没有创建 `GOAL-006`，也没有把阶段 4 标为完成；下一步仅可在 D-008 的边界内决定是否立项。

### 2026-07-19 · 立项阶段 4 核心交付包

- 按用户明确指令创建 [GOAL-006-core-methodology-template-productization](../GOAL-006-core-methodology-template-productization/00-meta.md)，其 `parent` 为 `GOAL-001-main-vision`，初始状态为 `active / 0%`。
- GOAL-006 的范围承接 D-008：核心文档与模板入口、独立复制启用说明、空 Git 仓复制验证，以及 canonical 模板到 Skills 镜像的单向同步记录。
- 本次只完成立项、范围落盘与目标树同步；尚未修改或验证阶段 4 的实际交付物，未将阶段 4 或根目标标记为完成。

### 2026-07-19 · GOAL-006 正式结项

- GOAL-006 完成 A-001 阶段 self 审计、A-002 independent 条件审计、A-003 编排响应、A-004 F-002 targeted independent 复审和 A-005 self close-out。
- F-002 已关闭；F-003 保留为非阻塞 recommended residual。GOAL-006 状态同步为 `done / 100%`，阶段 4 → 5 门槛满足，阶段 5 尚未启动。
- `goal-tree.md` 与 GOAL-001 的阶段/子目标摘要已同步；`0.4.0` 仍绑定无 release tag 的基线 commit，不创建 tag。

### 2026-07-19 · 立项信息就绪协议修订

- 对核心闭环进行自审，确认现有 P-001～P-004 未将目标设立后的信息发现、分阶段收集与信息门禁表达为正式协议。
- 用户确认采用 P-005，并创建 [GOAL-007-information-readiness-governance](../GOAL-007-information-readiness-governance/00-meta.md) 承接该 required 修订。
- GOAL-007 已先写高层路线图与信息需求 I-001；本轮不自动创建“澄清”和“收集”两个子目标，待信息工作量和依赖明确后再按 P-001 判断。

### 2026-07-19 · 完成信息就绪协议修订并关闭 F-004

- [GOAL-007-information-readiness-governance](../GOAL-007-information-readiness-governance/00-meta.md) 已完成 P-005、canonical / Skills 模板镜像、编排与审计 prompts、Claude/Grok/Copilot 安装分发面和契约测试，状态为 `done / 100%`。
- 实施过程中的两轮核验发现并修正信息项等级/延期语义与 Copilot 高级原语同步两个缺口；GOAL-007 A-001 已留下关闭证据。
- 验证结果为 Skills 契约测试 26 项通过（其中两项防止 P-005 退化为仅关键词存在的语义契约）、独立启用测试 3 项通过、Web 回归 20 项通过（1 项因 Windows 符号链接权限跳过），`git diff --check` 通过。
- 本轮未改动 Web 业务代码或 Markdown 数据合同；其测试仅用于确认协议层改动未造成回归。根目标 A-005 据此关闭 A-004 / F-004，当前焦点回到阶段 5 的后续立项。

### 2026-07-19 · 自审并合并响应 A-006

- 用户按 P-004 明确选择“先自审，然后合并响应审计结果”；[A-007](03-audit.md#a-007--goal-001007-组合战略与阶段-5-发布边界自审2026-07-19) 已完成与 A-006 同 scope 的 `source: self` 核验。
- A-007 与 A-006 同为 `conditional`：三层交付、canonical 归属和既有漂移整改记录有效；当前发布证据仍只有工作树版本说明、canonical/mirror 台账与本地测试，不能关闭 `F-005`。
- [D-010](01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19) 已将阶段 5 收敛为一个 Skills 跨宿主/跨版本发布一致性子目标，并登记 I-001～I-003 为 `required / collecting`；Web 深化、真实采用度试点和阶段 7 最终三面发布保持在范围外。
- [A-008](03-audit.md#a-008--合并响应-a-006--a-007-与阶段-5-立项门禁2026-07-19) 已汇总两条意见及用户裁决：P-004 问询已闭环，`F-005` 仍为 `open / required`，`F-006` 仍为 `open / recommended`。
- 本轮实际重跑：编号/字段结构检查通过（D-001～D-010、A-001～A-008、I-001～I-003）；Skills 契约测试 26 项通过；独立启用测试 3 项通过；Web 回归 20 项通过（1 项因 Windows 符号链接权限跳过）；`git diff --check` 通过。
- 本轮只完成审计、决策、信息登记和响应留痕；没有创建 `GOAL-008`，没有修改 GOAL-001 的 `status` / `progress` / `parent`，也没有把阶段 5 发布范围、阶段 7 验收或根目标关门写成已放行。

**本轮下一步（计划）**：用户确认启动时，按 D-010 的边界创建当前下一编号的阶段 5 子目标；其方案冻结前先关闭 I-001，并按受影响门禁继续关闭 I-002 / I-003 与 F-005。

### 2026-07-19 · 按 D-010 创建 GOAL-008

- 用户明确要求按 D-010 创建 [GOAL-008](../GOAL-008-skills-consumer-adapter-release-consistency/00-meta.md)；已创建完整五件套并将其设置为 `draft / 0%`。
- I-001～I-003 的责任已按 D-010 从根目标的暂代登记移交 GOAL-008；三项仍为 `required / collecting`，没有 residual risk 接受。
- 本次只完成阶段 5 子目标设立、边界记录和门禁移交；没有冻结发布范围、进入受影响实施、关闭 `F-005` 或放行阶段 7/GOAL-001 关门。

**下一步（计划）**：GOAL-008 先收集并审视 I-001，之后按 I-002 / I-003 的最晚阶段形成兼容范围、fixtures 与可追溯发行证据。

### 2026-07-19 · 用户确认当前最低可用并延期发布一致性

- 用户确认当前“Skills 能安装、能使用”已经足够；现有 canonical 契约、安装分发测试和三宿主固定版本 current `/govern` dispatch 证据可作为有界最低可用结论。
- 记录 [D-011](01-decision.md#d-011--当前最低可用基线与发布一致性延期2026-07-19)：I-002、I-003 和 `F-005` 保持 `required`，但在当前没有对外/可复现发布或新增宿主/版本计划时为 `deferred`；本轮没有接受 residual risk、关闭 F-005 或改变 GOAL-001 / GOAL-008 状态。
- `GOAL-008` 的 [D-004](../GOAL-008-skills-consumer-adapter-release-consistency/01-decision.md#d-004--当前最低可用基线与发布一致性延期2026-07-19) 与 [A-008](../GOAL-008-skills-consumer-adapter-release-consistency/03-audit.md#a-008--当前最低可用裁决与发布一致性延期响应2026-07-19) 已记录最低可用边界、责任人与触发；首次对外/可复现发布时先恢复 I-003 / F-005，首次支持新宿主/版本时先恢复 I-002。
- 对本轮治理记录运行 Skills 契约测试（30 passed）、独立启用测试（3 passed）和 Web 回归（20 passed / 1 Windows symlink-permission skipped）；`git diff --check` 无空白错误。

### 2026-07-19 · 用户重启阶段 5 完整关门

- 用户确认“核心文档体系 → Skills 体系 → Web 体系”的顺序，并要求重启 GOAL-008 的完整关门；记录 D-012 与 GOAL-008 D-005，不重写 D-011 的历史最低可用事实。
- 当前机器的 Claude Code `2.1.215`、Grok Build `0.2.103 (89c3d36fb6)`、VS Code `1.129.1` / built-in Copilot Chat `0.57.0` build `1` 已作为候选基线发现并留存到 GOAL-008 执行记录。
- I-002、I-003 与 F-005 由 `deferred required` 恢复为 `collecting / required`；本次尚未关闭门禁、创建 release tag 或启动 Web 深化。

### 2026-07-19 · GOAL-008 完成发布自动化基础并响应 A-010

- GOAL-008 已实现 canonical/Skills compatibility matrix、current/negative 基线、Ubuntu/Windows CI、兼容与发行报告工具、release evidence schema、CHANGELOG 与 rehearsal；对应执行事实已写入其 `02-execution.md`，并以 A-011 响应独立 A-010。
- A-010 F-001（执行台账漂移）、F-004（历史 verified 与候选 readiness 误读）、F-005（摘要过时）已有关闭证据；GOAL-008 保持 `active / 20%`，goal-tree 状态与进度无需变化。
- I-002 仍有三宿主 `/govern` / `/audit` 六个候选 runtime 单元和 Web parser CI replay 共 7 个 uncovered；I-003 仍无 ready coverage、干净 release commit 与 annotated tag/release。根目标 F-005 因而继续 `open / required`。
- 本地最终验证：发行工具 19 项、Skills 31 项、standalone 3 项、Web 20 项通过（1 项 Windows symlink 权限跳过）；完整 rehearsal 的 5 个固定 checks 全部通过，但报告仍为 coverage pending / 7 uncovered、`candidateRevision: unreleased`、工作树不干净。
- Web 深化仍按 D-012 后置；本轮没有创建 Web 目标、tag、commit、push 或 release。

### 2026-07-19 · GOAL-008 验证 Claude/Grok 候选双入口

- GOAL-008 以 D-008、执行记录和 A-013 建立 runtime evidence schema、捕获器、陈旧/摘要/timeout 门禁与 Claude 脱敏 transcript；Claude Code 与 Grok Build 的 `/govern`、`/audit` 四个候选单元现为 `runtime-verified`。
- Grok 主 `grok-4.5` 调用均通过；可选 session-title `grok-build` alias 的 502 作为 warning 保留，不将辅助失败扩大为主 dispatch 失败。具体 endpoint/model 配置保留在 GOAL-008 附件，不污染根 `AGENTS.md`。
- compatibility report 从 7 个 uncovered 缩小为 3 个：Copilot `/govern`、Copilot `/audit` 与 Web parser CI replay。完整 rehearsal 5/5 checks 通过；Skills 31、standalone 3、scripts 30、Web 20 项通过，1 项 Windows symlink 权限跳过。
- I-002 仍为 `collecting / required`，I-003 仍缺 ready coverage、干净候选和 annotated tag；根 F-005 继续 `open / required`。本轮没有 status/progress 变化，也没有 commit、push、tag 或 release。

## 2026-07-22 · 阶段 6 有界结项审视（不关 Root）

- 用户：`/govern 在 GOAL-001 记录阶段 6 有界结项审视（不关 Root；R-009-X 仍 accepted）`。
- [D-015](01-decision.md#d-015--阶段-6-有界结项审视不关-rootr-009-x-仍-accepted2026-07-22) / [A-014](03-audit.md#a-014--阶段-6-有界结项审视2026-07-22)。
- **有界结项**：阶段 6 Web 工作台在有界交付意义上完成（009 + 012～017）。
- Root **仍 active**；**R-009-X 仍 accepted**；**未**宣称阶段 6 终态或 Root done。
- 阶段 7 / residual 产品 / 人手 UX 全文等仍可另立或触发。
