---
id: A-018
goal: GOAL-008-consumer-layer-split-and-hosting
doc: audit-entry
record_id: A-018
source: independent
provider: grok build / grok-4.6 / reasoning-effort high（本地 CLI `grok` 1.0.30）
scope: 发布后/关门前独立核验（发布身份、台账陈述、legacy 迁移实测、开放 required）
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# A-018 · 发布后独立核验（grok build · grok-4.6 · high，2026-09-13）

> 独立会话**只读**核对（含自行构造的 legacy 迁移实测，未写入仓库）。编排器代贴落盘并保留 `source: independent`。
> **重要时点说明**：本审在编排器**正在改写台账期间**读取工作树，因此其“台账与 git/GitHub 不一致”的判断对应的是**中间态快照**；编排器随后完成了同一批改写。下文保留独立会话原文判断，并在 [A-019](A-019-response-a018.md) 逐条核对当前事实。

## verdict

**conditional**

## 独立核对结果（要点）

### 发布身份（独立会话读数 vs 当时台账）

| 项 | 只读事实（独立会话） | 当时台账 | 一致 |
|----|----------------------|----------|------|
| `origin/main` HEAD | `dfa8600`（GitHub 签名 merge，双亲 `d073f44`+`4e6c8fd`） | 已写 `dfa8600` | 是 |
| tag `v0.13.3` | 对象类型 `tag`；tag 对象 `5580bfdf…` → `dfa8600`；tagger 2026-09-13T17:04:28+08:00；与 `ls-remote` 一致 | 部分文件仍写「tag 已删除、待重打」 | **否（中间态）** |
| GitHub Release | **存在且 Latest**：published `2026-09-13T09:11:04Z`，`targetCommitish=main`，9 项资产 `uploaded` | `CHANGELOG`/`README` 仍写「尚未发布」 | **否（中间态）** |
| tag workflow | `34748891084` **success**（pack + Publish 全绿，含 Create Release / Upload assets / GHCR）；原 `34748633773` 仍 queued | 凭据只登记了原 run | **漏记**（后已补） |
| GitHub PR #21 | `state=open`、`merged=false`（尽管 merge commit 已在 main） | 台账写「已 merge」 | 台账与 git 一致；**PR UI 状态为残留** |

独立会话明确记录：**没有**出现「把未发生的发布写成已发生」的超前宣称（A-013 F-002 已被 A-014 改正）；本次方向相反，是**发布完成后台账未跟上**。

### legacy 迁移实测（独立构造，4 例）

| 例 | 构造 | 结果 | 独立会话判读 |
|----|------|------|--------------|
| A | 包内嵌套规则面整份副本，改**内层对内部**一行 | `sentinel_preserved=False`、框架行恢复 | **不算丢消费方内容**（在内层标记对内＝框架受管区） |
| B | pre-S4 规则面（仅内层对）改内层一行 | 同上，且出现规则面重复包裹 | 同上 |
| C | 与源完全一致 | `changed=False`、无丢失 | 支持不变量 |
| D | 消费者内容在**区间外** | `changed=False`、区间外保留 | **支持不变量** |

独立结论与编排器的自查一致：**区间外保留成立；区间内按设计刷新**。同时指出 `merge_agents_text` 的 docstring/注释**与实现不符**（写 keep verbatim、实际替换 frame）——见 F-002。

## Findings

### F-001 · 台账发布身份与 git/GitHub 事实分裂（required / high）

| 字段 | 值 |
|------|-----|
| evidence | tag `refs/tags/v0.13.3` → `dfa8600`（类型 `tag`）；Release `v0.13.3` Latest、9 资产 `uploaded`；run `34748891084` publish success；对比当时 `00-meta` S6 行、`v0.13.3-halt-and-misdiagnosis-correction.md` §6、`CHANGELOG`、`docs/README` 仍写「未发布／tag 已删／待审批」 |
| 影响门禁 | 发布身份 / S6 关门；但独立会话明确「F-005 保持 open 直到 sha256 复核落盘」 |

### F-002 · `merge_agents_text` 注释与实现不符（recommended / low）

| 字段 | 值 |
|------|-----|
| evidence | 独立会话 A/B 例：`sentinel_preserved=False`；`skills/agents_merge.py` 注释写「keep verbatim」，代码为 `target[:begin] + block + target[end:]` |
| 影响门禁 | 无（不推翻 S4 不变量，不构成补丁发布理由） |

## 与既有意见的异同

- 与 A-001 F-005 / A-015 同向：产出已出现，缺的是**核对与台账改写**。
- 与 A-013 F-002 / A-014 同向：公开台账必须与 tag/workflow 同相（本次为反方向）。
- 与编排器的「误判更正附件」产品结论同向：区间内被替换 ≠ 丢消费方内容。
- 无「一要一否」冲突需要用户裁决。

## 范围与限制（独立会话自述）

只读指定路径与只读 `git`/`gh`；未跑测试、未重下载 zip 做字节比对，故**不能**代为闭合 A-001 F-005；未追 PR timeline；`merge` 实验为合成嵌套面。

## 建议下一步（独立会话原文要点）

1. **不要**撤回 tag、**不要**改实现去「保住」区间内那一行；
2. A-001 F-005 保持 open，直到按 D-011 重下载 9 项资产、与 sidecar 逐项比对并写入凭据；
3. 立刻改写已过时的台账陈述（S6 / I-006 / 更正附件 §6 / CHANGELOG / README）；
4. 处理仍 queued 的 `34748633773`，并核对 PR #21 为何仍 open，避免重复 merge；
5. F-002：把注释改成与代码/测试一致的措辞。
