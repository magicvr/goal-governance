---
id: GOAL-015-audit-command-labeled-form
doc: execution-entry
record_id: E-007
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-007 · S5 步骤 b–e：清单、本地门禁、PR/CI、merge 与 tag

## 2026-10-17 · 已发生事实

1. **清单与边界文档**：`CHANGELOG.md` 新增 `0.13.7` 节并把 `Unreleased` 复位；`docs/README.md` 的 GOAL-015 边界补记改写为「v0.13.7 候选 + 16 格重捕获已通过」；安装/GHCR pin、矩阵、CI 证据目录与测试断言已在 [E-006](E-006-s5-evidence-recapture.md) 记录。
2. **本地门禁（系统 Python 3.11.9）**：skills `Ran 102 tests … OK`、docs `Ran 67 tests … OK`、scripts `Ran 147 tests … OK (skipped=4)`——S3 记录的 4 failures / 12 errors 随证据转绿消失；`capture_runtime_evidence --check --evidence-dir docs/releases/runtime/v0.13.7` → `ok (22 evidence file(s))`；`compatibility_report` → `ready-for-release-evidence`、`uncovered: 0`；`release_evidence.py --mode rehearsal --run-checks` → **`checks passed: True`**、exit 0（4/4 内部检查）。`.venv`（3.14.6）按 GOAL-014 E-002 的环境配方临时移出以让子进程回落到系统解释器，执行后立即恢复（`leftover: False`）；未改产品代码或测试来掩盖差异。
3. **检查点**：`8f1315f` `release: prepare v0.13.7 manifests and recaptured runtime evidence`（250 files changed, +40406/−78）。
4. **PR**：分支 `codex/release-v0.13.7` 推送后开 [PR #31](https://github.com/magicvr/goal-governance/pull/31)（base `main`）。CI run [39034452347](https://github.com/magicvr/goal-governance/actions/runs/39034452347) 双 job 全绿：`contract-and-report` pass 55s、`windows-install-surface` pass 3m6s。
5. **合并**：`gh pr merge 31 --merge` → main merge commit **`6ca04ee1cb07ae4b5efe1d0e06bed08524bdd2d1`**；本地 `main` 快进同步到该 commit，工作树干净（`git status --porcelain` 为空）。
6. **Strict 发布预检（在 merge commit 上）**：重生成 compatibility report（`ready-for-release-evidence`）后执行 `release_evidence.py --mode release --tag v0.13.7 --run-checks` → **`release status: release-candidate`、`checks passed: True`**、exit 0；`source.commit = 6ca04ee…`、`workingTree.clean = true`。同样使用「`.venv` 移出 + 系统 3.11.9」的配方，随后恢复。
7. **Annotated tag**：`v0.13.7`（tag object **`6197ed6ea4f720d0d0a966665e75b7821d0a5df5`** → commit `6ca04ee…`）已推送；推送前 `git ls-remote --tags origin v0.13.7` 为空（新 tag，未移动既有 tag）。
8. **Tag workflow** [39034827440](https://github.com/magicvr/goal-governance/actions/runs/39034827440)：`pack` **completed / success**（12 s，含 M-001 证据一致性门禁、pack 单测与两个 ZIP，artifact `skills-pack-0.13.7`）；`Publish GitHub Release (gated)` 状态 **waiting**——等待 Environment `release` 的**人工审批**。
9. **未做（不得写成已发生）**：Environment 审批由维护者人工完成，AI 未代批、未改环境配置；Release 尚未发布；资产验收（数量、双 ZIP 摘要与 sidecar、Core⊂Skills、隔离消费安装、GHCR digest 与内置版本）待发布后执行。

### 证据

| 主张 | 路径 / 命令 |
|------|-------------|
| 本地门禁全绿 | 三套 unittest 摘要；`capture_runtime_evidence --check`；`compatibility_report`；`release_evidence --mode rehearsal --run-checks` |
| 检查点 | `git log --oneline` → `8f1315f` |
| PR CI 全绿 | `gh pr checks 31`：contract-and-report pass、windows-install-surface pass |
| merge commit | `git log -1 origin/main` → `6ca04ee1cb07ae4b5efe1d0e06bed08524bdd2d1` |
| strict 预检 | `release_evidence.py --mode release --tag v0.13.7 --run-checks` → `checks passed: True`；`artifacts/gg015-release-evidence-main.json`（本地忽略目录） |
| tag 身份 | `git for-each-ref refs/tags/v0.13.7` → tag `6197ed6e…` → `6ca04ee…`；`git ls-remote --tags origin v0.13.7` |
| pack 成功、publish 等待审批 | `gh run view 39034827440`：`pack` success；`Publish GitHub Release (gated)` waiting |
