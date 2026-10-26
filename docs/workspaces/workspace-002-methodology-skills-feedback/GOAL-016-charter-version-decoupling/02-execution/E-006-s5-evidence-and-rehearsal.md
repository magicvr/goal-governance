---
id: E-006
goal: GOAL-016-charter-version-decoupling
doc: execution-entry
title: S5 v0.13.8 证据重捕获、清单与严格预检
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

# E-006 · S5 v0.13.8 证据重捕获、清单与严格预检（2026-10-26）

## 已发生事实

### 运行证据

1. 从 GOAL-015 的 S5 驱动派生 [s5-host-probes.py](../attachments/s5-host-probes.py) 与 [s5-run-captures.ps1](../attachments/s5-run-captures.ps1)，仅改目标说明、日期、证据目录与 Claude 可选模型/effort 参数；探针正文仍是正式命令形式（合成夹具 `/audit workspace-002 goal-013`、`/vision-audit vp-002`），不附加 scope/结论预期。
2. 在 `docs/releases/runtime/v0.13.8/` 采集 **16 格**：
   - 3 宿主（Claude Code CLI 2.1.310 / Grok Build CLI / GitHub Copilot CLI）× 4 治理入口；
   - 4 宿主（Claude / Grok / Copilot / Codex）MCP 目录探针；
   - 16 格全部 `verdict=pass`、`exitCode=0`、marker 观测。
3. 失败重试事实：
   - Claude audit 首轮因宿主 `Glob` 对 `architecture/*.md` 返回 0 而误判架构文件不可用，未写台账；重试仍出现同样 `Glob`/不写台账。最终以 `--claude-model gpt-6.1-sol --claude-effort high` 重取 **`claude-code-cli-audit-2026-10-26-r5.json`**，`pass`，实际写入 `03-audit.md` 与 A-001。矩阵记录实际 host/model；这不是命令形式或协议失败。
   - Copilot audit 首轮把 `.gitkeep` 写入 `01-decision`/`02-execution`/`attachments`，边界检查 `fail`；`--attempt 02 -r2` 重取后只写 `03-audit`，`pass`。
   - 其余 14 格首轮 `pass`。
4. `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.8`：**evidence consistency ok**（含所有落盘证据，包括失败重试的历史文件）。
5. 矩阵 `docs/contracts/skills-consumer-compatibility-matrix.json`：`candidateRevision` = `v0.13.8`；12 条入口证据指向新目录（Claude audit = `-r5`，Copilot audit = `-r2`）；3 处 `evidenceScope` 更新为 GOAL-016/issue #34 与 Claude 模型覆盖说明；`skills/contracts` 镜像由 stage 同步。

### 版本清单与门禁

6. `CHANGELOG.md` 新增 `0.13.8 - 2026-10-26` 节并复位 `Unreleased`；根 `README.md`、`skills/README.md`、`scripts/bootstrap/README.md`、`mcp/README.md`、`docs/releases/README.md` 的安装/GHCR pin 改为 `v0.13.8` / `0.13.8`（BOM 已清除）。
7. `.github/workflows/skills-pack-release.yml` 的 evidence dir、`scripts/tests/test_pack_skills_release.py`、`scripts/tests/test_release_evidence.py`、`skills/tests/test_skills_orchestrator.py` 的版本/路径断言改为 v0.13.8。
8. `python scripts/compatibility_report.py --output <tmp>`：`coverage status: ready-for-release-evidence`，exit 0。
9. `python scripts/release_evidence.py --mode rehearsal --run-checks --compatibility-report <tmp>/compat-v0138.json --output <tmp>/release-evidence-v0138.json`：`release status: rehearsal`、**`checks passed: True`**、exit 0。为避开 `.venv` Python 3.14.6 下 `test_skills_update` 的 `mktemp` 权限失败，运行前把 `.venv` 临时改名、使用系统 Python 3.11.9，结束后立即恢复；这是本机解释器选择，不是仓库改动。
10. 镜像：`stage_skills_mirrors.py --check` 38 对一致；`git diff --check` 干净。

### 尚未完成

- 尚未提交 release 候选；尚未 push/PR/CI；尚未合并 `main`；尚未创建/推送 annotated tag；尚未触发 gated Release；Environment `release` 审批与 9 项资产验收尚未发生；issue #34 未关闭；GOAL-016 未 `done`。
- 未把 rehearsal 的 `checks passed: True` 当作正式发布身份。

## 证据路径

- 运行证据：`docs/releases/runtime/v0.13.8/`
- 矩阵：`docs/contracts/skills-consumer-compatibility-matrix.json`（镜像 `skills/contracts/...`）
- 清单：`CHANGELOG.md`、根 `README.md`、`skills/README.md`、`scripts/bootstrap/README.md`、`mcp/README.md`、`docs/releases/README.md`
- 驱动：`GOAL-016/attachments/s5-host-probes.py`、`s5-run-captures.ps1`
