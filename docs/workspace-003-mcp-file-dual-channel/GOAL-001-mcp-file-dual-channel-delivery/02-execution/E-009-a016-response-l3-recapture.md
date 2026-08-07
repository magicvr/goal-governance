---
id: E-009
goal: GOAL-001-mcp-file-dual-channel-delivery
doc: execution
title: 响应 A-016：F-001 关闭证据重捕获（四宿主 L3 全 pass，绑定当前树）
status: recorded
created: 2026-08-07
updated: 2026-08-07
version: 0.1.0
---

# E-009 · A-016 响应：L3 重捕获执行事实（2026-08-07）

## 事实

用户 `/govern` 指令：「响应 Root A-016（independent conditional）：F-002/F-003/F-004/F-005/F-007 维持 fixed；F-001 关闭证据过期（server.py 哈希演进），重新捕获检查」。

- 背景：A-016（independent，conditional）核验发现 A-014 重捕获后，A-015 修 F-004/F-005 再次改动 `mcp/server.py`（`c0af461e… → cd31cbde…`），四条 L3 证据 JSON `behaviorSources[server.py]` 与当前树不一致；无 required，F-001r（recommended · med）。
- 本轮执行 **F-001 选项 A（重新捕获）**：以 `scripts/capture_runtime_evidence.py` 驱动**四宿主并行重跑**，同一探针 prompt（四条 prompt 文件哈希未变：`a423385d…`/`5d98a018…`/`107ebc4b…`/`fe57e7b7…`）与同一宿主 CLI 版本（claude 2.1.223 / grok 1.0.0 / codex 0.146.1 / copilot 1.0.75）。
- 结果（capture 内建 schema 校验 + 本编排器复核）：

| 宿主 | capturedAt（UTC） | 耗时 | verdict | server.py 哈希 |
|------|-------------------|------|---------|----------------|
| claude-code-cli | 2026-08-07T16:00:51Z | 76s | pass（exit 0，marker observed） | `cd31cbde…` |
| grok-build-cli | 2026-08-07T15:59:54Z | 19s | pass（exit 0，marker observed） | `cd31cbde…` |
| codex-cli | 2026-08-07T16:01:10Z | 95s | pass（exit 0，marker observed） | `cd31cbde…` |
| github-copilot-cli | 2026-08-07T16:00:37Z | 63s | pass（exit 0，marker observed） | `cd31cbde…` |

- 哈希对照：`entries.py ab183e15…`、`kernel.py b0168b2e…` 与既往一致（未变）；**`server.py cd31cbde…` = 当前树**（F-004/F-005 修复后哈希，A-016 报告值）。四条 JSON 的 `behaviorSources` 现与当前树**逐字一致**，Root `00-meta` 宿主表备注「behaviorSources 哈希与当前树一致」恢复字面成立（未改 meta 正文）。
- 证据文件原地刷新：`GOAL-002/attachments/runtime/evidence/{claude,grok,codex,copilot}-l3-four-entry-2026-08-07.json` + 对应 `.d/stdout.txt`、`.d/stderr.txt`。
- `GOAL-002/attachments/runtime/README.md`「捕获点与重捕获」节补记第三次捕获点（A-015 后 server.py 哈希演进 → 本轮重捕获绑定当前树）。

## 验证

| 动作 | 结果 |
|------|------|
| 四宿主 L3 重捕获 | 全 pass（见上表）；capture 内建 schema 校验通过 |
| 重捕获后 `behaviorSources` vs 当前树哈希 | 3/3 一致（entries/kernel/server），4 prompt 输入哈希不变 |
| 全量测试（上一轮 A-016 已验） | 210 passed（本轮未改代码，无新增测试面） |
| stage 镜像 | 本轮未改 canonical 白名单，无需 stage；上一轮 `--check` 36 对 0 漂移 |

## Checkpoint

- 提交 hash 见本轮 commit 记录；owned paths = 四个 L3 JSON + 四个 `.d/` 证据目录、GOAL-002 runtime README、GOAL-001 03-audit A-017 + 索引 + `02-execution.md` 索引 + 本执行记录。未用 `git add -A`。

## 下一步（待用户）

1. F-001r 关闭证据已补齐（A-017 响应登记）；F-001～F-005、F-007 全部维持 fixed。
2. F-006 归 VP-002 消费面；F-008 / I-007 于首次真实 `v*` GHCR 发布验收时关闭（均不变）。
3. 可选：A-016 建议的「capture/CI 增加 L3 证据哈希一致性检查」（防再犯）待用户决定是否立项。
