---
id: GOAL-006-core-methodology-template-productization
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-19
updated: 2026-07-19
version: 0.4.0
---

# 决策记录 · GOAL-006

## D-001 · 以 GOAL-001 D-008 作为阶段 4 的唯一交付边界

**决定**：

本目标严格承接 [GOAL-001 D-008](../GOAL-001-main-vision/01-decision.md#d-008--阶段-4-产品化与退出契约2026-07-19) 定义的最小交付包、独立复制场景、版本与镜像同步策略、非目标及阶段 4 → 5 门槛；本轮只建立目标与范围，不声明任何实际交付已经完成。

**为什么**：

- 用户明确要求以 GOAL-006 承接 D-008 的阶段 4 最小交付包。
- D-008 已提供可执行边界，避免把“产品化”重新解释为任意的文档整理、Skills 发布或 Web 开发。
- 将阶段 5～7 的工作排除在本目标外，才能让后续放行建立在可核对的阶段 4 事实之上。

**未选方案**：

- **在本目标并入 Skills 发布或 Web 写入**：这些属于 D-008 明确留给阶段 5、阶段 6 或阶段 7 的工作。
- **只创建占位目标、不写成功标准与验收边界**：会重新引入 A-002 / F-003 已关闭的范围歧义。

## D-002 · 将独立启用说明与验证放在核心文档层

**日期**：2026-07-19
**状态**：accepted

**决定**：新增 `docs/standalone-bootstrap.md`，由 `docs/README.md` 作为入口链接；新增 `docs/tests/test_standalone_bootstrap.py`，在临时空 Git 仓库中复制 `AGENTS.md`、`docs/README.md`、`docs/architecture/` 与 `docs/templates/`，再生成并核对一个 Root Goal。保持 `skills/install.*` 不负责核心 Root 初始化。

**为什么**：

- D-008 将独立启用说明的 canonical 所有者明确为核心文档层，并要求证明核心包脱离 Skills/Web 可用。
- 把复制来源、生成路径和核对清单写入 `docs/`，能让人类协作者在没有 AI 宿主时复现同一边界。
- 把场景测试放在 `docs/tests/`，可验证 `git init`、Root 五件套、`parent: null` 和 goal-tree 一致性，同时不把 Skills 安装测试冒充核心产品证据。

**未选方案**：

- **扩展 `skills/install.*` 增加 Root 初始化**：会把核心文档所有权和 Skills 分发职责混在一起，也超出阶段 4 的独立核心包边界。
- **只在 `skills/README.md` 写启用步骤**：安装包说明不能作为核心文档层的 canonical 入口。

## D-003 · 以核心入口版本作为可复制包快照

**日期**：2026-07-19
**状态**：accepted

**决定**：将 `docs/README.md` 的 `version: 0.4.0` 作为本轮核心可复制包快照版本，并在该入口记录变更范围与 canonical → Skills 镜像核验台账。由于 `docs/templates/goal-folder/` 本轮没有内容变更，采用“无覆盖复制 + 字节级核验”的同步事实，不伪造一次模板改写；快照身份绑定到 2026-07-19 的已提交基线 `2f54048db32b0e02194b0c0092e3e801b9532bc3`，但不声明为 release，也不创建 tag。

**为什么**：

- D-008 要求版本/变更范围由核心入口持有；沿用入口版本能避免再造一个与文档版本脱节的包号。
- 明确“模板未变更但镜像已核对”比无事实地写“已同步”更准确，也保留了 canonical 单向所有权。
- 记录基线 commit 与无 release tag 的边界，避免把可追溯 revision 误解为已发布版本。

**未选方案**：

- **新增独立 package manifest 或 release tag**：当前阶段只需可核对的核心入口台账；本轮明确不声明 release，发布标识留待后续版本化工作。
- **强制覆盖复制模板以制造同步差异**：canonical 未变更时没有必要改写镜像，且会制造无意义的 metadata churn。

## D-004 · 明确 0.4.0 快照身份与后续治理修正边界

**日期**：2026-07-19
**状态**：accepted

**决定**：响应 A-002/F-002 时采用“不声明 release、仅记录 commit revision”的处理方式。`0.4.0` 绑定到已提交基线 `2f54048db32b0e02194b0c0092e3e801b9532bc3`；该基线没有指向它的 release tag。A-002 响应产生的 README、决策、执行和审计台账修正属于基线之后的未发布治理工作树，不冒充 `0.4.0` 的内容。

**为什么**：

- A-002 发现“没有 commit”的旧措辞已与仓库事实不符，但没有发现必须创建 release tag 的用户需求。
- 绑定已提交 SHA 能提供可追溯身份，同时保留“未声明 release”的阶段边界。
- 将后续纠错与快照内容分开，避免正式 close-out 时把工作树修正误读为已发布包的一部分。

**未选方案**：

- **立即创建 `0.4.0` release tag**：会扩大本轮授权范围，并把阶段性治理修正混入发布动作。
- **把 `0.4.0` 绑定到本次响应后的最终 commit**：该 commit 尚未产生，且会使快照身份随响应台账变动。

**影响**：D-003 的发布身份措辞按本条修正；F-002 可在有路径、SHA、日期、无 tag 与工作树边界证据后关闭。F-003 继续作为 low / recommended / open 的非阻塞历史记录项保留。
