---
id: GOAL-016-charter-version-decoupling
doc: decision-entry
record_id: D-003
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-26
updated: 2026-10-26
version: 0.1.0
---

## D-003 · S5 发布 v0.13.8：范围、证据与审批边界（2026-10-26）

### 触发

A-004 independent 复审 `pass`，开放 required 0；A-005 退出 S4。按 D-001/D-002，S5 承载 `v0.13.8` 正式发布与资产验收，并关闭 issue #34。用户 Q-004 已裁决 **patch `v0.13.8`**。

### 决定

1. **版本**：patch **`v0.13.8`**。协议 `0.1.0`、consumer contract 数据结构与 MUST 门禁不变；发布内容是 issue #34 的治理协议修正、校验/测试/模板/Skills/安装面同步。
2. **证据策略**：
   - 在 `docs/releases/runtime/v0.13.8/` 重新采集 **16 格**：3 宿主（Claude Code / Grok Build / GitHub Copilot）× 4 治理入口（govern / audit / vision / vision-audit）+ 4 宿主 MCP 目录探针。探针正文仍只含正式命令形式，不附加 scope/结论预期。
   - 证据使用当前工作树的 `behaviorSources`；采集后不得再改 `skills/AGENTS.template.md`、`docs/architecture/{principles,workspace-protocol}.md`、`docs/vision/alignment.md`、`skills/prompts/*`、`skills/install/*` 入口文件，否则须重采。
   - 矩阵 `candidateRevision` = `v0.13.8`，12 条入口证据指向新目录；`capture_runtime_evidence --check` 与 `compatibility_report --require-ready` 必须转绿。
3. **版本清单**：`CHANGELOG.md` 新增 `0.13.8` 节并复位 `Unreleased`；根 README、`skills/README.md`、`scripts/bootstrap/README.md`、`mcp/README.md`、`docs/releases/README.md` 的安装/GHCR pin 改为 `v0.13.8` / `0.13.8`；矩阵与 `skills/contracts` 镜像同步；CI 证据目录与相关测试断言改为 v0.13.8。
4. **发布链路**（串行）：
   a. 16 格采集与矩阵/清单；
   b. 全量回归（docs / skills / scripts / stage / compatibility / strict rehearsal）；
   c. 提交 release 候选并 push 分支，开 PR，Ubuntu/Windows CI 全绿；
   d. 合并 `main`；在 merge commit 上跑 strict 预检；创建并 push annotated `v0.13.8`；
   e. tag workflow 的 `pack` 与 `Publish GitHub Release (gated)` 全绿；Environment `release` 由**用户人工审批**（AI 不代批、不改配置）；
   f. 9 项 Release 资产逐项验收；GHCR digest 与内置版本核对；隔离消费安装通过；
   g. 关闭 issue #34；关门审计 + 用户确认后 GOAL-016 → `done`。
5. **失败处理**：provider 容量/凭据/超时失败时保留失败事实并重试同一 provider/model/输入，不降级、不伪造 pass；CI 失败则修复后重跑；发布门禁失败不得 tag 或上传资产。Environment 未批则目标 `blocked`，等待真实用户审批。
6. **审计**：S5 发布产出属 release 高影响门禁；A-004 已覆盖修正复审，但发布产出仍需关门前审计（self + 如用户要求的 independent）。未完成前不得宣称发布或关门。

### 为什么

- 用户明确要求发布新版本；issue #34 的消费面修正只有在发货资产与运行证据上闭环，才能被消费仓实际获得。
- 版本号用 patch 符合既有协议修补惯例，且不改变 protocol `0.1.0` / consumer contract 数据结构。
- 先行采集证据再改非 behavior-source 的 CHANGELOG/README/matrix，可避免清单更新反复使证据过期。

### 未选方案

- **minor `v0.14.0`**：Q-004 已选 patch；本 change 不改变 protocol/consumer contract 数据结构。
- **复用 v0.13.7 的 16 格证据**：behaviorSources 已过期，不能复用。
- **AI 代批 Environment `release`**：禁止；仍须用户人工审批。
- **跳过发布直接关门**：用户明确要求发布，不选。
- **用 semver 范围/改矩阵以绕过红门禁**：禁止。

### 用户裁决留痕

| 问题 ID | 原题 / 选项 | 影响门禁 | 真实答复 |
|---------|-------------|----------|----------|
| Q-004 | 发布版本号：patch `v0.13.8` / minor `v0.14.0` / S5 前再定 | S5 清单、tag、资产身份 | **patch `v0.13.8`**（2026-10-26 卡片） |
