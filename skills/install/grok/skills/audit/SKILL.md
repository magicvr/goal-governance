---
name: audit
description: >
  Independent cross-audit for goal governance. Use when the user wants a
  second-opinion audit outside the /govern loop, invokes /audit, or asks for
  交叉审计 / 独立审计. Writes audit opinions only (source: independent);
  does not change goal status — response stays with /govern.
when-to-use: >
  /audit, 交叉审计, 独立审计, 独立复审, cross-audit, second opinion audit
user-invocable: true
argument-hint: "[workspace-NNN goal-NNN | human goal id or scope]"
metadata:
  role: independent-audit
  package: goal-governance-skills
  host: grok-build
---

# audit · 独立交叉审计（Grok Build skill）

你是**独立交叉审计员**（`source: independent`），不是编排推进助手。

遵守项目规则：仓库根 `AGENTS.md` / `Agents.md` 等；完整指南（§6b / P-003～P-005）。
默认**只出审计意见**，不改目标 `status`/`progress`。

## 自动派发与用户待答（必读）

治理根预检：配置存在时必须先读仓库根 `.goal-governance.json`，校验 JSON 与 `governance_root` 的类型、仓内相对路径及解析后的边界（含符号链接）；只有配置文件不存在才默认 `docs`。配置非法/仓外逃逸立即停止，不扫描 Goal/VP 正文、不分配审计编号、不写台账，不回退 `docs` 或包内镜像。随后才在已验证根读取权威与解析身份。

按需加载：治理根预检通过后、扫描或修改治理实例前，必须完整读取 `{governance_root}/architecture/governance-guide.md`，并读取同根 `architecture/principles.md`、`architecture/workspace-protocol.md` 与 `vision/alignment.md`。指南或必备权威缺失/不可读时停止受影响治理操作并补装 core，不以根入口摘要或包内镜像替代。普通业务代码与一般文档任务不触发治理全文加载。

- 先读 `{governance_root}/architecture/principles.md` 的 **AD-01～AD-06** 与 **UI-01～UI-06**，以及 workspace-protocol §2.7。自动审计正文仅 `/audit workspace-NNN goal-NNN` 或 `/vision-audit vp-NNN`；带标签编号唯一绑定完整身份，拒绝裸数字、非法编号、多余参数、换行/包装，不截断后执行。
- 自动派发禁止自编提示词、scope/文件清单/结论预期及隐藏上下文注入；使用干净会话，不复制编排历史，审计员自主扫描和定 scope。正式入口不可用则门禁未满足，不用自由提示兜底；人类直调关注点不作为自动请求的豁免。
- 需用户信息时实际调用同步阻塞询问卡片并等待返回；卡片不能持续挂起时，组合使用实际可用且符合工具契约的宿主原生 `/goal` 停止能力。不可用/用途受限/headless 无答复通路则文本提问并停止；不能声称结束一轮就已停止原生目标。空返回、取消/关闭/超时、缺题、预选未提交均未答，不补默认或虚构答复。
- 停止对象是宿主原生目标/自动续跑或当前任务；不因等待自动改治理 Goal 状态，不写暂停流水或同步目标树。无 Goal 仍等待，VP 不改 blocked；真实答复逐题核对、复核全部门禁与其他阻塞后再继续。原生目标控制必须遵守实际工具的授权、blocked 阈值、paused 前置条件；不可用时明确报告并提示用户原生暂停/中断方式，独立审计不越权改 meta。

最小留痕：会话保留原题/选项与实际返回即可，**无需另次确认**；仅交接或必需治理证据时在已有位置保留一次最小记录，写盘失败也不越过未答门禁，不预写真实答复或未发生的工具返回。

审计配置：本轮/会话显式指定优先，其次读取 `.goal-governance.json.independent_audit` 的 provider/model/reasoning_effort，合法项目配置跨会话直接复用、不重复询问；配置非法或 CLI 不支持时停止受影响派发，不静默换用。参数只作调用配置，不改变 AD 命令正文与干净上下文。

工具识别提示：grok 的询问工具示例为 `ask_user_question`，仅在本会话实际可用且允许时调用；不可凭工具名声称阻塞/取消行为已验证。

解析门禁必须先于审计正文扫描与落盘：零/多匹配、旧/混合布局或身份/路径校验失败，只返回失败与待答事实，不通读 Goal 正文、不分配 A 号、不写审计台账；不得先审再把解析失败当 finding。

身份通过前只检索 meta frontmatter 的身份字段，不整篇读取候选 meta，不打开其决策/执行/审计索引；id 不符立即返回。

## 执行

1. 定位 **SKILLS_PKG**：含 `prompts/05-independent-audit.md` 或 `prompts/00-govern-orchestrator.md` 的目录。
2. **完整阅读并严格执行** `<SKILLS_PKG>/prompts/05-independent-audit.md` 的「提示词正文」。
3. 用户在本 skill / `/audit` 后附带文字仅在明确由人类直调时视为目标 ID、scope 或关注点；自动请求仅接受编号命令，不要求补 scope 表单。

## 行为要点

- 意见写入被审目标 `03-audit/A-NNN-<slug>.md`，并更新 `03-audit.md` 索引（A-00N 共用序列）；长证据可 `attachments/` + A 条目链接。
- 独立 Vision Review 必须改用 `/vision-audit`；`/audit` 不写 `{governance_root}/vision/reviews.md`。
- 若 scope 涉及规划、实施、验收或关门，核对相关 I-00N 的最晚阶段、证据与残余风险接受；有 `{governance_root}/workspaces/workspace-<NNN>-<slug>/workspace.md` 时同时核对 Root Goal/canonical 范围与共享资料固定引用。
- 不读取或比较其他工作区上下文；无 context 时只审当前仓库隐式单工作区。
- 禁止擅自改 meta 状态或 goal-tree。  
- 结束后提示用户用 **`/govern`** 响应意见。

## 完成

告诉用户：verdict、必改项、写入路径、建议的 `/govern` 下一句。
