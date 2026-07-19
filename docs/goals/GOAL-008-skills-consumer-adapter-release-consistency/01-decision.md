---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 1.1.0
---

# 决策记录 · GOAL-008

## 信息需求与阶段门禁

本表承接 [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19)；权威登记与当前状态见 [00-meta.md](00-meta.md)。

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|------------------|------|-------------|-------------|
| I-001 | required | 机读协议/模板版本、兼容声明的 canonical 位置、字段和演进语义 | 方案与发布范围冻结 | 方案冻结前 | 按 D-002 创建 canonical schema/manifest、同步分发镜像并以正反 fixtures、适配器契约测试验证 | verified | 已于方案审视复核 | [D-002](#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；29 项 Skills 契约测试与 3 项 core bootstrap 测试通过；见 [02-execution.md](02-execution.md) 与 [A-002](03-audit.md#a-002--i-001-契约实现与验证复审2026-07-19) |
| I-002 | required | 当前/上一协议版本需支持的宿主、wrapper、Web 解析器及 fixtures 边界 | 受影响实施与兼容验收 | 阶段 5 兼容验收前 | 建立矩阵、current/negative fixtures 与自动化重放；固定三宿主版本并为 `/govern`、`/audit` 分别取得可观察 dispatch | collecting | D-005：用户重启完整关门；责任人：项目维护者；无延期。首个基线 `previousSupportedProtocol: null` 只能以显式 N/A 与负例验证。 | [D-003](#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)、[D-005](#d-005--重启完整发布一致性关门路径2026-07-19)、[D-008](#d-008--候选运行时证据契约与宿主配置边界2026-07-19)；Claude/Grok 四个候选入口已验证，Copilot 两项与 Web CI replay 仍开放。 |
| I-003 | required | 发行物唯一身份及 CI 重放 canonical/mirror、报告、变更日志、tag/release 的方式 | 阶段 5 验收、F-005 关闭、阶段 7 输入 | 阶段 5 发布验收前 | 定义流水线产物，实施 CI 和发布演练，核对 tag/release 追溯 | collecting | D-005：用户重启完整关门；责任人：项目维护者；无延期。tag/release 操作须由维护者授权。 | [D-004](#d-004--当前最低可用基线与发布一致性延期2026-07-19)、[D-005](#d-005--重启完整发布一致性关门路径2026-07-19)；当前无 release tag |

## D-001 · 承接 D-010 的阶段 5 发布一致性边界（2026-07-19）

**状态**：accepted

> **历史立项状态**：本条中的 `collecting` 是立项当时状态；I-002、I-003 与 F-005 的当前状态和复核触发以 [D-004](#d-004--当前最低可用基线与发布一致性延期2026-07-19) 为准。

**依据**：用户明确要求按 [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19) 创建本目标；根目标 [A-008](../GOAL-001-main-vision/03-audit.md#a-008--合并响应-a-006--a-007-与阶段-5-立项门禁2026-07-19) 已确认该边界可执行，但保留开放 required 门禁。

**决定**：

1. 由本目标承接一个阶段 5 子目标的完整发布一致性范围：机读协议/模板版本与兼容声明、跨宿主/跨版本兼容矩阵、当前/上一版本 fixtures、可重复测试/报告、canonical/mirror 校验和可追溯发行证据。
2. Web 在本目标中只作为协议消费者参与只读解析与 fixture 验证；核心方法论、模板上游和三面最终发布验收不在本目标内。
3. I-001～I-003 保持 `required / collecting`，先完成信息收集和方案设计；未关闭项不得被写成已验证，也不得越过其影响的规划、实施、验收或关门门禁。

**为什么**：D-010 已将阶段 5 的独立依赖、证据和持续实施范围收敛为一个可审计子目标；单一目标能保持发布契约和证据链的一致，同时避免把 Web 功能、采用度试点或阶段 7 关门责任混入本范围。

**未选方案**：

- 为 I-001～I-003 机械创建三个信息子目标；这些信息共同服务同一发布契约，当前没有独立到需要拆分的范围或并行价值。
- 把 `collecting` 信息项或工作树内现有测试当作跨宿主/跨版本发布证据；这会绕过 D-010 的阶段门禁。
- 将 Web 写入、真实消费者采用度试点或阶段 7 三面最终验收纳入本目标 required 成功标准；D-010 已将它们留在其他阶段或后续试点。

## D-002 · I-001 单一机读版本声明契约（2026-07-19）

**状态**：accepted

**依据**：用户要求以公开行业实践确定 I-001；[调研附件](attachments/i-001-industry-practice-research-2026-07-19.md) 直接核对了 SemVer 2.0.0、JSON Schema Core 2020-12 与 JSON Schema Test Suite。

**决定**：

1. 以未来的 `docs/contracts/skills-consumer-contract.json` 作为唯一 canonical 声明，并以 `docs/contracts/skills-consumer-contract.schema.json` 验证；`skills/contracts/` 仅为其分发镜像，宿主安装产物不得另立版本/兼容真相。
2. 验证 schema 使用 JSON Schema 2020-12 的 `$schema`，并使用 canonical `$id` `https://github.com/magicvr/goal-governance/schema/skills-consumer-contract/v1`；普通 manifest 以 `contractSchemaId` 引用该身份。业务语义另用 `contractFormat`、`contractFormatVersion`、`canonical`、`protocol.version`、`protocol.versionPolicy`、`templateSet.version`、`templateSet.implementsProtocol` 和每个 adapter 的 `supportsProtocol` 表达；不把 `$schema`、`$id`、`contractSchemaId` 或任一现有文档 frontmatter 的 `version` 混作协议版本。
3. 协议和模板集均采用 SemVer：删除/重命名 required 字段、改变字段语义、required frontmatter 或已承诺宿主消费行为时升 MAJOR；可忽略的 optional 增量升 MINOR；不改变 public contract 的修复升 PATCH。`0.y.z` 不宣称稳定兼容，首个经 schema、fixtures 与适配器契约测试验证的稳定 public contract 才进入 `1.0.0`。
4. 适配器兼容区间采用语言无关的 `{ minInclusive, maxExclusive }` 结构；其含义等价于 SemVer 区间，但避免把某个宿主的 range 语法设为跨宿主协议。I-002 再填充实际矩阵与当前/上一版本 fixtures；I-003 再处理 digest、tag/release、CI 重放和 provenance。

**为什么**：SemVer 要求先定义 public API，并以兼容性决定版本升级；JSON Schema 将 dialect、schema 身份和业务版本清晰分层；官方测试套件强调通过按版本的有效/无效实例验证行为。该结构以 canonical docs 为唯一上游，同时为多宿主消费者保留可执行、可测试的边界。

**未选方案**：

- 把 `docs/README.md`、`skills/README.md` 或模板 frontmatter 的既有 `version` 选作唯一协议版本；这些值目前语义不同，无法表达 adapter 兼容边界。
- 让 Claude、Grok、Copilot 或 Web 各自保存 canonical manifest；会制造第二状态源和跨宿主漂移风险。
- 将发行物 digest、tag/release 或 provenance 纳入本决策的必填字段；这些属于 I-003 的发布证据范围，提前合并会混淆门禁。

**影响与后续（决定时）**：本决定回答了 I-001 的位置、字段和语义；实现和验证证据须另行记录，未有证据前 I-001 继续阻断方案与发布范围冻结。

**实施结果（2026-07-19）**：已在 `docs/contracts/` 创建 JSON Schema、canonical manifest 与正反 fixtures，并逐字节同步到 `skills/contracts/`；`-All/--all` 安装同时分发该镜像。29 项 Skills 契约测试、3 项 core bootstrap 测试与 Git Bash 的 `install.sh` 语法检查均通过。I-001 因此为 `verified`；具体复审见 [A-002](03-audit.md#a-002--i-001-契约实现与验证复审2026-07-19)。

## D-003 · I-002 首个支持基线与分层宿主范围（2026-07-19）

**状态**：accepted

**依据**：用户在 [A-003](03-audit.md#a-003--i-002-宿主兼容证据收集与阶段审视2026-07-19) / [A-004](03-audit.md#a-004--grok-build-仓库-skills-证据更正复核2026-07-19) 所要求的 P-004 裁决点作出书面决定；[I-002 证据附件](attachments/i-002-host-compatibility-evidence-2026-07-19.md) 已区分 source-level discovery、声明范围与实际运行时验证。

**决定**：

1. 协议 `0.1.0` 是首个支持基线，`previousSupportedProtocol` 明确为 `null`。不存在“上一版本” fixture，不伪造 `0.0.x`、文档 frontmatter 版本或其他历史工件。
2. `docs/contracts/skills-consumer-contract.json` 以 `supportBaseline` 和每 adapter 的 `supportCommitment` 记录此次边界：Claude Code CLI 与 GitHub Copilot VS Code 当前为 `committed`；Grok Build CLI 纳入 `declared` 支持范围。三者的 `verificationStatus` 继续是 `unverified`，直到有精确产品版本、环境、fixture 和实际调用输出。
3. adapter 对首个协议线采用 D-002 已确定的 `>=0.1.0 <0.2.0` 无宿主语法区间；本次将 schema/manifest format 从 `0.1.0` 演进到 `0.2.0`，该 format 版本与协议基线、核心包版本和 tag/release 身份各自独立。
4. Web 当前仅承担目标文档解析/浏览，不读取此 manifest，也不作为 adapter、声明支持或当前承诺的一行。未来可发展为完整闭环，但其范围不由本决定提前实现。核心文档/模板是可独立应用的方法论基础；Skills 与 Web 是彼此独立、均建立于核心文档之上的辅助闭环工具体系。

**为什么**：`0.1.0` 之前没有可追溯协议工件；把“无上一版本”显式写入契约可防止虚构跨版本覆盖。用户同时区分了已声明范围和当前支持承诺，故以独立字段保留 Grok Build 的已确认仓库 Skills 语义，又不把没有运行时证据的产品行为写成已验证。Web 的职责边界须独立记录，避免把目标文档解析能力误报为跨宿主适配器能力。

**未选方案**：

- 把 Grok Build 排除在声明范围之外；这与已核对的 xAI `.grok/skills/` 发现和 slash-command 资料及用户裁决相冲突。
- 将 Grok Build 标为当前 committed 支持，或将三类宿主标为 `verified`；缺少固定 release 的端到端运行证据，违反 I-002 的证据分层。
- 将 Web 写入/完整闭环、manifest 消费或 Skills 与 Web 的相互依赖纳入当前承诺；这些均超出当前只读解析器范围。
- 凭空生成上一协议版本 fixture；不存在可追溯前身，且会污染兼容矩阵。

**影响与后续（当时）**：D-003 关闭 I-002 中“首个/上一协议策略、声明/承诺范围和 Web 是否为 adapter”的范围冻结子问题，并授权同步 canonical schema/manifest、镜像、fixtures 与契约测试。I-002 当时仍为 `required / collecting`：其固定版本 current `/govern` 运行时证据已在后续执行中收集，但其余入口、自动化重放、完整矩阵与兼容验收仍须在门禁前完成；I-003、F-005 及发布证据不受本决定放行。当前延期状态以 D-004 为准。

## 门禁结论

- 允许本目标先进行 I-001～I-003 的信息收集、方案设计和必要的有界验证实验；实验范围外的实施仍受信息项门禁约束。
- I-002 的范围冻结已由 D-003 完成；其运行时兼容性、矩阵单元和验收证据仍未关闭，不得把 `declared` / `committed` 写成 `verified` 或通过兼容验收。
- I-003 与 `F-005` 未关闭前，不通过阶段 5 发布验收；`F-005` 也继续阻断阶段 7 三面发布验收和 GOAL-001 关门。
- `F-006` 是 `open / recommended`，不阻断本目标立项或其 required 范围推进，也不升级为本目标的 required 门禁。

本决策记录 D-010 的范围承接、D-002 的 I-001 设计取舍与 D-003 的 I-002 范围冻结；目标为 `active / 20%`。I-001 的 schema/manifest 与测试已实现并验证；D-003 的历史结论随后已由三宿主 `/govern` 运行时证据补充，当前发布一致性门禁状态以 D-004 为准。

## D-004 · 当前最低可用基线与发布一致性延期（2026-07-19）

**状态**：accepted

> **历史状态**：本条记录当时暂停完整发布一致性投入的有界裁决。该暂停已由 [D-005](#d-005--重启完整发布一致性关门路径2026-07-19) 在 2026-07-19 的后续用户指令中解除；历史最低可用证据仍有效，但不再决定当前工作顺序。

**确认来源**：用户在本对话核对当前证据后确认「同意」：当前以 Skills 能安装、能使用为足够范围，不在本目标继续投入完整发布一致性验收。

**决定**：

1. 当前可声明的交付是 `0.1.0` current `/govern` 的最低可用基线：canonical 契约与安装分发受测试覆盖，Claude Code `2.1.215`、Grok Build `0.2.103`、Copilot VS Code `1.129.1` / `copilot-chat 0.57.0` 均有版本固定的实际 dispatch 证据。
2. I-002、I-003 与上游 `F-005` 保持 `required`，但当前状态改为 `deferred`；这不是 residual risk 接受、不是 `verified`，也不放行阶段 5 发布验收、阶段 7 三面验收或 GOAL-001 关门。
3. I-002 在首次支持新的宿主/版本、或首次对外/可复现发布时复核；I-003 与 F-005 在首次对外/可复现发布时复核。责任人为项目维护者（本轮用户确认）。触发到来时，相关 `deferred required` 按开放 required 重新处理。

**为什么**：现有证据足以支撑当前三宿主 `/govern` 的有界可用主张，但不支撑 `/audit` 运行时、完整兼容矩阵、自动化重放、CI 或 release 主张。当前没有对外/可复现发布计划，提前建设完整发布证据会把高成本的未来发布工作误作当前使用的必要条件。

**未选方案**：

- 立即完成完整兼容矩阵、自动化重放、CI 与 tag/release：这些仍是有价值的发布一致性工作，但不满足当前使用的必要性。
- 将 I-002、I-003 或 F-005 改为 `non-blocking`、`verified` 或关闭：这会把尚未取得的发布证据伪装为事实。
- 接受无边界 residual risk 并将 GOAL-008 标为 `done`：用户没有接受 residual，且本目标的完整发布一致性成功标准仍未完成。

**影响与后续**：GOAL-008 保持 `active / 20%`，不关门；当前可以按最低可用范围使用 Skills。触发条件出现前不安排 I-002 / I-003 的进一步实现；触发后先复核台账和上游 F-005，再恢复相应的矩阵、自动化重放或发行证据工作。

## D-005 · 重启完整发布一致性关门路径（2026-07-19）

**状态**：accepted

**确认来源**：用户明确要求重启 GOAL-008，使用其机器当前的 Claude Code CLI、Grok Build CLI 与 VS Code 内置 GitHub Copilot 版本作为首个支持基线；并要求在 Skills 完整关门后才继续 Web 深化。

**决定**：

1. 解除 D-004 对完整发布一致性工作的暂停。I-002、I-003 与上游 F-005 从 `deferred required` 恢复为 `collecting / required`；不接受 residual risk，未取得的证据不得提前写成通过。
2. 本次候选发行物的宿主基线固定为 Claude Code CLI `2.1.215`、Grok Build CLI `0.2.103 (89c3d36fb6)`、VS Code `1.129.1` / commit `8a7abeba6e03ea3af87bfbce9a1b7e48fed567b8`，以及内置 GitHub Copilot Chat `0.57.0` build `1`。三者均为 `committed` 支持基线；版本、安装来源/哈希、环境与证据链接必须写入 canonical 兼容矩阵和发行证据。此承诺不替代 runtime、CI 或 release 验收。
3. I-002 的 required 矩阵覆盖三个宿主在协议 `0.1.0` 上的 `/govern` 与 `/audit`；Web 保持独立的只读目标文档解析消费者，不冒充 manifest adapter。每个矩阵单元需区分自动化、真实运行时、阻断和未覆盖状态。
4. `previousSupportedProtocol: null` 仍是首个支持基线的真实事实。完整关门以 current `0.1.0` fixture、无 predecessor 的显式 N/A 和“拒绝伪造 predecessor / 不支持协议”的负例为证据；不凭空生成 `0.0.x`。只有未来存在可追溯前一协议 artifact 后，才把 previous 纳入实际执行矩阵。
5. I-003 / F-005 以可重复 CI、canonical/mirror SHA-256 清单、兼容性报告、测试报告、变更日志、发行物身份和一次 annotated SemVer tag/release 或等价可追溯发布演练关闭。CI 和材料可由自动化生成；真实宿主运行、tag/release 授权及最终关门确认保留给用户/维护者。
6. 完成实现后，先写阶段 self 审计；对发布与关门证据建议再请求 independent 复审。所有 required finding 和信息项闭环后，才向用户请求 `done` 确认并同步目标树。

**为什么**：当前机器的版本已可作为明确、可重复的首个支持边界；将完整关门工作恢复到 GOAL-008 可保持既有 D-010 的范围，避免在尚未完成 Skills 发布一致性时推进 Web 深化或把最小可用证据误作发布证据。

**未选方案**：

- 继续沿用 D-004 的延期，并把三宿主 `/govern` 最低可用写成完整发布一致性：会绕过 I-002、I-003 与 F-005。
- 人为制造不存在的前一协议版本 fixture：与 D-003 的可追溯性约束冲突。
- 将 Web 写入、真实消费者采用度试点或阶段 7 最终验收混入本目标：超出 D-010 的边界。

**影响与后续**：本目标保持 `active / 20%`，先实现矩阵、fixtures、CI 与发行证据；随后再向用户索取 Claude、Grok、Copilot 的 `/govern` 与 `/audit` 真实运行时证据。GOAL-001 的阶段 6 Web 深化在 GOAL-008 完整关门前不启动。

## D-007 · Grok headless 测试的 provider/model 防漂移约定（2026-07-19）

**状态**：accepted

**确认来源**：用户要求修复未来测试调用 Grok Build 时出现 `unknown provider for model grok-build` 的误用路径。

**决定**：

1. 根目录 `AGENTS.md` 明确区分宿主适配器 ID 与 API provider/model：`grok-build-cli` 只表示适配器，不是 API model。
2. 当前本机 `GROK_MODELS_BASE_URL` endpoint 的 headless 测试 model 固定为 `grok-4.5`；未来重放命令必须显式传入 `--model grok-4.5`。若 endpoint 或可识别 model 改变，必须先同步规则、测试断言和实际环境证据。
3. `unknown provider`、模型相关 5xx 或无法核对实际 model 时，fixture 记为 `blocked`；不能用 CLI exit `0`、prompt 回显或交互式成功截图覆盖 headless 失败。
4. 用 `scripts/tests/test_grok_runtime_fixture.py` 对重放命令和规则做静态防漂移断言；保留历史 502 原文，不把历史失败改写成新配置的结果。

**为什么**：旧 fixture 没有显式 model，适配器标识 `grok-build` 被下游当成 API model，触发 `unknown provider`。把适配器身份与实际 model 分开，并在测试阶段拒绝错误命令，可以在再次调用 CLI 前暴露这类配置错误。

**未选方案**：

- 仅在历史 runtime fixture 中追加说明：不能约束未来新测试命令。
- 修改 `skills-consumer-contract.json`：该契约描述适配器兼容身份，不是运行时 provider/model 调用配置，混入会扩大契约职责。
- 直接把现有 502 记录改成 `grok-4.5` 的成功记录：会抹去真实历史，也没有新的 runtime 成功证据支持。

**影响与后续**：本次不改变 GOAL-008 的 `status`、`progress`、I-002/F-002 状态或 `goal-tree.md`。防漂移规则和静态测试已补齐；实际 Grok `/govern`、`/audit` 候选 runtime 兼容证据仍需按 I-002 另行取得。

## D-006 · 候选验证状态与发行身份分层（2026-07-19）

**状态**：accepted

**依据**：[A-010 F-004](03-audit.md#a-010--独立交叉审计当前状态执行事实与门禁2026-07-19) 指出 contract manifest 的历史 `verificationStatus: verified` 与候选 matrix 的 `pending-runtime-validation` 容易被误读；发行工具独立复核还发现 rehearsal 不应接受调用方注入的检查结果，且 compatibility report 必须与当前仓库状态完整一致。

**决定**：

1. 保留 contract manifest 的历史 `verificationStatus: verified`，但其语义严格限定为 A-007 已归档的固定版本 current `/govern` 子范围；不将其改写成当前候选全面通过。
2. 候选发行物的真实 readiness 只由 canonical compatibility matrix 的逐入口状态与重新生成报告的 `coverage` 判定。Skills README、matrix `evidenceScope` 与目标台账均显式说明这层区别。
3. matrix `candidateRevision` 只允许 `unreleased`、完整 Git commit 或 `v` 前缀 SemVer tag。`release-candidate` 模式要求其精确等于指向 HEAD 的 annotated tag，并将该值写入 release evidence。
4. `release_evidence.py` 的检查只允许内部执行，不接受调用方提供“已通过”记录；传入 compatibility report 必须与当前 HEAD 重新生成的 source、contract、matrix、mirror 和 coverage 全部一致。rehearsal 仍可记录失败事实，但不能靠伪造输入得到可信通过。

**为什么**：历史证据与候选发行证据服务不同时间范围。保留历史有界事实同时把候选 readiness 收敛到矩阵、coverage、HEAD、tag 和内部执行检查，可避免抹去真实历史，也避免发布工具或外部读者把它扩大为未经验证的全面兼容。

**未选方案**：

- 将 contract 三条 adapter 统一改回 `unverified`：会抹去 A-007 的真实历史子范围，且仍不能替代候选矩阵。
- 仅在 README 加一句说明而不收紧工具和 schema：无法防止 rehearsal 假阳性或 tag 与矩阵身份漂移。
- 允许自由文本 `candidateRevision`：不能建立候选发行物与 commit/tag 的可核对绑定。

**影响与后续**：D-006 关闭 A-010 F-004 的误读风险和本轮工具复核发现；不关闭 I-002、I-003、A-010 F-002/F-003 或 GOAL-001 F-005。矩阵当前仍为 `unreleased`，正式发布前须由维护者选择并授权版本/tag，再把两份镜像的 `candidateRevision` 同步为该 tag。

## D-008 · 候选运行时证据契约与宿主配置边界（2026-07-19）

**状态**：accepted

**依据**：A-010 F-002 要求候选发行物对三宿主 `/govern`、`/audit` 分别形成可观察证据；前序 headless 探测还暴露 Grok 主请求与辅助 session-title 请求必须分开判定、Claude stream-json 不应归档模型思考块或完整文件正文、长探针必须有有界超时。

**决定**：

1. `docs/contracts/runtime-evidence.schema.json` 是候选宿主运行时证据的 canonical schema，`skills/contracts/` 保存逐字节分发镜像。`scripts/capture_runtime_evidence.py` 负责执行探针并生成 JSON、stdout/stderr 摘要与可选截图索引。
2. 证据绑定实际宿主行为源、探针输入 SHA-256、命令/环境、退出码、marker、stdout/stderr SHA-256；不绑定最终 commit 或 matrix digest，以避免“写入证据又改变 commit/矩阵”的循环。任何 skill、wrapper、核心 prompt、根规则或探针输入变化都会使对应证据失效。
3. `runtime-verified` 单元必须引用有效 JSON；验证器须核对 schema、consumer/entrypoint/protocol 身份、`verdict: pass`、行为源新鲜度、stdout/stderr 摘要和截图路径。文件后缀、截图存在或调用方声明均不能替代这些检查。
4. 探针使用有界超时；超时写为 `blocked`，不无限等待。Claude Code 的 stream-json 仅保存初始化、工具调用、工具结果哈希/计数、可见文本和最终进程结果，剔除 thinking/signature 与完整工具结果正文；Grok 保留可诊断 stdout/stderr，但把本机 `Request URL` 值脱敏，并将辅助 session-title `grok-build` alias 的 502 与主 `grok-4.5` 调用分开记录。
5. 对 D-007 作范围修正：`grok-build-cli` 与具体 endpoint/model 的防误用规则属于本目标 runtime 证据附件和测试，不属于可分发的根级 `AGENTS.md`。根规则保持宿主无关；`scripts/tests/test_grok_runtime_fixture.py` 同时断言具体配置留在附件、未泄漏进根规则。

**为什么**：候选 release 需要可重复核验真实 dispatch，而不是 prompt 回显或历史截图。行为源/输出摘要能发现证据陈旧和内容篡改；脱敏 transcript 保留工具调用与最终 marker，又避免把模型私有思考和完整仓库正文当作发行物。

**未选方案**：

- 只在矩阵里放 screenshot 或自由文本状态：无法验证单元身份、来源新鲜度或输出摘要。
- 把 runtime evidence 绑定最终 commit/matrix digest：证据写入会改变被绑定对象，形成不可收敛循环。
- 将产品专用 endpoint/model 配置写入根 `AGENTS.md`：会污染可复制核心规则，并把本机环境误作通用协议。
- 保留 Claude 原始 verbose stream-json：其中含 thinking/signature 和大段工具结果，不适合作为仓库发布证据。

**影响与后续**：Claude Code 与 Grok Build 的 `/govern`、`/audit` 四个单元已按本契约进入 `runtime-verified`；Grok 证据保留辅助 502 警告。Copilot `/govern`、`/audit` 与 Web CI replay 仍为 3 个 uncovered 单元，所以 I-002、A-010 F-002、I-003、A-010 F-003 与 GOAL-001 F-005 均不关闭。
