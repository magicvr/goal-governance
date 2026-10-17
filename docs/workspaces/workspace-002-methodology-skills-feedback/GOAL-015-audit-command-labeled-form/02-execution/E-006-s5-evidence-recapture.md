---
id: GOAL-015-audit-command-labeled-form
doc: execution-entry
record_id: E-006
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-006 · S5 证据重捕获（11/16 pass；Copilot 5 格阻塞于 provider 认证）

## 2026-10-17 · S5 步骤 a：16 格运行证据重捕获

### 已发生事实

1. **驱动**：从 GOAL-013 的 `s3-host-probes.py` 派生 [s5-host-probes.py](../attachments/s5-host-probes.py)（9 处精确替换：fixture 前缀 `gg-goal015-s5-`、输出目录 `s5-runtime`、test 标签、以及**探针正文改为带标签命令** `/audit workspace-002 goal-013` 与 `/vision-audit vp-002`，含 MCP catalog 的 task 正文）；批量脚本 [s5-run-captures.ps1](../attachments/s5-run-captures.ps1)。派生前以 `--prepare-only` 校验 fixture 与输入（`input.txt` = `/audit workspace-002 goal-013`）。
2. **目标单元**：3 宿主 × 4 治理入口 = 12 格 + 4 宿主 MCP 目录探针 = 16 格，写入 `docs/releases/runtime/v0.13.7/`。
3. **环境失败（两次，均无状态写入）**：直接 `& script.ps1` 被执行策略拒绝；改用 `pwsh -File` 又因该会话 PATH 无 `pwsh` 失败（本会话 PowerShell 为 Windows PowerShell 5.1）。第三次以 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File` 成功启动四宿主并行捕获。
4. **首轮结果**：**11 pass**——claude govern / vision / vision-audit / catalog、grok 四入口 + catalog、codex catalog，以及 claude audit 的重试 `-r2`；claude audit 首轮失败后重试通过；GitHub Copilot CLI 5 格失败（原因见第 6 条，已更正）。
5. **claude audit 首轮失败原因（已核对，非命令形式问题）**：宿主 `Glob` 对 `docs/workspaces/workspace-002-synthetic/GOAL-013*` 这类**只匹配目录**的模式返回空，模型据此判定目标不存在并停止，未写台账（`changed: []`，exit 0）。fixture 实际含 `GOAL-013-synthetic-counter/00-meta.md`。以 `--attempt 02` 重试 → **pass**（写入 `03-audit/A-001-counter-implementation-mismatch.md` 与索引），与 GOAL-013 当年 r5→r6 同类。矩阵已指向 `claude-code-cli-audit-r2-2026-10-17.json`。
6. **Copilot 5 格失败原因（编排侧派发环境缺变量；初判有误，已更正）**：
   - 现象：`session.error` / `model.call_failure` 报 `Authentication failed with provider at http://192.168.31.213:8317/v1 (HTTP 401)`、`"Invalid API key"`；4 个入口与 catalog 全部 exit 1、无台账写入；`--attempt 02` 复测同样 401。
   - 编排侧**初次误判**为「用户凭据失效」，据此登记 I-006、把目标置 `blocked` 并发出 Q-006。用户随后质疑是否真的用到了 `COPILOT_PROVIDER_API_KEY`，据此核对进程环境。
   - **实际根因**：harness 进程环境里 `COPILOT_PROVIDER_BASE_URL` / `COPILOT_PROVIDER_TYPE` / `COPILOT_MODEL` 已继承，但 **`COPILOT_PROVIDER_API_KEY` 只在 User 作用域（`HKCU:\Environment`，len=36），Process 作用域为空**——该变量写入用户环境的时间晚于 harness 进程启动。驱动以 `os.environ.copy()` 传给宿主，于是 copilot 拿到 provider URL 却没有 key。**不是凭据失效，也不是治理/代码问题。**
   - **修复**：在 [s5-run-captures.ps1](../attachments/s5-run-captures.ps1) 增加「从 User 作用域注入 provider 变量」的步骤（不落盘、不打印值），并支持 `-Attempt` / `-NameSuffix` 参数。
   - **重取结果**：`-Attempt 02 -NameSuffix '-r2'` → copilot audit / vision / vision-audit / catalog **pass**；`govern` 因早先探测已占用 `copilot-govern-02` 目录而中止，改用 `--attempt 04` 单独重跑 → **pass**。
