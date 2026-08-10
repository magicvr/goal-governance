---
title: I-001 / I-002 · Codex skills 加载机制与四入口形态调研
status: active
created: 2026-07-31
updated: 2026-07-31
parent: GOAL-002-codex-skills-entry
version: 0.1.0
---

# Codex skills 加载机制与四入口形态（I-001 / I-002）

> 收集日：2026-07-31  
> 范围：官方文档结论，用于**方案冻结**；**不**替代阶段 D 的 Codex 宿主 runtime 探针。  
> 关联目标：`GOAL-002-codex-skills-entry` · 工作区 `workspace-002-methodology-skills-feedback`

## 1. 信息项结论摘要

| ID | 问题 | 结论（方案可用） | 状态建议 |
|----|------|------------------|----------|
| **I-001** | Codex 如何发现 skills；与 AGENTS 关系 | 见 §2 | `verified`（文档证据） |
| **I-002** | 四入口最小可行形态 | 见 §3：四独立 skill 目录 | `verified`（对照 + 能力） |

## 2. I-001 · Skills 加载与 AGENTS.md

### 2.1 Skill 形状（Agent Skills 兼容）

官方 [Build skills](https://developers.openai.com/codex/build-skills) / [learn.chatgpt.com/docs/build-skills](https://learn.chatgpt.com/docs/build-skills)：

- 一个 skill = **目录** + 必需 `SKILL.md` + 可选 `scripts/`、`references/`、`assets/`、`agents/openai.yaml`
- `SKILL.md` frontmatter **必须**含 `name`、`description`
- **渐进披露**：宿主先用 name/description 做发现；选中后再读完整 `SKILL.md`；需要时再读 references / 跑 scripts
- Codex 初始 skills 列表还带 **file path**；列表有上下文预算（约上下文 2% 或 8000 字符上限），技能过多会缩短 description 甚至省略部分 skill

### 2.2 调用方式

| 方式 | 说明 |
|------|------|
| **显式** | Codex CLI / IDE：`/skills` 或 `$skill-name` 提及 skill |
| **隐式** | 任务与 `description` 匹配时由宿主选用 |

### 2.3 本地发现路径（官方表 · 权威）

| Scope | Location | 用途 |
|-------|----------|------|
| REPO | `$CWD/.agents/skills` | 当前工作目录下的项目 skill |
| REPO | 向上各级 `…/.agents/skills` 至 `$REPO_ROOT/.agents/skills` | 嵌套目录 / 仓库根共享 skill |
| USER | `$HOME/.agents/skills` | 用户级，跨仓库 |
| ADMIN | `/etc/codex/skills` | 机器/容器级 |
| SYSTEM | Codex 内置 | 如 skill-creator、plan |

补充（官方 customization 摘要表）：

| 层 | Global | Repo |
|----|--------|------|
| AGENTS | `~/.codex/AGENTS.md`（或 `CODEX_HOME`） | 仓库根/嵌套 `AGENTS.md` / `AGENTS.override.md` |
| Skills | `~/.agents/skills` | **`.agents/skills`** |

- 支持 **symlink** skill 目录。  
- 同 `name` 的 skill **不合并**，可同时出现在选择器。  
- `~/.codex/config.toml` 可用 `[[skills.config]]` 按 path 禁用 skill（需重启）。  
- 社区/历史仍可见 `~/.codex/skills`、`.codex/skills` 叙述；**方案以现行官方 `.agents/skills` 为准**，不把遗留路径写进默认 install。

### 2.4 AGENTS.md（规则层 · 非 skill 目录）

官方 [AGENTS.md](https://learn.chatgpt.com/codex/agent-configuration/agents-md)：

- Codex 在动手前读取 instruction 链：全局（`CODEX_HOME` / `~/.codex` 下 `AGENTS.override.md` 优先于 `AGENTS.md`）→ 自项目根向下至 CWD 每层至多一个文件（override → AGENTS → fallback 名）
- 与 skills **互补**：AGENTS = 持久项目规则；skills = 可复用工作流包
- 默认合计上限 `project_doc_max_bytes`（默认 32 KiB）

**对 install 的含义**：与 Claude 类似，Codex 消费方也受益于仓库根 `AGENTS.md`（本包已有 `install/claude/AGENTS.md` 可复用）；**skills 安装目标目录是 `.agents/skills/`，不是 `.claude/skills/` 或 `.codex/skills/`（默认）**。

### 2.5 证据来源（文档）

| # | 来源 | 用途 |
|---|------|------|
| 1 | https://learn.chatgpt.com/docs/build-skills（developers.openai.com/codex/build-skills 重定向） | 形状、发现路径表、调用、插件分发 |
| 2 | https://learn.chatgpt.com/codex/customization/overview | AGENTS vs Skills 分层表 |
| 3 | https://learn.chatgpt.com/codex/agent-configuration/agents-md | AGENTS 发现链 |
| 4 | 对照本仓 `skills/install/claude/`、`skills/install/grok/` | 四入口薄包装模式 |

**未做（留给阶段 D）**：本机 Codex CLI/IDE 的 runtime 探针（成功标准第 4 项）。

## 3. I-002 · 四入口最小形态

### 3.1 宿主能力对照

| 能力 | Codex | 对本包含义 |
|------|-------|------------|
| 多 skill 目录 | 是（`.agents/skills/<name>/`） | 可与 claude/grok 同构四入口 |
| 显式 `$name` | 是 | 用户可 `$govern` / `$audit` / `$vision` / `$vision-audit` |
| 隐式匹配 description | 是 | description 需含触发词（治理/审计/愿景等） |
| 单入口 dispatch | 可做但不必要 | 会丢独立 `/audit` 与 `/vision` 语义，且与现三宿主不一致 |

### 3.2 推荐形态（方案冻结）

**四独立 skill**（薄包装 → `skills/prompts/` 真相），包内源：

```text
skills/install/codex/skills/
  govern/SKILL.md
  audit/SKILL.md
  vision/SKILL.md
  vision-audit/SKILL.md
```

安装落点（项目根）：

```text
.agents/skills/govern/SKILL.md
.agents/skills/audit/SKILL.md
.agents/skills/vision/SKILL.md
.agents/skills/vision-audit/SKILL.md
```

| 入口 | skill `name` | 用户侧 | 指向核心 prompt |
|------|--------------|--------|-----------------|
| 实现编排 | `govern` | `$govern` / 隐式 | `prompts/00-govern-orchestrator.md` |
| 目标交叉审 | `audit` | `$audit` | `prompts/05-independent-audit.md` |
| 愿景决策 | `vision` | `$vision` | `prompts/06-vision-orchestrator.md` |
| 独立 Vision Review | `vision-audit` | `$vision-audit` | `prompts/07-independent-vision-review.md` |

**AGENTS.md**：`--codex` 安装时写入/覆盖策略对齐 Claude（复用同一 `install/claude/AGENTS.md` 源，或 codex 目录旁路指针到同一文件），保证规则层与 skill 层同时可用。

### 3.3 未选形态

| 形态 | 未选理由 |
|------|----------|
| 单 skill dispatch | 弱化四入口契约与矩阵对齐；description 过载 |
| 仅 USER `~/.agents/skills` | 不可随仓库复现；消费方 install 默认应是 **repo 可提交** 路径 |
| 默认写 `.codex/skills` | 非现行官方 REPO 路径 |
| 首发只装 govern | 可分期验证，但源面与 `--codex` 应一次覆盖四入口（与 claude/grok 一致） |

## 4. 对 install 脚本的含义（供 D-002 / 阶段 C）

| 项 | 建议 |
|----|------|
| 包路径 | `skills/install/codex/skills/{govern,audit,vision,vision-audit}/SKILL.md` |
| 开关 | `install.ps1` / `install.sh`：`-Codex` / `--codex`；`-All` 纳入 Codex |
| 目标 | `./.agents/skills/<name>/SKILL.md` |
| AGENTS | 与 Claude 相同源 → 仓库根 `AGENTS.md`（已存在则按现有 overwrite 策略） |
| 契约/矩阵 | I-003 non-blocking：发版宣称再决是否 `committed`；本轮不强制改矩阵 |
| 平台 | I-004：路径 POSIX/Windows 均用相对 `.agents/skills`；脚本双平台在 C 实现 |

## 5. 残余与复审

| 项 | 处理 |
|----|------|
| 本机 runtime 未跑 | **不**写入 I-001 residual；作为成功标准 #4 / 阶段 D 证据 |
| 官方路径变更 | 若 OpenAI 改 REPO skill 根路径，重开 I-001 复核后再改 install |
| 历史 `.codex/skills` | 文档可 footnote；默认 install **不**双写 |
