---
id: A-001
goal: GOAL-009-info-deadlock-and-managed-placeholders
doc: audit-entry
record_id: A-001
source: independent
provider: local codex CLI / gpt-6.1-sol / reasoning effort high
scope: S2 规则区分与 S3 安装升级执行事实
verdict: fail
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-09-30
updated: 2026-09-30
version: 0.1.0
---

# A-001 · S2/S3 执行事实独立审计（2026-09-30）

> 编排器代贴。下面是独立会话的最后一条消息，verdict 与 findings 未改写。调用横幅为 model gpt-6.1-sol、reasoning effort high、sandbox read-only，退出码 0。

**verdict：fail。** S2 的规则区分成立；S3 的常规安装/升级路径与 D-004 基本一致，但整树渲染可能改写消费方自有文件和技能包源码，AGENTS 合并也未守住标记外字节不变的承诺。

- **source**：independent
- **auditor**：本地 codex CLI / gpt-6.1-sol / reasoning effort high
- **日期**：2026-09-30
- **audit_type**：execution-facts
- **scope**：workspace-002 / GOAL-009 的 S2、S3；不是关门审计。
- **基线**：HEAD 为 `693a4e6c33803c40c15fc4fd129a7fdeb305c938`，审计前后工作树均无 Git 状态变更。本轮未写文件、未提交、未修改目标状态或 goal-tree。

**成果（有证据的路径）**

- [原则 P-005](C:/Users/magicvr/Documents/Code/goal-governance/docs/architecture/principles.md:344)、[AGENTS 摘要](C:/Users/magicvr/Documents/Code/goal-governance/AGENTS.md:184)及[编排提示](C:/Users/magicvr/Documents/Code/goal-governance/skills/prompts/00-govern-orchestrator.md:225)同时保留两句规则：研究结果不成为进入自身工作的门禁；可预先独立核对的事实仍可设 required 门禁。
- [规则回归测试](C:/Users/magicvr/Documents/Code/goal-governance/skills/tests/test_skills_orchestrator.py:820)检查两侧规则、编排器 §3.5 和完成清单。本轮实际运行该测试，**1 项通过**。
- 本轮实际执行 `python -B scripts/stage_skills_mirrors.py --check`，**37 对一致，复制与删除均为 0**。
- [共享渲染模块](C:/Users/magicvr/Documents/Code/goal-governance/skills/render_managed.py)与[升级比较函数](C:/Users/magicvr/Documents/Code/goal-governance/skills/update.py:187)已实现指定目录渲染及原文/渲染双基线。
- 提交链与记录对应：`d1256eb` 为 S2 规则修改，`5ca9fd3` 回填 S2 hash；`a1730ba` 仅冻结方案及更新治理记录，不含安装器；`ecca659` 为安装/升级实现，`693a4e6` 回填 S3 hash。

**对照成功标准**

1. **S2 两侧规则：满足文本层验收。** 测试在限定章节内分别断言两句话，删除任一侧会失败。但 `blocks_entry` 是测试内按字符串定义的判断，不能证明宿主模型实际遵守规则；本轮没有宿主行为实测。

2. **用户书面选择与 D-004：基本一致。** 两个安装器增加方法论目录参数，并将两个目录输入传给共享渲染模块；AGENTS 使用临时渲染副本合并。用户拒绝不替换分支，因此无需补全截断句。边界实现存在 F-001、F-002。

3. **双基线判断：属于有依据的兼容读法，无需仅为此再次确认。** 修改前的 updater 本就接受与包内原文一致的受管文件；新代码保留该基线，再增加本次渲染结果，没有接受任意目录替换或任意差异。其余差异仍进入冲突列表。D-004 明确没有虚构第二次用户确认。本判断依据旧比较逻辑与新代码差异，并非因为 D-004 已标 accepted 就自动认可。F-001 必须处理，才能保证包内原文基线不会被安装过程污染。

4. **消费方目的地与源码隔离：未完全满足。** 常规分离目录下，渲染调用指向列出的消费方目的地；但递归整树没有受管文件清单或包源码排除。AGENTS 标记外字节也存在实际反例。

5. **安装后升级测试：接线真实，断言符合要求。** [测试辅助函数](C:/Users/magicvr/Documents/Code/goal-governance/scripts/tests/test_skills_update.py:267)通过 subprocess 调用仓库里的 `install.ps1` / `install.sh`，检查原则文件字节等于 `render_managed_bytes`，再执行离线 `update_package(dry_run=True)`；追加手改后要求抛出指定异常。期望字节没有写死。[冲突检查](C:/Users/magicvr/Documents/Code/goal-governance/skills/update.py:481)位于 dry-run 返回之前，因此 dry-run 仍检查冲突。本轮未运行这些会创建临时文件的测试，未独立复验 E-004 所述 25 项通过，也未实测自定义目录下的实际升级写入。

