---
id: GOAL-014-ai-collaboration-runtime
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 0.7.0
---

# 决策记录 · GOAL-014

## D-001 · 立项：AI 协作运行时有界实现（2026-07-22）

**状态**：accepted

**确认来源**：用户 `OK R1：创建 X-AI（GOAL-014 AI 协作运行时）`（GOAL-009 D-028 / A-051）。

**决定**：

1. 创建本目标，`parent: GOAL-001-main-vision`，`planning_source: GOAL-009-ai-assisted-governance-workbench`，扩展代号 **X-AI**。  
2. 范围 = **有界 AI 运行时 + 候选确认链**，对齐 GOAL-009 未勾成功标准与 I-002 收集方向；**不**一次交付多模型运维、资料 AI 读全文、多区导航。  
3. 必须遵守：canonical 仍为工作区 Markdown；AI 输出默认候选；用户显式确认前不写事实；不自动 P-004 / 关门 / 关 finding。  
4. 实施前完成路线图阶段 A（边界冻结）；阶段 A 未冻结前不得宣称 AI 产品可用。  
5. GOAL-009 保持 `active`；本立项 **不**关闭 R-E-3-X。

**为什么**：α 切片已验证受控写入，但产品愿景「AI 协助」仍缺运行时；R1 优先补愿景缺口。

**未选方案**：

- R3 先做导航/资料：延后 AI 成功标准。  
- 在 GOAL-009 内直接改代码不立项：违背「规划台账 vs 实现子目标」分离。  
- 无边界即接真实 API：越过 I-002 / 密钥与确认门禁。

**影响与后续**：五件套 + goal-tree；下一步 `/govern` 推进阶段 A 边界冻结（或用户指定实现步）。

## D-002 · 冻结阶段 A：AI 运行时边界（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-014 阶段 A：冻结 AI 运行时边界`。

**决定**：

1. 接受 [attachments/r-014-a-runtime-boundary.md](attachments/r-014-a-runtime-boundary.md)（**R-014-A v1.0**）为阶段 A 权威冻结基线。  
2. 冻结内容包括：范围/非目标、硬边界、`.env` 字段语义、可见上下文允许/禁止、工具矩阵（阶段 C 仅 completion；检索默认延至 D 或明确不做）、`source_kind` 升格、确认→R-004 写衔接、失败降级、trust/密钥规则。  
3. **继承** GOAL-009 R-002 / D-012 / D-017 设计默认，不削弱 D-001～D-006 / D-011 治理边界。  
4. 阶段 A **退出**；路线图 A → **完成**；成功标准第 1 条勾选。  
5. I-001 字段语义、I-002 可见上下文边界标为 **verified（边界）**；**不**将 GOAL-009 I-002 整项 verified；**不**实现代码；**不**启用真实 API。  
6. 阶段 B 起实现必须 fail closed 于 `AI_ENABLED=false` 或配置不全。

**为什么**：边界先于 broker，避免无契约接模型；用户明确要求冻结阶段 A。

**未选方案**：边写代码边补边界；阶段 C 默认开放网络检索；AI 直写 canonical。

**影响**：progress **15%**；A-001 记录；下一步阶段 B 配置加载与 broker 骨架。

## D-003 · 完成阶段 B：AI 配置加载与 broker 骨架（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-014 阶段 B：AI 配置加载与 broker 骨架`。

**决定**：

1. 实现 `web/services/ai_config.py`：按 R-014-A 解析 AI env；默认禁用；不全则 `ready=false`。  
2. 实现 `web/services/ai_broker.py`：配置门禁、`FakeTransport`、OpenAI-compatible HTTP 骨架；成功产出带 `ai-knowledge` 标签的候选字段（**不**写盘）。  
3. `/api/health` 增加 `ai` 公开状态（无 API key）。  
4. unittest 覆盖禁用/不全/就绪/无泄漏/fake 成功/错误映射。  
5. 阶段 B **退出**；进度 **35%**；**不**接 UI 确认链（阶段 C）。  

**为什么**：边界已冻结；先可测骨架再 UI。

