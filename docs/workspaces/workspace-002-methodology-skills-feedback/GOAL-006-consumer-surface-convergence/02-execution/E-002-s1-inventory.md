---
id: E-002
goal: GOAL-006-consumer-surface-convergence
doc: execution
title: S1 盘点：影响面清单与量化（模板/prompts/install/薄壳/canonical 扫尾）
status: recorded
created: 2026-08-08
updated: 2026-08-08
version: 0.1.0
---

# E-002 · S1 影响面盘点（2026-08-08）

## 事实

对消费面路径硬编码（`docs/…`）做全量盘点（grep 计数，路径相对仓库根）：

| 文件 | `docs/` 计数 | `{governance_root}` 计数 | 类别 |
|------|-------------|--------------------------|------|
| `skills/AGENTS.template.md` | 35 | 0 | 消费方 AGENTS 模板（F-006 核心对象） |
| `skills/prompts/00-govern-orchestrator.md` | 33 | 0 | 四治理入口正文（F-006 核心对象） |
| `skills/prompts/06-vision-orchestrator.md` | 15 | 0 | 同上 |
| `skills/prompts/07-independent-vision-review.md` | 10 | 0 | 同上 |
| `skills/prompts/01/02/03/04-create…`（原语） | 19 | 0 | 原语正文 |
| `skills/prompts/05-independent-audit.md` | 5 | 0 | 四治理入口正文 |
| `skills/install.sh` | 30 | 0 | 安装脚本（输出/说明文本） |
| `skills/update.py` | 8 | 0 | 更新逻辑 |
| `skills/install.ps1` | 2 | 0 | 安装脚本 |
| `mcp/lifecycle.py` | 2 | 1 | 薄壳 managed 段（第 96 行 `docs/architecture/principles.md` 硬编码；第 93 行已用 `{governance_root}`） |
| `docs/architecture/overview.md` | 12 | 0 | R-001 扫尾 |
| `docs/architecture/directory-layout.md` | 16 | 0 | R-001 扫尾 |
| `docs/README.md` | 34 | 0 | R-001 扫尾 |
| `docs/vision/alignment.md` | 2 | 26 | **已相对化（R3 车辆基准）** |

**合计：约 240 处 `docs/` 引用，14 个文件**（不含 `skills/core`/`skills/contracts` 镜像——stage 自动同步）。

## 关键观察

1. **相对化先例已存在**：`docs/vision/alignment.md`（R3 车辆 D-002 必改清单）已用 `{governance_root}` 相对化（26 处），语义定义句「`{governance_root}` 默认 `docs`、可经 `.goal-governance.json` 配置、仓外 fail closed」已在 AGENTS §1 / principles 顶部。
2. **模板已有 `{{...}}` 占位机制**：`skills/AGENTS.template.md` 使用说明「将 `{{...}}` 替换为项目真实信息后生效」（如 `{{CORE_TEMPLATES_DIR}}`、`{{WORKSPACE_ROOT}}`、`{{SKILLS_DIR}}`），但路径类引用（`docs/…`）未纳入该机制；install.sh/ps1/update.py **无机器替换逻辑**（占位符为文档语义，由消费方/AI 在安装时替换）。
3. **薄壳**：`mcp/lifecycle.py` managed 段 93 行已写 `{governance_root}`（默认 `docs/`，可配置），96 行仍硬编码 `docs/architecture/principles.md`——同类不一致。
4. **镜像面**：`skills/core/docs/**` 与 `skills/contracts/**` 由 stage 生成（§8c）；改 canonical 后必须 stage + `--check`。

## 方案取舍（待用户确认 → D-001）

- **方案 A（推荐）· 字面 `{governance_root}` 相对化**：全部 `docs/…` → `{governance_root}/…`（语义定义句与 alignment/AGENTS §1 同构：「默认 docs，可经 `.goal-governance.json` 配置，仓外 fail closed」）。零运行时改动；与已发布消费仓兼容（文档语义）；测试面小（文本相对化 + 少量断言 + stage 0 漂移）。
- 方案 B · 安装时 pin 展开：install 脚本把 `{governance_root}` 替换为实际 pin 值（机器展开）。需改 install.sh/ps1/update.py + 消费契约 + 已安装内容不回滚策略；成本高、收益有限（AI 消费时读仓库实际布局，占位符语义已足够）。
- 方案 C · 模板并入 `{{...}}` 体系（如 `{{GOVERNANCE_ROOT}}`），prompts 用 `{governance_root}` 字面：介于 A/B 之间；模板的 `{{...}}` 本就要求安装时替换，路径类并入一致。

## Checkpoint

- 提交 hash 见本轮 commit 记录；owned paths = 本执行记录 + `02-execution.md` 索引。未用 `git add -A`。

## 下一步（待用户）

1. 确认方案 A / B / C（推荐 A，模板路径类可并入 `{{...}}` 形成 A+C 混合：prompts/薄壳/canonical 用 `{governance_root}` 字面，模板路径并入 `{{GOVERNANCE_ROOT}}` 占位）。
2. 确认后 D-001 冻结方案 → I-001 closed（盘点 + 决策证据）→ S1 完成 → S2 实施。
