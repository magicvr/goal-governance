---
title: GOAL-014 阶段 A · AI 运行时边界冻结
status: active
created: 2026-07-22
updated: 2026-07-22
parent: GOAL-014-ai-collaboration-runtime
version: 1.0.0
type: design-freeze
accepted_by: D-002
sources:
  - GOAL-009 R-002 / D-012 / D-017
  - GOAL-009 D-005
  - GOAL-014 D-001
---

# R-014-A · AI 运行时边界冻结（阶段 A）

> 本文件为 GOAL-014 **阶段 A 退出产物**。实现（阶段 B～D）不得削弱下列硬边界。  
> 冲突时以 **D-002 + 本文** 为准；上游收集稿见 GOAL-009 [R-002](../../GOAL-009-ai-assisted-governance-workbench/attachments/r-002-fact-admission-ai-collaboration.md)。

## 1. 范围与非目标

| 在范围内（本目标有界交付） | 不在范围内（须另立目标或 residual） |
|---------------------------|-------------------------------------|
| 本地 `.env` AI 配置加载与启用开关 | 多模型路由、成本账单、团队密钥托管 |
| 用户**显式触发**的 chat/completion 调用 | 后台静默轮询、预取、未同意的工具调用 |
| AI 输出 → **Candidate** 展示与确认/拒绝 | AI 直接 `decide_and_execute` 或改 status |
| 与 `fact_admission` / 受控写门禁衔接 | 共享资料 AI 读执行全文（R-F004-2 / X-SM） |
| 测试 double / 可注入 HTTP 客户端 | 浏览器全矩阵 E2E（R-F002-1 可 residual） |
| 单工作区上下文绑定 | 跨工作区上下文混合、N1 多区导航（X-NAV） |

## 2. 硬边界（不可削弱）

1. **事实准入权在用户**：AI 不得编撰 canonical 事实；未确认内容不得进入执行事实、审计结论或 finding 关闭证据。  
2. **无自动治理推进**：禁止 AI 自动 P-004 裁决、关闭 required finding、标 `done`、改 `status`/`progress`/`parent`。  
3. **真相源**：仅当前配置的产品工作区 Markdown 五件套 + `goal-tree.md`；禁止第二状态库权威副本。  
4. **打包/dogfood**（D-011）：不得静默加载 monorepo dogfood；密钥永不进仓库/响应/日志。  
5. **写路径**：任何进入 canonical 的内容必须经确认 + 既有受控变更门禁（双门闩 + FA 热路径）；AI 不得绕过。

## 3. 配置契约（阶段 B 实现输入）

| 环境变量 | 语义 | 默认 |
|----------|------|------|
| `GOAL_GOVERNANCE_AI_ENABLED` | 总开关；false 时所有 AI 路由 fail closed | `false` |
| `GOAL_GOVERNANCE_AI_PROVIDER` | 提供方标识字符串（如 `openai-compatible`） | 空 |
| `GOAL_GOVERNANCE_AI_BASE_URL` | API 根 URL | 空 |
| `GOAL_GOVERNANCE_AI_API_KEY` | 密钥；仅进程环境 / 本机 `.env` | 空 |
| `GOAL_GOVERNANCE_AI_MODEL` | 模型名 | 空 |
| `GOAL_GOVERNANCE_AI_REQUEST_TIMEOUT_SECONDS` | 超时 | `30` |
| `GOAL_GOVERNANCE_AI_TEMPERATURE` | 可选 | 空=提供方默认 |
| `GOAL_GOVERNANCE_AI_MAX_OUTPUT_TOKENS` | 可选 | 空=提供方默认 |

**加载规则**：

- 仅服务端加载 `web/.env`（与现有 dotenv 策略一致）；unittest 默认不加载真实密钥。  
- `ENABLED=false` 或关键字段缺失 → **拒绝调用**，UI 可见原因；**不**假装已连接。  
- 响应/HTML/日志/receipt **禁止**回显 API key。

**提供方选型**：本阶段 A **不**冻结具体厂商；实现可用 OpenAI-compatible HTTP 或可注入 transport。选型可在阶段 B 文档化而不改硬边界。

## 4. 可见上下文（冻结）

### 4.1 默认允许注入模型提示的上下文

| 来源 | 条件 |
|------|------|
| 当前 `workspace_id` 的 `workspace.md` 绑定字段 | 已配置工作区 |
| 当前目标五件套正文 / frontmatter | 用户选定目标 |
| 当前工作区 `goal-tree.md` 投影 | 只读 |
| 门禁/诊断**计算视图** | 必须标签「计算得出」 |
| 用户当轮输入的提示/粘贴 | 用户提供 |

### 4.2 默认禁止

