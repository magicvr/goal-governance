---
id: GOAL-001-main-vision
doc: decision
status: active
parent: null
created: 2026-07-18
updated: 2026-07-28
version: 0.3.0
---

# 决策记录 · GOAL-001

## D-001 · 采用「目标中心」而非「文档中心」

**决定**：以 Goal 为第一公民，围绕每个目标记录决策、执行与审计。

**为什么**：

- 传统文档仓库容易变成「写了就扔」，缺少目标牵引与闭环。
- 以目标聚合三类记录，更利于追踪「为什么做 / 做了什么 / 做得怎样」。
- 便于后续 Web 与 Skills 用同一数据模型读写。

## D-002 · 双交付：Web + Skills/提示词

> **历史状态**：`superseded`（2026-07-19）。本条保留当时的范围决策；当前交付层级由 D-007 重述，不删除历史。

**决定**：同时交付 Web 应用与 AI 协作规范（Skills / 提示词 / `AGENTS.md`）。

**为什么**：

- 仅靠 Web 难覆盖离线协作与 AI 辅助写作。
- 仅靠提示词缺少可视化与人机协作入口。
- 双交付可互为校验：文档规则驱动应用，应用实践反哺规则。

## D-003 · 扁平目标存储 + parent 字段

**决定**：`docs/goals/` 下所有目标平铺；层级只通过 `00-meta.md` 的 `parent` 维护，并在 `goal-tree.md` 展示。

**为什么**：

- 嵌套文件夹在移动/重命名/检索时成本高，也容易与编号冲突。
- 显式 `parent` 便于机器解析与校验。
- 单独的 `goal-tree.md` 给人读，给 AI 快速建立全局上下文。

## D-004 · GOAL-001 固定为总目标

**决定**：`GOAL-001` 永久为 Root Goal；新目标从 `GOAL-002` 起顺序编号。

**为什么**：

- 固定根节点降低协作歧义。
- 顺序编号便于审计与引用。

## D-005 · 高层路线图（分阶段推进）

> **历史状态**：本路线图由 D-007 重述为新的阶段 1～7 路线；以下内容保留当时的阶段事实，不作为当前路线图的唯一版本。

**决定**：总目标按五阶段推进（详见 [00-meta.md](00-meta.md)「高层路线图」）：

1. 项目初始化（GOAL-002，已完成）
2. Skills 完善与实践验证（GOAL-003，进行中）
3. 核心数据模型与 Goal 基础管理
4. Web 与文档体系联动
5. 高级能力与打磨（漂移检测、AI 辅助等）

**为什么**：

- 先稳住文档规则与 AI 协作，再做数据与 Web 联动，降低返工。
- 阶段 3 及以后仅作方向指引，待实践反馈后再正式拆分子目标，避免过早锁死范围。

**未选方案**：在根目标下一次性枚举全部细粒度子目标（会过早承诺、难随反馈调整）。

## D-006 · 采纳「目标可执行性与路线图」元规则

**决定**：将「不可直接执行的目标须先有高层路线图，再拆分子目标」上升为正式治理原则（P-001），并写入 `docs/architecture/principles.md`、根目录 `AGENTS.md` 与 `skills/AGENTS.template.md`，要求人与 AI 在处理较大目标时强制遵守。

**为什么**：

- D-005 的分阶段推进已证明：先路线图、后按阶段立项，比一次性枚举全部子目标更稳。
- 将实践固化为元规则，避免后续大目标再次「先拆细再后悔」。
- 统一文档原则、AI 强制规则与 Skills 模板，保证双交付两侧行为一致。

**未选方案**：仅在 GOAL-001 内部约定、不写入 AGENTS / principles（约束范围过窄，易被新目标忽略）。

## D-007 · 根目标重基线：三层交付、一个真相源（2026-07-19）

**状态**：partially superseded by D-014（Web 的“当前阶段只读”定位已由新的阶段 6 方向替代；三层交付与 `docs/goals/` 唯一真相源仍有效）

**决定**：将 GOAL-001 当前有效的交付模型重述为三层交付、一个真相源：

1. **核心方法论与文档协议**：生命周期、治理原则、五件套结构、写作约定和 canonical 模板；核心模板落在 `docs/templates/goal-folder/`。
2. **Skills**：面向 AI / Agent 在 Git 仓库中消费核心协议的编排、审计、原语、宿主适配与安装包；`skills/templates/goal-folder/` 保留为同步分发镜像。
3. **Web**：面向人的目标浏览与文档诊断工作台；当前阶段只读，从 `docs/goals/` 读取，不建立第二状态源。

三层共享 `docs/goals/` 的 Markdown 文档协议，但只有具体目标文档拥有运行时状态真相；Skills 与 Web 不得各自定义一套生命周期或数据模型。

**为什么**：

