---
id: GOAL-002-codex-skills-entry
doc: decision
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-07-31
updated: 2026-07-31
version: 0.3.0
---

# 决策记录 · GOAL-002

## 信息需求与阶段门禁

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 状态 |
|----|------|-----------------|----------|--------------|------|
| I-001 | required | Codex skills 加载机制 | 方案冻结 | B | **verified**（2026-07-31） |
| I-002 | required | 四入口最小形态 | 方案冻结 | B | **verified**（2026-07-31） |
| I-003 | non-blocking | 矩阵是否 committed | 发版宣称 | 验收 | open |
| I-004 | non-blocking | 跨平台路径 | 实施完整度 | C | **verified**（2026-07-31） |

> **门禁**：I-001/I-002 已 verified → **允许**冻结目录/安装开关方案并进入实现（阶段 C）。  
> Runtime 探针仍属成功标准 #4 / 阶段 D，**不**回退本冻结。

## D-001 · 立项：Codex Skills 入口（2026-07-31）

**决定**：

1. 新建本目标，`parent` = Root，`status: active`。
2. 范围：**安装面 + 可调用入口**，使 Codex 能消费本包治理 Skills；核心 prompts 仍以 `skills/prompts/` 为真相，不复制第二套编排正文。
3. 对标现有三宿主适配模式；具体 Codex 目录约定待 I-001 关闭后写入 D-00N 方案决策。
4. 阶段 A→D 见 meta；先信息澄清再方案再实现。

**为什么**：

- 用户明确需要「Codex 所能使用的 skills 入口」。
- 现包已有 claude / copilot / grok，缺 Codex 是明确的消费面缺口，适合作为 VP-002 / R1 首刀。

**未选方案**：

- **仅 README 说明「请手工复制 prompts」**：不能称为可用入口，也难与 install 门禁对齐。
- **改核心协议代替宿主适配**：问题在消费入口，不在 P-001～P-006 正文。
- **四入口一次全部 runtime-verified 才允许任何代码**：可作为关门高标准，但不应阻塞有界探测与骨架落地；验收标准仍要求至少主入口可核对验证。

## D-002 · 冻结 install/codex 方案（2026-07-31）

**状态**：accepted  
**依据**：I-001/I-002 verified；用户 `/govern` 确认「OK 全套写入」  
**证据**：[attachments/i-001-i-002-codex-skills-loading-2026-07-31.md](attachments/i-001-i-002-codex-skills-loading-2026-07-31.md)

### 决定

1. **REPO skill 根路径（默认）**：项目根下 **`.agents/skills/<skill-name>/SKILL.md`**（官方 REPO scope；非 `.claude/skills`、非默认 `.codex/skills`）。
2. **四入口独立 skill**（与 claude/grok 同构，非单入口 dispatch）：
   - `govern` · `audit` · `vision` · `vision-audit`
   - 用户侧：`$govern` / `$audit` / `$vision` / `$vision-audit`（及隐式 description 匹配）
   - 正文：薄包装，执行时定位 SKILLS_PKG 并读 `prompts/00` / `05` / `06` / `07`。
3. **包内源目录**：
   ```text
   skills/install/codex/skills/
     govern/SKILL.md
     audit/SKILL.md
     vision/SKILL.md
     vision-audit/SKILL.md
   ```
4. **安装开关**：`install.ps1` / `install.sh` 增加 **`-Codex` / `--codex`**；**`-All` / `--all` 纳入 Codex**（与 claude + grok + copilot 并列）。
5. **AGENTS.md**：`--codex` 时安装仓库根 `AGENTS.md`，源文件复用 `install/claude/AGENTS.md`（与 Claude 同一规则真相；不另起第二套协议文）。
6. **契约/矩阵（I-003）**：本轮**不**强制把 Codex 标为 matrix `committed`；发版宣称前再决；允许 residual。
7. **阶段边界**：本决策只冻结方案；**实现与脚本改动属阶段 C**；runtime 验证属阶段 D。

### 为什么

- 官方明确 REPO skills 在 `.agents/skills`，AGENTS 为独立 instruction 链；对标 claude（`.claude/skills`）与 grok（`.grok/skills`）的「宿主专用 skill 根 + 四入口」。
- 四独立 skill 对齐 `requiredEntrypoints` 与现有三宿主，避免单 dispatch 稀释 `/audit` 与 `/vision` 角色。
- 复用 Claude AGENTS 源避免第四套规则漂移。

### 未选方案

| 方案 | 未选理由 |
|------|----------|
| 默认安装到 `~/.agents/skills`（仅 USER） | 不可随仓复现；消费方默认应提交 repo skill |
| 默认 `.codex/skills` 或双写历史路径 | 非现行官方 REPO 表；增加维护面 |
| 单 skill + 内部 dispatch | 与四入口契约/矩阵不一致 |
| 首发只交付 govern | 可分期 **验证**，但 install 面应一次齐四入口（同 claude/grok） |
| 本轮改 consumer 矩阵为 verified/committed | 无 runtime 证据；I-003 仍 non-blocking |

### 影响

- 解除方案冻结门禁 → 可进入阶段 C 实现。
- 阶段 A 完成；成功标准 #1 勾选；`progress` 1/4。
- 不改 Charter / VP；不改 workspace-001。

### 后续

1. ~~阶段 C：创建 `install/codex/skills/*` SKILL 包装；改 `install.ps1` / `install.sh`；按需更新 skills README/help。~~ **已完成**（2026-07-31）。
2. 阶段 D：Codex 宿主对 `$govern`（或等价）runtime 探针 + 关门审计。
3. I-003：发版前决定矩阵是否 committed。