6. **I-001～I-004：状态含义与主要证据一致。** I-001、I-002 对应 S1 条文核对和占位符差异证据；I-003 的 verified 仅表示用户排除了不替换分支，不表示该分支已实测；I-004 仅表示 provider 已指定，不表示审计已完成。当前信息表有一处过时表述，见 F-003。

7. **发布与 progress：没有实质性冒充交付或放行。** meta、E-004、审计索引明确 S4 尚未完成、未发布、未关门；75% 可由 3/4 阶段重算，未被用作放行依据。E-003 的“已发布文本”措辞应修正，见 F-003。当前正式审计台账为空，本意见也不落盘，不能据此宣称 cross 审计闭环已完成。

**Findings**

**F-001｜严重度 high｜建议 required｜状态 open：整树渲染超出受管文件边界，且允许触及包源码。**

- **证据路径**：[递归渲染](C:/Users/magicvr/Documents/Code/goal-governance/skills/render_managed.py:77)、[PowerShell 调用](C:/Users/magicvr/Documents/Code/goal-governance/skills/install.ps1:314)、[Bash 调用](C:/Users/magicvr/Documents/Code/goal-governance/skills/install.sh:336)。
- `_render_tree` 递归处理所有非隐藏文件，没有按包映射限定受管目的地。消费方方法论目录里的自有笔记、目标台账，以及其他宿主已有的自定义 skill/prompt，只要含匹配占位符，就会被写回。
- 参数允许 `methodology` 与 `methodology/my-skills`。当包位于后者时，方法论整树渲染会包含包内 `core/docs/architecture/principles.md`、安装源及渲染程序自身，违背“不改技能包源码”的承诺。
- 本轮以内存探针核对：消费方笔记、目标 meta、嵌套包源码均被选中；未进行落盘复现。
- **建议修正**：按明确受管映射渲染，排除包源及消费方自有文件；无法保证隔离的路径组合在写入前 fail closed，并补相应反例覆盖。

**F-002｜严重度 med｜建议 required｜状态 open：AGENTS 标记外换行字节会被改写。**

- **证据路径**：[整份目标文本换行归一化](C:/Users/magicvr/Documents/Code/goal-governance/skills/agents_merge.py:178)、[文件读取与写入](C:/Users/magicvr/Documents/Code/goal-governance/skills/agents_merge.py:224)、[临时副本合并调用](C:/Users/magicvr/Documents/Code/goal-governance/skills/install.ps1:288)。
- `merge_agents_text` 对整个目标文本做 CRLF/CR→LF 转换；文件层又以 `read_text` 读取、LF 写回。受管块发生更新时，消费方标记外前后缀也随之改变。
- 本轮用真实包源、渲染源及内存中的 CRLF 前后缀调用该函数：合并发生，前后缀字节保留检查均为 **False**，前缀已变为 LF。
- 此问题位于既有共享 helper，但直接影响本次 S3 的明确承诺。本意见不重开其他工作区目标。
- **建议修正**：保留目标原始换行与标记外字节，仅替换受管区间；覆盖 CRLF、混合换行及末尾无换行场景。

**F-003｜严重度 low｜建议 recommended｜状态 open：当前记录保留过时或易误读措辞。**

- **证据路径**：[I-001 当前表述](C:/Users/magicvr/Documents/Code/goal-governance/docs/workspaces/workspace-002-methodology-skills-feedback/GOAL-009-info-deadlock-and-managed-placeholders/00-meta.md:56)、[E-003](C:/Users/magicvr/Documents/Code/goal-governance/docs/workspaces/workspace-002-methodology-skills-feedback/GOAL-009-info-deadlock-and-managed-placeholders/02-execution/E-003-rule-distinction.md:18)。
- I-001 仍写“原则正文尚未改”，与当前 D-003、代码及决策索引不一致；E-003 写“已发布文本”，而同条明确没有发布。
- **建议修正**：将前者限定为 S1 时点，将后者改为“已修改的规则文本”或“包内规则文本”。

**必改项汇总**

- F-001：限定渲染写集，保护消费方自有文件与技能包源码。
- F-002：保证 AGENTS 标记外原始字节不被改写。

**结论和下一步**

S2 可认可为文本层实现成立；S3 尚不能无条件认可其隔离与字节保留承诺。双基线本身不构成需要重新确认的静默决策。

F-001、F-002 必须由用户选择 **fixed、accepted-residual 或 user-overruled**，并形成可追踪记录；审计员不能代选。建议选择 fixed，修正后由 `/govern` 响应并安排复审。在必改项合法闭合前，不得据本意见宣称 S3 已通过审计或消费面可交付。