- 当前 `docs/README.md` 与架构已经把文档定义为 source of truth，并分别描述 Web 与 Skills 的不同职责；将核心方法论单独命名能反映真实依赖关系。
- Skills 包已经具备 `/govern`、`/audit`、原语、安装脚本和测试；Web 已具备只读目标工作台。继续称为“双交付”会把核心规范误当成背景而不是交付物。
- 核心模板需要能脱离 AI 宿主和 Web 使用；将 canonical 模板放在 `docs/templates/`，再由 Skills 携带分发镜像，可避免工具层成为规范唯一归属。

**未选方案**：

- **继续使用“双交付”**：无法表达文档/模板是独立核心，也会掩盖 Skills 与 Web 的消费关系。
- **把 Skills 或 Web 作为权威状态层**：会产生第二真相源，违反现有 Markdown 文档协议和 Web 只读边界。
- **本轮立即批量创建所有新子目标或开放 Web 写入**：范围尚未分别可执行，违反 P-001；先完成核心路线图与阶段门槛。

**影响**：

- 根目标保持 `active`；GOAL-002～005 的历史状态与审计记录不重写。
- 阶段 4 先承接核心方法论、文档协议和模板产品化；后续阶段再分别推进 Skills 对齐、Web 深化和三面发布验收。
- 相关入口文档、AGENTS 模板和 Skills 分发说明须同步三层模型；Web 第一阶段仍明确为只读。

## D-008 · 阶段 4 产品化与退出契约（2026-07-19）

**状态**：accepted

**决定**：阶段 4 只负责把既有核心方法论、文档协议与 canonical 模板整理为可独立复制、可验证、可版本化演进的核心交付包。它由一个后续子目标（从 `GOAL-006` 起）承接；本决策只使该子目标具备可立项边界，不声明阶段 4 已完成，也不自动启动立项。

### 最小交付包与 canonical 所有者

| 交付物 | canonical 所有者 | 阶段 4 完成时必须具备的事实 |
|------|-----------------|------------------------------|
| 核心使用说明与协议入口 | `docs/README.md`、`docs/architecture/`；根 `AGENTS.md` 是本仓库的 AI 执行约束 | 明确目标存储、五件套、路线图和审计闭环，并能从入口找到全部规范 |
| 可复制模板包 | `docs/templates/goal-folder/` | 五件套和 `attachments/` 起点完整；模板不依赖 Skills 或 Web 才能理解其结构 |
| 独立启用说明 | 核心文档层（以 `docs/README.md` 为入口） | 说明如何在空 Git 仓库复制核心包、建立 `docs/goals/goal-tree.md` 和第一个 Root Goal |
| Skills 模板分发镜像 | `skills/templates/goal-folder/`，仅为 `docs/templates/goal-folder/` 的派生镜像 | 仅在 canonical 模板变更后同步；不得从镜像反向定义核心协议 |

### 独立复制与使用场景

阶段 4 必须验证一个不安装 `skills/`、不启动 `web/` 的空 Git 仓库场景：复制 `AGENTS.md`、核心文档入口、`docs/architecture/` 与 `docs/templates/` 后，协作者能按说明建立 `docs/goals/goal-tree.md` 和一个符合五件套、`parent` 与编号规则的 Root Goal。验收记录须指出复制来源、生成路径和核对结果；该场景证明核心包可独立使用，而不是证明 Skills 或 Web 已发布。

### 版本与同步策略

1. 核心规则和模板的语义变更先落在 canonical 文档层；受影响文档刷新各自的 `updated` 与 `version`，并在核心入口记录本次可复制包的版本/变更范围。
2. `docs/templates/goal-folder/` 是模板唯一上游。修改模板后必须同步 `skills/templates/goal-folder/`，运行现有镜像一致性测试；镜像不得反向覆盖 canonical 内容。
3. Skills 安装产物、宿主包装和 Web 消费兼容性不属于阶段 4 的完成事实，分别留给阶段 5、阶段 6 与阶段 7 验收。

### 明确不做项

- 不在阶段 4 开放 Web 写入、创建/更新界面、独立数据库或写入同步。
- 不把 Skills 多宿主安装、发布或兼容性验收当作核心产品包已完成的替代证据。
- 不进行三层联合发布、跨面漂移检测或阶段 7 的发布验收。
- 不改变既有 P-001～P-004 的语义，除非另有可审计决策。

### 验收证据与阶段 4 → 5 门槛

后续 `GOAL-006` 必须在 `02-execution.md` 留下上述四类交付物的路径、独立复制场景的可复现证据、版本/镜像同步记录和验证结果；并在该目标的阶段审计中确认没有开放 required finding。只有在这些事实齐备、阶段 4 子目标按其关门条件完成后，才可创建或推进阶段 5 的 Skills 一致性工作。阶段 5 不得重新定义 canonical 协议或把未完成的核心产品化工作转移过去。

**为什么**：

- A-002 的 F-003 指出原路线图只有主题，没有可判断完成与退出的边界；上述契约把“产品化”从泛化口号转换为可验证工作包。
- 独立复制场景能检验核心方法论是否真的脱离工具层可用，同时避免把 Skills 镜像或 Web 页面误认作规范本身。
- 将单向模板同步和阶段边界写明，能避免阶段 5/7 承担阶段 4 的未完成工作。

