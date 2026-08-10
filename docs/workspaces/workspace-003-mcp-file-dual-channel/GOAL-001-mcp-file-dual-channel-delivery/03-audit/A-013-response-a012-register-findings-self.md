---
id: A-013
goal: GOAL-001-mcp-file-dual-channel-delivery
title: 响应 A-012（independent pass）· 登记 F-001～F-008（self · 编排器）
status: recorded
source: self
date: 2026-08-07
scope: 响应 A-012（independent，post-close，pass）的 recommended findings F-001～F-008；登记处置与触发；不改变任何目标 status/progress、不修改 VP-004 / workspace 状态
verdict: pass
version: 0.1.0
---

# A-013 · 响应 A-012 并登记 F-001～F-008（2026-08-07）

## 结论

`pass`。A-012（independent · grok build 独立会话 · 未加载 Skill）**verdict pass、无 required findings**，与既有意见（A-009/A-010/A-011、GOAL-005 A-002/A-003）**无冲突** → 不触发 P-004 裁决、不构成任何门禁阻断，**不回退** Root `done` / 子目标 done / VP-004 `closed` / workspace `closed` / goal-tree 状态（与 A-012 自身处理决定一致）。

recommended F-001～F-008 按用户 2026-08-07 指令**全部登记**（open，非必改），逐条给出拟处置与触发条件；**本条目不宣布任何 finding `fixed` / `accepted-residual` / `user-overruled`**——推荐项处置方案（尤其 F-001 选项 A/B、F-002、F-003 的取舍）留待用户确认的维护轮执行。

## 响应对象

- **A-012**（independent · 关门后独立审计：方法论/Skills 完整性 + MCP server 体系）verdict `pass`；required 0；recommended F-001～F-008。
- 核验面：198 passed / stage `--check` 36 对 0 漂移 / pack 80 成员 0 `mcp/` 实现 / L2 10/10 / fail closed 现场 / tools 无 commit。
- A-012 自身建议：无需回退关门；F-001～F-003 优先维护；F-006 挂 VP-002 消费面。

## Findings 登记表

| Finding | source | 级别 | 登记状态 | 拟处置（待维护轮） | 触发 / 留痕 |
|---------|--------|------|----------|--------------------|-------------|
| **F-001**：L3 `behaviorSources` 与当前树字面不一致（R4 迁 `mcp/` 后证据账本过期；`server.py` 哈希合法演进；Root 00-meta 宿主表备注「与当前树一致」在字面路径层不成立） | independent | med | **open** | 选项 A：重捕获 L3 并将 `behaviorSources` 更新为 `mcp/*` 当前哈希（需 reopen 性质维护轮）；选项 B：Root 宿主备注 + GOAL-002 runtime README 注明「R1 捕获点绑定历史路径；R4 后以 remap + L1/L2 复核」 | 用户选择 A/B 后执行；不据此宣称宿主 L3 当时 verdict 作废 |
| **F-002**：`mcp/__version__ = "0.1.0"` 与发布 tag 体系（0.13.x）脱节；经 MCP tools 安装会写入 0.1.0 | independent | med | **open** | 发布时以构建参数/环境/`__version__` 与 pack version 同源钉死；或明确「server 内部 layout version ≠ 产品 release version」并由 doctor 分列报告 | 下一次发布轮 / 维护轮 |
| **F-003**：File zip 内 `tests/test_mcp_*.py` 在纯 skills 解包环境失败（本审隔离解包 6 failed） | independent | low | **open** | pack 排除 MCP 集成测试；或文档标明「仅 monorepo CI」，避免消费者误判 File 通道损坏 | 维护轮（与 F-001/F-002 同批） |
| **F-004**：MCP 协议未强制 `initialize` 后再 `tools/list|call` | independent | low | **open** | 可选：未 initialize 时拒绝 tools 并返回明确错误 | 维护轮，按需 |
| **F-005**：lifecycle `root` 参数可指向任意本机目录并写 AGENTS.md（allowlist 相对该 root） | independent | low | **open** | 文档声明信任模型；可选：默认强制 `root` ⊆ server.repo_root | 维护轮，按需 |
| **F-006**：消费面路径收敛未完成（`skills/AGENTS.template.md`、四治理 prompts 硬编码 `docs/…`） | independent | low | **open** | 归 **VP-002 消费面/协议正文收敛**（A-012 建议；与 A-009 R-001 扫尾同类），**不** reopening workspace-003 | VP-002 推进或下一次协议面修订轮 |
| **F-007**：`directory-layout.md` 未反映 R4 根目录 `mcp/` | independent | low | **open** | 增补 monorepo 布局一行（与 README 对齐） | 维护轮（可与 F-001 选项 B 同步） |
| **F-008**：真实 GHCR 发布物未在本审环境验证可 pull（non-blocking） | independent | info | **open** | **并入既有 I-007**（GOAL-005 登记，non-blocking，同触发） | 首次真实 `v*` 发布后回填 digest/URL 并关闭 I-007 |

## 登记结论

- **无 required / 必改项**：不触发任何门禁；A-012 不改变关门语义。Root `done`（progress 100%）、GOAL-002～005 `done`、VP-004 `closed`、workspace `closed` 状态**保持不变**；goal-tree 无变化（无状态/检查点变更，无需更新）。
- F-001～F-008 全部为 open 非必改登记项，均有明确处置路径与触发条件；其中 F-001/F-002/F-003 为 A-012 建议的优先维护项，F-006 移交 VP-002 波次，F-008 与 I-007 合并跟踪。
- 未将任何推荐项伪装为已闭合或 required；未把编排响应标为 `source: independent`。

## 仍开放项（均不阻断）

- F-001 选项 A/B 待用户选择（重捕获 L3 vs 历史路径注解）。
- F-002～F-005、F-007：待维护轮按登记表执行。
- F-006：归 VP-002 消费面波次。
- F-008 / I-007：首次真实 GHCR 发布验收时关闭。
- 观察（非本 scope）：Charter「现行版本」表仍列 VP-004 为 active，与 VP-004 文件 `status: closed` 不一致——属愿景层维护，建议后续 `/vision` 轮顺手更正。

## 边界

- 未修改任何目标 `status` / 检查点 / 派生 `progress`；未改 VP-004 / workspace.md 状态；goal-tree 未变。
- 本响应为编排器 self 侧记录（response 模式），不冒充 `source: independent`。
- 真实 GHCR 发布、L3 重捕获与消费面模板收敛不在本登记范围内，需用户确认后另行执行。
