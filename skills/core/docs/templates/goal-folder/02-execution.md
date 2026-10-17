---
id: GOAL-NNN-short-slug
doc: execution
status: active
parent: GOAL-001-root-slug
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.2.0
---

# 执行记录 · GOAL-NNN

## 执行索引

| E-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| E-001 | YYYY-MM-DD | `<事实标题>` | recorded | `02-execution/E-001-<slug>.md` |

## 用户待答与恢复（按需保留）

> 按 `{governance_root}/architecture/principles.md#user-input-wait` 的 UI-01～UI-06：阻塞卡片优先，缺答（含空返回/取消/预选未提交）即暂停；由有权编排侧将当前 active/draft Goal 置 blocked，同步 meta、goal-tree 树/表与已有父级投影，不改检查点/progress。无 Goal 仍暂停任务，VP 不改 blocked；保留其他阻塞，写盘失败仍停止。

| 问题 ID | 原题 / 选项 | 影响范围 / 门禁 | 等待原因 / 提问方式 | 原有阻塞 | 恢复条件 | 真实答复来源 / 内容 |
|---------|-------------|-----------------|---------------------|----------|----------|---------------------|

> 答复到达前最后一列留空，不补默认选择或伪造提交；实际提交后先留痕，再复核全部门禁与未答部分，仅解除该答案解决的原因。独立审计员只记录/返回待答事实，不越权改 Goal 状态。

## 事实边界

> 只写已经发生且有证据的事实。每个独立时间线条目放在 `02-execution/E-NNN-<slug>.md`；计划、未知和建议分别留在决策或审计记录。不能把 `open`、`deferred` 或 `accepted-residual` 写成已验证事实。checkpoint commit hash 与覆盖路径在对应 E 条目中登记。

> legacy inline 的 `### YYYY-MM-DD` 时间线仍可保留并被读取；新事实从目录写入。编号在本目标内单调不复用。
