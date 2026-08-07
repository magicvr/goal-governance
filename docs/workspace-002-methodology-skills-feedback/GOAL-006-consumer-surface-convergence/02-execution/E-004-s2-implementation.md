---
id: E-004
goal: GOAL-006-consumer-surface-convergence
doc: execution
title: S2 实施完成：消费面路径相对化（prompts/模板/薄壳/安装形态/canonical）+ 矩阵证据刷新
status: recorded
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
---

# E-004 · S2 实施事实（2026-08-08）

## 事实

用户 `/govern` 指令「推进 GOAL-006 S2」；按 D-001（A+C 混合）实施。

### 1. 文本相对化（逐文件，UTF-8 安全脚本 + 人工校验）

| 面 | 文件 | 替换目标 | 结果 |
|----|------|----------|------|
| 四治理入口 + 原语 | `skills/prompts/00/05/06/07 + 01/02/03/04`（8 文件） | `{governance_root}/` 字面 | 32+5+14+10+8+3+3+3 → **0 残留** |
| 消费方模板 | `skills/AGENTS.template.md`（35 处） | `{{GOVERNANCE_ROOT}}/` 占位 + 使用说明补条目 | 35 → **0** |
| MCP 薄壳 | `mcp/lifecycle.py`（2 处） | `{governance_root}/` | 2 → **0** |
| R-001 扫尾 | `docs/architecture/overview.md`、`directory-layout.md`、`docs/README.md` | 协议语义前缀相对化；**目录树/标题/`docs/tests`/`skills/core/docs` 保留** | 12→1、16→4（目录树）、34→5（标题/树/tests/§8c 指引） |
| 安装形态（S1 盘点外新发现） | `skills/install/`（AGENTS.md ×2 + copilot-instructions + 壳 17） | AGENTS 拷贝 → `{{GOVERNANCE_ROOT}}`；壳 → `{governance_root}` | 111 → **0** |
| dogfood 安装 | `.grok/`、`.claude/`、`.agents/` skills（12）+ `.github/prompts/`（5） | `{governance_root}` | 39 → **0** |

- **执行判断 1（install 链路）**：`install.sh` / `install.ps1` / `update.py` 中 `docs/` 为**物理安装路径与包内真实路径**（`$TARGET_DIR/docs/`、`core/docs`、`TEMPLATES_SRC`）——保留不改（D-001 第 3 条细化：这些是默认布局的物理事实与包内路径，相对化会失真；F-006 针对「规则正文让 AI 误读」，install 输出/映射非规则正文）。
- **执行判断 2（E-002 盘点缺口）**：安装形态面（`skills/install/` 111 处 + dogfood 39 处）未被 S1 盘点覆盖，S2 发现后补入（P-002 事实回流）；最终影响面 = 25 个源/分发文件 + 17 个 dogfood + 3 个 canonical ≈ 390 处引用。
- **误伤修复**：`docs/README.md` 表格与 `directory-layout.md` 的 `skills/core/docs/*` 包内路径被协议前缀模式误替换（`skills/core/{governance_root}/…` ×5）——全部修复并重跑 stage。

### 2. 防再犯测试（`skills/tests/test_consumer_surface_relativeization.py`，新增）

- `test_prompts_template_lifecycle_have_no_bare_docs`：prompts/模板/lifecycle 无裸 `docs/`（排除 `core/`）
- `test_installed_surface_and_dogfood_have_no_bare_docs`：install 拷贝/壳 + dogfood 无裸 `docs/`
- `test_template_carries_governance_root_placeholder` / `test_prompts_carry_governance_root_literal`：占位/字面语义成立
- `test_r001_sweep_files_have_no_protocol_semantic_docs_prefix`：canonical 扫尾文件无协议语义前缀（regex 排除 `core/`）

### 3. 既有测试断言更新（相对化后语义，6 处）

