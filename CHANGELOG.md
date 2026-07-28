# Changelog

所有可发布变更以 annotated SemVer tag 和对应的 release evidence 为准。工作树中的“Unreleased”内容不构成发布声明。

## Unreleased

- （无尚未绑定 tag 的变更）

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
