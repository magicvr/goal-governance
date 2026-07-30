---
id: GOAL-023-skills-core-dual-asset-install
doc: execution
status: active
parent: GOAL-001-main-vision
created: 2026-07-30
updated: 2026-07-30
version: 0.3.0
---

# 执行记录 · GOAL-023

## 时间线

### 2026-07-30 · 立项与产品裁决落盘（D-001）

- 用户确认产品方向：  
  1. 提供 core 方法论资产的同时，**skills 资产仍内嵌 core**（安装不必再从网上拉 core）；  
  2. **在线 bootstrap 脚本**与**包内 install 脚本**双入口。  
- 新建五件套：`GOAL-023-skills-core-dual-asset-install/`。  
- 纲领路线图 A→F 写入 `00-meta`；信息项 I-001～I-004 登记为 open。  
- 同步 `goal-tree.md`（树 + 表）；下一编号 **GOAL-024**。  
- **未** tag/Release。

### 2026-07-30 · 阶段 A 冻结 + 阶段 B core pack（D-002）

- 用户接受 I-001～I-004 推荐默认 → [D-002](01-decision.md#d-002--阶段-a-方案冻结接受推荐默认--2026-07-30)。  
- 实现 `scripts/pack_core_release.py`：产出 `goal-governance-core-v{version}.zip` + `.sha256`；拒绝 tech-stack / symlink；可 stage 再打包。  
- 实现 `assert_core_subset_of_skills_core`（I-004）。  
- 单测 `scripts/tests/test_pack_core_release.py`：**6 passed**；既有 pack skills 测试仍绿（1 skipped symlink 权限）。  
- 本地示例：`python scripts/pack_core_release.py --version 0.0.0-testpack --output-dir dist/ --skip-stage`。  
- **未**实现 bootstrap / 文档双入口 / CI 挂 core（阶段 C～E）。

### 2026-07-30 · 阶段 C～E + 回归（停在独立审计前）

- **C · Bootstrap**：`scripts/bootstrap/install-online.ps1` + `install-online.sh` + README。  
  - 默认：skills zip（内嵌 core）→ SHA-256 fail closed → 物化 `./skills` → 包内 install `-All` / `--all`。  
  - 离线：`-ZipPath` / `--zip-path` + sidecar。  
  - 单测：`scripts/tests/test_bootstrap_install_online.py`（PS 成功 + digest 失败；bash 结构 + usable bash 时 e2e）。  
- **D · 文档**：根 `README.md`、`skills/README.md`、`docs/releases/README.md`、`docs/standalone-bootstrap.md` 双入口 + core-only 并行说明。  
- **E · CI**：`skills-pack-release.yml` pack core zip + 复制 bootstrap 进 dist；publish 强制 skills+core zip/sha256。  
- **回归**：pack 13（1 skip）/ bootstrap 6（1 skip WSL bash）/ skills 39 / docs 26 OK。  
- **未** tag/Release；**未** self close-out；**status 仍 active**。  
- 显式停止点：等待 **独立 `/audit`** 后再关门。

### 2026-07-30 · Bootstrap 相对路径修复（skeptic）

- **缺陷**：相对 `-ZipPath` / `--zip-path`（及 sha 路径）曾错误解析到 **TargetDir**，导致 CWD 下 `dist\…zip` + 独立 `-TargetDir` 失败。  
- **修复**：相对路径相对 **进程 CWD**（`Get-Location` / `pwd`）；绝对路径不变。PS + bash 对齐。  
- **测试**：`test_offline_relative_zip_resolved_against_cwd_not_target`（TargetDir≠CWD + 相对 zip）。bootstrap suite **7**（1 skip WSL bash）。  
- **仍** `active`；**不**关门；待独立 `/audit`。

## 当前进展

| 阶段 | 状态 |
|------|------|
| A 方案冻结 | **done**（D-002） |
| B Core 独立资产 | **done** |
| C 在线 bootstrap | **done** |
| D 文档双入口 | **done** |
| E CI / Release 挂接 | **done** |
| F 回归与关门 | 回归绿；**关门待独立审计** |

## 下一步

1. 用户或协作者运行 **`/audit`** 对本目标（scope：GOAL-023 C～E 交付）。  
2. `/govern` 响应 findings 后，再阶段 F 关门（用户确认 → `done`）。

## 实现触点索引

| 区域 | 路径 |
|------|------|
| core pack | `scripts/pack_core_release.py` |
| skills pack（仍内嵌 core） | `scripts/pack_skills_release.py` |
| core 单测 | `scripts/tests/test_pack_core_release.py` |
| bootstrap | `scripts/bootstrap/install-online.ps1` / `.sh` / `README.md` |
| bootstrap 单测 | `scripts/tests/test_bootstrap_install_online.py` |
| 包内 install | `skills/install.ps1` / `install.sh` |
| 文档 | 根 `README.md`、`skills/README.md`、`docs/releases/README.md`、`docs/standalone-bootstrap.md` |
| CI | `.github/workflows/skills-pack-release.yml` |
