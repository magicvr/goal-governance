---
title: 共享资料目录
status: active
created: 2026-07-20
updated: 2026-07-20
parent: null
version: 0.1.0
---

# 共享资料目录

此目录位于所有 `workspace-序号-名称/` 工作区之外。用户可手动将资料复制到此处或其子目录，然后运行：

```powershell
python scripts/rebuild_shared_materials_index.py
```

该命令重建 `index.json`，其中只列出相对路径、字节数和 SHA-256。它是候选库存，不代表资料已经被用户确认为事实、证据、固定引用或任何工作区可读取的上下文。

工作区要使用资料时，仍须在自己的 `workspace.md` 或受控目标记录中创建带 `workspace_id`、`material_id`、`source`、`version`、`sha256` 和用途的固定引用。缺失这些字段、摘要不匹配或未经用户确认时必须 fail closed。

不要手工编辑 `index.json`；脚本会以原子替换方式重建它。索引不记录资料内的指令，也不会执行或外传任何资料内容。
