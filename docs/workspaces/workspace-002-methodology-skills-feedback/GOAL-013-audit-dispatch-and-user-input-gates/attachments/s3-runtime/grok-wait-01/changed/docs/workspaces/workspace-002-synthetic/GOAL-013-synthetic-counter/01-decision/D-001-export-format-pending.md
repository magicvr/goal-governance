---
id: GOAL-013-synthetic-counter
doc: decision-entry
record_id: D-001
status: proposed
parent: GOAL-001-synthetic-root
created: 2026-10-16
updated: 2026-10-16
version: 0.1.0
---

## D-001 · 导出格式待用户选择

- **日期**：2026-10-16
- **状态**：proposed（未 accepted；无用户提交）

### 触发

GOAL-013 成功标准要求：用户真实选择留痕后才实现导出。I-001 为 required，影响实施门禁，最晚阶段为实施前。用户本轮指令为推进下一步，进入实施前必须先闭合 I-001。

### 决定

尚未选定导出格式。提案：由用户在 **JSON** 与 **TSV** 中择一；推荐 JSON（结构化、便于本仓库 `counter.py` 结果复核）。本条不把推荐写成已选格式。

关联：I-001；问题 ID `Q-I-001-export-format`。

### 为什么

格式决定输出契约与验收方式。用模型默认值实施会违反成功标准与 P-004/P-005。

### 未选方案

- 静默采用 JSON 或 TSV 并开工：否决，等同用默认值取代用户选择。
- `accepted-residual` 跳过格式选择：无用户书面残余接受，不采用。
- 同时实现两种格式：超出 I-001 题面，除非用户书面要求。

### 影响

阻断 GOAL-013 实施与导出实现，直至真实答复按 UI-06 留痕。

### 后续

用户提交后：将本条或后继条目改为 accepted，更新 I-001 为 verified（或用户书面指定的其他合法闭合），再提议实施导出。
