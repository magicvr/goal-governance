# Changelog

所有可发布变更以 annotated SemVer tag 和对应的 release evidence 为准。工作树中的“Unreleased”内容不构成发布声明。

## Unreleased

（无。当前候选已冻结为 **0.12.0** / `v0.12.0`。）

## 0.12.0 - 2026-08-04

Skills **consumer** minor：把真实消费反馈闭成可发布能力，包括 producer / consumer 证据分层、可扩展 ledger、风险分级审计、安全 checkpoint 与事务型 Skills updater（workspace-002 GOAL-003）。

### 更新 / 分发

- 新增 `skills/update.py`、`update.ps1`、`update.sh`：支持固定版 / latest、在线 Release / 离线 zip、SHA-256、协议 minor 预检、managed-file 冲突检查、备份与失败自动恢复。
- 默认消费包只携带 consumer contract + schema；compatibility matrix、runtime-evidence schema 与 release evidence 保持 producer-only，消费仓不再继承生产发布门禁。
- 根 README、Skills README 与 bootstrap README 的固定安装示例同步到 `v0.12.0`；Skills README 增加安装后更新入口。

### 治理协议 / 长流程

- 新目标从第一条记录起使用 `01-decision/`、`02-execution/`、`03-audit/` 平铺 ledger；legacy inline 继续兼容读取。
- 审计模式按 `none` / `self` / `independent` / `cross` 风险分级；required finding、冲突与 residual 继续按 P-004 fail closed。
- `/govern` 长流程在可验证节点使用显式 owned paths 创建 Git checkpoint；脏树重叠、验证失败或提交失败时停止自动提交。

### 兼容矩阵 / 证据

- 矩阵 `candidateRevision: v0.12.0`；Claude Code `2.1.220`、Grok Build `0.2.118` 与 GitHub Copilot CLI `1.0.75` 的四入口于 2026-08-04 重新执行，共 12 个单元 `runtime-verified`。
- 版本化 runtime evidence 位于 `docs/releases/runtime/v0.12.0/`，其行为源与 stdout/stderr 摘要由 canonical 校验器复核。
- Web parser 保持 `automated-verified`；Codex 继续只声明 install surface，不进入本次 committed/runtime-verified 矩阵。

## 0.11.0 - 2026-07-31

Skills **consumer** minor：新增 **OpenAI Codex** 安装面（GOAL-002 · workspace-002）+ 入口 1 bootstrap 文档 pin 同步最新正式 tag（GOAL-023 D-003）。三宿主四入口 runtime 证据沿用 2026-07-30；本版**不**宣称 Codex 为矩阵 `committed` / `runtime-verified`。

### 宿主 / 安装（GOAL-002）

- 包内 `skills/install/codex/skills/{govern,audit,vision,vision-audit}/SKILL.md` → 消费方 `.agents/skills/*`（官方 REPO skill 根）。
- `install.ps1` / `install.sh`：`-Codex` / `--codex`；**`-All` / `--all` 纳入 Codex**（与 Claude / Grok / Copilot 并列）。
- 主入口 `$govern` 只读 dispatch 探针（Codex CLI · 目标附件证据链）；**非**矩阵单元、**非**写盘 e2e。

### 文档 / pin（GOAL-023 D-003）

- 入口 1 bootstrap 示例 pin **`v0.11.0`**（Release 固定 tag URL；禁止 branch raw 作权威入口）。

### 兼容矩阵 / 证据

- 矩阵 `candidateRevision: v0.11.0`；四入口 × 三宿主（Claude / Grok / Copilot）仍为 **runtime-verified**（证据路径 2026-07-30；behaviorSources 对现树 fresh）。
- 刷新 12 份 2026-07-30 runtime evidence 中 `AGENTS.md` behaviorSource digest（`docs(agents)` 后树变更；**未**全量重采宿主会话；R-021-RUNTIME-RECAPTURE residual 仍 open）。
- Web parser 保持 automated-verified。
- **Codex 不在 matrix 声明面**（I-003 residual / non-blocking）：install surface shipped only。

### 非目标（本 tag 不宣称）

- Codex 矩阵 `committed` / `runtime-verified` 或四入口全量 runtime 重采。
- Root / 阶段 6 产品终态；R-009-X closed；F-006 外部采用。
- `/vision-audit` 写盘全路径 e2e。

## 0.10.0 - 2026-07-30

Skills **consumer** minor：执行链加固 + 方法论镜像 stage SSOT + **双资产分发与双入口安装**（GOAL-021～023）。宿主四入口 runtime 证据沿用 2026-07-30 行为源 capture（源 digest 仍匹配现树）；本版不宣称 Root 终态。

