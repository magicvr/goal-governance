---
id: GOAL-008-consumer-layer-split-and-hosting
doc: attachment
title: S1 盘点报告 · I-001～I-004 证据汇总
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-13
updated: 2026-09-13
version: 0.1.0
---

# 附件 · S1 盘点报告（I-001～I-004，2026-09-13）

> 只读盘点的证据汇总，供独立审计逐条复核。所有主张均带 `file:line`；未运行实现、安装或发布验证。
> 汇总与结论见 [D-004](../01-decision/D-004-s1-inventory-acceptance.md)；验收矩阵见 [s1-acceptance-matrix.md](s1-acceptance-matrix.md)。

## 1. 方法与边界

- 范围：本目标 S1；baseline = 本地 `dev`（S1 产物提交前的 HEAD `b90b2d8`）。
- 方法：静态只读核对（canonical 文档、Skills prompts、install/update 脚本、mcp、contracts、tests、vision 实例、工作区实例）。
- 排除：实现正确性、消费宿主运行时行为（S4/S6 才验）、远端版本与正式发布、其他工作区上下文。
- 限制：四路盘点由并行只读会话完成，**未**改动任何文件；引用行号可在本提交检出后复核。

## 2. 逐项证据

### 2.A I-001 · 双层语义命名与判定缺口

**结论：现行 canonical 不足以阻止三类混淆。**

| 概念 | 定义落点 | 判定谓词现状 |
|------|----------|--------------|
| 组合编排 | `principles.md:440`；`alignment.md:70`；`AGENTS.md:221`；`roadmap.md:10,12` | **无内容谓词**；只有「层=愿景」「非 progress%」与「不在此维护审计意见或 Goal finding」 |
| 纲领路线图 | `principles.md:441`；`alignment.md:72`；`AGENTS.md:222`；落点 `principles.md:47` | 有 P-001「要不要写」的谓词（`principles.md:62-74`），**无「某段文字属于哪一层」谓词** |
| 阶段计划 | `principles.md:442`；`alignment.md:73`；`AGENTS.md:223` | 仅「非树节点」可判；落点「多在 01-decision」是建议 |
| 意图（VP） | `principles.md:443,451`；`alignment.md:71`；`workspace-protocol.md:30` | **最完整**（`test_vision_protocol.py:78-103` 可执行）；但只有否命题，**未规定 VP 可否内含纲领阶段/路线图** |
| 子目标 | 仅见 `principles.md:388`、`alignment.md:96`、`AGENTS.md:205` | **三处命名表都没有该行，无判定谓词** |

主要缺口（文件:行 → 使能哪类混淆）：

| # | 证据 | 混淆 |
|---|------|------|
| 1 | `总路线图` 在 canonical **零出现**（全仓 12 处均在 workspace-002 目标记录内） | (a) 术语无指称 |
| 2 | `docs/vision/plans/VP-004-...md:75` `## 方向级路线图（纲领阶段 · 非 progress%）` | (a)(c) 愿景层出现与「纲领路线图」同名的工件 |
| 3 | `workspace-003/GOAL-001-.../00-meta.md:32` `## 纲领路线图（P-001 · 对齐 VP-004 R1–R3）`，与缺口 2 标签同为 R1–R3，R1–R4 又各落成子目标 | (a)(c) 同名同标签双层路线图，无法判定权威 |
| 4 | `docs/vision/plans/VP-002-...md:52` `## 消费面承接路线图`（实为移交/触发跟踪表） | (a)(c) VP 内第三种「路线图」 |
| 5 | 三处命名表（`principles.md:438-443`、`AGENTS.md:219-224`、`alignment.md:66-74`）缺「子目标」「VP 内阶段结构」行 | (b)(c) |
| 6 | 消费端安装的规则面 `skills/install/claude/AGENTS.md:208-218`、`skills/AGENTS.template.md:209-219`、copilot 说明 §6e **无命名消歧表** | (a)(b)(c) AI 第一入口全是裸词 |
| 7 | `docs/templates/goal-folder/00-meta.md`、`01-decision.md` **无纲领路线图/阶段计划槽位** | (a)(c) 各仓自创节名 |
| 8 | `docs/templates/workspace-context.md:47` 称「跨区纲领阶段」；`docs/vision/charter.md:71` 把「纲领阶段」划给愿景层 | (a)(c) 层归属相反 |
| 9 | `alignment.md:53` 要求 `vision/roadmap.md` 存在，但 `docs/templates/vision/` **无 roadmap 模板** | (a)(c) 消费仓自行发明列与节 |
| 10 | `docs/tests/test_vision_protocol.py:16-25,203-217` 仅判文件存在，**无内容断言** | (a)(b)(c) 无机器门禁 |
| 11 | `AGENTS.md:226` 结构选型缺「VP → 容器 = 工作区 + Root」一步；唯一否决是 `principles.md:484`（只管 VP 自身） | (b) |
| 12 | `alignment.md:90-98`、`principles.md:386-391` 无「VP 不得作 parent」正面禁止 | (b) |
| 13 | `principles.md:72` 的 P-001 谓词会把「愿景层要求分波次」判成必须先写纲领路线图，却不规定落哪一层 | (a) |

