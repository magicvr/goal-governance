---
id: GOAL-019-independent-audit-lifecycle
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-13
updated: 2026-11-13
version: 0.1.0
---

# D-001 · 范围、证据及发布路径冻结

- 日期：2026-11-13
- 状态：accepted
- 授权来源：用户本轮要求「在工作区2增加一个新的子目标承载治理上下文，完成这个修正。在dev分支完成，然后提交pr合并到main分支并发布新版本资产」。

## 决定与理由

1. 在本区 Root 的 R3 下创建 GOAL-019，不另开工作区/VP、不修改 Charter。该反馈属于既有 VP-002 的真实消费问题。
2. 先修 `docs/architecture/principles.md` 的独立审计契约，明确正式审计本身不因子代理承载而自动继承普通探索策略；同时明确派发方监测、完成、异常中断与未满足门禁责任。`governance-guide.md` 同步摘要，再 stage 生成镜像。沿用 AD-01～AD-06，不为本次调用追加解释或隐藏上下文。
3. 现有 govern/vision/audit/vision-audit 入口都强制读取指南与 principles，因此无需修改 Skills prompts、宿主 wrappers 或 MCP 实现。生成的 core 镜像及发布元数据仍需随版本更新；不能把“不改 Skills 实现”理解为“不更新分发包”。
4. 用户明确适用于审计的策略、取消、权限和宿主硬限制仍有效；正式台账写入权限不扩大到业务代码或治理状态。审计内部普通探索子代理继续遵守消费仓策略。
5. 版本采用未占用的下一 patch v0.15.1。dev checkpoint → PR 到 main → CI → merge → annotated tag → 受保护发布 → 正式下载资产/GHCR 验收。用户已经授权该执行链，不重复索取一般步骤确认；实际 Environment 人工门禁依其保护机制处理，不绕过。
6. 审计模式 cross，provider 按项目 `.goal-governance.json.independent_audit` 复用 Grok / grok-4.7 / xhigh。正式调用只有 `/audit workspace-002 goal-019`，不复制编排历史；不套用旧探针的600秒参数作为正式审计时限。

## 证据策略（I-001 / I-002）

基线现行 v0.15.0 的18份信封一致性检查通过，compatibility ready。逐项读取选用信封发现12格CLI（Claude/Grok/Copilot × 四入口）及4格MCP目录探针都把 principles/governance-guide 列入 behaviorSources。两份权威变化后16格均须重新采集；历史信封不得只重写哈希。采集完成后更新 canonical matrix 的 candidateRevision、证据路径与范围，再 stage contracts 镜像。

运行证据只支持相应代表入口及台账边界，不宣称已经验证任意宿主中的十分钟中断、所有原生目标机制或系统级强制隔离。采集夹具可保留普通探索策略以验证审计入口不会被只读探子约束误用。

## 未选方案

- 仅在审计员入口补一句：派发方仍可能提前终止，不能完整覆盖反馈。
- 所有仓库规则整体豁免：会扩大权限并覆盖用户明确策略，不符合修正边界。
- 不重采或更新旧信封哈希：两份权威属于已固定行为源，违反发布新鲜度与真实采集要求。
- 为减少采集而避开 canonical：会产生第二套规范，不能接受。

## owned paths 与后续

本目标五件套及附件、父 meta、当前 goal-tree/workspace 摘要、两份 canonical 与其 core 镜像、v0.15.1 runtime、canonical/镜像矩阵、CHANGELOG、当前安装/GHCR pin、发布 evidence-dir 与相应版本断言。只暂存这些明确路径；测试/采集输出另放 artifacts 或本目标附件。先完成 S2，再以当前来源采集与审计，未验证结果保持 open/collecting。
