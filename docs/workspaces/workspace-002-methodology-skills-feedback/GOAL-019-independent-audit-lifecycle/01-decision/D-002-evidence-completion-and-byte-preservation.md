---
id: GOAL-019-independent-audit-lifecycle
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-13
updated: 2026-11-13
version: 0.1.0
---

# D-002 · 审计补录与运行快照字节保真

本目标的真实取证发现两个实验判定缺口：被否定/引用的标记也会命中子串断言，报告与索引文件存在也不能证明元数据和审计员署名正确。最终选用前增加实际正文核对；原始错误信封不重写为通过，保留并明确弃选。目录角色探针澄清本项的只读 guidance 核对范围，并要求实际助手消息中独立一行的正向标记；不以目录角色证据冒充四项生产执行。

Copilot直接审计夹具去掉可选的、与本次直接调用不一致的Grok派发默认，不改生产仓 `.goal-governance.json` 或正式Grok审计配置。用户指定的 `gpt-6-luna` 继续用于Copilot采集，自动审计正文仍严格只有正式命令，不追加scope或提示。

依P-003允许独立意见输出后由本侧代贴，实验可由编排侧仅补缺失的最低frontmatter；独立正文、verdict与findings不改，保存前后摘要、原文不变证明和补录事实，不宣称宿主原生格式已通过。若本次原生报告已有frontmatter，则不补录。attempt11暴露补录器只识别LF、误给已有CRLF frontmatter的报告再加头的问题；弃选该中间尝试，最终补录器按规范化换行判断是否已有frontmatter，旧源和旧信封保留。

扩展owned paths纳入根 `.gitattributes` 的本目标专属证据路径：JSONL固定LF；host生成的 `attachments/s3-runtime/**/changed/**/*.md` 原始快照禁用Git文本换行转换，并只对这些不可变快照保留原生硬换行/末尾空行。原因是其字节摘要及独立原文保真不能在Windows暂存或跨平台checkout时被改写。canonical文档的LF与空白检查不放宽。该操作是已有运行证据与发布验收范围内的保真措施。
