---
title: 目录布局
status: active
created: 2026-07-18
updated: 2026-07-20
parent: null
version: 0.4.0
---

# 目录布局

```text
goal-governance/
├── AGENTS.md                 # AI 助手强制规则
├── README.md                 # 项目入口说明
├── docs/
│   ├── README.md             # 文档体系规范
│   ├── workspace.md          # 可选：工作区 Root/范围/资料固定引用
│   ├── goals/
│   │   ├── goal-tree.md      # 目标树与状态总览
│   │   ├── GOAL-001-.../     # 目标（平铺，无嵌套）
│   │   └── GOAL-00N-.../
│   ├── templates/
│   │   ├── README.md            # 核心模板层说明
│   │   ├── goal-folder/         # canonical 五件套模板
│   │   └── workspace-context.md # 可选 docs/workspace.md 模板
│   ├── contracts/               # canonical 机读协议/模板版本与兼容声明
│   │   ├── skills-consumer-contract.schema.json
│   │   └── skills-consumer-contract.json
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── principles.md     # 治理原则（元规则）
│   │   ├── workspace-protocol.md
│   │   ├── tech-stack.md
│   │   └── directory-layout.md
│   └── _index/               # 预留
├── skills/                    # AI/Agent 消费适配器与分发包
│   ├── prompts/
│   ├── templates/             # docs/templates 的同步镜像
│   │   └── workspace-context.md
│   ├── contracts/             # docs/contracts 的同步镜像
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
- `docs/workspace.md` 是可选工作区上下文，绑定一个 Root Goal 与 `docs/goals/` 范围；`docs/templates/workspace-context.md` 与 Skills 镜像必须同步。没有该文档时按隐式单工作区处理。
- 共享资料只以版本/哈希固定引用出现在工作区上下文或受控记录中，不能成为跨工作区目标状态或第二真相源。
- `docs/contracts/` 是消费适配器版本与兼容声明的 canonical；`skills/contracts/` 只用于离线分发，必须逐字节同步且不得另立版本真相。
