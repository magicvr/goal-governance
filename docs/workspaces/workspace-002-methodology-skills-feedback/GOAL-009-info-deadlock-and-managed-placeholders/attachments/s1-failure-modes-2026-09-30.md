---
title: S1 失败模式证据 · 死锁措辞与受管占位符
status: recorded
parent: GOAL-009-info-deadlock-and-managed-placeholders
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# S1 · 失败模式证据（2026-09-30）

本附件只记录核对结果。原则正文、AGENTS、编排提示、安装器和 update 脚本都还没有改。

## 1. FB-010 · 哪些句子把「调查的结果」写成进入调查的门禁

这些句子都不区分两种事实：只有做完该项工作才存在的结论，以及该项工作开始前已经可以核对的事实。编排器允许把「收集信息」当作下一步，但没有写明前一种事实不得成为进入该项工作的 required 门禁。

### 原则全文（权威）

`docs/architecture/principles.md` P-005「设立与阶段门禁」：

- 第 341 行，规划门禁：影响范围、验收、资源、安全、合规或关键依赖的 required 信息，在方案冻结或承诺不可逆实施前必须验证。尚未验证时，允许规划「如何收集信息」，不允许把未经验证的假设当成实施承诺。
- 第 342–343 行，实施门禁：实施受某一 required 信息项影响的范围前，该项必须有证据。有界实验只能进入明确的信息收集范围，信息项保持 `collecting`。
- 第 344 行，关门门禁：影响成功标准、验收或风险主张的 required 信息项未闭环时，不得标 `done`。

镜像 `skills/core/docs/architecture/principles.md` 目前是同一段落、同一行号。本阶段没有改它。

有界实验条款只允许进入「信息收集范围」，并且不解除门禁。它没有说：若某个 required 项的答案就是这项工作本身的结果，则该项不得挡住这项工作。

### 操作摘要里的同一句

下面四处是同一句「阶段门禁」：影响方案冻结、实施、验收或关门的 required 信息项，必须在对应阶段前由证据关闭；唯一写明能解除明确门禁的例外是用户书面接受的残余风险。

| 文件 | 行 |
|------|----|
| `AGENTS.md` | 183 |
| `skills/AGENTS.template.md` | 182 |
| `skills/install/claude/AGENTS.md` | 181 |
| `skills/install/copilot/copilot-instructions.md` | 181 |
| `.github/copilot-instructions.md` | 175 |

完成清单把同一要求再写了一次：「本次要推进的阶段没有开放 required 信息门禁」。`.github/copilot-instructions.md` 没有这句原文。

| 文件 | 行 |
|------|----|
| `AGENTS.md` | 374 |
| `skills/AGENTS.template.md` | 337 |
| `skills/install/claude/AGENTS.md` | 336 |
| `skills/install/copilot/copilot-instructions.md` | 336 |

相邻硬约束「不得以以后再说绕过 required 信息门禁」在 `AGENTS.md:357`、`skills/AGENTS.template.md:323`、`skills/install/claude/AGENTS.md:322`、`skills/install/copilot/copilot-instructions.md:322`。这句本身不是死锁；S2 改门禁时不能把它改成可以跳过真正的前置事实。

### 编排提示

`skills/prompts/00-govern-orchestrator.md`：

- 第 75 行：开放的 required 信息项只阻断其影响的阶段；允许把收集信息作为下一步。这里仍没有「结果只有做完才存在」的例外。
- 第 217–224 行，§3.5：提议规划冻结、实施、验收或关门前，required 须已 verified，或已有书面 residual。到期则停止放行。
- 第 338 行，完成标准：未跨越到期 required 信息门禁。

该文件里以「- 禁止」开头的条目已有上限，S2 增补要用肯定句，不能再加一条这样的禁止项。

### 两条反例（S2 要同时保住）

**研究结论死锁反例。** 一个研究目标把「这项调查会得出什么结论」登记为 required，最晚阶段写成「调查开始前」。按上面的实施门禁和阶段门禁，进入调查就要先有这条结论的证据。结论要做完调查才存在。修订后的规则不得挡住这个反例。

