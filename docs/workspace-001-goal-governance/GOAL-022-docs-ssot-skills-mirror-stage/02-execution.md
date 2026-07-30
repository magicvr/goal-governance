---
id: GOAL-022-docs-ssot-skills-mirror-stage
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.2.0
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

**未做**：阶段 F 正式自审/关门；tag/Release；I-004 AGENTS 生成链。

## 待办（计划）

1. 阶段 F：自审 A-00N 或用户确认关门。  
2. （可选 follow-up）AGENTS.template 单源生成 install 宿主规则。

## 进度评估

- 路线图检查点：**5 / 6** → `progress: 83%`。  
- 状态：`active`；开放 required findings = 0；开放 required I = 0。