**未选**：真实网络 E2E 作为 B 退出条件；默认 `AI_ENABLED=true`。

**影响**：A-002；goal-tree 同步。

## D-004 · 完成阶段 C：候选 API 与确认链（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 推进 GOAL-014 阶段 C：候选 API 与确认链`。

**决定**：

1. 实现进程内 AI 候选台账与 confirm/reject；confirm 经 **FA** 后构建 R-004 提案（**decide 才写盘**）。  
2. 详情页增加 AI 候选面板；`POST .../ai/suggest|confirm|reject` 与 `POST /api/.../ai/complete`。  
3. `controlled_change` 允许 FA 合法 `source_kind`（含 `ai-knowledge`），禁止非法 kind 与伪装。  
4. 阶段 C **退出**；progress **65%**；阶段 D 工具/检索仍默认关闭。  

**为什么**：R-014-A §7 确认链是 AI 可用的最小闭环。

**未选**：confirm 直接写盘；默认开放网络检索。

**影响**：A-003；goal-tree 同步。

## D-005 · 阶段审视结论登记（不关门）（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 阶段审视 GOAL-014`。

**决定**：

1. 接受 [A-004](03-audit.md#a-004--阶段审视goal-014-有界-ai-运行时不关门2026-07-22) 阶段审视：A～C **完成**；verdict **conditional**。  
2. GOAL-014 **保持 `active`**；progress **75%**；**不** `done`。  
3. 登记 residual：**R-014-D**（工具/检索实现或书面不做）、**R-014-E2E**（浏览器/真联调 recommended）。  
4. 有界关门前必须裁决 R-014-D；关闭 R-014-D 不等于关 GOAL-009。  

**为什么**：阶段审只确认事实；工具阶段未做，不可伪装全文验收。

**影响**：台账 + goal-tree；下一步由用户选 D 或有界关门路径。

## D-006 · 阶段 D 声明「本目标不做」检索/敏感工具，关闭 R-014-D（2026-07-22）

**状态**：accepted

**确认来源**：用户 `OK D-skip：阶段 D 声明本目标不做检索/敏感工具，关闭 R-014-D`。

**决定**：

1. **阶段 D 有界退出**：GOAL-014 **不实现**网络/外站检索、本地 shell、任意文件写，以及其他 R-014-A §5 中的敏感工具调用路径。  
2. 运行时保持 **用户触发 completion only**（阶段 B/C 已交付）；默认 `AI_ENABLED=false` 不变。  
3. **关闭 residual R-014-D** 与 A-004 **F-001**（关闭证据 = 本决定书面范围 + A-005）。  
4. 若未来需要检索/工具：须**另立目标**或新 residual，不得 silently 扩 GOAL-014 范围。  
5. **R-014-E2E** 仍 open（recommended）；**不**因本条将 GOAL-014 标 `done`（有界关门须另令）。  
6. progress **85%**。

**为什么**：A-004 要求关门前显式裁决工具；用户选择「不做」而非实现，避免未决项伪装完成。

**未选**：实现有界工具矩阵；无书面声明即关 R-014-D。

**影响**：A-005；meta 路线图 D；goal-tree 同步。

## D-007 · 有界关门 GOAL-014（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 有界关门审计 GOAL-014`。

**决定**：

1. 执行有界 close-out（A-006）：成功标准在声明范围内均有证据；R-014-D 已 closed。  
2. **接受 residual R-014-E2E**（浏览器 DOM 全矩阵 / 真实提供方生产联调）；复审触发：宣称 UI 全矩阵验收或生产真联调前。  
3. GOAL-014 → `status: done` · `progress: 100%`。  
4. **不**因本条：GOAL-009 `done`；勾选 GOAL-009 AI 成功标准；默认 `AI_ENABLED=true`；实现检索工具。  

**为什么**：有界 X-AI 交付与 residual 齐备；用户明确要求有界关门审计。

**未选**：无 residual 全文关（含 E2E）；连 GOAL-009 一并关门。

**影响**：goal-tree；GOAL-009 可记交接（AI 运行时有界交付）。