**先于执行的事实。** 一个发布实施目标需要目标环境的版本号，而这个版本在发布实施开始前已经可以查询。这种事实仍然可以是进入该发布实施的 required 门禁。执行场景里已经存在的凭据、或用户已经书面指定的审计 provider，同样属于这一类。

## 2. FB-011 · 指定目录与占位符替换

### 负结果：今天不能同时用安装参数指定两个目录

2026-09-30 读安装脚本并做字符串核对（见下节复现输出）：

| 检查 | 结果 | 位置 |
|------|------|------|
| `skills/install.sh` 有 `--skills-dir` | 有，默认 `./skills` | 第 95 行 |
| `skills/install.sh` 有 `--docs-dir` 或 `--methodology-dir` | 没有 | 全文无这两个参数 |
| 方法论目录写死 | `ALWAYS installs package core/docs → ./docs/` | `install.sh` 第 109 行；安装时打印在第 452 行 |
| `skills/install.ps1` 有 `-DocsDir` | 没有 | 全文无此参数 |
| PowerShell 同样写死到 `.\docs\` | 是 | 第 98 行说明，第 372–376 行复制 |

`install.sh` 与 `install.ps1` 全文都没有 `GOVERNANCE_ROOT`。安装器不替换占位符。

### 正结果：替换受管占位符会被升级当成本地改动

比较函数是仓库里的 `skills/update.py`，不是另写的一份判断。

- 根 `AGENTS.md` 不是整文件托管（`managed_file_pairs`，约第 172–174 行）。`agents_managed_conflict`（第 203–235 行）只在受管块相对包内 `install/claude/AGENTS.md` 有改动时，把该文件算进冲突。
- `docs/architecture/**` 是整文件 sha256 比较。来源根是包内 `core/docs/architecture`，目标是消费仓 `docs/architecture`（第 181–186 行）。
- `update_package` 在上述列表非空、且没有 `--force-managed` 时抛出 `managed files have local changes`（第 390–393 行）。

复现没有调用 `update_package`：它会下载 GitHub Release。调用的是它用来决定是否抛错的 `modified_managed_files`。

做法：临时消费目录中复制 `skills/`；把 `install/claude/AGENTS.md` 里的 `{{GOVERNANCE_ROOT}}`、`{{SKILLS_DIR}}`、`{{CORE_TEMPLATES_DIR}}` 分别换成 `methodology`、`my-skills`、`methodology/templates`，写到消费仓根 `AGENTS.md`；把包内 `core/docs/architecture/principles.md` 的 `{governance_root}` 换成 `methodology`，写到 `docs/architecture/principles.md`。对照是把这两个文件改回与包内源一致后再查一次。

输出（退出码 0）：

```text
install.sh has --skills-dir: True
install.sh has --docs-dir: False
install.sh has --methodology-dir: False
install.ps1 has -DocsDir: False
methodology hardcoded to ./docs/: True
template == install/claude/AGENTS.md: False
template says unsubstituted means docs: True
modified count: 2
listed AGENTS.md: True
listed docs/architecture/principles.md: True
control lists AGENTS.md: False
control lists principles: False
control modified count: 0
```

替换后列出的就是这两个路径。字节与包内源一致时一个都不列出。因此「占位符已被替换」本身就会让升级的受管文件检查失败。

### 不替换时路径怎么读（I-003 的前半，不是策略）

只有 `skills/AGENTS.template.md` 第 15 行写了：`{{GOVERNANCE_ROOT}}` 不替换则按默认 `docs` 理解。`skills/install/claude/AGENTS.md` 与这份模板不是同一份文件（模板 0.13.0，安装副本 0.12.0），安装副本没有这句话。

所以：治理根不是 `docs` 时，留下未替换的 `{{GOVERNANCE_ROOT}}`，按模板自己的定义会把 AI 指到 `docs`。`{{SKILLS_DIR}}` 没有对应的「不替换则用某目录」定义，留下字面占位符就不会指向真实 skills 目录。

这只说明「不替换」在自定义目录下和模板定义相撞。用户原话在「尤其是让ai从」处截断，不替换这一支仍不能冻结。

## 3. 本附件没有决定的事

- 没有选定安装/升级对占位符的策略，也没有新增方法论目录参数。
- 没有开始 cross 审计。provider 的指定见 D-002，审计仍未跑。
- 没有另开子目标。
