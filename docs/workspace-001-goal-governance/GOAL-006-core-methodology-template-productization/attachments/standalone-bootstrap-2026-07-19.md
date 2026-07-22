---
title: GOAL-006 独立核心包启用验收记录
status: active
created: 2026-07-19
updated: 2026-07-19
parent: null
version: 0.1.0
---

# 独立核心包启用验收记录

## 来源

验证使用仓库根 `C:/Users/magicvr/Documents/Code/goal-governance` 的以下 canonical 来源：

- `AGENTS.md`
- `docs/README.md`
- `docs/architecture/`
- `docs/templates/`

没有复制 `skills/` 或 `web/`。

## 生成路径

测试 `docs/tests/test_standalone_bootstrap.py` 每次创建并清理一个临时 Git 仓库，目录模式为：

```text
<system-temp>/gg-core-bootstrap-*/
├── AGENTS.md
├── docs/README.md
├── docs/architecture/
├── docs/templates/
└── docs/goals/
    ├── goal-tree.md
    └── GOAL-001-main-vision/
        ├── 00-meta.md
        ├── 01-decision.md
        ├── 02-execution.md
        ├── 03-audit.md
        └── attachments/
```

临时仓库由 `git init` 建立；测试结束后自动清理，避免把验证产物混入核心文档层。

## 核对结果

- `python -m unittest discover -s docs/tests -p "test_standalone_bootstrap.py" -v`：2 项测试通过。
- `git rev-parse --is-inside-work-tree`：`true`。
- Root ID 与目录名均为 `GOAL-001-main-vision`。
- 四个 Markdown 文件均包含最低 frontmatter；Root `parent: null`、`status: active`、`progress: 0%`。
- `goal-tree.md` 同时包含 Root 树节点和状态表，且与 Root 元数据一致。
- `attachments/.gitkeep` 存在；目标仓库没有 `skills/` 或 `web/`。

本记录证明核心文档包可以脱离 Skills/Web 初始化 Root；不作为 Skills 安装、Web 发布或阶段 5 验收证据。
