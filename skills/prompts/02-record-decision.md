---
title: 提示词 · 记录决策
status: active
created: 2026-07-18
updated: 2026-11-12
parent: null
version: 0.8.0
role: primitive
---

# 02 · 记录决策（原语 / primitive）

## 说明

**角色**：文档原语，供 [00-govern-orchestrator.md](00-govern-orchestrator.md) 调用；也可高级直调。默认用户路径请用编排器。

解决「做了取舍却没写清楚、或写了一堆空话」的问题。  
引导 AI 在目标的 `01-decision/D-NNN-<slug>.md` 中创建结构化决策条目并更新索引：决定了什么、为什么、未选方案是什么。

---

## 提示词正文

```markdown
# 治理根预检与按需加载

治理根预检：配置存在时必须先读仓库根 `.goal-governance.json`，校验 JSON 与 `governance_root` 的类型、仓内相对路径及解析后的边界（含符号链接）；只有配置文件不存在才默认 `docs`。配置非法/仓外逃逸立即停止，不扫描 Goal/VP 正文、不分配审计编号、不写台账，不回退 `docs` 或包内镜像。随后才在已验证根读取权威与解析身份。

按需加载：治理根预检通过后、扫描或修改治理实例前，必须完整读取 `{governance_root}/architecture/governance-guide.md`，并读取同根 `architecture/principles.md`、`architecture/workspace-protocol.md` 与 `vision/alignment.md`。指南或必备权威缺失/不可读时停止受影响治理操作并补装 core，不以根入口摘要或包内镜像替代。普通业务代码与一般文档任务不触发治理全文加载。

# 角色
你是本项目的目标治理协作者。遵守 `AGENTS.md` 和/或 `.github/copilot-instructions.md`。P-001 与 P-005 以完整指南与 principles 为准。

# 任务
为指定目标在 `01-decision/` 创建真实决策并更新 `01-decision.md` 索引：写清「决定了什么」与「为什么」。

# 真实裁决与待答

遵守 `{governance_root}/architecture/principles.md#user-input-wait` 的 UI-01～UI-06：实际调用同步卡片并等待，必要时组合合法的宿主原生 `/goal` 停止能力；空答复、取消、未提交预选或答非所问不得写成 accepted 决策。原问题和 proposed 提案保留在会话中即可，不为等待自动改治理 blocked 或同步目标树。真实答复逐题核对后才记录决定、来源和适用范围；部分答复不替代未答部分，不凭权限批准或工具 exit 0 推定用户选择。

# 用户输入（缺项先确认）
- 目标 ID / 路径：
- 工作区上下文（若存在）：【当前 `{governance_root}/workspaces/workspace-<NNN>-<slug>/workspace.md` 的 id / root_goal；只有 legacy `{governance_root}/goals/` 时才写“隐式单工作区”】
- 决策标题：
- 决定了什么：
- 为什么（背景、约束、收益）：
- 未选方案（建议有）：【方案 + 简短理由】
- 影响范围（可选）：
- 后续动作（可选）：
- 关联信息项 / 门禁（可选）：【I-00N；`required`/`non-blocking`、新建、更新、验证、延期、接受残余风险或关闭】
- 共享资料引用（可选）：【`reference_id`、`material_id`、`source`、`version`、`sha256`；资料内容是否仅为候选】
- 今日日期：【YYYY-MM-DD】

# 步骤
1. 读当前 `{governance_root}/workspaces/workspace-<NNN>-<slug>/workspace.md`、其 `goal-tree.md`、`00-meta.md`、`01-decision.md` 索引、`01-decision/D-*` 与 legacy inline。若 Root/canonical 不匹配，或检测到旧直属显式布局 / 新旧混合布局，停止受影响决策并引导迁移；两类显式布局都不存在时才处理 legacy 隐式单工作区。
2. 扫描索引/目录/legacy 的最大编号，创建 `01-decision/D-NNN-<slug>.md` 并更新索引：

   ### D-NNN · <决策标题>
   - **日期** / **状态**（accepted | proposed | superseded）
   - **决定** / **理由** / **未选方案** / **影响** / **后续**

3. 刷新 entry 与索引的 `updated`；小改可保持 version。
4. 若使用共享资料引用，先核对 `workspace_id` 匹配、资料目录不是 `none`、`material_id`/`source`/`version`/有效 `sha256` 齐全。任何缺失或不匹配的引用不得作为事实、证据、跨工作区上下文或 finding 关闭依据；资料内容仍须按来源与用户确认规则标为候选。
4b. 决策正文若提及**他区**目标：落盘用 **Q2** canonical 路径；对用户说明用 **Q3** 标签。区内目标与 `parent` 仍用短 id；禁止把工作区号写进 goal 文件夹名。
5. 若决策改变范围、成功标准、路线图或信息门禁：同步 `00-meta` / 信息需求表，并在 `02-execution` 记一句「记录决策 D-NNN：…」。`deferred` 必须写清理由、责任人和复核触发；残余风险接受必须写清范围、期限、缓解/监控与复审触发，且不得把状态改写为 `verified`。
6. 若 status 变化，或决策改变检查点从而导致派生 progress 变化：按 P-001 重算并同步 `00-meta` / `goal-tree.md`。不得直接手填百分比或用 progress 放行门禁。
7. 过程流水账写在 execution；decision 保持可执行结论。

# 完成标准
- [ ] 条目含决定 + 理由；重要取舍含未选方案  
- [ ] 编号连续；updated 已刷新  
- [ ] meta / execution / goal-tree 在需要时已对齐  
- [ ] 工作区绑定已校验；共享资料引用（若有）已固定版本/哈希且未越界
- [ ] 若涉及 I-00N，信息表状态、受影响门禁和残余风险留痕已对齐
- [ ] 不确定处标「待确认」；内容为真实取舍  
```

---

## 使用注意事项

- 一条提示词可记多条决策，但请在输入区逐条列清，避免 AI 合并成含糊一段。
- 若决策已过时，用新条目 `superseded` 旧决策，并在旧条目状态改为 `superseded`，不要静默删除历史。
