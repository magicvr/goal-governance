# 发布证据与 Skills 安装包

本目录定义发行证据格式，并说明 **Skills 消费 zip** 如何与 annotated tag / GitHub Release 对齐。它不是目标状态源。

## 证据（兼容矩阵 / release-evidence）

- canonical 兼容性声明仍位于 `docs/contracts/skills-consumer-contract.json`；兼容矩阵位于 `docs/contracts/skills-consumer-compatibility-matrix.json`。
- CI 使用 `scripts/compatibility_report.py` 与 `scripts/release_evidence.py` 生成 JSON 报告、测试结果和 SHA-256 清单，并将其作为 workflow artifact 或 release attachment 保存。运行了检查时，任一检查失败会让命令和 CI 失败；报告文件仍会保留失败事实。
- `release-evidence.schema.json` 描述并约束证据格式。`rehearsal` 证明一条可重放路径被执行，不等同于 GitHub Release；`release-candidate` 仅在 annotated `vMAJOR.MINOR.PATCH` tag 指向 HEAD、矩阵 `candidateRevision` 与该 tag 一致、工作树干净、CHANGELOG 有同版本节、兼容矩阵无未覆盖 required 单元且全部检查通过时生成。
- 检查结果只能由 `release_evidence.py` 内部执行并记录，API/CLI 都不接受调用方注入的“已通过”结果；传入的 compatibility report 必须与当前 HEAD 重新生成的 source、contract、matrix、mirror 与 coverage 全部一致。
- rehearsal 命令：`python scripts/release_evidence.py --mode rehearsal --run-checks --include-web --output artifacts/release-evidence.json`。发布候选命令在维护者创建 annotated tag 后改用 `--mode release --tag vX.Y.Z`；该命令只生成证据，**不**推送 tag。
- **创建或推送 annotated tag** 仍须维护者授权（人或受控流程）。自动化**不得**把缺少 tag / 门禁失败的工作树写成已发布。

## Skills / Core 安装包（消费方资产 · GOAL-023）

其他项目应安装 **skills** 归档（**内嵌 core**），而不是整个 monorepo。可选并行挂载 **core-only** 与 **bootstrap** 脚本。

| 资产 | 命名 | 内容 |
|------|------|------|
| 主包（默认安装路径） | `goal-governance-skills-vX.Y.Z.zip` | 仓库 `skills/` 分发面（prompts、install、`core/` **内嵌**、templates/contracts 镜像等） |
| 主包校验 | `goal-governance-skills-vX.Y.Z.zip.sha256` | `sha256sum` 风格一行：`<hex>  <zip basename>` |
| 方法论并行包 | `goal-governance-core-vX.Y.Z.zip` | `skills/core/` 子集（standalone / 无 Skills）；**非**默认 skills 安装路径 |
| 方法论校验 | `goal-governance-core-vX.Y.Z.zip.sha256` | 同上 |
| Bootstrap | `install-online.ps1` / `install-online.sh` | 入口 1：下 skills zip（或本地 zip）→ 校验 → 包内 install（默认 `-All`） |
| Bootstrap 说明 | `bootstrap-README.md` | 与 `scripts/bootstrap/README.md` 同源摘要 |
| 证据 | `release-evidence.json`（及可选 `compatibility-report.json`） | 与该 tag 绑定的发行证据 |

**排除**：`docs/workspace-*` 过程树、`web/`、`artifacts/`、`__pycache__` / `*.pyc` 等缓存、`tech-stack.md`。

**双安装入口**（消费方）：

1. **Bootstrap**（Release **tag 固定 URL** 拉 `install-online.*`，或 monorepo `scripts/bootstrap/`）— 可在线或离线 zip。  
2. **包内** `skills/install.ps1` / `install.sh` — 解压后离线。  

默认 skills 路径**不**要求联网拉取 core；core-only 与 skills 内嵌 core 在同 version 下应字节一致（pack 单测）。

**文档 pin 规则（GOAL-023 D-003）**：根 `README.md`、`skills/README.md`、`scripts/bootstrap/README.md` 入口 1 示例**必须**使用**当前最新正式 annotated tag**（现为 `v0.10.0`）。每次正式发版后同步改写示例中的 tag/version；**禁止**以 `main`/branch raw 或无版本 pin 的 always-latest 作权威安装入口。

