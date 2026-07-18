---
title: 提示词 · 创建新目标
status: active
created: 2026-07-18
updated: 2026-07-18
parent: null
version: 0.2.0
role: primitive
---

# 01 · 创建新目标（原语 / primitive）

## 说明

供 [00-govern-orchestrator.md](00-govern-orchestrator.md) 在用户确认「需要新建目标」后调用；也可高级直调。  
日常默认路径请用编排器。

交付物：正确编号的目标文件夹 + 完整五件套 + 已同步的 `goal-tree.md`。

---

## 提示词正文

```markdown
# 角色

你是本项目的目标治理协作者。遵守 `AGENTS.md` 和/或 `.github/copilot-instructions.md`。  
P-001（大目标先路线图）以 AGENTS 为准；若存在 architecture 原则文档，可作补充。

# 任务

按已确认信息创建一个新目标：五件套齐全，goal-tree 已更新。

# 用户输入（缺项先问清再写）

- 目标标题：【用户语言】
- 英文短 slug（小写、短横线）：【如 improve-auth】
- 父目标完整 ID：【如 GOAL-001-my-root-slug；Root 则 null】
- 一句话概述：
- 成功标准（2～5 条可验证项）：
- 是否需要高层路线图（范围大/步骤不明）？【是 / 否】
  - 若是：本回合在 00-meta 或 01-decision 写阶段与先后；子目标留待后续阶段
- 初始状态：draft 或 active（默认 draft）
- 今日日期：【会话/系统 YYYY-MM-DD】

# 步骤

1. 读 `docs/goals/goal-tree.md`，新编号 = 最大编号 + 1（三位）。Root 固定为 GOAL-001。
2. 创建 `docs/goals/GOAL-NNN-<slug>/`（与现有目标平铺，层级只写在 parent）。
3. 一次写入五件套：`00-meta` / `01-decision` / `02-execution` / `03-audit` / `attachments/`。
4. 优先定位项目的核心模板层 `docs/templates/goal-folder/`；若目标仓库没有独立核心层，再定位 **SKILLS_PKG**（含 `prompts/01-create-new-goal.md` 或 `templates/goal-folder/` 的目录）并参考包内镜像 `templates/goal-folder/`。两者结构必须一致。
5. Frontmatter 至少：status, created, updated, parent, version；meta 另含 id、title（建议 progress）。
   - Root 的 slug 使用用户确认的名称。
6. 正文：
   - meta：概述、成功标准、parent 链接；需要时含路线图
   - decision：已有取舍则写「决定 + 为什么」；否则「待立项后补充」
   - execution：只记已发生事实（如「今日创建目标」）
   - audit：可写「尚未到达复盘节点」
7. 更新 `goal-tree.md` 的 ASCII 树与状态表。
8. 如需，在父目标文档轻量提及新子目标；progress 与事实一致。

# 完成标准

- [ ] 编号无冲突；id = 文件夹名  
- [ ] 五件套齐全；parent 为完整 id 或 null  
- [ ] goal-tree 树与表已更新  
- [ ] 大目标已写路线图（若适用）  
- [ ] 内容真实，无虚构完成项  
```

---

## 使用注意事项

- 缺信息时先确认再写入。
- 创建后建议用 03 追加一条「目标已创建」执行记录。
- Root：`GOAL-001` + `parent: null`；slug 由用户定。
