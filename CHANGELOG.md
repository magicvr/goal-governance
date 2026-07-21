# Changelog

所有可发布变更以 annotated SemVer tag 和对应的 release evidence 为准。工作树中的“Unreleased”内容不构成发布声明。

## Unreleased

- Skills 消费 zip 打包入口：`scripts/pack_skills_release.py`（版本化 zip + SHA-256）；消费/维护者文档见 `skills/README.md`、根 `README.md`、`docs/releases/README.md`；tag 触发 pack workflow `.github/workflows/skills-pack-release.yml`（默认 artifact-only，不自动创建 GitHub Release）。
- 后续变更尚未绑定新的 release tag；`v0.7.0` 的阶段 5 发布一致性证据见下方条目。

## 0.7.0 - 2026-07-20

- 完成 Skills 消费适配器兼容矩阵、GitHub Copilot CLI runtime replay、Web parser CI replay 与 release evidence 链路。
- 以 annotated `v0.7.0` tag、clean candidate commit 和内部 checks 绑定可追溯候选证据。
