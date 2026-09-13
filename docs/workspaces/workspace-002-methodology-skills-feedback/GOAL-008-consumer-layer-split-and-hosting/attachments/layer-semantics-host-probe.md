---
id: GOAL-008-consumer-layer-split-and-hosting
doc: attachment
title: 层语义 CE1–CE10 宿主探针证据（S6）
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# 附件 · 层语义宿主探针（2026-09-13）

> 目的：闭合 [A-005](../03-audit/A-005-s2-stage-self.md) **F-001**／[A-013](../03-audit/A-013-independent-s6-close-review.md) **F-001**——S2 通过阈值要求「静态谓词 **加上** 至少一个真实宿主对 CE1–CE10 corpus 复核」。
> 探针：`attachments/probes/layer-semantics-probe.txt`（只读；要求逐例输出 `{verdict, action, evidence}` + marker）。
> 判据：`attachments/s1-acceptance-matrix.md` §4 的判定键。

## 1. 原始输出

| 宿主 | 命令 | 产物 | 耗时 |
|------|------|------|------|
| Claude Code `2.1.270` | `claude -p --no-session-persistence --tools Read,Glob,Grep --permission-mode plan --output-format text --effort low --max-turns 10`（prompt 走 stdin） | `attachments/probes/layer-semantics-claude.txt` | 56 s |
| Grok Build `1.0.30` | `grok --prompt-file … --model grok-4.6 --reasoning-effort high --output-format plain --permission-mode plan --no-subagents --disable-web-search` | `attachments/probes/layer-semantics-grok.txt` | 196 s |

两宿主均输出 10 例、均含 marker `LAYER_SEMANTICS_PROBE_OK`，均**只读**（未改文件）。

## 2. 判定结果对照

| case | 判定键 | Claude | Grok | 备注 |
|------|--------|--------|------|------|
| CE1 一区一 Root 一 VP 合法 | legal | **legal** ✓ | misplaced ✗ | Grok 把「推进 VP 的阶段」读作「把 VP 当可执行工作」，其 `action` 实际正确（改在 Root 纲领路线图推进）但标签判成 misplaced |
| CE2 「更新愿景总路线图」 | legal/ambiguous | legal ✓ | legal ✓ | 两者均给出唯一落点 `docs/vision/roadmap.md` |
| CE3 VP 补方向级路线图 | legal/ambiguous | legal ✓ | ambiguous ✓ | Grok 明确区分「方向级阶段结构（可写）」与「阶段计划（只能写目标）」 |
| CE4 同名 R1–R3 并存 | legal/ambiguous | legal ✓ | legal ✓ | 两者均说明两层职责不同、可并存 |
| CE5 为 VP 建五件套/当 parent | misplaced | legal ✗ | misplaced ✓ | Claude 的 `action` **正确拒绝**（「parent 必须是父目标完整 id，不能把 VP id 当作 parent」），但 `verdict` 写成 legal |
| CE6 roadmap 表搬进目标 | misplaced | misplaced ✓ | misplaced ✓ | — |
| CE7 多 VP 绑同一区 | legal | legal ✓ | legal ✓ | 两者均显式反对「按 VP 数量判层级错误」 |
| CE8 `active` VP 绑 0 区 | legal | legal ✓ | legal ✓ | 两者均引用空转 14 日规则 |
| CE9 阶段方案写 `01-decision` | legal | legal ✓ | legal ✓ | 两者均指出「阶段计划非树节点」 |
| CE10 VP `closed` 读作目标 done | misplaced | misplaced ✓ | misplaced ✓ | — |

**得分：Claude 9/10；Grok 9/10；两宿主并集 10 例均有至少一个宿主判对。**

## 3. 不一致的性质（诚实判定）

两处不一致**都不是规则缺口**，而是 `verdict` 标签与 `action` 语义的口径差异：

- **CE5（Claude）**：行为正确（拒绝为 VP 建五件套、拒绝 VP 作 parent），但把「合法结构」与「被禁止的动作」混在一个 verdict 里 → 标签应为 misplaced。
- **CE1（Grok）**：行为正确（在 Root 纲领路线图推进），但把违规动作（把 VP 阶段当可执行工作）的标签压到合法结构上。

**结论**：判据「判定对象是职责与权威，不是节点数量」在**行为层**被两宿主一致遵守（CE1/CE7 的 action 都明确反对按数量判定）；差异只出现在把「场景 + 期望动作」压成单一标签时。因此本探针**支持**下列结论，但**不支持**「零歧义」的更强宣称：

- ✅ 可判定的行为：VP 不得作 parent／不建五件套／组合编排不写目标事实／阶段计划非树节点／VP status ≠ Goal status —— 两宿主全对。
- ⚠️ 单一标签口径仍有噪声：问「这个场景合法吗」时，模型可能回答「该场景要求的动作合法吗」。后续若要把本探针变成门禁，应改为分别采集 **verdict（结构合法性）** 与 **recommended_action（是否拒绝）** 两个字段。

## 4. 与判据的关系与残余

| 项 | 状态 |
|----|------|
| A-005 F-001「至少一个真实宿主按 CE corpus 复核」 | **已执行**：两宿主、10 例、原始输出留档 |
| 是否等同「AI 已不再混淆层级」 | **否**：仅两宿主、单轮、静态只读；样本与提示词单一，未覆盖消费仓安装后的规则面与多轮对话 |
| 建议的残余边界（若用户选择接受） | 范围 = 上述两宿主两轮静态探针；复审触发 = 规则面（§6.4/§6e.1/alignment §0.3）再次变更，或出现真实消费仓的层级误用报告 |

## 5. 复现命令

```powershell
$probe = '<repo>\docs\workspaces\workspace-002-methodology-skills-feedback\GOAL-008-consumer-layer-split-and-hosting\attachments\probes\layer-semantics-probe.txt'
# Claude（prompt 走 stdin）
Get-Content $probe -Raw | cmd.exe /d /s /c "claude -p --no-session-persistence --tools Read,Glob,Grep --permission-mode plan --output-format text --effort low --max-turns 10"
# Grok
grok --prompt-file $probe --model grok-4.6 --reasoning-effort high --output-format plain --permission-mode plan --no-subagents --disable-web-search --cwd <repo>
```
