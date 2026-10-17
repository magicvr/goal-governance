---
id: GOAL-015-audit-command-labeled-form
doc: execution-entry
record_id: E-008
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-008 · S5 步骤 e–f：Environment 审批、正式发布与资产验收

## 2026-10-17 · 已发生事实

1. **Environment 人工审批（I-007）**：用户答复「我已批准」后，编排侧先回读事实再记录——`gh run view 39034827440` 的 `Publish GitHub Release (gated)` 由 `waiting` 变为 `in_progress`；部署 `release`（deployment id `7139921295`，创建于 13:01:14Z）的状态链为 `waiting`（13:01:15Z）→ `queued`（13:09:22Z）→ `in_progress`（13:09:23Z）→ `success`（13:10:22Z），creator 均为 **`magicvr`（人工维护者）**；发布后 `pending_deployments` 为空。**AI 未代批、未改环境配置**。
2. **Tag workflow** [39034827440](https://github.com/magicvr/goal-governance/actions/runs/39034827440)：`pack` completed/success；`Publish GitHub Release (gated)` completed/**success**（`gh run watch --exit-status` → run `completed success`）。日志里程碑：`Release evidence passed for v0.13.7`（13:10:00Z）、`containerimage.digest = sha256:3f9fc5e5…dd6f`、`Uploaded 9 asset(s) to release v0.13.7`（13:10:16Z）。
3. **Release 身份**：[Release v0.13.7](https://github.com/magicvr/goal-governance/releases/tag/v0.13.7) 于 **2026-10-17T13:10:14Z** 发布，`isDraft = false`、`isPrerelease = false`，**9 项**资产；annotated tag `v0.13.7`（tag object `6197ed6e…`）→ merge commit `6ca04ee…`。
4. **资产验收（全部使用实际下载的发布产物，未用本地预演 ZIP）**，逐项见 [asset-verification.json](../attachments/asset-verification.json)：
   - 数量：9/9（`bootstrap-README.md`、`compatibility-report.json`、core ZIP + sidecar、skills ZIP + sidecar、`install-online.ps1`、`install-online.sh`、`release-evidence.json`）。
   - 摘要：两个 ZIP 的 sha256 与各自 sidecar **逐项一致**（skills `0c9c2dee…`、core `e512c0c6…`）。
   - 包边界：Core **27** 成员在 Skills（**86** 成员）的 `core/` 前缀下**逐字节相同**（missing 0 / byte-differing 0）。
   - 发布证据：下载的 `release-evidence.json` 为 `releaseStatus: release-candidate`、`checksPassed: true`、`source.commit = 6ca04ee…`、`source.annotatedTag = v0.13.7`、`source.tagObject = 6197ed6e…`、`workingTree.clean = true`、657 条 digests。
   - 隔离消费安装：用**实际下载**的 `install-online.ps1` + skills ZIP + sidecar 在 `artifacts/consumer-0.13.7` 新建隔离 consumer，执行 `-Version 0.13.7 -Channel files -Force -ZipPath … -Sha256Path … -TargetDir …` → **exit 0**；`docs/standalone-bootstrap.md`、`docs/architecture/principles.md`、`docs/templates/goal-folder/00-meta.md`、`skills/prompts/00-govern-orchestrator.md`、`skills/contracts/skills-consumer-contract.json` 就位；四宿主入口目录生成；消费者自有规则 `KEEP-CONSUMER-RULE-137` **原样保留**，且安装后的 `AGENTS.md` 已含带标签命令形式（第 139 行）。输出见 `artifacts/consumer-0.13.7-install.txt`。
   - MCP 镜像：`docker pull ghcr.io/magicvr/goal-governance-mcp-server:0.13.7` 的 digest `sha256:3f9fc5e5…dd6f` 与发布日志 `containerimage.digest` **一致**；`docker run … -c 'import __init__; print(__init__.__version__)'` 返回 **`0.13.7`**。
5. **状态**：S5 步骤 a–f 全部完成，`I-007 → verified`；GOAL-015 由 `blocked` 恢复 `active`，派生 `progress` = 完成阶段 **5/5 = 100%**（`status` 仍为 `active`，关门待用户）。S5 的审计模式为 `independent`（release/compatibility 高影响门禁），仍需一条指定 provider 的独立意见后方可关门。

### 证据

| 主张 | 路径 / 命令 |
|------|-------------|
| Environment 由人工批准 | `gh api repos/…/deployments/7139921295/statuses` 的 creator `magicvr` 与 waiting→success 链 |
| run 成功 | `gh run watch 39034827440 --exit-status` → `completed success` |
| Release 与资产 | `gh release view v0.13.7 --json …`（9 项、非 draft、非 prerelease）；`gh release download v0.13.7` |
| 摘要/子集/安装/镜像 | [asset-verification.json](../attachments/asset-verification.json) 与 `artifacts/consumer-0.13.7-install.txt` |
