---
id: D-011
goal: GOAL-008-consumer-layer-split-and-hosting
doc: decision-entry
record_id: D-011
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# D-011 · S6 发布范围冻结（I-006）与版本选择（2026-09-13）

**状态**：accepted

**触发**：S1～S5 完成，S6 进入前必须先冻结发布范围（I-006，[A-001](D-002-a001-response.md) F-005 的闭合依据）。用户在两项 P-004 裁决中选择：
- **S6 范围 = B「含正式发布」**（全量回归 + 冻结 revision 上重捕获 runtime 证据 + 宿主探针 + cross 关门审计 + 版本/资产/发布）；
- **开放 required 处理 = 分轮推进，本轮不接受残余**（不得以 residual 提前关门）。

## 决定

### 1. 版本与 revision

| 项 | 值 | 依据 |
|----|-----|------|
| 发布版本 | **`0.13.3`** | `CHANGELOG.md` 当前最高 `0.13.2`（2026-08-11）；`docs/README.md` 台账同为 `0.13.2` → 下一个补丁版本 |
| tag | **annotated `v0.13.3`**，指向**合入 `main` 后的 merge commit** | 沿用 GOAL-005/GOAL-007 的既有发布纪律（tag 不得指向未合入的 `dev` 提交） |
| revision 冻结 | **待定**：S6 全部实施与审计完成后，以 `main` 上的 merge commit hash 作为发布 revision | 证据锚点必须与发布 revision 一致（见 §4） |
| CHANGELOG | 在 `## Unreleased` 内新增 `0.13.3` 条目，覆盖 S1～S5 的协议/模型/安装面/Skills 变更 | 发布门禁要求 CHANGELOG 版本存在 |

### 2. 资产清单（沿用 v0.13.2 的既有集合）

| # | 资产 | 说明 |
|---|------|------|
| 1 | `goal-governance-skills-0.13.3.zip` | Skills 分发包 |
| 2 | `goal-governance-skills-0.13.3.zip.sha256` | 摘要 sidecar |
| 3 | `goal-governance-core-0.13.3.zip` | core 文档包（可选发布物） |
| 4 | `goal-governance-core-0.13.3.zip.sha256` | 摘要 sidecar |
| 5–9 | workflow 上传的 compatibility report / release evidence / 校验文件 | 由 `skills-pack-release.yml` 的 publish job 产出（以实际上传为准，不得事后补记） |

**规则**：实际资产以 tag workflow 上传结果为准；核对时逐项重下载并比对 sha256，**不得**把计划清单写成已上传事实。

### 3. 回归矩阵（S6 必跑，任一失败即阻断发布）

| 套件 | 命令 | 通过阈值 |
|------|------|----------|
| 镜像 stage 门禁 | `python scripts/stage_skills_mirrors.py` → `--check` → `git diff --exit-code -- skills/core skills/contracts skills/templates` | 0 漂移（CI 同名门禁） |
| Skills 编排/安装 | `python -m unittest discover -s skills/tests -p 'test_*.py'` | 全绿 |
| docs 协议/愿景/入口 | `python -m unittest discover -s docs/tests -p 'test_*.py'` | 全绿 |
| scripts（打包/更新/证据） | `python -m unittest discover -s scripts/tests -p 'test_*.py'` | **全绿**（当前 4F/12E 的 runtime 证据过期项必须在 §4 重捕获后转绿） |
| 空白/行尾 | `git diff --check` | 0 命中 |
| compatibility 就绪 | `python scripts/compatibility_report.py --require-ready` | 通过 |
| release rehearsal | `python scripts/release_evidence.py --mode rehearsal --run-checks --compatibility-report artifacts/compatibility-report.json --output artifacts/…` | 通过 |

### 4. Runtime 证据重捕获（A-005 F-002 的闭合路径）

