---
id: GOAL-003-consumer-governance-ergonomics
doc: execution-entry
record_id: E-003
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-003 · self 预检 required 修复

## 2026-08-04 · updater 新路径回滚与 ledger parser 对齐

### 已发生事实

- self 预检发现 updater 只按旧包枚举外部 managed paths：新版本若新增宿主文件，既不能在覆盖既有本地文件前报冲突，也不能在安装失败后删除新写入文件。
- updater 现在对旧包与 incoming 包取 managed destination 并集：旧路径按旧 source 检测本地修改；incoming-only 路径按新 source 检测冲突；回滚备份/缺失清单覆盖两边。
- self 预检发现 canonical D/E entry 模板的标题层级与 Web parser 不一致；模板与实际 E 条目改为 parser-compatible heading，镜像同步。
- 新增回归证明 incoming-only 本地冲突 fail closed、模拟安装失败后新增 managed 文件被清除、D/E 目录条目可进入 Web 结构化列表。
- 全量复跑：docs 26 passed；Web 143 passed / 1 skipped；Skills/发行/更新 66 passed / 2 skipped；mirror 34 pairs matched。
- 创建修复 checkpoint **`ac6a741`**（`fix(governance): 补全更新回滚与 ledger 解析`）。

### 证据

| 主张 | 路径 / 命令 / commit |
|------|----------------------|
| incoming managed 并集冲突/备份/恢复 | `skills/update.py`、`scripts/tests/test_skills_update.py` |
| parser-compatible D/E 模板 | `docs/templates/ledger-entry/`、`web/tests/test_goals_repo.py` |
| canonical mirror | `python scripts/stage_skills_mirrors.py --check` → 34 pairs matched |
| 修复 checkpoint | Git commit `ac6a741` |
