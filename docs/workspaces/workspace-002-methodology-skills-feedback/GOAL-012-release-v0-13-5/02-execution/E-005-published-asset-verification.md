---
id: E-005
goal: GOAL-012-release-v0-13-5
doc: execution
title: 真实资产下载、摘要与消费安装验收
status: active
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-10-15
updated: 2026-10-15
version: 0.1.0
---

# E-005 · 资产验收

通过 `gh release download v0.13.5` 下载正式 Release 的全部 9 项资产，`gh release view --json ...assets` 回读清单；未用本地预演 ZIP 冒充正式产物。验收结果见 [asset-verification.json](../attachments/asset-verification.json)，正式身份见 [release-receipt.json](../attachments/release-receipt.json)。

1. 缺失/多余资产均 0；两个 ZIP SHA-256 与 sidecar 中摘要和文件名逐项相同。全部下载文件核对 GitHub 元数据中提供的 digest。
2. core 的 27 个成员逐字节等于 Skills 包的 core 子集；`docs/standalone-bootstrap.md` 存在并与 canonical 一致，Skills README 的包内相对链接有效。
3. 远端 release-evidence 的 checksPassed true，全部 checks pass；annotatedTag、source.commit、candidateRevision 与 v0.13.5 / merge 1a6668e 一致；compatibility coverage ready。字段 `releaseStatus: release-candidate` 是门禁 schema 的产出值，Release 是否正式由 GitHub isDraft/isPrerelease 与 publishedAt 判断。
4. 下载的 PS/SH bootstrap 与受审源码一致（仅规范化 checkout 换行）。使用实际下载的 PS bootstrap、Skills ZIP 和 sidecar，在仓库忽略目录内新建隔离 consumer，执行 `-Version 0.13.5 -Channel files -Force -ZipPath ... -Sha256Path ...`。安装 exit 0，guide 已复制且 governance_root 正确渲染；预置 AGENTS 原文 `KEEP-CONSUMER-RULE-135` 保留。完整输出见 [consumer-install.txt](../attachments/consumer-install.txt)。
5. 实际 `docker pull ghcr.io/magicvr/goal-governance-mcp-server:0.13.5` 成功，digest 与发布日志相同；执行无挂载的临时容器 `docker run --rm ...:0.13.5 -c 'import __init__; print(__init__.__version__)'` 返回 `0.13.5`。`:latest` 的推送以同 run 成功日志为证，未宣称额外拉取 latest。

正式 ZIP 摘要：Skills `b164f20c7e9ff6bbc1f85cf4c4e1dff7fb419b39ef53bbdfcac3d7e6f2cd8900`；core `f74a1c5c94d3392970582d183299093b2fda689a7903a82dcaaf6be53349ac2a`。预演与正式 ZIP 可因生成时间有不同摘要，验收使用各自 sidecar。

本次为发布资产验收，不重新声称在所有宿主执行新 runtime capture；复用的 2026-10-01 captures 仍保持原始日期、路径。I-005 verified、S4 完成，交 A-003 关门审计。

关门文档更新后的验证：`python -m unittest discover -s docs/tests -v` 67 tests OK，`stage_skills_mirrors.py --check` 38 对一致，`git diff --check` 通过。仅更新发行事实与目标记录，不涉及需重新生成镜像的 canonical 正文。
