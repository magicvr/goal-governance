---
id: GOAL-018-skills-release-packaging
doc: decision
status: done
parent: GOAL-001-main-vision
created: 2026-07-22
updated: 2026-07-22
version: 1.0.1
---

# 决策记录 · GOAL-018

## D-001 · 交付面：skills-only zip + 离线 install（2026-07-22）

**决定**：

1. 对外主路径是 **GitHub Release 上的 skills-only 安装包**（`goal-governance-skills-vX.Y.Z.zip`），不是 clone 全仓。
2. 包内容 = 仓库 `skills/` 分发面（prompts、install 适配、templates/contracts 镜像、install 脚本、可选 tests）；排除 `docs/workspace-*`、`web/`、`artifacts/`、Python 缓存。
3. 消费方：下载 → 解压到目标仓库（通常为 `./skills`）→ `install.ps1` / `install.sh` 按宿主安装 `/govern` + `/audit`。
4. 维护者打包入口：`scripts/pack_skills_release.py`（给定 version + output dir → zip + SHA-256）。
5. 正式 annotated tag 时：zip + release-evidence 作为 Release 附件；CI 在 tag 上 **只 pack + 上传 workflow artifact**，`gh release` 挂载须维护者授权，默认不自动发布。

**为什么**：

- `skills/` 已是自包含离线包；Release 只补版本固定、下载入口与 digest。
- 与 GOAL-008 发布证据纪律一致：证据脚本不替维护者推 tag/建 Release。
- 避免 monorepo dogfood 过程树进入消费者目录。

**未选方案**：

- **整仓 zip 给消费者**：体积大、易带过程树与 Web 代码，安装面不清晰。
- **npm/PyPI**：交付物是 Markdown + 脚本，registry 无收益。
- **CI 无条件 `gh release create`**：违反维护者授权门禁与 sandbox 安全边界。

## D-002 · 打包不宣称新 release identity（2026-07-22）

**决定**：pack 脚本接受任意合法版本字符串（含测试用 `0.0.0-testpack`），只负责归档与 digest；**不得**改写兼容矩阵、`candidateRevision` 或 `verificationStatus`。新的 verified release 仍走 annotated tag + release_evidence + 宿主证据路径。

**为什么**：当前工作树在 GOAL-010 后可为 `unreleased`；打包能力与「已发布身份」必须分离。

## D-003 · 有界关门（2026-07-22）

**决定**：四项 P0～P2 交付完成且单测/pack 重放通过后，将本目标标为 `done / 100%`。不把「未实际创建公开 Release」列为 open required——验收以文档路径 + 可重放 pack + 门禁式 CI 为准（与计划 Non-goals 一致）。

## D-004 · 响应 A-002 recommended 三项且维持 done（2026-07-22）

**决定**：

1. **F-001**（CI artifact 名）：立即修正为单一 NORM 身份（`skills-pack-${version}`），upload/download 对齐；属维护性修复，**不**重开目标。
2. **F-002**（缺 residual/I 表）：接受为 **R-018-FIRST-RELEASE** residual（首次真实 tag+Release 挂载演练），写在 `00-meta`；**非** required 信息门禁。
3. **F-003**（A-001 结构偏薄）：接受为过程约定，后续 self 关门用更完整模板；**不**回溯改写 A-001。
4. GOAL-018 **保持** `status: done` / `progress: 100%`。

**为什么**：A-002 verdict=pass 且无 required finding；用户明确指示 recommended 响应 + 维持 done + 可选修 artifact 名。

**未选方案**：因 recommended 项将目标重开为 `active`（过度；与 A-002 建议冲突）。
