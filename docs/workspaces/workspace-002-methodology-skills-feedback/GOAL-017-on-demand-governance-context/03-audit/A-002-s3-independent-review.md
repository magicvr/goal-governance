---
id: GOAL-017-on-demand-governance-context
doc: audit-entry
record_id: A-002
source: independent
scope: S2 implementation facts and S3 evidence gate
verdict: conditional
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-11-03
updated: 2026-11-03
auditor: Grok Build CLI（Grok 4.7 / xhigh）
version: 0.1.0
---

# A-002 · S2 事实与 S3 证据门禁独立审计

## 范围与区间

- auditor: Grok Build CLI（Grok 4.7 / xhigh），正式命令 `/audit workspace-002 goal-017`
- type: stage（S3 交叉审计）；兼核 S2 已声称的实施事实
- 工作区: `workspace-002-methodology-skills-feedback`；目标 `GOAL-017-on-demand-governance-context`
- covered: D-003 加载契约是否落到消费入口与提示词；E-003 所引测试日志；信息项 I-001～I-004；A-001 F-001；落盘前已能打开的 `docs/releases/runtime/v0.14.0/` 信封与对应 `attachments/s3-runtime/` 转录
- excluded: S4 的 PR、tag、Release 与 GHCR（尚未开始）；其他工作区目标正文；把本意见自己的阅读过程当成矩阵证据
- 保证等级: L0。本意见不修改 status、检查点、progress 或 goal-tree

本目录在审计期间仍有新信封写入。下面的格子清单是落盘前最后一次清点，不是已冻结的证据集。

## 成果（有证据）

| 主张 | 证据 |
|------|------|
| 消费常驻入口在预算内 | `docs/templates/governance-entry.md` 与 `skills/AGENTS.template.md`、`skills/install/claude/AGENTS.md`、`skills/install/copilot/copilot-instructions.md` 同为 17 行、1391 UTF-8 bytes（CRLF）。LF 归一后为 1374 bytes，与 E-003 的 1374 一致。均低于 D-003 的 ≤40 行、≤4096 bytes |
| 治理提示词要求先读完整指南 | 分发面 28 个文件含同一「按需加载」句：`skills/prompts/00`～`07` 共 8 个，加上 Claude/Codex/Grok 各 4 个 skill 与 Copilot 8 个 prompt。另有 16 个 dogfood 副本（`.claude`、`.grok`、`.agents`、`.github` 各 4 个）含同一句 |
| S2 三份测试日志为 OK | `attachments/s2-skills-tests.txt`：Ran 103 tests，OK；`attachments/s2-docs-tests.txt`：Ran 76 tests，OK；`attachments/s2-migration-tests.txt`：Ran 50 tests，OK。本审计未重跑这些测试 |
| 一条普通任务转录未读治理权威 | `attachments/s3-runtime/claude-ordinary-ordinary-01/`：`changed` 为空；stdout 未出现 `governance-guide.md`、`principles.md`、`alignment.md`、`workspace-protocol.md` |
| 带 Bash 的 Claude audit 重试读了指南并打出标记 | `docs/releases/runtime/v0.14.0/claude-code-cli-audit-2026-11-03-r2.json`：`verdict=pass`，marker `A-001` observed。工具列表含 Bash。`claude-code-cli-audit-2026-11-03-r2.d/stdout.txt` 有对 `docs/architecture/governance-guide.md` 与 `principles.md` 的 Read |
| 已通过且本意见直接看到 verdict 的其他信封 | Claude govern、govern-r2、vision；Copilot govern、audit、vision、vision-audit；Grok govern、audit、vision；Codex MCP。均为 `verdict=pass` 且 marker observed。Grok govern 信封的 `behaviorSources` 与当前文件 LF 归一 SHA-256 一致 |
| 身份与对齐 | 唯一 `workspace-002`；`GOAL-017` 的 `id` 与目录名一致，`parent` 为本区 Root；Root `parent: null` 且 `primary_plan` 为 VP-002；VP-002 `vision_ref` 为 `vision-goal-governance@0.2.0`，与现行 Charter 一致。本目标未声明共享资料引用 |

## 对照成功标准

五条成功标准在 `00-meta.md` 中都未勾选，与「S4 未开始、S3 未退出」一致。

| 标准 | 本意见 |
|------|--------|
| 常驻块预算，且非治理任务不读全文 | 预算已核对。非治理不读全文只有一条 Claude 普通任务转录，尚未进入兼容矩阵 |
| 治理命令先加载完整规则；非法根则停止 | 静态提示词已要求加载。代表运行里仍有失败格，见 F-001 |
| 新装、升级、自定义根、用户字节保留 | E-003 将这类检查计入 50 项迁移测试；本意见只核对日志为 OK，未重跑 |
| canonical、入口、打包一致且 self + independent 无开放 required | 本意见与 A-001 都仍有开放 required |
| dev → main → tag → 发布资产验收 | 未开始，不在本 scope 的通过范围 |

## Findings

### F-001 · S3 代表运行证据尚未形成可接受集合

| 字段 | 值 |
|------|-----|
| level | required |
| 严重度 | med |
| status | open |
| 影响门禁 | S3 退出、S4 发布、目标关门。不阻断继续采集证据本身 |
| 关联 | I-003、I-004；A-001 F-001 仍开放，本条不关闭它 |

