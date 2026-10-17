---
status: blocked
created: 2026-10-17
updated: 2026-10-17
parent: GOAL-001-synthetic-root
version: 0.1.1
id: GOAL-013-synthetic-counter
doc: execution
---

# execution 索引

| E-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| E-001 | 2026-10-17 | 等待 I-001 输出格式选择 | recorded | `02-execution/E-001-await-output-format.md` |

## 用户待答与恢复

> 按 `docs/architecture/principles.md#user-input-wait` 的 UI-01～UI-06。答复到达前最后一列留空，不补默认选择或伪造提交。

| 问题 ID | 原题 / 选项 | 影响范围 / 门禁 | 等待原因 / 提问方式 | 原有阻塞 | 恢复条件 | 真实答复来源 / 内容 |
|---------|-------------|-----------------|---------------------|----------|----------|---------------------|
| Q-001 | 计数结果导出格式选哪一种？选项：JSON（推荐）；TSV。保留自由输入。 | [workspace-002-synthetic] GOAL-013-synthetic-counter；I-001 required；实施门禁 | I-001 到期且无真实选择，禁止实施导出。提问方式：`ask_user_question` 同步阻塞卡片。 | 无其他阻塞 | 用户对 Q-001 提交真实格式选择并留痕；I-001 变为 `verified` 或合规 `accepted-residual`；无其他阻塞后恢复 `active` | |
