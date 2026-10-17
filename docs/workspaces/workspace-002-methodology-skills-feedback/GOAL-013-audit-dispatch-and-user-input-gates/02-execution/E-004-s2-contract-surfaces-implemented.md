---
id: E-004
goal: GOAL-013-audit-dispatch-and-user-input-gates
doc: execution
title: S2 核心规则与四宿主消费面修正完成
status: active
parent: GOAL-013-audit-dispatch-and-user-input-gates
created: 2026-10-16
updated: 2026-10-16
version: 0.1.0
---

# E-004 · S2 规则与消费面修正

## 授权与门禁

用户输入：`/govern 工作区2 GOAL-013，按 D-003 开展 S2`。执行已冻结路径 A，provider 为 Grok Build；S1 设计/裁决信息 verified，正式审计索引无 A 条目、无已登记开放 required finding 阻止本次实施。I-004 仍在 S3 退出前阻断运行时验收，不将它伪造为已闭合。

## 已完成实现

| 写集 | 具体事实 |
|------|----------|
| canonical | 先在 `docs/architecture/principles.md` 增加稳定锚点 audit-dispatch / user-input-wait，AD-01～AD-06 与 UI-01～UI-06；workspace-protocol §2.7 明确数字选择器与完整身份唯一绑定，alignment §9.3 落愿景侧边界 |
| 核心 prompts | 00/06 编排入口加入自动命令派发与同步询问/缺答/恢复；05/07 独立入口明确命令解析、自动请求不填 scope 表、审计员自主定 scope；02/03/04 明确真实决定、blocked 事实与审计角色权限 |
| 安装规则与入口 | 更新根 AGENTS、三份可分发规则摘要及本仓 Copilot 摘要；四宿主共 16 份发货 wrapper 与 16 份本仓对应副本同步。自动附言不能伪装人类直调，询问工具名仅作为实际可用时的提示 |
| 模板与镜像 | 执行模板增加待答问题/选项/门禁/原因/方式/其他阻塞/恢复条件/真实答复来源表。执行 stage，38 对中复制 4 对，--check 通过；没有手改镜像或新增 producer 状态源 |
| MCP | 仅扩展现有 role/guidance 与说明；薄消费方无 File prompts 时也得到约束。参数字段/类型/required、只读角色与状态写入边界保持；没有新增 provider runner 或命令拦截器 |
| 文档与防漂移 | docs/README 将历史 release runtime-verified 与当前修改区分，明确 12 份证据过期。新增 8 项跨分发/本仓副本/参数兼容/薄 MCP 无写盘/模板字段契约检查，不模拟不存在的 agent 状态机 |

详细源文件版本见 [S2 源清单](../attachments/s2-source-manifest-2026-10-16.json)，验证摘要见 [S2 验证记录](../attachments/s2-validation-2026-10-16.json)。S1 的源快照保持原样，不改历史哈希来掩盖本轮修改。

## 验证事实

| 检查 | 结果 |
|------|------|
| 文档全套 unittest | 67 tests，OK；首次沙箱下两项临时 git init 因 .git/config 写权限失败，所需权限重跑后全部通过 |
| Skills 全套 unittest | 101 tests，OK，含新增 8 项；既有 subprocess ResourceWarning 不影响退出码 |
| stage / delivery-channel 契约 | 11 tests，OK |
| 打包回归 | 10 tests，OK（1 skipped）；不把打包测试当正式发布 |
| PowerShell 隔离安装 | PASS；在隔离临时目录实际生成四宿主入口、core 与 workspace scaffold，不覆盖当前用户仓规则 |
| stage 镜像 | 38 对一致，4 对刷新；无孤儿清理动作 |
| 旧 runtime evidence 一致性 | **exit 1：12 份记录、24 个 behavior source stale 问题**，均涉及 AGENTS 与 00 prompt；原记录未改，保留 S3 必须重取证门禁 |

本仓 `.agents/skills/` 先被只读沙箱拒绝写入；仅四份已准备的 Codex wrapper 经 require_escalated 审核后同步成功，没有把第一次失败后的提示文字当作成功事实。其他源/安装面均在本次显式写集中。

收尾定向核对通过：本目标全部 Markdown frontmatter/相对链接/空白、S1+S2 的 2/4=50%、目标树与 Root 67% 一致、I-004 仍 open、56 个 S2 源/镜像文件哈希一致、原 runtime/contracts 未修改、无虚构 A 条目、暂存区为空；`git diff --check` 通过。

## 阶段与边界

S2 完成，S1/S2 为 2/4，派生 progress 50%；Goal 保持 active，Root R3 active / 67% 不变。成功标准前三项只按规范/入口交付勾选，不声称运行时命令已被系统强制拦截或四宿主 UI 行为通过；其余验收与 cross 审计仍未完成。

I-004 保持 open：12 格入口证据须按实际行为重取，22 条正反例中的当前版本卡片取消/空返回/恢复事实仍须 S3 验证；新的 marker 探针也不能代替问答证据。没有接受 residual、删除用例、降低门禁或由编排器冒充 independent；本轮未调用 Grok 审计、未进 S4、未发布。

## Git checkpoint

本轮 baseline 已包含 Root meta/goal-tree 的既有未提交改动与整个未跟踪 GOAL-013；沿用 §3.6 的保守 ownership 门禁，且当前 runtime producer 检查尚未满足，本轮不自动提交或宣称 checkpoint hash。canonical 与生成镜像均留在同一工作树变更集中，后续提交不得漏镜像；未暂存其他路径。

## 下一步（计划）

建议 `/govern 工作区2 GOAL-013，开展 S3`，按已冻结矩阵验证实际派发与问答边界、重取受影响 runtime 证据；本轮不把 S3 标成已开始。