**未选方案**：

- **立即创建多个阶段 4 子目标**：尚无按工作量拆分后的最小范围，且本次只需响应审计缺口；保留一个可执行的 `GOAL-006` 入口。
- **把 Skills 或 Web 的现有测试作为阶段 4 已完成证据**：它们只能佐证消费适配器或模板镜像，不能替代独立核心包的复制验收。

**影响**：

- F-003 的“先有可执行契约”要求已具备关闭证据；阶段 4 仍为 `active`，实际交付和关门证据待 `GOAL-006` 产生。
- 阶段 5 的启动门槛固定为阶段 4 完成后的证据与审计结论，不因本轮响应而提前放行。

## D-009 · 将信息就绪纳入核心闭环（2026-07-19）

**状态**：accepted

**确认来源**：用户在本对话于 2026-07-19 对本审计提出的协议修订方向回复「同意」。

**决定**：采纳根目标 A-004 的审计结论，在现有 P-001～P-004 之外新增 P-005「信息就绪与未知项门禁」，并以 `GOAL-007-information-readiness-governance` 承接规则、模板、Skills 和测试同步。

**为什么**：范围不明不等于信息不全。当前协议可延后细粒度拆分，却没有要求记录“需要验证什么、最晚何时需要、用何种证据关闭”。这会让目标质量审视把未知误当成既定边界，或只能在后续审计被动发现。

**未选方案**：

- 将每个未知自动拆成两个子目标：与 P-001 的按阶段拆分冲突，且会制造无价值的目标树噪音。
- 只在 Skills 内增加追问：核心文档、独立启用场景和审计仍会缺少同一规则。

**影响**：P-005 将先落在根 AGENTS、核心 principles、canonical 模板与分发镜像，再同步 Skills 编排/审计入口和契约测试。Web 结构化展示留待另一个有明确数据合同的目标。

## D-010 · P-004 自审裁决与阶段 5 发布一致性立项边界（2026-07-19）

**状态**：accepted

**确认来源**：用户在本对话于 2026-07-19 对 A-006 的 P-004 裁决回复「先自审，然后合并响应审计结果」。

**决定**：

