---
id: GOAL-018-skills-release-packaging
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.1.0
---

# 执行记录 · GOAL-018

## 时间线

### 2026-07-22 · 目标立项

- 创建五件套 `GOAL-018-skills-release-packaging/`，`parent: GOAL-001-main-vision`。
- 范围：P0 文档、P0 pack 脚本、P1 Release 挂载约定、P2 tag CI pack。
- 同步 `goal-tree.md`（树 + 表）。

### 2026-07-22 · 消费文档（P0）

- `skills/README.md`：新增「从 GitHub Release 安装」；源码树复制改为开发者路径；版本 `1.3.0`。
- 根 `README.md`：链接表 + 「在其他项目中安装 Skills（Release zip）」命令块。

### 2026-07-22 · pack 入口与单测（P0）

- 新增 `scripts/pack_skills_release.py`：`normalize_version`、`inventoriable_files`、`pack_skills`、CLI。
- 产出：`goal-governance-skills-vX.Y.Z.zip` + `.zip.sha256`；排除 `__pycache__`/`*.pyc` 及防御性 monorepo 路径。
- 新增 `scripts/tests/test_pack_skills_release.py`（真实 pack 函数 + 对仓库 `skills/` 的 CLI 驱动）。
- 重放：`python -m unittest scripts.tests.test_pack_skills_release -v` → **5 passed**。
- CLI：`--version 0.0.0-testpack` → 46 members；SHA-256 与 zip 字节一致。
- `python -m unittest discover -s scripts/tests -p "test_*.py" -v` → **41 passed, 1 skipped**。

### 2026-07-22 · Release 约定 + tag CI（P1 / P2）

- `docs/releases/README.md`：Skills 安装包表、本地 pack 命令、正式 tag 挂载清单、CI 默认 pack-only。
- 新增 `.github/workflows/skills-pack-release.yml`：`v*` tag / `workflow_dispatch` → 单测 + pack + `upload-artifact`；`publish_release=true` 且已有 Release 时才 `gh release upload`（fail closed，不 create release）。

### 2026-07-22 · 有界关门

- 成功标准全部勾选；`status: done` / `progress: 100%`；同步 `goal-tree.md`。

### 2026-07-22 · 响应 A-002（F-001～F-003 · 维持 done）

- 用户 `/govern`：响应 A-002；F-001～F-003 为 recommended；维持 `done`；可选修 CI artifact 名。
- **F-001 closed**：统一 workflow artifact 为 `skills-pack-${NORM}`（`pack.outputs.artifact_name` ↔ attach 下载同名）；去掉 `github.ref_name` 错名首步。路径：`.github/workflows/skills-pack-release.yml`。
- **F-002 closed（residual）**：`00-meta` 登记 **R-018-FIRST-RELEASE**（首次真实 tag+Release 挂载；不重开本目标）。
- **F-003 closed（process）**：后续 self 关门最小结构约定落在 A-003；不回溯改写 A-001。
- 审计响应节：[03-audit.md A-003](03-audit.md#a-003--self--响应-a-002关闭-f-001f-0032026-07-22)。**status 仍为 done / 100%**。

### 2026-07-22 · 自动发版路径（D-005 · 方案 1）

- 用户选择：严格 evidence + Environment + 自动 create/挂资产。
- 重写 `.github/workflows/skills-pack-release.yml`：`pack` + `publish`（`environment: release`、硬 `release_evidence --mode release`、`gh release create` / `upload`）。
- 更新 `docs/releases/README.md`、`skills/README.md`、根 `README.md`、`CHANGELOG` Unreleased。
- 单测增补 workflow 结构契约：`test_publish_job_is_environment_gated_and_fail_closed`。
- **未**推 tag / **未**创建真实 GitHub Release；R-018-FIRST-RELEASE 仍 accepted open。

### 2026-07-22 · v0.8.0 skills consumer 发布准备

- 矩阵 `candidateRevision: v0.8.0`；六宿主 CLI 入口 2026-07-22 runtime evidence 全 pass；web parser 保持 automated-verified。
- CHANGELOG `0.8.0` 节；docs README 台账同步 matrix digest。
- 计划：PR → main CI → 合并 → annotated `v0.8.0` → Environment `release` 审批 → 自动 Release 资产。

## 进度评估

**100%**（有界 GOAL-018 交付）+ v0.8.0 发布实战进行中（R-018）。