- **触发原因**：S2 改根 `AGENTS.md`、S4 改三个规则源面 → `docs/releases/runtime/v0.13.2/` 12 份证据 `behaviorSources` 全部过期（`capture_runtime_evidence.py --check` 12 problems）。
- **落点**：`docs/releases/runtime/v0.13.3/<host>-<entrypoint>-2026-09-13.json`（新版本目录，**不改写** v0.13.2 历史快照）。
- **覆盖**：`claude-code-cli` / `grok-build-cli` / `github-copilot-cli` × `govern` / `audit` / `vision` / `vision-audit` = 12 格；每格须 `verdict=pass`、marker 观测成立、条目 token 出现、stdout 非平凡。
- **版本漂移处理**：宿主 CLI 版本可能与 v0.13.2 捕获时不同（如 grok 由 `1.0.0` 升至 `1.0.30`）。捕获时**如实记录**当前版本，并同步更新 `skills-consumer-compatibility-matrix.json` 的 `candidateRevision` / 版本字段与 `docs/contracts/skills-consumer-contract.json` 的证据路径；**不**把旧版本数字保留成已过期事实。
- **便利入口单列**：`/commit` **不进入** 12 格矩阵（它不是治理必达入口）；其行为证据以独立条目标注为非必达，避免污染必达集（[D-010](D-010-s5-commit-entry.md) §2）。
- **测试日期断言**：`skills/tests/test_skills_orchestrator.py` 现断言证据文件名含 `-2026-08-`；重捕获后必须改为**按实际捕获月份**断言（或改为从证据路径解析月份），否则门禁与事实脱节。

### 5. cross 覆盖面与证据归属

| 类别 | 内容 | 归属 |
|------|------|------|
| self | 各阶段 A-004 / A-005 / A-006 / A-008 / A-009 与 S6 关门自审 | 本目标 `03-audit/` |
| independent | 现有 A-001 / A-003 / A-007（provider = grok build）；**S6 关门需新增一次 independent**（S6 为发布面高影响，按 P-003 需 `cross`） | 本目标 `03-audit/A-0NN-*.md`，`source: independent`，provider 标注 |
| consumer 侧证据 | 隔离消费仓冷启动/升级实测（`attachments/s6-isolated-consumer-evidence.md`） | 本目标 `attachments/` |
| producer 侧证据 | runtime 证据、compatibility report、release evidence、pack 摘要 | `docs/releases/`、`artifacts/`（发布轮） |

**禁止**：以 producer 侧证据顶替 consumer 侧；以任何 checkpoint/hash 替代审计或发布通过证据。

### 6. 本轮（S6 首轮）范围

- **做**：本决定（I-006 冻结）、全量回归、grok 宿主证据重捕获（4 格）、隔离仓实测归档、S6 自审。
- **未完成即不得关门**：其余 8 格（claude / copilot）重捕获、compat 报告与 rehearsal、S6 independent 关门审计、版本落地、PR/merge/tag/Release。
- 用户已明确「分轮推进，本轮不开残余」→ 上述未完成项保持 **open required**，不得以 residual 关门。

## 为什么

- 发布版本的选择有唯一可判定依据（CHANGELOG/台账最高版本 + 1 补丁位），属可静默执行的常规动作；但**是否发布**与**如何处置残余**已由用户裁决（P-004）。
- 证据必须在**冻结 revision** 上重捕获，否则发布时锚点再次失效；因此把版本、tag 语义、资产集合与证据目录一次性写入 I-006 冻结，避免发布轮反复。
- 把「宿主 CLI 版本漂移」显式写入决定，是为了避免两种错误：沿用旧版本数字（失真）或只更新证据文件而不更新契约/矩阵（不一致）。
- `/commit` 单列而非并入矩阵，直接来自 D-002 §4 的必达/便利边界。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| `0.14.0`（minor） | 本批为协议措辞/判定谓词/安装面与入口补齐，未新增能力域；补丁位更贴合既有实践（GOAL-005～007 亦为补丁位发布） |
| 复用 `v0.13.2` 目录就地刷新证据 | 会改写历史快照，破坏「证据绑定发布时点」的既有纪律 |
| 把 `/commit` 并入 12 格矩阵 | 会把它升格为必达证据面，违反 D-002 §4 与 D-010 §6 |
| 本轮以 residual 接受未完成项并关门 | 用户明确选择「分轮推进，不开残余」 |
| 先发 Release 再补证据 | 违反 producer 发布门禁（证据过期时 `--require-ready` 失败，本就 fail closed） |

## 影响

- I-006 由此**冻结**（A-001 F-005 的闭合依据待 S6 实际产出后判定）。
- S6 通过阈值、证据路径与 cross 覆盖面以本决定为准。
- 后续 S6 轮次必须按 §3～§5 执行；任何偏离（改版本、改资产集合、跳过 independent）须回到用户并留痕。