- `docs/tests/test_standalone_bootstrap.py`：README 断言 `{governance_root}/templates|contracts/`
- `docs/tests/test_vision_protocol.py`：orchestrator 断言 `{governance_root}/vision`
- `skills/tests/test_skills_orchestrator.py`：workspace 规则断言兼容 `{governance_root}`/`{{GOVERNANCE_ROOT}}`；principles 路径断言分列；`docs/vision/reviews.md` → `{governance_root}/vision/reviews.md`；matrix 证据日期断言放宽为 `-2026-08-`

### 4. v0.13.0 release evidence 过期（M-001 语义的预期检出）与刷新

- prompts/AGENTS/install 变更 → `docs/releases/runtime/v0.13.0/*-2026-08-06.json` 的 `behaviorSources` 哈希与当前树不符 → 12 个 release/rehearsal 测试红（`generate_report` 校验）。
- **处置**：复用 GOAL-008 四入口探针 prompts（**12/12 inputSha256 与 v0.13.0 证据一致**，字节级同 prompt），以同命令/同 marker/同模式在**当前 dev 树**重捕获 12 个宿主证据（claude/grok/copilot × govern/audit/vision/vision-audit；并行 244s；**12/12 pass**），输出 `docs/releases/runtime/v0.13.0/*-2026-08-08.json`；**历史 08-06 证据保留**（发布时点快照）。
- matrix cells 证据引用 08-06 → 08-08（12 处）；`evidenceScope` 注明「runtime captures refreshed 2026-08-08 after consumer-surface relativeization (GOAL-006 F-006)」。

### 5. §8c stage（3 轮）

- `overview.md` + `directory-layout.md`（白名单）→ stage copied 2，`--check` 0 漂移
- 误伤修复后 → stage copied 1，`--check` 0 漂移
- `skills-consumer-compatibility-matrix.json`（白名单）→ stage copied 1，`--check` 0 漂移

## 验证

| 动作 | 结果 |
|------|------|
| 全量 `pytest docs/tests skills/tests scripts/tests` | **239 passed**, 4 skipped, 88 subtests passed（无回归；新增 5 条防再犯测试 + 既有断言更新） |
| `stage_skills_mirrors.py --check` | ok（36 pairs，0 漂移） |
| 12 宿主证据重捕获 | 12/12 pass（inputSha256 与 v0.13.0 一致；capturedAt 2026-08-08） |
| 相对化残留扫描 | prompts/模板/lifecycle/install/dogfood **0 裸 docs/**；canonical 仅布局树/标题/物理路径残留（防再犯测试固化） |

## 成功标准对照

| 标准 | 状态 |
|------|------|
| 1. 模板/prompts 无裸 `docs/` 硬编码 | ✅（测试固化） |
| 2. 安装展开链路一致 + `governance_root≠docs` 有测试覆盖 | ✅ 字面层（防再犯测试）；完整消费场景验收留 S3（I-002） |
| 3. 全量测试绿 + stage 0 漂移 | ✅ 239 passed / 36 pairs 0 漂移 |
| 4. 既有已安装消费仓不回滚 | ✅ 无运行时/契约变更；物理路径（install 目标 docs/）未动；仅规则正文语义相对化 |
| 5. F-006/R-001 关闭留痕 | → S3 关门审计 |

## Checkpoint

- 提交 hash 见本轮 commit 记录；owned paths = 全部相对化文件（prompts×8、AGENTS.template、lifecycle.py、install×19、dogfood×17、canonical×3 + 镜像 skills/core×2、matrix + 镜像 skills/contracts、12 个新证据 JSON + .d、4 个测试文件、E-004、02-execution 索引、00-meta、goal-tree）。未用 `git add -A`。

## 下一步（待用户）

1. **S3**：关门审计（self + 建议 `/audit` independent 复审协议正文相对化）；I-002 验收（兼容面）；F-006/R-001 关闭留痕（workspace-003 台账 + VP-002 路线图登记更新）。
