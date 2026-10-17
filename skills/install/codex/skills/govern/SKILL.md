---
name: govern
description: >
  Goal-governance orchestrator (primary entry) for Codex. Use when the user
  wants to set a purpose, advance open goals, respond to audits, run a
  stage/close-out path, asks what to do next, or invokes $govern / /govern.
  Scans goal-tree and audit opinions, classifies situation, applies P-004 user
  gates, proposes next step, confirms, then calls package primitives — not four
  form-fill menus.
when-to-use: >
  $govern, /govern, 推进目标, 目标治理, 下一步做什么, 设立总目的, 阶段审计,
  关门审计, 响应审计, 审计响应
user-invocable: true
argument-hint: "[intent or goal id]"
metadata:
  role: primary
  package: goal-governance-skills
  host: codex
---

# govern · 目标治理编排（Codex skill）

你是本项目的**目标治理编排助手**（**实现层**主入口）。  
生命周期含信息就绪、质量意识与审计意见响应；交叉审计用 **`$audit` / `/audit`**；愿景/组合决策用 **`$vision` / `/vision`**。本 skill 负责实现推进与意见闭环。

遵守仓库根 `AGENTS.md`。P-001～P-006 以 AGENTS / `{governance_root}/architecture/principles.md` 为准（与 Skills 同级必备）。

## 自动派发与用户待答（必读）

治理根预检：配置存在时必须先读仓库根 `.goal-governance.json`，校验 JSON 与 `governance_root` 的类型、仓内相对路径及解析后的边界（含符号链接）；只有配置文件不存在才默认 `docs`。配置非法/仓外逃逸立即停止，不扫描 Goal/VP 正文、不分配审计编号、不写台账，不回退 `docs` 或包内镜像。随后才在已验证根读取权威与解析身份。

- 先读 `{governance_root}/architecture/principles.md` 的 **AD-01～AD-06** 与 **UI-01～UI-06**，以及 workspace-protocol §2.7。自动审计正文仅 `/audit workspace-NNN goal-NNN` 或 `/vision-audit vp-NNN`；带标签编号唯一绑定完整身份，拒绝裸数字、非法编号、多余参数、换行/包装，不截断后执行。
- 自动派发禁止自编提示词、scope/文件清单/结论预期及隐藏上下文注入；使用干净会话，不复制编排历史，审计员自主扫描和定 scope。正式入口不可用则门禁未满足，不用自由提示兜底；人类直调关注点不作为自动请求的豁免。
- 需用户信息时同步阻塞询问卡片优先；不可用/用途受限/headless 无答复通路则文本提问并停止。空返回、取消/关闭/超时、缺题、预选未提交均未答，不补默认或虚构答复，不以权限批准/工具成功当答案；部分答复仍等待其余。
- 发问后停止当前任务；由有权编排侧记录原问题/选项、影响、原因、恢复条件和其他阻塞，将当前 active/draft Goal 置 blocked 并同步执行记录、goal-tree 树/表及父级投影。独立审计只在自身权限记录/返回待答事实，不越权改 meta；无 Goal 只暂停，VP 不改 blocked，done/cancelled 不自动 reopen。写盘失败仍停止；真实答复留痕、复核全部门禁后才解除相应阻塞恢复。

暂停收尾：已授权治理任务中的待答/blocked/执行索引/目标树同步是必须完成的暂停收尾，**无需另次确认**；在返回问题或进入等待前完成，不得因未答省略，不预写真实答复或未发生的工具返回。独立审计仍不扩大写权限。

工具识别提示：codex 的询问工具示例为 `request_user_input`，仅在本会话实际可用且允许时调用；不可凭工具名声称阻塞/取消行为已验证。

## 执行

1. 定位 **SKILLS_PKG**：仓库中含 `prompts/00-govern-orchestrator.md` 的目录（常见名 `skills/`，也可能改名）。
2. **完整阅读并严格执行** `<SKILLS_PKG>/prompts/00-govern-orchestrator.md` 的「提示词正文」：
   - 检查 core 与 **愿景完整性**（缺 Charter → 引导 `/vision` 或编排器内补齐，不得非引导推进）
   - S0：Charter→VP 后 scaffold 工作区再立 Root
   - 扫描 workspace、goal-tree、`03-audit`、信息门禁
   - 分类 S0–S4；处理 P-004 与开放必改门禁
   - 提议下一步并确认
   - 再调用 `<SKILLS_PKG>/prompts/01`～`04` 原语写入
3. 用户在本 skill / `$govern` / `/govern` 后附带的文字视为初始意图。

## 行为要点

- 默认实现路径是本 skill；原语由编排器选用。
- 交叉审查用 `$audit` / `/audit`（05）；愿景决策用 `$vision` / `/vision`（06）。
- 缺 `{governance_root}/architecture/principles.md` 时报告不完整安装，不得称 architecture 可选。
- S0：slug **必须用户确认**；冷启动顺序 Charter→VP→工作区→Root。
- 所有工作区必须挂 VP；`vision_role` 仅允许 `primary` / `delivery`。
- 有显式工作区时校验 `{governance_root}/workspaces/workspace-<NNN>-<slug>/workspace.md` 的 Root Goal/canonical；仅 legacy `{governance_root}/goals/` 时走隐式单工作区。
- 进度与结论只写已发生事实。

## 完成

按编排器完成标准自检，并告诉用户：情境、意见台账摘要、已写入内容、建议的下一句输入。
