---
id: GOAL-003-consumer-governance-ergonomics
doc: decision
status: done
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-03
updated: 2026-08-04
version: 0.5.0
---

# 决策记录 · GOAL-003

## 目录决策索引

| D-ID | 日期 | 标题 | 状态 | 文件 |
|------|------|------|------|------|
| D-009 | 2026-08-04 | GOAL-003 关门并完成 Root R2 | accepted | [D-009-close-out.md](01-decision/D-009-close-out.md) |
| D-010 | 2026-08-04 | A-004 F-001 采用 fixed 与 v0.12.0 受控发布切片 | accepted | [D-010-fixed-v0-12-release.md](01-decision/D-010-fixed-v0-12-release.md) |
| D-011 | 2026-08-04 | v0.12.0 正式闭环并恢复 GOAL-003 关门 | accepted | [D-011-v0-12-f001-close-out.md](01-decision/D-011-v0-12-f001-close-out.md) |

> D-001～D-008 为切换前的 legacy inline 决策，继续有效且只读；新决策写入 `01-decision/D-NNN-*.md`。

## 信息需求与阶段门禁

信息项 I-001～I-007 以 [00-meta.md](00-meta.md) 为当前同源台账。它们均不阻断目标设立，但分别阻断 S2～S7 的方案冻结、实施或验收；未经验证不得把候选机制写成已选方案。

## D-001 · 将五项实战摩擦纳入同一 R2 大目标（2026-08-03）

**状态**：accepted

**触发**：用户 `$govern` 明确要求在 workspace-002 新建目标并解决 FB-001～FB-005

### 决定

1. 创建 **`GOAL-003-consumer-governance-ergonomics`**，父目标为 `GOAL-001-methodology-skills-feedback-evolution`，初始状态 `active`。
2. 将用户列出的五项问题作为已确认的真实项目反馈输入；这关闭 Root I-002 的“首批问题清单”缺口，但不证明问题根因、方案或实现已经验证。
3. 将它们放在一个 P-001 大目标内统一治理，因为共同影响消费仓边界与长流程体验，并横跨核心原则、模板、Skills 编排、契约、安装/更新和验证面。
4. 冻结问题边界与验收方向，不预先冻结以下实现选择：记录拆分阈值、审计风险算法、独立工具调度方式、Git 提交节点、Skills 更新协议。
5. required finding、意见冲突、residual / overruled 与信息冲突仍保留 P-004 用户责任；“减少反复询问”不得被实现为静默关闭必改项或静默接受风险。

### 为什么

- 五项均来自实际使用而非功能想象，直接服务 VP-002 与 Root R2。
- 其中至少五个可独立验收的交付块，且跨越协议、模板、编排、Git 与分发门禁，满足 P-001 必须先写路线图的条件。
- 先统一冻结角色、兼容和安全不变量，可避免各自局部修补后互相冲突。

### 未选方案

| 方案 | 未选理由 |
|------|----------|
| 要求每个消费仓手工删除 runtime evidence 门禁 | 把生产方责任转嫁给消费方，无法形成可复制产品行为 |
| 仅继续把长审计正文放入 `attachments/`，不定义拆分谓词 | 只能人工缓解，无法保证索引、迁移和其它多记录文件的一致行为 |
| 保留每次询问 self / independent 的固定流程 | 已被真实长流程证明产生显著摩擦；应以风险和阶段规则降低无价值交互 |
| 只在最终关门后提交 Git | 中间失败不可回溯，无法满足长任务恢复需求 |
| 每次通过完整 reinstall 更新 Skills | 已知体验问题未被解决，且缺少版本发现与回滚语义 |
| 立刻机械创建五个子目标 | S1 尚未冻结依赖、共享契约和验收矩阵；会制造编号与边界返工 |

## D-002 · 采用 S1 先行、S2～S6 可并行、S7 汇总的路线图（2026-08-03）

**决定**：

1. S1 先完成现状复现、职责边界、兼容基线和验收矩阵。
2. S2～S6 在各自 required 信息项关闭后可并行，不要求人为串行五个问题。
3. S7 统一完成迁移、回归、canonical→Skills 镜像与发布准备。
4. S1 后仅在某阶段具备独立范围、依赖、证据或并行价值时创建子目标；否则保留为目标内阶段计划。

**为什么**：共同基线先行可减少规则冲突；中段能力相对独立，允许并行；最终必须由统一兼容矩阵证明组合后仍可消费。

**未选方案**：边分析边直接修改 canonical 规则；它会在阈值、P-004、安全提交和更新信任模型未定时制造不可审计的既成事实。

## D-003 · producer / consumer 证据职责按安装 profile 分离（2026-08-04）

**决定**：

1. `skills-consumer-contract.json` 与其 schema 是消费安装必需的协议契约。
2. compatibility matrix、matrix schema、runtime-evidence schema、捕获脚本和 release evidence 属于 producer / release 验证面；可以进入生产仓发行检查，但不得成为消费仓目标推进门禁，也不随默认消费安装复制。
3. 生产仓继续对 adapter runtime、矩阵和 release 证据 fail closed；本修正不得以“消费仓不需要”为由削弱生产发布门禁。
4. 消费仓若主动参与适配器开发，可显式选择 producer profile；默认 profile 不要求用户删除任何门禁或文件。

