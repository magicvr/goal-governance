---
id: GOAL-015-audit-command-labeled-form
doc: execution-entry
record_id: E-002
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-002 · S2：规范与全部消费面同步

## 2026-10-17 · S2 实施

### 已发生事实

按 [D-002](../01-decision/D-002-labeled-command-contract.md) 的写集，把正式命令改为 `/audit workspace-NNN goal-NNN` 与 `/vision-audit vp-NNN`，裸数字判为非法：

1. **canonical**：`docs/architecture/principles.md`（AD-01 重写为带标签语法与扩展拒绝面、AD-02 改「带标签编号只是入口选择器」、示例行改为 `workspace-002 goal-013` 合法 / `002 013` 非法；version 0.14.1 → 0.15.0）；`docs/architecture/workspace-protocol.md` §2.7 标题改为「审计命令的带标签选择器」并改写 1～5 项（version 1.1.0 → 1.2.0）；`docs/vision/alignment.md` §9.3（version 0.9.0 → 0.10.0）。
2. **仓库规则**：根 `AGENTS.md` §6b 自动派发条目。
3. **Skills prompts**：`00-govern-orchestrator.md`、`04-write-audit.md`、`05-independent-audit.md`、`06-vision-orchestrator.md`、`07-independent-vision-review.md`。
4. **规则模板**：`skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md`、`.github/copilot-instructions.md`。
5. **四宿主安装源**：`skills/install/{claude,grok,codex}/skills/{govern,audit,vision,vision-audit}/SKILL.md`（12 份）与 `skills/install/copilot/prompts/{govern,audit,vision,vision-audit}.md`（4 份）；其中 audit 与 vision-audit 的 `argument-hint` 改为 `[workspace-NNN goal-NNN | …]` / `[vp-NNN | …]`，vision-audit 的「自动请求仅接受 VP 编号命令」改为「仅接受 `vp-NNN` 命令」。
6. **MCP guidance**：`mcp/entries.py` 的 `_INPUT_BOUNDARY` 与 `mcp/README.md`；参数形状未改，仍是 guidance 文本。
7. **契约测试**：`skills/tests/test_governance_interaction_contract.py` 更新 guidance 断言，并新增防再犯测试 `test_automatic_audit_commands_use_labeled_selectors`（要求规则面含带标签形式、且不含裸数字旧形式）。
8. **生成面**：`python scripts/stage_skills_mirrors.py` 复制 3 份镜像（`skills/core/docs/architecture/principles.md`、`workspace-protocol.md`、`skills/core/docs/vision/alignment.md`），`--check` 报 `checked_pairs: 38`、`ok: skills mirrors match docs/`。
9. **dogfood 副本**：`.claude|.grok|.agents/skills/*/SKILL.md`（12）与 `.github/prompts/*.prompt.md`（4）从安装源复制；复制前用 `git rev-parse HEAD:<path>` 逐对比对，16 对 blob 全部相同（`SAME`），因此复制只引入本次预期改动。
10. 变更面（最终计数）：`git status --short` 计 **55** 个已修改文件 + 1 个新增目标目录（13 个文件）；`git diff --stat` 为 **55 files changed, 161 insertions(+), 102 deletions(-)**，含下方两项文档卫生追加（S2 实施刚完成、尚未做该两项追加时的中间计数为 53 files / +152 −100）。

### 写集追加（超出 D-002 冻结清单的两项文档卫生）

- `docs/README.md`：补记本次边界——16 份运行记录因 24 个 `behaviorSources` 变更而全部过期（否则该文件的「当前来源一致」叙述会失真）；版本 0.14.9 → 0.15.0。
- GOAL-013 `01-decision/D-002-s1-contract-proposal.md`：加「现时注（2026-10-17 · GOAL-015）」指针，说明该条的裸数字形式已被取代；不改写其历史结论、状态与 verdict。

### 证据

| 主张 | 路径 / 命令 / commit |
|------|----------------------|
| canonical 与全部消费面已改 | 上列 53 个修改文件；`git diff --stat` |
| 镜像一致 | `python scripts/stage_skills_mirrors.py --check` → `checked_pairs: 38` / `ok: skills mirrors match docs/`（exit 0） |
| dogfood 与安装源逐字节一致 | 复制前 `git rev-parse HEAD:` 16 对全部 `SAME`；复制后 `skills/tests/test_governance_interaction_contract.py::test_install_and_dogfood_copies_do_not_divergence` 通过 |
| 旧形式在规则面无残留 | 定向检索 `AGENTS.md`、`skills/`、`docs/architecture`、`docs/vision`、`docs/tests`、`mcp/`、`.claude`、`.grok`、`.agents`、`.github` 仅命中测试内的 legacy 断言元组 |
| 未改历史证据与历史台账 | `docs/releases/runtime/**`、GOAL-013 执行/审计条目未改；只加现时注 |
