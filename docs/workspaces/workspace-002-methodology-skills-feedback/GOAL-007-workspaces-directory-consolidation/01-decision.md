---
id: GOAL-007-workspaces-directory-consolidation
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-10
updated: 2026-08-10
version: 0.3.0
---

# 决策记录 · GOAL-007

## 信息需求与阶段门禁

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 决策 |
|----|------|-----------------|----------|--------------|-----------------|------|-------------|-------------|
| I-001 | required | 旧直属路径到 `workspaces/` 的兼容/迁移策略 | S1 方案冻结 / S2 实施 | S1 | 跨协议、安装器、MCP、packaging、工作区和历史链接盘点后写 D-002 | **verified**（2026-08-10） | 混合布局或迁移工具需求变化时复核 | D-002：唯一新 canonical + 旧布局迁移引导 + 混合 fail closed |
| I-002 | required | cross audit independent provider | S2 实施 | S1 | 用户指定 provider；provider 不可用时 fail closed | **verified**（2026-08-10） | provider 失效时回到门禁 | 用户书面指定 Grok Build；D-004 |
| I-003 | required | 正式发布版本与 tag/revision | S5 发布 | S3 验收前 | 对齐当前版本源、candidateRevision、workflow 与已发布 Release | **verified**（2026-08-10） | main/tag 基线前移时重算 | D-003：`v0.13.2` |

## 决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-001 | 2026-08-10 | 立项目的、路线图与 cross 审计门禁 | accepted | `01-decision/D-001-goal-scope-and-gates.md` |
| D-002 | 2026-08-10 | 工作区布局迁移与兼容策略 | accepted | `01-decision/D-002-layout-migration-compatibility.md` |
| D-003 | 2026-08-10 | v0.13.2 发布基线与门禁 | accepted | `01-decision/D-003-release-baseline-v0-13-2.md` |
| D-004 | 2026-08-10 | cross audit provider 与职责边界 | accepted | `01-decision/D-004-cross-audit-provider.md` |