**理由**：当前 `-All` 把整个 `skills/contracts/` 复制到消费仓，导致角色语义只靠人理解；按 allowlist 安装可以让责任边界成为可执行行为。

## D-004 · 三类 append-only 台账从第一条记录起使用平铺目录（2026-08-04）

**决定**：

1. 新目标仍保留 `01-decision.md`、`02-execution.md`、`03-audit.md` 作为稳定 frontmatter 与索引入口；同时创建同名无扩展目录 `01-decision/`、`02-execution/`、`03-audit/`。
2. 独立记录分别写为 `D-NNN-<slug>.md`、`E-NNN-<slug>.md`、`A-NNN-<slug>.md`，目录内只允许单层平铺；编号在目标内各台账单调不复用。
3. “多记录文件”按语义判定：允许追加两个或以上独立 D/E/A 记录的台账即属于多记录台账，不等待文件变大才采用目录。`00-meta.md` 不属于此类。
4. legacy inline 文件继续有效；兼容 reader 同时读取索引文件 inline 内容与目录文件。legacy 索引达到 **32 KiB、800 行、12 条独立记录任一条件**时，下一次追加前必须迁移或改写到目录；单条记录超过 32 KiB 时把证据正文放 `attachments/`，台账文件保留摘要与索引。
5. 迁移不重编号、不改语义；索引文件登记目录条目。迁移工具先 dry-run，验证解析等价后原子替换并保留 Git 可回溯点。

**未选方案**：只以字节阈值决定新目标何时拆分。它会让所有台账先经历一次可避免的重写，并让不同语言/格式在阈值附近产生不稳定行为。

## D-005 · 审计启动改为风险分级而非逐次询问（2026-08-04）

| 模式 | 适用范围 | 必需意见 |
|------|----------|----------|
| `none` | 低风险、可逆、无门禁语义变化的局部维护；允许由下一阶段或关门审计兜底 | 无阶段意见；仍需事实与验证 |
| `self` | 常规、边界清楚、可逆的非平凡实施或阶段验收 | 覆盖 scope 的 self |
| `independent` | 高影响但判定标准明确的 security / data / migration / production / release / compatibility 门禁 | 至少一个指定 provider 的 independent；self 非固定前置 |
| `cross` | 元规则、治理协议、不可逆或跨边界变更、证据矛盾，或用户要求多工具 | self + 至少一个指定 provider 的 independent；多 provider 各自保留意见 |

**决定**：

1. `/govern` 在实施前记录 scope、风险因子、模式和 provider 集；能由规则唯一判定时不询问用户。
2. 仅在 `independent` / `cross` 已被判定且用户未指定、会话无可用 provider 时，请用户指定工具；本目标已授权 Grok Build，无需重复询问。
3. provider 失败、超时或无可核对输出时不伪造 independent 意见；对应门禁保持未满足。
4. 删除“只要已有 independent 且无 self 就逐次询问是否自审”的固定交互。是否需要 self 由上表模式决定。
5. required finding、意见冲突、accepted-residual、user-overruled、信息冲突仍按 P-004 请求用户裁决；风险分级不得静默关闭责任决策。

## D-006 · 长流程默认创建安全 Git checkpoint（2026-08-04）

**决定**：

1. 长治理运行默认 `checkpoint_mode: auto`；用户可在任务开始时禁用。小型原子变更只需最终 checkpoint。
2. 合理节点是：方案/信息门禁冻结后、每个可独立验证的实现切片后、required finding 合法闭合后、关门前最终验证后。
3. 每次提交只允许显式列出的 owned paths；禁止 `git add -A`。若 owned path 含任务开始前的未提交改动或与无关改动不可分离，停止自动提交并报告，不擅自暂存或覆盖。
4. 验证失败、无实际 diff、commit 失败、非 Git 仓库均不宣称 checkpoint 成功；失败不改变治理门禁。成功后把 commit hash 和覆盖 scope 记入执行台账。
5. checkpoint 是恢复点，不是实现、审计或发布通过证据。

## D-007 · 提供包内事务型 Skills updater（2026-08-04）

**决定**：

1. Skills 包携带跨平台 updater，支持固定版本或 `latest` 发现、GitHub Release 在线源与 zip + `.sha256` 离线源。
2. updater 在写入前验证 SHA-256、zip 路径安全、包结构和协议兼容；协议 minor 边界变化默认 fail closed，需显式允许升级。
3. 更新前备份现有 Skills 包与会被 installer 管理的外部文件；新包安装或验证失败时自动恢复。成功后写安装状态（版本、协议、来源摘要、时间），保留可定位的回滚信息。
4. 已安装 managed 文件与当前包来源不同视为本地修改；默认停止并报告冲突，只有显式 force-managed 才覆盖。
5. 首次获得 updater 仍需安装包含该能力的新包；此后更新不再要求删除并完整重装。

## D-008 · 本目标不拆五个子目标（2026-08-04）

S1 证明五个切片共享同一协议版本、模板、installer、镜像与集成回归；在当前单人实现中拆子目标会增加跨目标 finding 与发布一致性成本。保留为 S2～S6 并行阶段，使用独立 checkpoint 隔离回溯。
