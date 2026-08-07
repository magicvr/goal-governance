---
id: E-011
goal: GOAL-001-mcp-file-dual-channel-delivery
doc: execution
title: 执行维护项 M-001：capture --check 一致性校验 + 测试
status: recorded
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
---

# E-011 · M-001 执行事实（2026-08-08）

## 事实

用户 `/govern` 指令：「执行维护项 M-001：为 capture_runtime_evidence.py 增加 --check 一致性校验并补测试」。

### 实现（`scripts/capture_runtime_evidence.py`）

- **`check_evidence_file(path, root)`**：读取证据 JSON；无 `behaviorSources` 的返回 `None`（跳过非证据）；有则先跑 schema 校验（复用 `_validate`），再对每条 `behaviorSources` 条目：`_repo_file`（防穿越 + 存在性）→ `_sha256_repo_text`（与捕获写入同哈希语义，LF 规范化）→ 与记录 sha256 比对；缺失/穿越/哈希漂移逐条报问题。
- **`run_evidence_check(directories, root)`**：递归扫描给定目录（可多个）的 `*.json`，汇总 `(problems, checked_count)`。
- **CLI `--check`**：`--evidence-dir`（可重复）**check 模式必填**——设计修正：历史时点证据（`docs/releases/runtime/`、早期工作区捕获）绑定捕获时点树，过期是预期语义，**禁止隐式全仓扫描误报**；只有显式指定目录才检查。exit 0 = 全部一致；exit 1 = 任一问题；缺 `--evidence-dir` = parser.error（exit 2）。
- capture 分支参数由 `required=True` 改为解析后手动校验（保持既有 CLI 行为与错误码不变；`test_cli_accepts_vision_entrypoint_choice` 等既有测试未改动仍绿）。

### 测试（`scripts/tests/test_runtime_evidence.py` · `EvidenceConsistencyCheckTests`，10 条新增）

| 用例 | 验证 |
|------|------|
| `test_check_file_ok_when_sources_match` | 一致 → 无问题 |
| `test_check_file_reports_stale_source` | 改行为源 → 「behavior source is stale」（F-001 场景） |
| `test_check_file_reports_missing_source` | 删行为源 → 「missing」 |
| `test_check_file_rejects_path_escape` | `../` 穿越 → 拒绝 |
| `test_check_file_skips_non_evidence_json` | 无 behaviorSources → `None` 跳过 |
| `test_run_check_counts_evidence_and_skips_others` | 混合目录计数正确 |
| `test_check_cli_exit_codes` | 一致 → 0；stale → 1 |
| `test_check_cli_missing_dir_fails` | 目录不存在 → 1 |
| `test_check_cli_requires_evidence_dir` | `--check` 缺目录 → exit 2（不隐式全仓） |
| `test_check_cli_accepts_multiple_evidence_dirs` | 多目录累加 → 0 |

### 端到端验证（真实仓库）

- `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/workspace-003-mcp-file-dual-channel/GOAL-002-r1-mcp-equivalence-kernel/attachments/runtime/evidence` → **`evidence consistency ok (4 evidence file(s))`**（exit 0；重捕获后绑定当前树）。
- 对 `docs/releases/runtime/v0.12.1`（历史发布时点证据）显式检查 → 正确检出 AGENTS.md 等 stale、exit 1——证明检查有效；该类历史证据绑定发布时点树，由显式指定目录才检查。
- 全量 `python -m pytest docs/tests skills/tests scripts/tests -q` → **234 passed, 4 skipped, 8 subtests passed**（~42s；新增 10 条均绿，既有 210+ 基线无回归）。
- stage：本轮未改 canonical 白名单路径（`scripts/`、测试、附件 README），无需 stage；`docs/contracts/runtime-evidence.schema.json` 未改。

## M-001 验收对照

| 验收标准 | 结果 |
|----------|------|
| ① 枚举已捕获证据 `behaviorSources` 并比对当前树哈希 | ✅ `check_evidence_file` + `--check` |
| ② `mcp/` 实现变更后该检查红 | ✅ stale 单元测试 + 历史目录端到端红 |
| ③ 重捕获后绿 | ✅ workspace-003 4 证据文件 ok |
| ④ 全量测试绿 | ✅ 234 passed（+10 新增，无回归） |
| ⑤ stage `--check` 不受影响 | ✅ 未改 canonical 白名单 |

**M-001 状态：registered → done（closed）**。可选 CI 挂接（对 L3 证据目录定期 `--check`）留作后续发布轮决策，非本项必要交付。

## 文档

- `GOAL-002/attachments/runtime/README.md` 增「一致性检查（M-001 · A-016）」节：用法、语义边界（只处理证据 JSON、历史证据须显式检查）、维护钩子命令。

## Checkpoint

- 提交 hash 见本轮 commit 记录；owned paths = `scripts/capture_runtime_evidence.py`、`scripts/tests/test_runtime_evidence.py`、GOAL-002 runtime README、GOAL-001 03-audit A-018 + 索引、`02-execution.md` 索引 + 本执行记录。未用 `git add -A`。

## 下一步（待用户）

1. M-001 已闭环；A-016 全部建议处置完毕（F-001r fixed + 防再犯落地）。
2. 仍开放项不变：F-006（VP-002）、F-008 / I-007（首次真实 GHCR 发布验收）。
3. 可选：CI 挂接 `--check`（在发布 workflow 对 L3 证据目录执行），随下次发布轮决定。
