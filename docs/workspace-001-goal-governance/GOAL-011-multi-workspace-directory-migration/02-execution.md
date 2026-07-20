---
id: GOAL-011-multi-workspace-directory-migration
doc: execution
status: done
parent: GOAL-001-main-vision
created: 2026-07-20
updated: 2026-07-21
version: 0.3.0
---

# 执行记录 · GOAL-011

## 时间线

### 2026-07-20 · 目标立项与迁移边界确认

- 用户确认以 `docs/workspace-001-名称/` 工作区根取代全局 `docs/goals/`，并要求新建同级共享资料目录和用户可触发的索引重建脚本。
- 依据 Root Goal 的稳定目的，选择当前工作区目录 `docs/workspace-001-goal-governance/`。
- 已登记 I-001～I-004；尚未把目录、索引、消费者适配或测试结果记为已完成。

### 2026-07-20 · 显式工作区迁移、资料索引与验证完成

- 已将原 `docs/goals/` 整体迁移为 `docs/workspace-001-goal-governance/`，在该工作区根新增 `workspace.md`，并将 GOAL-011 五件套与 `goal-tree.md` 同步纳入。`docs/goals/` 不再存在。
- 已建立 `docs/shared-materials/`、候选 `index.json` 与 [重建脚本](../../../scripts/rebuild_shared_materials_index.py)。脚本只输出相对路径、字节数和 SHA-256，拒绝目录逃逸和符号链接；当前库存为 0 条候选。
- 已更新核心协议、standalone 流程、模板/Skills 镜像、安装面、Web 默认读取根、历史 runtime 证据路径和相关测试。`GoalsRepository` 保留 `goals_dir` 参数作为 scope 注入接口。
- 已验证：`python -m unittest discover -s docs/tests` 通过 10 项；`python -m unittest skills/tests/test_skills_orchestrator.py` 通过 32 项；`.venv\\Scripts\\python.exe -m unittest discover -s scripts/tests` 通过 36 项；在 `web/` 运行 `..\\.venv\\Scripts\\python.exe -m unittest discover -s tests` 通过 21 项。两个符号链接用例因 Windows 权限限制跳过；系统 Python 缺少 `jsonschema`，因此 scripts 套件使用项目虚拟环境复跑。
- `git diff --check` 通过；工作区根扫描确认包含 11 个 `GOAL-*` 目录及共享资料 `index.json`。

### 2026-07-21 · 响应 A-003 F-001（现时入口标注）

- `/govern` 在 [goal-tree.md](../goal-tree.md) 增加「路径语义说明」：现时 canonical = 本工作区根；历史 `docs/goals/` = 迁移前叙述。
- A-004 关闭 A-002/A-003 recommended F-001；**未**批量改写已关门目标历史附件；status 保持 `done / 100%`。

## 进度评估

**100%**：本目标的目录迁移、共享资料候选索引、消费适配器同步和关门验证均有可核对产物与测试证据。I-004 保持 non-blocking/open，已明确留给 GOAL-009 的后续产品工作。F-001（文档一致性）已于 2026-07-21 关闭。
