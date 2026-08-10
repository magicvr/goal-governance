---
id: A-016
goal: GOAL-001-mcp-file-dual-channel-delivery
title: 独立复审 · F-001～F-005、F-007 关闭证据（A-014/A-015 响应核验）
status: recorded
source: independent
provider: grok build / 经 /audit skill 入口执行
date: 2026-08-07
scope: workspace-003 Root（GOAL-001，done）post-close 维护轮的 finding 关闭证据复审：F-001（L3 重捕获）、F-002（server 版本发布钉）、F-003（File 包测试隔离）、F-004（initialize 门禁）、F-005（lifecycle root 信任边界）、F-007（directory-layout 增补 mcp/）；不修改任何 status/progress/VP/workspace 状态
audit_type: finding-closure
verdict: conditional
version: 0.1.0
---

# A-016 · 独立复审：F-001～F-005、F-007 关闭证据（2026-08-07）

## 结论

**verdict: `conditional`。**

对 A-014（F-001 选项 A / F-002 / F-003 fixed）与 A-015（F-004 / F-005 / F-007 fixed）的关闭证据逐条独立复核（亲自执行：全量测试、stage 检查、真实打包、哈希比对、git 时序核验）：

- **F-002 / F-003 / F-004 / F-005 / F-007：关闭证据充分、可重复核对。**
- **F-001：fixed 声明在 A-015 修改 `mcp/server.py` 后再次过期**——四条 L3 证据 JSON 的 `behaviorSources[server.py]` = `c0af461ece…`（A-014 重捕获时点正确），当前树 `mcp/server.py` 哈希为 `cd31cbdebe…`（A-015 修 F-004/F-005 所致，提交 `7087d6a` 晚于重捕获提交 `8770825`）。Root `00-meta` 宿主表备注「behaviorSources 哈希与当前树一致」再次字面不成立。

功能语义未受影响（L3 探针为宿主 File 通道只读 dispatch 探针，不经 MCP server 进程；MCP 面由 L1/L2 与 210 测试覆盖），本缺口属**证据账本可复核性**（med，与原 F-001 同类），不构成对关门状态或任何门禁的阻断。

- **auditor**：grok build · 独立复审 · 经 `/audit` skill（`05-independent-audit.md`）执行
- **source**：`independent`

## 范围与区间

| 项 | 内容 |
|----|------|
| 工作区 | `workspace-003-mcp-file-dual-channel`（closed） |
| Root | `GOAL-001-mcp-file-dual-channel-delivery`（done · progress 100%） |
| 复审对象 | A-012（independent）F-001～F-008 → A-013 登记 → A-014（F-001 选项 A/F-002/F-003 fixed）→ A-015（F-004/F-005/F-007 fixed） |
| 本审 scope | F-001～F-005、F-007 关闭证据（F-006 归 VP-002、F-008/I-007 首次真实 GHCR 发布验收，不在本审） |
| 排除 | 不改 status/progress/检查点；不改 VP-004 / workspace.md / goal-tree；不写 Vision Review |

## 独立核验动作（本审亲自执行）