### 分发 / 安装（GOAL-023）

- **双资产**：`goal-governance-skills-vX.Y.Z.zip`（内嵌 core）与并行 **`goal-governance-core-vX.Y.Z.zip`**（core-only / standalone）。
- **双入口**：Release/bootstrap 在线脚本（`install-online.ps1` / `install-online.sh`）与包内 `install.ps1` / `install.sh`；在线默认下 skills zip（含 core），**不**强制再拉 core。
- CI / Release 路径挂载 skills + core + digests + bootstrap 脚本。
- bootstrap 相对路径 zip 相对**进程 CWD** 解析；digest 失败 fail closed。

### 方法论镜像 SSOT（GOAL-022）

- `scripts/stage_skills_mirrors.py`：从 `docs/` stage 到 `skills/core/docs/` 与 `skills/contracts/`；pack/CI 强制 stage + dirty-tree 门禁。
- `skills/templates/` 收敛为指针；包内权威模板源为 `skills/core/docs/templates/`。

### 执行链加固（GOAL-021）

- runtime 证据断言策略 `marker+entrypoint+nontrivial-stdout@1`；兼容性报告重算 stdout，拒绝 marker-only。
- pack 拒绝 symlink 逃逸；install 增加 force / non-interactive / dry-run。
- 愿景/工作区校验收紧（active Charter、plan_refs、Root on disk 等）。

### 兼容矩阵 / 证据

- 矩阵 `candidateRevision: v0.10.0`；四入口 × 三宿主仍为 **runtime-verified**（证据路径 2026-07-30；behaviorSources 对现树 fresh）。
- Web parser 保持 automated-verified。
- residual（non-blocking）：R-021-RUNTIME-RECAPTURE（若要以新断言 payload 作唯一正式证明可另拍全量重采）、R-021-SYMLINK-CI、R-022-ORPHAN-PRUNE、R-022-INSTALL-TEMPLATES-COPY、R-023-BASH-HOST。

### 非目标（本 tag 不宣称）

- Root / 阶段 6 产品终态；R-009-X closed；F-006 外部采用。
- bootstrap 安装后再宿主 slash 全路径 e2e 作为 matrix 单元。
- `/vision-audit` 写盘全路径 e2e。

## 0.9.2 - 2026-07-30

Skills **consumer** patch：默认**四入口**面（`/govern` `/audit` `/vision` `/vision-audit`）全矩阵 runtime 证据 + P-006 愿景栈与路径 D 协议卫生。

### 入口 / runtime

- 默认 install 与契约 `requiredEntrypoints`：govern + audit + vision + **vision-audit**。
- 独立入口：`skills/prompts/07-independent-vision-review.md`；三宿主 wrapper；`/vision-audit` 只写 `docs/vision/reviews.md`。
- 兼容矩阵：四入口 × Claude Code `2.1.220` / Grok Build `0.2.114` / Copilot CLI `1.0.75` 均为 **runtime-verified**（**2026-07-30** 对当前行为源重采；Copilot BYOK；`/vision-audit` 为只读 dispatch，非写盘 e2e）。
- Web parser 保持 automated-verified。
- 矩阵 `candidateRevision: v0.9.2`；coverage **ready-for-release-evidence**。

### 协议 / 愿景 / 路径 D

- P-006 愿景栈 dogfood：Charter / VP / alignment / Vision Review；V-F-001～V-F-007 editorial fixed。
- GOAL-001 路径 D（仅维护不关 Root）：A-015 F-007/F-008 fixed；A-018 F-012～F-015 fixed；GOAL-020 methodology adversarial audit fix done。
- 文档卫生：`skills/README` 装机树/手动安装对齐四入口；Goal 历史「三入口」叙述加现时注（D-018→D-020）。
- standalone / core 分发含 `vision/alignment.md`；权威面与 AGENTS 门禁语义对齐 P-006。

### 发布热修（同 tag 内容补丁 · 2026-07-30）

- 修正 runtime evidence 的 stdout/stderr/behaviorSource **SHA-256** 与 git `text eol=lf` 一致（Windows 采集时 CRLF 哈希导致 Linux CI `stdout digest is stale`）。
- `capture_runtime_evidence` / `compatibility_report` 统一按 LF 落盘与比对，避免再发版门禁假失败。

### 非目标（本 tag 不宣称）

- Root / 阶段 6 产品终态；R-009-X closed；F-006 外部采用。
- `/vision-audit` 写盘全路径 e2e。

## 0.9.1 - 2026-07-28

Skills **consumer** patch：跨区目标限定引用（A0）+ 同窗口治理/愿景澄清；六 CLI runtime 对当前行为源重采。

