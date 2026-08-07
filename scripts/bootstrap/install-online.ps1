# Goal Governance · online / offline bootstrap installer (GOAL-023)
#
# Entry point 1 (bootstrap): obtain skills zip (embedded core) → verify SHA-256
# → materialize ./skills → invoke package-local install.ps1 (default -All).
# Does NOT download core separately; skills zip already embeds core.
#
# Offline / air-gap:
#   .\install-online.ps1 -Version 0.9.2 -ZipPath .\goal-governance-skills-v0.9.2.zip
# Online (network):
#   .\install-online.ps1 -Version 0.9.2
#
# Package-local install (entry point 2) remains: skills\install.ps1 after extract.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [string]$TargetDir = '',

    [string]$SkillsDirName = 'skills',

    [string]$ZipPath = '',

    [string]$Sha256Path = '',

    [string]$Channel = 'files',

    [string]$Repo = 'magicvr/goal-governance',

    [string]$ReleaseTag = '',

    [switch]$SkipInstall,

    [switch]$Force,

    [switch]$Help
)

$ErrorActionPreference = 'Stop'

function Show-Usage {
    @"
Goal Governance bootstrap installer (GOAL-023 / VP-004 R2 dual entry)

Downloads or uses a local skills zip (core embedded), verifies SHA-256,
then installs via one of the two first-class channels:

  -Channel mcp   (推荐 MCP 通道): 薄通道——仅安装 skills/mcp + consumer
                 contract + AGENTS.md managed 段 + .goal-governance 状态。
                 **File 通道仍为一等发布路径、未被废除、非日落**；
                 File-classic（无 Docker / 无 MCP）始终可用。
  -Channel files (默认): 完整 File 通道——materialize 整包并运行包内
                 install -All（docs/architecture + skills + 宿主面）。

Usage:
  .\install-online.ps1 -Version X.Y.Z [-Channel files|mcp] [-TargetDir DIR] [-ZipPath PATH] [-Sha256Path PATH]
  .\install-online.ps1 -Version X.Y.Z -ZipPath .\goal-governance-skills-vX.Y.Z.zip   # offline
  .\install-online.ps1 -Version X.Y.Z                                               # online Release

Options:
  -Version        SemVer (optional leading v); archive name uses stripped form
  -Channel        files (默认完整 File 通道) | mcp (薄 MCP 通道；需 python)
  -TargetDir      Project root (default: current directory)
  -SkillsDirName  Directory name under TargetDir (default: skills)
  -ZipPath        Local skills zip (skip download when set)
  -Sha256Path     Local .sha256 sidecar (default: <ZipPath>.sha256 or beside zip)
  -Repo           GitHub owner/repo for online mode (default: magicvr/goal-governance)
  -ReleaseTag     Tag for download URL (default: v + normalized version)
  -SkipInstall    Only verify + extract; do not run package install
  -Force          Pass -Force to package install (overwrite)
  -Help           Show this help

Default install flags: -All -NonInteractive (-Force when -Force set).
"@
}

if ($Help) {
    Show-Usage
    exit 0
}

function Write-Err([string]$Message) {
    Write-Host "Error: $Message" -ForegroundColor Red
    exit 1
}

function Normalize-Version([string]$Raw) {
    $v = $Raw.Trim()
    if ($v.Length -eq 0) { Write-Err 'Version must be non-empty' }
    if ($v.StartsWith('v') -or $v.StartsWith('V')) { $v = $v.Substring(1) }
    if ($v -notmatch '^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$') {
        Write-Err "Version must be SemVer-like (got $Raw)"
    }
    return $v
}

function Get-FileSha256Hex([string]$Path) {
    # Prefer .NET so restricted / minimal hosts without Microsoft.PowerShell.Utility
    # (Get-FileHash) still verify digests (observed on some GitHub Actions runners).
    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $sha = [System.Security.Cryptography.SHA256]::Create()
        try {
            $hash = $sha.ComputeHash($stream)
            return ([System.BitConverter]::ToString($hash) -replace '-', '').ToLowerInvariant()
        } finally {
            $sha.Dispose()
        }
    } finally {
        $stream.Dispose()
    }
}

