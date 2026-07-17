---
title: 目录布局
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.1
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
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── principles.md     # 治理原则（元规则）
│   │   ├── tech-stack.md
│   │   └── directory-layout.md
│   └── _index/               # 预留
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
