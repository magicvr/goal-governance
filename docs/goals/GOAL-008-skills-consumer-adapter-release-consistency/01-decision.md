---
id: GOAL-008-skills-consumer-adapter-release-consistency
doc: decision
status: active
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.4.0
---

# 决策记录 · GOAL-008

## 信息需求与阶段门禁

本表承接 [GOAL-001 D-010](../GOAL-001-main-vision/01-decision.md#d-010--p-004-自审裁决与阶段-5-发布一致性立项边界2026-07-19)；权威登记与当前状态见 [00-meta.md](00-meta.md)。

| ID | 级别 | 所需信息 / 假设 | 影响门禁 | 最晚需要阶段 | 验证 / 收集动作 | 状态 | 延期 / 复核 | 证据 / 结论 |
|----|------|-----------------|----------|--------------|------------------|------|-------------|-------------|
| I-001 | required | 机读协议/模板版本、兼容声明的 canonical 位置、字段和演进语义 | 方案与发布范围冻结 | 方案冻结前 | 按 D-002 创建 canonical schema/manifest、同步分发镜像并以正反 fixtures、适配器契约测试验证 | verified | 已于方案审视复核 | [D-002](#d-002--i-001-单一机读版本声明契约2026-07-19)；`docs/contracts/`、`skills/contracts/`；29 项 Skills 契约测试与 3 项 core bootstrap 测试通过；见 [02-execution.md](02-execution.md) 与 [A-002](03-audit.md#a-002--i-001-契约实现与验证复审2026-07-19) |
| I-002 | required | 当前/上一协议版本需支持的宿主、wrapper、Web 解析器及 fixtures 边界 | 受影响实施与兼容验收 | 实施前冻结支持范围；验收前完成 fixtures | 按 D-003 固化 `0.1.0` 首个基线、无上一版本、adapter 层级和 Web 边界；再以精确 host release、fixture 与实际调用完成验证 | collecting | 实施前、验收前复核 | [D-003](#d-003--i-002-首个支持基线与分层宿主范围2026-07-19)；canonical manifest 已为 Claude Code CLI / GitHub Copilot VS Code 记录 `committed`，为 Grok Build CLI 记录 `declared`，三者均 `unverified`；30 项 Skills 契约测试与 3 项 standalone bootstrap 测试通过 |
| I-003 | required | 发行物唯一身份及 CI 重放 canonical/mirror、报告、变更日志、tag/release 的方式 | 阶段 5 验收、F-005 关闭、阶段 7 输入 | 方案冻结前定义契约；验收前形成实际证据 | 定义流水线产物，实施 CI 和发布演练，核对 tag/release 追溯 | collecting | 方案冻结、阶段验收复核 | D-010；当前无 release tag |

## D-001 · 承接 D-010 的阶段 5 发布一致性边界（2026-07-19）

**状态**：accepted

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

**影响与后续**：D-003 关闭 I-002 中“首个/上一协议策略、声明/承诺范围和 Web 是否为 adapter”的范围冻结子问题，并授权同步 canonical schema/manifest、镜像、fixtures 与契约测试。I-002 整体仍为 `required / collecting`：具体 Claude Code / Grok Build / Copilot VS Code release、运行环境与 actual runtime fixture 仍须在兼容验收前收集；I-003、F-005 及发布证据不受本决定放行。

## 门禁结论

- 允许本目标先进行 I-001～I-003 的信息收集、方案设计和必要的有界验证实验；实验范围外的实施仍受信息项门禁约束。
- I-002 的范围冻结已由 D-003 完成；其运行时兼容性、矩阵单元和验收证据仍未关闭，不得把 `declared` / `committed` 写成 `verified` 或通过兼容验收。
- I-003 与 `F-005` 未关闭前，不通过阶段 5 发布验收；`F-005` 也继续阻断阶段 7 三面发布验收和 GOAL-001 关门。
- `F-006` 是 `open / recommended`，不阻断本目标立项或其 required 范围推进，也不升级为本目标的 required 门禁。

本决策记录 D-010 的范围承接、D-002 的 I-001 设计取舍与 D-003 的 I-002 范围冻结；目标为 `active / 20%`。I-001 的 schema/manifest 与测试已实现并验证；D-003 已冻结 I-002 的声明/承诺边界，但尚未取得宿主运行时验证或 I-003 发布证据。