1. 先以 [A-007](03-audit.md#a-007--goal-001007-组合战略与阶段-5-发布边界自审2026-07-19) 对 A-006 的同一 scope 做 `source: self` 自审，再由 A-008 合并 independent 与 self 两条意见；不把响应记录冒充自审。
2. 接受 A-006 / A-007 的共同判断：三层交付与 canonical 归属保持有效，未发现尚未治理的持续战略漂移；`F-005` 保持 `open / required`，`F-006` 保持 `open / recommended`。
3. 阶段 5 先由**一个**可执行子目标承接 Skills 消费适配器的跨宿主、跨版本发布一致性；当前下一编号为 `GOAL-008`，但本决策不创建或占用该编号。只有后续工作出现独立依赖、证据、持续时间或并行价值时，才继续拆分子目标。

### 阶段 5 纳入范围

- 定义一个不产生第二状态源的、可机读的协议/模板版本与兼容性声明，并明确版本演进与兼容判定语义。
- 建立 core docs / canonical 模板、Skills 安装产物及 Claude Code、Grok Build、GitHub Copilot 宿主 wrappers、Web 只读解析器之间的兼容矩阵；Web 在此只作为协议消费者参与 fixture 验证，不扩展产品功能。
- 建立当前版本与上一版本 fixtures、跨宿主安装/消费测试，以及可重复执行的兼容性报告。
- 建立 canonical/mirror 校验、测试报告、变更日志、发行物身份和可追溯 Git tag/release 证据；阶段 5 交付的是可复核的 Skills 发布契约与发行证据，不替代阶段 7 的三面最终发布验收。

### 明确排除

- 不重新定义 canonical 方法论、P-001～P-005 或模板上游；必要的核心协议语义变更须另行按治理流程留痕。
- 不开发 Web 写入、创建/更新界面、独立数据库或同步机制；Web 深化仍属阶段 6。
- 不承担三面联合发布、跨面漂移的最终验收或 GOAL-001 关门；这些仍属阶段 7 与根目标关门范围。
- 不把 A-006 / F-006 的真实消费者采用度试点设为阶段 5 required 成功标准；该项保留为后续独立试点或阶段 7 发布复盘的 recommended 证据。

### 信息需求与门禁（P-005；D-010 历史登记，当前状态以 D-011 为准）

| ID | 要回答的问题 / 所需信息 | 级别 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 责任、复核与当前证据 |
|---|---|---|---|---|---|---|---|
| I-001 | 哪个 canonical 位置和字段承载跨交付面的机读协议/模板版本与兼容声明；版本演进和兼容判定采用什么语义？ | required | 阶段 5 方案与发布范围冻结 | 阶段 5 方案冻结前 | 盘点现有 frontmatter / 核心包版本入口，形成单一声明契约并以 schema/契约测试验证 | collecting | GOAL-001 暂代责任；创建阶段 5 子目标时移交，并在其方案审视复核。A-006/A-007 已证明当前仅有文档版本与工作树说明，尚无跨适配器契约。 |
| I-002 | 哪些宿主/wrapper/Web 解析器版本必须支持当前与上一协议版本；兼容矩阵和 fixtures 的边界是什么？ | required | 阶段 5 受影响实施与兼容验收 | 支持范围在实施前冻结；fixture 证据在验收前完成 | 枚举三宿主安装面和 Web 只读解析合同，定义兼容矩阵、当前/上一版本 fixtures 与跨宿主测试 | collecting | GOAL-001 暂代责任；创建阶段 5 子目标时移交，并在实施前审视复核。现有测试主要证明同工作树模板镜像和当前 fixture 行为。 |
| I-003 | 发行物如何唯一标识，CI 如何重放 canonical/mirror、测试报告、变更日志与 tag/release 证据？ | required | 阶段 5 发布验收、F-005 关闭、阶段 7 输入 | 证据契约在方案冻结前定义；实际证据在阶段 5 验收前完成 | 定义发行物身份和流水线产物，实施 CI 与发布演练并核对可追溯 tag/release | collecting | GOAL-001 暂代责任；创建阶段 5 子目标时移交，并在阶段验收复核。`docs/README.md` 当前明确 `0.5.0` 尚无 release tag。 |

### 门禁解释

- 允许按上述边界创建阶段 5 子目标，并先做信息收集、方案设计和必要的验证实验；这不等于发布范围已经冻结。
- I-001 / I-002 未由证据关闭前，不冻结受影响的发布范围或进入相应实施；I-003 与 F-005 未关闭前，不通过阶段 5 发布验收，也不放行阶段 7 三面发布验收或 GOAL-001 关门。
- 本次没有接受残余风险，也没有把 `collecting` 写成 `verified`。

**为什么**：A-006 与 A-007 都确认现有字节一致性、安装冒烟和工作树内测试只能证明当前仓库内部一致，不能证明跨宿主、跨版本与发行物可重放。上述范围具有独立的兼容矩阵、CI/发行证据和实施周期，足以作为一个可审计子目标；同时把 Web 功能、采用度试点和最终三面发布留在各自阶段，可避免再次发生交付定义错位。

**未选方案**：

- 直接把现有 `0.5.0` 工作树和模板哈希台账视为已发布契约：缺少兼容声明、上一版本 fixtures 与 tag/release 证据。
- 将 Web 深化、真实采用度试点和阶段 7 最终发布一并塞入阶段 5：范围跨越多个独立交付与验收周期，不可直接执行。
- 为 I-001～I-003 各建一个信息子目标：三个信息项共同服务同一发布契约，当前没有足够独立依赖或并行价值，机械拆分会制造目标树噪音。

**影响**：GOAL-001 保持 `active`；阶段 5 在实际创建子目标前仍为“未开始”。本决策只确定下一次立项的边界和门禁，不修改 `status` / `progress` / `parent`，不需要同步 `goal-tree.md` 的树与状态表。

## D-011 · 当前最低可用基线与发布一致性延期（2026-07-19）

**状态**：accepted

**确认来源**：用户在本对话审视 GOAL-008 的现有证据后确认「同意」：当前以 Skills 能安装、能使用为足够范围，不继续为完整发布一致性投入工作。

**决定**：

1. 当前可声明的范围是三宿主固定版本的 `0.1.0` current `/govern` 最低可用：canonical 契约和安装分发有测试证据，Claude Code `2.1.215`、Grok Build `0.2.103`、Copilot VS Code `1.129.1` / `copilot-chat 0.57.0` 有实际调度证据。
2. I-002、I-003 与 `F-005` 均保留 `required`，当前改为 `deferred`；这不构成 residual risk 接受，不把 `/audit` 运行时、完整兼容矩阵、自动化重放、CI、tag/release 或阶段 5 发布验收写成已通过。
3. I-002 的复核触发为首次支持新的宿主/版本或首次对外/可复现发布；I-003 与 F-005 的复核触发为首次对外/可复现发布。责任人为项目维护者（本轮用户确认）。触发到来时，相关 `deferred required` 必须按开放 required 复核并阻断其受影响门禁。

### 当前信息项与门禁

| 项 | 级别 / 状态 | 当前结论 | 复核触发 |
|----|-------------|----------|----------|
| I-001 | required / verified | canonical schema/manifest、镜像与契约测试已关闭其门禁 | 无 |
| I-002 | required / deferred | 三宿主 current `/govern` 最低可用已证；完整兼容验收未完成 | 首次支持新宿主/版本或首次对外/可复现发布 |
| I-003 | required / deferred | 无 CI、发行物身份或 tag/release 证据；不进行当前发布验收 | 首次对外/可复现发布 |
| F-005 | open / required（deferred） | 未关闭；继续阻断阶段 5 发布验收、阶段 7 验收和根目标关门 | 首次对外/可复现发布 |

**为什么**：完整发布一致性工作服务于可复现发布和跨版本承诺，而当前有界使用只需要安装、契约分发和三宿主 `/govern` 可用。保留 required 与触发复核可避免把未来发布风险误报为已经验证，同时避免在没有发布计划时投入不必要的高成本工作。

**未选方案**：

- 立即完成矩阵、自动化重放、CI 和 tag/release：保留为触发后的发布一致性工作。
- 将 I-002、I-003 或 F-005 降为 `non-blocking`、标为 `verified` 或关闭：与现有证据不符。
- 以 residual risk 接受换取 GOAL-008 关门：用户未接受 residual，GOAL-008 仍保持 `active / 20%`。

**影响与后续**：D-010 保留为历史立项边界；当前状态由本条补充。GOAL-008 不关门，GOAL-001 保持 `active`。触发出现前不安排发布一致性工作；触发出现后先重新进入 `/govern GOAL-008`，再按 I-002、I-003 和 F-005 的门禁恢复相应工作。

## D-012 · 重启阶段 5 完整关门并将 Web 深化后置（2026-07-19）

**状态**：accepted

**确认来源**：用户明确要求先完成核心文档体系、再完整完成 Skills 体系；现要求重启 GOAL-008，并在 Skills 完整关门后才继续推进 Web 体系。

**决定**：

1. D-011 的延期是历史的有界投入取舍，现由本条在时间与优先级上取代；其“最低可用不等于发布验收”的证据边界继续有效。GOAL-008 D-005 负责恢复 I-002、I-003 与 F-005 的具体工作。
2. 阶段 5 的退出条件保持 D-010：可机读兼容声明、三宿主/安装产物/Web parser 的兼容矩阵、current/negative fixtures、可重复 CI/报告、发行物身份与可追溯 tag/release 证据；F-005 关闭后才可将 GOAL-008 标为 done。
3. 阶段 6 Web 人类工作台深化在 GOAL-008 正式 close-out 前不启动。现有 Web 只读基线不受影响，但不创建新的 Web 深化目标或将其工作混入阶段 5。
4. 当前机器版本是阶段 5 的候选基线：Claude Code `2.1.215`、Grok Build `0.2.103 (89c3d36fb6)`、VS Code `1.129.1` / built-in GitHub Copilot Chat `0.57.0` build `1`。真实宿主 runtime 与发布授权仍需维护者参与；自动化只能生成和核对证据，不能替代它们。

**为什么**：核心文档层已完成，现有最低可用 Skills 证据不足以证明可发布的跨宿主/跨版本一致性。按用户确认的顺序关闭阶段 5，可避免 Web 深化与未关闭发布门禁并行造成范围漂移。

**未选方案**：

- 维持延期并直接推进阶段 6：与用户明确的交付顺序冲突。
- 将最低可用 runtime 或 CI 绿灯单独视为 F-005 已关闭：缺少完整矩阵、发行物身份与 tag/release 证据。

**影响与后续**：GOAL-001 继续 `active`，阶段 5 保持当前焦点；本条不关闭 F-005、不改变 GOAL-008 progress，也不触发阶段 7 或根目标关门。

## D-013 · 阶段性整合 `dev` 到 `main` 并在验证后删除 `dev`（2026-07-20）

**状态**：accepted

**确认来源**：用户在本对话接受 `dev` 到 `main` 的分阶段 PR、合并与删除分支建议，并明确要求开始执行。

**决定**：

1. 从 `dev` 创建到 `main` 的 Pull Request，先完成 PR CI 和平台合并检查，再使用普通 merge commit 合入；不使用 squash 或 rebase merge。
2. 合并后必须等待并核对 `main` 上对应提交的 CI 成功，确认 `main` 已包含 `dev` 的提交链后，才删除远端与本地 `dev` 分支。
3. 本次整合仅收束已完成的阶段 5 发布一致性和其 close-out 记录；GOAL-001 保持 `active`，阶段 6/7 和 F-006 的后续范围不因分支整合而变更。

**为什么**：annotated `v0.7.0` 指向候选提交 `8a33ecd21d9183a680c9c0d63e471469f5e515a8`，该提交是当前 `dev` 的祖先。普通 merge 保留原提交图和 tag 的可追溯性；在 `main` CI 成功前保留 `dev` 也保留回退和诊断锚点。

**未选方案**：

- **直接推送 `dev` 内容到 `main`**：绕过 PR 的变更审阅与合并前 CI 观察。
- **squash 或 rebase merge**：会重写候选提交身份，使 tag、digest 和 release evidence 需要重新绑定。
- **在合并前或未验证 `main` CI 时删除 `dev`**：会失去尚未被 `main` 证实的恢复路径。

**影响与后续**：本决定不改变目标状态、进度、信息项或审计 finding，因此不更新 `goal-tree.md`。执行记录只在 PR 创建、合并、`main` CI 与分支删除实际发生后追加对应事实和链接。

## D-014 · 阶段 6 重定向为 AI 协助的人类目标治理工作台（2026-07-20）

**状态**：accepted

**确认来源**：用户明确指出“只读显然是毫无价值的”，并要求 GOAL-009 先规划供人类工作时有 AI 协助的 Web 形式目标治理工作台，再逐步实现；不将“完善的只读工具”误作产品目标。

**决定**：

1. 阶段 6 的目标是一个人类实际使用的目标治理工作台。人可在其中发现目标上下文、审视门禁与证据、与 AI 协作形成候选决策/计划/执行或审计响应，并对 AI 的建议进行编辑、拒绝或确认。
2. `docs/goals/` 继续是唯一 runtime truth source。Web 不是只读终点，但也不得拥有独立目标状态、生命周期或“AI 已认定完成”的第二真相；任何后续写入都必须将变更回写到 canonical 五件套和 `goal-tree.md`。
3. AI 只能提出可引用、可预览的候选动作。涉及创建/更新、状态/进度/parent 变化、P-004 裁决、required finding 关闭或 `done` 的动作，必须经过明确的人类确认，并保留输入快照、提案、diff、操作者、确认、事务结果和审计关联证据。
4. 创建 [GOAL-009-ai-assisted-governance-workbench](../GOAL-009-ai-assisted-governance-workbench/00-meta.md) 作为阶段 6 的产品定义与信息发现目标。它先确定产品形态、读模型、受控变更语义、AI/安全/部署门禁和高层路线图；不得因立项而自动开放 Web 写入、部署外部服务或批量创建实现子目标。

**为什么**：

- 单纯展示 Markdown 没有显著增加工作价值；目标治理的价值在于让人能够看清状态、做出决策、推动动作、审查证据并形成可追溯记录。
- `docs/goals/` 为真相源并不等于 Web 必须只读。正确的边界是“Web 不另立事实”，而不是“Web 不参与受控的事实变更”。
- 现有 `GoalsRepository` 已有五件套同步与可恢复写入基础，但缺少身份、确认、AI 提案溯源、并发和 Web 暴露契约；这些必须作为事实未定项规划，而不能被 UI 想象掩盖。

**未选方案**：

- **完善纯只读浏览器**：用户仍需回到 Markdown 或 Skills 才能推进工作，不能形成有价值的人机协作闭环。
- **立即开放自由文本编辑或 AI 自动写入**：缺少确认、P-004、身份、事务、审计与安全边界，会把方便性建立在不可审计的状态变更上。
- **为 Web 建立独立数据库/状态同步层**：会与 canonical 文档竞争真相，扩大一致性和恢复风险。

**影响与后续**：D-007 的三层模型和 canonical 归属保持有效，其“Web 当前阶段只读”产品定位由本条部分取代。D-010/D-012 对阶段 5 的历史排除与后置条件已完成，不被改写。本决策启动阶段 6 的规划，不冻结实现方案；每个 GOAL-009 required 信息项只阻断其明确影响的门禁，受控写入和部署分别须等待相关门禁关闭。

## D-015 · 阶段 6 有界结项审视（不关 Root；R-009-X 仍 accepted）（2026-07-22）

**状态**：accepted

**确认来源**：用户 `/govern 在 GOAL-001 记录阶段 6 有界结项审视（不关 Root；R-009-X 仍 accepted）`。

**决定**：

1. **记录阶段 6 有界结项**：阶段 6「AI 协助的人类目标治理 Web 工作台」在**有界交付**意义上完成，证据为 GOAL-009 有界关门 + GOAL-012～017 有界交付（α 详情/受控写、X-AI、N1、共享资料产品、路径试点证据）。  
2. **GOAL-001 保持 `status: active`**；**不**因本条标 `done`；**不**宣称 Root 或「一期 Web 产品终态」已关闭。  
3. **GOAL-009 residual R-009-X 仍 `accepted`**，继续约束：  
   - I-00N 扩展全文 verified（含 I-002/I-008/I-009/I-010 等）  
   - 人手 UX 全文（R-017-HUMAN-UX 等）  
   - AI 读资料全文（R-016-AI-READ 等）  
   - 浏览器/真联调全矩阵（R-014/015/016-E2E 等）  
   - **阶段 6 终态宣称**与无清单的 Root 终态审  
4. **阶段 7**（三面一致性、版本化与发布验收）与 **X-DEPLOY / residual 产品** 仍按需另立或触发，不在本条自动立项。  
5. 现时叙事以本条 + [00-meta 阶段 6 有界结项](00-meta.md) + [goal-tree.md](../goal-tree.md) 为准；历史「阶段 6 未开始」快照不得当作现时。

**为什么**：扫描显示 002～017 均 done、无 active 实现目标，但 R-009-X 与阶段 7 未关闭；有界结项可固定阶段 6 成果而不伪装终态。

**未选**：Root `done`；R-009-X closed；无 residual 清单的阶段 6 终态宣称。

**影响**：A-014；00-meta 现时节；02-execution；goal-tree 日志。GOAL-009 状态不变。

## D-016 · 核心协议逻辑一致性修订（finding 闭合 / 隐式工作区 / P-004 扩表）（2026-07-28）

**状态**：accepted

**确认来源**：用户要求「审视当前的核心协议是否存在逻辑问题」，随后确认「修改你所发现的问题」，并要求「在合适的地方记录本次修改操作」。

**决定**：

1. **采纳并落盘**对核心协议的一致性修订（不新立子目标、不重开已 `done` 的 GOAL-006/007/010；属 Root 层方法论维护）。
2. **Finding 合法闭合**（P-003）固定为三路径，与编排器/AGENTS 对齐：  
   - `fixed`：可核对修正  
   - `accepted-residual`：用户书面接受残余（范围、期限、复审触发）  
   - `user-overruled`：用户书面驳回/降级（**单条意见亦可**，不要求先有冲突）  
3. **P-004 扩表**：在「是否自审」「意见冲突」之外，正式包含单条 finding residual/overruled（4.3）与信息 residual/有界实验/信息冲突（4.4）。  
4. **隐式工作区**：无显式 `workspace-*/workspace.md` 时，**仅** `docs/goals/` legacy 可作隐式单工作区；否则空治理 scaffold，禁止猜测任意 `<workspace-root>`。  
5. **其它边界**：P-002 嵌入 P-001 路线图槽位；纲领阶段串行、阶段内可并行；`GOAL-*` 仅区内唯一、跨区须 `workspace_id`；Primary 三处冲突 fail closed；`active` VP 零工作区 14 日空转宽限；编号单调不复用 cancelled。  
6. **权威文件版本**（本轮）：`principles.md` **0.6.0**；`workspace-protocol.md` **0.4.0**；`alignment.md` **0.2.0**；`overview.md` **0.7.0**；根 `AGENTS.md` / Skills 模板 **0.9.1**；`00-govern-orchestrator` **0.8.1**。  
7. **不构成**：Root / 任一子目标 `done` 变更；R-009-X closed；新 release tag；runtime evidence 刷新义务自动免除（若后续发布含行为面，仍按 GOAL-008 惯例）。

**为什么**：

- 审视发现门禁「何为已解除」在 finding 维度分叉（原则只认修正，AGENTS/编排器已允许 residual），以及根 AGENTS 隐式工作区宽于 protocol，会导致编排器与规范各写各的。  
- 单条 required finding 无用户否决通道会造成可治理性死锁。  
- 串行/并行、Primary 冲突、VP 空转「长期」等边界糊会在多区与愿景层放大。

**未选方案**：

- **只改 AGENTS/提示词、不改正文 principles**：继续权威分叉。  
- **禁止 finding residual**：与 dogfood（如 R-009-X）及检查清单已有表述冲突，成本高。  
- **新开 GOAL-020 专做协议修订**：范围是元规则维护，挂 Root 决策更贴切；已关门 GOAL-010 仅追加交叉引用，不重开。

**影响与后续**：见 [02-execution 本轮事实](02-execution.md#2026-07-28--核心协议逻辑一致性修订d-016)；GOAL-010 执行追加交叉说明；`goal-tree` 日志；愿景 `revisions` editorial（alignment 0.2.0）。不改 Root `status`/`progress`。

## D-017 · P-006 愿景组合治理与级联对齐（第一刀）（2026-07-28）

**状态**：accepted

**确认来源**：用户就愿景审计、建愿景工具、路线图/开区/子目标方法论讨论后，逐项确认 D0–D24（含单愿景制、冷启动串行、取消 sandbox opt-out 等），并确认「开始」第一刀文档落盘。

**决定**：

1. 将 **P-006（愿景、组合治理与级联对齐）** 写入 `docs/architecture/principles.md`（**0.7.0**），含：单愿景制、冷启动 Charter→VP→工作区、对齐递归、总流程命名（组合编排 / 纲领路线图 / 阶段计划 / 意图=VP）、结构选型判定树、分层审视、strategic 宽阻断、工具分工与 v1 非目标。
2. **alignment.md 0.3.0** 为愿景门禁权威：取消 sandbox plan opt-out；`reviews.md`（`VRev-00N`）；lead 多区必填；完整安装必有 Charter。
3. 同步：`workspace-protocol` **0.6.0**、根 `AGENTS` **0.10.0**（§6d/6e）、vision README/checklist/roadmap/workspaces、模板 `docs/templates/vision/*` 与 workspace-context **0.4.0**、协议测试与 fixtures、`00-govern-orchestrator` **0.9.0**（S0 冷启动顺序；实现层门禁）。
4. **Skills `/vision` 为第二刀**（本轮不新建 skill 全文）；编排器在无 skill 时仍须按 P-006 引导补齐与 fail closed。
5. **不构成**：Root/`VP-001` 关门；R-009-X closed；多愿景；恢复 sandbox opt-out。

**为什么**：执行层 P-001～P-005 已闭环，但缺战略/组合层统一叙事时，人与 AI 在「何时改愿景 / 开区 / 拆子目标」上无法对齐；无强制 Charter 则对齐链无源头。

**未选**：多愿景；sandbox 免挂 VP；先工作区后补愿景；把 Vision Review 写入某 Root 的 `03-audit`；本轮一次做完 `/vision` skill 全文。

**影响**：见 [02-execution 本轮](02-execution.md#2026-07-28--p-006-愿景组合治理第一刀d-017)；愿景 `revisions`；`goal-tree` 日志。不改 Root `status`/`progress` 宣称。

## D-018 · Skills `/vision` 决策层第二刀（2026-07-28）

**状态**：accepted

**确认来源**：用户在 D-017 第一刀落盘后确认「做第二刀」。

**决定**：

1. 新增 **`skills/prompts/06-vision-orchestrator.md`**（决策层核心：V0–V6）。  
2. 默认 install 三入口：`/govern` + `/audit` + **`/vision`**（Claude/Grok skill + Copilot prompt）。  
3. 契约 `hostEntrypoints` / 矩阵 `requiredEntrypoints` 含 `vision`；矩阵 status = **`pending-runtime-validation`**（不伪造 runtime evidence）。  
4. 更新 skills README、AGENTS §9b、govern wrapper 交叉引用、隔离安装测试。  
5. **不构成**：`/vision` runtime-verified；Root 关门；发版 tag。

**为什么**：决策层与实现层分入口，避免 `/govern` 既开区又改 Charter；与 P-006 工具分工一致。

**未选**：仅文档不装 skill；把 vision 塞进 `/govern` 单一入口。

**影响**：[02-execution](02-execution.md#2026-07-28--skills-vision-第二刀d-018)；goal-tree 日志。

## D-019 · `/vision` follow-through（runtime + 消费面 + VRev；不发版）（2026-07-28）

**状态**：accepted

**确认来源**：目标「完成后继的全部工作（除了正式发版）」；计划 acceptance 1–5。

**决定**：

1. 扩展 `capture_runtime_evidence.py` 接受 `entrypoint=vision`；新增 claude/grok/copilot vision 探针 prompt。  
2. **Dual-pass** 捕获：Claude + Grok **pass** → 矩阵 vision=`runtime-verified`；Copilot **fail**（monthly quota）→ 保持 `pending-runtime-validation`，失败 JSON/stderr 与 scratch log 留痕，**不伪造** verified。  
3. 同步消费面：`skills/AGENTS.template.md`、`install/claude/AGENTS.md`、`install/copilot/copilot-instructions.md` 写入单愿景 / `/vision` vs `/govern` vs `/audit`。  
4. 补录 **VRev-001**（self，charter-init + stack coherence，verdict pass）。  
5. **明确非目标**：annotated tag、GitHub Release、`release_evidence --mode release`。

**为什么**：第二刀 skill 已装，但缺 runtime 证据、消费 AGENTS 叙事与 dogfood Review 则矩阵/install 仍撒谎。

**影响**：[02-execution](02-execution.md#2026-07-28--vision-follow-throughd-019)；GOAL-008 运行时附件；矩阵/README；**不发版**。

## D-020 · 响应 V-F-001：独立 Vision Review 专用入口（2026-07-28）

**状态**：accepted

**确认来源**：用户在 `/vision` 对 `V-F-001` 的 P-004 裁决中选择“新增 `/vision-audit`”，而非扩展 Goal `/audit` 的 scope 路由。

**决定**：

1. 新增 `07-independent-vision-review.md` 与默认 `/vision-audit` 入口：只写 `docs/vision/reviews.md`（`source: independent` / `VRev-00N`），不改 Charter、VP、Goal 或 Goal `03-audit.md`。
2. 保持 `/audit` 为 Goal 独立审计；`/vision` 负责 self Review、愿景决策与 Vision finding 响应。三个边界均在 core prompts、Claude/Grok/Copilot 安装入口与消费者说明中明确。
3. 将 `vision-audit` 加入消费契约和默认安装面；当前候选标记为 `unreleased`，该入口三宿主均 `pending-runtime-validation`，不将结构测试写成 runtime evidence。
4. 以 `VRev-002` 响应节记录 `V-F-001: fixed`；不创建 Goal 五件套，不改 Root 或子目标 status/progress，不发版。

**为什么**：专用入口保持 Vision Review 与 Goal Audit 的台账、响应方和门禁边界可执行且无歧义；按 scope 扩展 `/audit` 会把既有 Goal 审计契约变为隐式路由。

**未选**：扩展 `/audit` 按 scope 写入 `reviews.md`；接受 residual 或 overrule 该 required finding。

**影响**：实施事实与验证见 [02-execution.md](02-execution.md#2026-07-28--响应-v-f-001独立-vision-review-专用入口d-020不发版)；正式闭合见 [VRev-002](../../../vision/reviews.md#响应--v-f-0012026-07-28)。