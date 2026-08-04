---
id: GOAL-001-main-vision
doc: decision-entry
record_id: D-029
status: accepted
parent: null
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# D-029 · 退役冻结 Web 资产并正式挂起 VP-003

## 触发

用户书面决定：冻结 Web 遗产持续占用回归测试和全量审计注意力，保留成本已经高于参考价值；要求彻底移除资产、挂起对应 VP，并推进到完成，同时不得损坏核心方法论文档或 Skills 资产，也不发布新的方法论 / Skills 版本。

## 决定

1. **窄幅取代 D-027** 的两项旧约束：撤销“默认不删除 `web/`”与“物理退役是非目标”；D-027 的 Skills 主投资面、H-WEB-01、不得借退役宣称 Web 产品终态等其余内容继续有效。
2. **物理退役范围**：删除仓库 `web/` 全部冻结资产，并移除只为该资产存在的 CI、release-evidence Web check、compatibility matrix Web parser consumer、对应测试与现行入口链接。
3. **历史记录保留**：workspace-001 既有 Goal 决策、执行、审计、附件和历史发布叙述不做批量改写。历史链接可失效，但不得把过去的 Web 证据伪装成从未发生。
4. **VP-003 正式挂起**：保持 VP 合法状态 `planned`，正文明确无排期、无绑定工作区、无当前实现门禁；恢复须新的书面决策、边界和工作区，不复活本次删除的 FastAPI 资产。
5. **实施承接**：不重开已 `done` 的 workspace-001 Root，不在封存树创建 GOAL-024；由 [workspace-002 GOAL-004](../../../workspace-002-methodology-skills-feedback/GOAL-004-frozen-web-asset-retirement/00-meta.md) 承接一次性退役和验证。
6. **保护边界**：`docs/architecture/principles.md`、`docs/architecture/workspace-protocol.md`、`docs/templates/**`、`skills/prompts/**`、`skills/install/**`、`skills/core/**` 不改；`docs/contracts` 只删除 Web consumer 声明并通过 stage 生成唯一允许变化的 `skills/contracts` 镜像。
7. **发行边界**：本次不创建 tag、GitHub Release 或新方法论 / Skills 版本；CHANGELOG 只记 `Unreleased` 仓库维护事实。

## 为什么

- 冻结资产仍被 Linux/Windows CI、release evidence 与兼容矩阵强制带入每次全量验证，已经持续消耗与现行 Skills 主路径无关的工作流成本。
- 未来人类 UI 方向仍由 Charter 与 VP-003 保留；保留方向不要求保留一套已冻结且不再投资的具体实现。
- 在封存 Root 写后置授权、在活动 workspace-002 新建实施目标，既尊重 D-027 的历史所有权，也不破坏工作区封存和跨区 `parent` 边界。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 继续冻结并从 CI 跳过 | 资产和引用仍会进入审计与维护面，不能实现彻底退役 |
| 把 VP-003 改为非法 `paused` 状态 | VP schema 不支持；用 `planned` + 正文挂起可以准确表达 |
| 删除历史 Goal / 审计证据 | 会破坏可追溯性并改写已发生事实 |
| 顺带修改或发布方法论 / Skills | 超出用户边界，且退役无需协议版本变化 |

## 放行与关门

- 实施审计模式固定为 **independent**：改动触及 producer release / compatibility 门禁，但不改元规则，故无需 cross。
- workspace-002 GOAL-004 完成资产删除、现行引用清理、镜像验证、核心/Skills 边界校验与独立审计且开放 required 为 0 后，才可标记完成。
- `R-009-X` 继续作为未来 UI 产品终态宣称的历史 residual 指针；物理删除不会自动将其 `fixed`。