function Read-ExpectedDigest {
    param(
        [string]$SidecarPath,
        [string]$ZipBaseName
    )
    if (-not (Test-Path -LiteralPath $SidecarPath -PathType Leaf)) {
        Write-Err "SHA-256 sidecar not found: $SidecarPath"
    }
    $raw = (Get-Content -LiteralPath $SidecarPath -Raw -Encoding utf8).Trim()
    if ($raw -notmatch '^([0-9a-fA-F]{64})[ \t]+(\S+)\s*$') {
        Write-Err "Invalid SHA-256 sidecar format (want '<hex>  <filename>'): $SidecarPath"
    }
    $hex = $Matches[1].ToLowerInvariant()
    $name = $Matches[2]
    $base = [System.IO.Path]::GetFileName($name)
    if ($base -ne $ZipBaseName) {
        Write-Err "Sidecar filename '$name' does not match zip basename '$ZipBaseName'"
    }
    return $hex
}

function Assert-DigestMatch {
    param(
        [string]$ZipFile,
        [string]$SidecarPath
    )
    $zipBase = [System.IO.Path]::GetFileName($ZipFile)
    $expected = Read-ExpectedDigest -SidecarPath $SidecarPath -ZipBaseName $zipBase
    $actual = Get-FileSha256Hex -Path $ZipFile
    if ($actual -ne $expected) {
        Write-Err "SHA-256 mismatch for $zipBase`n  expected: $expected`n  actual:   $actual"
    }
    Write-Host "SHA-256 OK: $zipBase"
}

function Resolve-FullPath([string]$Path, [string]$Base) {
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $Base $Path))
}

$norm = Normalize-Version $Version
if ($Channel -notin @('files', 'mcp')) {
    Write-Err "Channel must be 'files' or 'mcp' (got $Channel)"
}
$archiveRoot = "goal-governance-skills-v$norm"
$zipName = "$archiveRoot.zip"
$shaName = "$zipName.sha256"