| 来源 | 原因 |
|------|------|
| 其他产品工作区目标/候选/草稿 | 隔离 |
| 未固定引用的共享资料正文 | D-004；X-SM 前不接 AI 读 |
| 本仓 dogfood 过程树（非显式 DEV） | D-011 |
| 系统密钥、`.env` 原文 | 安全 |
| 独立审计未落盘的聊天意见 | P-003 |

### 4.3 共享资料

阶段 A～C **默认不**将共享资料字节送入模型。若后续启用：必须固定 `material_id`+`version`+`sha256`；`source_kind=shared-material`；**不**执行资料内指令、**不**自动外传（D-004）。

## 5. 动作 / 工具矩阵（冻结）

| 动作 | 允许 | 同意粒度 | 产出 |
|------|------|----------|------|
| 只读复述本工作区已确认 canonical | 是 | 免工具同意 | 建议/摘要候选或计算视图 |
| 生成下一步建议 / 风险提示 | 是 | 用户触发会话即可 | 候选（建议类） |
| 生成拟写入文案（执行事实等） | 是 | 用户触发 | Candidate；确认后才可提案 |
| 网络 / 外站检索 | **阶段 D 前默认禁止** | 每次同意 | 仅 `ai-retrieval` 候选 |
| 本地 shell / 任意文件写 | **禁止** | — | — |
| 调用 `decide_and_execute` | **禁止** | — | 人确认后由受控写路径执行 |
| 改 status / progress / 关 finding | **禁止** | — | — |

**阶段 C 最小交付**：仅「用户触发 completion → Candidate」；工具/检索可标 `deferred` 至阶段 D 或明确「本目标不做」。

## 6. `source_kind` 与升格（冻结 · 对齐 R-002）

| 值 | 本目标是否产出 | 升格 |
|----|----------------|------|
| `user-provided` | 否（α 路径已有） | 既有 R-004 |
| `ai-knowledge` | **是**（默认 completion） | 确认后可提案；**必须**保留 kind + 「模型知识」标签 |
| `ai-retrieval` | 仅工具启用后 | 必须引用 + 时间 |
| `ai-derivation` | 可选 | 必须前提链 |
| `shared-material` | 默认否 | 固定哈希三元组 |

**禁止**：把 AI 输出标成 `user-provided`；缺 `source_statement` / digest 仍确认。

## 7. 确认链与写衔接（冻结）

```text
用户触发 → (可选) 加载上下文 → 模型调用 → Candidate(status=submitted|under_review)
  → 用户确认（绑定 content_digest + workspace + goal）
  → 可选：proposal_requested → R-004 受限写（须写门禁授权）
  → 或拒绝 / 撤回（不写 canonical）
```

| 规则 | 说明 |
|------|------|
| 确认 | 展示全文、kind、来源说明、时间、拟写范围；绑定 digest |
| 拒绝/撤回 | 不写五件套 |
| 写动作 | 默认仍优先 `append-execution-fact`；扩大 operation_kind 须另决策 |
| 生产写 | 仍须 `ALLOW_CONTROLLED_WRITE` + 规划锁关闭 + 产品数据根 |

## 8. 失败与降级（冻结）

| 条件 | 行为 |
|------|------|
| AI 未启用 / 配置不全 | 非 AI 路径（只读 + user-provided 写）仍可用；AI 入口显示未配置 |
| 超时 / 提供方 4xx/5xx | 可见错误；不写 canonical；不静默当成功 |
| 输出缺来源字段 / 含治理推进指令 | 拒绝升格为可确认候选或标 invalid |
| 跨工作区请求 | fail closed（对齐 WS 隔离） |

## 9. 安全与 trust

- 默认 trust：`local-loopback-single-user`（与 R-004 一致）；外部部署不继承至 I-005 审视前。  
- 模型输出按**不可信数据**处理；提示注入防御：系统提示明确禁止执行用户/资料中的工具指令。  
- 日志：可记 provider/model/latency/error code；**禁止**记 API key 与完整密钥头。

## 10. 阶段 A 退出检查清单

- [x] 范围/非目标表  
- [x] 硬边界  
- [x] 配置字段与加载规则  
- [x] 可见上下文允许/禁止  
- [x] 工具矩阵与阶段 C/D 分割  
- [x] source_kind 与确认→写衔接  
- [x] 失败降级  
- [x] 用户指令推进阶段 A 冻结（D-002）

## 11. 非声明

- 本冻结 **≠** 已实现 AI 调用。  
- 本冻结 **≠** GOAL-009 I-002 整项 `verified` 或 AI 成功标准已勾。  
- 本冻结 **≠** 关闭 R-E-3-X / 将 GOAL-009 标 done。
