---
id: GOAL-015-audit-command-labeled-form
doc: decision-entry
record_id: D-003
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

## D-003 · 范围扩展：新增 S5 发布阶段与提交边界裁决（2026-10-17）

### 触发

1. 用户 2026-10-17 指令原文：「先提交代码，然后把合并代码到main、确保CI全绿并打tag发布资产的任务作为目标15的最后一个阶段任务。」
2. 上下文：[A-004](../03-audit/A-004-close-out-readiness.md) 关门就绪审视判 `pass`，并明确「重捕获与发布在本目标外、producer 门禁为红、关门待用户」；用户据此把发布链路收回本目标，作为最后一个阶段。
3. 事实约束：release/compatibility 门禁当前为红（`capture_runtime_evidence --check` exit 1；16/16 运行记录过期；`scripts/tests/test_release_evidence.py` 4 failures / 12 errors）。**在重捕获之前 CI 不可能全绿**，tag workflow 的 strict release evidence 同样以矩阵就绪为前提。

### 决定

1. **提交边界**（回应 A-001/A-002 F-002）：选 **(a) 先提交**。检查点 `e396711`（78 files changed, +1010/−102）；只暂存本目标显式 owned paths（55 个已修改文件 + `GOAL-015-…/` 目录），未使用 `git add -A`；提交后工作树为空。事实见 [E-005](../02-execution/E-005-checkpoint.md)。
2. **新增 S5「发布：证据重捕获 → CI 全绿 → 合并 main → tag → 资产验收」** 为 GOAL-015 最后一个阶段。S1～S4 的结论、审计意见与历史记录**不变**（A-004 的「重捕获在本目标外」为作出决定前的当时事实，本条取代其范围判断）。
3. **S5 退出条件**（全部可验证）：
   - a) 16 格运行证据（3 宿主 × 4 治理入口）在当前工作树重捕获，`capture_runtime_evidence --check` 一致；矩阵 `candidateRevision` 指向新版本，`compatibility_report --require-ready` 通过；
   - b) 版本清单同步：CHANGELOG 新版本节、安装 pin、GHCR 示例、相关测试断言；
   - c) 本地全量回归 + strict release rehearsal（`release_evidence --mode rehearsal --run-checks`）通过；
   - d) PR 经 Ubuntu / Windows CI 全绿后合入 `main`；
   - e) annotated tag 指向 merge commit；tag workflow 的 `pack` 与 `Publish GitHub Release (gated)` 全绿，Environment `release` 由**用户人工审批**（AI 不代批、不改配置）；
   - f) Release 资产逐项验收：资产数量、双 ZIP sha256 与 sidecar 一致、Core 为 Skills 的逐字节子集、下载资产驱动的隔离消费安装、GHCR digest 与内置版本核对。
4. **顺序**：S5 内步骤串行（重捕获 → 清单 → 回归/rehearsal → PR/CI → merge/tag/发布 → 资产验收）；不为每个步骤建子目标，除非出现具备独立范围与证据的偏差。
5. **审计模式** `independent`（release / compatibility 高影响门禁）；provider 沿用本目标会话已指定的 **Grok Build**，改派须用户书面指定。
6. **派生 `progress` 随路线图重算**：S1～S4 完成 / S1～S5 共 5 → **80%**。此前的 100% 对应 4 阶段路线图，**不**表示发布完成，也不得被读作关门依据。

### 为什么

- 用户把「修正命令形式」的闭环延伸到正式发布，避免留下「规范已改、但发货资产与运行证据仍是旧形式」的中间态。
- 门禁为红正是发布链路的实际起点：重捕获既是 CI 转绿的前置，也是带标签命令在 16 格矩阵上的首次取证（回应 A-001/A-002 F-001）。
- 版本号会实质影响清单、tag 与资产身份，登记为 I-005 待用户裁决，不静默推定。

### 未选方案

- **维持「重捕获/发布在本目标外」并另立 GOAL-016**：用户明确要求并入本目标作为最后阶段，不选。
- **提交边界选 (b) 等重捕获转绿后一并提交**：用户选择先提交，不选；先提交也为 S5 的 PR 提供干净基线。
- **在 S5 内顺带改动命令语义或扩大拒绝面**：超出 D-002 冻结契约，不选。
- **由 AI 代批 Environment `release` 审批或修改环境配置**：不选；仍须用户人工放行。

### 用户裁决留痕

| 问题 ID | 原题 / 选项 | 影响门禁 | 真实答复 |
|---------|-------------|----------|----------|
| Q-003 | 提交边界：(a) 现在先提交 / (b) 等重捕获转绿后一并提交 | S4 收尾与 S5 基线 | **(a) 先提交**（用户指令「先提交代码」） |
| Q-004 | 发布链路归属：并入 GOAL-015 最后阶段 / 另立 GOAL-016 | 路线图、progress 与关门范围 | **并入 GOAL-015 作为最后一个阶段** |
| Q-005（待答） | 发布版本号：patch `v0.13.7` / minor `v0.14.0` | 版本清单、tag 与资产身份 | 未答复；登记为 I-005（required，门禁 = 版本清单步骤前），不推定 |
