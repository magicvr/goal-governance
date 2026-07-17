---
title: Skills · 目标治理可复用包
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.1.0
---

# Skills

本目录提供可复制到**其他项目**的目标治理约定与模板。  
本仓库运行中的强制规则仍以根目录 [AGENTS.md](../AGENTS.md) 为准；此处是提炼后的**可复用交付物**。

## 目录结构

```text
skills/
├── README.md                 # 本文件：如何在其他项目中使用
├── AGENTS.template.md        # AI 助手规则模板（可复制为 AGENTS.md）
├── prompts/                  # 可复制的常用提示词模板
│   ├── README.md
│   ├── 01-create-new-goal.md
│   ├── 02-record-decision.md
│   ├── 03-update-execution.md
│   └── 04-write-audit.md
└── templates/
    └── goal-folder/          # 单个目标文件夹空模板
        ├── 00-meta.md
        ├── 01-decision.md
        ├── 02-execution.md
        ├── 03-audit.md
        └── attachments/
```

## 在其他项目中快速启用

### 1. 复制规则文件

```text
# 将模板复制到目标仓库根目录，并改名为 AGENTS.md
skills/AGENTS.template.md  →  <your-repo>/AGENTS.md
```

按项目实际情况替换模板中的占位符（如路径、是否有 Web 应用等）。

### 2. 建立文档骨架

```text
docs/
├── README.md                 # 可参考本仓库 docs/README.md
├── goals/
│   └── goal-tree.md          # 先建空总览，再加目标
└── architecture/             # 可选
```

### 3. 创建第一个目标（Root Goal）

复制模板文件夹并重命名：

```text
skills/templates/goal-folder/
  → docs/goals/GOAL-001-main-vision/
```

然后：

1. 填写 `00-meta.md`：`id`、`title`，`parent: null`
2. 补全决策 / 执行 / 审计初稿（可简短）
3. 在 `docs/goals/goal-tree.md` 登记该目标

### 4. 后续目标

1. 查看 `goal-tree.md` 取下一个编号（如 `GOAL-002`）
2. 再复制一份 `goal-folder` → `docs/goals/GOAL-NNN-short-slug/`
3. 设置 `parent` 为父目标 ID
4. **同步更新** `goal-tree.md`

## 核心约定（摘要）

| 规则 | 说明 |
|------|------|
| 扁平存储 | 所有目标平铺在 `docs/goals/`，不用嵌套文件夹表示层级 |
| 编号 | `GOAL-001` 为 Root；之后顺序编号 |
| 层级 | 仅用 `00-meta.md` 的 `parent` 字段 |
| 总览 | 变更后必须更新 `goal-tree.md` |
| 五件套 | meta / decision / execution / audit / attachments |

完整条文见 [AGENTS.template.md](AGENTS.template.md)。

## 与本仓库的关系

| 路径 | 角色 |
|------|------|
| 根 [AGENTS.md](../AGENTS.md) | 本仓库生效的 AI 规则 |
| [skills/AGENTS.template.md](AGENTS.template.md) | 对外可复用的模板 |
| [docs/goals/](../docs/goals/) | 本仓库真实目标数据 |
| [web/](../web/) | 本仓库 Web 应用（其他项目可选） |

## 提示词模板

日常操作可直接复制 [prompts/](prompts/) 中的提示词给 AI 使用：

| 文件 | 用途 |
|------|------|
| [01-create-new-goal.md](prompts/01-create-new-goal.md) | 创建新目标（五件套 + goal-tree） |
| [02-record-decision.md](prompts/02-record-decision.md) | 记录决策（决定了什么 / 为什么） |
| [03-update-execution.md](prompts/03-update-execution.md) | 更新执行时间线与进度 |
| [04-write-audit.md](prompts/04-write-audit.md) | 阶段性复盘 |

用法详见 [prompts/README.md](prompts/README.md)。

## 尚未包含（后续可扩展）

- 可安装的 VS Code / Copilot Skill 包
- 编号 / parent / goal-tree 一致性校验工具
- goal-folder 更丰富的示例正文

当前交付定位：**可复制的规则 + 提示词 + 目标文件夹模板**。
