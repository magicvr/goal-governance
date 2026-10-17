---
id: GOAL-015-audit-command-labeled-form
doc: execution-entry
record_id: E-003
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-003 · S3：回归、静态核对与运行证据影响

## 2026-10-17 · S3 验证

### 已发生事实

1. **回归（Python 3.11.9）**：
   - `python -m unittest discover -s skills/tests -p 'test_*.py'` → `Ran 102 tests` / `OK`（exit 0；含新增防再犯测试，较 GOAL-013 时点的 101 项多 1 项）。
   - `python -m unittest discover -s docs/tests -p 'test_*.py'` → `Ran 67 tests` / `OK`（exit 0）。
   - `python -m unittest discover -s scripts/tests -p 'test_*.py'` → `Ran 147 tests` / **FAILED (failures=4, errors=12, skipped=7)**（exit 1）。
2. **失败归因（已核对，不是猜测）**：16 个失败/错误全部落在 `test_release_evidence.ReleaseEvidenceToolTests`，首条异常为 `compatibility_report.ValidationError: runtime evidence behavior source is stale: skills/AGENTS.template.md`；`test_release_evidence.py` 内多条用例通过 `compatibility_report.generate_report(REPO_ROOT)` 触发同一校验。无其他失败类。
3. **官方一致性门禁**：`python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/goal-013-s3-2026-10-17-current` → exit 1，`evidence consistency FAILED`。
4. **过期范围（逐文件重算 sha256）**：`docs/releases/runtime/goal-013-s3-2026-10-17-current/` 的 **16/16** 份记录全部过期，涉及 **24 个** `behaviorSources` 路径：`docs/architecture/principles.md`、`docs/architecture/workspace-protocol.md`、`docs/vision/alignment.md`、`skills/AGENTS.template.md`（各 16 份记录）、`skills/prompts/00·04·05·06·07`（7/10/3/3/6 份）、四宿主 `install` 源 13 个文件、`mcp/entries.py`（4 份）。
5. **保证范围（不得夸大）**：本轮交付的是**规范与消费面文本契约 + 仓库静态/回归**层面的修正。**没有**为新的带标签命令重取任何宿主运行证据，也**没有**新建 runner；旧 16 份运行证据验证的是已被取代的裸数字形式，现全部过期。因此「宿主能正确解析带标签命令」目前**未获运行验证**，须由后续重捕获给出。
6. **未做（按 D-001 用户裁决留在本目标外）**：16 份运行证据重捕获、`candidateRevision`/矩阵更新、版本发布、tag/Release。
7. 结论：S1～S3 的事实可核对；release / compatibility 门禁在重捕获前保持红，本目标不宣称发布就绪。
8. **Git checkpoint**：按 P-002「验证失败时 fail closed」，本轮**未**创建 checkpoint 提交。工作树变更保留待裁决：可先提交规范与消费面改动，或在重捕获使门禁转绿后再提交；本目标不自行 `git add -A` 或代替用户决定提交边界。

### 证据

| 主张 | 路径 / 命令 / commit |
|------|----------------------|
| skills / docs 回归通过 | 上列 unittest 命令与计数（exit 0） |
| scripts 回归红且归因明确 | `Ran 147 tests … FAILED (failures=4, errors=12, skipped=7)`；traceback 指向 `compatibility_report.py:274` 的 stale 校验 |
| 一致性门禁红 | `capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/goal-013-s3-2026-10-17-current` → exit 1 |
| 16/16 过期、24 个来源 | 对 16 份 JSON 的 `behaviorSources[].sha256` 与当前文件逐项重算比对 |
| 失败类只有 stale 一类 | `python -m unittest discover -s scripts/tests -p 'test_*.py' -v` 的 FAIL/ERROR 名单 |