### 2.B I-002 · 愿景总路线图承载物与 VP 跟踪权威

**现状**：`docs/vision/roadmap.md`（36 行，7 列，4 行数据，对应 4 个 VP）= 唯一的「愿景总路线图」候选；其自述为「愿景规划索引（组合编排）」。

| 判断 | 事实 |
|------|------|
| 属组合编排 | 标题与定位声明（`:12-13`）、`id`、`detail` 链接、波次先后（`:22-29`）、`lead_workspace`（`principles.md:440` 列入组合编排） |
| 属 VP 跟踪（重复） | `status` / `vision_ref` / `title` / `workspace_count` 四列；波次括注中的状态与关门叙述；**`使用说明` 第 4 条「再更新本表 `status`」**（自带双写义务，`:36`） |
| 一致性 | 4/4 逐字段与 VP frontmatter 一致 ⇒ **可无损收敛** |
| 权威 | **canonical 未规定**；`roadmap.md:36` 要求维护本表 status，`skills/prompts/06-vision-orchestrator.md:193` 称「意图权威 = 已落盘 VP 文件」，无裁断句 |
| 已有漂移 | `docs/architecture/overview.md:70`（+镜像）与 `GOAL-001-main-vision/00-meta.md:50` 的组合编排摘要**均漏 VP-004** |
| 机读读取者 | **零**：`scripts/**`、`mcp/**`、`docs/contracts/**` 都不解析该表；`docs/tests/test_vision_protocol.py` 只判存在；fixture 甚至是 3 列（`fixtures/vision/valid-stack/roadmap.md:9-11`） |
| 文本读取者 | `skills/prompts/06:73,76,113,130,171`、`07:52`、`00:261-262`；`docs/standalone-bootstrap.md:104,113-120`（**整文件复制**）；`consumer-checklist.md:24`；`directory-layout.md:21`（+镜像）；`charter.md:71,83` |
| 消费侧风险 | `standalone-bootstrap.md:113-115` 整文件复制把生产仓 VP-001～VP-004 行带进消费仓；任何新增 MUST 文件会让存量仓瞬时「不完整安装」（`alignment.md:30,169`） |

### 2.C I-003 · 消费仓写入面、冲突面与共存模型

**写入面（消费仓）**：根 `AGENTS.md`、`docs/{README.md,architecture/**,templates/**,vision/{alignment.md,README.md}}`、`.claude|.grok|.agents/skills/{govern,audit,vision,vision-audit}/SKILL.md`、`.github/copilot-instructions.md`、`.github/prompts/*.prompt.md`、`$SKILLS_DIR/{prompts,templates,contracts}`；由 core 安装无条件触发（`skills/install.sh:643-644`、`skills/install.ps1:738-739`）。**覆盖策略**：同名即覆盖（prompt / `--force`）+ 目录合并不删；唯一拒绝覆盖的是 `--init-workspace` 的工作区目录（`install.sh:288-290`）。updater 以 `--all --non-interactive --force` 重跑安装器（`update.py:253-278`）。

**硬碰撞**：

