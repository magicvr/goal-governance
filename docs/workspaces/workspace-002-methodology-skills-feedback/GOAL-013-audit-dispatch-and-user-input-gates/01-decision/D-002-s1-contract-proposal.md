---
id: D-002
goal: GOAL-013-audit-dispatch-and-user-input-gates
doc: decision
title: S1 命令派发与缺答等待契约提案
status: accepted
parent: GOAL-013-audit-dispatch-and-user-input-gates
created: 2026-10-16
updated: 2026-10-16
version: 0.2.0
---

# D-002 · S1 契约提案（路径 A 已采纳）

## 依据与当前状态

用户本轮明确授权开展 S1。调查证据见 [S1 核对](../attachments/s1-contract-and-host-evidence.md)，后续用例见 [验收矩阵](../attachments/s1-acceptance-cases.md)。以下保留提交裁决时的提案及选项；用户随后通过同步卡片选择路径 A 和 Grok Build，正式采纳及保证边界见 [D-003](D-003-s1-freeze-and-grok-provider.md)。尚未修改规范或实现。

## 共同契约建议

1. **自动派发正文**只允许单行 `/audit NNN NNN` 或 `/vision-audit NNN`；编排器输出三位正整数编号，如 `/audit 002 013`。入口可接收 1～3 位十进制正整数并补零；0、超过三位、负数、小数、指数、未替换占位、额外 token/换行/注释均拒绝。不得先删去非法附言再发送。
2. **解析**：先用治理根协议定位 canonical workspace 声明，按数字选中唯一工作区，再核对 workspace.id/canonical_scope/Root、目标目录与 meta.id、tree；VP 按 plans/ 内唯一编号文件核对文件名与 frontmatter id。数字只是入口选择器，解析后的真实身份仍是完整 ID，不改变 Q1/Q2/Q3 或 parent。只枚举其他区的声明定位，不读取其目标正文；歧义、缺失、逃逸或旧/混合布局立即停止。
3. **独立范围**：只传标识，不传审计阶段、文件清单、已知 finding 提示或预期结论。由审计员自行读完整目标台账/VP 与适用权威，确定范围与所需证据；不得因编排器当前焦点而禁止审计员提出其他相关问题。
4. **上下文**：使用干净独立会话/子代理上下文，不 fork 编排器历史。模型、仓库 cwd 和供应商标识可以是调用配置；任何 description/system/context/附件/stdin 不得夹带编排器自编审计指令。标准已安装 skill/prompt 是审计入口自身的方法论，不是编排器为本次生成的提示。供应商不能识别/加载正式入口时停止，不靠自编提示补齐。
5. **人类直调与 MCP**：本需求限定编排器自动派发；不推定用户禁止人类直接表达 scope。自动路径不能伪装人类直调。MCP 现有 task/scope 参数不是白名单豁免；task 若承载自动派发，语义正文同样只能为合法命令，goal_id 等身份元数据必须与解析结果一致，不能以可选 scope/guidance 增加审计限制。是否增加代码校验由下方路径选择决定。
6. **询问发起**：当前宿主有可用且允许用于该问题的同步卡片则用卡片；没有时用文本提问并停止。给 2～3 个互斥可执行选项、推荐与取舍，保留客户端自由输入。异步工具不充当同步卡片；headless 无真人答复通路时停止，不伪造 stdin 或后台“代答”。
7. **答复核验**：将问题编号、原题、选项、影响范围与真实提交逐项对应。空结果、取消、超时、只展示成功、默认预选未提交、缺问题或答非所问均保持未答；部分答复不解除其余问题。不可凭工具成功/批准执行权限/模型叙述代替用户答复。
8. **持久阻塞**：发出待答请求并暂停时，记录问题与恢复条件；对当前可治理 active/draft Goal 置 blocked，在执行 ledger 写事实并同步 goal-tree 树/表/父级索引。保留已有阻塞原因。无 Goal 仅暂停当前任务；独立审计只返回待答事实，由编排侧处理状态；已 done/cancelled 的 Goal 不自动 reopen；VP 不使用 Goal 的 blocked。
9. **等待与恢复**：无真实答复时不实施、不放行、不关门、不编造裁决；允许的后续动作仅是记录待答/阻塞、报告问题、停止。真实答复到达后核对原问题并留痕，复查全部信息/审计门禁与其他阻塞；只解除被本答复解决的原因。写盘失败仍停止，明确未持久成功。
10. **宿主保证**：能力矩阵是设计依据；未知返回值统一按“没有可核对答复则未答”保守处理。真实版本 UI 的取消/恢复证据仍在 S3 验证，不用 S1 静态调查宣称已实现或宿主行为已验证；不能以采纳提案替代 I-004 验收证据。

