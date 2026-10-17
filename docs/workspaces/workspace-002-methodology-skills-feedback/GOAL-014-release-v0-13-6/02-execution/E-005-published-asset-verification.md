---
id: E-005
goal: GOAL-014-release-v0-13-6
doc: execution-entry
title: S4 正式资产逐项验收
status: recorded
parent: GOAL-014-release-v0-13-6
created: 2026-10-17
updated: 2026-10-17
version: 0.1.0
---

# E-005 · 正式资产验收

通过 `gh release download v0.13.6` 下载正式 Release 的全部 9 项资产并用 `gh release view --json assets` 回读清单；未用本地预演 ZIP 冒充正式产物。验收结果见 [asset-verification.json](../attachments/asset-verification.json)。

1. **资产齐全**：9 项 = Skills ZIP、Core ZIP 及两个 `.sha256`、`install-online.ps1`、`install-online.sh`、`bootstrap-README.md`、`compatibility-report.json`、`release-evidence.json`；状态均 `uploaded`，无缺项、无多余项。
2. **摘要一致**：重下载后本地 SHA-256 与各自 sidecar 逐项相同（skills `de3ce7b8…`、core `b06b55ec…`）；sidecar 内容与 `Get-FileHash` 结果一致。
3. **包结构**：Skills ZIP 86 个成员、Core ZIP 27 个成员；Core 的 27 个成员在 Skills ZIP 的 `core/` 下**逐字节存在**（missing 0 / byte mismatch 0）；Skills ZIP 内含 `core/docs/standalone-bootstrap.md` 与包内 `README.md`。
4. **发布证据**：下载的 `release-evidence.json` 为 `releaseStatus: release-candidate`、`checksPassed: true`，四项 check 全 pass；`annotatedTag = v0.13.6`、`tagObject = a1224918…`、`source.commit = 97f6f1ea…`、`candidateRevision = v0.13.6`、`workingTree.clean = true`、591 条 digests。`compatibility-report.json` 为 `ready-for-release-evidence`、`uncovered = 0`、mirror passed。
5. **隔离消费安装**：使用**实际下载**的 `install-online.ps1`、Skills ZIP 与 sidecar，在仓库忽略目录 `artifacts/consumer-0.13.6` 新建隔离 consumer，执行 `-Version 0.13.6 -Channel files -Force -ZipPath … -Sha256Path … -TargetDir …`。安装 **exit 0**；`docs/standalone-bootstrap.md`、`docs/architecture/principles.md`、`docs/templates/goal-folder/00-meta.md`、`skills/prompts/00-govern-orchestrator.md`、`skills/contracts/skills-consumer-contract.json` 就位；四宿主入口目录（`.claude` / `.grok` / `.agents` / `.github`）生成；预置的消费者自有规则 `KEEP-CONSUMER-RULE-136` **原样保留**，且 managed 段已写入。完整输出见 [consumer-install.txt](../attachments/consumer-install.txt)。
6. **MCP 镜像**：`docker pull ghcr.io/magicvr/goal-governance-mcp-server:0.13.6` 成功，digest `sha256:0d48e35e80967128d1d3c8e37b6436afc6092b2d56bff996a211eb702b87389b`，与发布日志 `containerimage.digest` **一致**；`docker run --rm …:0.13.6 -c 'import __init__; print(__init__.__version__)'` 返回 **`0.13.6`**。`:latest` 的推送以同一 run 的成功日志为证，未宣称额外拉取 latest。

## 结论与边界

S4 的资产验收通过，I-006 verified。本次只验证已发布资产与其身份；未修改 `docs/` canonical、`skills/` 入口或运行时代码；未移动既有 tag、未覆盖旧 Release。保证等级仍为框架默认 L0：这是对本仓发布流程的自证，不是第三方鉴证；不把「九项资产核对通过」外推为所有下游环境的安装结果。