| 路径 | 现状 | 证据 |
|------|------|------|
| 根 `AGENTS.md` | 框架整份占据；消费方改动 → updater fail closed；`--force-managed` 后无条件覆盖 ⇒ 消费方规则无合法存放位置 | `update.py:159,319-322,379` |
| `docs/README.md`、`docs/architecture/{principles,overview,directory-layout}.md` | 同名覆盖；异名文件保留 | `install.sh:387,193-214` |
| `docs/vision/`、整个 `docs/` | 治理根默认即 `docs`；命名空间被框架占用 | `alignment.md §0` |
| `.github/copilot-instructions.md` | 整份被框架规则覆盖 | `install.sh:613-614` |
| `./skills/`（bootstrap） | 有 `-Force` 时 `rm -rf` 整包 | `install-online.ps1:245`、`install-online.sh:249` |
| 大小写变体 | 代码层无归一；Windows/macOS 上 `Test-Path 'AGENTS.md'` 会命中 `agents.md` | `install.ps1:156`（仅用于 src==dest 判定） |

**共存候选 A～E**（不选优；S4 需用户裁决）：

| 模型 | 机制 | 迁移成本 | 主要失败模式 |
|------|------|----------|--------------|
| A. `AGENTS.md` 标记块合并 | 无文件写全份；有文件则替换受管段 | 已装仓可自动迁移（既有 MCP 通道 `mcp/lifecycle.py:25-29,86-115` 可复用） | 标记损坏/被删须 fail closed；File 与 MCP 两套合并逻辑需统一 |
| B. 命名空间子目录 + 根薄指针 | 框架规则放 `$SKILLS_DIR`/`{governance_root}/framework/`，根文件仅指针 | 已装仓需一次性拆文件 | 宿主只自动加载根 `AGENTS.md`，指针丢失即断链 |
| C. 可配置治理根 + 独立消费文档树 | 安装器读 `.goal-governance.json` | 缺省仍 `docs` ⇒ 已装仓零迁移 | 安装/更新层与 mcp 层易漂移；`docs/` 已被占用的仓仍需搬迁 |
| D. 安装时显式选择 | 新增 `--agents-mode` / `--docs-mode` | 需持久化并重放选择 | flag 与状态漂移；矩阵膨胀 |
| E. 不写根 `AGENTS.md` | 仅写宿主专属目录 | 需接管既有根文件 | 触碰 MUST「规则入口」行；治理摘要失去默认载体 |

**完整安装 MUST 覆盖差距**：安装器**不写** `vision/{charter,roadmap,revisions,reviews,workspaces,consumer-checklist}.md`、`vision/plans/VP-*`、`{governance_root}/contracts/`（契约实际落 `$SKILLS_DIR/contracts`）。这与「缺 Charter = 不完整安装」自洽，但 S4 必须显式说明。

**未实现清单**：①安装/更新不读 `.goal-governance.json`；②`{{GOVERNANCE_ROOT}}` 无安装期替换（消费端拿到字面占位符）；③无大小写碰撞处理；④无 `.gitignore` 写入；⑤无可写性预检/回滚；⑥不产出上列 MUST 文件；⑦File 通道无卸载；⑧updater 跳过点文件（`update.py:178`）；⑨managed-block 合并只在 MCP 通道。

### 2.D I-004 · `/commit` 命令形状、宿主覆盖与负例

**现状**：`/commit` **仅存在于 monorepo 自用** `.github/prompts/commit.prompt.md`；四个安装源目录均无 commit 壳 ⇒ 任何 `--claude/--grok/--codex/--copilot/--all` 安装都**不产出** `/commit`（未实现）。MCP 工具集不含 commit（`mcp/entries.py`）；契约 `hostEntrypoints` / `requiredEntrypoints` 仅四入口（`docs/contracts/skills-consumer-contract.json`）。

**先例 prompt 契约**（`.github/prompts/commit.prompt.md`）：先看 `git diff --cached --name-status`；非空则确认路径归属，可疑即停止报告；为空则仅在已明确 owned paths 时 `git add -- <owned paths>`，不得扩大；随后 `git diff --cached --check`；提交信息用中文 Conventional Commits（类型集合 `feat, fix, docs, style, refactor, test, chore`，≤50 字）；**禁止** `git add -A` / `git add .`；无改动不提交。

**与 checkpoint 的边界**：checkpoint 由编排器在长流程自动触发、写 `02-execution` 台账、用户可禁用、**非门禁证据**；`/commit` 由用户显式调用、非必需、缺它不使安装不完整、不得作 checkpoint 替代（`principles.md:129-136`；`D-002 §4`；VP-004 入口面）。

