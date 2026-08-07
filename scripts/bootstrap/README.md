---
title: Bootstrap installers · dual entry point (online)
status: active
created: 2026-07-30
updated: 2026-08-07
parent: null
version: 0.3.0
---

# Bootstrap installers (GOAL-023 / VP-004 R2 dual entry)

**Entry point 1 — bootstrap** (this directory): obtain the **skills** zip (core **embedded**), verify SHA-256, then install via one of the two **一等（first-class）通道**：

| 通道 | 说明 |
|------|------|
| **`-Channel mcp`（推荐 MCP）** | 薄通道（R4 重定义）：不落 MCP 代码；写 `skills/contracts/` + 经 **GHCR 镜像内 lifecycle** 写 `AGENTS.md` managed 段与 `.goal-governance/` 状态，并输出 MCP client 配置指引（`docker run` 固定入口，零参数）。运行时为 **Docker 镜像** `ghcr.io/magicvr/goal-governance-mcp-server:<版本>`（与 File 资产同 tag 同版本发布）；需要 docker。本地 stdio 进程形态仍合法（源码 `mcp/`）。**File 通道仍为一等发布路径、未被废除、非日落**。 |
| **`-Channel files`（默认）** | 完整 File 通道：materialize 整包 + 包内 install `-All`（docs/architecture + skills + 宿主面）。**File-classic**（无 Docker、无 MCP）始终可用。 |

> **推荐叙述声明**：本安装器**推荐**新装走 MCP 薄通道以降低 footprint 与升级噪音；这不废除 File 通道——File zip 安装、File-classic 路径与生产仓 File 自举继续一等支持（VP-004 Charter 叙事选择 V-F-015）。

**Entry point 2 — package-local**: after the zip is already extracted, run `skills/install.ps1` or `skills/install.sh` (offline, no network).

Bootstrap **never** downloads a separate core package for the default skills install path. The optional **core-only** asset (`goal-governance-core-v*.zip`) is a parallel methodology package (standalone / no-Skills); see `docs/standalone-bootstrap.md` and `scripts/pack_core_release.py`.

## Scripts

| Script | Host |
|--------|------|
| `install-online.ps1` | Windows PowerShell (complete) |
| `install-online.sh` | bash + unzip + sha256sum/shasum (complete; requires bash environment) |

## Offline (air-gap / tests)

Relative `-ZipPath` / `--zip-path` (and sidecar paths) resolve against the **process current working directory**, not `--target-dir` / `-TargetDir`. Absolute paths are unchanged.

```powershell
# CWD = repo root; zip under dist\; install into empty consumer (TargetDir ≠ CWD)
python scripts/pack_skills_release.py --version 0.0.0-testpack --output-dir dist/ --skip-stage
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\bootstrap\install-online.ps1 `
  -Version 0.0.0-testpack `
  -TargetDir C:\path\to\empty-project `
  -ZipPath dist\goal-governance-skills-v0.0.0-testpack.zip `
  -Force
```

```bash
python scripts/pack_skills_release.py --version 0.0.0-testpack --output-dir dist/ --skip-stage
bash scripts/bootstrap/install-online.sh \
  --version 0.0.0-testpack \
  --target-dir /path/to/empty-project \
  --zip-path dist/goal-governance-skills-v0.0.0-testpack.zip \
  --force
```

Digest mismatch → non-zero exit; package install is not applied from a bad zip.

### MCP 薄通道（-Channel mcp）

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\bootstrap\install-online.ps1 `
  -Version 0.0.0-testpack -Channel mcp `
  -TargetDir C:\path\to\empty-project `
  -ZipPath dist\goal-governance-skills-v0.0.0-testpack.zip `
  -Force
```

```bash
bash scripts/bootstrap/install-online.sh \
  --version 0.0.0-testpack --channel mcp \
  --target-dir /path/to/empty-project \
  --zip-path dist/goal-governance-skills-v0.0.0-testpack.zip \
  --force
```

结果：`skills/contracts/skills-consumer-contract.{json,schema.json}` + `AGENTS.md` managed 段（`<!-- goal-governance:begin managed -->` … `end managed`）+ `.goal-governance/install.json`（`channel=mcp`）+ MCP client 配置指引（`docker run -i --rm -v <仓库根>:/workspace ghcr.io/magicvr/goal-governance-mcp-server:<版本>`）。**不**安装 File 大包（docs/architecture、prompts 全量等），**不**落 MCP 代码（R4：MCP 通道资产 = GHCR Docker 镜像，与 File zip 同 tag 发布）。File 通道仍为一等，未被废除。

## Online (Release)

**Docs pin the latest published tag** (currently **`v0.13.1`**). On each formal release, update examples here and in root / `skills` README to that tag. Commands still **pin a version** — this is not unversioned always-latest install. Prefer **tag-fixed Release URLs** over floating branch raw (D-002 / D-003).

Fetch bootstrap from the Release, then run (save to disk first; avoid `curl | bash` / `irm | iex` as the default path):

```powershell
# Current latest formal tag: v0.13.1
Invoke-WebRequest -Uri "https://github.com/magicvr/goal-governance/releases/download/v0.13.1/install-online.ps1" `
  -OutFile .\install-online.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-online.ps1 -Version 0.13.1 -Force
```

```bash
curl -fsSL -o install-online.sh \
  "https://github.com/magicvr/goal-governance/releases/download/v0.13.1/install-online.sh"
chmod +x install-online.sh
bash ./install-online.sh --version 0.13.1 --force
```

URL shape (D-002 / D-003):

- Bootstrap: `https://github.com/magicvr/goal-governance/releases/download/vX.Y.Z/install-online.ps1` (or `.sh`)
- Skills zip: `https://github.com/magicvr/goal-governance/releases/download/vX.Y.Z/goal-governance-skills-vX.Y.Z.zip` (+ matching `.sha256`)

Release attachments also include these bootstrap scripts and the core-only zip (CI pack job).

## Update after first install

Bootstrap is the first-install entry. A package that includes `skills/update.py` can update itself thereafter with `skills/update.ps1` or `skills/update.sh`; it supports fixed/latest Release discovery, offline zip + sidecar, protocol preflight, managed-file conflict detection, backup and automatic rollback. This avoids deleting and reinstalling `skills/` for every compatible release. Python 3 is required for the shared transactional updater.