落盘前清点到的失败格：

- `docs/releases/runtime/v0.14.0/claude-code-cli-vision-audit-2026-11-03.json`：`verdict=fail`，marker `VRev-001` 未观察到。对应 `attachments/s3-runtime/claude-vision-audit-01/stdout.jsonl` 只读了 `.goal-governance.json` 和 `skills/prompts/07-independent-vision-review.md`，随后因工具列表没有路径解析能力（session tools 为 Edit/Glob/Grep/Read/Skill/Write，无 Bash）而停在符号链接边界预检，未读 `governance-guide.md`，也未写 VRev。
- `docs/releases/runtime/v0.14.0/claude-mcp-four-entry.json`：`verdict=fail`，marker `MCP_L3_FOUR_ENTRY_OK` 未观察到。`attachments/s3-runtime/claude-catalog-01/stdout.jsonl` 写明符号链接预检未完成，因此不输出成功标记。
- `docs/releases/runtime/v0.14.0/claude-code-cli-audit-2026-11-03.json`：同样因无 Bash 的预检而 `verdict=fail`，且 stdout 未出现四份权威文件名。同目录的 `-r2` 在加入 Bash 后 pass，并实际 Read 了指南与 principles。`-r2` 说明该入口可以被跑通；它不把第一份失败信封变成矩阵证据，也不填补其他失败格。

同时：

- `docs/contracts/skills-consumer-compatibility-matrix.json` 的 `candidateRevision` 仍是 `v0.13.8`，证据路径仍指向 `docs/releases/runtime/v0.13.8/`。
- 最后一次清点时，Grok `vision-audit` 信封、Copilot MCP 信封、Grok MCP 信封和 Codex 四个 CLI 入口信封都还不在 `v0.14.0/`。采集目录在本审计过程中仍在增加文件。
- `00-meta.md` 将 I-003 保持为 `open`，I-004 保持为 `collecting`。这与「证据未闭环」一致。

因此不能把 `v0.14.0/` 的部分 pass 当作 S3 退出证据，也不能把 I-003 标成 verified。

修正：等采集停止后冻结一份完整集合；对仍失败的 Claude vision-audit 与 Claude MCP 格，用能够完成符号链接边界检查的工具列表重抓，并保留指南被实际读取的转录。再用当前行为源更新矩阵与 host 版本，跑兼容/发布检查。通过之后才可由 `/govern` 按 fixed 路径处理 A-001 F-001 与本 F-001。

### F-002 · 台账投影与一项测试计数和所引日志不一致

| 字段 | 值 |
|------|-----|
| level | recommended |
| 严重度 | low |
| status | open |
| 影响门禁 | 不单独阻断 S3。会让后续编排读到过期的 0% 或「I-001 仍在收集」 |

- `00-meta.md`「当前阻塞」仍写 active / 0%、I-001 继续收集、S3/S4 证据未产生。同文件路线图与信息表已是 S2 完成、progress 50%、I-001 verified、S3 进行中。
- `02-execution.md` 索引末段仍写 progress 保持 0/4。E-003 已写 2/4。
- 本索引在 A-002 写入前写着 I-001 收集中，以及尚未到达阶段审计。
- Root `00-meta.md` 概述仍写本目标「尚未实施」。同区 `goal-tree.md` 表行已是 active / 50%。
- E-003 写 focused stage/pack/orchestrator 65 tests OK，并说日志在 `attachments/s2-*.txt`。这三份日志的计数是 103、76、50，没有 `Ran 65`。103/76/50 与日志一致。65 与「stage 43 对」本意见没有另寻到可核对日志，未重跑 `stage_skills_mirrors.py --check`。

## 必改项汇总

| ID | 级别 | 状态 | 要做什么 |
|----|------|------|----------|
| F-001 | required | open | 冻结完整的当前行为源运行证据，替换失败格，更新矩阵后再谈 S3 退出 |
| F-002 | recommended | open | 把 0%、I-001 收集中、Root「尚未实施」改成与路线图和 goal-tree 相同的事实；为 65 项测试补日志或改写表述 |

## 与既有意见的异同

A-001（self，conditional）的 F-001 认为运行证据与按需加载验证尚未取得，且不放行发布。本意见同意该门禁仍开放。补充的事实是：采集已经写出部分信封；其中 Claude vision-audit 与 Claude MCP 仍是 fail，原因是无路径解析工具时新的符号链接预检会停住且不读指南；Claude audit 的无 Bash 失败格之后有一份含 Bash 的 pass 重试。两边都是 conditional，没有 verdict 互否。A-001 F-001 不因本意见而闭合。

## 结论与下一步

S2 的入口预算、提示词接线和三份已附测试日志可以核对。S3 退出条件尚未满足。verdict 为 **conditional**。

建议 `/govern`：先按 F-001 把代表运行证据做成一套稳定、失败格已替换、矩阵已改到当前行为源的集合，再响应 A-001 与 A-002；F-002 可在同一次台账整理中改掉。不要用 progress 50% 或个别 pass 信封放行 S4。

## 声明

本意见不修改 status、检查点、派生 progress 或 goal-tree。响应与 finding 闭合由 `/govern` 处理。
