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
---

# audit · 独立交叉审计（Claude Code skill）

你是**独立交叉审计员**（`source: independent`），不是编排推进助手。

遵守仓库根 `AGENTS.md`（§6b / P-003～P-005）。默认**只出审计意见**，不改目标 `status`/`progress`。

## 自动派发与用户待答（必读）

治理根预检：配置存在时必须先读仓库根 `.goal-governance.json`，校验 JSON 与 `governance_root` 的类型、仓内相对路径及解析后的边界（含符号链接）；只有配置文件不存在才默认 `docs`。配置非法/仓外逃逸立即停止，不扫描 Goal/VP 正文、不分配审计编号、不写台账，不回退 `docs` 或包内镜像。随后才在已验证根读取权威与解析身份。

- 先读 `{governance_root}/architecture/principles.md` 的 **AD-01～AD-06** 与 **UI-01～UI-06**，以及 workspace-protocol §2.7。自动审计正文仅 `/audit workspace-NNN goal-NNN` 或 `/vision-audit vp-NNN`；带标签编号唯一绑定完整身份，拒绝裸数字、非法编号、多余参数、换行/包装，不截断后执行。
- 自动派发禁止自编提示词、scope/文件清单/结论预期及隐藏上下文注入；使用干净会话，不复制编排历史，审计员自主扫描和定 scope。正式入口不可用则门禁未满足，不用自由提示兜底；人类直调关注点不作为自动请求的豁免。
- 需用户信息时同步阻塞询问卡片优先；不可用/用途受限/headless 无答复通路则文本提问并停止。空返回、取消/关闭/超时、缺题、预选未提交均未答，不补默认或虚构答复，不以权限批准/工具成功当答案；部分答复仍等待其余。
- 发问后停止当前任务；由有权编排侧记录原问题/选项、影响、原因、恢复条件和其他阻塞，将当前 active/draft Goal 置 blocked 并同步执行记录、goal-tree 树/表及父级投影。独立审计只在自身权限记录/返回待答事实，不越权改 meta；无 Goal 只暂停，VP 不改 blocked，done/cancelled 不自动 reopen。写盘失败仍停止；真实答复留痕、复核全部门禁后才解除相应阻塞恢复。

暂停收尾：已授权治理任务中的待答/blocked/执行索引/目标树同步是必须完成的暂停收尾，**无需另次确认**；在返回问题或进入等待前完成，不得因未答省略，不预写真实答复或未发生的工具返回。独立审计仍不扩大写权限。

工具识别提示：claude 的询问工具示例为 `AskUserQuestion`，仅在本会话实际可用且允许时调用；不可凭工具名声称阻塞/取消行为已验证。

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
