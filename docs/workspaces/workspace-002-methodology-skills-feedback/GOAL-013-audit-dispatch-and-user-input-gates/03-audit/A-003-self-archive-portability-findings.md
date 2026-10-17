---
id: A-003
goal: GOAL-013-audit-dispatch-and-user-input-gates
doc: audit-entry
source: self
auditor: Codex orchestrator
scope: Windows Git checkout portability of archived S3 evidence
verdict: conditional
status: recorded
parent: GOAL-013-audit-dispatch-and-user-input-gates
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# A-003 · 原始证据检出可移植性补充自审

- source：self
- scope：e37cad3 的原始 JSONL 证据在 Windows Git 检出时的字节保持，以及深层原始快照路径的检出配置；不是否定 A-002 的当前 envelope 内容/来源检查
- verdict：conditional

## F-001 · JSONL 未固定 LF，重新检出会改变已记录摘要

- 严重度：med
- 建议：required
- 状态：open
- 证据：当前仓 core.autocrlf=true；对 claude-wait-readonly-fault-current/stdout.jsonl 实际执行 git cat-file --filters，当前/记录摘要为 107d4a8290940b0e8f8cd68d9d4c22570d6908cea91a8ebe14ae643be4a78c80，检出过滤后为 09d5e9d5e17d24d4cb979dcce555c7815b7fb23c88fa0d3c758c02f205f5393d，LF 被改为 53 个 CRLF。现有 .gitattributes 固定 json/txt 等，但未固定这些 jsonl。
- 复现：临时 Git 仓 core.autocrlf=true，复制当前 attributes，写合成 JSONL 后提交、移除工作文件、checkout；实际字节/SHA 不一致，回归测试红。未改写真实证据。
- 影响：原始 observation 的 stdoutSha256 在重新检出后可能不可核对；当前工作树与 16 份 envelope 校验仍通过，不把未来检出缺陷写成当前 envelope 已失败。
- 关闭要求：对本目标归档 JSONL 固定 LF；真实 Git checkout 回归通过，原记录 SHA 保持，不重算历史 SHA 兜底。

## F-002 · 深层原始快照需要 Windows Git 长路径配置

- 严重度：low
- 建议：recommended
- 状态：open
- 证据：已提交路径最长相对 276 字符、当前绝对 324 字符；未启用长路径时，Git status 曾误报深层文件删除，E-010 记录本地 core.longpaths=true 后消失。Windows CI checkout 前尚无显式配置。
- 建议：Windows CI 在 checkout 前启用 Git 长路径；维护说明记录生产仓 clone/已有仓要求，不将其扩成普通消费安装门禁。

## 必改项与下一步

F-001 未闭合前不完成 S4/关门。两项均存在明确、可逆、保持原证据的 fixed 路径；按本轮 S4 修正授权执行，不需要 residual/overruled。新发现的归档范围区别于 A-001/A-002 已审的规范与当前运行内容，不构成 verdict 相反或必改项要否冲突。
