---
title: 提示词 · 更新执行进度
status: active
created: 2026-07-18
updated: 2026-10-17
parent: null
version: 0.8.1
role: primitive
---

# 03 · 更新执行进度（原语 / primitive）

## 说明

**角色**：文档原语，供 [00-govern-orchestrator.md](00-govern-orchestrator.md) 调用；也可高级直调。默认用户路径请用编排器。

解决「做了工作却不写、或写成虚假 100%」的问题。  
引导 AI 在 `02-execution/E-NNN-<slug>.md` 追加一条独立**事实**并更新索引；legacy inline 只读兼容。确有检查点变化时同步 meta / goal-tree 的进度。

---

## 提示词正文

```markdown
# 角色
你是本项目的目标治理协作者。遵守 `AGENTS.md` 和/或 `.github/copilot-instructions.md`，包括 P-005 的信息就绪与未知项门禁。

# 任务
在 `02-execution/` 创建下一条 `E-NNN-<slug>.md` **已发生事实**并更新 `02-execution.md` 索引；完成检查点时更新其标记并确定性重算派生 progress，status 仅按治理事实更新；同步 goal-tree。

# 待答与阻塞记录

执行 `{governance_root}/architecture/principles.md#user-input-wait` 的 UI-01～UI-06。需用户信息时同步卡片优先，缺答/空返回/取消等只记待答事实并停止，不补默认答案。由有权编排侧为当前 active/draft Goal 置 blocked，并同步 meta、goal-tree 树/表与已有父级投影；已有 blocked 保留其他原因，done/cancelled 不自动 reopen，无 Goal 只暂停任务、VP 不改 blocked。不得因记录阻塞而虚增检查点/progress。

待答记录至少含问题 ID、原题/选项、影响范围/门禁、等待原因、提问方式、原有阻塞与恢复条件；答案只在真实提交后登记来源与内容。已授权治理任务中的这些暂停收尾写入**无需另次确认**：在返回问题/进入阻塞等待前完成待答、meta blocked、执行索引、goal-tree 树/表及已有父级投影；不能以“未答不写入”为由省略，也不能预写实际答复或未发生的工具返回。恢复时核对所有门禁，未答部分/其他原因保留。写盘失败仍停止并报告未持久成功；独立审计员不得用本原语越权改状态。

# 用户输入（缺项先确认）
- 目标 ID / 路径：
- 工作区上下文（若存在）：【当前 `{governance_root}/workspaces/workspace-<NNN>-<slug>/workspace.md` 的 id / root_goal；只有 legacy `{governance_root}/goals/` 时才写“隐式单工作区”】
- 今日日期：【YYYY-MM-DD】
- 本次实际完成（具体条目，含路径/产物更佳）：
  1. …
- 阻塞 / 风险：【或「无」】
- 关联信息项（可选）：【I-00N；收集 / 验证 / 新发现 / 状态变化】
- 共享资料引用（可选）：【`reference_id`、`material_id`、`source`、`version`、`sha256`；确认状态】
- 下一步计划（可选，标明为计划）：
- progress：【无显式检查点则省略/—；有则按完成检查点/总检查点或显式权重重算，并给来源】
- status：【保持 / draft|active|blocked|done|cancelled】

# 步骤
1. 读当前 `{governance_root}/workspaces/workspace-<NNN>-<slug>/workspace.md`、`00-meta.md`（含信息需求）、decision/execution 索引与 ledger 目录、`goal-tree.md`。若 Root/canonical 不匹配，或检测到旧直属显式布局 / 新旧混合布局，停止受影响写入并引导迁移；两类显式布局都不存在时才处理 legacy 隐式单工作区。
2. 扫描索引、目录与 legacy inline 的已有编号，创建下一条 `02-execution/E-NNN-<slug>.md`，并把链接写入索引。条目正文至少含：

   ### YYYY-MM-DD · <短标题>
   - 事实（做了什么、改了哪些路径）
   - 阻塞（如有）
   - 下一步（计划单独标注）

3. 条目具体可核对；计划与已完成分开写。
4. 涉及共享资料时，先核对引用的 `workspace_id`、`material_id`、`source`、`version` 与有效 `sha256`；缺失或不匹配时记录拒绝/阻断事实，不能把资料内容写成 confirmed 事实、证据或跨工作区上下文。固定引用只说明来源，事实准入仍须用户显式确认。
4b. 时间线若提及**他区**目标或产物：落盘用 **Q2** 路径；对话用 **Q3**。本区目标用短 id；禁止改 goal id 形状。
5. 涉及 I-00N 时：记录实际收集/验证动作与证据路径；新发现的未知追加到信息表，并写明 `required`/`non-blocking`、影响门禁和最晚需要阶段。`deferred` 要保留理由、责任人与复核触发；没有证据时不得把状态改为 `verified`。
6. 刷新 entry 与索引的 `updated`。
7. 检查点或 status 变化时：先按 P-001 确定性重算派生 progress（无来源则省略/—），再同步 meta 与 goal-tree（树 + 表）；关门前确认没有未处理的 required finding / 信息项。`progress=100%` 不自动推导 `done`。
8. 完成某条成功标准时：勾选 meta 并在 execution 点明。
9. 决策论证写入 `01-decision`；execution 保持时间线事实。

# 进度说明（建议）
文末一两句说明百分比依据（对照成功标准）。

# 完成标准
- [ ] 新条目为可核对事实  
- [ ] updated 已刷新  
- [ ] status 与 meta、goal-tree 一致；progress（若有）可从显式检查点重算且三处展示一致
- [ ] 工作区绑定已校验；共享资料引用（若有）固定且任何拒绝路径未产生写入
- [ ] 成功标准勾选与事实一致  
- [ ] I-00N 状态与可核对证据一致；新未知没有被遗漏或伪装为已知
```

---

## 使用注意事项

- 输入区尽量写「改了什么文件 / 达成什么可验证结果」，AI 才能避免空话。
- 小步提交未改变检查点时，progress 保持其派生值，只追加时间线即可。
- 若工作实际属于另一目标，应改记到正确目标，勿堆在错误 ID 下。
