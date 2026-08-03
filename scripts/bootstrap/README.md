---
title: Bootstrap installers · dual entry point (online)
status: active
created: 2026-07-30
updated: 2026-08-04
parent: null
version: 0.2.0
---

# Bootstrap installers (GOAL-023)

**Entry point 1 — bootstrap** (this directory): obtain the **skills** zip (core **embedded**), verify SHA-256, materialize `./skills`, run package-local install (default `-All` / `--all`).

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

## Online (Release)

**Docs pin the latest published tag** (currently **`v0.12.0`**). On each formal release, update examples here and in root / `skills` README to that tag. Commands still **pin a version** — this is not unversioned always-latest install. Prefer **tag-fixed Release URLs** over floating branch raw (D-002 / D-003).

Fetch bootstrap from the Release, then run (save to disk first; avoid `curl | bash` / `irm | iex` as the default path):

```powershell
# Current latest formal tag: v0.12.0
Invoke-WebRequest -Uri "https://github.com/magicvr/goal-governance/releases/download/v0.12.0/install-online.ps1" `
  -OutFile .\install-online.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-online.ps1 -Version 0.12.0 -Force
```

```bash
curl -fsSL -o install-online.sh \
  "https://github.com/magicvr/goal-governance/releases/download/v0.12.0/install-online.sh"
chmod +x install-online.sh
bash ./install-online.sh --version 0.12.0 --force
```

URL shape (D-002 / D-003):

- Bootstrap: `https://github.com/magicvr/goal-governance/releases/download/vX.Y.Z/install-online.ps1` (or `.sh`)
- Skills zip: `https://github.com/magicvr/goal-governance/releases/download/vX.Y.Z/goal-governance-skills-vX.Y.Z.zip` (+ matching `.sha256`)

Release attachments also include these bootstrap scripts and the core-only zip (CI pack job).

## Update after first install

Bootstrap is the first-install entry. A package that includes `skills/update.py` can update itself thereafter with `skills/update.ps1` or `skills/update.sh`; it supports fixed/latest Release discovery, offline zip + sidecar, protocol preflight, managed-file conflict detection, backup and automatic rollback. This avoids deleting and reinstalling `skills/` for every compatible release. Python 3 is required for the shared transactional updater.
