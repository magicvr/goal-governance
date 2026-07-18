---
title: 目录布局
status: active
created: 2026-07-18
updated: 2026-07-19
parent: null
version: 0.2.0
---

# 目录布局

```text
goal-governance/
├── AGENTS.md                 # AI 助手强制规则
├── README.md                 # 项目入口说明
├── docs/
│   ├── README.md             # 文档体系规范
│   ├── goals/
│   │   ├── goal-tree.md      # 目标树与状态总览
│   │   ├── GOAL-001-.../     # 目标（平铺，无嵌套）
│   │   └── GOAL-00N-.../
│   ├── templates/
│   │   ├── README.md            # 核心模板层说明
│   │   └── goal-folder/         # canonical 五件套模板
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── principles.md     # 治理原则（元规则）
│   │   ├── tech-stack.md
│   │   └── directory-layout.md
│   └── _index/               # 预留
├── skills/                    # AI/Agent 消费适配器与分发包
│   ├── prompts/
│   ├── templates/             # docs/templates 的同步镜像
│   └── install.*
└── web/
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── static/
    └── templates/
```

## 约束

- `docs/goals/GOAL-*` 之间**不得**再嵌套目标目录。
- 新目标只新增同级文件夹，并改 `parent` + `goal-tree.md`。
- `docs/templates/goal-folder/` 是核心 canonical 模板；`skills/templates/goal-folder/` 只用于 Skills 离线分发，不保存目标状态。
