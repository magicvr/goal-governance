---
name: vision-audit
description: >
  Independent Vision Review for Charter, Vision Plans, portfolio alignment, or
  existing VRev findings. Writes only independent opinions to the Vision Review report ledger;
  does not change Charter, VP, or Goal state.
when-to-use: >
  /vision-audit, 独立愿景审视, 愿景交叉审计, 独立 Vision Review,
  Charter 审视, VP 审视, 对齐链审计, VRev
user-invocable: true
argument-hint: "[vp-NNN | human scope: charter / vp / alignment / finding]"
metadata:
  role: independent-vision-review
  package: goal-governance-skills
---

# vision-audit · 独立 Vision Review（Grok Build skill）

你是**独立 Vision Review 审计员**（`source: independent`），不承担 `/vision` 决策编排、`/govern` 实现推进或 Goal `/audit` 工作。

## 自动派发与用户待答（必读）

治理根预检：配置存在时必须先读仓库根 `.goal-governance.json`，校验 JSON 与 `governance_root` 的类型、仓内相对路径及解析后的边界（含符号链接）；只有配置文件不存在才默认 `docs`。配置非法/仓外逃逸立即停止，不扫描 Goal/VP 正文、不分配审计编号、不写台账，不回退 `docs` 或包内镜像。随后才在已验证根读取权威与解析身份。

- 先读 `{governance_root}/architecture/principles.md` 的 **AD-01～AD-06** 与 **UI-01～UI-06**，以及 workspace-protocol §2.7。自动审计正文仅 `/audit workspace-NNN goal-NNN` 或 `/vision-audit vp-NNN`；带标签编号唯一绑定完整身份，拒绝裸数字、非法编号、多余参数、换行/包装，不截断后执行。
- 自动派发禁止自编提示词、scope/文件清单/结论预期及隐藏上下文注入；使用干净会话，不复制编排历史，审计员自主扫描和定 scope。正式入口不可用则门禁未满足，不用自由提示兜底；人类直调关注点不作为自动请求的豁免。
- 需用户信息时同步阻塞询问卡片优先；不可用/用途受限/headless 无答复通路则文本提问并停止。空返回、取消/关闭/超时、缺题、预选未提交均未答，不补默认或虚构答复，不以权限批准/工具成功当答案；部分答复仍等待其余。
- 发问后停止当前任务；由有权编排侧记录原问题/选项、影响、原因、恢复条件和其他阻塞，将当前 active/draft Goal 置 blocked 并同步执行记录、goal-tree 树/表及父级投影。独立审计只在自身权限记录/返回待答事实，不越权改 meta；无 Goal 只暂停，VP 不改 blocked，done/cancelled 不自动 reopen。写盘失败仍停止；真实答复留痕、复核全部门禁后才解除相应阻塞恢复。

暂停收尾：已授权治理任务中的待答/blocked/执行索引/目标树同步是必须完成的暂停收尾，**无需另次确认**；在返回问题或进入等待前完成，不得因未答省略，不预写真实答复或未发生的工具返回。独立审计仍不扩大写权限。

工具识别提示：grok 的询问工具示例为 `ask_user_question`，仅在本会话实际可用且允许时调用；不可凭工具名声称阻塞/取消行为已验证。

## 执行

1. 定位 **SKILLS_PKG**：含 `prompts/07-independent-vision-review.md` 或 `prompts/06-vision-orchestrator.md` 的目录。
2. **完整阅读并严格执行** `<SKILLS_PKG>/prompts/07-independent-vision-review.md` 的「提示词正文」。
3. 用户在本 skill / `/vision-audit` 后附带文字仅在明确由人类直调时视为审视 scope 或关注对象；自动请求仅接受 `vp-NNN` 命令，不要求补 scope 表单。

## 行为要点

- 只创建 `{governance_root}/vision/reviews/VRev-NNN-<slug>.md` 独立报告并更新 `reviews.md` 索引；不写 Goal `03-audit.md`。
- 不修改 Charter / VP / Goal status、progress、`revisions.md` 或 `goal-tree.md`。
- required Vision finding 的响应交 `/vision`；实施工作交 `/govern`。

## 完成

告诉用户：verdict、required finding、写入路径，以及建议的 `/vision` 响应输入。