| 动作 | 结果 |
|------|------|
| `python -m pytest docs/tests skills/tests scripts/tests -q` | **210 passed**, 4 skipped, 4 subtests passed（~41s）——与 A-015 声明一致 |
| `python scripts/stage_skills_mirrors.py --check` | **ok**（36 pairs；0 漂移）——F-007 镜像已随提交同步 |
| `pack_skills_release.py --version 0.0.0-auditcheck`（临时目录） | **77 成员**；zip 内 `test_mcp_*` **0 条**；`mcp/` 实现路径 **0 条**；其他 skills 测试保留（`test_install_ps1_isolated.ps1`、`test_skills_orchestrator.py` 等） |
| 当前树哈希 vs L3 JSON `behaviorSources` | `entries.py` `ab183e15…` ✓ 一致；`kernel.py` `b0168b2e…` ✓ 一致；四个探针 prompt 哈希（`a423385d…`/`5d98a018…`/`107ebc4b…`/`fe57e7b7…`）✓ 全部一致；**`server.py`：JSON `c0af461e…` ≠ 当前树 `cd31cbde…` ✗** |
| 四条 L3 JSON 元数据 | capturedAt 2026-08-07T15:34:55Z / 15:35:10Z / 15:36:57Z / 15:37:48Z（落在 A-014 声称区间）；verdict 全 `pass`、exit 0、marker observed；stdoutPath 目录名与磁盘实际一致（含 grok `-l3-four-entry-…d` 修正） |
| git 时序 | `8770825`（23:39 重捕获 L3 + F-002/F-003，A-014）→ `7087d6a`（23:47 修 F-004/F-005/F-007，A-015，改 `mcp/server.py`）——**server.py 在重捕获后被修改** |
| git 工作树 | 干净（无未提交变更） |
| 测试断言存在性 | `McpVersionPinTests`（env 覆盖/回退/serverInfo）、`McpInitializeGateTests`（tools/list·tools/call·ping 握手前 `-32002`）、`McpLifecycleRootBoundaryTests`（install/doctor 越界 `-32602`）、`test_pack_skills_release.py`（`should_exclude` test_mcp_*、workflow `build-args` 契约）均存在且随 210 绿 |

## 对照关闭声明逐条核验

| Finding | 声称 | 独立核验 | 判定 |
|---------|------|----------|------|
| **F-001**（L3 `behaviorSources` 与当前树不一致） | A-014 fixed（选项 A：四宿主同 prompt/同版本重捕获；`behaviorSources` = `mcp/*` 当前哈希；00-meta 备注恢复字面成立） | 重捕获本身真实（capturedAt/verdict/prompt 哈希/entries/kernel 哈希全对）；但 **A-015 改 `server.py` 后哈希演进为 `cd31cbde…`，四条 JSON 仍绑 `c0af461e…`**——「与当前树一致」再次字面不成立；00-meta 备注失效；runtime README「捕获点与重捕获」节存在但未覆盖 A-015 之后的哈希演进 | **fixed 声明需刷新**（med 证据缺口） |
| **F-002**（`mcp/__version__` 与发布 tag 脱节） | A-014 fixed | `mcp/__init__.py` `MCP_LAYOUT_VERSION` 独立 + `effective_version()` 读 `GOAL_GOVERNANCE_MCP_VERSION`；Dockerfile ARG/ENV 接线；workflow docker 步骤 `build-args: GOAL_GOVERNANCE_MCP_VERSION=${{ needs.pack.outputs.version }}` 且 GHCR tag 同源；`doctor.py` 分列 `server.version`/`server.layoutVersion`；README「版本语义」节；测试断言在 | **充分** |
| **F-003**（File zip 内 MCP 测试隔离） | A-014 fixed | `pack_skills_release.py` `should_exclude` 增 `tests/test_mcp_*`（注释引 F-003）；单元断言 + 真实打包片段断言；**本审实包复核 77 成员、0 `test_mcp_*`、0 `mcp/` 实现** | **充分** |
| **F-004**（未强制 initialize 顺序） | A-015 fixed | `server.py` `serve()`：`initialize` 之外的方法在 `self.initialized` 前返回 `-32002`（含 `ping`；`notifications/initialized` 通知路径不受影响）；`McpInitializeGateTests` 4 条断言在 | **充分** |
| **F-005**（lifecycle `root` 任意目录） | A-015 fixed | `server.py` `_handle_lifecycle_call`：`root.relative_to(self.repo_root)` 越界 `-32602` fail closed；四个 lifecycle schema `root` 描述注明；README「安全与信任模型」节；`McpLifecycleRootBoundaryTests` 3 条断言在 | **充分** |
| **F-007**（`directory-layout.md` 缺 `mcp/`） | A-015 fixed | `docs/architecture/directory-layout.md` v0.6.5 目录树含 `mcp/` 块 + 「通道资产分离（VP-004 R4 / A-012 F-007）」约束；stage 镜像已同步（本审 `--check` 36 对 0 漂移） | **充分** |