7. **门禁（最终）**：
   - `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.7` → `evidence consistency ok (22 evidence file(s))`，**exit 0**（GOAL-015 S3 记录的 stale 红已由本批重捕获解除）。
   - `python scripts/compatibility_report.py` → **exit 0**，`coverage status: ready-for-release-evidence`、`uncovered: 0`、`candidateRevision: v0.13.7`。
   - 证据目录保留首轮失败的 6 个 envelope（claude audit r1 与 copilot r1 ×5）作为历史尝试；矩阵只引用通过（pass）的 16 格。
8. **版本清单（v0.13.7，均为非 behaviorSource 路径）**：矩阵 `candidateRevision` = `v0.13.7`、12 条证据路径与 3 处 `evidenceScope` 改写；安装/GHCR pin 同步（根 `README.md`、`skills/README.md`、`scripts/bootstrap/README.md`、`mcp/README.md`、`docs/releases/README.md`）；CI 证据目录与 `scripts/tests/test_pack_skills_release.py`、`skills/tests/test_skills_orchestrator.py` 断言同步；`stage_skills_mirrors.py` 复制 1 份（矩阵镜像）后 `--check` 38 对 ok。
9. **状态**：S5 步骤 a **已完成**（16/16 pass、两个门禁转绿）。I-006 经根因更正后置 **verified**（不是凭据失效，而是编排侧环境未继承 key）；GOAL-015 从 `blocked` 恢复 **`active` / 80%**，检查点与 `progress` 未变。

### 证据

| 主张 | 路径 / 命令 / commit |
|------|----------------------|
| 探针正文即带标签命令 | `attachments/s5-runtime/grok-audit-00-prep-validate/input.txt`；各 run 的 `input.txt` / `invocation.json` |
| 16 格捕获结果与逐格 verdict | `docs/releases/runtime/v0.13.7/*.json` 的 `result.verdict`；`attachments/s5-runtime/<host>-<case>-01/observation.json` |
| claude audit 首轮未写台账、重试写入 | `s5-runtime/claude-audit-01/observation.json`（`changed: []`）与 `claude-audit-02/observation.json`（`changed: [03-audit.md, 03-audit/A-001-…]`） |
| Copilot 401 根因（编排侧环境） | `[Environment]::GetEnvironmentVariable('COPILOT_PROVIDER_API_KEY','Process')` = NOT SET，`'User'` = len 36；`BASE_URL` / `TYPE` / `MODEL` 两个作用域均在 |
| 修复与重取 | `s5-run-captures.ps1` 的注入段；`s5-runtime/copilot-{audit,vision,vision-audit,catalog}-02/`、`copilot-govern-04/`；envelope `*-r2.json` 均 `verdict=pass` |
| 一致性门禁转绿 | `capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.7` → `ok (22 evidence file(s))`，exit 0 |
| 兼容门禁转绿 | `compatibility_report.py` → exit 0，`ready-for-release-evidence`、`uncovered: 0`、`candidateRevision: v0.13.7` |
| 镜像一致 | `stage_skills_mirrors.py --check` → `checked_pairs: 38` / ok |

## 2026-10-17 · 待答、答复与根因更正

- 同步阻塞卡片 Q-006 提出后，用户真实选择 **A「我恢复凭据后你重取」**（未选改派替代宿主、未选暂停 S5），答复留痕见 `02-execution.md` 待答表。
- 答复后编排侧以 `--attempt 03` 复测仍为同一 401；**该复测本身也跑在同一缺 key 的进程环境里，因此不可能通过**——这一点当时未意识到，属编排侧疏漏。
- 用户质疑「是否真的用了 `COPILOT_PROVIDER_API_KEY`」后，核对进程/用户作用域环境并定位真实根因（第 6 条）；修复注入后 16/16 pass。
- **记录更正**：I-006 由「凭据失效」更正为「编排侧派发环境未继承 provider key，已由 runner 注入修复」并置 `verified`；GOAL-015 恢复 `active`。用户凭据本身有效，从未需要更换——Q-006 选项文字基于错误前提，实际未发生凭据变更。未复用过期证据、未改派替代宿主。

