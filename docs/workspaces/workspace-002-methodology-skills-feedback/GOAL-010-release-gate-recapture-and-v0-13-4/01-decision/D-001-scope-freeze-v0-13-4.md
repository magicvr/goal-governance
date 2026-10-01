---
id: D-001
goal: GOAL-010-release-gate-recapture-and-v0-13-4
doc: decision
title: 范围冻结：v0.13.4 patch 发布，走证据重捕获而非回滚
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-01
updated: 2026-10-01
version: 0.1.0
---

# D-001 · 范围冻结：v0.13.4 patch 发布，走证据重捕获而非回滚

**状态**：accepted（2026-10-01）

## 触发

用户要求「推送 PR，确保 CI 全绿后合并到 `main`，再打 tag 发布新资产」。编排前的只读核对发现 `dev` 顶端的发布门禁是红的。

## 核对到的缺口（事实）

在同一台机器上对两个检出点跑同一条测试：

| 检出点 | `scripts/tests/test_release_evidence.py::test_rehearsal_evidence_never_claims_a_release` |
|--------|------------------------------------------------------------------------------------------|
| `4d35623`（v0.13.3 证据录制提交） | 通过 |
| `d30abb3`（`dev` 顶端） | 失败：`release evidence failed: runtime evidence behavior source is stale: AGENTS.md` |

`docs/releases/runtime/v0.13.3/` 的 **12 份**证据全部记录：

| behavior source | 证据记录值 | 当前树值 |
|-----------------|------------|----------|
| `AGENTS.md` | `edccf61a…` | `e8afa1d4…` |
| `skills/prompts/00-govern-orchestrator.md` | `d2df7a81…` | `222d37a7…` |

这两个文件在 `d1256eb`（GOAL-009 S2「记录研究门禁区分」）被修改，证据录制点 `4d35623` 在其之前。因此 `d1256eb` 之后 `dev` 上：
`scripts/compatibility_report.py` 失败、`release_evidence.py --mode rehearsal --run-checks` 失败、`scripts/tests` 4 failures / 12 errors。

`d1256eb` 的改动本身是正确的：它把 P-005 的「结果尚不存在时」例外写进原则、AGENTS 摘要与编排提示。回滚它等于撤销 GOAL-009 已关门的规则修正。

## 决定

1. **修复路径是重捕获，不是回滚。** 对当前树重跑 **3 宿主**（claude-code-cli / grok-build-cli / github-copilot-cli）× 4 治理入口 = 12 格 L3 证据，落在**新目录** `docs/releases/runtime/v0.13.4/`；v0.13.3 与更早的目录保留为历史捕获点，不改写。codex 不是矩阵消费者，不参与这 12 格。
2. **发布版本 = `v0.13.4`（patch）。** 依据：`dev` 相对 v0.13.3 是修正性质（安装器 containment 路径、AGENTS 空后缀保留、GOAL-009 治理记录）。用户 2026-10-01 裁决确认。
3. **发布纪律沿用 GOAL-008（v0.13.3）**：annotated tag 只指向**已合并 `main` 的 merge commit**；资产集合沿用 9 项形态（skills/core 双 zip + 各自 `.sha256` + 双 bootstrap 脚本 + bootstrap README + release-evidence + compatibility-report）；publish job 必须经 Environment `release` 人工审批。
4. **不改 `docs/architecture/` 与 `docs/templates/` 的 canonical 正文。** 本轮只改契约、测试、CHANGELOG、README pin 与证据目录。
5. **`docs/contracts/**` 在 stage 白名单内**，因此同一提交内必须 stage 镜像并 `--check`。

## 未选方案

| 方案 | 未选理由 |
|------|----------|
| 回滚 `d1256eb` 的 AGENTS/编排提示改动，让旧证据重新有效 | 会撤销 GOAL-009 已关门并已审计的 P-005 语义修正；用「删掉正确改动」换绿灯是把门禁当装饰 |
| 手改 12 份证据里的 sha256 让它匹配当前树 | 证据必须来自真实探针执行；改哈希是伪造，且违反「不得把未验证写成已验证」 |
| 发布 go 前只把 `dev` 门禁转绿，发布另起一轮 | 用户明确选择本轮完整执行到 tag |

## 仍待后续

- 若某个宿主在本机无法产出 `pass` 证据，该格保持未满足，门禁回到未通过；不得静默降级或以其他宿主顶替（见 `00-meta.md` I-002）。
