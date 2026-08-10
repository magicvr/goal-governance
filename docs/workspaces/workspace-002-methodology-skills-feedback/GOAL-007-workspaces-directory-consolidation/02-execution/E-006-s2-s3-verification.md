---
id: E-006
goal: GOAL-007-workspaces-directory-consolidation
status: recorded
created: 2026-08-11
updated: 2026-08-11
version: 0.1.0
---

# E-006 · S2/S3 验证

## 已执行事实

- `python scripts/stage_skills_mirrors.py --check` 通过，canonical → Skills 镜像检查 `36` 对，无漂移。
- `python scripts/capture_runtime_evidence.py --check --evidence-dir docs/releases/runtime/v0.13.2` 通过，12 个候选 runtime evidence 全部 `pass` 且行为源哈希一致。
- `python scripts/compatibility_report.py --output artifacts/compatibility-report.json` 通过，矩阵 `candidateRevision: v0.13.2`，coverage `ready-for-release-evidence`，`uncovered: []`，mirror verification `passed: true`。
- docs 测试 `50` 项通过；Skills 编排测试 `42` 项通过；scripts 测试 `114` 项通过（4 项按环境条件跳过：本机 bash 为无 distro 的 WSL stub，symlink 测试无 Windows 权限）。MCP L1/config 定向测试 `57` 项通过；Copilot surface 定向测试 `8` 项通过；Windows isolated installer smoke 通过。
- `git diff --check` 通过；当前 `docs/` 直属 `workspace-*` 目录为 `0`，`mcp.config.workspace_layout_report(Path("docs"))` 返回 `state: canonical`，列出三个 `docs/workspaces/workspace-*`。
- 静态扫描仅保留协议迁移说明、安装器拒绝逻辑、打包排除测试和历史 VRev 审计原文中的旧路径；没有当前活动工作区或 canonical 写入逻辑继续使用旧直属路径。

## 范围边界

本记录不宣称 PR、main 合并、annotated tag 或正式 Release 已完成；这些事实留待 S5 的远端证据。