if (-not $TargetDir) {
    $TargetDir = (Get-Location).Path
}
$TargetDir = [System.IO.Path]::GetFullPath($TargetDir)
if (-not (Test-Path -LiteralPath $TargetDir -PathType Container)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$workDir = Join-Path $TargetDir '.goal-governance-bootstrap-tmp'
if (Test-Path -LiteralPath $workDir) {
    Remove-Item -LiteralPath $workDir -Recurse -Force
}
New-Item -ItemType Directory -Path $workDir -Force | Out-Null

try {
    $localZip = $null
    $localSha = $null

    if ($ZipPath) {
        # Relative zip/sha paths resolve against process CWD (not TargetDir), so
        # pack-here\zip + -TargetDir empty-consumer works as documented.
        $cwd = (Get-Location).Path
        $localZip = Resolve-FullPath $ZipPath $cwd
        if (-not (Test-Path -LiteralPath $localZip -PathType Leaf)) {
            Write-Err "ZipPath not found: $localZip"
        }
        if ($Sha256Path) {
            $localSha = Resolve-FullPath $Sha256Path $cwd
        } else {
            $sibling = "$localZip.sha256"
            if (Test-Path -LiteralPath $sibling -PathType Leaf) {
                $localSha = $sibling
            } else {
                $beside = Join-Path (Split-Path -Parent $localZip) $shaName
                if (Test-Path -LiteralPath $beside -PathType Leaf) {
                    $localSha = $beside
                } else {
                    Write-Err "SHA-256 sidecar not found next to zip (pass -Sha256Path)"
                }
            }
        }
        Write-Host "Offline mode: using local zip $localZip"
    } else {
        $tag = if ($ReleaseTag) { $ReleaseTag } else { "v$norm" }
        $baseUrl = "https://github.com/$Repo/releases/download/$tag"
        $localZip = Join-Path $workDir $zipName
        $localSha = Join-Path $workDir $shaName
        Write-Host "Online mode: downloading $baseUrl/$zipName"
        try {
            Invoke-WebRequest -Uri "$baseUrl/$zipName" -OutFile $localZip -UseBasicParsing
            Invoke-WebRequest -Uri "$baseUrl/$shaName" -OutFile $localSha -UseBasicParsing
        } catch {
            Write-Err "Download failed: $_"
        }
    }

    Assert-DigestMatch -ZipFile $localZip -SidecarPath $localSha

    $extractDir = Join-Path $workDir 'extract'
    New-Item -ItemType Directory -Path $extractDir -Force | Out-Null
    Expand-Archive -LiteralPath $localZip -DestinationPath $extractDir -Force

    $packageSrc = Join-Path $extractDir $archiveRoot
    if (-not (Test-Path -LiteralPath $packageSrc -PathType Container)) {
        # Some extractors flatten or nest differently; accept single top-level dir.
        $children = @(Get-ChildItem -LiteralPath $extractDir -Directory)
        if ($children.Count -eq 1) {
            $packageSrc = $children[0].FullName
        } else {
            Write-Err "Expected archive root folder '$archiveRoot' under extract dir"
        }
    }

    $destSkills = Join-Path $TargetDir $SkillsDirName
    if (Test-Path -LiteralPath $destSkills) {
        if (-not $Force) {
            Write-Err "Destination already exists (use -Force to replace): $destSkills"
        }
        Remove-Item -LiteralPath $destSkills -Recurse -Force
    }

    if ($Channel -eq 'mcp') {
        # 薄 MCP 通道：仅 materialize skills/mcp + consumer contract，然后由
        # lifecycle CLI（单一真相源）写 AGENTS.md managed 段与薄壳状态。
        # 注：zip 归档根即 skills 包内容（mcp/、contracts/ 直接位于归档根）。
        $mcpSrc = Join-Path $packageSrc 'mcp'
        if (-not (Test-Path -LiteralPath (Join-Path $mcpSrc 'server.py') -PathType Leaf)) {
            Write-Err "Package missing mcp/server.py (MCP channel unavailable)"
        }
        Copy-Item -LiteralPath $mcpSrc -Destination (Join-Path $destSkills 'mcp') -Recurse -Force

        $contractsSrc = Join-Path $packageSrc 'contracts'
        $contractsDest = Join-Path $destSkills 'contracts'
        New-Item -ItemType Directory -Path $contractsDest -Force | Out-Null
        foreach ($name in @('skills-consumer-contract.json', 'skills-consumer-contract.schema.json')) {
            $src = Join-Path $contractsSrc $name
            if (-not (Test-Path -LiteralPath $src -PathType Leaf)) {
                Write-Err "Package missing $name (consumer contract required)"
            }
            Copy-Item -LiteralPath $src -Destination (Join-Path $contractsDest $name) -Force
        }

        # 复用 lifecycle 模块写 managed 段与状态（与 MCP server 同一真相源）。
        $lifecycleCli = Join-Path $destSkills 'mcp\lifecycle.py'
        $python = Get-Command python -ErrorAction SilentlyContinue
        if (-not $python) {
            Write-Err "MCP channel requires python on PATH (stdio runtime); use -Channel files for File-classic"
        }
        $lifecycleArgs = @(
            (Join-Path $destSkills 'mcp\lifecycle.py'), 'install',
            '--root', $TargetDir, '--version', $norm, '--channel', 'mcp', '--confirm'
        )
        & python @lifecycleArgs
        if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
            Write-Err "Thin-shell lifecycle install failed (exit $LASTEXITCODE)"
        }
        Write-Host 'MCP channel bootstrap complete.'
        Write-Host 'Note: the File channel remains a first-class release path and is NOT sunset; use -Channel files for the full File install (File-classic needs no Docker/MCP).'
        exit 0
    }

    # Copy package into place (preserve install scripts at package root)
    Copy-Item -LiteralPath $packageSrc -Destination $destSkills -Recurse -Force
    Write-Host "Materialized skills package: $destSkills"

    $installPs1 = Join-Path $destSkills 'install.ps1'
    if (-not (Test-Path -LiteralPath $installPs1 -PathType Leaf)) {
        Write-Err "Package install.ps1 missing after extract: $installPs1"
    }

    if ($SkipInstall) {
        Write-Host 'SkipInstall: package extracted; package install not run.'
        exit 0
    }

    # Invoke package install with the *same* host process image (pwsh or
    # Windows PowerShell). Hardcoding "powershell" fails on Linux pwsh-only hosts.
    $hostExe = (Get-Process -Id $PID).Path
    $installArgs = @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-File', $installPs1,
        '-All',
        '-NonInteractive',
        '-SkillsDir', $destSkills
    )
    if ($Force) {
        $installArgs += '-Force'
    }

    Write-Host "Running package install: install.ps1 -All -NonInteractive$(if ($Force) { ' -Force' } else { '' })"
    Push-Location $TargetDir
    try {
        & $hostExe @installArgs
        if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
            Write-Err "Package install failed with exit code $LASTEXITCODE"
        }
    } finally {
        Pop-Location
    }

    Write-Host 'Bootstrap complete.'
    exit 0
} finally {
    if (Test-Path -LiteralPath $workDir) {
        Remove-Item -LiteralPath $workDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
