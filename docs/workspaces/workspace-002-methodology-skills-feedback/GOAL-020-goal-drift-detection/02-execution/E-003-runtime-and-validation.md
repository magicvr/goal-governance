---
id: E-003
goal: GOAL-020-goal-drift-detection
title: 实际宿主对照、16格证据和完整回归
doc: execution
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-16
updated: 2026-11-16
version: 0.1.0
---

# E-003 · S3验证事实

16份选用当前源码信封均pass：三宿主四入口12格、四宿主实际stdio+目录核对4份。`capture_runtime_evidence --check`一致，兼容矩阵candidateRevision v0.16.0、coverage ready；明细见 [选用清单](../attachments/s3-selected-runtime-evidence.json)。信封pass只证明入口/台账边界；漂移语义结果另见 [semantic-results.md](../attachments/semantic-results.md)。只读意见按P-003逐字代贴，保留来源、实际写入方和原始changed事实。

Skills113、docs76、scripts156通过（scripts4项按环境跳过）；完整 `release_evidence --mode rehearsal --run-checks` checksPassed=true。安装文档、候选测试和tag workflow已钉v0.16.0。新跨MCP测试不随纯File包分发，真实打包成员回归覆盖排除边界。

旧证据使早期scripts套件失败；487ed9a仅保存源码/初步证据，不作为已验证checkpoint或发布放行依据。此次重采后已消除该失败并跑通完整回归。失败/解析/未落盘的探针保留且未被计为成功。

归档处理删除provider私有reasoningText等字段，保留实际公开内容/工具事件，before/after摘要见s3-representation-processing.json；受影响信封增加处理器来源和说明，重新校验16份来源与输出摘要通过。不更改任何实际审计verdict。

指定Grok正式cross尚待返回；S3未退出，S4/发布未发生。Root/R3/VP不关门。