**未规定项（8 类）**：非 Git 仓库、验证范围、hook 拒绝/`--no-verify`、禁用/卸载语义、detached HEAD / mid-rebase、CRLF、push、以 commit 作放行依据。**已规定**：owned-path 越界、无改动不提交、无关路径停止报告、提交信息格式。

**S5 关键缺口**：契约层缺「默认安装但不入必达集」的表达位——现有 install 默认清单（`install.sh:618`、`install.ps1:706`）与契约必达字段同语义；`docs/tests/test_file_l1.py:101,110` 与 `skills/tests/test_skills_orchestrator.py:639,682` 是 D-002 §4 边界的机读守卫。

## 3. 证据路径表（claim → 位置）

| 主张 | 位置 |
|------|------|
| 三处命名表及其行数 | `docs/architecture/principles.md:438-443`；`AGENTS.md:219-224`；`docs/vision/alignment.md:66-74` |
| `总路线图` 零出现于 canonical | 全仓 grep：12 处，全部在 `workspace-002` 目标记录与本目标 meta 内 |
| 同名同标签双层路线图 | `docs/vision/plans/VP-004-mcp-file-dual-channel-delivery.md:75`；`docs/workspaces/workspace-003-mcp-file-dual-channel/GOAL-001-mcp-file-dual-channel-delivery/00-meta.md:32` |
| VP 内跟踪表式「路线图」 | `docs/vision/plans/VP-002-methodology-skills-feedback-evolution.md:52,56-59` |
| Charter/template 层归属相反 | `docs/vision/charter.md:71`；`docs/templates/workspace-context.md:47` |
| 目标模板无路线图槽位 | `docs/templates/goal-folder/00-meta.md:14-47`；`01-decision.md:13-27` |
| 无 roadmap 模板 | `docs/templates/vision/` 目录清单；`docs/templates/README.md:28-33` |
| roadmap MUST 且可极简 | `docs/vision/alignment.md:53` |
| 缺 MUST = 不完整安装 | `docs/vision/alignment.md:30,32,64,169` |
| roadmap 双写义务 | `docs/vision/roadmap.md:36` |
| 意图权威 = VP 文件 | `skills/prompts/06-vision-orchestrator.md:193` |
| roadmap 与 plans 一致性（唯一规范句） | `skills/prompts/06-vision-orchestrator.md:76` |
| 消费侧整文件复制 | `docs/standalone-bootstrap.md:104,113-120` |
| 机读只判存在 | `docs/tests/test_vision_protocol.py:16-25,203-217` |
| 消费端规则面无消歧表 | `skills/install/claude/AGENTS.md:208-218`；`skills/AGENTS.template.md:209-219`；`skills/install/copilot/copilot-instructions.md` |
| 安装写入面与覆盖策略 | `skills/install.sh:581-644,130-214`；`skills/install.ps1:664-739,127-247` |
| updater 托管集与冲突 | `skills/update.py:156-184,319-322,379`；`mcp/lifecycle.py:25-29,86-130` |
| MUST 表 | `docs/vision/alignment.md:40-62` |
| checkpoint 契约 | `docs/architecture/principles.md:129-136`；`skills/prompts/00-govern-orchestrator.md:226-232` |
| `/commit` 先例与守卫 | `.github/prompts/commit.prompt.md`；`skills/tests/test_skills_orchestrator.py:147-161` |
| 必达等式守卫（S5 约束） | `docs/tests/test_file_l1.py:51-70,101,110` |
| VP-004 入口面（commit 便利可选） | `docs/vision/plans/VP-004-mcp-file-dual-channel-delivery.md:41-47,95` |
| stage 白名单 | `AGENTS.md` §8c |

## 4. 残余不确定性

1. 盘点为**静态**核对，未执行安装/更新/宿主 probe；「AI 是否仍会混淆」需 S2 的 corpus 执行证据。
2. 消费宿主实际行为（大小写不敏感卷、只读目标、hooks）需 S4 在目标平台实测，本次仅登记为负例候选。
3. `workspace_count` 等自定义列在 canonical 无定义句；其去留属 S3 方案细节。
4. 「已支持消费宿主」当前可核对集合 = 三契约宿主（claude-code-cli / grok-build-cli / github-copilot-cli）；Codex 仅安装面、未进矩阵 committed，`/commit` 的宿主覆盖须在 S5 显式声明。
