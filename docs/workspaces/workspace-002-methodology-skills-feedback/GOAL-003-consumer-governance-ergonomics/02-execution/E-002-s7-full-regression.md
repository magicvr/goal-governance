---
id: GOAL-003-consumer-governance-ergonomics
doc: execution-entry
record_id: E-002
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-002 · S7 全量回归与发布准备

## 2026-08-04 · S7 全量回归与发布准备

### 已发生事实

- 文档治理测试原有一条陈旧断言要求 VP-001 `active`；现行 workspace-001 已 `archived`、Root `done`、VP-001 `closed`。测试以这组三层真实状态修正后 **26/26 passed**。
- Web 全量回归 **143 passed，1 skipped**；跳过项仅为 Windows 无 symlink 创建权限。ledger merge、新目标三个目录与全部既有受控写入路径通过。
- Skills、发行打包、bootstrap、updater、mirror 全量回归 **65 passed，2 skipped**；跳过项为 Windows symlink 权限与无可用 WSL Bash。
- 新增真实离线 updater 成功路径：从带 SHA-256 sidecar 的消费发行 zip 更新既有 Skills，实际运行 `install.ps1 -All`，安装四宿主入口；更新后消费包不含三个 producer-only 证据文件。
- 发行包回归核对 consumer contract + schema、updater、核心架构与模板存在，并排除 runtime evidence、compatibility matrix、工作区状态、Web、cache 与 `tech-stack.md`。
- canonical → Skills mirror **34 pairs matched**；`git diff --check` 通过。
- 创建 S7 checkpoint **`ef39f9c`**（`test(governance): 补齐 S7 兼容回归`）。

### 验证矩阵

| 范围 | 命令 | 结果 |
|------|------|------|
| 文档 / 愿景 / 工作区协议 | `python -m unittest discover -s docs/tests -v` | 26 passed |
| Web | `cd web; ..\.venv\Scripts\python.exe -m unittest discover -s tests` | 143 passed，1 skipped（symlink privilege） |
| Skills / pack / bootstrap / updater / mirror | `python -m unittest skills.tests.test_skills_orchestrator scripts.tests.test_pack_skills_release scripts.tests.test_bootstrap_install_online scripts.tests.test_skills_update scripts.tests.test_stage_skills_mirrors` | 65 passed，2 skipped（symlink privilege、WSL Bash unavailable） |
| mirror | `python scripts/stage_skills_mirrors.py --check` | 34 pairs matched |
| whitespace | `git diff --check` | pass |
| checkpoint | Git commit `ef39f9c` | committed |

### 关门前边界

S7 实现与回归门禁已满足，I-007 verified。目标仍为 `active`：按 D-005 的 `cross` 模式，还必须完成 self close-out、用户指定的 Grok Build independent audit，并由 `/govern` 响应全部意见后才可标 `done`。