### 本地打包（维护者 / 调试）

```bash
python scripts/pack_skills_release.py --version 0.7.0 --output-dir dist/
python scripts/pack_core_release.py --version 0.7.0 --output-dir dist/
# 产出：
#   dist/goal-governance-skills-v0.7.0.zip (+ .sha256)
#   dist/goal-governance-core-v0.7.0.zip (+ .sha256)
# bootstrap 脚本由 CI 复制进 dist/；本地可直接用 scripts/bootstrap/
```

打包**不**改写兼容矩阵，**不**宣称新的 verified release identity。
### 正式发布路径（自动：pack + 门禁 + Environment + Release）

工作流 [`.github/workflows/skills-pack-release.yml`](../../.github/workflows/skills-pack-release.yml)：

```text
维护者：冻结 CHANGELOG + 矩阵 candidateRevision=tag + 必要 runtime
        → 创建并 push annotated tag vX.Y.Z
              ↓
        pack job：单测 + skills zip + core zip + bootstrap 脚本 + workflow artifact
              ↓
        publish job：
          1) environment: release  （Required reviewers + wait timer + main/v* 策略）
          2) release_evidence --mode release --run-checks --include-web  （硬失败则停）
          3) gh release create（若不存在；含 -rc 等 pre-release 段则 --prerelease）
          4) gh release upload：skills/core zip + digests + bootstrap + release-evidence + compatibility-report
```

| 规则 | 说明 |
|------|------|
| **严格 evidence** | `--mode release` 任一门禁失败 → **不** create、**不** upload（fail closed） |
| **Environment `release`** | 仓库 Settings 中配置；publish 前需审批（及 wait timer）。未批过则不会发版 |
| **触发** | `push` tags `v*` 自动进入 publish；或在 **tag ref** 上 `workflow_dispatch` 且 `publish_release=true` 重跑发布 |
| **幂等** | Release 已存在则只 upload `--clobber` |
| **不自动做** | 不创建 git tag、不推远程、不改矩阵 identity |

#### 维护者发布检查清单（推 tag 前）

1. 工作树干净；`CHANGELOG.md` 有对应版本节。  
2. 兼容矩阵 `candidateRevision` **等于**将要打的 tag（如 `v0.8.0`），required 单元无 uncovered。  
3. 需要宣称的宿主 runtime 证据已按 GOAL-008 惯例就位。  
4. 本地可先：`python scripts/release_evidence.py --mode release --tag vX.Y.Z --run-checks --include-web --output artifacts/release-evidence.json`。  
5. **同步安装文档 pin（D-003）**：根 `README.md`、`skills/README.md`、`scripts/bootstrap/README.md` 入口 1 示例中的 tag / `-Version` / zip 名改为**本发版 tag**（消费方复制即对最新正式版；命令仍版本固定）。  
6. `git tag -a vX.Y.Z -m "..."` 并 `git push origin vX.Y.Z`（tag 必须打在**含本工作流**的 commit 上，通常为已合并的 `main`）。  
7. 打开 Actions → 等待 pack → 在 Environment **release** 上 **Approve**（并满足 wait timer）。  
8. 确认 GitHub Release 资产齐全（含 `install-online.ps1` / `.sh`）；消费方按 [skills/README.md](../../skills/README.md) 安装。

#### 手工重挂（不重新打 tag）

在该 **tag** 上运行 workflow_dispatch，勾选 `publish_release`：再次走 Environment + 硬 evidence + upload（可补资产）。

### Workflow 细节

- Workflow artifact 名：`skills-pack-<SemVer去v>`（例：tag `v0.8.0` → `skills-pack-0.8.0`）。  
- publish 通过 `needs.pack.outputs.artifact_name` 下载；不得用带错误前缀的名字。  
- Environment 名必须为 **`release`**（与仓库 Settings 一致）。  
- 默认仓库 `GITHUB_TOKEN` 权限为 read；**仅** publish job 申请 `contents: write`。
