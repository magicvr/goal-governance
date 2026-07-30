---
id: GOAL-022-docs-ssot-skills-mirror-stage
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.3.0
---

# 执行记录 · GOAL-022

## 时间线

### 2026-07-30 · 目标立项（D-001）

- 新建 `GOAL-022-docs-ssot-skills-mirror-stage/` 五件套；goal-tree 同步；progress 0%。

### 2026-07-30 · D-002 冻结 + 阶段 A～E 实现

**方案**：见 D-002（I-001～I-003 closed；I-004 out of scope）。

**产物**：

| 路径 | 说明 |
|------|------|
| `scripts/stage_skills_mirrors.py` | 从 docs stage core + contracts；`--check` 漂移门禁；剥离 legacy `skills/templates` 五件套 |
| `scripts/tests/test_stage_skills_mirrors.py` | 单测（含 monorepo check） |
| `scripts/pack_skills_release.py` | monorepo pack 前自动 stage；`--skip-stage` |
| `.github/workflows/ci.yml` | stage + dirty tree fail |
| `.github/workflows/skills-pack-release.yml` | pack 前 stage |
| `skills/core/docs/README.md` | 消费方精简入口（手维） |
| `skills/templates/README.md` | 指针说明 |
| `docs/contracts/*` + fixtures | `mirrorPath` → `skills/core/docs/templates/goal-folder` |
| `skills/install.{sh,ps1}` | `--all` 模板源改为 `core/docs/templates` |
| 文档 | `docs/README` 0.10.6、directory-layout、templates README、skills README、core README |

**验证（本机 2026-07-30）**：

- `python scripts/stage_skills_mirrors.py --check` → ok  
- docs tests **26** OK  
- scripts tests **52** OK（2 skip）  
- skills orchestrator **39** OK  

**未做（当时）**：阶段 F 正式自审/关门；tag/Release；I-004 AGENTS 生成链。

### 2026-07-30 · 独立交叉审计 A-001 落盘

- `/audit` 独立意见写入 `03-audit.md` A-001；verdict **conditional**。
- 开放 required findings = **0**；recommended F-001～F-003 open。
- 本机复跑：stage 28 pairs ok；docs 26 / scripts 52(2 skip) / skills 39。

### 2026-07-30 · 响应 A-001 + 阶段 F 关门（D-003）

**决策**：D-003 — F-001 **accepted-residual** R-022-ORPHAN-PRUNE；F-002 **accepted-residual** R-022-INSTALL-TEMPLATES-COPY；F-003 **fixed**；用户确认 self close-out → `done`。

**F-003 fixed 产物**：

| 路径 | 改动 |
|------|------|
| `GOAL-001-main-vision/00-meta.md` | 三层交付「模板镜像」现行句 → stage / `core/docs/templates`；子目标表含 022 done + residual；下一编号 GOAL-023 |
| `GOAL-001-main-vision/01-decision.md` | D-007 / D-008 现时注（历史句保留 + supersede 指引） |

**审计**：

- A-002 · response（关闭证据表）
- A-003 · self close-out · verdict **pass**

**回归（关门前 2026-07-30）**：

- `python scripts/stage_skills_mirrors.py --check` → ok（28 pairs）
- docs unittest **26** OK  
- scripts unittest **52** OK（2 skip）  
- skills orchestrator unittest **39** OK

**状态变更**：`active / 83%` → **`done / 100%`**（路线图 F `[x]`；成功标准第 7 项勾选）。**未** tag/Release。

## 待办（计划 · 本目标外）

1. （可选 follow-up）stage orphan prune → 可闭合 R-022-ORPHAN-PRUNE。  
2. （可选）install extras 取消 templates 物化 → 可闭合 R-022-INSTALL-TEMPLATES-COPY。  
3. （可选）AGENTS.template 单源生成 install 宿主规则（I-004）。

## 进度评估

- 路线图检查点：**6 / 6** → `progress: 100%`。  
- 状态：`done`；开放 required findings = 0；开放 required I = 0；residual 2 条 non-blocking。
