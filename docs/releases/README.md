# 发布证据与 Skills 安装包

本目录定义发行证据格式，并说明 **Skills 消费 zip** 如何与 annotated tag / GitHub Release 对齐。它不是目标状态源。

## 证据（兼容矩阵 / release-evidence）

- canonical 兼容性声明仍位于 `docs/contracts/skills-consumer-contract.json`；兼容矩阵位于 `docs/contracts/skills-consumer-compatibility-matrix.json`。
- CI 使用 `scripts/compatibility_report.py` 与 `scripts/release_evidence.py` 生成 JSON 报告、测试结果和 SHA-256 清单，并将其作为 workflow artifact 或 release attachment 保存。运行了检查时，任一检查失败会让命令和 CI 失败；报告文件仍会保留失败事实。
- `release-evidence.schema.json` 描述并约束证据格式。`rehearsal` 证明一条可重放路径被执行，不等同于 GitHub Release；`release-candidate` 仅在 annotated `vMAJOR.MINOR.PATCH` tag 指向 HEAD、矩阵 `candidateRevision` 与该 tag 一致、工作树干净、CHANGELOG 有同版本节、兼容矩阵无未覆盖 required 单元且全部检查通过时生成。
- 检查结果只能由 `release_evidence.py` 内部执行并记录，API/CLI 都不接受调用方注入的“已通过”结果；传入的 compatibility report 必须与当前 HEAD 重新生成的 source、contract、matrix、mirror 与 coverage 全部一致。
- rehearsal 命令：`python scripts/release_evidence.py --mode rehearsal --run-checks --include-web --output artifacts/release-evidence.json`。发布候选命令在维护者创建 annotated tag 后改用 `--mode release --tag vX.Y.Z`；该命令只生成证据，不推送 tag、不创建 GitHub Release。
- 创建或推送 tag、发布 GitHub Release、以及确认真实宿主 runtime 证据均须维护者授权。自动化不得把缺少这些动作的工作树写成已发布。

## Skills 安装包（消费方 zip）

其他项目应安装 **skills-only** 归档，而不是整个 monorepo。

| 资产 | 命名 | 内容 |
|------|------|------|
| 主包 | `goal-governance-skills-vX.Y.Z.zip` | 仓库 `skills/` 分发面（prompts、install 适配、templates/contracts 镜像、install 脚本等） |
| 校验 | `goal-governance-skills-vX.Y.Z.zip.sha256` | `sha256sum` 风格一行：`<hex>  <zip basename>` |

**排除**：`docs/workspace-*` 过程树、`web/`、`artifacts/`、`__pycache__` / `*.pyc` 等缓存。

### 本地打包（维护者）

在干净、意图发布的提交上：

```bash
python scripts/pack_skills_release.py --version 0.7.0 --output-dir dist/
# 产出：
#   dist/goal-governance-skills-v0.7.0.zip
#   dist/goal-governance-skills-v0.7.0.zip.sha256
```

可选前缀 `v`（`v0.7.0` → 文件名仍用 `v0.7.0` 中的数字段 `0.7.0`）。打包**不**改写兼容矩阵，**不**宣称新的 verified release identity。

### 正式 annotated tag：挂到 GitHub Release

下次（及以后）创建正式 annotated SemVer tag（如 `vX.Y.Z`）并发布时，维护者应：

1. 通过 `release_evidence.py --mode release --tag vX.Y.Z ...` 生成候选证据（门禁仍适用）。
2. 运行 `pack_skills_release.py --version X.Y.Z --output-dir dist/`（版本与 tag 对齐）。
3. 创建 GitHub Release（**须维护者授权**），将下列文件作为 **Release assets** 挂上：
   - `goal-governance-skills-vX.Y.Z.zip`
   - `goal-governance-skills-vX.Y.Z.zip.sha256`
   - `release-evidence.json`（及可选 `compatibility-report.json`）
4. 消费方按 [skills/README.md](../../skills/README.md)「从 GitHub Release 安装」解压并运行 `install.ps1` / `install.sh`。

### Tag 触发 CI：默认只 pack，不自动发布

工作流 [`.github/workflows/skills-pack-release.yml`](../../.github/workflows/skills-pack-release.yml) 在 `v*` tag 推送时：

1. 运行打包相关单测；
2. 调用 `pack_skills_release.py` 产出 zip + `.sha256`；
3. 可选生成 rehearsal/compatibility 产物并 **upload-artifact**。

**默认不**执行 `gh release create`、不推送 tag、不把工作树写成已发布。将 artifact 挂到 GitHub Release 仍由维护者在授权后手动（或经显式 `workflow_dispatch` 输入 `publish_release=true` 且具备 `contents: write` 时）完成。缺少该闸门的自动化不得发布。

Workflow artifact 名与 pack 版本统一为 **`skills-pack-<SemVer去v>`**（例：tag `v0.8.0` → artifact `skills-pack-0.8.0`）。`attach-to-release` 通过 `needs.pack.outputs.artifact_name` 下载，不得使用带 `v` 前缀的 tag 字符串作为 artifact 名（GOAL-018 A-002 F-001 / A-003）。