## Findings（本审）

| ID | source | 级别 | 严重度 | 说明 |
|----|--------|------|--------|------|
| **F-001r** | independent（本审） | recommended | med | **F-001 关闭证据过期**：A-014 重捕获后，A-015 修改 `mcp/server.py`（F-004/F-005 修复，提交 `7087d6a`），当前树哈希 `cd31cbdebe10e15cc6d6b2f47e6ba365874cd1c9ffb87cf847f75b3d1bdedb82` ≠ 四条 L3 JSON `behaviorSources[server.py]` `c0af461ece0b4e5f4b8a3421daed91538869d7f3f97bb0a61838ccd86c2ecc46`；Root `00-meta` 宿主表「behaviorSources 哈希与当前树一致」备注再次字面不成立；runtime README「捕获点与重捕获」节未记录 A-015 后 server.py 的哈希演进。证据路径：四条 `GOAL-002/attachments/runtime/evidence/*-l3-four-entry-2026-08-07.json`（behaviorSources）、`mcp/server.py`（当前哈希）、`git log 7087d6a`、`00-meta.md` 宿主表备注。功能语义不受影响（L3 为 File 通道只读 dispatch 探针，不经 MCP server；L1/L2 + 210 测试覆盖 MCP 面）；属证据账本可复核性缺口，与原 F-001 同类。 |

## 必改项汇总

无 required / 必改项（本审缺口为 recommended · med，延续 A-012 无 required 的判定；不阻断任何门禁，不回退关门状态）。

## 与既有意见的异同

- 与 **A-012**（原 independent）：本审确认其 F-001 原始问题在 A-014 后**复发一次**（A-015 改 server.py 未同步证据账本）；其余 F-002～F-007 修复与 A-012 建议一致且证据充分。
- 与 **A-014 / A-015**（self）：本审独立复核其声称；A-014 的 F-001 关闭声明在其实施时点（23:39）成立，A-015（23:47）使其在字面层过期——两轮 self 审计本身真实，缺的是「修改 `mcp/` 实现后刷新 L3 证据」的维护钩子。
- 无 required 冲突；无与既有 independent 意见互斥。

## 结论 + 建议给编排器 / 用户的下一步

1. **F-002 / F-003 / F-004 / F-005 / F-007：关闭证据充分，维持 fixed。**
2. **F-001：fixed 声明需补充**（无需 reopen、无需重跑四宿主——探针语义不经 MCP server 进程，重捕获收益低）。建议 `/govern` 采纳 **选项 B 同构注解**：
   - `GOAL-002/attachments/runtime/README.md`「捕获点与重捕获」节补记：A-015（F-004/F-005）后 `server.py` 哈希 `c0af461e… → cd31cbde…`；L3 探针只读 dispatch 不经 MCP server 进程，MCP 面复核以 L1/L2（210 测试）为准；或按选项 A 重捕获刷新 JSON。
   - Root `00-meta` 宿主表备注改为可复核表述：「behaviorSources 哈希与捕获时点一致（entries/kernel 与当前树一致；server 哈希演进见 GOAL-002 runtime README 重捕获节）」。
3. **防再犯（recommended）**：为 `scripts/capture_runtime_evidence.py` 或 CI 增加「L3 证据 `behaviorSources` 与当前树哈希」一致性检查（纳入 `scripts/tests/`），使修改 `mcp/` 实现后证据过期在测试层即暴露。
4. F-006（VP-002）、F-008/I-007（首次真实 GHCR 发布验收）维持既有归属，不在本审范围。

### 建议的下一句（可选）

```text
/govern 响应 Root A-016（independent conditional）：F-002/F-003/F-004/F-005/F-007 维持 fixed；F-001 关闭证据过期（server.py 哈希演进），按选项 B 注解 runtime README + 00-meta 备注，并评估 capture 一致性检查
```

## 声明

本意见不修改任何 `status` / 检查点 / 派生 `progress` / 方案正文 / goal-tree；响应与改状态由 `/govern` 处理。
