---
id: D-001
goal: GOAL-007-workspaces-directory-consolidation
status: accepted
created: 2026-08-10
updated: 2026-08-10
version: 0.1.0
---

# D-001 · 立项目的、路线图与 cross 审计门禁

## 决定

1. 将显式工作区 canonical 路径收敛为 `{governance_root}/workspaces/workspace-<NNN>-<slug>/`。
2. 先修订核心方法论与分发契约，再迁移本仓三个工作区；不得只移动实例目录而保留旧发现、安装或打包规则。
3. 采用 S1～S5 串行路线，正式发布属于目标成功边界，不把 PR、tag 或资产发布写成预期外的可选后续。
4. 审计模式为 `cross`：本变更同时触及元规则、协议、迁移和 release 边界，S4 至少需要 self + 指定 provider independent。
5. I-002 在 provider 指定前阻断 S2；provider 失败、超时或无可核对输出时不得静默降级。

## 理由

旧布局在工作区数量增加后持续占用治理根的第一层，降低文档查阅效率。引入固定 `workspaces/` 容器能将运行时目标真相与 architecture、vision、templates、contracts 等治理资料分区，同时保留工作区内部目标平铺、Root 绑定与隔离不变量。

## 未选方案

- **只迁移本仓目录，不改协议**：会导致消费者、MCP、安装器和测试继续按旧路径发现，违反 fail-closed 与 canonical 单一真相。
- **长期双布局并存**：会制造两种活动显式工作区布局和歧义发现；是否允许仅用于一次性迁移检测，留给 I-001/D-002 冻结。
