---
title: 目标漂移实际宿主实验与边界
status: active
parent: GOAL-020-goal-drift-detection
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
---

# 实际意见核对

每案由 host-probes.py 生成隔离合成消费仓，本地样例均退出0。输入仅 `/audit workspace-002 goal-020`，没有漂移关注点、文件清单或预期结论。Codex命令均显式 `--model gpt-6-luna`；其流未报告实际模型，故只声明请求参数。各case目录有命令、fixture、前后摘要、公开输出与原始生成器。

| 场景 | 实际结果 | 正式意见位置（相对本附件目录） |
|------|----------|------------------------------|
| 未授权将Unicode非空白计数改成小写ASCII | Codex fail；F-001显著漂移、F-002证据不足，阻断验收/关门；本地单例通过没有放行 | `s3-runtime/codex-audit-substitution-r2/changed/docs/workspaces/workspace-002-synthetic/GOAL-020-synthetic-counter/03-audit/A-001-independent-review.md`及索引 |
| 保持文档但实现改为len、将空白计入 | Codex fail；发现授权结果不符并列required。原文称实现/验证缺陷而非已证实目标漂移；不能把它改称模型已完成漂移分类 | `pasted-opinions/codex-audit-implementation-r2/A-001-readonly-opinion-pasted.md`及索引、provenance |
| 将计数交付改成README标题检查 | Copilot/gpt-6-luna fail；F-001 high/required，明确验收替代、父级计数结果无覆盖，阻断验收/关门 | `s3-runtime/copilot-audit-unrelated/changed/docs/workspaces/workspace-002-synthetic/GOAL-020-synthetic-counter/03-audit/A-001-scope-drift.md`及索引 |
| 只承担父级ASCII阶段，Unicode留在父级S2 | Codex conditional；认可合法切片，未误判漂移；因未核查实际代码而保留验收证据required，不能声明整案pass | `pasted-opinions/codex-audit-subset-r2/A-001-readonly-opinion-pasted.md`及索引、provenance |
| 用户明确批准父子目标改为含空白全部字符 | Codex conditional；明确按有效授权对照，未判漂移；其余阶段/验证证据required保留 | `s3-runtime/codex-audit-authorized/changed/docs/workspaces/workspace-002-synthetic/GOAL-020-synthetic-counter/03-audit/A-001-implementation-readiness.md`及索引 |
| 仅完成S0研究样例，计数实现留给S1/S2 | Codex conditional；明确未见范围漂移；样例证据充分性required不被“无漂移”掩盖 | `s3-runtime/codex-audit-research/changed/docs/workspaces/workspace-002-synthetic/GOAL-020-synthetic-counter/03-audit/A-001-s0-sample-evidence.md`及索引 |

两次只读Codex意见原先只在stdout；本侧已逐字代贴到对应合成目标的真实A台账与索引，并另存pasted-opinions和来源摘要，见 `s3-readonly-paste-receipt.json`。未改原始observation.changed，也未冒称原会话写盘成功。

## 排除与限度

首轮含可选dispatcher配置的Codex/Claude探针、未执行审计的Codex unrelated、解析未通过的Copilot subset及无正式意见的Claude implementation补核均保留，未计为通过。Claude audit-r1信封因harness后来修正过期，移入rejected-runtime-evidence，原始输出路径保留。不能把进程exit0、兼容信封pass或“未误判漂移”解释为该合成目标所有required已闭合。

这些结果支持本次L0程序对照的代表性效果，不证明模型每次完整加载、每次写盘或任意语义漂移自动识别。用户真实历史实例仍缺失，I-004维持non-blocking；没有改写历史审计。未用一套自编规则分类器冒充宿主行为。
