---
id: GOAL-003-consumer-governance-ergonomics
doc: execution-entry
record_id: E-001
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-001 · S2～S6 实现与 checkpoint

## 2026-08-04 · S2～S6 实现与 checkpoint

### 已发生事实

- **S2**：消费契约增加 `evidenceBoundary` 与 ledger 目录；默认安装和消费发行包只携带 consumer contract + schema。隔离 `-All` 回归预置三个 producer-only 文件后仍成功，且这些文件逐字节保持不变。
- **S3**：canonical 模板改为稳定索引 + `D/E/A-NNN-slug.md` 平铺条目；Web reader 合并 legacy inline 与目录条目，新建目标创建三个 ledger 目录。本目标从本条开始 dogfood additive migration。
- **S4**：原则、宿主规则、编排器与审计入口采用 `none` / `self` / `independent` / `cross` 风险矩阵；仅在需要 independent provider 且会话未指定或模式实质歧义时询问。
- **S5**：长流程 checkpoint 节点、owned paths、验证前置与 fail-closed 行为已写入 canonical 与宿主表面；仓库 commit prompt 不再自动 `git add -A`。
- **S6**：新增 `skills/update.py` 与 PowerShell/Bash 入口，支持固定版/最新版本、在线/离线 SHA-256、协议预检、managed-file 冲突检测、备份与失败自动恢复。
- 创建实现 checkpoint **`51872c9`**（`feat(governance): 修复消费门禁与长流程体验`），只包含本切片 owned paths。

### 证据

| 主张 | 路径 / 命令 / commit |
|------|----------------------|
| consumer / producer 资产分离 | `docs/contracts/skills-consumer-contract.json`、`skills/install.ps1`、`skills/install.sh`、`scripts/pack_skills_release.py` |
| ledger 兼容读取与新建目录 | `docs/templates/goal-folder/`、`docs/templates/ledger-entry/`、`web/services/goals_repo.py` |
| 风险审计与 checkpoint 契约 | `docs/architecture/principles.md`、`skills/prompts/00-govern-orchestrator.md`、`.github/prompts/commit.prompt.md` |
| updater 与回滚 | `skills/update.py`、`scripts/tests/test_skills_update.py` |
| 主回归 | `python -m unittest skills.tests.test_skills_orchestrator scripts.tests.test_pack_skills_release scripts.tests.test_bootstrap_install_online scripts.tests.test_skills_update scripts.tests.test_stage_skills_mirrors -v` → 64 passed，2 skipped |
| Web ledger 定向回归 | `cd web; ..\.venv\Scripts\python.exe -m unittest tests.test_goals_repo -v` → 17 passed，1 skipped |
| canonical mirror | `python scripts/stage_skills_mirrors.py --check` → 34 pairs matched |
| checkpoint | Git commit `51872c9` |