## 互斥实施路径（原提案，A 已选）

| 方案 | 动作与产物 | 主要取舍与风险 |
|------|------------|----------------|
| A · 现有入口规范化（AI 推荐） | 将共同契约落到 canonical P-003/P-004/P-005 与 workspace/vision 适用规则，更新 00/03/05/06/07、四宿主包装与安装规则模板；MCP 保持现有参数兼容，补入口 guidance/消费说明；补静态契约、适用回归和实际宿主用例 | 符合当前 Skills 架构，改动边界较小；File 路径主要由 agent 遵守规范，不能宣称拥有系统级强制拦截 |
| B · 现有入口 + 代码强制校验路径 | A 的规则要求全部保留；另设计统一纯解析/校验模块及自动派发接口，在适用 MCP/CLI 路径拒绝非白名单载荷；自动调用统一经此路径，并新增安装/兼容/绕过测试 | 可在受控路径强制校验；新增 API、分发与兼容范围，需先补设计；仍不能拦截绕过该接口的任意宿主调用，不承诺全平台强制 |

推荐 A：用户提出的是编排与治理规则问题；仓库当前没有供应商 runner，新造 runner 不必作为规则修正的前置。若用户需要代码强制校验，则选 B 并先补 S1 对接口与分发的设计，不直接进入 S2。

## 预计写集与验证（尚未实施）

- canonical：`docs/architecture/principles.md`；按精确规则落位修改 `workspace-protocol.md` 与 `docs/vision/alignment.md`（不改 Charter/VP 意图）。根 AGENTS 与可分发规则模板同步摘要。
- Skills：00/03/05/06/07 prompts，必要的 02/04 记录边界；`skills/install/{claude,grok,codex}/skills/{govern,audit,vision,vision-audit}/SKILL.md` 与 Copilot 四 prompt；`skills/AGENTS.template.md` 及安装用规则正文。`.agents/` 等实际已安装面先确认同步机制，禁止手改镜像替代上游。
- MCP：`mcp/entries.py`、`mcp/README.md`（A 只同步语义 guidance，不破坏 schema）；B 才另列解析/接口代码写集并评估 `mcp/server.py`、`mcp/kernel.py` 等兼容面。
- 测试：`skills/tests/test_skills_orchestrator.py`、`docs/tests/test_file_l1.py`、必要的 `skills/tests/test_mcp_l1.py` 和 `docs/tests/test_dual_channel_l2.py`；B 补解析与拒绝路径行为测试。测试不能仅断言新增句子存在。
- stage 白名单变更后运行生成与 --check，镜像一并提交；S3 对受影响 behaviorSources 重新取证，问答证据与现有 dispatch marker 分开。不发 tag/Release。

## 审计与暂停（提交裁决时的上下文）

模式 cross 已由风险唯一确定；provider 本会话尚未指定。建议 Codex 独立子代理（干净上下文，仅命令输入）；也可由用户指定 Grok Build 或 Claude Code。provider 失败保持门禁，不替换为 self。

待用户裁决：Q-001 采用 A 或 B（亦可自由输入修改契约）；Q-002 指定 independent provider。S1 保持进行中、0/4，提案未冻结；目标在发出裁决请求后 blocked，等待真实用户回复。若卡片空返回，仍保持该状态，不重复计阻塞、不虚构选择。

## 裁决响应

实际答复已由 D-003 留痕：Q-001 = A，Q-002 = Grok Build。上段是发问时的历史事实，当前待答已解除、S1 已完成；不改写原选项或伪造此前已知答案。