### 协议 / Skills（A0 · GOAL-010 D-003）

- 工作区协议 **0.5.0** §2.6：短 `GOAL-*` id 不变；跨区限定引用 **Q1**（双字段）/ **Q2**（canonical 路径，**文档默认**）/ **Q3**（行内标签，**对话默认**）；禁止把工作区编号嵌进 goal id。
- 根 `AGENTS.md` / `skills/AGENTS.template.md` **0.9.2**；编排器 `00` 与原语 `01`～`05` 对齐工作区页眉与 Q2/Q3 纪律。
- `skills/core` 镜像同步 protocol / directory-layout / docs README。

### 治理面（同窗口合入）

- finding 三路径闭合与愿景门禁澄清（principles / AGENTS / 编排器）。
- Charter → VP → 工作区愿景对齐体系。

### 兼容矩阵 / 证据

- 矩阵 `candidateRevision: v0.9.1`。
- Claude Code CLI `2.1.220` `/govern` + `/audit`：2026-07-28 **runtime-verified**。
- Grok Build CLI `0.2.112` `/govern` + `/audit`：2026-07-28 **runtime-verified**（CLI 子进程 + proxy-managed key）。
- GitHub Copilot CLI `1.0.71` `/govern` + `/audit`：2026-07-28 **runtime-verified**（GitHub 月度配额耗尽时经 `COPILOT_PROVIDER_BASE_URL` BYOK 走 OpenAI-compatible 代理；宿主仍为 Copilot CLI）。
- Web parser 保持 automated-verified。
- 六 CLI 入口 coverage **ready-for-release-evidence**。

## 0.9.0 - 2026-07-24

Skills **consumer** release 候选（GOAL-019）：**核心方法论与 Skills 同级必备** + 消费方工作区骨架。

### 消费包 / install

- skills zip 内嵌 `skills/core/`（principles、workspace-protocol、overview、directory-layout、templates、精简 docs/README；**不含** tech-stack / dogfood）。
- `install.sh` / `install.ps1` **默认**将 core 安装到目标仓 `docs/architecture/`、`docs/templates/`、`docs/README.md`。
- 可选 `--init-workspace` / `-InitWorkspace`（须显式 `--workspace-slug` + `--root-slug`；只建 `workspace.md` + `goal-tree.md`，不建 Root 五件套；路径已存在则 refuse）。
- 编排器 S0 / 原语 01：空仓先 scaffold 工作区再立 Root；slug 禁止静默默认。
- AGENTS / 宿主 wrappers：architecture 必备与「不完整安装」话术；pack required 校验 core。

### 兼容矩阵 / 证据

- 矩阵 `candidateRevision: v0.9.0`。
- GitHub Copilot CLI `1.0.71` `/govern` + `/audit`：2026-07-24 **runtime-verified**。
- Grok Build CLI `0.2.111` `/govern` + `/audit`：2026-07-24 **runtime-verified**（CLI 子进程 + proxy-managed key）。
- Claude Code CLI `2.1.218` `/govern` + `/audit`：2026-07-24 **runtime-verified**。
- Web parser 保持 automated-verified。
- 六 CLI 入口 coverage **ready-for-release-evidence**（正式 annotated tag 前置条件）。

### 治理

- GOAL-019 有界关门（D-003～D-007；A-001 independent + A-002 self）。

## 0.8.0 - 2026-07-22

Skills **consumer** release（安装包与宿主入口；**不**要求 Web 产品功能完成）。

- Tag 发布路径：`.github/workflows/skills-pack-release.yml` 在 annotated `v*` 上 pack 后，经 Environment `release` 与硬 `release_evidence --mode release` 门禁，自动 `gh release create` 并挂 skills zip / sha256 / evidence。
- Skills 消费 zip 打包入口：`scripts/pack_skills_release.py`；消费/维护者文档见 `skills/README.md`、根 `README.md`、`docs/releases/README.md`。
- 兼容矩阵 `candidateRevision: v0.8.0`；Claude Code / Grok Build / Copilot CLI 的 `/govern` 与 `/audit` 六单元以 2026-07-22 机读 runtime evidence 重新验证；Web parser 保持 automated-verified（CI/parser 检查，非产品终态）。
- 工作区协议与 Skills 适配（GOAL-010）、Release 打包与自动发版路径（GOAL-018）纳入本 skills 发布面。

## 0.7.0 - 2026-07-20

- 完成 Skills 消费适配器兼容矩阵、GitHub Copilot CLI runtime replay、Web parser CI replay 与 release evidence 链路。
- 以 annotated `v0.7.0` tag、clean candidate commit 和内部 checks 绑定可追溯候选证据。
